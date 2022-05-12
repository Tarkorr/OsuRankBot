import requests
import datetime

# version 1.1


class KEYS:
    OSU_API = "bab47c942d3ceda760dfcd8aca8856b0f795560f"
    OSU_API_V2 = "pR5lvVtUcQ82psQCWRhBTkwgUYYfPUZrqP2oU2Gf"


def get_data_beatmaps(mode: str = ""):
    # print(datetime.datetime.now()-datetime.timedelta(1))
    if mode == "":
        url = "https://osu.ppy.sh/api/get_beatmaps?k=" + KEYS.OSU_API + "&since=" \
              + str(datetime.datetime.now() - datetime.timedelta(1)) + "&m=" + mode
    else:
        url = "https://osu.ppy.sh/api/get_beatmaps?k=" + KEYS.OSU_API + "&since=" \
              + str(datetime.datetime.now() - datetime.timedelta(1)) + "&m=" + "0"
    r = requests.get(url=url)
    if r.status_code == 200:
        return r.json()
    else:
        print(f"The request failed. \nReason: {r.reason}")
        return


def get_data_beatmap(beatmap_id, mode: str = ""):
    if mode == "":
        url = "https://osu.ppy.sh/api/get_beatmaps?b=" + beatmap_id + "&k=" + KEYS.OSU_API
    else:
        url = "https://osu.ppy.sh/api/get_beatmaps?b=" + beatmap_id + "&k=" + KEYS.OSU_API + "&m=" + mode
    r = requests.get(url=url)
    if r.status_code == 200:
        return r.json()
    else:
        print(f"The request failed. \nReason: {r.reason}")
        return


def get_data_beatmapset(beatmapset_id, mode: str = ""):
    if mode == "":
        url = "https://osu.ppy.sh/api/get_beatmaps?b=" + beatmapset_id + "&k=" + KEYS.OSU_API
    else:
        url = "https://osu.ppy.sh/api/get_beatmaps?b=" + beatmapset_id + "&k=" + KEYS.OSU_API + "&m=" + mode
    r = requests.get(url=url)
    if r.status_code == 200:
        return r.json()
    else:
        print(f"The request failed. \nReason: {r.reason}")
        return


def get_data_user(user_id, mode: str = ""):
    if mode == "":
        url = "https://osu.ppy.sh/api/get_user?u=" + user_id + "&k=" + KEYS.OSU_API
    else:
        url = "https://osu.ppy.sh/api/get_user?u=" + user_id + "&k=" + KEYS.OSU_API + "&m=" + mode
    r = requests.get(url=url)
    if r.status_code == 200:
        return r.json()
    else:
        print(f"The request failed. \nReason: {r.reason}")
        return


def get_data_user_recent(user_id, mode: str = ""):
    if mode == "":
        url = "https://osu.ppy.sh/api/get_user_recent?u=" + user_id + "&k=" + KEYS.OSU_API
    else:
        url = "https://osu.ppy.sh/api/get_user_recent?u=" + user_id + "&k=" + KEYS.OSU_API + "&m=" + mode
    r = requests.get(url=url)
    if r.status_code == 200:
        return r.json()
    else:
        print(f"The request failed. \nReason: {r.reason}")
        return


def get_data_user_score(map_id, user_id, mode: str = ""):
    if mode == "":
        url = "https://osu.ppy.sh/api/get_scores?u=" + user_id + "&k=" + KEYS.OSU_API + "&b=" + map_id
    else:
        url = "https://osu.ppy.sh/api/get_scores?u=" + user_id + "&k=" + KEYS.OSU_API + "&b=" + map_id + "&m=" + mode
    r = requests.get(url=url)
    if r.status_code == 200:
        return r.json()
    else:
        print(f"The request failed. \nReason: {r.reason}")
        return
