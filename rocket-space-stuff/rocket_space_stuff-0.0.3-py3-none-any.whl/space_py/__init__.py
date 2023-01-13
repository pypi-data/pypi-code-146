import requests
import datetime
from datetime import date, datetime


class SpaceApi:
    def __init__(self):
        self.__default_url = "http://127.0.0.1:4533"
        self.__url = self.__default_url

    @staticmethod
    def populate_launch(name: str, net: str, status_name: str, launch_service_provider_name: str,
                        rocket_config_full_name: str,
                        mission_description: str, pad_location_name: str,
                        window_start: str = "None", window_end: str = "None", fail_reason: str = "None",
                        image: str = "None",
                        infographic: str = "None", orbital_launch_attempt_count: str = "None",
                        orbital_launch_attempt_count_year: str = "None",
                        location_launch_attempt_count: str = "None", location_launch_attempt_count_year: str = "None",
                        pad_launch_attempt_count: str = "None", pad_launch_attempt_count_year: str = "None",
                        agency_launch_attempt_count: str = "None", agency_launch_attempt_count_year: str = "None",
                        launch_service_provider_type: str = "None", rocket_id: str = "None",
                        mission_name: str = "None", mission_type: str = "None",
                        mission_orbit_name: str = "None", pad_wiki_url: str = "None", pad_longitude: str = "None",
                        pad_latitude: str = "None",
                        pad_location_country_code: str = "None"):
        temp_dict = {"name": name, "net": net, "window_start": window_start,
                     "window_end": window_end, "failreason": fail_reason, "image": image,
                     "infographic": infographic,
                     "orbital_launch_attempt_count": orbital_launch_attempt_count,
                     "orbital_launch_attempt_count_year": orbital_launch_attempt_count_year,
                     "location_launch_attempt_count": location_launch_attempt_count,
                     "location_launch_attempt_count_year": location_launch_attempt_count_year,
                     "pad_launch_attempt_count": pad_launch_attempt_count,
                     "pad_launch_attempt_count_year": pad_launch_attempt_count_year,
                     "agency_launch_attempt_count": agency_launch_attempt_count,
                     "agency_launch_attempt_count_year": agency_launch_attempt_count_year,
                     "status_name": status_name,
                     "launch_service_provider_name": launch_service_provider_name,
                     "launch_service_provider_type": launch_service_provider_type, "rocket_id": rocket_id,
                     "rocket_configuration_full_name": rocket_config_full_name,
                     "mission_name": mission_name, "mission_description": mission_description,
                     "mission_type": mission_type, "mission_orbit_name": mission_orbit_name,
                     "pad_wiki_url": pad_wiki_url, "pad_longitude": pad_longitude,
                     "pad_latitude": pad_latitude, "pad_location_name": pad_location_name,
                     "pad_location_country_code": pad_location_country_code}
        return Launch(temp_dict)

    @staticmethod
    def populate_launcher(launcher_config_full_name: str, serial_number: str, status: str, details: str, flights: str,
                          image_url: str = "None",
                          last_launch_date: str = "None", first_launch_date: str = "None",
                          flight_proven: str = "False"):
        temp_dict = {"flight_proven": flight_proven, "serial_number": serial_number, "status": status,
                     "details": details, "image_url": image_url, "flights": flights,
                     "last_launch_date": last_launch_date, "first_launch_date": first_launch_date,
                     "launcher_config_full_name": launcher_config_full_name}
        return Launcher(temp_dict)

    @staticmethod
    def populate_astro(name: str, birth: str, death: str, nationality: str, description: str, flights: str,
                       landings: str, last_fl: str, agency_acr: str, twitter: str = "None", insta: str = "None",
                       wiki: str = "None", profile_img: str = "None", profile_img_thmb: str = "None",
                       first_fl: str = "None",
                       status: str = "None", enroll: str = "None", agency: str = "None", agency_type: str = "None",
                       agency_countries: str = "None", agency_logo: str = "None"):
        temp_dict = {"name": name, "date_of_birth": birth, "date_of_death": death, "nationality": nationality,
                     "bio": description,
                     "twitter": twitter, "instagram": insta, "wiki": wiki,
                     "profile_image": profile_img,
                     "profile_image_thumbnail": profile_img_thmb,
                     "flights_count": flights, "landings_count": landings, "last_flight": last_fl,
                     "first_flight": first_fl, "status_name": status, "type_name": enroll,
                     "agency_name": agency, "agency_type": agency_type,
                     "agency_country_code": agency_countries, "agency_abbrev": agency_acr,
                     "agency_logo_url": agency_logo}
        return Astronaut(temp_dict)

    @property
    def url(self):
        return self.__url

    def set_new_url(self, value: str):
        self.__url = value

    @property
    def default_url(self):
        return self.__default_url

    # Start of Astronaut methods

    def find_astro_by(self, variable: str, value):
        url = f"{self.url}/astronauts/{variable}/'{value}'"
        r = requests.get(url)
        if str(r) == "<Response [404]>":
            return {"error": f"Entry not found:  {variable} == {value}"}
        key = list(r.json(strict=False).keys())[0]
        response = r.json(strict=False)[key]
        return Astronaut(response)

    def search_astro_by(self, variable: str, value):
        astro_dict = {}
        url = f"{self.url}/astronauts/search?{variable}={value}"
        r = requests.get(url)
        if str(r) == "<Response [404]>":
            return {"error": f"Entry not found:  {variable} == {value}"}
        key_list = list(r.json(strict=False).keys())
        for key in key_list:
            astro_dict[int(key)] = Astronaut(r.json(strict=False)[key])
        return astro_dict

    def add_astro(self, astro: Astronaut):
        url = f"{self.url}/astronauts"
        r = requests.post(url, json=astro.jsonify)
        return r.json()

    def delete_astro_by(self, variable: str, value):
        url = f"{self.url}/astronauts/{variable}/'{value}'"
        r = requests.delete(url)
        return r.json()

    def update_astro_by(self, variable: str, value, astro: Astronaut):
        url = f"{self.url}/astronauts/{variable}/'{value}'"
        r = requests.put(url, json=astro.jsonify)
        return r.json()

    # Start of Launcher methods

    def find_launcher_by(self, variable: str, value):
        url = f"{self.url}/launchers/{variable}/'{value}'"
        r = requests.get(url)
        if str(r) == "<Response [404]>":
            return {"error": f"Entry not found:  {variable} == {value}"}
        key = list(r.json(strict=False).keys())[0]
        response = r.json(strict=False)[key]
        return Launcher(response)

    def search_launcher_by(self, variable: str, value):
        launcher_dict = {}
        url = f"{self.url}/launchers/search?{variable}={value}"
        r = requests.get(url)
        if str(r) == "<Response [404]>":
            return {"error": f"Entry not found:  {variable} == {value}"}
        key_list = list(r.json(strict=False).keys())
        for key in key_list:
            launcher_dict[int(key)] = Launcher(r.json(strict=False)[key])
        return launcher_dict

    def add_launcher(self, launcher: Launcher):
        url = f"{self.url}/launchers"
        r = requests.post(url, json=launcher.jsonify)
        return r.json()

    def delete_launcher_by(self, variable: str, value):
        url = f"{self.url}/launchers/{variable}/'{value}'"
        r = requests.delete(url)
        return r.json()

    def update_launcher_by(self, variable: str, value, launcher: Launcher):
        url = f"{self.url}/launchers/{variable}/'{value}'"
        r = requests.put(url, json=launcher.jsonify)
        return r.json()

    # Start of Launch methods

    def find_launch_by(self, variable: str, value):
        url = f"{self.url}/launches/{variable}/'{value}'"
        r = requests.get(url)
        if str(r) == "<Response [404]>":
            return {"error": f"Entry not found:  {variable} == {value}"}
        key = list(r.json(strict=False).keys())[0]
        response = r.json(strict=False)[key]
        return Launch(response)

    def search_launch_by(self, variable: str, value):
        launch_dict = {}
        url = f"{self.url}/launches/search?{variable}={value}"
        r = requests.get(url)
        if str(r) == "<Response [404]>":
            return {"error": f"Entry not found:  {variable} == {value}"}
        key_list = list(r.json(strict=False).keys())
        for key in key_list:
            launch_dict[int(key)] = Launch(r.json(strict=False)[key])
        return launch_dict

    def add_launch(self, launch: Launch):
        url = f"{self.url}/launches"
        r = requests.post(url, json=launch.jsonify)
        return r.json()

    def delete_launch_by(self, variable: str, value):
        url = f"{self.url}/launches/{variable}/'{value}'"
        r = requests.delete(url)
        return r.json()

    def update_launch_by(self, variable: str, value, launch: Launch):
        url = f"{self.url}/launches/{variable}/'{value}'"
        r = requests.put(url, json=launch.jsonify)
        return r.json()

