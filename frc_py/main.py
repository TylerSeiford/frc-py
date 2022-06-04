from datetime import date, datetime
import tbapy
import statbotics
from .models import EventSimple, TeamSimple, Team, MatchSimple
from .cache import Cache

class FRC_PY:
    @staticmethod
    def team_key_to_number(team: str) -> int:
        return int(team[3:])

    @staticmethod
    def event_key_to_year(event: str) -> int:
        return int(event[:4])

    @staticmethod
    def match_key_to_year(match: str) -> int:
        return int(match[:4])

    @staticmethod
    def match_key_to_event(match: str) -> str:
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

    @staticmethod
    def __validate_winner(winner: str, red_score: int, blue_score: int) -> str:
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
                winner = 'tie' # TBA does not give us a tie
        return winner


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
        if cached and self.__cache.is_cached(['teams'], 'index_tba'):
            teams = self.__cache.get(['teams'], 'index_tba', cache_expiry)
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
            self.__cache.save(['teams'], 'index_tba', teams)
        return teams

    def get_team_participation(self, team: str, cached: bool = True, cache_expiry: int = 90) -> list[int]:
        if cached and self.__cache.is_cached(['teams', team], 'participation_tba'):
            participation = self.__cache.get(['teams', team], 'participation_tba', cache_expiry)
            if participation is not None:
                return participation
        participation = self.__tba_client.team_years(team)
        if cached:
            self.__cache.save(['teams', team], 'participation_tba', participation)
        return participation

    def __team_simple(self, key: str, cached: bool = True, cache_expiry: int = 90) -> TeamSimple:
        if cached:
            team = self.__cache.get_team_simple(key, cache_expiry)
            if team is not None:
                return team
        simple = self.__tba_client.team(key, simple=True)
        team = TeamSimple(
            key,
            simple.nickname,
            simple.name,
            (simple.city, simple.state_prov, simple.country)
        )
        if cached:
            self.__cache.save_team_simple(team)
        return team

    def get_team_location(self, team: str, cached: bool = True, cache_expiry: int = 90) -> tuple[str, str, str]:
        return self.__team_simple(team, cached, cache_expiry).get_location()

    def get_team_nickname(self, team: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__team_simple(team, cached, cache_expiry).get_nickname()

    def get_team_name(self, team: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__team_simple(team, cached, cache_expiry).get_name()

    def __team(self, key: str, cached: bool = True, cache_expiry: int = 90) -> Team:
        if cached:
            team = self.__cache.get_team(key, cache_expiry)
            if team is not None:
                return team
        api_data = self.__tba_client.team(key)
        team = Team(
            key,
            api_data.school_name,
            api_data.website,
            api_data.rookie_year,
            api_data.motto
        )
        if cached:
            self.__cache.save_team(team)
        return team

    def get_team_school(self, team: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__team(team, cached, cache_expiry).get_school_name()

    def get_team_website(self, team: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__team(team, cached, cache_expiry).get_website()

    def get_team_rookie_year(self, team: str, cached: bool = True, cache_expiry: int = 90) -> int:
        return self.__team(team, cached, cache_expiry).get_rookie_year()

    def get_team_motto(self, team: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__team(team, cached, cache_expiry).get_motto()

    def get_team_events_year(self, team: str, year: int, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        if cached and self.__cache.is_cached(['teams', team, str(year)], 'events_tba'):
            events = self.__cache.get(['teams', team, str(year)], 'events_tba', cache_expiry)
            if events is not None:
                return events
        events = self.__tba_client.team_events(team, year, keys=True)
        if cached:
            self.__cache.save(['teams', team, str(year)], 'events_tba', events)
        return events

    def get_events_year(self, year: int, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        if cached and self.__cache.is_cached(['events', str(year)], 'events_tba'):
            events = self.__cache.get(['events', str(year)], 'events_tba', cache_expiry)
            if events is not None:
                return events
        events = self.__tba_client.events(year, keys=True)
        if cached:
            self.__cache.save(['events', str(year)], 'events_tba', events)
        return events

    def __event_simple(self, key: str, cached: bool = True, cache_expiry: int = 90) -> dict[str, any]:
        if cached:
            event = self.__cache.get_event_simple(key, cache_expiry)
            if event is not None:
                return event
        event = self.__tba_client.event(key, simple=True)
        district = event.district
        if district is not None:
            district = district['key']
        event = EventSimple(
            key, event.name,
            (event.city, event.state_prov, event.country),
            event.event_type,
            (event.start_date, event.end_date),
            district
        )
        if cached:
            self.__cache.save_event_simple(event)
        return event

    def get_event_name(self, event: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__event_simple(event, cached, cache_expiry).get_name()

    def get_event_location(self, event: str, cached: bool = True, cache_expiry: int = 90) -> tuple[str, str, str]:
        return self.__event_simple(event, cached, cache_expiry).get_location()

    def get_event_type(self, event: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__event_simple(event, cached, cache_expiry).get_type()

    def get_event_dates(self, event: str, cached: bool = True, cache_expiry: int = 90) -> tuple[str, str]:
        start, end = self.__event_simple(event, cached, cache_expiry).get_dates()
        return date.fromisoformat(start), date.fromisoformat(end)

    def get_event_district(self, event: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__event_simple(event, cached, cache_expiry).get_district_key()

    def get_event_teams(self, event: str, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        year = FRC_PY.event_key_to_year(event)
        if cached and self.__cache.is_cached(['events', str(year), event], 'teams_tba'):
            teams = self.__cache.get(['events', str(year), event], 'teams_tba', cache_expiry)
            if teams is not None:
                return teams
        teams = self.__tba_client.event_teams(event, keys=True)
        if cached:
            self.__cache.save(['events', str(year), event], 'teams_tba', teams)
        return teams

    def get_event_matches(self, event: str, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        year = FRC_PY.event_key_to_year(event)
        if cached and self.__cache.is_cached(['events', str(year), event], 'matches_tba'):
            matches = self.__cache.get(['events', str(year), event], 'matches_tba', cache_expiry)
            if matches is not None:
                return matches
        matches = self.__tba_client.event_matches(event, keys=True)
        if cached:
            self.__cache.save(['events', str(year), event], 'matches_tba', matches)
        return matches

    def get_team_event_matches(self, team: str, event: str, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        year = FRC_PY.event_key_to_year(event)
        if cached and self.__cache.is_cached(['teams', team, str(year), event], 'matches_tba'):
            matches = self.__cache.get(['teams', team, str(year), event], 'matches_tba', cache_expiry)
            if matches is not None:
                return matches
        matches = self.__tba_client.team_matches(team, event, keys=True)
        if cached:
            self.__cache.save(['teams', team, str(year), event], 'matches_tba', matches)
        return matches

    def __match_simple(self, key: str, cached: bool = True, cache_expiry: int = 90) -> dict[str, any]:
        if cached:
            simple = self.__cache.get_match_simple(key, cache_expiry)
            if simple is not None:
                return simple
        simple = self.__tba_client.match(key, simple=True)
        red_score = simple.alliances['red']['score']
        blue_score = simple.alliances['blue']['score']
        winner = FRC_PY.__validate_winner(simple.winning_alliance, red_score, blue_score)
        match = MatchSimple(
            key, simple.comp_level, simple.set_number, simple.match_number,
            red_score, blue_score,
            {
                'team_keys': simple.alliances['red']['team_keys'],
                'dq': simple.alliances['red']['dq_team_keys'],
                'surrogate': simple.alliances['red']['surrogate_team_keys']
            }, {
                'team_keys': simple.alliances['blue']['team_keys'],
                'dq': simple.alliances['blue']['dq_team_keys'],
                'surrogate': simple.alliances['blue']['surrogate_team_keys']
            },
            winner,
            datetime.fromtimestamp(simple.time),
            datetime.fromtimestamp(simple.predicted_time),
            datetime.fromtimestamp(simple.actual_time)
        )
        if cached:
            self.__cache.save_match_simple(match)
        return match

    def get_match_level(self, match: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__match_simple(match, cached, cache_expiry).get_level()

    def get_match_set_number(self, match: str, cached: bool = True, cache_expiry: int = 90) -> int:
        return self.__match_simple(match, cached, cache_expiry).get_set_number()

    def get_match_number(self, match: str, cached: bool = True, cache_expiry: int = 90) -> int:
        return self.__match_simple(match, cached, cache_expiry).get_match_number()

    def get_match_winner(self, match: str, cached: bool = True, cache_expiry: int = 90) -> str:
        return self.__match_simple(match, cached, cache_expiry).get_winner()

    def get_match_red_score(self, match: str, cached: bool = True, cache_expiry: int = 90) -> int:
        return self.__match_simple(match, cached, cache_expiry).get_red_score()

    def get_match_blue_score(self, match: str, cached: bool = True, cache_expiry: int = 90) -> int:
        return self.__match_simple(match, cached, cache_expiry).get_blue_score()

    def get_match_red_teams(self, match: str, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        return self.__match_simple(match, cached, cache_expiry).get_red_teams()['team_keys']

    def get_match_blue_teams(self, match: str, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        return self.__match_simple(match, cached, cache_expiry).get_blue_teams()['team_keys']

    def get_match_time(self, match: str, cached: bool = True, cache_expiry: int = 90) -> datetime:
        return self.__match_simple(match, cached, cache_expiry).get_actual_time()
