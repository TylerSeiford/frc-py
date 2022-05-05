import json
import random
import time
from threading import Thread
from frc_py import FRCPY
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd



class TeamStats:
    def __init__(self, api: FRCPY, team: str):
        self.__api = api
        self.__team = team
        self.results = {
            'Team': [], 'Year': [], 'Elo': [],
            'Regionals': [],
            'Districts': [], 'District Championship': [],
            'Championship': [],
            'Offseason': [], 'Preseason': []
        }

    def __call__(self):
        participation = api.get_team_participation(self.__team)
        for year in participation:
            events = api.get_team_events_year(self.__team, year)
            regionals = 0
            districts = 0
            district_championship = False
            championship = False
            offseasons = 0
            preseasons = 0
            stats = api.get_team_year_stats(self.__team, year)
            if isinstance(stats, Warning):
                continue
            for event in events:
                event_type = api.get_event_type(event)
                match event_type:
                    case 0:
                        regionals += 1
                    case 1:
                        districts += 1
                    case 2 | 5: # District Championship or District Championship Division
                        district_championship = True
                    case 3 | 4 | 6: # Championship or Championship Division or Festival of Champions
                        championship = True
                    case 7: # Remote
                        pass
                    case 99:
                        offseasons += 1
                    case 100:
                        preseasons += 1
                    case _:
                        pass
            self.results['Team'].append(self.__team)
            self.results['Year'].append(year)
            self.results['Elo'].append(stats['elo']['max'])
            self.results['Regionals'].append(regionals)
            self.results['Districts'].append(districts)
            self.results['District Championship'].append(district_championship)
            self.results['Championship'].append(championship)
            self.results['Offseason'].append(offseasons)
            self.results['Preseason'].append(preseasons)

def get_data(api: FRCPY, teams: list[str]) -> pd.DataFrame:
    try:
        df = pd.read_csv('temp-cache/events.csv')
        print('Loaded data from cache.')
        return df
    except FileNotFoundError:
        pass

    print(f"Preparing {len(teams)} teams...")
    random.shuffle(teams)
    ready_threads = []
    for team in teams:
        loader = TeamStats(api, team)
        thread = Thread(name=team, target=loader)
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

    # Merge data
    data = {
        'Team': [], 'Year': [], 'Elo': [],
        'Regionals': [],
        'Districts': [], 'District Championship': [],
        'Championship': [],
        'Offseason': [], 'Preseason': []
    }
    for team, thread, loader in done_threads:
        for key in data.keys():
            data[key].extend(loader.results[key])

    # Convert and save
    df = pd.DataFrame(data)
    print("Saving data...")
    df.to_csv('temp-cache/events.csv', index=False)
    return df

if __name__ == '__main__':
    f = open('token.json', 'r')
    token = json.load(f)
    f.close()

    api = FRCPY(token)
    teams = api.get_team_index()
    df = get_data(api, teams)

    # Filter out non-regional teams
    df = df[df['Districts'] == 0]
    df = df[df['Regionals'] > 0]

    # Plot
    sns.set_theme(style='darkgrid', font_scale=0.625)
    sns.boxplot(x='Regionals', y='Elo', data=df)
    plt.xlabel('Regionals')
    plt.ylabel('Elo')
    plt.savefig('events.png', dpi=512, bbox_inches='tight')
    plt.show()