class Launcher:
    def __init__(self, json: dict = None):
        if json is not None:
            self.__flight_proven = json["flight_proven"]
            self.__serial_number = json["serial_number"]
            self.__status = json["status"]
            self.__details = json["details"]
            self.__image_url = json["image_url"]
            self.__flights = json["flights"]
            self.__last_launch_date = json["last_launch_date"]
            self.__first_launch_date = json["first_launch_date"]
            self.__launcher_config_full_name = json["launcher_config_full_name"]
        else:
            self.__flight_proven = None
            self.__serial_number = None
            self.__status = None
            self.__details = None
            self.__image_url = None
            self.__flights = None
            self.__last_launch_date = None
            self.__first_launch_date = None
            self.__launcher_config_full_name = None

    @property
    def full_name(self):
        return self.__launcher_config_full_name

    @property
    def serial_n(self):
        return self.__serial_number

    @property
    def status(self):
        return self.__status

    @property
    def description(self):
        return self.__details

    @property
    def launcher_image(self):
        return self.__image_url

    @property
    def flights_count(self):
        return self.__flights

    @property
    def is_flight_proven(self):
        return self.__flight_proven == "True"

    @property
    def last_launch(self):
        return self.__last_launch_date

    @property
    def first_launch(self):
        return self.__first_launch_date

    def __repr__(self):
        return f"\nEXTENDED LAUNCHER INFO:\nFull Name: {self.__launcher_config_full_name}\nSerial Number: {self.__serial_number}\n" \
               f"Status: {self.__status}\nDescription: {self.__details}\nLauncher Image: {self.__image_url}\n" \
               f"Flights count: {self.__flights}\nIs Flight Proven: {self.__flight_proven}\nLast launch date: {self.__last_launch_date}\n" \
               f"First launch date: {self.__first_launch_date}"

    @property
    def show_basic_info(self):
        return f"\nBASIC LAUNCHER INFO:\nFull Name: {self.__launcher_config_full_name}\n" \
               f"Status: {self.__status}\nDescription: {self.__details}\nLauncher Image: {self.__image_url}\n"

    @property
    def jsonify(self):
        return {"flight_proven": self.__flight_proven, "serial_number": self.__serial_number, "status": self.__status,
                "details": self.__details, "image_url": self.__image_url, "flights": self.__flights,
                "last_launch_date": self.__last_launch_date, "first_launch_date": self.__first_launch_date,
                "launcher_config_full_name": self.__launcher_config_full_name}

    @full_name.setter
    def full_name(self, value):
        self.__launcher_config_full_name = value

    @serial_n.setter
    def serial_n(self, value):
        self.__serial_number = value

    @status.setter
    def status(self, value):
        self.__status = value

    @description.setter
    def description(self, value):
        self.__details = value

    @launcher_image.setter
    def launcher_image(self, value):
        self.__image_url = value

    @flights_count.setter
    def flights_count(self, value):
        self.__flights = value

    @is_flight_proven.setter
    def is_flight_proven(self, value):
        self.__flight_proven = value

    @last_launch.setter
    def last_launch(self, value):
        self.__last_launch_date = value

    @first_launch.setter
    def first_launch(self, value):
        self.__first_launch_date = value


