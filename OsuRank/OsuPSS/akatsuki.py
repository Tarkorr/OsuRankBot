import requests
from bs4 import BeautifulSoup
from pprint import pprint
import datetime
from typing import Literal
from typing import Optional



class GET:
    
    
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
        
        server = "akatsuki.pw"  # (akatsuki)
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
        
        self.API_URL = f"https://{server}"
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
    
    
    def scores(self, user: Optional[str] = None, mode: Optional[int] = 0, limit: Optional[int] = 50, relax: Optional[bool] = False, b: Optional[int] = 0):
        
        r = requests.get(f'{self.API_URL}/api/get_scores?b={b}&m={mode}&rx={relax}&u={user}&limit={limit}')
        print(r.url)

        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_scores failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    # limit, since (igonred imo c'est écrit), b, m, a, h, 
    def beatmaps(self, m: Optional[str] = "", limit: Optional[int] = 50, b: Optional[int] = 0, since: Optional[str] = "", h: Optional[str] = ""):
        
        # m = ????
        r = requests.get(f'{self.API_URL}/api/get_beatmaps?b={b}&limit={limit}&since={since}&h={h}')
        print(r.url)
        
        if r.status_code == 200 and r.json() is not None:
            return r.json()
        else:
            print(f"The request get_beatmaps failed. args : "
                  f"\nReason: {r.reason}")
        return {}
    
    


a = GET()
# pprint(a.user("NyanPotato"))  # (working)
# pprint(a.user_recent("Ahnnotea", 0))  # (working)
# pprint(a.user_best("Ahnnotea", 0))  # (working)
# pprint(a.scores(user="21922", mode=0, b=1860169))  # (working)
# pprint(a.beatmaps(b=1860169))   # (working)