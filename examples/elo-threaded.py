from datetime import datetime, timedelta
import json
import random
from threading import Thread
import time
from typing import Dict, List
from frc_py import FRCPY
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



class TeamElo:
    def __init__(self, team: str, api: FRCPY):
        self.__team = team
        self.__api = api
        self.results = []

    def __call__(self):
        team_years = api.get_team_participation(self.__team)
        city, state_prov, country = api.get_team_location(self.__team)
        minnesota = state_prov == 'Minnesota' or state_prov == 'MN'
        for year in team_years:
            stats = api.get_team_year_stats(self.__team, year)
            if isinstance(stats, Dict):
                self.results.append((self.__team, year, stats['elo']['max'], minnesota))


def get_data(api: FRCPY, teams: List[str]) -> Dict[int, List[float]]:
    raw_data = api._load('temp-cache', 'elo.json')
    if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=280):
        print(f"Preparing {len(teams)} teams...")
        random.shuffle(teams)
        ready_threads = []
        for team in teams:
            loader = TeamElo(team, api)
            thread = Thread(target=loader)
            ready_threads.append((team, thread, loader))

        print("Starting execution...")
        active_threads = {}
        done_threads = []
        while len(ready_threads) > 0 or len(active_threads.keys()) > 0:
            # Detect done threads
            to_prune = []
            for team in active_threads.keys():
                thread, loader = active_threads[team]
                if not thread.is_alive():
                    to_prune.append(team)

            # Prune done threads
            pruned = 0
            for team in to_prune:
                print(f"{team}", end='\t')
                thread, loader = active_threads.pop(team)
                done_threads.append((team, thread, loader))
                pruned += 1

            # Start new threads
            added = 0
            while len(active_threads.keys()) < 2048 and len(ready_threads) > 0 and added < 128:
                team, thread, loader = ready_threads.pop()
                active_threads[team] = thread, loader
                thread.start()
                added += 1

            # Print status
            print(f"\nReady: {len(ready_threads)}, Active: {len(active_threads.keys())}, Done: {len(done_threads)}")
            if pruned == 0 and added == 0:
                time.sleep(0.5)

        # Convert data into structure
        structure = { 'Team': [], 'Year': [], 'Elo': [], 'MN': [] }
        for team, thread, loader in done_threads:
            for result in loader.results:
                structure['Team'].append(result[0])
                structure['Year'].append(result[1])
                structure['Elo'].append(result[2])
                structure['MN'].append(result[3])

        # Save to cache
        api._save('temp-cache', 'elo.json', structure)
        return structure
    return raw_data[1]



if __name__ == '__main__':
    print()
    f = open('token.json', 'r')
    token = json.load(f)
    f.close()
    api = FRCPY(token)

    # Prepare MN teams
    teams = api.get_team_index()
    print(f"{len(teams)} teams")

    # Get data
    data = get_data(api, teams)

    # Reformat into pandas
    df = pd.DataFrame(data)

    # Plot
    sns.set_theme(style='darkgrid', font_scale=0.625)
    sns.boxplot(x='Year', y='Elo', hue='MN', data=df)
    plt.xlabel('Year')
    plt.ylabel('Elo')
    plt.legend(loc='upper left', title='MN')
    plt.savefig('elo.png', dpi=512, bbox_inches='tight')
    plt.show()


