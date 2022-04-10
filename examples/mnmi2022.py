import json
from frc_py import FRCPY



if __name__ == '__main__':
    f = open('token.json', 'r')
    token = json.load(f)
    f.close()

    api = FRCPY(token)
    teams = api.get_event_teams('2022mnmi')
    print(f"{len(teams)} teams")

    stats = {}
    for team in teams:
        stats[team] = api.get_team_year_stats(team, 2022)

    elos = {}
    first = []
    for team in teams:
        elos[team] = stats[team]['elo']['end']
        if elos[team] is None:
            elos[team] = stats[team]['elo']['start']
            first.append(team)
    elos = sorted(elos.items(), key=lambda x: x[1], reverse=True)
    print('Elos:')
    for i in elos:
        print(f"\t{i[0]}\t: {i[1]}")

    oprs = {}
    rookies = []
    for team in teams:
        oprs[team] = stats[team]['opr']['opr']
        if oprs[team] == 13.8:
            del oprs[team]
            rookies.append(team)
    oprs = sorted(oprs.items(), key=lambda x: x[1], reverse=True)
    print('OPRs:')
    for i in oprs:
        print(f"\t{i[0]}\t: {i[1]}")
    print(f"Rookies: {rookies}")
    print(f"First: {first}")
