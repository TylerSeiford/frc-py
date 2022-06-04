import os
from frc_py import FRC_PY



if __name__ == '__main__':
    TOKEN = os.environ['SECRET_TBA_TOKEN'] # Replace with your TBA token
    api = FRC_PY(TOKEN)

    print('***** Teams *****')
    teams = api.get_teams()
    print(f"Found {len(teams)} teams")
    print(f"Years: {api.get_team_participation('frc2501')}")
    print(f"Location: {api.get_team_location('frc2501')}")
    print(f"Nickname: {api.get_team_nickname('frc2501')}")
    print(f"Name: {api.get_team_name('frc2501')}")
    print(f"School: {api.get_team_school('frc2501')}")
    print(f"Website: {api.get_team_website('frc2501')}")
    print(f"Rookie Year: {api.get_team_rookie_year('frc2501')}")
    print(f"Motto: {api.get_team_motto('frc2501')}")
    for year in api.get_team_participation('frc2501'):
        print(f"{year}: {api.get_team_events_year('frc2501', year)}")

    print('***** Events *****')
    min_year, max_year = api.get_year_range()
    for year in range(min_year, max_year + 1):
        print(f"{year}: {len(api.get_events_year(year))}")
    print(f"Name: {api.get_event_name('2022mndu')}")
    print(f"Location: {api.get_event_location('2022mndu')}")
    print(f"Type: {FRC_PY.event_type_to_str(api.get_event_type('2022mndu'))}")
    print(f"Dates: {api.get_event_dates('2022mndu')}")
    print(f"District: {api.get_event_district('2022mndu')}")
    print(f"Teams: {len(api.get_event_teams('2022mndu'))}")
    print(f"Matches: {len(api.get_event_matches('2022mndu'))}")

    print('***** Team @ Event *****')
    print(f"Matches: {len(api.get_team_event_matches('frc2501', '2022mndu'))}")

    print('***** Matches *****')
    print(f"Level: {api.get_match_level('2022mndu_qm48')}")
    print(f"Set Number: {api.get_match_set_number('2022mndu_qm48')}")
    print(f"Match Number: {api.get_match_number('2022mndu_qm48')}")
    print(f"Winner: {api.get_match_winner('2022mndu_qm48')}")
    print(f"Red Score: {api.get_match_red_score('2022mndu_qm48')}")
    print(f"Blue Score: {api.get_match_blue_score('2022mndu_qm48')}")
    print(f"Red Alliance: {api.get_match_red_teams('2022mndu_qm48')}")
    print(f"Blue Alliance: {api.get_match_blue_teams('2022mndu_qm48')}")
    print(f"Time: {api.get_match_time('2022mndu_qm48')}")