class Launch:
    def __init__(self, json: dict = None):
        if json is not None:
            self.__name = json["name"]
            self.__net = json["net"]
            self.__window_end = json["window_end"]
            self.__window_start = json["window_start"]
            self.__fail_reason = json["failreason"]
            self.__image = json["image"]
            self.__infographic = json["infographic"]
            self.__orbital_launch_attempt_count = json["orbital_launch_attempt_count"]
            self.__location_launch_attempt_count = json["location_launch_attempt_count"]
            self.__pad_launch_attempt_count = json["pad_launch_attempt_count"]
            self.__agency_launch_attempt_count = json["agency_launch_attempt_count"]
            self.__orbital_launch_attempt_count_year = json["orbital_launch_attempt_count_year"]
            self.__location_launch_attempt_count_year = json["location_launch_attempt_count_year"]
            self.__pad_launch_attempt_count_year = json["pad_launch_attempt_count_year"]
            self.__agency_launch_attempt_count_year = json["agency_launch_attempt_count_year"]
            self.__status_name = json["status_name"]
            self.__launch_service_provider_name = json["launch_service_provider_name"]
            self.__launch_service_provider_type = json["launch_service_provider_type"]
            self.__rocket_id = json["rocket_id"]
            self.__rocket_config_full_name = json["rocket_configuration_full_name"]
            self.__mission_name = json["mission_name"]
            self.__mission_description = json["mission_description"]
            self.__mission_type = json["mission_type"]
            self.__mission_orbit_name = json["mission_orbit_name"]
            self.__pad_wiki_url = json["pad_wiki_url"]
            self.__pad_latitude = json["pad_latitude"]
            self.__pad_longitude = json["pad_longitude"]
            self.__pad_location_name = json["pad_location_name"]
            self.__pad_location_country_code = json["pad_location_country_code"]
        else:
            self.__name = None
            self.__net = None
            self.__window_end = None
            self.__window_start = None
            self.__fail_reason = None
            self.__image = None
            self.__infographic = None
            self.__orbital_launch_attempt_count = None
            self.__location_launch_attempt_count = None
            self.__pad_launch_attempt_count = None
            self.__agency_launch_attempt_count = None
            self.__orbital_launch_attempt_count_year = None
            self.__location_launch_attempt_count_year = None
            self.__pad_launch_attempt_count_year = None
            self.__agency_launch_attempt_count_year = None
            self.__status_name = None
            self.__launch_service_provider_name = None
            self.__launch_service_provider_type = None
            self.__rocket_id = None
            self.__rocket_config_full_name = None
            self.__mission_name = None
            self.__mission_description = None
            self.__mission_type = None
            self.__mission_orbit_name = None
            self.__pad_wiki_url = None
            self.__pad_latitude = None
            self.__pad_longitude = None
            self.__pad_location_name = None
            self.__pad_location_country_code = None

    @property
    def name(self):
        return self.__name

    @property
    def net(self):
        return self.__net

    @property
    def window_end(self):
        return self.__window_end

    @property
    def window_start(self):
        return self.__window_start

    @property
    def fail_reason(self):
        return self.__fail_reason

    @property
    def image(self):
        return self.__image

    @property
    def infographic(self):
        return self.__infographic

    @property
    def orbital_launch_attempt_count(self):
        return self.__orbital_launch_attempt_count

    @property
    def location_launch_attempt_count(self):
        return self.__location_launch_attempt_count

    @property
    def pad_launch_attempt_count(self):
        return self.__pad_launch_attempt_count

    @property
    def agency_launch_attempt_count(self):
        return self.__agency_launch_attempt_count

    @property
    def orbital_launch_attempt_count_year(self):
        return self.__orbital_launch_attempt_count_year

    @property
    def location_launch_attempt_count_year(self):
        return self.__location_launch_attempt_count_year

    @property
    def pad_launch_attempt_count_year(self):
        return self.__pad_launch_attempt_count_year

    @property
    def agency_launch_attempt_count_year(self):
        return self.__agency_launch_attempt_count_year

    @property
    def launch_service_provider_name(self):
        return self.__launch_service_provider_name

    @property
    def status_name(self):
        return self.__status_name

    @property
    def launch_service_provider_type(self):
        return self.__launch_service_provider_type

    @property
    def rocket_id(self):
        return self.__rocket_id

    @property
    def rocket_config_full_name(self):
        return self.__rocket_config_full_name

    @property
    def mission_name(self):
        return self.__mission_name

    @property
    def mission_description(self):
        return self.__mission_description

    @property
    def mission_type(self):
        return self.__mission_type

    @property
    def mission_orbit_name(self):
        return self.__mission_orbit_name

    @property
    def pad_wiki_url(self):
        return self.__pad_wiki_url

    @property
    def pad_latitude(self):
        return self.__pad_latitude

    @property
    def pad_longitude(self):
        return self.__pad_longitude

    @property
    def pad_location_name(self):
        return self.__pad_location_name

    @property
    def pad_location_country_code(self):
        return self.__pad_location_country_code

    def __repr__(self):
        return f"\nEXTENDED LAUNCH INFO:\n" \
               f"Name: {self.__name}\nNet launch: {self.__net}\nWindow start: {self.__window_start}\nWindow end: {self.__window_end}\n" \
               f"Fail reason: {self.__fail_reason}\nImage url: {self.__image}\nInfographic url: {self.__infographic}\n" \
               f"All_time Orbital launch attempt count: {self.__orbital_launch_attempt_count}\n" \
               f"Current_year Orbital launch attempt count: {self.__orbital_launch_attempt_count_year}\n" \
               f"All_time Location launch attempt count: {self.__location_launch_attempt_count}\n" \
               f"Current_year Location launch attempt count: {self.__location_launch_attempt_count_year}\n" \
               f"All_time Pad launch attempt count: {self.__pad_launch_attempt_count}\n" \
               f"Current_year Pad launch attempt count: {self.__pad_launch_attempt_count_year}\n" \
               f"All_time Agency launch attempt count: {self.__agency_launch_attempt_count}\n" \
               f"Current_year Agency launch attempt count: {self.__agency_launch_attempt_count_year}\n" \
               f"Launch status: {self.__status_name}\nService provider name: {self.__launch_service_provider_name}\n" \
               f"Service provider type: {self.__launch_service_provider_type}\nRocket ID: {self.__rocket_id}\n" \
               f"Rocket name: {self.__rocket_config_full_name}\nMission name: {self.__mission_name}\n" \
               f"Mission description: {self.__mission_description}\nMission type: {self.__mission_type}\n" \
               f"Mission orbit: {self.__mission_orbit_name}\nPad wikipedia link: {self.__pad_wiki_url}\n" \
               f"Pad longitude: {self.__pad_longitude}\nPad latitude: {self.__pad_latitude}\n" \
               f"Pad location name: {self.__pad_location_name}\nPad location country code: {self.__pad_location_country_code}"

    @property
    def show_basic_info(self):
        return f"\nBASIC LAUNCH INFO:\n" \
               f"Name: {self.__name}\nNet launch: {self.__net}\nImage url: {self.__image}\n" \
               f"Launch status: {self.__status_name}\nService provider name: {self.__launch_service_provider_name}\n" \
               f"Rocket name: {self.__rocket_config_full_name}\nMission description: {self.__mission_description}\n" \
               f"Pad longitude: {self.__pad_longitude}\nPad latitude: {self.__pad_latitude}\n" \
               f"Pad location name: {self.__pad_location_name}\n"

    @property
    def jsonify(self):
        return {"name": self.__name, "net": self.__net, "window_start": self.__window_start,
                "window_end": self.__window_end, "failreason": self.__fail_reason, "image": self.__image,
                "infographic": self.__infographic,
                "orbital_launch_attempt_count": self.__orbital_launch_attempt_count,
                "orbital_launch_attempt_count_year": self.__orbital_launch_attempt_count_year,
                "location_launch_attempt_count": self.__location_launch_attempt_count,
                "location_launch_attempt_count_year": self.__location_launch_attempt_count_year,
                "pad_launch_attempt_count": self.__pad_launch_attempt_count,
                "pad_launch_attempt_count_year": self.__pad_launch_attempt_count_year,
                "agency_launch_attempt_count": self.__agency_launch_attempt_count,
                "agency_launch_attempt_count_year": self.__agency_launch_attempt_count_year,
                "status_name": self.__status_name,
                "launch_service_provider_name": self.__launch_service_provider_name,
                "launch_service_provider_type": self.__launch_service_provider_type, "rocket_id": self.__rocket_id,
                "rocket_configuration_full_name": self.__rocket_config_full_name,
                "mission_name": self.__mission_name, "mission_description": self.__mission_description,
                "mission_type": self.__mission_type, "mission_orbit_name": self.__mission_orbit_name,
                "pad_wiki_url": self.__pad_wiki_url, "pad_longitude": self.__pad_longitude,
                "pad_latitude": self.__pad_latitude, "pad_location_name": self.__pad_location_name,
                "pad_location_country_code": self.__pad_location_country_code}

    @name.setter
    def name(self, value):
        self.__name = value

    @net.setter
    def net(self, value):
        self.__net = value

    @window_end.setter
    def window_end(self, value):
        self.__window_end = value

    @window_start.setter
    def window_start(self, value):
        self.__window_start = value

    @fail_reason.setter
    def fail_reason(self, value):
        self.__fail_reason = value

    @image.setter
    def image(self, value):
        self.__image = value

    @infographic.setter
    def infographic(self, value):
        self.__infographic = value

    @orbital_launch_attempt_count.setter
    def orbital_launch_attempt_count(self, value):
        self.__orbital_launch_attempt_count = value

    @location_launch_attempt_count.setter
    def location_launch_attempt_count(self, value):
        self.__location_launch_attempt_count = value

    @pad_launch_attempt_count.setter
    def pad_launch_attempt_count(self, value):
        self.__pad_launch_attempt_count = value

    @agency_launch_attempt_count.setter
    def agency_launch_attempt_count(self, value):
        self.__agency_launch_attempt_count = value

    @orbital_launch_attempt_count_year.setter
    def orbital_launch_attempt_count_year(self, value):
        self.__orbital_launch_attempt_count_year = value

    @location_launch_attempt_count_year.setter
    def location_launch_attempt_count_year(self, value):
        self.__location_launch_attempt_count_year = value

    @pad_launch_attempt_count_year.setter
    def pad_launch_attempt_count_year(self, value):
        self.__pad_launch_attempt_count_year = value

    @agency_launch_attempt_count_year.setter
    def agency_launch_attempt_count_year(self, value):
        self.__agency_launch_attempt_count_year = value

    @launch_service_provider_name.setter
    def launch_service_provider_name(self, value):
        self.__launch_service_provider_name = value

    @status_name.setter
    def status_name(self, value):
        self.__status_name = value

    @launch_service_provider_type.setter
    def launch_service_provider_type(self, value):
        self.__launch_service_provider_type = value

    @rocket_id.setter
    def rocket_id(self, value):
        self.__rocket_id = value

    @rocket_config_full_name.setter
    def rocket_config_full_name(self, value):
        self.__rocket_config_full_name = value

    @mission_name.setter
    def mission_name(self, value):
        self.__mission_name = value

    @mission_description.setter
    def mission_description(self, value):
        self.__mission_description = value

    @mission_type.setter
    def mission_type(self, value):
        self.__mission_type = value

    @mission_orbit_name.setter
    def mission_orbit_name(self, value):
        self.__mission_orbit_name = value

    @pad_wiki_url.setter
    def pad_wiki_url(self, value):
        self.__pad_wiki_url = value

    @pad_latitude.setter
    def pad_latitude(self, value):
        self.__pad_latitude = value

    @pad_longitude.setter
    def pad_longitude(self, value):
        self.__pad_longitude = value

    @pad_location_name.setter
    def pad_location_name(self, value):
        self.__pad_location_name = value

    @pad_location_country_code.setter
    def pad_location_country_code(self, value):
        self.__pad_location_country_code = value





