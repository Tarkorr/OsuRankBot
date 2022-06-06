import requests
from bs4 import BeautifulSoup
from pprint import pprint
import datetime
from typing import Literal
from typing import Optional



class GET:
    
    
    def __init__(self):
        server = "seventwentyseven.xyz"
        server = "sakuru.pw"
        # server = "aisuru.xyz"
        server = "tski.moe"
        # server = "abypass.wtf"
        server = "cs0su.net"
        # server = "kurikku.pw" (akatsuki)
        # server = "denopia.ml" (not found)
        # server = "ripple.moe" (not found)
        # server = "osu.gatari.pw" (akatsuki)
        # server = "ez-pp.farm" (akatsuki)
        # server = "kawata.pw" (akatsuki)
        # server = "lemres.de" (bad request)
        # server = "ussr.pl" (bad gateway)
        # server = "cripple.moe" (akatsuki)
        # server = "masayuki.cf" (akatsuki)
        # server = "osu.shizofrenia.pw" (akatsuki)
        # server = "osu.chronoskia.com" (akatsuki)
        # server = "osu.datenshi.pw" (akatsuki)
        # server = "aeris-dev.pw" (akatsuki)
        # server = "katsumi.cf" (dead)
        # server = "tesco.moe" (SSLError)
        server = "nekos.cc"
        server = "fumosu.pw"
        # server = "rina.place" (not found)
        # server = "sukyio.xyz" (akatsuki)
        # server = "lazer.dhcpcd.xyz" (akatsuki)
        self.API_URL = f"https://api.{server}"
        pass
    
    
    def player_count(self):
        r = requests.get(f'{self.API_URL}/get_player_count')

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request player_count failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def player_info(self, scope: Literal["stats", "info", "all"], user_id: Optional[int] = None, username: Optional[str] = None):
        
        r = requests.get(f'{self.API_URL}/get_player_info?scope={scope}&name={username}')

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request player_count failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def player_status(self, user_id: Optional[int] = None, username: Optional[str] = None):
        r = requests.get(f'{self.API_URL}/get_player_status?id={user_id}')
        print(r.url)
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request player_status failed. args : "
                  f"\nReason: {r.reason}")
        return r.json()
    
    
    def player_scores(self,
        scope: Literal["recent", "best"],
        user_id: Optional[int] = None,
        username: Optional[str] = None,
        mods_arg: Optional[str] = None,
        mode_arg: int = 0,
        limit: int = 25,
        include_loved: bool = False,
        include_failed: bool = True):
        
        r = requests.get(f'{self.API_URL}/get_player_scores?id={user_id}&scope={scope}')
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request player_scores failed. args : "
                  f"\nReason: {r.reason}")
        return r.json()
    
    
    def player_most_played(self,
        user_id: Optional[int] = None,
        username: Optional[str] = None,
        mode_arg: int = 0,
        limit: int = 25):
        
        r = requests.get(f'{self.API_URL}/get_player_most_played?id={user_id}&limit={limit}')
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request player_scores failed. args : "
                  f"\nReason: {r.reason}")
        return r.json()
    
    
    def map_info(self,
        map_id: Optional[int] = None,
        md5: Optional[str] = None):
        
        if md5 is not None:
            r = requests.get(f'{self.API_URL}/get_map_info?md5={md5}')
        else:
            r = requests.get(f'{self.API_URL}/get_map_info?id={map_id}')
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request map_info failed. args : "
                  f"\nReason: {r.reason}")
        return r.json()
    
    
    def map_scores(self,
        scope: Literal["recent", "best"],
        map_id: Optional[int] = None,
        map_md5: Optional[str] = None,
        mods_arg: Optional[str] = None,
        mode_arg: int = 0,
        limit: int = 50):
        
        if map_md5 is not None:
             r = requests.get(f'{self.API_URL}/get_map_scores?scope={scope}&md5={map_md5}&mods_arg={mods_arg}&mode_arg={mode_arg}&limit={limit}')
        else:   
              r = requests.get(f'{self.API_URL}/get_map_scores?scope={scope}&id={map_id}&mods_arg={mods_arg}&mode_arg={mode_arg}&limit={limit}')
        
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request map_scores failed. args : "
                  f"\nReason: {r.reason}")
        return r.json()
    
    
    def score_info(self,
        score_id: int = ...):
        
        r = requests.get(f'{self.API_URL}/get_score_info?id={score_id}')

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request score_info failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def replay(self,
        score_id: int = ...,
        include_headers: bool = False):
        
        r = requests.get(f'{self.API_URL}/get_replay?id={score_id}&include_headers={include_headers}')
        
        if r.status_code == 200:
            return r.url
        else:
            print(f"The request replay failed. args : "
                  f"\nReason: {r.reason}")
        return 
    
    
    def match(self,
        match_id: int = ...):
        
        r = requests.get(f'{self.API_URL}/get_match?id={match_id}')

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_match failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def global_leaderboard(self,
        sort: Literal["tscore", "rscore", "pp", "acc"] = "pp",
        mode_arg: int = 0,
        limit: int = 25,
        offset: int = 0,
        country: Optional[str] = None):
        
        url = f'{self.API_URL}/get_leaderboard?sort={sort}&mode_arg={mode_arg}&limit={limit}&offset={offset}&mode_arg={mode_arg}'
        
        if country is not None:
            url = url + f"&country={country}"
            
        r = requests.get(url=url)
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_leaderboard failed. args : "
                  f"\nReason: {r.reason}")
        return r.json()
    
    
    def clan(self,
        clan_id: int = ...):
        
        r = requests.get(f'{self.API_URL}/get_clan?id={clan_id}')

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_clan failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def pool(self,
        pool_id: int = ...):
        
        r = requests.get(f'{self.API_URL}/get_pool?id={pool_id}')

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_pool failed. args : "
                  f"\nReason: {r.reason}")
        return {}


a = GET()
pprint(a.player_count())
# pprint(a.player_info(scope="all", username="xQc"))
# pprint(a.player_status(user_id=76))
# pprint(a.player_scores(scope="recent", user_id=76))
# pprint(a.player_most_played(user_id=76))
# pprint(a.map_info(map_id=3569917))
# pprint(a.map_scores(scope='recent', map_id=3569917))
# pprint(a.score_info(score_id=183764))
# pprint(a.replay(score_id=183764))
# pprint(a.global_leaderboard())
# pprint(a.clan(clan_id=1))
# pprint(a.pool(pool_id=10))