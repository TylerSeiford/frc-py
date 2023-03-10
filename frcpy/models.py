'''
Classes for the models in this library.
'''
from datetime import datetime
import json


class Location:
    '''
    Represents a team or event's location.
    '''

    def __init__(self, city: str, state_prov: str, country: str):
        self.__city = city
        self.__state_prov = state_prov
        self.__country = country

    def city(self) -> str:
        '''Returns the city of this location'''
        return self.__city

    def state_prov(self) -> str:
        '''Returns the state or province of this location'''
        return self.__state_prov

    def country(self) -> str:
        '''Returns the country of this location'''
        return self.__country

    def __str__(self) -> str:
        '''Returns a string representation of this location'''
        return f"{self.__city, self.__state_prov, self.__country}"


class PreciseLocation:
    '''
    Represents the precise location of a team or event.
    '''

    def __init__(self, location: Location, latitude: float, longitude: float,
                 address: str, postal_code: str | None, place_id: str):
        self.__location = location
        self.__latitude = latitude
        self.__longitude = longitude
        self.__address = address
        self.__postal_code = postal_code
        self.__place_id = place_id

    def location(self) -> Location:
        '''Returns the location of this precise location'''
        return self.__location

    def latitude(self) -> float:
        '''Returns the latitude of this precise location'''
        return self.__latitude

    def longitude(self) -> float:
        '''Returns the longitude of this precise location'''
        return self.__longitude

    def address(self) -> str:
        '''Returns the address of this team'''
        return self.__address

    def postal_code(self) -> str | None:
        '''Returns the postal code of this precise location'''
        return self.__postal_code

    def place_id(self) -> str:
        '''Returns the place ID of this team'''
        return self.__place_id

    def lat_lng(self) -> tuple[float, float]:
        '''Returns a tuple of latitude and longitude of this precise location'''
        return self.__latitude, self.__longitude


class Team:
    '''
    Represents a team
    '''
    @staticmethod
    def team_key_to_number(team_key: str) -> int:
        '''Converts a team key to a team number'''
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
        '''Returns the key of this team'''
        return self.__key

    def nickname(self) -> str:
        '''Returns the nickname of this team'''
        return self.__nickname

    def name(self) -> str:
        '''Returns the name of this team'''
        return self.__name

    def location(self) -> Location:
        '''Returns the location of this team'''
        return self.__location

    def school_name(self) -> str:
        '''Returns the school name of this team'''
        return self.__school_name

    def website(self) -> str:
        '''Returns the website of this team'''
        return self.__website

    def rookie_year(self) -> str:
        '''Returns the rookie year of this team'''
        return self.__rookie_year

    def motto(self) -> str:
        '''Returns the motto of this team'''
        return self.__motto


