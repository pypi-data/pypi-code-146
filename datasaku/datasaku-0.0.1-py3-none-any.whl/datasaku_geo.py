"""geo related module"""

#############################
###### import packages ######
#############################

import h3
import pandas as pd
import geopandas as gpd
import fiona

##############################
###### set the settings ######
##############################

fiona.drvsupport.supported_drivers['libkml'] = 'rw' # enable KML support which is disabled by default
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw' # enable KML support which is disabled by default
fiona.drvsupport.supported_drivers['kml'] = 'rw' # enable KML support which is disabled by default
fiona.drvsupport.supported_drivers['KML'] = 'rw' # enable KML support which is disabled by default

###########################
###### initial value ######
###########################

projections = {'argentina': 5343
                , 'chile': 5361
                , 'colombia': 6244
                , 'mexico': 6372
                , 'peru': 5387
                }

class Geo:
    """Class for geo country"""
    def __init__(self, country_var_def):
        """initiate the class"""
        self.country = country_var_def
        self.projection_default = 4326
        self.projection_meter = projections[country_var_def]

    def geo_read(self, file_path_var_def):
        """read shape file"""
        geo = gpd.read_file(file_path_var_def)
        geo_default = geo.to_crs(self.projection_default)
        return geo_default

    def geo_write(self, geo_file_def, file_path_var_def, file_type_var_def = 'shp'):
        """
        write geo file
        possible value for file_type_var_def are shp, kml, csv, parquet
        """
        if file_type_var_def == 'shp':
            geo_file_def.to_file(driver = 'ESRI Shapefile', filename = file_path_var_def)
        elif file_type_var_def == 'kml':
            geo_file_def.to_file(driver='kml', filename = file_path_var_def)
        elif file_type_var_def == 'csv':
            geo_file_def.to_csv(file_path_var_def, index=False)
        elif file_type_var_def == 'parquet':
            geo_file_def.to_csv(file_path_var_def, index=False)

    def geo_change_projection(self, geo_file_def, projection_var_def = 'degree'):
        """change projection of the map"""
        if projection_var_def == 'degree':
            projection_def = self.projection_default
        elif projection_var_def == 'meter':
            projection_def = self.projection_meter
        geo_file = geo_file_def.to_crs(projection_def)
        return geo_file

    def geo_calculate_area(self, geo_file_def):
        """calculate area in m2"""
        geo_file = geo_file_def.to_crs(self.projection_meter)
        geo_file['area'] = geo_file.area
        return geo_file

    def geo_buffer(self, geo_file_def, buffer_in_meter_var_def):
        """make buffer with 6 precision"""
        geo_file = geo_file_def.to_crs(self.projection_meter)
        geo_file.geometry = geo_file.geometry.buffer(buffer_in_meter_var_def, 6)
        return geo_file

    def geo_pandas_join_shortestdistance(self, geo_df_def_1, lat_col_def_1, lon_col_def_1, geo_df_def_2, lat_col_def_2, lon_col_def_2):
        """
        Spatial join from two geopandas dataframe with the shortest distance between them.  
        The column will not be filtered out and there will be additional **distance** information that will be in meters.
        - geo_df_def_1 = the first geopandas dataframe
        - lat_col_def_1 = latitude column for the first geopandas dataframe
        - lon_col_def_1 = longitude column for the first geopandas dataframe
        - geo_df_def_2 = the second geopandas dataframe
        - lat_col_def_2 = latitude column for the second geopandas dataframe
        - lon_col_def_2 = longitude column for the second geopandas dataframe
        """
        geo_df_def_1 = gpd.GeoDataFrame(geo_df_def_1
                                            , geometry = gpd.points_from_xy(geo_df_def_1[lon_col_def_1], geo_df_def_1[lat_col_def_1])
                                            ) # make the first dataset as geopandas
        try:
            geo_df_1 = geo_df_def_1.to_crs(self.projection_default) # change the crs to default
            geo_df_1 = geo_df_def_1.to_crs(self.projection_meter) # change the crs to meters
        except ValueError:
            geo_df_1 = geo_df_def_1 # copy to the new dataframe
            geo_df_1.crs = "EPSG:" + str(self.projection_default) # set the crs to default
            geo_df_1 = geo_df_def_1.to_crs(self.projection_meter) # change the crs to meters
        geo_df_def_2 = gpd.GeoDataFrame(geo_df_def_2
                                            , geometry = gpd.points_from_xy(geo_df_def_2[lon_col_def_2], geo_df_def_2[lat_col_def_2])
                                            ) # make the second dataset as geopandas
        try:
            geo_df_2 = geo_df_def_2.to_crs(self.projection_default) # change the crs to default
            geo_df_2 = geo_df_def_2.to_crs(self.projection_meter) # change the crs to meters
        except ValueError:
            geo_df_2 = geo_df_def_2
            geo_df_2.crs = "EPSG:" + str(self.projection_default)
            geo_df_2 = geo_df_def_2.to_crs(self.projection_meter)
        geo_df_merge = geo_df_1.sjoin_nearest(geo_df_2, distance_col = "distances")
        return geo_df_merge
