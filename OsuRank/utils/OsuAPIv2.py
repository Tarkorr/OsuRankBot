import datetime
from pprint import pprint
import requests
import json
# version 2.0.1

API_URL = "https://osu.ppy.sh/api/v2"
cfg = json.loads(open("config_OSU.json", "r").read())

client_secret = cfg["client_secret"]
client_id = cfg["client_id"]

def get_token():
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "public",
    }
    result = requests.post("https://osu.ppy.sh/oauth/token", data=data)
    if result.status_code != 200:
        print(f"the request get_token failed, \nreason: {result.reason}")
        return get_token()
    return result.json().get('access_token')


def get_data_beatmaps(ids: list):
    """
    not tested yet.
    :param ids:
    :return:
    """
    token = get_token()

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    params = {
        "ids": ids
    }

    r = requests.get(f'{API_URL}/beatmaps', headers=headers, params=params)

    if r.status_code == 200:
        if r.json() is not None:
            return r.json()
    else:
        print(f"The request get_data_beatmaps failed. args :{ids}. \nReason: {r.reason}")
        return


def get_data_beatmapsets_events():
    token = get_token()

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    params = {
        "limit": 50,
        "beatmapset_status": "ranked"
    }

    r = requests.get(f'{API_URL}/beatmapsets/events', headers=headers, params=params)

    if r.status_code == 200:
        if r.json() is not None:
            return r.json()
    else:
        print(f"The request get_data_beatmap failed. args : \nReason: {r.reason}")
        return


def get_data_beatmap(beatmap_id):
    token = get_token()

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    r = requests.get(f'{API_URL}/beatmaps/{str(beatmap_id)}', headers=headers)

    if r.status_code == 200:
        if r.json() is not None:
            return r.json()
    else:
        print(f"The request get_data_beatmap failed. args : {beatmap_id} \nReason: {r.reason}")
        return


def get_data_beatmapset(beatmapset_id):
    token = get_token()

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    r = requests.get(f'{API_URL}/beatmapsets/{beatmapset_id}', headers=headers)

    if r.status_code == 200:
        if r.json() is not None:
            return r.json()
    else:
        print(f"The request get_data_beatmapset failed. args : {beatmapset_id} \nReason: {r.reason}")
        return


def get_data_user(user_id, mode: str = ""):
    token = get_token()

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    r = requests.get(f'{API_URL}/users/{user_id}/{mode}', headers=headers)

    if r.status_code == 200:
        if r.json() is not None:
            return r.json()
    else:
        print(f"The request get_data_user failed. args : {user_id}, {mode} \nReason: {r.reason} "
              f"\nstatus code : {r.status_code}")
        if r.status_code == 404:
            return "404"
        return


def get_data_user_score(map_id, user_id, mods: str = "", mode: str = ""):
    token = get_token()

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # "mods": f"{mods}" // TODO when available
    params = {
        "mode": mode,
    }

    r = requests.get(f'{API_URL}/beatmaps/{map_id}/scores/users/{user_id}', headers=headers, params=params)

    if r.status_code == 200:
        if r.json() is not None:
            return r.json()
    else:
        print(f"The request get_data_user_score failed. args : {map_id}, {user_id}, {mode} \nReason: {r.reason}")
        return


def get_data_user_scores(map_id, user_id, mode: str = ""):
    token = get_token()

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    params = {
        "mode": mode,
    }

    r = requests.get(f'{API_URL}/beatmaps/{map_id}/scores/users/{user_id}/all', headers=headers, params=params)

    if r.status_code == 200:
        if r.json() is not None:
            return r.json()
    else:
        print(f"The request get_data_user_score failed. args : {map_id}, {user_id}, {mode} \nReason: {r.reason}")
        return


def get_data_user_recent(user_id, mode: str = "osu"):
    token = get_token()

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    params = {
        "mode": mode,
        "limit": 5
    }

    r = requests.get(f'{API_URL}/users/{user_id}/scores/recent', headers=headers, params=params)

    if r.status_code == 200:
        if r.json() is not None:
            return r.json()
    else:
        print(f"The request get_data_user_recent failed. args : {user_id}, {mode} \n Reason: {r.reason}")
        return


def get_data_user_best(user_id, mode: str = "osu", limit: int = 5):
    token = get_token()

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    params = {
        "mode": mode,
        "limit": limit
    }

    r = requests.get(f'{API_URL}/users/{user_id}/scores/best', headers=headers, params=params)

    if r.status_code == 200:
        if r.json() is not None:
            return r.json()
    else:
        print(f"The request get_data_user_recent failed. args : {user_id}, {mode} \n Reason: {r.reason}")
        return


def search(query, mode: str = ""):
    token = get_token()

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    params = {
        "query": query,
        "mode": mode
    }

    r = requests.get(f'{API_URL}/search', headers=headers, params=params)

    if r.status_code == 200:
        if r.json() is not None:
            return r.json()
    else:
        print(f"The request get_data_user_recent failed. args : {mode}, {query} \n Reason: {r.reason}")
        return


# pprint(search("Tarkor"))
# pprint(get_data_user_recent("16748782", "mania"))
# pprint(get_data_user_recent(user_id="16748782", mode="mania"), depth=2)
# pprint(get_data_user("16748782", "mania"), depth=2)
# pprint(get_data_user_score(user_id="16748782", map_id="2191733"), depth=3)
# pprint(get_data_beatmapset("1488666"), indent=2, depth=2)
