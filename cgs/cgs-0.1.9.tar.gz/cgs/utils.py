import requests
from bs4 import BeautifulSoup
import json, os, platform, tempfile

def formattime(time: int) -> tuple:
    """
    adds zero to single digits
    """
    time = str(time)
    if len(time) < 2:
        starthour = "0" + time + ":00:00"
    else:
        starthour = time + ":00:00"
    endhour = str(int(time) + 1)
    if len(endhour) < 2:
        endhour = "0" + endhour + ":00:00"
    else:
        endhour = endhour + ":00:00"

    return (starthour, endhour)

def find_ressource_id(username, password, sportrange, proxies=None, r_session=None) -> list:
    '''finds the ressource id of an element, throws error if none'''
    login_data = {
        'email': username,
        'password': password,
        'login': 'submit',
        'resume': ''
    }
    try:
        if (r_session != None):
            r_session.post('https://scop-sas.csfoy.ca/booked_sas/Web/index.php', data=login_data, proxies=proxies)
            r = r_session.get(f'https://scop-sas.csfoy.ca/booked_sas/Web/schedule.php?sid={sportrange}', proxies=proxies)
        else:
            with requests.session() as session:
                session.post('https://scop-sas.csfoy.ca/booked_sas/Web/index.php', data=login_data, proxies=proxies)
                r = session.get(f'https://scop-sas.csfoy.ca/booked_sas/Web/schedule.php?sid={sportrange}', proxies=proxies)
        ress_soup = BeautifulSoup(r.text, features='html.parser')
        ress_id_list = []
        for i in ress_soup.find_all('a', {'class': 'resourceNameSelector'}):
            ress_id_list.append(i.get('resourceid'))

        return ress_id_list
    except:
        raise Exception("find_ressource_id error")

def get_uid(username, password, sport_id: list, proxies=None, r_session=None):
    """
    get the uid of user by looking at html response
    """
    print("trying to get userid..."+ sport_id[0])

    login_data = {'email': username, 'password': password, 'login': 'submit', 'resume': ''}
    if (r_session == None):
        session = requests.Session()
        # getting loggeg in
        session.post('https://scop-sas.csfoy.ca/booked_sas/Web/index.php', data=login_data, proxies=proxies)
    else:
        session = r_session

    try:
        dashboard = session.get(f"https://scop-sas.csfoy.ca/booked_sas/Web/schedule.php?sid={sport_id[0]}")
        dashboard_soup = BeautifulSoup(dashboard.text, features='html.parser')
        page_href = dashboard_soup.find('td', {'class': 'reservable'}).get('data-href')
        page_response = session.get(f"https://scop-sas.csfoy.ca/booked_sas/Web/{page_href}")
        page_soup = BeautifulSoup(page_response.text, features='html.parser')
        userid = page_soup.find('input', id='userId').get('value')
        if userid != None:
            configfile.mod("userID", userid)
            print("successfully fetched userid \U00002705") # green checkmark
        else:
            raise Exception
    except:
        try:
            get_uid(username, password, sport_id=sport_id[1:], proxies=proxies, r_session=session)
        except:
            raise Exception("CGS is currently unable to get the uid, try to add it manually or type 'cgs config -h' for help")


class _Config():
    """
    Parses and create a config object from configcgs.json
    """
    def __init__(self) -> None:
        # for production - from https://github.com/instaloader/instaloader/blob/3cc29a4ceb3ff4cd04a73dd4b20979b03128f454/instaloader/instaloader.py#L30
        try: # if file exist
            with open(os.path.join(self._get_config_dir(),'configcgs.json'), "r") as f:
                self.json = json.load(f)
        except:
            try: # if file not exist
                self.json = {
                    "gym_scheduleId": "64", 
                    "userID": "", 
                    "username": "", 
                    "password": "", 
                    "proxies": {}
                }
                with open(os.path.join(self._get_config_dir(),'configcgs.json'), "w+") as f:
                    json.dump(self.json, f)
            except:
                raise Exception("If you are having problems or you are using Windows, CGS will soon be available, see: https://github.com/Msa360/cgs-csfoy-gym for more info, or reach out to the devs.")
        self.gym_scheduleId = self.json["gym_scheduleId"]
        self.userID = self.json["userID"]
        self.username = self.json["username"]
        self.password = self.json["password"]
        self.proxies = self.json["proxies"]

    def __str__(self) -> str:
        return self.json.__str__()

    # https://github.com/instaloader/instaloader/blob/3cc29a4ceb3ff4cd04a73dd4b20979b03128f454/instaloader/instaloader.py#L30
    def _get_config_dir(self) -> str:
        if platform.system() == "Windows":
            # on Windows, use %LOCALAPPDATA%\
            localappdata = os.getenv("LOCALAPPDATA")
            if localappdata is not None:
                return localappdata
            # legacy fallback - store in temp dir if %LOCALAPPDATA% is not set
            return os.path.join(tempfile.gettempdir(), ".cgs-python")
        # on Unix, use ~/.config/
        return os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))

    def mod(self, key:str, value):
        """
        modify the value for the specified key in the configcgs.json
        "userID", "username", "password", "proxies"
        """
        self.json[key] = value
        # for production
        with open(os.path.join(self._get_config_dir(), 'configcgs.json'), "w") as f:
            json.dump(self.json, f)
        
configfile = _Config()
