from datetime import datetime, timedelta
import json
from typing import Dict, List
from frc_py import FRCPY
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt, matplotlib as mpl



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

def get_data(api: FRCPY, teams: List[str]) -> Dict[int, List[float]]:
    raw_data = api._load('temp-cache', 'mn-elo.json')
    if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=280):
        # Get years of any participation
        years = []
        for team in teams:
            team_years = api.get_team_participation(team)
            for year in team_years:
                if year not in years:
                    years.append(year)

        # Prepare and fill structure
        structure = { 'Team': [], 'Year': [], 'Elo': [] }
        for team in teams:
            print(f"{team}", end='\t')
            team_years = api.get_team_participation(team)
            for year in years:
                if year not in team_years:
                    print(' ', end='')
                else:
                    stats = api.get_team_year_stats(team, year)
                    if isinstance(stats, Dict):
                        print('-', end='')
                        structure['Team'].append(team)
                        structure['Year'].append(year)
                        structure['Elo'].append(stats['elo']['max'])
                    else:
                        print('+', end='')
            print('')

        # Save to cache
        api._save('temp-cache', 'mn-elo.json', structure)
        return structure
    return raw_data[1]



if __name__ == '__main__':
    print()
    f = open('token.json', 'r')
    token = json.load(f)
    f.close()
    api = FRCPY(token)

    # Prepare MN teams
    teams = get_mn(api)
    print(f"{len(teams)} teams in MN")

    # Get data
    data = get_data(api, teams)

    # Reformat into pandas
    df = pd.DataFrame(data)

    # Plot
    sns.set_theme(style='darkgrid', font_scale=0.625)
    sns.boxplot(x='Year', y='Elo', data=df)
    plt.title('Minnesota Elo')
    plt.xlabel('Year')
    plt.ylabel('Elo')
    plt.savefig('mn-elo.png', dpi=512, bbox_inches='tight')
    plt.show()


