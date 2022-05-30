import os
from frc_py import FRC_PY


if __name__ == '__main__':
    TOKEN = os.environ['SECRET_TBA_TOKEN'] # Replace with your TBA token
    api = FRC_PY(TOKEN)

    teams = api.get_team_index()
    print(f"Found {len(teams)} teams")

    print(f"Years: {api.get_team_participation('frc2501')}")
    print(f"Location: {api.get_team_location('frc2501')}")
    print(f"Nickname: {api.get_team_nickname('frc2501')}")
    print(f"Name: {api.get_team_name('frc2501')}")
    print(f"School: {api.get_team_school('frc2501')}")
    print(f"Website: {api.get_team_website('frc2501')}")
    print(f"Rookie Year: {api.get_team_rookie_year('frc2501')}")
    print(f"Motto: {api.get_team_motto('frc2501')}")
