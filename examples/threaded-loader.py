import random
from threading import Thread
import time
from frc_py import FRC_PY



class TeamLoader:
    def __init__(self, team: str, api: FRC_PY):
        self.__team = team
        self.__api = api

    def __call__(self):
        team_nickname = self.__api.get_team_nickname(self.__team)
        years = self.__api.get_team_participation(self.__team)
        for year in years:
            if year < 2007 or year == 2020 or year == 2021:
                continue
            events = self.__api.get_team_events_year(self.__team, year)
            stats = self.__api.get_team_year_stats(self.__team, year)



api = FRC_PY(yaml.load(open('config.yml'), yaml.Loader))
teams = api.get_team_index()
random.shuffle(teams)

print(f"Preparing {len(teams)} teams...")
ready_threads = []
for team in teams:
    loader = TeamLoader(team, api)
    thread = Thread(target=loader)
    ready_threads.append((team, thread))

print("Starting execution...")
active_threads = {}
while len(ready_threads) > 0 or len(active_threads.keys()) > 0:
    # Detect done threads
    to_prune = []
    for team in active_threads.keys():
        thread = active_threads[team]
        if not thread.is_alive():
            to_prune.append(team)

    # Prune done threads
    pruned = 0
    for team in to_prune:
        print(f"{team}", end='\t')
        active_threads.pop(team)
        pruned += 1

    # Start new threads
    added = 0
    while len(active_threads.keys()) < 2048 and len(ready_threads) > 0 and added < 128:
        team, thread = ready_threads.pop()
        active_threads[team] = thread
        thread.start()
        added += 1

    # Print status
    print(f"\nReady: {len(ready_threads)}, Active: {len(active_threads.keys())}, Done: {len(teams) - len(ready_threads) - len(active_threads.keys())}")
    if pruned == 0 and added == 0:
        time.sleep(0.5)