class TeamYearStats:
    '''
    Represents a team's statistics for a single year
    '''

    def __init__(self, team_key: str, year: int,
                 epa_start: float, epa_pre_champs: float, epa_end: float,
                 epa_mean: float, epa_max: float, epa_diff: float,
                 auto_epa_start: float, auto_epa_pre_champs: float, auto_epa_end: float, auto_epa_mean: float, auto_epa_max: float,
                 teleop_epa_start: float, teleop_epa_pre_champs: float, teleop_epa_end: float, teleop_epa_mean: float, teleop_epa_max: float,
                 endgame_epa_start: float, endgame_epa_pre_champs: float, endgame_epa_end: float, endgame_epa_mean: float, endgame_epa_max: float,
                 rp_1_epa_start: float, rp_1_epa_pre_champs: float, rp_1_epa_end: float, rp_1_epa_mean: float, rp_1_epa_max: float,
                 rp_2_epa_start: float, rp_2_epa_pre_champs: float, rp_2_epa_end: float, rp_2_epa_mean: float, rp_2_epa_max: float,
                 norm_epa_end: float,
                 wins: int, losses: int, ties: int, count: int, winrate: float,
                 epa_rank: float, epa_percent: float
                 ) -> None:
        self.__team_key = team_key
        self.__year = year
        self.__epa_start = epa_start
        self.__epa_pre_champs = epa_pre_champs
        self.__epa_end = epa_end
        self.__epa_mean = epa_mean
        self.__epa_max = epa_max
        self.__epa_diff = epa_diff
        self.__auto_epa_start = auto_epa_start
        self.__auto_epa_pre_champs = auto_epa_pre_champs
        self.__auto_epa_end = auto_epa_end
        self.__auto_epa_mean = auto_epa_mean
        self.__auto_epa_max = auto_epa_max
        self.__teleop_epa_start = teleop_epa_start
        self.__teleop_epa_pre_champs = teleop_epa_pre_champs
        self.__teleop_epa_end = teleop_epa_end
        self.__teleop_epa_mean = teleop_epa_mean
        self.__teleop_epa_max = teleop_epa_max
        self.__endgame_epa_start = endgame_epa_start
        self.__endgame_epa_pre_champs = endgame_epa_pre_champs
        self.__endgame_epa_end = endgame_epa_end
        self.__endgame_epa_mean = endgame_epa_mean
        self.__endgame_epa_max = endgame_epa_max
        self.__rp_1_epa_start = rp_1_epa_start
        self.__rp_1_epa_pre_champs = rp_1_epa_pre_champs
        self.__rp_1_epa_end = rp_1_epa_end
        self.__rp_1_epa_mean = rp_1_epa_mean
        self.__rp_1_epa_max = rp_1_epa_max
        self.__rp_2_epa_start = rp_2_epa_start
        self.__rp_2_epa_pre_champs = rp_2_epa_pre_champs
        self.__rp_2_epa_end = rp_2_epa_end
        self.__rp_2_epa_mean = rp_2_epa_mean
        self.__rp_2_epa_max = rp_2_epa_max
        self.__norm_epa_end = norm_epa_end
        self.__wins = wins
        self.__losses = losses
        self.__ties = ties
        self.__count = count
        self.__winrate = winrate
        self.__epa_rank = epa_rank
        self.__epa_percent = epa_percent

    def team_key(self) -> str:
        '''Returns the key of this team'''
        return self.__team_key

    def year(self) -> int:
        '''Returns the year of this team'''
        return self.__year

    def epa_start(self) -> float:
        return self.__epa_start

    def epa_pre_champs(self) -> float:
        return self.__epa_pre_champs

    def epa_end(self) -> float:
        return self.__epa_end

    def epa_mean(self) -> float:
        return self.__epa_mean

    def epa_max(self) -> float:
        return self.__epa_max

    def epa_diff(self) -> float:
        return self.__epa_diff

    def auto_epa_start(self) -> float:
        return self.__auto_epa_start

    def auto_epa_pre_champs(self) -> float:
        return self.__auto_epa_pre_champs

    def auto_epa_end(self) -> float:
        return self.__auto_epa_end

    def auto_epa_mean(self) -> float:
        return self.__auto_epa_mean

    def auto_epa_max(self) -> float:
        return self.__auto_epa_max

    def teleop_epa_start(self) -> float:
        return self.__teleop_epa_start

    def teleop_epa_pre_champs(self) -> float:
        return self.__teleop_epa_pre_champs

    def teleop_epa_end(self) -> float:
        return self.__teleop_epa_end

    def teleop_epa_mean(self) -> float:
        return self.__teleop_epa_mean

    def teleop_epa_max(self) -> float:
        return self.__teleop_epa_max

    def endgame_epa_start(self) -> float:
        return self.__endgame_epa_start

    def endgame_epa_pre_champs(self) -> float:
        return self.__endgame_epa_pre_champs

    def endgame_epa_end(self) -> float:
        return self.__endgame_epa_end

    def endgame_epa_mean(self) -> float:
        return self.__endgame_epa_mean

    def endgame_epa_max(self) -> float:
        return self.__endgame_epa_max

    def rp_1_epa_start(self) -> float:
        return self.__rp_1_epa_start

    def rp_1_epa_pre_champs(self) -> float:
        return self.__rp_1_epa_pre_champs

    def rp_1_epa_end(self) -> float:
        return self.__rp_1_epa_end

    def rp_1_epa_mean(self) -> float:
        return self.__rp_1_epa_mean

    def rp_1_epa_max(self) -> float:
        return self.__rp_1_epa_max

    def rp_2_epa_start(self) -> float:
        return self.__rp_2_epa_start

    def rp_2_epa_pre_champs(self) -> float:
        return self.__rp_2_epa_pre_champs

    def rp_2_epa_end(self) -> float:
        return self.__rp_2_epa_end

    def rp_2_epa_mean(self) -> float:
        return self.__rp_2_epa_mean

    def rp_2_epa_max(self) -> float:
        return self.__rp_2_epa_max

    def norm_epa_end(self) -> float:
        return self.__norm_epa_end

    def wins(self) -> int:
        '''Returns the wins of this team'''
        return self.__wins

    def losses(self) -> int:
        '''Returns the losses of this team'''
        return self.__losses

    def ties(self) -> int:
        '''Returns the ties of this team'''
        return self.__ties

    def count(self) -> int:
        '''Returns the count of this team'''
        return self.__count

    def winrate(self) -> float:
        '''Returns the winrate of this team'''
        return self.__winrate

    def epa_rank(self) -> float:
        return self.__epa_rank

    def epa_percent(self) -> float:
        return self.__epa_percent


