from datetime import date, datetime, timedelta
import json
import os
import shutil
from typing import Any, Dict, List, Tuple
import tbapy
import statbotics



class FRCPY:
    def __init__(self, token: str,
            tba_cache: str = 'tba-cache',
            statbotics_cache: str = 'statbotics-cache',
            cache_expiry: Dict[str, int] = {
                'team-index': 280, 'team-participation': 280, 'team-simple': 280, 'team-events-year': 280,
                'event-simple': 280, 'event-teams': 280, 'team-year-stats': 7
            }) -> None:
        self.__client = tbapy.TBA(token)
        self.__tba_cache = tba_cache
        self.__statbotics_cache = statbotics_cache
        self.__cache_expiry = cache_expiry

    def _save(self, path: str, filename: str, data) -> None:
        data = {'datetime': datetime.utcnow().isoformat(), 'data': data}
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(os.path.join(path, filename), 'w')
        json.dump(data, f)
        f.close()

    def _load(self, path: str, filename: str) -> Tuple[datetime, Dict] | BaseException:
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

    def _event_key_to_year(self, event: str) -> int:
        return int(event[:4])

    def _team_key_to_number(self, team: str) -> int:
        return int(team[3:])

    def _purge_cache_team(self, team: str) -> None:
        if os.path.exists(os.path.join(self.__tba_cache, 'teams', team)):
            shutil.rmtree(os.path.join(self.__tba_cache, 'teams', team), ignore_errors=True)
        if os.path.exists(os.path.join(self.__statbotics_cache, 'teams', team)):
            shutil.rmtree(os.path.join(self.__statbotics_cache, 'teams', team), ignore_errors=True)

    def _purge_cache_event(self, event: str) -> None:
        year = self._event_key_to_year(event)
        if os.path.exists(os.path.join(self.__tba_cache, 'events', str(year), event)):
            shutil.rmtree(os.path.join(self.__tba_cache, 'events', str(year), event), ignore_errors=True)

    def get_team_index(self) -> List:
        raw_data = self._load(os.path.join(self.__tba_cache, 'teams'), 'index.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['team-index']):
            teams = []
            page = 0
            while True:
                teams_page = self.__client.teams(page=page, keys=True)
                if len(teams_page) == 0:
                    break
                for team in teams_page:
                    teams.append(team)
                page += 1
            self._save(os.path.join(self.__tba_cache, 'teams'), 'index.json', teams)
            return teams
        return raw_data[1]

    def get_team_participation(self, team: str) -> List[int]:
        raw_data = self._load(os.path.join(self.__tba_cache, 'teams', team), 'participation.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['team-participation']):
            years = self.__client.team_years(team)
            self._save(os.path.join(self.__tba_cache, 'teams', team), 'participation.json', years)
            return years
        return raw_data[1]

    def __team_simple(self, team: str) -> Dict[str, Any]:
        simple = self.__client.team(team, simple=True)
        location = simple.city, simple.state_prov, simple.country
        nickname = simple.nickname
        name = simple.name
        data = {'location': location, 'nickname': nickname, 'name': name}
        self._save(os.path.join(self.__tba_cache, 'teams', team), 'simple.json', data)
        return data

    def get_team_location(self, team: str) -> Tuple[str, str, str]:
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

    def get_team_events_year(self, team: str, year: int) -> List[str] | BaseException:
        raw_data = self._load(os.path.join(self.__tba_cache, 'teams', team, str(year)), 'events.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['team-events-year']):
            try:
                events = self.__client.team_events(team, year=year, keys=True)
                self._save(os.path.join(self.__tba_cache, 'teams', team, str(year)), 'events.json', events)
                return events
            except BaseException as e:
                return e
        return raw_data[1]

    def __save_simple_event(self, event: str, year: int, simple: Any) -> Dict:
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

    def __event_simple(self, event: str, year: int) -> Dict:
        simple = self.__client.event(event, simple=True)
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

    def get_event_location(self, event: str) -> Tuple[str, str, str]:
        year = self._event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'simple.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['event_simple']):
            return self.__event_simple(event, year)['location']
        return raw_data[1]['location']

    def get_event_dates(self, event: str) -> Tuple[date, date]:
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

    def get_event_teams(self, event: str) -> List[str] | BaseException:
        year = self._event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'teams.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['event-teams']):
            teams = []
            try:
                teams = self.__client.event_teams(event, keys=True)
                self._save(os.path.join(self.__tba_cache, 'events', str(year), event), 'teams.json', teams)
                return teams
            except BaseException as e:
                return e
        return raw_data[1]

    def get_team_year_stats(self, team: str, year: int) -> Dict | BaseException:
        raw_data = self._load(os.path.join(self.__statbotics_cache, 'teams', team, str(year)), 'stats.json')
        if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=self.__cache_expiry['team-year-stats']):
            try:
                api_stats = statbotics.Statbotics().get_team_year(self._team_key_to_number(team), year)
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


