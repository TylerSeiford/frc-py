import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from frc_py import FRCPY



division_map = {
    '2022carv': 'Carver',
    '2022gal': 'Galileo',
    '2022hop': 'Hopper',
    '2022new': 'Newton',
    '2022roe': 'Roebling',
    '2022tur': 'Turing'
}

if __name__ == '__main__':
    f = open('token.json', 'r')
    token = json.load(f)
    f.close()

    api = FRCPY(token)

    divisions = api._tba_client().event('2022cmptx')['division_keys']
    teams = {}
    for division in divisions:
        teams[division] = []
        for team in api.get_event_teams(division):
            teams[division].append(team)
        print(f"Found {len(teams[division])} teams in {division}")

    data = { 'Team': [], 'Elo': [], 'OPR': [], 'Division': [] }
    for division in divisions:
        print(f"{division_map[division]}", end='\t')
        for team in teams[division]:
            stats = api.get_team_year_stats(team, 2022)
            data['Team'].append(team)
            data['Elo'].append(stats['elo']['pre_champs'])
            data['OPR'].append(stats['opr']['opr'])
            data['Division'].append(division_map[division])
            print('-', end='')
        print(f"\t{len(teams[division])} teams")
    df = pd.DataFrame(data)

    # Plot
    sns.set_theme(style='darkgrid', font_scale=0.625)
    sns.boxplot(x='Division', y='Elo', data=df)
    plt.xlabel('Division')
    plt.ylabel('Elo')
    plt.savefig('2022cmptx_Elo.png', dpi=512, bbox_inches='tight')
    plt.show()

    sns.set_theme(style='darkgrid', font_scale=0.625)
    sns.boxplot(x='Division', y='OPR', data=df)
    plt.xlabel('Division')
    plt.ylabel('OPR')
    plt.savefig('2022cmptx_OPR.png', dpi=512, bbox_inches='tight')
    plt.show()