class TeamEventStats:
    '''
    Represents a team's statistics for a single event
    '''

    def __init__(self, team_key: str, event_key: str,
                 epa_start: float, epa_pre_playoffs: float, epa_end: float,
                 epa_mean: float, epa_max: float, epa_diff: float,
                 auto_epa_start: float, auto_epa_pre_playoffs: float, auto_epa_end: float, auto_epa_mean: float, auto_epa_max: float,
                 teleop_epa_start: float, teleop_epa_pre_playoffs: float, teleop_epa_end: float, teleop_epa_mean: float, teleop_epa_max: float,
                 endgame_epa_start: float, endgame_epa_pre_playoffs: float, endgame_epa_end: float, endgame_epa_mean: float, endgame_epa_max: float,
                 rp_1_epa_start: float, rp_1_epa_end: float, rp_1_epa_mean: float, rp_1_epa_max: float,
                 rp_2_epa_start: float, rp_2_epa_end: float, rp_2_epa_mean: float, rp_2_epa_max: float,
                 wins: int, losses: int, ties: int, count: int, winrate: float,
                 rps: int, rps_per_match: float, rank: int, num_teams: int
                 ) -> None:
        self.__team_key = team_key
        self.__event_key = event_key
        self.__epa_start = epa_start
        self.__epa_pre_playoffs = epa_pre_playoffs
        self.__epa_end = epa_end
        self.__epa_mean = epa_mean
        self.__epa_max = epa_max
        self.__epa_diff = epa_diff
        self.__auto_epa_start = auto_epa_start
        self.__auto_epa_pre_playoffs = auto_epa_pre_playoffs
        self.__auto_epa_end = auto_epa_end
        self.__auto_epa_mean = auto_epa_mean
        self.__auto_epa_max = auto_epa_max
        self.__teleop_epa_start = teleop_epa_start
        self.__teleop_epa_pre_playoffs = teleop_epa_pre_playoffs
        self.__teleop_epa_end = teleop_epa_end
        self.__teleop_epa_mean = teleop_epa_mean
        self.__teleop_epa_max = teleop_epa_max
        self.__endgame_epa_start = endgame_epa_start
        self.__endgame_epa_pre_playoffs = endgame_epa_pre_playoffs
        self.__endgame_epa_end = endgame_epa_end
        self.__endgame_epa_mean = endgame_epa_mean
        self.__endgame_epa_max = endgame_epa_max
        self.__rp_1_epa_start = rp_1_epa_start
        self.__rp_1_epa_end = rp_1_epa_end
        self.__rp_1_epa_mean = rp_1_epa_mean
        self.__rp_1_epa_max = rp_1_epa_max
        self.__rp_2_epa_start = rp_2_epa_start
        self.__rp_2_epa_end = rp_2_epa_end
        self.__rp_2_epa_mean = rp_2_epa_mean
        self.__rp_2_epa_max = rp_2_epa_max
        self.__wins = wins
        self.__losses = losses
        self.__ties = ties
        self.__count = count
        self.__winrate = winrate
        self.__rps = rps
        self.__rps_per_match = rps_per_match
        self.__rank = rank
        self.__num_teams = num_teams

    def team_key(self) -> str:
        '''Returns the key of this team'''
        return self.__team_key

    def event_key(self) -> str:
        '''Returns the key of this event'''
        return self.__event_key

    def epa_start(self) -> float:
        return self.__epa_start

    def epa_pre_playoffs(self) -> float:
        return self.__epa_pre_playoffs

    def epa_end(self) -> float:
        return self.__epa_end

    def epa_mean(self) -> float:
        return self.__epa_mean

    def epa_max(self) -> float:
        return self.__epa_max

    def epa_diff(self) -> float:
        return self.__epa_diff

    def auto_epa_start(self) -> float:
        return self.__auto_epa_start

    def auto_epa_pre_playoffs(self) -> float:
        return self.__auto_epa_pre_playoffs

    def auto_epa_end(self) -> float:
        return self.__auto_epa_end

    def auto_epa_mean(self) -> float:
        return self.__auto_epa_mean

    def auto_epa_max(self) -> float:
        return self.__auto_epa_max

    def teleop_epa_start(self) -> float:
        return self.__teleop_epa_start

    def teleop_epa_pre_playoffs(self) -> float:
        return self.__teleop_epa_pre_playoffs

    def teleop_epa_end(self) -> float:
        return self.__teleop_epa_end

    def teleop_epa_mean(self) -> float:
        return self.__teleop_epa_mean

    def teleop_epa_max(self) -> float:
        return self.__teleop_epa_max

    def endgame_epa_start(self) -> float:
        return self.__endgame_epa_start

    def endgame_epa_pre_playoffs(self) -> float:
        return self.__endgame_epa_pre_playoffs

    def endgame_epa_end(self) -> float:
        return self.__endgame_epa_end

    def endgame_epa_mean(self) -> float:
        return self.__endgame_epa_mean

    def endgame_epa_max(self) -> float:
        return self.__endgame_epa_max

    def rp_1_epa_start(self) -> float:
        return self.__rp_1_epa_start

    def rp_1_epa_end(self) -> float:
        return self.__rp_1_epa_end

    def rp_1_epa_mean(self) -> float:
        return self.__rp_1_epa_mean

    def rp_1_epa_max(self) -> float:
        return self.__rp_1_epa_max

    def rp_2_epa_start(self) -> float:
        return self.__rp_2_epa_start

    def rp_2_epa_end(self) -> float:
        return self.__rp_2_epa_end

    def rp_2_epa_mean(self) -> float:
        return self.__rp_2_epa_mean

    def rp_2_epa_max(self) -> float:
        return self.__rp_2_epa_max

    def wins(self) -> int:
        return self.__wins

    def losses(self) -> int:
        return self.__losses

    def ties(self) -> int:
        return self.__ties

    def count(self) -> int:
        return self.__count

    def winrate(self) -> float:
        return self.__winrate

    def rps(self) -> int:
        return self.__rps

    def rps_per_match(self) -> float:
        return self.__rps_per_match

    def rank(self) -> int:
        return self.__rank

    def num_teams(self) -> int:
        return self.__num_teams


