from datetime import datetime, timedelta
import json
from typing import Dict, List
from frc_py import FRCPY



def get_mn(api: FRCPY) -> List[str]:
    raw_data = api._load('temp-cache', 'mn.json')
    if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=280):
        teams = api.get_team_index()
        mn = []
        for team in teams:
            city, state_prov, country = api.get_team_location(team)
            if state_prov == 'Minnesota' or state_prov == 'MN':
                mn.append(team)
        api._save('temp-cache', 'mn.json', mn)
        return mn
    return raw_data[1]



if __name__ == '__main__':
    print()
    f = open('token.json', 'r')
    token = json.load(f)
    f.close()
    api = FRCPY(token)

    # Prepare MN teams
    teams = []
    for team in get_mn(api):
        teams.append((team, api._team_key_to_number(team)))
    teams.sort(key=lambda x: x[1])
    print(f"{len(teams)} teams in MN")

    # Get years of any participation from Minnesota
    years = []
    for team in teams:
        team_years = api.get_team_participation(team[0])
        for year in team_years:
            if year not in years:
                years.append(year)

    # Prepare file
    years.sort()
    f = open('mn_elo.csv', 'w')
    f.write('Year,')
    for team in teams:
        f.write(f"{team[1]},")
    f.write('\n')

    # Fill file
    for year in years:
        print(f"{year}", end='\t')
        f.write(f"{year},")
        for team in teams:
            team_years = api.get_team_participation(team[0])
            if year not in team_years:
                print(' ', end='')
                f.write(',')
            else:
                stats = api.get_team_year_stats(team[0], year)
                if isinstance(stats, Dict):
                    print('-', end='')
                    f.write(f"{stats['elo']['max']},")
                else:
                    print('+', end='')
                    f.write(',')
        print('')
        f.write('\n')

    # Close file
    f.close()


