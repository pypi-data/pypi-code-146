import csv, random
import pkg_resources

# initializing path to csv file
file_path = pkg_resources.resource_filename('rcoc', 'cities.csv')

def read_data() -> list:
    '''Reads "cities.csv" file and returns random [city, country] entity as list
    Used by:
        1. get_random_location()
        2. get_random_country()
        3. get_random_city()
    '''
    with open(file_path) as data:
        reader = csv.reader(data)
        location = random.choice(list(reader))
        data.close()
        return location

def get_random_location() -> str:
    '''Calls read_data() to get random row from csv file
    returns random "city, location" as string
    '''
    location = read_data()
    return "{0}, {1}".format(location[0], location[1])

def get_random_country() -> str:
    '''Calls read_data() to get random row from csv file
    returns random country as string
    '''
    location = read_data()
    return location[1]

def get_random_city() -> str:
    '''Calls read_data() to get random row from csv file
    returns random city as string
    '''
    location = read_data()
    return location[0]

def get_random_city_by_country(country: str) -> str:
    '''Takes country name as argument
    Reads "cities.csv" file, filters records where country equals to argument
    returns random city from specified countrty as a string

    if specified country not found returns empty string
    '''
    data = open(file_path)
    reader = csv.reader(data)
    filtered = filter(lambda p: country.title() == p[1], reader)
    try:
        res = random.choice(list(filtered))[0]
        data.close()
        return res
    except IndexError:
        data.close()
        return ""

def get_all_countries():
    '''Returns list of all countries from CSV file as a list
    '''
    all_countries = []
    with open(file_path) as data:
        reader = csv.reader(data)

        # getting all unique values
        for country in list(reader):
            if country[1] not in all_countries:
                all_countries.append(country[1])

        data.close()
    return all_countries[1:]