class Webcast:
    '''
    Represents a webcast
    '''

    def __init__(self, webcast_type: str, channel: str, date: str, file: str):
        self.__type = webcast_type
        self.__channel = channel
        self.__date = date
        self.__file = file

    def webcast_type(self) -> str:
        '''Returns the type of webcast'''
        return self.__type

    def channel(self) -> str:
        '''Returns the channel of this webcast'''
        return self.__channel

    def date(self) -> str | None:
        '''Returns the date of this webcast'''
        return self.__date

    def file(self) -> str | None:
        '''Returns the file of this webcast'''
        return self.__file

    def __str__(self) -> str:
        '''Returns a string representation of this webcast'''
        return f"{self.__type, self.__channel, self.__date, self.__file}"

    def to_json(self) -> str:
        '''Returns a JSON representation of this webcast'''
        return json.dumps({
            'type': self.__type,
            'channel': self.__channel,
            'date': self.__date,
            'file': self.__file
        })


class Event:
    '''
    Represents an event
    '''
    @staticmethod
    def event_key_to_year(event_key: str) -> int:
        '''Converts an event key to an event year'''
        return int(event_key[:4])

    def __init__(self, key: str, name: str, location: Location, event_type: int,
                 dates: tuple[str, str], district_key: str, short_name: str, week: int,
                 precise_location: PreciseLocation, location_name: str, timezone: str,
                 website: str, first_event_id: str, first_event_code: str,
                 webcasts: list[Webcast], divisions: list[str],
                 parent_event_key: str, playoff_type: int):
        self.__key = key
        self.__name = name
        self.__location = location
        self.__type = event_type
        self.__dates = dates
        self.__district_key = district_key
        self.__short_name = short_name
        self.__week = week
        self.__location_name = location_name
        self.__precise_location = precise_location
        self.__timezone = timezone
        self.__website = website
        self.__first_event_id = first_event_id
        self.__first_event_code = first_event_code
        self.__webcasts = webcasts
        self.__divisions = divisions
        self.__parent_event_key = parent_event_key
        self.__playoff_type = playoff_type

    def key(self) -> str:
        '''Returns the key of this event'''
        return self.__key

    def name(self) -> str:
        '''Returns the name of this event'''
        return self.__name

    def location(self) -> Location:
        '''Returns the location of this event'''
        return self.__location

    def event_type(self) -> int:
        '''Returns the event type of this event'''
        return self.__type

    def event_type_str(self) -> str:
        '''Returns the event type of this event as a string'''
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
        '''Returns whether this event is a district event'''
        return self.event_type_str() in {
            'District',
            'District Championship',
            'District Championship Division'
        }

    def is_non_championship_event(self) -> bool:
        '''Returns whether this event is a non-championship, in-season event'''
        return self.event_type_str() in {
            'Regional',
            'District',
            'District Championship',
            'District Championship Division',
            'Remote'
        }

    def is_championship_event(self) -> bool:
        '''Returns whether this event is a championship event'''
        return self.event_type_str() in {
            'Championship Division',
            'Einstein'
        }

    def is_season_event(self) -> bool:
        '''Returns whether this event is a season event'''
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

    def dates(self) -> tuple[datetime, datetime]:
        '''Returns the dates of this event'''
        return self.__dates

    def district_key(self) -> str:
        '''Returns the district key of this event'''
        return self.__district_key

    def short_name(self) -> str:
        '''Returns the short name of this event'''
        return self.__short_name

    def week(self) -> int:
        '''Returns the week of this event'''
        return self.__week

    def location_name(self) -> str:
        '''Returns the location name of this event'''
        return self.__location_name

    def precise_location(self) -> PreciseLocation:
        '''Returns the precise location of this event'''
        return self.__precise_location

    def timezone(self) -> str:
        '''Returns the timezone of this event'''
        return self.__timezone

    def website(self) -> str:
        '''Returns the website of this event'''
        return self.__website

    def first_event_id(self) -> str:
        '''Returns the FIRST event ID of this event'''
        return self.__first_event_id

    def first_event_code(self) -> str:
        '''Returns the FIRST event code of this event'''
        return self.__first_event_code

    def webcasts(self) -> list[Webcast]:
        '''Returns the webcasts of this event'''
        return self.__webcasts

    def divisions(self) -> list[str]:
        '''Returns the divisions of this event'''
        return self.__divisions

    def parent_event_key(self) -> str:
        '''Returns the parent event key of this event'''
        return self.__parent_event_key

    def playoff_type(self) -> int:
        '''Returns the playoff type of this event'''
        return self.__playoff_type

    def playoff_type_str(self) -> str:
        '''Returns the playoff type of this event as a string'''
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
        '''Returns whether this event is a bracket event'''
        return self.playoff_type_str() in {
            'Elimination Bracket (8 Alliances)',
            'Elimination Bracket (16 Alliances)',
            'Elimination Bracket (4 Alliances)'
        }

    def is_double_elimination_event(self) -> bool:
        '''Returns whether this event is a double elimination event'''
        return self.playoff_type_str() in {
            'Double Elimination Bracket (8 Alliances)'
        }


