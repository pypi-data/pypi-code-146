"""
Name: Oliver Gaither
Date: Jan 9, 2023
Description: provide functions for easily generated
names, cities and other useful placeholders
to be used as dummy data for testing code and
potentially building systems
"""
import random as rand
import os

from .lists import SURNAMES, FEMALE_NAMES, MALE_NAMES, COUNTRIES, random_numbers, CITIES, COUNTRY_ISOS, \
    COUNTRIES_WITH_CITY_DATA

__version__ = "4.0.0"
__SURNAMES_FILE = os.path.join(os.path.dirname(__file__), "./surnames.txt")
__FEMALE_NAMES_FILE = os.path.join(os.path.dirname(__file__), "./female-first-names.txt")
__MALE_NAMES_FILE = os.path.join(os.path.dirname(__file__), "./male-first-names.txt")
__COUNTRIES_FILE = os.path.join(os.path.dirname(__file__), "./countries.txt")
__WORLDCITIESCSV = os.path.join(os.path.dirname(__file__), "./world_cities.csv")


def __load_file(filename):
    f = open(filename)
    n = list(map(str.rstrip, f.readlines()))
    f.close()
    return n


# names data

def random_name(sex=None, reversed=False):
    """
    return a random full name,
    if sex is specified then the first name will be of that sex,
    otherwise it could be either a male or female name
    :param sex: optional sex indicator (1 for female, 0 for male)
    :param reversed: boolean of the format of the name
    True for Last, First or False for First Last
    :return: full name string
    """
    if sex is not None and sex not in (0, 1):
        raise ValueError("random_name(): sex argument is invalid, must be None, 1, or 0")
    if sex is None:
        names = FEMALE_NAMES + MALE_NAMES
    else:
        names = FEMALE_NAMES if (sex == 1) else MALE_NAMES
    fn = rand.choice(names)
    ln = rand.choice(SURNAMES)
    if reversed:
        name = "%s, %s" % (ln, fn)
    else:
        name = "%s %s" % (fn, ln)
    return name


def random_names(n=10, sex=None, reversed=False):
    """
    return an iterator of n random full names,
    if sex is specified all names will be of that sex,
    otherwise they will be a mix of male and female
    :param n: number of names to generator
    :param sex: optional sex indicator (1 for female, 0 for male)
    :return: iterator object of random name
    """
    
    return iter(random_name(sex, reversed) for _ in range(n))


def names_by_prefix(__prefix, n=None, sex=None, full=False):
    """
    return an iterator of all names that start with a given prefix,
    by default will return just given names but can optional generate full
    names
    :param __prefix: prefix
    :param n: number of names to generate, default = None (all names)
    :param sex: sex of names to generate, default = None (both)
    :param full: optional, whether to generate full names for the names
    :return: iterator of names
    """
    if (sex is not None) and (sex not in (0, 1)):
        raise ValueError("names_by_prefix(): sex argument is invalid, must be None, 1, or 0")
    if sex is None:
        names = FEMALE_NAMES + MALE_NAMES
    else:
        names = FEMALE_NAMES if (sex == 1) else MALE_NAMES
    
    # ensure safe slicing
    if n == None or n > len(names):
        n = len(names)
    # filter out all names that don't start with prefix
    names = list(filter(lambda x: (x.lower()).startswith(__prefix.lower()), names))
    names = names[:n]
    if full:
        names = map(lambda x: f"{x} {rand.choice(SURNAMES)}", names)
    return names


# cities data
__NAMEKEY = "name"
__LATKEY = "latitude"
__LNGKEY = "longitude"
__COUNTRYKEY = "country"
__ISO3KEY = "iso3"
__POPULATIONKEY = "population"
__AVERAGE_POPULATION = 111770  # average population of cities in dataset


def random_country(iso=False):
    """
    return string of a country in the world
    :param iso: whether to return country string in iso3 format
    :return: string of country name
    """
    if not iso:
        return rand.choice(COUNTRIES)
    else:
        return rand.choice(COUNTRY_ISOS)


