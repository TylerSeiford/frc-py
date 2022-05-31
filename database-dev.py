from datetime import datetime
import os
import sqlite3
import tbapy



def init_team_simple(connection: sqlite3.Connection) -> None:
    connection.execute("""CREATE TABLE IF NOT EXISTS tba_teams_simple (
        last_updated datetime,
        key text, nickname text, name text,
        city text, state_prov text, country text
    )""")
    connection.commit()

def insert_team_simple(connection: sqlite3.Connection, team_data: tbapy.Team) -> None:
    connection.execute("INSERT INTO tba_teams_simple VALUES (?, ?, ?, ?, ?, ?, ?)", (
        datetime.utcnow().isoformat(),
        team_data.key, team_data.nickname, team_data.name,
        team_data.city, team_data.state_prov, team_data.country
    ))
    connection.commit()

def get_team_simple(connection: sqlite3.Connection, team_key: str) -> str:
    connection.execute("SELECT * FROM tba_teams_simple WHERE key = ?", team_key)
    result = connection.fetchone()
    if result is None:
        return None
    timestamp, _, nickname, name, city, state_prov, country = result
    timestamp = datetime.fromisoformat(timestamp)
    return nickname, name, city, state_prov, country

def delete_team_simple(connection: sqlite3.Connection, team_key: str) -> None:
    connection.execute("DELETE FROM tba_teams_simple WHERE key = ?", team_key)
    connection.commit()



if __name__ == '__main__':
    TOKEN = os.environ['SECRET_TBA_TOKEN'] # Replace with your TBA token
    tba_client = tbapy.TBA(TOKEN)

    with sqlite3.connect('test.db') as conn:
        init_team_simple(conn)
