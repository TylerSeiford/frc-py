import datetime



class TeamSimple:
    def __init__(self, key: str, nickname: str, name: str, location: tuple[str, str, str]):
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

    def get_location(self) -> tuple[str, str, str]:
        return self.__location


class Team:
    def __init__(self, key: str, school_name: str, website: str, rookie_year: str, motto: str):
        self.__key = key
        self.__school_name = school_name
        self.__website = website
        self.__rookie_year = rookie_year
        self.__motto = motto

    def get_key(self) -> str:
        return self.__key

    def get_school_name(self) -> str:
        return self.__school_name

    def get_website(self) -> str:
        return self.__website

    def get_rookie_year(self) -> str:
        return self.__rookie_year

    def get_motto(self) -> str:
        return self.__motto


class EventSimple:
    def __init__(self, key: str, name: str, location: tuple[str, str, str], event_type: str, dates: tuple[str, str],
            district_key: str):
        self.__key = key
        self.__name = name
        self.__location = location
        self.__type = event_type
        self.__dates = dates
        self.__district_key = district_key

    def get_key(self) -> str:
        return self.__key

    def get_name(self) -> str:
        return self.__name

    def get_location(self) -> tuple[str, str, str]:
        return self.__location

    def get_type(self) -> str:
        return self.__type

    def get_dates(self) -> tuple[str, str]:
        return self.__dates

    def get_district_key(self) -> str:
        return self.__district_key


class MatchSimple:
    def __init__(self, key: str, level: str, set_number: int, match_number: int,
            red_score: int, blue_score: int,
            red_teams: dict[str, list[str]], blue_teams: dict[str, list[str]],
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

    def get_key(self) -> str:
        return self.__key

    def get_level(self) -> str:
        return self.__level

    def get_set_number(self) -> int:
        return self.__set_number

    def get_match_number(self) -> int:
        return self.__match_number

    def get_red_score(self) -> int:
        return self.__red_score

    def get_blue_score(self) -> int:
        return self.__blue_score

    def get_red_teams(self) -> dict[str, list[str]]:
        return self.__red_teams

    def get_blue_teams(self) -> dict[str, list[str]]:
        return self.__blue_teams

    def get_winner(self) -> str:
        return self.__winner

    def get_schedule_time(self) -> datetime:
        return self.__schedule_time

    def get_predicted_time(self) -> datetime:
        return self.__predicted_time

    def get_actual_time(self) -> datetime:
        return self.__actual_time
