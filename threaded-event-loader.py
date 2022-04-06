from threading import Thread
import time
from frc_py import FRC_PY



class TeamLoader:
    def __init__(self, team: str, year: int, api: FRC_PY):
        self.__team = team
        self.__year = year
        self.__api = api

    def __call__(self):
        stats = self.__api.get_team_year_stats(self.__team, self.__year)



api = FRC_PY()
teams = api.get_event_teams('2022mnmi')

print(f"Preparing {len(teams)} teams...")
ready_threads = []
count = 0
for team in teams:
    years = api.get_team_participation(team)
    for year in years:
        loader = TeamLoader(team, year, api)
        thread = Thread(target=loader)
        ready_threads.append((team, year, thread))
        count += 1

print("Starting execution...")
active_threads = {}
while len(ready_threads) > 0 or len(active_threads.keys()) > 0:
    # Detect done threads
    to_prune = []
    for (team, year) in active_threads.keys():
        thread = active_threads[(team, year)]
        if not thread.is_alive():
            to_prune.append((team, year))

    # Prune done threads
    pruned = 0
    for (team, year) in to_prune:
        print(f"{team} {year}", end='\t')
        active_threads.pop((team, year))
        pruned += 1

    # Start new threads
    added = 0
    while len(active_threads.keys()) < 2048 and len(ready_threads) > 0 and added < 128:
        team, year, thread = ready_threads.pop()
        active_threads[(team, year)] = thread
        thread.start()
        added += 1

    # Print status
    print(f"\nReady: {len(ready_threads)}, Active: {len(active_threads.keys())}, Done: {count - len(ready_threads) - len(active_threads.keys())}")
    if pruned == 0 and added == 0:
        time.sleep(0.5)