def random_countries(n=None, iso=False):
    """
    return a iterator of n strings of countries in the world
    :param n: number of country, default = None (all)
    :param iso: whether to return country string in iso3 format
    :return: iterator of countries
    """
    if n is None:
        n = len(COUNTRIES) if (not iso) else len(COUNTRY_ISOS)
    return iter(random_country(iso) for _ in range(n))


def random_city(country=None, populus=False, returnobj=False):
    """
    return a random city from a collection of ~37k
    :param country: optional country specifier to only get cities from a single country
    :param populus: optional populus specifer, if marked will only
    choose from cities with higher than the average population of the data set
    :param returnobj: optional object return, if marked it will return a dictionary object
    of the city data, otherwise, it will just return ascii name of city
    :return: string or dictionary object of city
    """
    cities = CITIES
    if country:
        if country not in COUNTRIES_WITH_CITY_DATA: raise ValueError(
            "random_city(): invalid country string or does not have city data")
        cities = filter(lambda x: CITIES[x][__COUNTRYKEY].lower() == country.lower(), cities)
    if populus:
        cities = filter(lambda x: CITIES[x][__POPULATIONKEY] > __AVERAGE_POPULATION, cities)
    
    city = rand.choice(list(cities))
    
    return CITIES[city] if returnobj else city


def random_cities(n=10, country=None, populus=False, returnobj=False):
    """
    return n random cities from a collection of ~37k cities
    :param n: number of random cities, default = 10
    :param country: optional country specifier to only get cities from a single country
    :param populus: optional populus specifer, if marked will only
    choose from cities with higher than the average population of the data set
    :param returnobj: optional object return, if marked it will return a dictionary object
    of the city data, otherwise, it will just return ascii name of city
    :return: iterator of cities
    """
    # TODO: overhaul function so that no city is repeated in final iterable
    if n > len(CITIES):
        n = len(CITIES)
    return iter(random_city(country, populus, returnobj) for _ in range(n))


def generate_number(area_code=None, country_code=None):
    """
    generates a random phone number esque string
    :param area_code: optional area code, default = None, randomly generated
    :param country_code: optional country code, default = +1
    :return:
    """
    NXX = str(rand.randint(2, 9)) + str(rand.randint(00, 99))
    XXXX = str(rand.randint(0000, 9999))
    
    out = "-" + NXX + "-" + XXXX
    
    if area_code is None:
        NPA = str(rand.randint(201, 999))
        
        phone = "(%s)" % NPA + out
    else:
        phone = f"({str(area_code)})" + out
    
    if country_code:
        phone = f"+{country_code} " + phone
    else:
        phone = "+1 " + phone
    
    return phone


def generate_email(fullname):
    """
    returns a string of a generated email
    for a user based on a passed full name
    :param fullname: string of a first and last name, will break if not
    :return: an email
    """
    # 3 formats
    # first initial full last name
    # full first name, first inital of last name
    # full first and last
    user_format = rand.choice(['fi last', 'first li', 'first last'])
    if user_format == 'fi last':
        user = (fullname.split()[0][0] + fullname.split()[1]).lower()
    elif user_format == 'first li':
        user = (fullname.split()[0] + fullname.split()[1][0]).lower()
    else:
        user = (fullname.split()[0] + fullname.split()[1]).lower()
    
    domain = "@" + rand.choice(['foo', 'bar', 'baz', 'qux']) + rand.choice(['.com', '.net', '.org'])
    
    return user + domain


import json


class Person(object):
    """
    A person API uses the functions of this package
    """
    
    def __init__(self, sex: str = None):
        """
        Initializes a new Person object, for now it only will generate
        a person from the United States. update coming pending creation of
        Country and country code lookup table
        :param sex: sex of person to be generated, default = None
        """
        self.name = random_name(sex)
        self.country = "United States"
        self.city = random_city(self.country, returnobj=True)
        self.email = generate_email(self.name)
        self.phone = generate_number()
    
    def json(self):
        """
        returns a Json Object of the generated
        Person object as an alternative to manually working
        with the Python object
        :return: JSON Object
        """
        response = json.dumps({
            'name': self.name,
            'location': self.city,
            'email': self.email,
            'phone': self.phone
        })
        
        return json.loads(response)
    
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError("Types do not match")
        return (self.name == other.name) and (self.email == other.email) and (self.city == other.city)

