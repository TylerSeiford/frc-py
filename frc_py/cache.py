from datetime import datetime, timedelta
import os
import sqlite3
import json
from .models import Location, Team, Webcast, Event, MatchAlliance, MatchSimple



class Cache:
    def __init__(self, cache_dir: str = './cache'):
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        self.__connection = sqlite3.connect(os.path.join(cache_dir, 'cache.db'))
        self.__init_teams()
        self.__init_team_years()
        self.__init_team_year_events()
        self.__init_year_events()
        self.__init_events()
        self.__init_match_simple()


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
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM teams WHERE key = ?', [team_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        timestamp, key, nickname, name, city, state_prov, country, school_name, website, rookie_year, motto = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_team(team_key)
            return None
        return Team(key, nickname, name, Location(city, state_prov, country), school_name, website, rookie_year, motto)

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
        self.__connection.execute('INSERT INTO team_years VALUES (?, ?, ?)', (
            datetime.utcnow().isoformat(),
            team_key, json.dumps(years)
        ))
        self.__connection.commit()

    def get_team_years(self, team_key: str, cache_expiry: int) -> list[int] | None:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM team_years WHERE key = ?', [team_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        timestamp, key, years = result
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
        self.__connection.execute('INSERT INTO team_year_events VALUES (?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            team_key, year, json.dumps(events)
        ))
        self.__connection.commit()

    def get_team_year_events(self, team_key: str, year: int, cache_expiry: int) -> list[str] | None:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM team_year_events WHERE key = ? AND year = ?', [team_key, year])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        timestamp, key, year, events = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_team_year_events(team_key, year)
            return None
        return json.loads(events)

    def _delete_team_year_events(self, team_key: str, year: int) -> None:
        self.__connection.execute('DELETE FROM team_year_events WHERE key = ? AND year = ?', [team_key, year])
        self.__connection.commit()


    def __init_year_events(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS year_events (
            last_updated datetime,
            year int, events text
        )''')
        self.__connection.commit()

    def save_year_events(self, year: int, events: list[str]) -> None:
        self.__connection.execute('INSERT INTO year_events VALUES (?, ?, ?)', (
            datetime.utcnow().isoformat(),
            year, json.dumps(events)
        ))
        self.__connection.commit()

    def get_year_events(self, year: int, cache_expiry: int) -> list[str] | None:
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
            short_name text, week int, address text, postal_code text,
            gmaps_place_id text, gmaps_url text, lat float, lng float,
            location_name text, timezone text,
            website text, fisrt_event_id text, first_event_code text,
            webcasts text, divisions text, parent_event_key text, playoff_type text
        )''')
        self.__connection.commit()

    def save_event(self, event: Event) -> None:
        location = event.location()
        start, end = event.dates()
        webcasts = []
        for webcast in event.webcasts():
            webcasts.append(webcast.to_json())
        self.__connection.execute('INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            event.key(), Event.event_key_to_year(event.key()), event.name(),
            location.city(), location.state_prov(), location.country(),
            event.event_type(),
            start, end,
            event.district_key(), 
            event.short_name(), event.week(), event.address(), event.postal_code(),
            event.gmaps_place_id(), event.gmaps_url(), event.lat(), event.lng(),
            event.location_name(), event.timezone(),
            event.website(), event.first_event_id(), event.first_event_code(),
            json.dumps(webcasts), json.dumps(event.divisions()), event.parent_event_key(), event.playoff_type()
        ))
        self.__connection.commit()

    def get_event(self, event_key: str, cache_expiry: int) -> Event | None:
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
            short_name, week, address, postal_code,
            gmaps_place_id, gmaps_url, lat, lng,
            location_name, timezone,
            website, first_event_id, first_event_code,
            raw_webcasts, divisions, parent_event_key, playoff_type
        ) = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_event(event_key)
            return None
        raw_webcasts = json.loads(raw_webcasts)
        webcasts = []
        for webcast in raw_webcasts:
            webcast = json.loads(webcast)
            webcasts.append(Webcast(webcast['type'], webcast['channel'], webcast['date'], webcast['file']))
        return Event(
            key, name,
            Location(city, state_prov, country),
            event_type,
            (start, end),
            event_district,
            short_name, week, address, postal_code,
            gmaps_place_id, gmaps_url, lat, lng,
            location_name, timezone,
            website, first_event_id, first_event_code,
            webcasts, divisions, parent_event_key, playoff_type
        )

    def _delete_event(self, event_key: str) -> None:
        self.__connection.execute('DELETE FROM events WHERE key = ?', [event_key])
        self.__connection.commit()


    def __init_match_simple(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS match_simple (
            last_updated datetime,
            key text, year int, event text,
            level text, set_number int, match_number int,
            red_score int, blue_score int,
            red_teams text, blue_teams text,
            winner text,
            scheduled_time datetime, predicted_time datetime, actual_time datetime
        )''')
        self.__connection.commit()

    def save_match_simple(self, match: MatchSimple) -> None:
        self.__connection.execute('INSERT INTO match_simple VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            match.key(), MatchSimple.match_key_to_year(match.key()), MatchSimple.match_key_to_event(match.key()),
            match.level(), match.set_number(), match.match_number(),
            match.red_score(), match.blue_score(),
            match.red_teams().to_json(), match.blue_teams().to_json(),
            match.winner(),
            match.schedule_time(), match.predicted_time(), match.actual_time()
        ))
        self.__connection.commit()

    def get_match_simple(self, match_key: str, cache_expiry: int) -> MatchSimple | None:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM match_simple WHERE key = ?', [match_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        timestamp, key, _, _, level, set_number, match_number, red_score, blue_score, red_teams, blue_teams, winner, scheduled_time, predicted_time, actual_time = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_match_simple(match_key)
            return None
        red_teams = json.loads(red_teams)
        red_teams = MatchAlliance(red_teams['teams'], red_teams['dq'], red_teams['surrogate'])
        blue_teams = json.loads(blue_teams)
        blue_teams = MatchAlliance(blue_teams['teams'], blue_teams['dq'], blue_teams['surrogate'])
        return MatchSimple(key, level, set_number, match_number, red_score, blue_score,
                           red_teams, blue_teams, winner,
                           scheduled_time, predicted_time, actual_time)

    def _delete_match_simple(self, match_key: str) -> None:
        self.__connection.execute('DELETE FROM match_simple WHERE key = ?', [match_key])
        self.__connection.commit()


    # Todo: Remove
    def is_cached(self, path: list[str], file: str) -> bool:
        return False

    def save(self, path: list[str], file: str, data: any) -> None:
        # print(f"Saving {os.path.join(*path, file)}: {data}")
        return None

    def get(self, path: list[str], file: str) -> any:
        # print(f"Getting {os.path.join(*path, file)}")
        return None