class MatchAlliance:
    '''
    Represents an alliance in a match
    '''

    def __init__(self, teams: list[str], disqualified: list[str], surrogate: list[str]):
        self.__teams = teams
        self.__dq = disqualified
        self.__surrogate = surrogate

    def teams(self) -> list[str]:
        '''Returns the teams in this alliance'''
        return self.__teams

    def disqualified(self) -> list[str]:
        '''Returns the disqualified teams in this alliance'''
        return self.__dq

    def surrogate(self) -> list[str]:
        '''Returns the surrogate teams in this alliance'''
        return self.__surrogate

    def __str__(self) -> str:
        '''Returns a string representation of this alliance'''
        return f"{self.__teams, self.__dq, self.__surrogate}"

    def to_json(self) -> str:
        '''Returns a JSON representation of this alliance'''
        return json.dumps({
            'teams': self.__teams,
            'dq': self.__dq,
            'surrogate': self.__surrogate
        })


class MatchVideo:
    '''
    Represents a video of a match
    '''

    def __init__(self, video_type: str, key: str):
        self.__type = video_type
        self.__key = key

    def video_type(self) -> str:
        '''Returns the video type of this video'''
        return self.__type

    def key(self) -> str:
        '''Returns the key of this video'''
        return self.__key

    def __str__(self) -> str:
        '''Returns a string representation of this video'''
        return f"{self.__type, self.__key}"

    def to_json(self) -> str:
        '''Returns a JSON representation of this video'''
        return json.dumps({
            'type': self.__type,
            'key': self.__key
        })


