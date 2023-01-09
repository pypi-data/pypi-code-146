import numpy as np
import geopandas as gpd    
from shapely.geometry import Point    
from shapely import geometry, ops


def deduplicate_concatenate_duns(duns, *args):
    """ this function deduplicates the duns dataset based on organization id + postcode and concatenates values in rows before deduplication"""

    # create key for deduplication using organization ID and postal code
    duns['deduplicate'] = duns.apply(lambda x: str(x['Organization ID']) + str(x['Postal Code']), axis=1)
    duns['deduplicate'] = duns['deduplicate'].apply(lambda x: ''.join(x.replace('nan', '').replace('.0', '').split()))

    # for each variable mentioned, create a cc_dd (concatenate values to retain information)
    for variable in args:
        new_variable_name = '_'.join(variable.split()) + '_cc_dd'    
        duns[new_variable_name] = duns[variable].astype(str)
        duns[new_variable_name] = duns.groupby(['deduplicate'])[new_variable_name].transform(lambda x: ' / '.join(x))
        duns[new_variable_name] = duns[new_variable_name].apply(lambda x: [item for item in list(set(x.split(' / '))) if item != 'nan'])
        duns[new_variable_name] = duns[new_variable_name].apply(lambda x: ', '.join(x))
        duns[new_variable_name] = duns[new_variable_name].replace(r'^\s*$', np.nan, regex=True) 

    # sort based on employees on entity
    duns = duns.sort_values(['deduplicate', '# employees on entity'], ascending=[True, False])        

    # drop duplicates
    duns = duns.drop_duplicates(subset=['deduplicate'], keep='first')     

    # change columns order
    column_order = []
    for col in duns.columns:
        if '_cc_dd' not in col:
            column_order.append(col)
            if '_'.join(col.split()) + '_cc_dd' in duns:
                column_order.append('_'.join(col.split()) + '_cc_dd')
    duns = duns[column_order] 

    return duns


def distance_to_line(lat, lon, line):
    """ this function calculates the perpendicular disance of a point to a line (KMZ file) """
    
    # calculate distance; https://stackoverflow.com/questions/69851086/calculate-distance-between-linestring-and-point-in-meters
    gdfl = gpd.GeoDataFrame(geometry=[line], crs="EPSG:4326")
    gdfp = gpd.GeoDataFrame(geometry=[Point(lon, lat)], crs="EPSG:4326")
    utm = gdfl.estimate_utm_crs()
    distance = gdfl.to_crs(utm).distance(gdfp.to_crs(utm)).iloc[0]

    return distance


def distance_to_network(lat, lon, network_kmz):
    """ this function calculates the perpendicular disance of a point to the network that is created by concatenating individual lines (KMZ file) """

    all_network = network_kmz['geometry_object'].tolist()
    multi_line = geometry.MultiLineString(all_network)

    # calculate distance; https://stackoverflow.com/questions/69851086/calculate-distance-between-linestring-and-point-in-meters
    gdfl = gpd.GeoDataFrame(geometry=[multi_line], crs="EPSG:4326")
    gdfp = gpd.GeoDataFrame(geometry=[Point(lon, lat)], crs="EPSG:4326")
    utm = gdfl.estimate_utm_crs()
    distance = gdfl.to_crs(utm).distance(gdfp.to_crs(utm)).iloc[0]

    return distance


def check_if_in_business_parc_optimized(lat, lon, province, ibis, increase_search_space=False):
    """ this function checks if a certain Point(lat, lon) is in a business parc polygon taking into account county for optimization"""

    # remove records without polygons 
    ibis = ibis.dropna(subset='geometry').reset_index(drop=True)

    # IMPORTANT: change coordinate reference sytem (https://stackoverflow.com/questions/47203938/convert-the-coordinates-of-a-shapefile-in-geopandas)
    ibis['geometry'] = ibis['geometry'].to_crs(epsg=4326)

    # clean ibis provinces
    ibis['PROV_NAMEN'] = ibis['PROV_NAMEN'].apply(lambda x: x.upper().strip() if x not in [np.nan] else np.nan)

    try:
        # make a specific subset of the ibis data based on the province    
        ibis_select = ibis[ibis['PROV_NAMEN']==province.upper().strip()].reset_index(drop=True)
        # make a specific subset of the ibis data without the province for search space increase if required
        ibis_non_select = ibis[~(ibis['PROV_NAMEN']==province.upper().strip())].reset_index(drop=True)
        # helper variable
        temp_val = 0

        # iterate over selected business parc and return rin number if intersect
        for index, bp in ibis_select.iterrows():
            if bp['geometry'].contains(Point(lon, lat)) == True: # contains function works only properly with (lon, lat)
                temp_val = 1
                return bp['RIN_NUMMER']

        # increase search space when no intersection on province selection
        if increase_search_space == True:
            if temp_val == 0:
                # iterate over selected business parc and return rin number if intersect
                for index, bp in ibis_non_select.iterrows():
                    if bp['geometry'].contains(Point(lon, lat)) == True: # contains function works only properly with (lon, lat)
                        return bp['RIN_NUMMER']   

    except:
        # in case no province use the entire search space
        for index, bp in ibis.iterrows():
            if bp['geometry'].contains(Point(lon, lat)) == True: # contains function works only properly with (lon, lat)
                return bp['RIN_NUMMER']


def check_if_in_business_parc(lat, lon, ibis):
    """ this function checks if a certain Point(lat, lon) is in a business parc polygon """

    # from shapely.geometry import Point 

    # remove records without polygons 
    ibis = ibis.dropna(subset='geometry').reset_index(drop=True)

    # change coordinate reference sytem (https://stackoverflow.com/questions/47203938/convert-the-coordinates-of-a-shapefile-in-geopandas)
    ibis['geometry'] = ibis['geometry'].to_crs(epsg=4326)

    # iterate over business parcs and return rin_number
    for index, bp in ibis.iterrows():
        if bp['geometry'].contains(Point(lon, lat)) == True: # contains function works only properly with (lon, lat)
            return bp['RIN_NUMMER']


def within_range(lat, lon, kmz, buffer_range):
    # kmz = gpd.GeoDataFrame(kmz, crs='epsg:4326')
    kmz = kmz.to_crs({'init': 'epsg:28992'}) # or 3763 https://epsg.io/?q=netherlands
    kmz['geometry'] = kmz['geometry'].buffer(buffer_range)
    kmz = kmz.to_crs({'init': 'epsg:4326'})

    for item in kmz['geometry']:
        if item.contains(Point(lon, lat)) == True: # contains function works only properly with (lon, lat)
            return True     