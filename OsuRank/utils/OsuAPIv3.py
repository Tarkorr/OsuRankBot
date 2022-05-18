import requests
import json
import typing

# TODO BEATMAPS:
# - lookup
# - Beatmap Attributes
#
class API:
     
    def __init__(self):
        
        self.cfg = json.loads(open("config_OSU.json", "r").read())
        
        self.url = "https://osu.ppy.sh/api/v2"
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_token()}'
        }
        
    # TOKEN 
    def get_token(self):
        
        client_id = self.cfg["client_id"]
        client_secret = self.cfg["client_secret"]
        
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "scope": "public",
        }
        
        r = requests.post("https://osu.ppy.sh/oauth/token", data=data)
        if r.status_code == 200:
            return r.json().get('access_token')
        else:
            print(f"the request get_token failed, \nReason: {r.reason}")
            return None
        
    
    # Beatmap related
    # get_data_beatmap
    def get_beatmap(self, 
                    beatmap_id: int):

        r = requests.get(f'{self.url}/beatmaps/{str(beatmap_id)}', headers=self.headers)

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_data_beatmap failed. args : "
                  f"\nbeatmap_id: {beatmap_id} \nReason: {r.reason}")
        return dict()
    
    
    # old: get_data_beatmaps
    def get_beatmaps(self, 
                     ids: list):
        params = {
            "ids": ids
        }

        r = requests.get(f'{self.url}/beatmaps', headers=self.headers, params=params)

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_data_beatmaps failed. args : "
                  f"\nids: {ids}. \nReason: {r.reason}")
        return dict()
    
    
    def get_beatmap_scores(self, 
                           beatmap_id: int, 
                           mode: str = "osu"):
        params = {
            "mode": mode
        }

        r = requests.get(f'{self.url}/beatmaps/{beatmap_id}/scores', headers=self.headers, params=params)

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_data_beatmaps failed. args : "
                  f"\nbeatmap_id: {beatmap_id}, mode: {mode}. \nReason: {r.reason}")
        return dict()


    # old: get_data_beatmapset
    def get_beatmapset(self, 
                       beatmapset_id: int):

        r = requests.get(f'{self.url}/beatmapsets/{beatmapset_id}', headers=self.headers)

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_data_beatmapset failed. args : "
                  f"\nbeatmapset_id: {beatmapset_id} \nReason: {r.reason}")
        return dict()
    
    
    # not documented
    # old: get_data_beatmapsets_events
    def get_beatmapsets_events(self, 
                               limit: int, 
                               beatmapset_status: str):

        params = {
            "limit": limit,
            "beatmapset_status": beatmapset_status
        }

        r = requests.get(f'{self.url}/beatmapsets/events', headers=self.headers, params=params)

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_data_beatmap failed. args :"
                  f"\nlimit: {limit}, beatmapset_status: {beatmapset_status} \nReason: {r.reason}")
        return dict()
    
    
    
    
    # USER RELATED
    # default mode set to: osu
    # old: get_user
    # typing hints et default arguments
    def get_user(self, 
                 user: str,
                 mode: str = "osu"):

        r = requests.get(f'{self.url}/users/{user}/{mode}', headers=self.headers)

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_data_user failed. args : "
                  f"\nuser: {user}, mode: {mode} \nReason: {r.reason} ")
        return dict()
    
    
    def get_users(self, 
                  ids: list):
        
        params = {
            "ids": ids
        }

        r = requests.get(f'{self.url}/users', headers=self.headers, params=params)

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_data_user failed. args : "
                  f"\nids: {ids} \nReason: {r.reason} ")
        return dict()
    
    
    def get_user_score(self, user: str,
                             type: str,
                             offset: str = "",
                             include_fails: int = 0,
                             limit: int = 5,
                             mode: str = "osu"):

        params = {
            "include_fails": include_fails,
            "mode": mode,
            "limit": limit,
            "offset": offset
        }

        r = requests.get(f'{self.url}/users/{user}/scores/{type}', headers=self.headers, params=params)

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_data_user_recent failed. args : "
                  f"\nuser: {user}, type: {type}, offset: {offset},"
                  f"\ninclude_fails: {include_fails}, limit: {limit}, mode: {mode} \nReason: {r.reason}")
        return dict()
    

    #old: get_data_user_score
    def get_user_beatmap_score(self, 
                               beatmap_id: int, 
                               user: str,
                               mode: str = "osu"):

        # "mods": mods // TODO when available
        params = {
            "mode": mode,
        }

        r = requests.get(f'{self.url}/beatmaps/{beatmap_id}/scores/users/{user}', headers=self.headers, params=params)

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_data_user_score failed. args : "
                  f"\nbeatmap_id: {beatmap_id}, user: {user}, mode: {mode} \nReason: {r.reason}")
        
        return dict()
    
    # old: get_data_user_scores
    def get_user_beatmap_scores(self, 
                                beatmap_id: int, 
                                user: str, 
                                mode: str = "osu"):

        params = {
            "mode": mode,
        }

        r = requests.get(f'{self.url}/beatmaps/{beatmap_id}/scores/users/{user}/all', headers=self.headers, params=params)

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_data_user_score failed. args : "
                  f"\nbeatmap_id: {beatmap_id}, user: {user}, mode: {mode} \nReason: {r.reason}")
        return dict()
    
    
    
    # OTHER imo
    # mode is not [osu, mania, ctb, fruits]
    # mode: all, user, wiki_page, default: all
    def search(self, 
               query: str, 
               page: int = 0, 
               mode: str = ""):

        params = {
            "query": query,
            "mode": mode,
            "page": page
        }

        r = requests.get(f'{self.url}/search', headers=self.headers, params=params)

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_data_user_recent failed. args : "
                  f"\n{mode}, {query} \n Reason: {r.reason}")
            
        return dict()