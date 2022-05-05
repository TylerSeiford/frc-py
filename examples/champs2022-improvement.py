import json
import pandas as pd
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
        print(f"Found {len(teams[division])} teams in {division_map[division]}")

    data = { 'Team': [], 'Predicted Rank': [], 'Actual Rank': [], 'Change': [], 'Division': [] }
    for division in divisions:
        print(f"{division_map[division]}", end='\t')
        raw = api._tba_client().event_rankings(division)['rankings']
        actuals = {}
        for i in raw:
            actuals[i['team_key']] = i['rank']
        predictions = api._stat_client().get_event_sim(division, index=0, full=True, iterations=None)['0']['sim_ranks']
        for team in teams[division]:
            predicted_rank = predictions[str(api._team_key_to_number(team))]
            try:
                actual_rank = actuals[team]
            except KeyError:
                print('X', end='')
                continue
            change = predicted_rank - actual_rank
            data['Team'].append(team)
            data['Predicted Rank'].append(predicted_rank)
            data['Actual Rank'].append(actual_rank)
            data['Change'].append(change)
            data['Division'].append(division)
            print('-', end='')
        print(f"\t{len(teams[division])} teams")
    df = pd.DataFrame(data)

    # Save
    df.to_csv('cmptx2022.csv', index=False)


