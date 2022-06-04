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


class Team:
    @staticmethod
    def team_key_to_number(team_key: str) -> int:
        return int(team_key[3:])


    def __init__(self, key: str, nickname: str, name: str, location: Location,
            school_name: str, website: str, rookie_year: str, motto: str):
        self.__key = key
        self.__nickname = nickname
        self.__name = name
        self.__location = location
        self.__school_name = school_name
        self.__website = website
        self.__rookie_year = rookie_year
        self.__motto = motto

    def key(self) -> str:
        return self.__key

    def nickname(self) -> str:
        return self.__nickname

    def name(self) -> str:
        return self.__name

    def location(self) -> Location:
        return self.__location

    def school_name(self) -> str:
        return self.__school_name

    def website(self) -> str:
        return self.__website

    def rookie_year(self) -> str:
        return self.__rookie_year

    def motto(self) -> str:
        return self.__motto


class Webcast:
    def __init__(self, webcast_type: str, channel: str, date: str, file: str):
        self.__type = webcast_type
        self.__channel = channel
        self.__date = date
        self.__file = file

    def webcast_type(self) -> str:
        return self.__type

    def channel(self) -> str:
        return self.__channel

    def date(self) -> str | None:
        return self.__date

    def file(self) -> str | None:
        return self.__file

    def __str__(self) -> str:
        return f"{self.__type} {self.__channel} {self.__date} {self.__file}"

    def to_json(self) -> str:
        return json.dumps({
            'type': self.__type,
            'channel': self.__channel,
            'date': self.__date,
            'file': self.__file
        })


class Event:
    @staticmethod
    def event_key_to_year(event_key: str) -> int:
        return int(event_key[:4])


    def __init__(self, key: str, name: str, location: Location, event_type: int,
            dates: tuple[str, str], district_key: str, short_name: str, week: int,
            address: str, postal_code: str, gmaps_place_id: str, gmaps_url: str,
            lat: float, lng: float, location_name: str, timezone: str,
            website: str, first_event_id: str, first_event_code: str,
            webcasts: list[Webcast], divisions: list[str], parent_event_key: str, playoff_type: int):
        self.__key = key
        self.__name = name
        self.__location = location
        self.__type = event_type
        self.__dates = dates
        self.__district_key = district_key
        self.__short_name = short_name
        self.__week = week
        self.__address = address
        self.__postal_code = postal_code
        self.__gmaps_place_id = gmaps_place_id
        self.__gmaps_url = gmaps_url
        self.__lat = lat
        self.__lng = lng
        self.__location_name = location_name
        self.__timezone = timezone
        self.__website = website
        self.__first_event_id = first_event_id
        self.__first_event_code = first_event_code
        self.__webcasts = webcasts
        self.__divisions = divisions
        self.__parent_event_key = parent_event_key
        self.__playoff_type = playoff_type

    def key(self) -> str:
        return self.__key

    def name(self) -> str:
        return self.__name

    def location(self) -> Location:
        return self.__location

    def event_type(self) -> int:
        return self.__type

    def event_type_str(self) -> str:
        match(self.__type):
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

    def is_district_event(self) -> bool:
        return self.event_type_str() in {
            'District',
            'District Championship',
            'District Championship Division'
        }

    def is_non_championship_event(self) -> bool:
        return self.event_type_str() in {
            'Regional',
            'District',
            'District Championship',
            'District Championship Division',
            'Remote'
        }

    def is_championship_event(self) -> bool:
        return self.event_type_str() in {
            'Championship Division',
            'Einstein'
        }

    def is_season_event(self) -> bool:
        return self.event_type_str() in {
            'Regional',
            'District',
            'District Championship',
            'District Championship Division',
            'Championship Division',
            'Einstein',
            'Festival of Champions',
            'Remote'
        }

    def dates(self) -> tuple[str, str]:
        return self.__dates

    def district_key(self) -> str:
        return self.__district_key

    def short_name(self) -> str:
        return self.__short_name

    def week(self) -> int:
        return self.__week

    def address(self) -> str:
        return self.__address

    def postal_code(self) -> str:
        return self.__postal_code

    def gmaps_place_id(self) -> str:
        return self.__gmaps_place_id

    def gmaps_url(self) -> str:
        return self.__gmaps_url

    def lat(self) -> float:
        return self.__lat

    def lng(self) -> float:
        return self.__lng

    def location_name(self) -> str:
        return self.__location_name

    def timezone(self) -> str:
        return self.__timezone

    def website(self) -> str:
        return self.__website

    def first_event_id(self) -> str:
        return self.__first_event_id

    def first_event_code(self) -> str:
        return self.__first_event_code

    def webcasts(self) -> list[Webcast]:
        return self.__webcasts

    def divisions(self) -> list[str]:
        return self.__divisions

    def parent_event_key(self) -> str:
        return self.__parent_event_key

    def playoff_type(self) -> int:
        return self.__playoff_type

    def playoff_type_str(self) -> str:
        match(self.__playoff_type):
            case 0:
                return 'Elimination Bracket (8 Alliances)'
            case 1:
                return 'Elimination Bracket (16 Alliances)'
            case 2:
                return 'Elimination Bracket (4 Alliances)'
            case 3:
                return 'Average Score (8 Alliances)'
            case 4:
                return 'Round Robin (8 Alliances)'
            case 5:
                return 'Double Elimination Bracket (8 Alliances)'
            case 6:
                return 'Best of 3 Finals'
            case 7:
                return 'Best of 5 Finals'
            case 8:
                return 'Custom'

    def is_bracket_event(self) -> bool:
        return self.playoff_type_str() in {
            'Elimination Bracket (8 Alliances)',
            'Elimination Bracket (16 Alliances)',
            'Elimination Bracket (4 Alliances)'
        }

    def is_double_elimination_event(self) -> bool:
        return self.playoff_type_str() in {
            'Double Elimination Bracket (8 Alliances)'
        }


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

    def to_json(self) -> str:
        return json.dumps({
            'teams': self.__teams,
            'dq': self.__dq,
            'surrogate': self.__surrogate
        })


class MatchSimple: # Todo: Convert to full match
    @staticmethod
    def match_key_to_year(match_key: str) -> int:
        return int(match_key[:4])

    @staticmethod
    def match_key_to_event(match_key: str) -> str:
        return match_key.split('_')[0]


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
