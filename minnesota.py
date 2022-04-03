from datetime import datetime, timedelta
from typing import List
from frc_py import FRC_PY



def get_mn(api: FRC_PY) -> List[str]:
    raw_data = api._load('temp-cache', 'mn.json')
    if raw_data is None or raw_data[0] < datetime.utcnow() - timedelta(days=280): # TODO
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
    api = FRC_PY()
    mn = get_mn(api)
    print(f"{len(mn)} teams in MN")

    # Get years of any participation from Minnesota
    years = []
    for team in mn:
        team_years = api.get_team_participation(team)
        for year in team_years:
            if year not in years:
                years.append(year)

    # Prepare participation structure
    participation = {}
    years.sort()
    for year in range(years[0], years[-1] + 1):
        participation[year] = {'rookies': 0, 'participants': 0, 'last': 0}

    # Fill participation structure
    for team in mn:
        team_years = api.get_team_participation(team)
        team_years.sort()
        if team_years == []:
            continue

        # Add rookie season
        participation[team_years[0]]['rookies'] += 1

        # Add participating seasons
        for i in range(1, len(team_years) - 1):
            participation[team_years[i]]['participants'] += 1

        # Add last season
        if team_years[-1] == 2022: # TODO
            # Currently active teams are just participants in 2022, not their last year
            participation[team_years[-1]]['participants'] += 1
        else:
            participation[team_years[-1]]['last'] += 1

    # Write participation to file
    f = open('mn_participation.csv', 'w')
    f.write('Year,Rookies,Participants,Last\n')
    for year in participation.keys():
        f.write(f"{year},{participation[year]['rookies']},{participation[year]['participants']},{participation[year]['last']}\n")
    f.close()
