from frc_py import FRC_PY



api = FRC_PY()

teams = api.get_team_index()

for team in teams[:10]:
    years = api.get_team_participation(team)
    for year in years:
        events = api.get_team_events_year(team, year)
        stats = api.get_team_year_stats(team, year)
        print(f"{team} {year}:\n\t- {events}\n\t- {stats}")


