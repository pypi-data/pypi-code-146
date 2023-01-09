from math import sin, cos, sqrt, atan2, radians


##################################
# month diff calculation
##################################

def month_diff(date_a, date_b):
    """
    This function returns month difference between calendar dates 'date_a' and 'date_b'
    """
    return 12 * (date_a.dt.year - date_b.dt.year) + (date_a.dt.month - date_b.dt.month)


# Pass cleaner tuple (string format) into SQL query
# Handles single item tuple

def sql_tuple(a_tuple):
    """
    This function converts a tuple into a parasable string format for SQL query purpose
    For example - (1,) a single item tuple will be converted to (1), But if tuple is (1,2) then will remain as (1,2)
    """
    if len(a_tuple) == 1:
        return '({})'.format(a_tuple[0])
    return str(a_tuple)


def nearest_store(store_id, data, lat_lon_col_name=['latitude', 'longitude'], from_distance=5, ):
    """
    helper function to get the nearby stores
    """
    """ filtering out the nan values """

    R = 6378.1  # radius of earth in KM
    print(f"nearest_store calculation started for store id: {store_id}")
    data['lat_r'] = data[lat_lon_col_name[0]].apply(lambda x: radians(float(x)))
    data['lon_r'] = data[lat_lon_col_name[1]].apply(lambda x: radians(float(x)))

    lat1 = data[data['store_id'] == store_id]['lat_r'].values[0]
    lon1 = data[data['store_id'] == store_id]['lon_r'].values[0]

    data['lat1'] = lat1
    data['lon1'] = lon1

    data['dlon'] = data['lon_r'] - data['lon1']
    data['dlat'] = data['lat_r'] - data['lat1']

    data['a'] = data.apply(
        lambda x: sin(x['dlat'] / 2) ** 2 + cos(x['lat1']) * cos(x['lat_r']) * sin(x['dlon'] / 2) ** 2, 1)
    data['c'] = data.apply(lambda x: 2 * atan2(sqrt(x['a']), sqrt(1 - x['a'])), 1)

    data['distance'] = R * data['c']

    near_stores = data[data['distance'] <= from_distance].sort_values('distance')['store_id'].values
    data.drop(columns=['lat_r', 'lon_r', 'lat1', 'lon1', 'dlon', 'dlat', 'a', 'c', 'distance'], inplace=True)

    return near_stores


# Change HH:MM:SS to seconds
def hms_to_seconds(t):
    """
    This function converts HH:MM:SS (for example 02:23:18 (2hrs, 23minutes, 18seconds)
    # into total seconds value, which is 8598 in this)
    """
    split_t = [int(i) for i in t.split(':')]
    if len(split_t) == 3:
        h, m, s = split_t
        return 3600 * h + 60 * m + s
    elif len(split_t) == 2:
        m, s = split_t
        return 60 * m + s
    else:
        s = split_t[0]
        return s
