from datetime import date, datetime, timedelta
import json
import os
from typing import Dict, List, Tuple
import tbaapiv3client
import yaml
import statbotics



class FRC_PY:
    def __init__(self):
        config = yaml.load(open('config.yml'), yaml.Loader)
        configuration = tbaapiv3client.Configuration(
            api_key = {
                'X-TBA-Auth-Key': config['api-key']
            }
        )
        self.__client = tbaapiv3client.ApiClient(configuration)
        self.__tba_cache = config['tba-cache']
        self.__statbotics_cache = config['statbotics-cache']
        self.__cache_expiry = config['cache-expiry']

    def _save(self, path: str, filename: str, data) -> None:
        data = {'datetime': datetime.utcnow().isoformat(), 'data': data}
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(os.path.join(path, filename), 'w')
        json.dump(data, f)
        f.close()

    def _load(self, path: str, filename: str) -> Tuple[datetime, Dict] | None:
        try:
            if not os.path.exists(path):
                return None
            f = open(os.path.join(path, filename), 'r')
            raw_data = json.load(f)
            date_time = datetime.strptime(raw_data['datetime'], '%Y-%m-%dT%H:%M:%S.%f')
            data = raw_data['data']
            f.close()
            return date_time, data
        except:
            return None

    def _event_key_to_year(self, event: str) -> int:
        return int(event[:4])

    def _team_key_to_number(self, team: str) -> int:
        return int(team[3:])

    def get_team_index(self) -> List:
        raw_data = self._load(os.path.join(self.__tba_cache, 'teams'), 'index.json')
        if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=280): # TODO
            teams = []
            page = 0
            while(True):
                teams_page = tbaapiv3client.TeamApi(self.__client).get_teams_keys(page)
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
        if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=280): # TODO
            years = tbaapiv3client.TeamApi(self.__client).get_team_years_participated(team)
            self._save(os.path.join(self.__tba_cache, 'teams', team), 'participation.json', years)
            return years
        return raw_data[1]

    def __team_simple(self, team: str) -> tbaapiv3client.TeamSimple:
        simple = tbaapiv3client.TeamApi(self.__client).get_team_simple(team)
        location = simple.city, simple.state_prov, simple.country
        nickname = simple.nickname
        name = simple.name
        data = {'location': location, 'nickname': nickname, 'name': name}
        self._save(os.path.join(self.__tba_cache, 'teams', team), 'simple.json', data)
        return data

    def get_team_location(self, team: str) -> Tuple[str, str, str]:
        raw_data = self._load(os.path.join(self.__tba_cache, 'teams', team), 'simple.json')
        if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=280): # TODO
            return self.__team_simple(team)['location']
        return raw_data[1]['location']

    def get_team_nickname(self, team: str) -> str:
        raw_data = self._load(os.path.join(self.__tba_cache, 'teams', team), 'simple.json')
        if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=280): # TODO
            return self.__team_simple(team)['nickname']
        return raw_data[1]['nickname']

    def get_team_name(self, team: str) -> str:
        raw_data = self._load(os.path.join(self.__tba_cache, 'teams', team), 'simple.json')
        if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=280): # TODO
            return self.__team_simple(team)['name']
        return raw_data[1]['name']

    def _save_simple_event(self, event: str, year: int, simple: tbaapiv3client.EventSimple) -> Dict:
        name = simple.name
        event_type = simple.event_type
        location = simple.city, simple.state_prov, simple.country
        dates = simple.start_date.isoformat(), simple.end_date.isoformat()
        if simple.district is None:
            district = None
        else:
            district = simple.district.key
        data = {'name': name, 'event_type': event_type, 'location': location, 'dates': dates, 'district': district}
        self._save(os.path.join(self.__tba_cache, 'events', str(year), event), 'simple.json', data)

    def get_team_events_year(self, team: str, year: int) -> List[str] | None:
        raw_data = self._load(os.path.join(self.__tba_cache, 'teams', team, str(year)), 'events.json')
        if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=280): # TODO
            events = []
            try:
                api_events = tbaapiv3client.TeamApi(self.__client).get_team_events_by_year_simple(team, year)
                for simple in api_events:
                    events.append(simple.key)
                    self._save_simple_event(simple.key, self.__event_key_to_year(simple.key), simple)
                self._save(os.path.join(self.__tba_cache, 'teams', team, str(year)), 'events.json', events)
                return events
            except ValueError as e:
                return None
            except BaseException as e:
                return None
        return raw_data[1]

    def __event_simple(self, event: str, year: int) -> Dict:
        simple = tbaapiv3client.EventApi(self.__client).get_event_simple(event)
        return self._save_simple_event(event, year, simple)

    def get_event_name(self, event: str) -> str:
        year = self.__event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'simple.json')
        if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=280): # TODO
            return self.__event_simple(event, year)['name']
        return raw_data[1]['name']

    def get_event_type(self, event: str) -> int:
        year = self.__event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'simple.json')
        if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=280): # TODO
            return self.__event_simple(event, year)['event_type']
        return raw_data[1]['event_type']

    def get_event_location(self, event: str) -> Tuple[str, str, str]:
        year = self.__event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'simple.json')
        if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=280): # TODO
            return self.__event_simple(event, year)['location']
        return raw_data[1]['location']

    def get_event_dates(self, event: str) -> Tuple[date, date]:
        year = self.__event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'simple.json')
        if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=280): # TODO
            start, end = self.__event_simple(event, year)['dates']
            start = date.fromisoformat(start)
            end = date.fromisoformat(end)
            return start, end
        start, end = raw_data[1]['dates']
        start = date.fromisoformat(start)
        end = date.fromisoformat(end)
        return start, end

    def get_event_district(self, event: str) -> str:
        year = self.__event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'simple.json')
        if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=280): 
            return self.__event_simple(event, year)['district']
        return raw_data[1]['district']

    def get_event_teams(self, event: str) -> List[str]:
        year = self._event_key_to_year(event)
        raw_data = self._load(os.path.join(self.__tba_cache, 'events', str(year), event), 'teams.json')
        if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=280):
            teams = []
            try:
                teams = tbaapiv3client.EventApi(self.__client).get_event_teams_keys(event)
                self._save(os.path.join(self.__tba_cache, 'events', str(year), event), 'teams.json', teams)
                return teams
            except ValueError as e:
                return []
            except BaseException as e:
                return []
        return raw_data[1]

    def get_team_year_stats(self, team: str, year: int) -> Dict:
        raw_data = self._load(os.path.join(self.__statbotics_cache, 'teams', team, str(year)), 'stats.json')
        if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=7): # TODO
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
                print(f"Error getting team stats for {team} in {year}: {e}")
                return {}
        return raw_data[1]