class Match:
    '''
    Represents a match
    '''
    @staticmethod
    def match_key_to_year(match_key: str) -> int:
        '''Converts a match key to a year'''
        return int(match_key[:4])

    @staticmethod
    def match_key_to_event(match_key: str) -> str:
        '''Converts a match key to an event key'''
        return match_key.split('_')[0]

    def __init__(self, key: str, level: str, set_number: int, match_number: int,
                 red_score: int, blue_score: int,
                 red_teams: MatchAlliance, blue_teams: MatchAlliance,
                 winner: str,
                 schedule_time: datetime, predicted_time: datetime,
                 actual_time: datetime, result_time: datetime,
                 videos=list[MatchVideo]):
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
        self.__result_time = result_time
        self.__videos = videos
        # TODO: Add score breakdowns

    def key(self) -> str:
        '''Returns the key of this match'''
        return self.__key

    def level(self) -> str:
        '''Returns the level of this match'''
        return self.__level

    def set_number(self) -> int:
        '''Returns the set number of this match'''
        return self.__set_number

    def match_number(self) -> int:
        '''Returns the match number of this match'''
        return self.__match_number

    def red_score(self) -> int:
        '''Returns the red score of this match'''
        return self.__red_score

    def blue_score(self) -> int:
        '''Returns the blue score of this match'''
        return self.__blue_score

    def red_teams(self) -> MatchAlliance:
        '''Returns the red alliance of this match'''
        return self.__red_teams

    def blue_teams(self) -> MatchAlliance:
        '''Returns the blue alliance of this match'''
        return self.__blue_teams

    def winner(self) -> str:
        '''Returns the winner of this match'''
        return self.__winner

    def schedule_time(self) -> datetime:
        '''Returns the schedule time of this match'''
        return self.__schedule_time

    def predicted_time(self) -> datetime:
        '''Returns the predicted time of this match'''
        return self.__predicted_time

    def actual_time(self) -> datetime:
        '''Returns the actual time of this match'''
        return self.__actual_time

    def result_time(self) -> datetime:
        '''Returns the result time of this match'''
        return self.__result_time

    def videos(self) -> list[MatchVideo]:
        '''Returns the videos of this match'''
        return self.__videos
