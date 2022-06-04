from datetime import datetime, timedelta
import os
import sqlite3
import json
from .models import TeamSimple, Team, EventSimple, MatchSimple



class Cache:
    def __init__(self, cache_dir: str = './cache'):
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        self.__connection = sqlite3.connect(os.path.join(cache_dir, 'cache.db'))
        self.__init_team_simple()
        self.__init_team()
        self.__init_event_simple()
        self.__init_match_simple()


    def __init_team_simple(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS team_simple (
            last_updated datetime,
            key text, nickname text, name text,
            city text, state_prov text, country text
        )''')
        self.__connection.commit()

    def save_team_simple(self, team: TeamSimple) -> None:
        city, state_prov, country = team.get_location()
        self.__connection.execute('INSERT INTO team_simple VALUES (?, ?, ?, ?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            team.get_key(), team.get_nickname(), team.get_name(),
            city, state_prov, country
        ))
        self.__connection.commit()

    def get_team_simple(self, team_key: str, cache_expiry) -> TeamSimple | None:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM team_simple WHERE key = ?', [team_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        timestamp, key, nickname, name, city, state_prov, country = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_team_simple(team_key)
            return None
        return TeamSimple(key, nickname, name, (city, state_prov, country))

    def _delete_team_simple(self, team_key: str) -> None:
        self.__connection.execute('DELETE FROM team_simple WHERE key = ?', team_key)
        self.__connection.commit()


    def __init_team(self) -> None:
        self.__connection.execute('''CREATE TABLE IF NOT EXISTS team (
            last_updated datetime,
            key text, school_name text, website text,
            rookie_year text, motto text
        )''')
        self.__connection.commit()

    def save_team(self, team: Team) -> None:
        self.__connection.execute('INSERT INTO team VALUES (?, ?, ?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            team.get_key(), team.get_school_name(), team.get_website(),
            team.get_rookie_year(), team.get_motto()
        ))
        self.__connection.commit()

    def get_team(self, team_key: str, cache_expiry) -> Team | None:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM team WHERE key = ?', [team_key])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        timestamp, key, school_name, website, rookie_year, motto = result
        timestamp = datetime.fromisoformat(timestamp)
        if timestamp + timedelta(days=cache_expiry) < datetime.utcnow():
            self._delete_team(team_key)
            return None
        return Team(key, school_name, website, rookie_year, motto)

    def _delete_team(self, team_key: str) -> None:
        self.__connection.execute('DELETE FROM team WHERE key = ?', [team_key])
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
        city, state_prov, country = event.get_location()
        start, end = event.get_dates()
        self.__connection.execute('INSERT INTO event_simple VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            datetime.utcnow().isoformat(),
            event.get_key(), event.get_name(),
            city, state_prov, country,
            event.get_type(),
            start, end,
            event.get_district_key()
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
        return EventSimple(key, name, (city, state_prov, country), event_type, (start, end), event_district)

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
            match.get_key(), match.get_level(), match.get_set_number(), match.get_match_number(),
            match.get_red_score(), match.get_blue_score(),
            json.dumps(match.get_red_teams()), json.dumps(match.get_blue_teams()),
            match.get_winner(),
            match.get_schedule_time(), match.get_predicted_time(), match.get_actual_time()
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
        return MatchSimple(key, level, set_number, match_number, red_score, blue_score,
                           json.loads(red_teams), json.loads(blue_teams), winner,
                           scheduled_time, predicted_time, actual_time)

    def _delete_match_simple(self, match_key: str) -> None:
        self.__connection.execute('DELETE FROM match_simple WHERE key = ?', [match_key])
        self.__connection.commit()


    # Todo: Remove
    def is_cached(self, path: list[str], file: str) -> bool:
        return False

    def save(self, path: list[str], file: str, data: any) -> None:
        print(f"Saving {os.path.join(*path, file)}: {data}")
        return None
