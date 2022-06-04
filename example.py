import os
from frc_py import FRC_PY



if __name__ == '__main__':
    TOKEN = os.environ['SECRET_TBA_TOKEN'] # Replace with your TBA token
    api = FRC_PY(TOKEN)

    print('***** Teams *****')
    teams: list[str] = api.get_teams()
    print(f"Found {len(teams)} teams")
    print(f"Years: {api.get_team_participation('frc2501')}")
    team = api.team('frc2501')
    print(f"Location: {team.location()}")
    print(f"Nickname: {team.nickname()}")
    print(f"Name: {team.name()}")
    print(f"School: {team.school_name()}")
    print(f"Website: {team.website()}")
    print(f"Rookie Year: {team.rookie_year()}")
    print(f"Motto: {team.motto()}")
    for year in api.get_team_participation('frc2501'):
        print(f"{year}: {api.get_team_events_year('frc2501', year)}")

    print('***** Events *****')
    min_year, max_year = api.get_year_range()
    for year in range(min_year, max_year + 1):
        print(f"{year}: {len(api.get_events_year(year))}")
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
    print(f"Teams: {len(api.get_event_teams('2022mndu'))}")
    print(f"Matches: {len(api.get_event_matches('2022mndu'))}")

    print('***** Team @ Event *****')
    print(f"Matches: {len(api.get_team_event_matches('frc2501', '2022mndu'))}")

    print('***** Matches *****')
    match_simple = api.match_simple('2022mndu_qm48')
    print(f"Level: {match_simple.level()}")
    print(f"Set Number: {match_simple.set_number()}")
    print(f"Match Number: {match_simple.match_number()}")
    print(f"Winner: {match_simple.winner()}")
    print(f"Red Score: {match_simple.red_score()}")
    print(f"Blue Score: {match_simple.blue_score()}")
    print(f"Red Alliance: {match_simple.red_teams()}")
    print(f"Blue Alliance: {match_simple.blue_teams()}")
    print(f"Time: {match_simple.schedule_time(), match_simple.predicted_time(), match_simple.actual_time()}")
