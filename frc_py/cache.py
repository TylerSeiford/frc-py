from datetime import datetime, timedelta
import os
import sqlite3
import json
from .models import Location, Team, EventSimple, MatchAlliance, MatchSimple



class Cache:
    def __init__(self, cache_dir: str = './cache'):
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        self.__connection = sqlite3.connect(os.path.join(cache_dir, 'cache.db'))
        self.__init_team()
        self.__init_event_simple()
        self.__init_match_simple()


    def __init_team(self) -> None:
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

    def get_team(self, team_key: str, cache_expiry) -> Team | None:
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


    def __init_event_simple(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS event_simple (
            last_updated datetime,
            key text, name text,
            city text, state_prov text, country text,
            type text,
            start_date datetime, end_date datetime,
            event_district text
        )''')
        self.__connection.commit()

    def save_event_simple(self, event: EventSimple) -> None:
        location = event.location()
        start, end = event.dates()
        self.__connection.execute('INSERT INTO event_simple VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            event.key(), event.name(),
            location.city(), location.state_prov(), location.country(),
            event.event_type(),
            start, end,
            event.district_key()
        ))
        self.__connection.commit()

    def get_event_simple(self, event_key: str, cache_expiry) -> EventSimple | None:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM event_simple WHERE key = ?', [event_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        timestamp, key, name, city, state_prov, country, event_type, start, end, event_district = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_event_simple(event_key)
            return None
        return EventSimple(key, name, Location(city, state_prov, country), event_type, (start, end), event_district)

    def _delete_event_simple(self, event_key: str) -> None:
        self.__connection.execute('DELETE FROM event_simple WHERE key = ?', [event_key])
        self.__connection.commit()


    def __init_match_simple(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS match_simple (
            last_updated datetime,
            key text, level text, set_number int, match_number text,
            red_score int, blue_score int,
            red_teams text, blue_teams text,
            winner text,
            scheduled_time datetime, predicted_time datetime, actual_time datetime
        )''')
        self.__connection.commit()

    def save_match_simple(self, match: MatchSimple) -> None:
        self.__connection.execute('INSERT INTO match_simple VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            match.key(), match.level(), match.set_number(), match.match_number(),
            match.red_score(), match.blue_score(),
            match.red_teams().toJSON(), match.blue_teams().toJSON(),
            match.winner(),
            match.schedule_time(), match.predicted_time(), match.actual_time()
        ))
        self.__connection.commit()

    def get_match_simple(self, match_key: str, cache_expiry) -> MatchSimple | None:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM match_simple WHERE key = ?', [match_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        timestamp, key, level, set_number, match_number, red_score, blue_score, red_teams, blue_teams, winner, scheduled_time, predicted_time, actual_time = result
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
