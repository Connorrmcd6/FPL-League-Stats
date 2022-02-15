import requests 
from configs import *

def get_league_members(league_id):
    endpoint = f'https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/'
    response = requests.get(endpoint).json()
    standings = response['standings']['results']
    user_ids = []
    user_names = []

    for i in standings:
        user_ids.append(i['entry'])
        user_names.append(i['player_name'])

    return user_ids, user_names

def get_user_history(manager_id):
    endpoint = f'https://fantasy.premierleague.com/api/entry/{manager_id}/history/'
    response = requests.get(endpoint).json()
    current_season = response['current']

    user_dict = {}

    points = []
    cumulative_points = []
    gw_rank = []
    overall_rank = []
    gw_transfers = []
    hits = []
    points_on_bench = []

    for i in current_season:
        points.append(i['points'])
        cumulative_points.append(i['total_points'])
        gw_rank.append(i['rank'])
        overall_rank.append(i['overall_rank'])
        gw_transfers.append(i['event_transfers'])
        hits.append(i['event_transfers_cost'])
        points_on_bench.append(i['points_on_bench'])

    user_dict['points'] = points
    user_dict['cumulative_points'] = cumulative_points
    user_dict['gw_rank'] = gw_rank
    user_dict['overall_rank'] = overall_rank
    user_dict['gw_transfers'] = gw_transfers
    user_dict['hits'] = hits
    user_dict['points_on_bench'] = points_on_bench

    return user_dict

def create_league_dict(league_id):
    user_ids, user_names = get_league_members(league_id)
    league_dict = {}

    for i in range(len(user_ids)):
        user_dict = get_user_history(user_ids[i])
        league_dict[str(user_names[i])] = user_dict
        
    return league_dict


def telegram_bot_sendtext(bot_message, chat_id, path):
    files = {'photo':open(path,'rb')}
    send_text = 'https://api.telegram.org/bot' + telegram_api_key + '/sendPhoto?chat_id=' + chat_id  + '&parse_mode=MarkdownV2&caption=' + bot_message
    response = requests.post(send_text, files=files)
    return response.json()
