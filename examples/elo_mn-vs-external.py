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



us_state_abbrev = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    'DC': 'District of Columbia',
    'MP': 'Northern Mariana Islands',
    'PW': 'Palau',
    'PR': 'Puerto Rico',
    'VI': 'Virgin Islands',
    'AA': 'Armed Forces Americas (Except Canada)',
    'AE': 'Armed Forces Other/Canada/Other/Middle East',
    'AP': 'Armed Forces Pacific'
}

class TeamElo:
    def __init__(self, team: str, api: FRCPY):
        self.__team = team
        self.__api = api
        self.results = []

    def __call__(self):
        team_years = api.get_team_participation(self.__team)
        team_city, team_state_prov, team_country = api.get_team_location(self.__team)
        if team_state_prov in us_state_abbrev.keys(): # Harmonize state names
            team_state_prov = us_state_abbrev[team_state_prov]
        for year in team_years:
            team_events = api.get_team_events_year(self.__team, year)
            if team_state_prov != 'Minnesota':
                # Check only non-Minnesota teams
                minnesota_event = False
                for event in team_events:
                    type = api.get_event_type(event)
                    if type != 0:
                        continue # Ignore non-Regional events
                    event_city, event_state_prov, event_country = api.get_event_location(event)
                    if event_state_prov in us_state_abbrev.keys(): # Harmonize state names
                        event_state_prov = us_state_abbrev[event_state_prov]
                    if event_state_prov == 'Minnesota':
                        minnesota_event = True
                        break # If the Regional event is in Minnesota, stop checking
                if not minnesota_event:
                    continue
            stats = api.get_team_year_stats(self.__team, year)
            if isinstance(stats, Dict):
                self.results.append((self.__team, year, stats['elo']['max'], team_country, team_state_prov, team_city))

def get_data(api: FRCPY, teams: List[str]) -> Dict[str, List]:
    raw_data = api._load('temp-cache', 'elo_mn-vs-external.json')
    if raw_data is None or isinstance(raw_data, BaseException) or raw_data[0] < datetime.utcnow() - timedelta(days=280):
        print(f"Preparing {len(teams)} teams...")
        random.shuffle(teams)
        ready_threads = []
        for team in teams:
            loader = TeamElo(team, api)
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

        # Convert data into structure
        structure = { 'Team': [], 'Year': [], 'Elo': [], 'Country': [], 'State/Province': [], 'City': [] }
        for team, thread, loader in done_threads:
            for result in loader.results:
                team, year, elo, country, state_prov, city = result
                structure['Team'].append(team)
                structure['Year'].append(year)
                structure['Elo'].append(elo)
                structure['Country'].append(country)
                structure['State/Province'].append(state_prov)
                structure['City'].append(city)

        # Save to cache
        api._save('temp-cache', 'elo_mn-vs-external.json', structure)
        return structure
    return raw_data[1]



if __name__ == '__main__':
    print()
    f = open('token.json', 'r')
    token = json.load(f)
    f.close()
    api = FRCPY(token)

    # Prepare teams
    teams = api.get_team_index()
    print(f"{len(teams)} teams")

    # Get data and reformat
    data = get_data(api, teams)
    new_data =  { 'Team': [], 'Year': [], 'Elo': [], 'Location': [] }
    locations = {}
    for i in range(len(data['Team'])):
        country = data['Country'][i]
        state_prov = data['State/Province'][i]
        city = data['City'][i]
        if country != 'USA' or state_prov != 'Minnesota':
            location = 'External'
        else:
            location = 'Minnesota'
        if location not in locations:
            locations[location] = 0
        locations[location] += 1

        new_data['Team'].append(data['Team'][i])
        new_data['Year'].append(data['Year'][i])
        new_data['Elo'].append(data['Elo'][i])
        new_data['Location'].append(location)
    df = pd.DataFrame(new_data)

    # Plot
    sns.set_theme(style='darkgrid', font_scale=0.625)
    sns.boxplot(x='Year', y='Elo', hue='Location', data=df)
    plt.xlabel('Year')
    plt.ylabel('Elo')
    plt.legend(loc='upper left', title='Location')
    plt.savefig('elo_mn-vs-external.png', dpi=512, bbox_inches='tight')
    plt.show()


