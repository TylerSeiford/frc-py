'''
Interact with the TBA and Statbotics APIs
'''
from datetime import datetime
import tbapy
import statbotics
from .models import Location, Team, Webcast, Event, MatchAlliance, MatchVideo, Match
from .cache import Cache



class FRCPy:
    '''
    Class to interact with the TBA and Statbotics APIs
    '''
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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.__cache.__exit__(exc_type, exc_value, traceback)


    def _tba_client(self) -> tbapy.TBA:
        return self.__tba_client

    def _stat_client(self) -> statbotics.Statbotics:
        return self.__statbotics_client

    def _save(self,
        data_type: str,
        data: list[str] | Team | Event | Match | tuple[str, list[str]]
            | tuple[str, list[int]] | tuple[str, int, list[str]] | tuple[str, str, list[str]]
    ) -> None:
        match(data_type):
            case 'team_index':
                if not isinstance(data, list[str]):
                    raise TypeError('data must be a list of team keys')
                self.__cache.save_team_index(data)
            case 'team_years':
                if not isinstance(data, tuple):
                    raise TypeError('data must be a tuple')
                if not isinstance(data[0], str):
                    raise TypeError('data[0] must be a team key')
                if not isinstance(data[1], list[int]):
                    raise TypeError('data must be a list of years')
                self.__cache.save_team_years(data[0], data[1])
            case 'team':
                if not isinstance(data, Team):
                    raise TypeError('data must be a Team object')
                self.__cache.save_team(data)
            case 'team_year_events':
                if not isinstance(data, tuple):
                    raise TypeError('data must be a tuple')
                if not isinstance(data[0], str):
                    raise TypeError('data[0] must be a team key')
                if not isinstance(data[1], int):
                    raise TypeError('data[1] must be a year')
                if not isinstance(data[2], list[str]):
                    raise TypeError('data[2] must be a list of event keys')
                self.__cache.save_team_year_events(data[0], data[1], data[2])
            case 'year_events':
                if not isinstance(data, tuple):
                    raise TypeError('data must be a tuple')
                if not isinstance(data[0], int):
                    raise TypeError('data[0] must be a year')
                if not isinstance(data[1], list[str]):
                    raise TypeError('data[1] must be a list of event keys')
                self.__cache.save_year_events(data[0], data[1])
            case 'event':
                if not isinstance(data, Event):
                    raise TypeError('data must be an Event object')
                self.__cache.save_event(data)
            case 'event_teams':
                if not isinstance(data, tuple):
                    raise TypeError('data must be a tuple')
                if not isinstance(data[0], str):
                    raise TypeError('data[0] must be an event key')
                if not isinstance(data[1], list[str]):
                    raise TypeError('data[1] must be a list of team keys')
                self.__cache.save_event_teams(data[0], data[1])
            case 'event_matches':
                if not isinstance(data, tuple):
                    raise TypeError('data must be a tuple')
                if not isinstance(data[0], str):
                    raise TypeError('data[0] must be an event key')
                if not isinstance(data[1], list[str]):
                    raise TypeError('data[1] must be a list of match keys')
                self.__cache.save_event_matches(data[0], data[1])
            case 'team_event_matches':
                if not isinstance(data, tuple):
                    raise TypeError('data must be a tuple')
                if not isinstance(data[0], str):
                    raise TypeError('data[0] must be a team key')
                if not isinstance(data[1], str):
                    raise TypeError('data[1] must be an event key')
                if not isinstance(data[2], list[str]):
                    raise TypeError('data[2] must be a list of match keys')
                self.__cache.save_team_event_matches(data[0], data[1], data[2])
            case 'match':
                if not isinstance(data, Match):
                    raise TypeError('data must be a Match object')
                self.__cache.save_match(data)
            case _:
                raise ValueError('Invalid data type')


    def year_range(self) -> tuple[int, int]:
        '''Get the year range of events (uncached)'''
        status = self.__tba_client.status()
        return (1992, status['max_season'])

    def teams(self, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        '''Get all teams'''
        if cached:
            teams = self.__cache.get_team_index(cache_expiry)
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
            self.__cache.save_team_index(teams)
        return teams

    def team_years(self, team: str, cached: bool = True, cache_expiry: int = 90) -> list[int]:
        '''Get the years the team has participated in'''
        if cached:
            participation = self.__cache.get_team_years(team, cache_expiry)
            if participation is not None:
                return participation
        participation = self.__tba_client.team_years(team)
        if cached:
            self.__cache.save_team_years(team, participation)
        return participation

    def team(self, key: str, cached: bool = True, cache_expiry: int = 90) -> Team:
        '''Get a team'''
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

    def team_year_events(self, team: str, year: int, cached: bool = True,
            cache_expiry: int = 90) -> list[str]:
        '''Get the events a team has participated in in a year'''
        if cached:
            events = self.__cache.get_team_year_events(team, year, cache_expiry)
            if events is not None:
                return events
        events = self.__tba_client.team_events(team, year, keys=True)
        if cached:
            self.__cache.save_team_year_events(team, year, events)
        return events

    def year_events(self, year: int, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        '''Get all the events in a year'''
        if cached:
            events = self.__cache.get_year_events(year, cache_expiry)
            if events is not None:
                return events
        events = self.__tba_client.events(year, keys=True)
        if cached:
            self.__cache.save_year_events(year, events)
        return events

    def event(self, key: str, cached: bool = True, cache_expiry: int = 90) -> Event:
        '''Get an event'''
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
            key, event.name, Location(event.city, event.state_prov, event.country),
            event.event_type, (event.start_date, event.end_date), district, event.short_name,
            event.week, event.address, event.postal_code, event.gmaps_place_id, event.gmaps_url,
            event.lat, event.lng, event.location_name, event.timezone,
            event.website, event.first_event_id, event.first_event_code,
            webcasts, event.division_keys, event.parent_event_key, event.playoff_type
        )
        if cached:
            self.__cache.save_event(event)
        return event

    def event_teams(self, event: str, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        '''Get the teams that have participated in an event'''
        if cached:
            teams = self.__cache.get_event_teams(event, cache_expiry)
            if teams is not None:
                return teams
        teams = self.__tba_client.event_teams(event, keys=True)
        if cached:
            self.__cache.save_event_teams(event, teams)
        return teams

    def event_matches(self, event: str, cached: bool = True, cache_expiry: int = 90) -> list[str]:
        '''Get the matches in an event'''
        if cached:
            matches = self.__cache.get_event_matches(event, cache_expiry)
            if matches is not None:
                return matches
        matches = self.__tba_client.event_matches(event, keys=True)
        if cached:
            self.__cache.save_event_matches(event, matches)
        return matches

    def team_event_matches(self, team: str, event: str, cached: bool = True,
            cache_expiry: int = 90) -> list[str]:
        '''Get the matches a team has participated in an event'''
        if cached:
            matches = self.__cache.get_team_event_matches(team, event, cache_expiry)
            if matches is not None:
                return matches
        matches = self.__tba_client.team_matches(team, event, keys=True)
        if cached:
            self.__cache.save_team_event_matches(team, event, matches)
        return matches

    def match(self, key: str, cached: bool = True, cache_expiry: int = 90) -> Match:
        '''Get a match'''
        if cached:
            match = self.__cache.get_match(key, cache_expiry)
            if match is not None:
                return match
        match = self.__tba_client.match(key)
        red_score = match.alliances['red']['score']
        blue_score = match.alliances['blue']['score']
        winner = FRCPy.__validate_winner(match.winning_alliance, red_score, blue_score)
        videos = []
        for video in match.videos:
            videos.append(MatchVideo(video['type'], video['key']))
        scheduled_time = match.time
        if scheduled_time is not None:
            scheduled_time = datetime.fromtimestamp(scheduled_time)
        predicted_time = match.predicted_time
        if predicted_time is not None:
            predicted_time = datetime.fromtimestamp(predicted_time)
        actual_time = match.actual_time
        if actual_time is not None:
            actual_time = datetime.fromtimestamp(actual_time)
        post_result_time = match.post_result_time
        if post_result_time is not None:
            post_result_time = datetime.fromtimestamp(post_result_time)
        match = Match(
            key, match.comp_level, match.set_number, match.match_number,
            red_score, blue_score,
            MatchAlliance(
                match.alliances['red']['team_keys'],
                match.alliances['red']['dq_team_keys'],
                match.alliances['red']['surrogate_team_keys']
            ),
            MatchAlliance(
                match.alliances['blue']['team_keys'],
                match.alliances['blue']['dq_team_keys'],
                match.alliances['blue']['surrogate_team_keys']
            ),
            winner,
            scheduled_time,
            predicted_time,
            actual_time,
            post_result_time,
            videos
        )
        if cached:
            self.__cache.save_match(match)
        return match
