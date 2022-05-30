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

    def get_team_index(self, cached: bool = True, cache_expiry: int = 90) -> list:
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
        self.__cache.save('teams', 'index_tba', teams)
        return teams

    def get_team_participation(self, team: str, cached: bool = True, cache_expiry: int = 90) -> list[int]:
        if cached and self.__cache.is_cached(os.path.join('teams', team), 'participation_tba'):
            participation = self.__cache.get(os.path.join('teams', team), 'participation_tba', cache_expiry)
            if participation is not None:
                return participation
        participation = self.__tba_client.team_years(team)
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
        self.__cache.save(os.path.join('teams', team, str(year)), 'events_tba', events)
        return events
