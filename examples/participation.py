import yaml
from frc_py import FRC_PY



if __name__ == '__main__':
    api = FRC_PY(yaml.load(open('config.yml'), yaml.Loader))
    teams = api.get_team_index()
    print(f"{len(teams)} teams")

    # Get years of any participation
    years = []
    for team in teams:
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
    for team in teams:
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
    f = open('participation.csv', 'w')
    f.write('Year,Rookies,Participants,Retiring\n')
    for year in participation.keys():
        f.write(f"{year},{participation[year]['rookies']},{participation[year]['participants']},{participation[year]['last']}\n")
    f.close()
