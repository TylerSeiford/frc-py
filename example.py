'''
Example on how to use the library.
'''
import json
import os
from frcpy import FRCPy



if __name__ == '__main__':
    try:
        # Load the tokens from the environment
        TBA_TOKEN = os.environ['SECRET_TBA_TOKEN']
        GMAPS_TOKEN = os.environ['SECRET_GMAPS_TOKEN']
    except KeyError:
        # Or load from JSON file
        with open('token.json', 'r', encoding='UTF+8') as f:
            tokens = json.load(f)
            TBA_TOKEN = tokens['TBA']
            GMAPS_TOKEN = tokens['GMAPS']

    with FRCPy(TBA_TOKEN, GMAPS_TOKEN) as api:
        print('***** Teams *****')
        teams: list[str] = api.teams()
        print(f"Found {len(teams)} teams")
        print(f"Years: {api.team_years('frc2846')}")
        team = api.team('frc2846')
        print(f"Location: {team.location()}")
        print(f"Nickname: {team.nickname()}")
        print(f"Name: {team.name()}")
        print(f"School: {team.school_name()}")
        print(f"Website: {team.website()}")
        print(f"Rookie Year: {team.rookie_year()}")
        print(f"Motto: {team.motto()}")
        try:
            location = api.team_precise_location(team)
            if location is not None:
                print('- Precise location -')
                print(f"Latitude/Longitude: {location.lat_lng()}")
                print(f"Address: {location.address()}")
                print(f"Place ID: {location.place_id()}")
                print(f"Postal Code: {location.postal_code()}")
        except BaseException:
            pass
        for year in api.team_years('frc2846'):
            print(f"{year}: {api.team_year_events('frc2846', year)}")

        print('***** Events *****')
        min_year, max_year = api.year_range()
        for year in range(min_year, max_year + 1):
            print(f"{year}: {len(api.year_events(year))}")
        event = api.event('2023iacf')
        print(f"Name: {event.name()}")
        print(f"Location: {event.location()}")
        print(f"Type: {event.event_type_str()}")
        start_date, end_date = event.dates()
        print(f"Dates: {start_date}, {end_date}")
        print(f"District: {event.district_key()}")
        print(f"Short Name: {event.short_name()}")
        print(f"Week: {event.week()}")
        print(f"Location Name: {event.location_name()}")
        print(f"Timezome: {event.timezone()}")
        print(f"Website: {event.website()}")
        print(f"First Event ID: {event.first_event_id()}")
        print(f"First Event Code: {event.first_event_code()}")
        print('- Precise location -')
        location = event.precise_location()
        print(f"Latitude/Longitude: {location.lat_lng()}")
        print(f"Address: {location.address()}")
        print(f"Place ID: {location.place_id()}")
        print(f"Postal Code: {location.postal_code()}")
        # Python doesn't automatically format each object in the list as a string
        webcasts = []
        for webcast in event.webcasts():
            webcasts.append(f"{webcast}")
        print(f"Webcasts: {webcasts}")
        print(f"Divisions: {event.divisions()}")
        print(f"Parent event: {event.parent_event_key()}")
        print(f"Playoff Type: {event.playoff_type_str()}")
        print(f"Teams: {len(api.event_teams('2023iacf'))}")
        print(f"Matches: {len(api.event_matches('2023iacf'))}")

        print('***** Event Alliances *****')
        alliances = api._tba_client().event_alliances('2023iacf')
        for alliance in alliances:
            print(alliance['status'])

        print('***** Team @ Event *****')
        print(f"Matches: {len(api.team_event_matches('frc2846', '2023iacf'))}")

        print('***** Matches *****')
        match = api.match('2023iacf_sf12m1')
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

        print('***** Team Event Stats *****')
        stats = api.team_event_stats('frc2846', '2023iacf')
        print(f"EPA: {stats.epa_max()}")
        print(f"Auto EPA: {stats.auto_epa_max()}")
        print(f"Teleop EPA: {stats.teleop_epa_max()}")
        print(f"Endgame EPA: {stats.endgame_epa_max()}")
        print(f"Win Rate: {stats.winrate() * 100:.2f}%")
        print(f"Rank: {stats.rank()} of {stats.num_teams()}")

        print('***** Team Year Stats *****')
        stats = api.team_year_stats('frc2846', 2023)
        print(f"EPA: {stats.epa_max()}")
        print(f"Auto EPA: {stats.auto_epa_max()}")
        print(f"Teleop EPA: {stats.teleop_epa_max()}")
        print(f"Endgame EPA: {stats.endgame_epa_max()}")
        print(f"Win Rate: {stats.winrate() * 100:.2f}%")
