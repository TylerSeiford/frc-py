from datetime import datetime
import tbapy
import statbotics
from .models import Location, Team, Webcast, Event, MatchAlliance, MatchSimple
from .cache import Cache



class FRC_PY:
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

    def year_range(self) -> tuple[int, int]:
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

    def team_years(self, team: str, cached: bool = True, cache_expiry: int = 90) -> list[int]:
        if cached:
            participation = self.__cache.get_team_years(team, cache_expiry)
            if participation is not None:
                return participation
        participation = self.__tba_client.team_years(team)
        if cached:
            self.__cache.save_team_years(team, participation)
        return participation

    def team(self, key: str, cached: bool = True, cache_expiry: int = 90) -> Team:
        if cached:
            team = self.__cache.get_team(key, cache_expiry)
            if team is not None:
                return team
        api_data = self.__tba_client.team(key)
        team = Team(
            key,
            api_data.nickname,
            api_data.name,
            Location(api_data.city, api_data.state_prov, api_data.country),
            api_data.school_name,
            api_data.website,
            api_data.rookie_year,
            api_data.motto
        )
        if cached:
            self.__cache.save_team(team)
        return team

    def team_year_events(self, team: str, year: int, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        if cached:
            events = self.__cache.get_team_year_events(team, year, cache_expiry)
            if events is not None:
                return events
        events = self.__tba_client.team_events(team, year, keys=True)
        if cached:
            self.__cache.save_team_year_events(team, year, events)
        return events

    def year_events(self, year: int, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        if cached:
            events = self.__cache.get_year_events(year, cache_expiry)
            if events is not None:
                return events
        events = self.__tba_client.events(year, keys=True)
        if cached:
            self.__cache.save_year_events(year, events)
        return events

    def event(self, key: str, cached: bool = True, cache_expiry: int = 90) -> Event:
        if cached:
            event = self.__cache.get_event(key, cache_expiry)
            if event is not None:
                return event
        event = self.__tba_client.event(key)
        district = event.district
        if district is not None:
            district = district['key']
        webcasts = []
        for webcast in event.webcasts:
            try:
                date = webcast['date']
            except KeyError:
                date = None
            try:
                file = webcast['file']
            except KeyError:
                file = None
            webcasts.append(Webcast(webcast['type'], webcast['channel'], date, file))
        event = Event(
            key, event.name, Location(event.city, event.state_prov, event.country), event.event_type,
            (event.start_date, event.end_date), district, event.short_name, event.week,
            event.address, event.postal_code, event.gmaps_place_id, event.gmaps_url,
            event.lat, event.lng, event.location_name, event.timezone,
            event.website, event.first_event_id, event.first_event_code,
            webcasts, event.division_keys, event.parent_event_key, event.playoff_type
        )
        if cached:
            self.__cache.save_event(event)
        return event

    def event_teams(self, event: str, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        if cached:
            teams = self.__cache.get_event_teams(event, cache_expiry)
            if teams is not None:
                return teams
        teams = self.__tba_client.event_teams(event, keys=True)
        if cached:
            self.__cache.save_event_teams(event, teams)
        return teams

    def event_matches(self, event: str, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        if cached:
            matches = self.__cache.get_event_matches(event, cache_expiry)
            if matches is not None:
                return matches
        matches = self.__tba_client.event_matches(event, keys=True)
        if cached:
            self.__cache.save_event_matches(event, matches)
        return matches

    def get_team_event_matches(self, team: str, event: str, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        if cached and self.__cache.is_cached(['teams', team, event], 'matches_tba'):
            matches = self.__cache.get(['teams', team, event], 'matches_tba', cache_expiry)
            if matches is not None:
                return matches
        matches = self.__tba_client.team_matches(team, event, keys=True)
        if cached:
            self.__cache.save(['teams', team, event], 'matches_tba', matches)
        return matches

    def match_simple(self, key: str, cached: bool = True, cache_expiry: int = 90) -> MatchSimple:
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
            MatchAlliance(
                simple.alliances['red']['team_keys'],
                simple.alliances['red']['dq_team_keys'],
                simple.alliances['red']['surrogate_team_keys']
            ),
            MatchAlliance(
                simple.alliances['blue']['team_keys'],
                simple.alliances['blue']['dq_team_keys'],
                simple.alliances['blue']['surrogate_team_keys']
            ),
            winner,
            datetime.fromtimestamp(simple.time),
            datetime.fromtimestamp(simple.predicted_time),
            datetime.fromtimestamp(simple.actual_time)
        )
        if cached:
            self.__cache.save_match_simple(match)
        return match
