'''
Example on how to use the library.
'''
import os
from frc_py import FRCPy



if __name__ == '__main__':
    TOKEN = os.environ['SECRET_TBA_TOKEN'] # Replace with your TBA token
    with FRCPy(TOKEN) as api:
        print('***** Teams *****')
        teams: list[str] = api.teams()
        print(f"Found {len(teams)} teams")
        print(f"Years: {api.team_years('frc2501')}")
        team = api.team('frc2501')
        print(f"Location: {team.location()}")
        print(f"Nickname: {team.nickname()}")
        print(f"Name: {team.name()}")
        print(f"School: {team.school_name()}")
        print(f"Website: {team.website()}")
        print(f"Rookie Year: {team.rookie_year()}")
        print(f"Motto: {team.motto()}")
        for year in api.team_years('frc2501'):
            print(f"{year}: {api.team_year_events('frc2501', year)}")

        print('***** Events *****')
        min_year, max_year = api.year_range()
        for year in range(min_year, max_year + 1):
            print(f"{year}: {len(api.year_events(year))}")
        event = api.event('2022mndu')
        print(f"Name: {event.name()}")
        print(f"Location: {event.location()}")
        print(f"Type: {event.event_type_str()}")
        print(f"Dates: {event.dates()}")
        print(f"District: {event.district_key()}")
        print(f"Short Name: {event.short_name()}")
        print(f"Week: {event.week()}")
        print(f"Address: {event.address()}")
        print(f"Postal Code: {event.postal_code()}")
        print(f"Google Maps Place ID: {event.gmaps_place_id()}")
        print(f"Google Maps URL: {event.gmaps_url()}")
        print(f"Latitude: {event.lat()}")
        print(f"Longitude: {event.lng()}")
        print(f"Location Name: {event.location_name()}")
        print(f"Timezome: {event.timezone()}")
        print(f"Website: {event.website()}")
        print(f"First Event ID: {event.first_event_id()}")
        print(f"First Event Code: {event.first_event_code()}")
        # Python doesn't automatically format each object in the list as a string
        webcasts = []
        for webcast in event.webcasts():
            webcasts.append(f"{webcast}")
        print(f"Webcasts: {webcasts}")
        print(f"Divisions: {event.divisions()}")
        print(f"Parent event: {event.parent_event_key()}")
        print(f"Playoff Type: {event.playoff_type_str()}")
        print(f"Teams: {len(api.event_teams('2022mndu'))}")
        print(f"Matches: {len(api.event_matches('2022mndu'))}")

        print('***** Team @ Event *****')
        print(f"Matches: {len(api.team_event_matches('frc2501', '2022mndu'))}")

        print('***** Matches *****')
        match = api.match('2022mndu_qm48')
        print(f"Level: {match.level()}")
        print(f"Set Number: {match.set_number()}")
        print(f"Match Number: {match.match_number()}")
        print(f"Winner: {match.winner()}")
        print(f"Red Score: {match.red_score()}")
        print(f"Blue Score: {match.blue_score()}")
        print(f"Red Alliance: {match.red_teams()}")
        print(f"Blue Alliance: {match.blue_teams()}")
        print(f"Time: {match.schedule_time()}, {match.predicted_time()}, "
                f"{match.actual_time()}, {match.result_time()}")
        # Python doesn't automatically format each object in the list as a string
        videos = []
        for video in match.videos():
            videos.append(f"{video}")
        print(f"Videos: {videos}")
