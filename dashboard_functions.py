import requests 
from dashboard_configs import league_id
import pandas as pd


#Step 1 get all the users in a given league
def get_league_standings(league_id):
    endpoint = f'https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/'
    response = requests.get(endpoint).json()
    standings = pd.DataFrame(response['standings']['results'])

    endpoint = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = requests.get(endpoint).json()
    clubs = pd.DataFrame(response['teams']).iloc[:, [3,5]]
    clubs.rename(columns = {'id':'club_id', 'name':'club'}, inplace = True)

    manager_ids = []
    manager_clubs = []
    manager_regions = []

    TC = []
    BB = []
    FH = []
    ids = []


    for i in standings.entry:
        endpoint = f' https://fantasy.premierleague.com/api/entry/{i}/'
        response = requests.get(endpoint).json()
        favourite_club_id = response['favourite_team']
        region = response["player_region_name"]
        manager_ids.append(i)
        manager_clubs.append(favourite_club_id)
        manager_regions.append(region)

        endpoint = f'https://fantasy.premierleague.com/api/entry/{i}/history/'
        response = requests.get(endpoint).json()
        chips = response['chips']
        season = response['current']

        if len(chips) == 0:
            TC.append(0)
            BB.append(0)
            FH.append(0)
            ids.append(i)

        else:
            for j in chips:
                if j['name'] == '3xc':
                    TC.append(1)
                else:
                    TC.append(0)

                if j['name'] == 'bboost':
                    BB.append(1)
                else:
                    BB.append(0)

                if j['name'] == 'freehit':
                    FH.append(1)
                else:
                    FH.append(0)

                ids.append(i)

    favourite_clubs_df = pd.DataFrame({'entry_id': manager_ids, 'club_id':manager_clubs, 'region': manager_regions})

    standings = pd.merge(standings, favourite_clubs_df, left_on='entry', right_on='entry_id', how='left').drop('entry_id', axis=1)
    standings = pd.merge(standings, clubs, on="club_id", how="left")

    chip_df =pd.DataFrame({'m_id': ids, 'used_tc': TC, 'used_bb': BB, 'used_fh': FH})
    standings = pd.merge(standings, chip_df, left_on='entry', right_on='m_id', how='left').drop('m_id', axis=1)

    return standings


def get_season_data(standings):
    season_df = pd.DataFrame()

    for i in standings.entry:

        endpoint = f'https://fantasy.premierleague.com/api/entry/{i}/history/'
        response = requests.get(endpoint).json()
        season = response['current']
        temp_season_df = pd.DataFrame(season)

        m_id = []
        for j in range(len(season)):
            m_id.append(i)

        temp_season_df['entry'] = m_id

        season_df = season_df.append(temp_season_df, ignore_index=True)

        
    season_df = pd.merge(season_df, standings[['entry','player_name']], on="entry", how="left")

    return season_df


league_standings = get_league_standings(league_id)

season_data = get_season_data(league_standings)

print(season_data)