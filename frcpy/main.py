'''
Interact with the TBA and Statbotics APIs
'''
from datetime import datetime
import googlemaps
import tbapy
import statbotics
from .models import Location, PreciseLocation, Team, TeamYearStats, Webcast, Event, MatchAlliance, MatchVideo, Match
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


    def __init__(self, tba_token: str, gmaps_token: str = ''):
        self.__tba_client = tbapy.TBA(tba_token)
        self.__statbotics_client = statbotics.Statbotics()
        if gmaps_token != '':
            self.__gmaps_client = googlemaps.Client(gmaps_token)
        else:
            self.__gmaps_client = None
        self.__cache = Cache()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.__cache.__exit__(exc_type, exc_value, traceback)


    def _tba_client(self) -> tbapy.TBA:
        return self.__tba_client

    def _stat_client(self) -> statbotics.Statbotics:
        return self.__statbotics_client

    def _gmaps_client(self) -> googlemaps.Client | None:
        return self.__gmaps_client

    def _cache(self) -> Cache:
        return self.__cache


    # The Blue Alliance API provided data
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
        location = Location(event.city, event.state_prov, event.country)
        precise_location = PreciseLocation(location, event.lat, event.lng,
                event.address, event.postal_code, event.gmaps_place_id)
        event = Event(
            key, event.name, location, event.event_type,
            (event.start_date, event.end_date), district, event.short_name, event.week,
            precise_location, event.location_name, event.timezone,
            event.website, event.first_event_id, event.first_event_code,
            webcasts, event.division_keys,
            event.parent_event_key, event.playoff_type
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


    # Statbotics API provided data
    def team_year_stats(self, team: str, year: int, cached: bool = True,
            cache_expiry: int = 90) -> TeamYearStats:
        '''Get the stats for a team in a year'''
        if cached:
            stats = self.__cache.get_team_year_stats(team, year, cache_expiry)
            if stats is not None:
                return stats
        stats = self.__statbotics_client.get_team_year(
            Team.team_key_to_number(team), year
        )

        epa_start = stats['epa_start']
        epa_pre_champs = stats['epa_pre_champs']
        epa_end = stats['epa_end']
        epa_mean = stats['epa_mean']
        epa_max = stats['epa_max']
        epa_diff = stats['epa_diff']
        auto_epa_start = stats['auto_epa_start']
        auto_epa_pre_champs = stats['auto_epa_pre_champs']
        auto_epa_end = stats['auto_epa_end']
        auto_epa_mean = stats['auto_epa_mean']
        auto_epa_max = stats['auto_epa_max']
        teleop_epa_start = stats['teleop_epa_start']
        teleop_epa_pre_champs = stats['teleop_epa_pre_champs']
        teleop_epa_end = stats['teleop_epa_end']
        teleop_epa_mean = stats['teleop_epa_mean']
        teleop_epa_max = stats['teleop_epa_max']
        endgame_epa_start = stats['endgame_epa_start']
        endgame_epa_pre_champs = stats['endgame_epa_pre_champs']
        endgame_epa_end = stats['endgame_epa_end']
        endgame_epa_mean = stats['endgame_epa_mean']
        endgame_epa_max = stats['endgame_epa_max']
        rp_1_epa_start = stats['rp_1_epa_start']
        rp_1_epa_pre_champs = stats['rp_1_epa_pre_champs']
        rp_1_epa_end = stats['rp_1_epa_end']
        rp_1_epa_mean = stats['rp_1_epa_mean']
        rp_1_epa_max = stats['rp_1_epa_max']
        rp_2_epa_start = stats['rp_2_epa_start']
        rp_2_epa_pre_champs = stats['rp_2_epa_pre_champs']
        rp_2_epa_end = stats['rp_2_epa_end']
        rp_2_epa_mean = stats['rp_2_epa_mean']
        rp_2_epa_max = stats['rp_2_epa_max']
        norm_epa_end = stats['norm_epa_end']
        wins = stats['wins']
        losses = stats['losses']
        ties = stats['ties']
        count = stats['count']
        winrate = stats['winrate']
        epa_rank = stats['total_epa_rank']
        epa_percent = stats['total_epa_percentile']


        stats = TeamYearStats(
            team, year,
            epa_start, epa_pre_champs, epa_end, epa_mean, epa_max, epa_diff,
            auto_epa_start, auto_epa_pre_champs, auto_epa_end, auto_epa_mean, auto_epa_max,
            teleop_epa_start, teleop_epa_pre_champs, teleop_epa_end, teleop_epa_mean, teleop_epa_max,
            endgame_epa_start, endgame_epa_pre_champs, endgame_epa_end, endgame_epa_mean, endgame_epa_max,
            rp_1_epa_start, rp_1_epa_pre_champs, rp_1_epa_end, rp_1_epa_mean, rp_1_epa_max,
            rp_2_epa_start, rp_2_epa_pre_champs, rp_2_epa_end, rp_2_epa_mean, rp_2_epa_max,
            norm_epa_end,
            wins, losses, ties, count, winrate,
            epa_rank, epa_percent
        )
        if cached:
            self.__cache.save_team_year_stats(team, year, stats)
        return stats


    # Google Maps API provided data
    def _geocode(self, string: str) -> tuple[float, float, str, str, str] | None:
        geocoded = self.__gmaps_client.geocode(string)
        lat = geocoded[0]['geometry']['location']['lat']
        lng = geocoded[0]['geometry']['location']['lng']
        address = geocoded[0]['formatted_address']
        postal_code = None
        for component in geocoded[0]['address_components']:
            if 'postal_code' in component['types']:
                postal_code = component['long_name']
                break
        place_id = geocoded[0]['place_id']
        return lat, lng, address, postal_code, place_id

    def __team_school(self, team: Team) -> PreciseLocation | None:
        school = team.school_name()
        location = team.location()
        state_prov = location.state_prov()
        country = location.country()

        result = self._geocode(f"{school}, {state_prov}, {country}")
        if result is None:
            return None
        lat, lng, address, postal_code, place_id = result
        if postal_code is None:
            return None
        return PreciseLocation(location, lat, lng, address, postal_code, place_id)

    def __team_high_school(self, team: Team) -> PreciseLocation | None:
        location = team.location()
        city = location.city()
        state_prov = location.state_prov()
        country = location.country()

        result = self._geocode(f"{city} High School, {state_prov}, {country}")
        if result is None:
            return None
        lat, lng, address, postal_code, place_id = result
        if postal_code is None:
            return None
        return PreciseLocation(location, lat, lng, address, postal_code, place_id)

    def __team_city(self, team: Team) -> PreciseLocation | None:
        location = team.location()
        city = location.city()
        state_prov = location.state_prov()
        country = location.country()

        result = self._geocode(f"{city}, {state_prov}, {country}")
        if result is None:
            return None
        lat, lng, address, postal_code, place_id = result
        return PreciseLocation(location, lat, lng, address, postal_code, place_id)

    def team_precise_location(self, team: Team, cached: bool = True,
            cache_expiry: int = 360) -> PreciseLocation | None:
        '''Attempt to get a precise google-maps location for a team'''
        if self.__gmaps_client is None:
            return None
        if cached:
            data = self.__cache.get_team_precise_location(team.key(), cache_expiry)
            if data is not None and data.postal_code() is not None:
                return data

        data = self.__team_school(team)
        if data is None:
            data = self.__team_high_school(team)
        if data is None:
            data = self.__team_city(team)
        if cached:
            self.__cache.save_team_precise_location(team.key(), data)
        return data

    def precise_distance(self, origin: PreciseLocation, destination: PreciseLocation,
            cached: bool = True, cache_expiry: int = 1800) -> float | None:
        '''Get a precise google-maps distance between two precise locations'''
        if self.__gmaps_client is None:
            return None
        if cached:
            data = self.__cache.get_precise_distance(
                origin.place_id(),
                destination.place_id(),
                cache_expiry
            )
            if data is not None:
                return data
        distance_matrix = self.__gmaps_client.distance_matrix(
            f"place_id:{origin.place_id()}",
            f"place_id:{destination.place_id()}"
        )
        data = distance_matrix['rows'][0]['elements'][0]
        if data['status'] == 'ZERO_RESULTS':
            return None
        meters = data['distance']['value']
        if cached:
            self.__cache.save_precise_distance(origin.place_id(), destination.place_id(), meters)
        return meters
