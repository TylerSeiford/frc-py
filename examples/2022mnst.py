import json
import pandas as pd
from frc_py import FRCPY



if __name__ == '__main__':
    f = open('token.json', 'r')
    token = json.load(f)
    f.close()

    api = FRCPY(token)

    matches = pd.read_csv('2022mnst.csv')

    # Gather teams
    teams = []
    for index, row in matches.iterrows():
        if row['Blue 1'] not in teams:
            teams.append(row['Blue 1'])
        if row['Blue 2'] not in teams:
            teams.append(row['Blue 2'])
        if row['Blue 3'] not in teams:
            teams.append(row['Blue 3'])
        if row['Red 1'] not in teams:
            teams.append(row['Red 1'])
        if row['Red 2'] not in teams:
            teams.append(row['Red 2'])
        if row['Red 3'] not in teams:
            teams.append(row['Red 3'])

    # Gather stats and prepare results
    stats = {}
    rp_results = {}
    score_results = {}
    for team in teams:
        team = f"frc{team}"
        stats[team] = api.get_team_year_stats(team, 2022)
        rp_results[team] = 0
        score_results[team] = 0

    # Calculate results
    match_results = []
    for index, row in matches.iterrows():
        red_1 = f"frc{row['Red 1']}"
        red_2 = f"frc{row['Red 2']}"
        red_3 = f"frc{row['Red 3']}"
        red_score = 0
        red_score += stats[red_1]['opr']['opr']
        red_score += stats[red_2]['opr']['opr']
        red_score += stats[red_3]['opr']['opr']
        red_score = round(red_score, 2)
        red_rps = 0
        red_cargo = (stats[red_1]['ils']['ils_1'] + stats[red_2]['ils']['ils_1'] + stats[red_3]['ils']['ils_1']) > 1.0
        if red_cargo:
            red_rps += 1
        red_hangar = (stats[red_1]['ils']['ils_2'] + stats[red_2]['ils']['ils_2'] + stats[red_3]['ils']['ils_2']) > 1.0
        if red_hangar:
            red_rps += 1

        blue_1 = f"frc{row['Blue 1']}"
        blue_2 = f"frc{row['Blue 2']}"
        blue_3 = f"frc{row['Blue 3']}"
        blue_score = 0
        blue_score += stats[blue_1]['opr']['opr']
        blue_score += stats[blue_2]['opr']['opr']
        blue_score += stats[blue_3]['opr']['opr']
        blue_score = round(blue_score, 2)
        blue_rps = 0
        blue_cargo = (stats[blue_1]['ils']['ils_1'] + stats[blue_2]['ils']['ils_1'] + stats[blue_3]['ils']['ils_1']) > 1.0
        if blue_cargo:
            blue_rps += 1
        blue_hangar = (stats[blue_1]['ils']['ils_2'] + stats[blue_2]['ils']['ils_2'] + stats[blue_3]['ils']['ils_2']) > 1.0
        if blue_hangar:
            blue_rps += 1


        result = None
        if blue_score == red_score:
            result = 'Tie'
            red_rps += 1
            blue_rps += 1
        elif blue_score > red_score:
            result = 'Blue'
            blue_rps += 2
        else:
            result = 'Red'
            red_rps += 2
        rp_results[red_1] += red_rps
        rp_results[red_2] += red_rps
        rp_results[red_3] += red_rps
        rp_results[blue_1] += blue_rps
        rp_results[blue_2] += blue_rps
        rp_results[blue_3] += blue_rps
        score_results[red_1] += red_score
        score_results[red_2] += red_score
        score_results[red_3] += red_score
        score_results[blue_1] += blue_score
        score_results[blue_2] += blue_score
        score_results[blue_3] += blue_score
        match_results.append({
            'Match': row['Match'],
            'Result': result,
            'Red Score': red_score,
            'Blue Score': blue_score,
            'Red Cargo RP': red_cargo,
            'Red Hangar RP': red_hangar,
            'Blue Cargo RP': blue_cargo,
            'Blue Hangar RP': blue_hangar
        })

    new_team_results = []
    for team in teams:
        team = f"frc{team}"
        new_team_results.append({
            'Team': team,
            'RP': round(rp_results[team] / 8, 2),
            'Score': round(score_results[team] / 8, 2)
        })

    # Save results
    team_df = pd.DataFrame.from_dict(new_team_results)
    team_df.to_csv('2022mnst_team_results.csv', index=False)
    match_df = pd.DataFrame(match_results)
    match_df.to_csv('2022mnst_match_results.csv', index=False)


