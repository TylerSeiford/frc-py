from datetime import date
import os
import tbapy
import statbotics
from .cache import Cache

class FRC_PY:
    @staticmethod
    def _team_key_to_number(team: str) -> int:
        return int(team[3:])

    @staticmethod
    def _event_key_to_year(event: str) -> int:
        return int(event[:4])

    @staticmethod
    def _match_key_to_year(match: str) -> int:
        return int(match[:4])

    @staticmethod
    def _match_key_to_event(match: str) -> str:
        return match.split('_')[0]

    @staticmethod
    def event_type_to_str(event_type: int) -> str:
        match(event_type):
            case 0:
                return 'Regional'
            case 1:
                return 'District'
            case 2:
                return 'District Championship'
            case 3:
                return 'Championship Division'
            case 4:
                return 'Einstein'
            case 5:
                return 'District Championship Division'
            case 6:
                return 'Festival of Champions'
            case 7:
                return 'Remote'
            case 99:
                return 'Offseason'
            case 100:
                return 'Preseason'
            case _:
                return 'Unknown'

    @staticmethod
    def is_event_type_district(event_type: int) -> bool:
        return FRC_PY.event_type_to_str(event_type) in [
            'District',
            'District Championship',
            'District Championship Division'
        ]

    @staticmethod
    def is_event_type_non_championship(event_type: int) -> bool:
        return FRC_PY.event_type_to_str(event_type) in [
            'Regional',
            'District',
            'District Championship',
            'District Championship Division',
            'Remote'
        ]

    @staticmethod
    def is_event_type_championship(event_type: int) -> bool:
        return FRC_PY.event_type_to_str(event_type) in [
            'Championship Division',
            'Einstein'
        ]

    @staticmethod
    def is_event_type_season(event_type: int) -> bool:
        return FRC_PY.event_type_to_str(event_type) in [
            'Regional',
            'District',
            'District Championship',
            'District Championship Division',
            'Championship Division',
            'Einstein',
            'Festival of Champions',
            'Remote'
        ]


    def __init__(self, tba_token: str):
        self.__tba_client = tbapy.TBA(tba_token)
        self.__statbotics_client = statbotics.Statbotics()
        self.__cache = Cache()

    def _tba_client(self) -> tbapy.TBA:
        return self.__tba_client

    def _stat_client(self) -> statbotics.Statbotics:
        return self.__statbotics_client

    def get_year_range(self) -> tuple[int, int]:
        status = self.__tba_client.status()
        return (1992, status['max_season'])

    def get_teams(self, cached: bool = True, cache_expiry: int = 90) -> list:
        if cached and self.__cache.is_cached('teams', 'index_tba'):
            teams = self.__cache.get('teams', 'index_tba', cache_expiry)
            if teams is not None:
                return teams
        teams = []
        page = 0
        while True:
            teams_page = self.__tba_client.teams(page=page, keys=True)
            if len(teams_page) == 0:
                break
            for team in teams_page:
                teams.append(team)
            page += 1
        if cached:
            self.__cache.save('teams', 'index_tba', teams)
        return teams

    def get_team_participation(self, team: str, cached: bool = True, cache_expiry: int = 90) -> list[int]:
        if cached and self.__cache.is_cached(os.path.join('teams', team), 'participation_tba'):
            participation = self.__cache.get(os.path.join('teams', team), 'participation_tba', cache_expiry)
            if participation is not None:
                return participation
        participation = self.__tba_client.team_years(team)
        if cached:
            self.__cache.save(os.path.join('teams', team), 'participation_tba', participation)
        return participation

    def __team_simple(self, team: str, cached: bool = True, cache_expiry: int = 90) -> dict[str, any]:
        if cached and self.__cache.is_cached(os.path.join('teams', team), 'simple_tba'):
            simple = self.__cache.get(os.path.join('teams', team), 'simple_tba', cache_expiry)
            if simple is not None:
                return simple
        simple = self.__tba_client.team(team, simple=True)
        data = {
            'location': (simple.city, simple.state_prov, simple.country),
            'nickname': simple.nickname,
            'name': simple.name
        }
        if cached:
            self.__cache.save(os.path.join('teams', team), 'simple_tba', data)
        return data

    def get_team_location(self, team: str, cached: bool = True, cache_expiry: int = 90) -> tuple[str, str, str]:
        return self.__team_simple(team, cached, cache_expiry)['location']

    def get_team_nickname(self, team: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__team_simple(team, cached, cache_expiry)['nickname']

    def get_team_name(self, team: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__team_simple(team, cached, cache_expiry)['name']

    def __team(self, team: str, cached: bool = True, cache_expiry: int = 90) -> dict[str, any]:
        if cached and self.__cache.is_cached(os.path.join('teams', team), 'full_tba'):
            data = self.__cache.get(os.path.join('teams', team), 'full_tba', cache_expiry)
            if data is not None:
                return data
        api_data = self.__tba_client.team(team)
        data = {
            'school_name': api_data.school_name,
            'website': api_data.website,
            'rookie_year': api_data.rookie_year,
            'motto': api_data.motto,
            # 'home_championships': api_data.home_championship
            # Documented in the TBA API docs, but not implemented in tbapy?
        }
        if cached:
            self.__cache.save(os.path.join('teams', team), 'full_tba', data)
        return data

    def get_team_school(self, team: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__team(team, cached, cache_expiry)['school_name']

    def get_team_website(self, team: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__team(team, cached, cache_expiry)['website']

    def get_team_rookie_year(self, team: str, cached: bool = True, cache_expiry: int = 90) -> int:
        return self.__team(team, cached, cache_expiry)['rookie_year']

    def get_team_motto(self, team: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__team(team, cached, cache_expiry)['motto']

    def get_team_events_year(self, team: str, year: int, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        if cached and self.__cache.is_cached(os.path.join('teams', team, str(year)), 'events_tba'):
            events = self.__cache.get(os.path.join('teams', team, str(year)), 'events_tba', cache_expiry)
            if events is not None:
                return events
        events = self.__tba_client.team_events(team, year, keys=True)
        if cached:
            self.__cache.save(os.path.join('teams', team, str(year)), 'events_tba', events)
        return events

    def get_events_year(self, year: int, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        if cached and self.__cache.is_cached(os.path.join('events', str(year)), 'events_tba'):
            events = self.__cache.get(os.path.join('events', str(year)), 'events_tba', cache_expiry)
            if events is not None:
                return events
        events = self.__tba_client.events(year, keys=True)
        if cached:
            self.__cache.save(os.path.join('events', str(year)), 'events_tba', events)
        return events

    def __event_simple(self, event: str, cached: bool = True, cache_expiry: int = 90) -> dict[str, any]:
        year = FRC_PY._event_key_to_year(event)
        if cached and self.__cache.is_cached(os.path.join('events', str(year), event), 'simple_tba'):
            simple = self.__cache.get(os.path.join('events', str(year), event), 'simple_tba', cache_expiry)
            if simple is not None:
                return simple
        simple = self.__tba_client.event(event, simple=True)
        data = {
            'name': simple.name,
            'location': (simple.city, simple.state_prov, simple.country),
            'type': simple.event_type,
            'dates': (simple.start_date, simple.end_date),
            'district': simple.district
        }
        if cached:
            self.__cache.save(os.path.join('events', str(year), event), 'simple_tba', data)
        return data

    def get_event_name(self, event: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__event_simple(event, cached, cache_expiry)['name']

    def get_event_location(self, event: str, cached: bool = True, cache_expiry: int = 90) -> tuple[str, str, str]:
        return self.__event_simple(event, cached, cache_expiry)['location']

    def get_event_type(self, event: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__event_simple(event, cached, cache_expiry)['type']

    def get_event_dates(self, event: str, cached: bool = True, cache_expiry: int = 90) -> tuple[str, str]:
        start, end = self.__event_simple(event, cached, cache_expiry)['dates']
        return date.fromisoformat(start), date.fromisoformat(end)

    def get_event_district(self, event: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__event_simple(event, cached, cache_expiry)['district']

    def get_event_teams(self, event: str, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        year = FRC_PY._event_key_to_year(event)
        if cached and self.__cache.is_cached(os.path.join('events', str(year), event), 'teams_tba'):
            teams = self.__cache.get(os.path.join('events', str(year), event), 'teams_tba', cache_expiry)
            if teams is not None:
                return teams
        teams = self.__tba_client.event_teams(event, keys=True)
        if cached:
            self.__cache.save(os.path.join('events', str(year), event), 'teams_tba', teams)
        return teams

    def get_event_matches(self, event: str, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        year = FRC_PY._event_key_to_year(event)
        if cached and self.__cache.is_cached(os.path.join('events', str(year), event), 'matches_tba'):
            matches = self.__cache.get(os.path.join('events', str(year), event), 'matches_tba', cache_expiry)
            if matches is not None:
                return matches
        matches = self.__tba_client.event_matches(event, keys=True)
        if cached:
            self.__cache.save(os.path.join('events', str(year), event), 'matches_tba', matches)
        return matches
