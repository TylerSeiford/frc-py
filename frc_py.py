from datetime import date, datetime, timedelta
import json
import os
import shutil
from threading import Semaphore
from typing import Any
import tbapy
import statbotics



class FRCPY:
    def __init__(self, token: str,
            tba_cache: str = 'tba-cache',
            statbotics_cache: str = 'statbotics-cache',
            cache_expiry: dict[str, int] = {
                'team-index': 280, 'team-participation': 280, 'team-simple': 280, 'team-events-year': 280,
                'event-simple': 280, 'event-teams': 280, 'event-matches': 280, 'events-year': 280,
                'match-simple': 280,
                'team-year-stats': 7
            }) -> None:
        self.__tba_client = tbapy.TBA(token)
        self.__statbotics_client = statbotics.Statbotics()
        self.__tba_cache = tba_cache
        self.__statbotics_cache = statbotics_cache
        self.__cache_expiry = cache_expiry
        self.__dir_semaphore = Semaphore()

    def _save(self, path: str, filename: str, data) -> None:
        data = { 'datetime': datetime.utcnow().isoformat(), 'data': data }
        self.__dir_semaphore.acquire()
        if not os.path.exists(path):
            os.makedirs(path)
        self.__dir_semaphore.release()
        f = open(os.path.join(path, filename), 'w')
        json.dump(data, f)
        f.close()

    def _load(self, path: str, filename: str) -> tuple[datetime, dict] | BaseException:
        try:
            if not os.path.exists(path):
                return None
            f = open(os.path.join(path, filename), 'r')
            raw_data = json.load(f)
            date_time = datetime.strptime(raw_data['datetime'], '%Y-%m-%dT%H:%M:%S.%f')
            data = raw_data['data']
            f.close()
            return date_time, data
        except BaseException as e:
            return e

    def _version(self) -> tuple[int, int, int, str | None]:
        return 0, 1, 0, None

    def _tba_client(self) -> tbapy.TBA:
        return self.__tba_client

    def _stat_client(self) -> statbotics.Statbotics:
        return self.__statbotics_client

    def _team_key_to_number(self, team: str) -> int:
        return int(team[3:])

    def _event_key_to_year(self, event: str) -> int:
        return int(event[:4])

    def _match_key_to_year(self, match: str) -> int:
        return int(match[:4])

    def _match_key_to_event(self, match: str) -> str:
        return match.split('_')[0]

    def _purge_cache_team(self, team: str) -> None:
        self.__dir_semaphore.acquire()
        if os.path.exists(os.path.join(self.__tba_cache, 'teams', team)):
            shutil.rmtree(os.path.join(self.__tba_cache, 'teams', team), ignore_errors=True)
        if os.path.exists(os.path.join(self.__statbotics_cache, 'teams', team)):
            shutil.rmtree(os.path.join(self.__statbotics_cache, 'teams', team), ignore_errors=True)
        self.__dir_semaphore.release()

    def _purge_cache_event(self, event: str) -> None:
        year = self._event_key_to_year(event)
        self.__dir_semaphore.acquire()
        if os.path.exists(os.path.join(self.__tba_cache, 'events', str(year), event)):
            shutil.rmtree(os.path.join(self.__tba_cache, 'events', str(year), event), ignore_errors=True)
        self.__dir_semaphore.release()

    def _purge_cache_match(self, match: str) -> None:
        year = self._match_key_to_year(match)
        event = self._match_key_to_event(match)
        self.__dir_semaphore.acquire()
        if os.path.exists(os.path.join(self.__tba_cache, 'matches', str(year), event, match)):
            shutil.rmtree(os.path.join(self.__tba_cache, 'matches', str(year), event, match), ignore_errors=True)
        self.__dir_semaphore.release()

    def get_year_range(self) -> tuple[int, int]:
        status = self.__tba_client.status()
        return (1992, status['max_season'])

    def get_team_index(self) -> list:
        raw_data = self._load(os.path.join(self.__tba_cache, 'teams'), 'index.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['team-index']):
            teams = []
            page = 0
            while True:
                teams_page = self.__tba_client.teams(page=page, keys=True)
                if len(teams_page) == 0:
                    break
                for team in teams_page:
                    teams.append(team)
                page += 1
            self._save(os.path.join(self.__tba_cache, 'teams'), 'index.json', teams)
            return teams
        return raw_data[1]

    def get_team_participation(self, team: str) -> list[int]:
        raw_data = self._load(os.path.join(self.__tba_cache, 'teams', team), 'participation.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['team-participation']):
            years = self.__tba_client.team_years(team)
            self._save(os.path.join(self.__tba_cache, 'teams', team), 'participation.json', years)
            return years
        return raw_data[1]

    def __team_simple(self, team: str) -> dict[str, Any]:
        simple = self.__tba_client.team(team, simple=True)
        location = simple.city, simple.state_prov, simple.country
        nickname = simple.nickname
        name = simple.name
        data = {'location': location, 'nickname': nickname, 'name': name}
        self._save(os.path.join(self.__tba_cache, 'teams', team), 'simple.json', data)
        return data

    def get_team_location(self, team: str) -> tuple[str, str, str]:
        raw_data = self._load(os.path.join(self.__tba_cache, 'teams', team), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['team-simple']):
            return self.__team_simple(team)['location']
        return raw_data[1]['location']

    def get_team_nickname(self, team: str) -> str:
        raw_data = self._load(os.path.join(self.__tba_cache, 'teams', team), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['team-simple']):
            return self.__team_simple(team)['nickname']
        return raw_data[1]['nickname']

    def get_team_name(self, team: str) -> str:
        raw_data = self._load(os.path.join(self.__tba_cache, 'teams', team), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['team-simple']):
            return self.__team_simple(team)['name']
        return raw_data[1]['name']

    def get_team_events_year(self, team: str, year: int) -> list[str] | BaseException:
        raw_data = self._load(os.path.join(self.__tba_cache, 'teams', team, str(year)), 'events.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['team-events-year']):
            try:
                events = self.__tba_client.team_events(team, year=year, keys=True)
                self._save(os.path.join(self.__tba_cache, 'teams', team, str(year)), 'events.json', events)
                return events
            except BaseException as e:
                return e
        return raw_data[1]

    def get_events_year(self, year: int) -> list[str] | BaseException:
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year)), 'index.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['events-year']):
            try:
                events = self.__tba_client.events(year=year, keys=True)
                self._save(os.path.join(self.__tba_cache, 'events', str(year)), 'index.json', events)
                return events
            except BaseException as e:
                return e
        return raw_data[1]

    def __save_simple_event(self, event: str, year: int, simple: Any) -> dict:
        name = simple.name
        event_type = simple.event_type
        location = simple.city, simple.state_prov, simple.country
        dates = simple.start_date, simple.end_date
        if simple.district is None:
            district = None
        else:
            district = simple.district['key']
        data = {'name': name, 'event_type': event_type, 'location': location, 'dates': dates, 'district': district}
        self._save(os.path.join(self.__tba_cache, 'events', str(year), event), 'simple.json', data)
        return data

    def __event_simple(self, event: str, year: int) -> dict:
        simple = self.__tba_client.event(event, simple=True)
        return self.__save_simple_event(event, year, simple)

    def get_event_name(self, event: str) -> str:
        year = self._event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['event-simple']):
            return self.__event_simple(event, year)['name']
        return raw_data[1]['name']

    def get_event_type(self, event: str) -> int:
        year = self._event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['event-simple']):
            return self.__event_simple(event, year)['event_type']
        return raw_data[1]['event_type']

    def get_event_location(self, event: str) -> tuple[str, str, str]:
        year = self._event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['event-simple']):
            return self.__event_simple(event, year)['location']
        return raw_data[1]['location']

    def get_event_dates(self, event: str) -> tuple[date, date]:
        year = self._event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['event-simple']):
            start, end = self.__event_simple(event, year)['dates']
            start = date.fromisoformat(start)
            end = date.fromisoformat(end)
            return start, end
        start, end = raw_data[1]['dates']
        start = date.fromisoformat(start)
        end = date.fromisoformat(end)
        return start, end

    def get_event_district(self, event: str) -> str:
        year = self._event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['event-simple']): 
            return self.__event_simple(event, year)['district']
        return raw_data[1]['district']

    def get_event_teams(self, event: str) -> list[str] | BaseException:
        year = self._event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'teams.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['event-teams']):
            teams = []
            try:
                teams = self.__tba_client.event_teams(event, keys=True)
                self._save(os.path.join(self.__tba_cache, 'events', str(year), event), 'teams.json', teams)
                return teams
            except BaseException as e:
                return e
        return raw_data[1]

    def get_event_matches(self, event: str) -> list[str] | BaseException:
        year = self._event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'matches.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['event-matches']):
            matches = []
            try:
                matches = self.__tba_client.event_matches(event, keys=True)
                self._save(os.path.join(self.__tba_cache, 'events', str(year), event), 'matches.json', matches)
                return matches
            except BaseException as e:
                return e
        return raw_data[1]

    def __save_simple_match(self, event: str, year: int, match: str, simple: Any) -> dict:
        level = simple.comp_level
        set_number = simple.set_number
        match_number = simple.match_number
        red_score = simple.alliances['red']['score']
        blue_score = simple.alliances['blue']['score']
        red_teams = {
            'team_keys': simple.alliances['red']['team_keys'],
            'dq': simple.alliances['red']['dq_team_keys'],
            'surrogate': simple.alliances['red']['surrogate_team_keys']
        }
        blue_teams = {
            'team_keys': simple.alliances['blue']['team_keys'],
            'dq': simple.alliances['blue']['dq_team_keys'],
            'surrogate': simple.alliances['blue']['surrogate_team_keys']
        }
        winner = simple.winning_alliance
        if winner == 'red':
            if red_score < blue_score:
                raise ValueError('Red alliance won but red score is less than blue score')
            elif red_score == blue_score:
                raise ValueError('Red alliance won but red score is equal to blue score')
            else:
                pass
        elif winner == 'blue':
            if blue_score < red_score:
                raise ValueError('Blue alliance won but blue score is less than red score')
            elif blue_score == red_score:
                raise ValueError('Blue alliance won but blue score is equal to red score')
            else:
                pass
        else:
            if red_score > blue_score:
                pass
            elif red_score < blue_score:
                pass
            else:
                winner = 'tie'
        time = simple.time
        data = {
            'level': level,
            'set_number': set_number,
            'match_number': match_number,
            'winner': winner,
            'red-score': red_score,
            'blue-score': blue_score,
            'red-teams': red_teams,
            'blue-teams': blue_teams,
            'time': time
        }
        self._save(os.path.join(self.__tba_cache, 'matches', str(year), event, match), 'simple.json', data)
        return data

    def __match_simple(self, year: int, event: str, match: str) -> dict:
        raw_data = self._load(os.path.join(self.__tba_cache, 'matches', str(year), event, match), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['match-simple']):
            try:
                simple = self.__tba_client.match(match, simple=True)
                return self.__save_simple_match(event, year, match, simple)
            except BaseException as e:
                return e
        return raw_data[1]

    def get_match_winner(self, match: str) -> str:
        year = self._match_key_to_year(match)
        event = self._match_key_to_event(match)
        raw_data = self._load(os.path.join(self.__tba_cache, 'matches', str(year), event, match), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['match-simple']):
            return self.__match_simple(year, event, match)['winner']
        return raw_data[1]['winner']

    def get_match_red_score(self, match: str) -> int:
        year = self._match_key_to_year(match)
        event = self._match_key_to_event(match)
        raw_data = self._load(os.path.join(self.__tba_cache, 'matches', str(year), event, match), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['match-simple']):
            return self.__match_simple(year, event, match)['red-score']
        return raw_data[1]['red-score']

    def get_match_blue_score(self, match: str) -> int:
        year = self._match_key_to_year(match)
        event = self._match_key_to_event(match)
        raw_data = self._load(os.path.join(self.__tba_cache, 'matches', str(year), event, match), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['match-simple']):
            return self.__match_simple(year, event, match)['blue-score']
        return raw_data[1]['blue-score']

    def get_match_red_teams(self, match: str) -> list:
        year = self._match_key_to_year(match)
        event = self._match_key_to_event(match)
        raw_data = self._load(os.path.join(self.__tba_cache, 'matches', str(year), event, match), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['match-simple']):
            return self.__match_simple(year, event, match)['red-teams']
        return raw_data[1]['red-teams']['team_keys']

    def get_match_blue_teams(self, match: str) -> list:
        year = self._match_key_to_year(match)
        event = self._match_key_to_event(match)
        raw_data = self._load(os.path.join(self.__tba_cache, 'matches', str(year), event, match), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['match-simple']):
            return self.__match_simple(year, event, match)['blue-teams']
        return raw_data[1]['blue-teams']['team_keys']

    def get_team_year_stats(self, team: str, year: int) -> dict | BaseException:
        raw_data = self._load(os.path.join(self.__statbotics_cache, 'teams', team, str(year)), 'stats.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['team-year-stats']):
            try:
                api_stats = self.__statbotics_client.get_team_year(self._team_key_to_number(team), year)
                elo = {
                    'start': api_stats['elo_start'],
                    'pre_champs': api_stats['elo_pre_champs'],
                    'end': api_stats['elo_end'],
                    'mean': api_stats['elo_mean'],
                    'max': api_stats['elo_max'],
                    'diff': api_stats['elo_diff'],
                    'rank': api_stats['elo_rank'],
                    'percentile': api_stats['elo_percentile']
                }
                opr = {
                    'opr' : api_stats['opr'],
                    'opr_auto' : api_stats['opr_auto'],
                    'opr_teleop' : api_stats['opr_teleop'],
                    'opr_1' : api_stats['opr_1'],
                    'opr_2' : api_stats['opr_2'],
                    'opr_endgame' : api_stats['opr_endgame'],
                    'opr_fouls' : api_stats['opr_fouls'],
                    'opr_no_fouls' : api_stats['opr_no_fouls'],
                    'rank' : api_stats['opr_rank'],
                    'percentile' : api_stats['opr_percentile']
                }
                ils = {
                    'ils_1' : api_stats['ils_1'],
                    'ils_2' : api_stats['ils_2']
                }
                record = {
                    'wins': api_stats['wins'],
                    'losses': api_stats['losses'],
                    'ties': api_stats['ties'],
                    'count': api_stats['count'],
                    'winrate': api_stats['winrate']
                }
                stats = {
                    'elo': elo,
                    'opr': opr,
                    'ils': ils,
                    'record': record
                }
                self._save(os.path.join(self.__statbotics_cache, 'teams', team, str(year)), 'stats.json', stats)
                return stats
            except BaseException as e:
                return e
        return raw_data[1]


