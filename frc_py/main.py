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
        if cached and self.__cache.is_cached('teams', 'index'):
            teams = self.__cache.get('teams', 'index', cache_expiry)
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
        self.__cache.save('teams', 'index', teams)
        return teams

    def get_team_participation(self, team: str, cached: bool = True, cache_expiry: int = 90) -> list[int]:
        if cached and self.__cache.is_cached(os.path.join('teams', team), 'participation'):
            participation = self.__cache.get(os.path.join('teams', team), 'participation', cache_expiry)
            if participation is not None:
                return participation
        participation = self.__tba_client.team_years(team)
        self.__cache.save(os.path.join('teams', team), 'participation', participation)
        return participation