class Astronaut:
    def __init__(self, json: dict = None):
        if json is not None:
            self.__name = json['name']
            self.__date_of_birth = json['date_of_birth']
            self.__date_of_death = json['date_of_death']
            self.__nationality = json['nationality']
            self.__bio = json['bio']
            self.__twitter = json['twitter']
            self.__instagram = json['instagram']
            self.__wiki = json['wiki']
            self.__profile_image = json['profile_image']
            self.__profile_image_thumbnail = json['profile_image_thumbnail']
            self.__flights_count = json['flights_count']
            self.__landings_count = json['landings_count']
            self.__last_flight = json['last_flight']
            self.__first_flight = json['first_flight']
            self.__status_name = json['status_name']
            self.__type_name = json['type_name']
            self.__agency_name = json['agency_name']
            self.__agency_type = json['agency_type']
            self.__agency_country_code = json['agency_country_code']
            self.__agency_abbrev = json['agency_abbrev']
            self.__agency_logo_url = json['agency_logo_url']
        else:
            self.__name = None
            self.__date_of_birth = None
            self.__date_of_death = None
            self.__nationality = None
            self.__bio = None
            self.__twitter = None
            self.__instagram = None
            self.__wiki = None
            self.__profile_image = None
            self.__profile_image_thumbnail = None
            self.__flights_count = None
            self.__landings_count = None
            self.__last_flight = None
            self.__first_flight = None
            self.__status_name = None
            self.__type_name = None
            self.__agency_name = None
            self.__agency_type = None
            self.__agency_country_code = None
            self.__agency_abbrev = None
            self.__agency_logo_url = None

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        today = date.today()
        try:
            return today.year - datetime.strptime(self.__date_of_birth, '%Y-%m-%d').year - ((today.month, today.day) < (
                datetime.strptime(self.__date_of_birth, '%Y-%m-%d').month,
                datetime.strptime(self.__date_of_birth, '%Y-%m-%d').day))
        except (ValueError, TypeError):
            return "The birth date was not found."

    @property
    def birth_date(self):
        return self.__date_of_birth

    @property
    def death_date(self):
        return self.__date_of_death

    @property
    def age_of_death(self):
        if self.death_date == "" or self.death_date is None:
            return "Still Alive!!"
        else:
            death = datetime.strptime(self.__date_of_death, '%Y-%m-%d')
            return death.year - datetime.strptime(self.__date_of_birth, '%Y-%m-%d').year - ((death.month, death.day) < (
                datetime.strptime(self.__date_of_birth, '%Y-%m-%d').month,
                datetime.strptime(self.__date_of_birth, '%Y-%m-%d').day))

    @property
    def nationality(self):
        return self.__nationality

    @property
    def bio(self):
        return self.__bio

    @property
    def twitter(self):
        return self.__twitter

    @property
    def instagram(self):
        return self.__instagram

    @property
    def wiki(self):
        return self.__wiki

    @property
    def profile_image(self):
        return self.__profile_image

    @property
    def profile_image_thumbnail(self):
        return self.__profile_image_thumbnail

    @property
    def flights_count(self):
        return self.__flights_count

    @property
    def landings_count(self):
        return self.__landings_count

    @property
    def last_flight(self):
        return self.__last_flight

    @property
    def first_flight(self):
        return self.__first_flight

    @property
    def status_name(self):
        return self.__status_name

    @property
    def type_name(self):
        return self.__type_name

    @property
    def agency_name(self):
        return self.__agency_name

    @property
    def agency_type(self):
        return self.__agency_type

    @property
    def agency_country_code(self):
        return self.__agency_country_code

    @property
    def agency_abbrev(self):
        return self.__agency_abbrev

    @property
    def agency_logo_url(self):
        return self.__agency_logo_url

    def __repr__(self):
        return f"\nEXTENDED ASTRONAUT INFO:\n" \
               f"Name: {self.__name}\nAge: {self.age}\nBirth Date: {self.__date_of_birth}\nDeath Date: {self.__date_of_death}\n" \
               f"Nationality: {self.__nationality}\nDescription: {self.__bio}\nTwitter link: {self.__twitter}\n" \
               f"Instagram link: {self.__instagram}\nWikipedia page: {self.__wiki}\nProfile image link: {self.__profile_image}\n" \
               f"Profile image thumbnail link: {self.__profile_image_thumbnail}\nFlights count: {self.__flights_count}\n" \
               f"Landings count: {self.__landings_count}\nLast flight: {self.__last_flight}\nFirst flight: {self.__first_flight}\n" \
               f"Status: {self.__status_name}\nEnrollment type: {self.__type_name}\nAgency Name: {self.__agency_name}\n" \
               f"Agency type: {self.__agency_type}\nAgency participating Counties: {self.__agency_country_code}\n" \
               f"Agency acronym: {self.__agency_abbrev}\nAgency logo link: {self.__agency_logo_url}"

    @property
    def show_basic_info(self):
        return f"\nBASIC ASTRONAUT INFO:\n" \
               f"Name: {self.__name}\nAge: {self.age}\nBirth Date: {self.__date_of_birth}\nDeath Date: {self.__date_of_death}\n" \
               f"Nationality: {self.__nationality}\nDescription: {self.__bio}\nProfile image link: {self.__profile_image}\n" \
               f"Flights count: {self.__flights_count}\n" \
               f"Landings count: {self.__landings_count}\nLast flight: {self.__last_flight}\n" \
               f"Agency acronym: {self.__agency_abbrev}"

    @property
    def jsonify(self):
        return {"name": self.__name, "date_of_birth": self.__date_of_birth, "date_of_death": self.__date_of_death,
                "nationality": self.__nationality,
                "bio": self.__bio,
                "twitter": self.__twitter, "instagram": self.__instagram, "wiki": self.__wiki,
                "profile_image": self.__profile_image,
                "profile_image_thumbnail": self.__profile_image_thumbnail,
                "flights_count": self.__flights_count, "landings_count": self.__landings_count,
                "last_flight": self.__last_flight,
                "first_flight": self.__first_flight, "status.name": self.__status_name, "type_name": self.__type_name,
                "agency_name": self.__agency_name, "agency_type": self.__agency_type,
                "agency_country_code": self.__agency_country_code, "agency_abbrev": self.__agency_abbrev,
                "agency_logo_url": self.__agency_logo_url}

    @name.setter
    def name(self, value):
        self.__name = value

    @birth_date.setter
    def birth_date(self, value):
        self.__date_of_birth = value

    @death_date.setter
    def death_date(self, value):
        self.__date_of_death = value

    @nationality.setter
    def nationality(self, value):
        self.__nationality = value

    @bio.setter
    def bio(self, value):
        self.__bio = value

    @twitter.setter
    def twitter(self, value):
        self.__twitter = value

    @instagram.setter
    def instagram(self, value):
        self.__instagram = value

    @wiki.setter
    def wiki(self, value):
        self.__wiki = value

    @profile_image.setter
    def profile_image(self, value):
        self.__profile_image = value

    @profile_image_thumbnail.setter
    def profile_image_thumbnail(self, value):
        self.__profile_image_thumbnail = value

    @flights_count.setter
    def flights_count(self, value):
        self.__flights_count = value

    @landings_count.setter
    def landings_count(self, value):
        self.__landings_count = value

    @last_flight.setter
    def last_flight(self, value):
        self.__last_flight = value

    @first_flight.setter
    def first_flight(self, value):
        self.__first_flight = value

    @status_name.setter
    def status_name(self, value):
        self.__status_name = value

    @type_name.setter
    def type_name(self, value):
        self.__type_name = value

    @agency_name.setter
    def agency_name(self, value):
        self.__agency_name = value

    @agency_type.setter
    def agency_type(self, value):
        self.__agency_type = value

    @agency_country_code.setter
    def agency_country_code(self, value):
        self.__agency_country_code = value

    @agency_abbrev.setter
    def agency_abbrev(self, value):
        self.__agency_abbrev = value

    @agency_logo_url.setter
    def agency_logo_url(self, value):
        self.__agency_logo_url = value
