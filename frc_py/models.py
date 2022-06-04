import datetime
import json



class Location:
    def __init__(self, city: str, state_prov: str, country: str):
        self.__city = city
        self.__state_prov = state_prov
        self.__country = country

    def city(self) -> str:
        return self.__city

    def state_prov(self) -> str:
        return self.__state_prov

    def country(self) -> str:
        return self.__country

    def __str__(self) -> str:
        return f"{self.__city}, {self.__state_prov}, {self.__country}"


class TeamSimple:
    def __init__(self, key: str, nickname: str, name: str, location: Location):
        self.__key = key
        self.__nickname = nickname
        self.__name = name
        self.__location = location

    def get_key(self) -> str:
        return self.__key

    def get_nickname(self) -> str:
        return self.__nickname

    def get_name(self) -> str:
        return self.__name

    def get_location(self) -> Location:
        return self.__location


class Team:
    def __init__(self, key: str, school_name: str, website: str, rookie_year: str, motto: str):
        self.__key = key
        self.__school_name = school_name
        self.__website = website
        self.__rookie_year = rookie_year
        self.__motto = motto

    def key(self) -> str:
        return self.__key

    def school_name(self) -> str:
        return self.__school_name

    def website(self) -> str:
        return self.__website

    def rookie_year(self) -> str:
        return self.__rookie_year

    def motto(self) -> str:
        return self.__motto


class EventSimple:
    def __init__(self, key: str, name: str, location: Location, event_type: int, dates: tuple[str, str],
            district_key: str):
        self.__key = key
        self.__name = name
        self.__location = location
        self.__type = event_type
        self.__dates = dates
        self.__district_key = district_key

    def key(self) -> str:
        return self.__key

    def name(self) -> str:
        return self.__name

    def location(self) -> Location:
        return self.__location

    def event_type(self) -> int:
        return self.__type

    def dates(self) -> tuple[str, str]:
        return self.__dates

    def district_key(self) -> str:
        return self.__district_key


class MatchAlliance:
    def __init__(self, teams: list[str], dq: list[str], surrogate: list[str]):
        self.__teams = teams
        self.__dq = dq
        self.__surrogate = surrogate

    def teams(self) -> list[str]:
        return self.__teams

    def dq(self) -> list[str]:
        return self.__dq

    def surrogate(self) -> list[str]:
        return self.__surrogate

    def __str__(self) -> str:
        return f"{self.__teams}, {self.__dq}, {self.__surrogate}"

    def toJSON(self) -> str:
        return json.dumps({
            'teams': self.__teams,
            'dq': self.__dq,
            'surrogate': self.__surrogate
        })


class MatchSimple:
    def __init__(self, key: str, level: str, set_number: int, match_number: int,
            red_score: int, blue_score: int,
            red_teams: MatchAlliance, blue_teams: MatchAlliance,
            winner: str,
            schedule_time: datetime, predicted_time: datetime, actual_time: datetime):
        self.__key = key
        self.__level = level
        self.__set_number = set_number
        self.__match_number = match_number
        self.__red_score = red_score
        self.__blue_score = blue_score
        self.__red_teams = red_teams
        self.__blue_teams = blue_teams
        self.__winner = winner
        self.__schedule_time = schedule_time
        self.__predicted_time = predicted_time
        self.__actual_time = actual_time

    def key(self) -> str:
        return self.__key

    def level(self) -> str:
        return self.__level

    def set_number(self) -> int:
        return self.__set_number

    def match_number(self) -> int:
        return self.__match_number

    def red_score(self) -> int:
        return self.__red_score

    def blue_score(self) -> int:
        return self.__blue_score

    def red_teams(self) -> MatchAlliance:
        return self.__red_teams

    def blue_teams(self) -> MatchAlliance:
        return self.__blue_teams

    def winner(self) -> str:
        return self.__winner

    def schedule_time(self) -> datetime:
        return self.__schedule_time

    def predicted_time(self) -> datetime:
        return self.__predicted_time

    def actual_time(self) -> datetime:
        return self.__actual_time
