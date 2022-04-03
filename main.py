from datetime import datetime, timedelta
from typing import List
from frc_py import FRC_PY



def get_mn(api: FRC_PY) -> List[str]:
    raw_data = api._load('temp-cache', 'mn.json')
    if raw_data is None or raw_data[0] < datetime.utcnow() - datetime.timedelta(days=280): # TODO
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
