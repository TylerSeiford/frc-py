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
    event_simple = api.event_simple('2022mndu')
    print(f"Name: {event_simple.name()}")
    print(f"Location: {event_simple.location()}")
    print(f"Type: {FRC_PY.event_type_to_str(event_simple.event_type())}")
    print(f"Dates: {event_simple.dates()}")
    print(f"District: {event_simple.district_key()}")
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
