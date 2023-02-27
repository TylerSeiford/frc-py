'''
Cache for the FRCPy class
'''
from datetime import datetime, timedelta
import os
import sqlite3
import json
from .models import Location, PreciseLocation, Team, TeamYearStats, Webcast, Event, MatchAlliance, MatchVideo, Match



class Cache:
    '''
    Class to cache data
    '''
    def __init__(self, cache_dir: str = './cache'):
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        self.__connection = sqlite3.connect(os.path.join(cache_dir, 'cache.db'))
        self.__init_team_index()
        self.__init_teams()
        self.__init_team_years()
        self.__init_team_year_events()
        self.__init_year_events()
        self.__init_events()
        self.__init_event_teams()
        self.__init_event_matches()
        self.__init_team_event_matches()
        self.__init_match()
        self.__init_team_year_stats()
        self.__init_team_precise_locations()
        self.__init_precise_distances()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__connection.close()

    def _connection(self) -> sqlite3.Connection:
        return self.__connection


    def __init_team_index(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS team_index (
            last_updated datetime,
            teams text
        )''')
        self.__connection.commit()

    def save_team_index(self, teams: list[str]) -> None:
        '''Save the team index'''
        self._delete_team_index()
        self.__connection.execute('INSERT INTO team_index VALUES (?, ?)', (
            datetime.utcnow().isoformat(),
            json.dumps(teams)
        ))
        self.__connection.commit()

    def get_team_index(self, cache_expiry: int) -> list[str] | None:
        '''Get the team index'''
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM team_index')
        result = cursor.fetchone()
        if result is None:
            return None
        timestamp, teams = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_team_index()
            return None
        return json.loads(teams)

    def _delete_team_index(self) -> None:
        self.__connection.execute('DELETE FROM team_index')
        self.__connection.commit()


    def __init_teams(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS teams (
            last_updated datetime,
            key text, nickname text, name text,
            city text, state_prov text, country text,
            school_name text, website text,
            rookie_year text, motto text
        )''')
        self.__connection.commit()

    def save_team(self, team: Team) -> None:
        '''Save a team'''
        self._delete_team(team.key())
        location = team.location()
        self.__connection.execute('INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            team.key(), team.nickname(), team.name(),
            location.city(), location.state_prov(), location.country(),
            team.school_name(), team.website(),
            team.rookie_year(), team.motto()
        ))
        self.__connection.commit()

    def get_team(self, team_key: str, cache_expiry: int) -> Team | None:
        '''Get a team'''
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM teams WHERE key = ?', [team_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        (
            timestamp, key, nickname, name,
            city, state_prov, country,
            school_name, website,
            rookie_year, motto
        ) = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_team(team_key)
            return None
        return Team(
            key, nickname, name,
            Location(city, state_prov, country),
            school_name, website,
            rookie_year, motto
        )

    def _delete_team(self, team_key: str) -> None:
        self.__connection.execute('DELETE FROM teams WHERE key = ?', [team_key])
        self.__connection.commit()


    def __init_team_years(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS team_years (
            last_updated datetime,
            key text, years text
        )''')
        self.__connection.commit()

    def save_team_years(self, team_key: str, years: list[int]) -> None:
        '''Save the years a team has participated in'''
        self._delete_team_years(team_key)
        self.__connection.execute('INSERT INTO team_years VALUES (?, ?, ?)', (
            datetime.utcnow().isoformat(),
            team_key, json.dumps(years)
        ))
        self.__connection.commit()

    def get_team_years(self, team_key: str, cache_expiry: int) -> list[int] | None:
        '''Get the years a team has participated in'''
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM team_years WHERE key = ?', [team_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        timestamp, _, years = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_team_years(team_key)
            return None
        return json.loads(years)

    def _delete_team_years(self, team_key: str) -> None:
        self.__connection.execute('DELETE FROM team_years WHERE key = ?', [team_key])
        self.__connection.commit()


    def __init_team_year_events(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS team_year_events (
            last_updated datetime,
            key text, year int, events text
        )''')
        self.__connection.commit()

    def save_team_year_events(self, team_key: str, year: int, events: list[str]) -> None:
        '''Save the events a team has participated in for a given year'''
        self._delete_team_year_events(team_key, year)
        self.__connection.execute('INSERT INTO team_year_events VALUES (?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            team_key, year, json.dumps(events)
        ))
        self.__connection.commit()

    def get_team_year_events(self, team_key: str, year: int, cache_expiry: int) -> list[str] | None:
        '''Get the events a team has participated in for a given year'''
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM team_year_events WHERE key = ? AND year = ?',
                [team_key, year])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        timestamp, _, year, events = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_team_year_events(team_key, year)
            return None
        return json.loads(events)

    def _delete_team_year_events(self, team_key: str, year: int) -> None:
        self.__connection.execute('DELETE FROM team_year_events WHERE key = ? AND year = ?',
                [team_key, year])
        self.__connection.commit()


    def __init_year_events(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS year_events (
            last_updated datetime,
            year int, events text
        )''')
        self.__connection.commit()

    def save_year_events(self, year: int, events: list[str]) -> None:
        '''Save the events for a given year'''
        self._delete_year_events(year)
        self.__connection.execute('INSERT INTO year_events VALUES (?, ?, ?)', (
            datetime.utcnow().isoformat(),
            year, json.dumps(events)
        ))
        self.__connection.commit()

    def get_year_events(self, year: int, cache_expiry: int) -> list[str] | None:
        '''Get the events for a given year'''
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM year_events WHERE year = ?', [year])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        timestamp, year, events = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_year_events(year)
            return None
        return json.loads(events)

    def _delete_year_events(self, year: int) -> None:
        self.__connection.execute('DELETE FROM year_events WHERE year = ?', [year])
        self.__connection.commit()


    def __init_events(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS events (
            last_updated datetime,
            key text, year int, name text,
            city text, state_prov text, country text,
            type int,
            start_date datetime, end_date datetime,
            event_district text,
            short_name text, week int,
            address text, postal_code text,
            place_id text, lat float, lng float,
            location_name text, timezone text,
            website text, fisrt_event_id text, first_event_code text,
            webcasts text, divisions text, parent_event_key text, playoff_type text
        )''')
        self.__connection.commit()

    def save_event(self, event: Event) -> None:
        '''Save an event'''
        self._delete_event(event.key())
        location = event.location()
        start, end = event.dates()
        webcasts = []
        for webcast in event.webcasts():
            webcasts.append(webcast.to_json())
        precise_location = event.precise_location()
        self.__connection.execute('INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '
                '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            event.key(), Event.event_key_to_year(event.key()), event.name(),
            location.city(), location.state_prov(), location.country(),
            event.event_type(),
            start.isoformat(), end.isoformat(),
            event.district_key(),
            event.short_name(), event.week(),
            precise_location.address(), precise_location.postal_code(),
            precise_location.place_id(),
            precise_location.latitude(), precise_location.longitude(),
            event.location_name(), event.timezone(),
            event.website(), event.first_event_id(), event.first_event_code(),
            json.dumps(webcasts), json.dumps(event.divisions()),
            event.parent_event_key(), event.playoff_type()
        ))
        self.__connection.commit()

    def get_event(self, event_key: str, cache_expiry: int) -> Event | None:
        '''Get an event'''
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM events WHERE key = ?', [event_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        (
            timestamp,
            key, _, name,
            city, state_prov, country,
            event_type,
            start, end,
            event_district,
            short_name, week,
            address, postal_code,
            place_id, lat, lng,
            location_name, timezone,
            website, first_event_id, first_event_code,
            raw_webcasts, divisions, parent_event_key, playoff_type
        ) = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_event(event_key)
            return None
        start = datetime.fromisoformat(start)
        end = datetime.fromisoformat(end)
        location = Location(city, state_prov, country)
        precise_location = PreciseLocation(
            location, lat, lng,
            address, postal_code, place_id
        )
        raw_webcasts = json.loads(raw_webcasts)
        webcasts = []
        for webcast in raw_webcasts:
            webcast = json.loads(webcast)
            webcasts.append(Webcast(webcast['type'], webcast['channel'],
                    webcast['date'], webcast['file']))
        return Event(
            key, name,
            location,
            event_type,
            (start, end),
            event_district,
            short_name, week, 
            precise_location,
            location_name, timezone,
            website, first_event_id, first_event_code,
            webcasts, divisions, parent_event_key, playoff_type
        )

    def _delete_event(self, event_key: str) -> None:
        self.__connection.execute('DELETE FROM events WHERE key = ?', [event_key])
        self.__connection.commit()


    def __init_event_teams(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS event_teams (
            last_updated datetime,
            event text, teams text
        )''')
        self.__connection.commit()

    def save_event_teams(self, event_key: str, teams: list[str]) -> None:
        '''Save the teams for an event'''
        self._delete_event_teams(event_key)
        self.__connection.execute('INSERT INTO event_teams VALUES (?, ?, ?)', (
            datetime.utcnow().isoformat(),
            event_key, json.dumps(teams)
        ))
        self.__connection.commit()

    def get_event_teams(self, event_key: str, cache_expiry: int) -> list[str] | None:
        '''Get the teams for an event'''
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM event_teams WHERE event = ?', [event_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        timestamp, _, teams = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_event_teams(event_key)
            return None
        return json.loads(teams)

    def _delete_event_teams(self, event_key: str) -> None:
        self.__connection.execute('DELETE FROM event_teams WHERE event = ?', [event_key])
        self.__connection.commit()


    def __init_event_matches(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS event_matches (
            last_updated datetime,
            event text, matches text
        )''')
        self.__connection.commit()

    def save_event_matches(self, event_key: str, matches: list[str]) -> None:
        '''Save the matches for an event'''
        self._delete_event_matches(event_key)
        self.__connection.execute('INSERT INTO event_matches VALUES (?, ?, ?)', (
            datetime.utcnow().isoformat(),
            event_key, json.dumps(matches)
        ))
        self.__connection.commit()

    def get_event_matches(self, event_key: str, cache_expiry: int) -> list[str] | None:
        '''Get the matches for an event'''
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM event_matches WHERE event = ?', [event_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        timestamp, _, matches = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_event_matches(event_key)
            return None
        return json.loads(matches)

    def _delete_event_matches(self, event_key: str) -> None:
        self.__connection.execute('DELETE FROM event_matches WHERE event = ?', [event_key])
        self.__connection.commit()


    def __init_team_event_matches(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS team_event_matches (
            last_updated datetime,
            team text, event text, matches text
        )''')
        self.__connection.commit()

    def save_team_event_matches(self, team_key: str, event_key: str, matches: list[str]) -> None:
        '''Save the matches for a team at an event'''
        self._delete_team_event_matches(team_key, event_key)
        self.__connection.execute('INSERT INTO team_event_matches VALUES (?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            team_key, event_key, json.dumps(matches)
        ))
        self.__connection.commit()

    def get_team_event_matches(self, team_key: str, event_key: str,
            cache_expiry: int) -> list[str] | None:
        '''Get the matches for a team at an event'''
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM team_event_matches WHERE team = ? AND event = ?',
                [team_key, event_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        timestamp, _, _, matches = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_team_event_matches(team_key, event_key)
            return None
        return json.loads(matches)

    def _delete_team_event_matches(self, team_key: str, event_key: str) -> None:
        self.__connection.execute('DELETE FROM team_event_matches WHERE team = ? AND event = ?',
                [team_key, event_key])
        self.__connection.commit()


    def __init_match(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS matches (
            last_updated datetime,
            key text, year int, event text,
            level text, set_number int, match_number int,
            red_score int, blue_score int,
            red_teams text, blue_teams text,
            winner text,
            scheduled_time datetime, predicted_time datetime,
            actual_time datetime, result_time datetime,
            videos text
        )''')
        self.__connection.commit()

    def save_match(self, match: Match) -> None:
        '''Save a match'''
        self._delete_match(match.key())
        videos = []
        for video in match.videos():
            videos.append(video.to_json())
        self.__connection.execute('INSERT INTO matches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, '
                '?, ?, ?, ?, ?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            match.key(),
            Match.match_key_to_year(match.key()),
            Match.match_key_to_event(match.key()),
            match.level(), match.set_number(), match.match_number(),
            match.red_score(), match.blue_score(),
            match.red_teams().to_json(), match.blue_teams().to_json(),
            match.winner(),
            match.schedule_time(), match.predicted_time(),
            match.actual_time(), match.result_time(),
            json.dumps(videos)
        ))
        self.__connection.commit()

    def get_match(self, match_key: str, cache_expiry: int) -> Match | None:
        '''Get a match'''
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM matches WHERE key = ?', [match_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        (
            timestamp, key, _, _, level, set_number, match_number, red_score, blue_score,
            red_teams, blue_teams, winner,
            scheduled_time, predicted_time, actual_time, result_time,
            raw_videos
        ) = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_match(match_key)
            return None
        red_teams = json.loads(red_teams)
        red_teams = MatchAlliance(red_teams['teams'], red_teams['dq'], red_teams['surrogate'])
        blue_teams = json.loads(blue_teams)
        blue_teams = MatchAlliance(blue_teams['teams'], blue_teams['dq'], blue_teams['surrogate'])
        raw_videos = json.loads(raw_videos)
        videos = []
        for video in raw_videos:
            video = json.loads(video)
            videos.append(MatchVideo(video['key'], video['type']))
        if scheduled_time is not None:
            scheduled_time = datetime.fromisoformat(scheduled_time)
        if predicted_time is not None:
            predicted_time = datetime.fromisoformat(predicted_time)
        if actual_time is not None:
            actual_time = datetime.fromisoformat(actual_time)
        if result_time is not None:
            result_time = datetime.fromisoformat(result_time)
        return Match(key, level, set_number, match_number,
                red_score, blue_score,
                red_teams, blue_teams,
                winner,
                scheduled_time, predicted_time, actual_time, result_time,
                videos
        )

    def _delete_match(self, match_key: str) -> None:
        self.__connection.execute('DELETE FROM matches WHERE key = ?', [match_key])
        self.__connection.commit()


    def __init_team_year_stats(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS team_year_stats (
            last_updated datetime,
            team_key text, year int,
            epa_start float, epa_pre_champs float, epa_end float, epa_mean float, epa_max float, epa_diff float,
            auto_epa_start float, auto_epa_pre_champs float, auto_epa_end float, auto_epa_mean float, auto_epa_max float,
            teleop_epa_start float, teleop_epa_pre_champs float, teleop_epa_end float, teleop_epa_mean float, teleop_epa_max float,
            endgame_epa_start float, endgame_epa_pre_champs float, endgame_epa_end float, endgame_epa_mean float, endgame_epa_max float,
            rp_1_epa_start float, rp_1_epa_pre_champs float, rp_1_epa_end float, rp_1_epa_mean float, rp_1_epa_max float,
            rp_2_epa_start float, rp_2_epa_pre_champs float, rp_2_epa_end float, rp_2_epa_mean float, rp_2_epa_max float,
            norm_epa_end float,
            wins int, losses int, ties int, count int, winrate float,
            epa_rank float, epa_percent float
        )''')
        self.__connection.commit()

    def save_team_year_stats(self, team_key: str, year: int, stats: TeamYearStats) -> None:
        '''Save the stats for a team in a given year'''
        self._delete_team_year_stats(team_key, year)
        self.__connection.execute('INSERT INTO team_year_stats VALUES ('
            '?, '
            '?, ?, '
            '?, ?, ?, ?, ?, ?, '
            '?, ?, ?, ?, ?, '
            '?, ?, ?, ?, ?, '
            '?, ?, ?, ?, ?, '
            '?, ?, ?, ?, ?, '
            '?, ?, ?, ?, ?, '
            '?, '
            '?, ?, ?, ?, ?, '
            '?, ?)', (
            datetime.utcnow().isoformat(),
            team_key, year,
            stats.epa_start(), stats.epa_pre_champs(), stats.epa_end(), stats.epa_mean(), stats.epa_max(), stats.epa_diff(),
            stats.auto_epa_start(), stats.auto_epa_pre_champs(), stats.auto_epa_end(), stats.auto_epa_mean(), stats.auto_epa_max(),
            stats.teleop_epa_start(), stats.teleop_epa_pre_champs(), stats.teleop_epa_end(), stats.teleop_epa_mean(), stats.teleop_epa_max(),
            stats.endgame_epa_start(), stats.endgame_epa_pre_champs(), stats.endgame_epa_end(), stats.endgame_epa_mean(), stats.endgame_epa_max(),
            stats.rp_1_epa_start(), stats.rp_1_epa_pre_champs(), stats.rp_1_epa_end(), stats.rp_1_epa_mean(), stats.rp_1_epa_max(),
            stats.rp_2_epa_start(), stats.rp_2_epa_pre_champs(), stats.rp_2_epa_end(), stats.rp_2_epa_mean(), stats.rp_2_epa_max(),
            stats.norm_epa_end(),
            stats.wins(), stats.losses(), stats.ties(), stats.count(), stats.winrate(),
            stats.epa_rank(), stats.epa_percent()
        ))
        self.__connection.commit()

    def get_team_year_stats(self, team_key: str, year: int,
            cache_expiry: int) -> TeamYearStats | None:
        '''Get the stats for a team in a given year'''
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM team_year_stats WHERE team_key = ? AND year = ?',
                [team_key, year])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        (
            timestamp,
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
        ) = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_team_year_stats(team_key, year)
            return None
        return TeamYearStats(
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

    def _delete_team_year_stats(self, team_key: str, year: int) -> None:
        self.__connection.execute('DELETE FROM team_year_stats WHERE team_key = ? AND year = ?',
                [team_key, year])
        self.__connection.commit()


    def __init_team_precise_locations(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS team_precise_locations (
            last_updated datetime,
            team_key text,
            city text, state_prov text, country text,
            latitude float, longitude float,
            address text, postal_code text,
            place_id text
        )''')
        self.__connection.commit()

    def save_team_precise_location(self, team_key: str, location: PreciseLocation) -> None:
        '''Save the precise location for a team'''
        self._delete_team_precise_location(team_key)
        self.__connection.execute('INSERT INTO team_precise_locations VALUES (?, ?, ?, ?, ?, '
                '?, ?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            team_key,
            location.location().city(),
            location.location().state_prov(),
            location.location().country(),
            location.latitude(), location.longitude(),
            location.address(),
            location.postal_code(),
            location.place_id()
        ))
        self.__connection.commit()

    def get_team_precise_location(self, team_key: str,
            cache_expiry: int) -> PreciseLocation | None:
        '''Get the precise location for a team'''
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM team_precise_locations WHERE team_key = ?', [team_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        (
            timestamp,
            _,
            city, state_prov, country,
            latitude, longitude,
            address,
            postal_code,
            place_id
        ) = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_team_precise_location(team_key)
            return None
        return PreciseLocation(
            Location(city, state_prov, country),
            latitude, longitude,
            address,
            postal_code,
            place_id
        )

    def _delete_team_precise_location(self, team_key: str) -> None:
        self.__connection.execute('DELETE FROM team_precise_locations WHERE team_key = ?',
                [team_key])
        self.__connection.commit()


    def __init_precise_distances(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS precise_distances (
            last_updated datetime,
            origin_id text, destination_id text,
            distance float
        )''')
        self.__connection.commit()

    def save_precise_distance(self, origin_id: str, destination_id: str, meters: float) -> None:
        '''Save the precise distance for a pair of IDs'''
        self._delete_precise_distances(origin_id, destination_id)
        self.__connection.execute('INSERT into precise_distances VALUES (?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            origin_id, destination_id,
            meters
        ))
        self.__connection.commit()

    def get_precise_distance(self, origin_id: str, destination_id: str, cache_expiry: int
            ) -> float | None:
        '''Get the precise distance for two IDs'''
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM precise_distances WHERE origin_id = ? AND destination_id = ?',
            [origin_id, destination_id])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        (
            timestamp, _, _, meters
        ) = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_precise_distances(origin_id, destination_id)
            return None
        return meters

    def _delete_precise_distances(self, origin_id: str, destination_id: str) -> None:
        self.__connection.execute(
            'DELETE FROM precise_distances WHERE origin_id = ? AND destination_id = ?',
            [origin_id, destination_id])
        self.__connection.commit()
