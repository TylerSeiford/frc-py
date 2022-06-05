'''
Classes for the models in this library.
'''
import datetime
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
            elo_start: float, elo_pre_champs: float, elo_end: float,
            elo_mean: float, elo_max: float, elo_diff: float,
            opr: float, opr_auto: float, opr_teleop: float, opr_1: float, opr_2: float,
            opr_endgame: float, opr_fouls: float, opr_no_fouls: float,
            ils_1: float, ils_2: float,
            wins: int, losses: int, ties: int, count: int,
            winrate: float,
            elo_rank: int, elo_percentile: float,
            opr_rank: int, opr_percentile: float
    ) -> None:
        self.__team_key = team_key
        self.__year = year
        self.__elo_start = elo_start
        self.__elo_pre_champs = elo_pre_champs
        self.__elo_end = elo_end
        self.__elo_mean = elo_mean
        self.__elo_max = elo_max
        self.__elo_diff = elo_diff
        self.__opr = opr
        self.__opr_auto = opr_auto
        self.__opr_teleop = opr_teleop
        self.__opr_1 = opr_1
        self.__opr_2 = opr_2
        self.__opr_endgame = opr_endgame
        self.__opr_fouls = opr_fouls
        self.__opr_no_fouls = opr_no_fouls
        self.__ils_1 = ils_1
        self.__ils_2 = ils_2
        self.__wins = wins
        self.__losses = losses
        self.__ties = ties
        self.__count = count
        self.__winrate = winrate
        self.__elo_rank = elo_rank
        self.__elo_percentile = elo_percentile
        self.__opr_rank = opr_rank
        self.__opr_percentile = opr_percentile

    def team_key(self) -> str:
        '''Returns the key of this team'''
        return self.__team_key

    def year(self) -> int:
        '''Returns the year of this team'''
        return self.__year

    def elo_start(self) -> float:
        '''Returns the starting elo of this team'''
        return self.__elo_start

    def elo_pre_champs(self) -> float:
        '''Returns the elo before the championship of this team'''
        return self.__elo_pre_champs

    def elo_end(self) -> float:
        '''Returns the ending elo of this team'''
        return self.__elo_end

    def elo_mean(self) -> float:
        '''Returns the mean elo of this team'''
        return self.__elo_mean

    def elo_max(self) -> float:
        '''Returns the max elo of this team'''
        return self.__elo_max

    def elo_diff(self) -> float:
        '''Returns the elo difference of this team'''
        return self.__elo_diff

    def opr(self) -> float:
        '''Returns the opr of this team'''
        return self.__opr

    def opr_auto(self) -> float:
        '''Returns the opr auto of this team'''
        return self.__opr_auto

    def opr_teleop(self) -> float:
        '''Returns the opr teleop of this team'''
        return self.__opr_teleop

    def opr_1(self) -> float:
        '''Returns the opr 1 of this team'''
        return self.__opr_1

    def opr_2(self) -> float:
        '''Returns the opr 2 of this team'''
        return self.__opr_2

    def opr_endgame(self) -> float:
        '''Returns the opr endgame of this team'''
        return self.__opr_endgame

    def opr_fouls(self) -> float:
        '''Returns the opr fouls of this team'''
        return self.__opr_fouls

    def opr_no_fouls(self) -> float:
        '''Returns the opr no fouls of this team'''
        return self.__opr_no_fouls

    def ils_1(self) -> float:
        '''Returns the ils 1 of this team'''
        return self.__ils_1

    def ils_2(self) -> float:
        '''Returns the ils 2 of this team'''
        return self.__ils_2

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

    def elo_rank(self) -> int:
        '''Returns the elo rank of this team'''
        return self.__elo_rank

    def elo_percentile(self) -> float:
        '''Returns the elo percentile of this team'''
        return self.__elo_percentile

    def opr_rank(self) -> int:
        '''Returns the opr rank of this team'''
        return self.__opr_rank

    def opr_percentile(self) -> float:
        '''Returns the opr percentile of this team'''
        return self.__opr_percentile


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
            address: str, postal_code: str, gmaps_place_id: str, gmaps_url: str,
            lat: float, lng: float, location_name: str, timezone: str,
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

    def dates(self) -> tuple[str, str]:
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

    def address(self) -> str:
        '''Returns the address of this event'''
        return self.__address

    def postal_code(self) -> str:
        '''Returns the postal code of this event'''
        return self.__postal_code

    def gmaps_place_id(self) -> str:
        '''Returns the Google Maps Place ID of this event'''
        return self.__gmaps_place_id

    def gmaps_url(self) -> str:
        '''Returns the Google Maps URL of this event'''
        return self.__gmaps_url

    def lat(self) -> float:
        '''Returns the latitude of this event'''
        return self.__lat

    def lng(self) -> float:
        '''Returns the longitude of this event'''
        return self.__lng

    def location_name(self) -> str:
        '''Returns the location name of this event'''
        return self.__location_name

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
            videos = list[MatchVideo]):
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
