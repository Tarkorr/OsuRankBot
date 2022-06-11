import requests
from bs4 import BeautifulSoup
from pprint import pprint
import datetime
from typing import Literal
from typing import Optional
import json


class GET:
    # TODO https://akatsuki.pw/api/status
    
    
    def __init__(self):
        # server = "cs0su.net"  # (727)
        # server = "seventwentyseven.xyz"  # (727)
        # server = "sakuru.pw"  # (727)
        # server = "tski.moe"  # (727)
        # server = "nekos.cc"  # (727)
        # server = "fumosu.pw"  # (727)
        
        # server = "aeris-dev.pw"  # (akatsuki) --> NOT WORKING, result:
        # server = "sukyio.xyz"  # (akatsuki) --> NOT WORKING, result:
        # server = "osu.shizofrenia.pw"  # (akatsuki) --> NOT WORKING, result:
        # server = "lazer.dhcpcd.xyz"  # (akatsuki) --> NOT WORKING, result: Bad Gateway
        # server = "osu.gatari.pw"  # (akatsuki) --> NOT WORKING, result: OK
        # server = "masayuki.cf"  # (akatsuki) --> NOT WORKING, result: Not Found
        # server = "abypass.wtf"  # (akatsuki) --> NOT WORKING, result: Not Found
        # server = "lemres.de"   # (akatsuki) --> NOT WORKING, result: Not Found
        # server = "tesco.moe"   # (akatsuki) --> NOT WORKING, result: Not Found
        
        # server = "akatsuki.pw"  # (akatsuki)
        # server = "kurikku.pw"  # (akatsuki)
        # server = "ez-pp.farm"  # (akatsuki)
        # server = "kawata.pw"  # (akatsuki)
        # server = "cripple.moe"  # (akatsuki)
        # server = "osu.chronoskia.com"  # (akatsuki)
        # server = "osu.datenshi.pw"  # (akatsuki)
        # server = "denopia.ml"  # (akatsuki)
        # server = "ripple.moe"  # (akatsuki)
        # server = "ussr.pl"   # (akatsuki)
        # server = "rina.place"   # (akatsuki)
                
        # server = "aisuru.xyz"
        # server = "katsumi.cf" --> Dead
        
        server = "ripple.moe"
        
        self.API_URL = f"https://{server}"
        self.cfg = json.loads(open("config_OSU.json", "r").read())
        self.token = self.cfg["Ripple_token"]
        pass
    
    #\=========================================\
    #
    #                  Peppy
    #
    #\=========================================\
    def user(self, user: Optional[str] = None, mode: Optional[int] = 0):
        
        r = requests.get(f'{self.API_URL}/api/get_user?u={user}&m={mode}')

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_user failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    # empty /akatsuki-api/blob/master/app/peppy/match.go
    def match(self):
        
        r = requests.get(f'{self.API_URL}/api/get_match')

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_match failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def user_recent(self, user: Optional[str] = None, mode: Optional[int] = 0, limit: Optional[int] = 50):
        
        r = requests.get(f'{self.API_URL}/api/get_user_recent?u={user}&m={mode}&limit={limit}')

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_user_recent failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def user_best(self, user: Optional[str] = None, mode: Optional[int] = 0, limit: Optional[int] = 50):
        
        r = requests.get(f'{self.API_URL}/api/get_user_best?u={user}&m={mode}&limit={limit}')

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_user_best failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def Pscores(self, user: Optional[str] = None, mode: Optional[int] = 0, limit: Optional[int] = 50, relax: Optional[bool] = False, b: Optional[int] = 0):
        
        r = requests.get(f'{self.API_URL}/api/get_scores?b={b}&m={mode}&rx={relax}&u={user}&limit={limit}')
        print(r.url)

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request [Pscores] get_scores failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    # limit, since (igonred imo c'est écrit), b, m, a, h, 
    def beatmaps(self, m: Optional[str] = "", limit: Optional[int] = 50, b: Optional[int] = 0, since: Optional[str] = "", h: Optional[str] = ""):
        
        # m = ????
        r = requests.get(f'{self.API_URL}/api/get_beatmaps?b={b}&limit={limit}&since={since}&h={h}')
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_beatmaps failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    #\=========================================\
    #
    #                  API V1
    #
    #\=========================================\
    def ping(self):
        
        r = requests.get(f'{self.API_URL}/api/v1/ping?k={self.token}')
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request ping failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def surprise_me(self):
        
        r = requests.get(f'{self.API_URL}/api/v1/surprise_me?k={self.token}')
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request surprise_me failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    def tokens(self):
        
        r = requests.get(f'{self.API_URL}/api/v1/tokens?k={self.token}')
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request tokens failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def badges(self):
        
        r = requests.get(f'{self.API_URL}/api/v1/badges?k={self.token}')
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request badges failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def badges_members(self, badge_id: int):
        
        r = requests.get(f'{self.API_URL}/api/v1/badges/members?k={self.token}&id={badge_id}')
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request badges_members failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def users(self, sort: Literal["id", "username", "privileges", "donor_expire", "latest_activity", "silence_end"], 
              iid : Optional[int] = None, 
              nname: Optional[str] = None, 
              ids: Optional[list] = [], 
              names: Optional[list] = [], 
              names_aka: Optional[list] = [], 
              countries: Optional[list] = [], 
              limit: Optional[int] = 10):
        
        url = f'{self.API_URL}/api/v1/users?k={self.token}'
        if ids is not None:
            if len(ids) > 1:
                for i in ids:
                    url = url + f"&ids={i}"
        
        if names is not None:
            if len(names) > 1:
                for i in names:
                    url = url + f"&names={i}"
        
        if names_aka is not None:
            if len(names_aka) > 1:
                for i in names_aka:
                    url = url + f"&names_aka={i}"
        
        if countries is not None:
            print("ok")
            if len(countries) > 1:
                for i in countries:
                    url = url + f"&countries={i}"
        
        if iid is not None:
            url = url + f'&id={iid}'
        
        if nname is not None:
            url = url + f"&name={nname}"  
                 
        r = requests.get(url=f"{url}&sort={sort}&l={limit}")
        print(r.url)
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request users failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    # must: iid or nname
    def users_full(self, relax: Literal[0, 1, -1], 
              iid: Optional[int] = None,
              nname: Optional[str] = None):
        
        url = f'{self.API_URL}/api/v1/users/full?k={self.token}'
        
        if iid is not None:
            url = url + f'&id={iid}'
        elif nname is not None:
            url = url + f"&name={nname}"
        else:
            return {"error": "iid or nname is required."}
                 
        r = requests.get(url=f"{url}&relax={relax}")
        print(r.url)
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request users_full failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    def users_whatid(self, nname: str):
        
        r = requests.get(f'{self.API_URL}/api/v1/users/whatid?k={self.token}&name={nname}')
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request users_whatid failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    # name doesn't work ?
    def users_userpage(self,
              iid: Optional[int] = None,
              nname: Optional[str] = None):
        
        url = f'{self.API_URL}/api/v1/users/userpage?k={self.token}'
        
        if iid is not None:
            url = url + f'&id={iid}'
        elif nname is not None:
            url = url + f"&name={nname}"
        else:
            return {"error": "iid or nname is required."}
                 
        r = requests.get(url=url)
        print(r.url)
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request users_userpage failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def users_lookup(self, nname: str):
        
        r = requests.get(f'{self.API_URL}/api/v1/users/lookup?k={self.token}&name={nname}')
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request users_lookup failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def users_achievements(self,
              iid: Optional[int] = None,
              nname: Optional[str] = None):
        
        url = f'{self.API_URL}/api/v1/users/achievements?k={self.token}'
        
        if iid is not None:
            url = url + f'&id={iid}'
        elif nname is not None:
            url = url + f"&name={nname}"
        else:
            return {"error": "iid or nname is required."}
                 
        r = requests.get(url=url)
        print(r.url)
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request users_achievements failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    def users_most_played(self,
              iid: Optional[int] = None,
              nname: Optional[str] = None):
        
        url = f'{self.API_URL}/api/v1/users/most_played?k={self.token}'
        
        if iid is not None:
            url = url + f'&id={iid}'
        elif nname is not None:
            url = url + f"&name={nname}"
        else:
            return {"error": "iid or nname is required."}
                 
        r = requests.get(url=url)
        print(r.url)
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request users_most_played failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    # b or md5 is needed
    def scores(self,
               sort: Literal["pp", "score", "accuracy", "id"],
               relax: Literal[0, 1, -1],
               md5 : Optional[str] = None, 
               b: Optional[int] = None, 
               mode: Optional[str] = "",
               limit: Optional[int] = 10):
        
        url = f'{self.API_URL}/api/v1/scores?k={self.token}'
        
        if md5 is not None:
            url = url + f'&md5={md5}'
        elif b is not None:
            url = url + f"&b={b}"
        else:
            return {"error": "md5 or b is required."}
                 
        r = requests.get(url=f"{url}&sort={sort}&relax={relax}&mode={mode}&l={limit}")
        print(r.url)
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request scores failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    # must: iid or nname
    def users_scores_recent(self, 
                            relax: Literal[0, 1, -1],
                            mode: Optional[str] = "",
                            iid: Optional[int] = None,
                            nname: Optional[str] = None,
                            limit: Optional[int] = 10):
        
        url = f'{self.API_URL}/api/v1/users/scores/recent?k={self.token}'
        
        if iid is not None:
            url = url + f'&id={iid}'
        elif nname is not None:
            url = url + f"&name={nname}"
        else:
            return {"error": "iid or nname is required."}
                 
        r = requests.get(url=f"{url}&relax={relax}&mode={mode}&l={limit}")
        print(r.url)
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request users_scores_recent failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    
    # must: iid or nname
    def users_scores_best(self, 
                            relax: Literal[0, 1, -1],
                            mode: Optional[str] = "",
                            iid: Optional[int] = None,
                            nname: Optional[str] = None,
                            limit: Optional[int] = 10):
        
        url = f'{self.API_URL}/api/v1/users/scores/best?k={self.token}'
        
        if iid is not None:
            url = url + f'&id={iid}'
        elif nname is not None:
            url = url + f"&name={nname}"
        else:
            return {"error": "iid or nname is required."}
                 
        r = requests.get(url=f"{url}&relax={relax}&mode={mode}&l={limit}")
        print(r.url)
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request users_scores_best failed. args : "
                  f"\nReason: {r.reason}")
        return {}


a = GET()
pprint(a.ping())
# pprint(a.user("NyanPotato"))  # (working)
# pprint(a.user_recent("Ahnnotea", 0))  # (working)
# pprint(a.user_best("Ahnnotea", 0))  # (working)
# pprint(a.scores(user="21922", mode=0, b=1860169))  # (working)
# pprint(a.beatmaps(b=1860169))   # (working)