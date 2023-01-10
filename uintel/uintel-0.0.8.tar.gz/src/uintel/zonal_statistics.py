"""
Calculate statistics of raster files over a polygon geometry ("zonal statistics")
"""

__all__ = ["calculate_zonal_statistics"]

import geopandas as gpd, os, numpy as np, rasterio as rio, warnings, tqdm
from osgeo import ogr, gdal, osr

def _boundingBoxToOffsets(vector_bbox, raster_geotransform):
    col1 = int((vector_bbox[0] - raster_geotransform[0]) / raster_geotransform[1])
    col2 = int((vector_bbox[1] - raster_geotransform[0]) / raster_geotransform[1]) + 1
    row1 = int((vector_bbox[3] - raster_geotransform[3]) / raster_geotransform[5])
    row2 = int((vector_bbox[2] - raster_geotransform[3]) / raster_geotransform[5]) + 1
    return [row1, row2, col1, col2]


def _geotFromOffsets(row_offset, col_offset, raster_geotransform):
    return [raster_geotransform[0] + (col_offset * raster_geotransform[1]), raster_geotransform[1], 0.0, raster_geotransform[3] + (row_offset * raster_geotransform[5]), 0.0, raster_geotransform[5]]


def _check_inputted_datasets(raster_path, vector_path):
    """
    Run compatibility checks to ensure:
        - Files exist
        - Vector file only contains Polygons
        - Geographic projections match
    """
    # Do some checks to make sure the vector file input is okay
    if type(vector_path) == gpd.GeoDataFrame:
        if not os.path.exists("shp-tmp"):
            os.makedirs("shp-tmp")
        vector_path.to_file("shp-tmp/vector_file.shp")
        vector_path = os.path.join(os.getcwd(), "shp-tmp", "vector_file.shp")
    elif type(vector_path) != str:
        raise TypeError(f"The vector file must be either a string of the filepath to the shape OR a GeoDataFrame. A {type(vector_path)} is not acceptable.")

    try:
        vector_file = gpd.read_file(vector_path)
    except Exception as e:
        raise e

    geom_types = vector_file.geom_type.unique()
    if len(geom_types) != 1:
        raise TypeError(f"The vector file: {vector_path} can only contain Polygon geometries, but it contains {geom_types}. Please correct this before running again.")
    if geom_types[0] != 'Polygon':
        raise TypeError(f"The vector file: {vector_path} can only contain Polygon geometries, but it contains {geom_types}. Please correct this before running again.")
    vector_epsg = vector_file.crs.to_epsg()
    del vector_file

    # Do some checks to make sure the raster file input is okay
    if type(raster_path) != str:
        raise TypeError(f"The raster file must be a string of the filepath to the raster. A {type(vector_path)} is not acceptable.")
    try:
        raster_epsg = rio.open(raster_path).crs.to_epsg()
        if rio.open(raster_path).crs.to_epsg() == None:
            raster_epsg = 2193
    except Exception as e:
        raise e


    # Check to see if the projections match
    if vector_epsg != raster_epsg:
        if type(raster_epsg) in (int, float):
            warnings.warn(f"The two inputted datasets are in different projections (raster: {raster_epsg}; vector: {vector_epsg}). An attempt will be made to reproject the vector layer into the projection of the raster. This will change the vector file saved at {vector_path} to EPSG:{raster_epsg}.")
            try:
                _ = gpd.read_file(vector_path).to_crs(raster_epsg).to_file(vector_path)
            except:
                raise TypeError(f"The automatic attempt at changing projections failed. Please correct this before running again.")
        else:
            raise TypeError(f"The two inputted datasets are in different projections (raster: {raster_epsg}; vector: {vector_epsg}). Please correct this before running again.")

    return raster_epsg


def _get_raster_array(raster_dataset, offsets, raster_x_size, raster_y_size, raster_band, raster_nodata):
    """
    Checks to see if the vector offset geometry lies within the raster dataset, and if so, returns the values from the raster_dataset. If only a proportion of the geometries overlap, then the other pixel values are given the raster_nodata value.
    """

    # Grab the "normal" parameters to pass to ReadAsArray  
    y_top, y_bottom, x_left, x_right = offsets         
    width, height = x_right-x_left, y_bottom-y_top
   
    if width == 0 or height == 0:
        # The  the requested raster has a zero dimension which is invalid
        return None
    if x_left > raster_x_size or y_top > raster_y_size:
        # Then the starting point (top left of the polygon) is outside of the bottom right raster extent
        return None
    elif x_right < 0 or y_bottom < 0:
        # Then the finishing point (bottom right of the polygon) is outside of the top left raster extent
        return None
    elif x_left >= 0 and x_right <= raster_x_size and y_top >= 0 and y_bottom <= raster_y_size and width >= 0 and height >= 0:
        # Then the whole vector geometry is within the raster
        return raster_dataset.GetRasterBand(raster_band).ReadAsArray(x_left, y_top, width, height)    
    elif (x_left < 0 or y_top < 0) and x_right > 0 and y_bottom > 0:
        # Then the starting point (top left of the polygon) is outside of the raster extent
        # Only some of the vector geometry is within the raster extent so create a full no-data array and overwrite values that exist
        raster = np.full((height, width), raster_nodata)
        
        x_offset, y_offset = 0, 0
        # Adjust the height and widths to be in the bounds of the raster
        if x_left < 0:
            x_offset = -x_left # Move everything left to make x_left = 0
            width -= x_offset  # sum negative number will reduce the width 
            x_left = 0
        if y_top < 0:
            y_offset = -y_top # Move everything down to make y_top =0 
            height -= y_offset  # sum negative number will reduce the width
            y_top = 0
        if x_right > raster_x_size:
            width -= (x_right - raster_x_size) # subtract how much over the boundary
            x_right = raster_x_size
        if y_bottom > raster_y_size:
            height -= (y_bottom - raster_y_size) # subtract how much over the boundary
            y_bottom = raster_y_size
        raster[y_offset:y_offset+height, x_offset:x_offset+width] = raster_dataset.GetRasterBand(raster_band).ReadAsArray(x_left, y_top, width, height)
        return raster
    elif x_left >= 0 and x_left < raster_x_size and y_top >= 0 and y_top < raster_y_size and (x_right > raster_x_size or y_bottom > raster_y_size):
        # Only some of the vector geometry is within the raster extent so create a full no-data array and overwrite values that exist
        raster = np.full((height, width), raster_nodata)
        new_xsize, new_ysize = min(raster_x_size-x_left, width), min(raster_y_size-y_top, height)
        raster[0:new_ysize, 0:new_xsize] = raster_dataset.GetRasterBand(raster_band).ReadAsArray(x_left, y_top, new_xsize, new_ysize)
        return raster
    else:
        warnings.warn(f"Uncaught case in zonal statistics get_raster_array! Details below:\n bounds = {offsets} with raster extends of {raster_x_size} x {raster_y_size}.")


def calculate_zonal_statistics(raster_path: str, vector_path: str, raster_band=1, allow_touching_pixels=True, show_progress=True) -> dict:
    """
    Collect stats (min, max, mean, median, std, sum and count) on pixel values (raster) which lie within polygons (vector). If allow_touching_pixels is set to True, then any pixel that touches the exterior of the vector geometry is included in the statistics calculation. The returned dictionary has the vector FID as the key, where the values is a dictionary mapping the statistic's name to value.
    
    Inspiration taken from https://opensourceoptions.com/blog/zonal-statistics-algorithm-with-python-in-4-steps/ and https://github.com/natcap/pygeoprocessing/blob/c364ba8e2429c841625c95a34cc871883d3a9cfd/src/pygeoprocessing/geoprocessing.py#L1144 and https://www.gis.usu.edu/~chrisg/python/2009/lectures/ospy_slides4.pdf
    """

    epsg = _check_inputted_datasets(raster_path, vector_path)

    # Get GDAL driver
    mem_driver = ogr.GetDriverByName("Memory")
    mem_driver_gdal = gdal.GetDriverByName("MEM")

    # Open datasets
    vector_dataset = ogr.Open(vector_path)
    vector_layer = vector_dataset.GetLayer()
    raster_dataset = gdal.Open(raster_path)

    # Get information about the raster dataset
    raster_geotransform = raster_dataset.GetGeoTransform()
    raster_nodata = raster_dataset.GetRasterBand(raster_band).GetNoDataValue()
    raster_x_size = raster_dataset.RasterXSize
    raster_y_size = raster_dataset.RasterYSize
    dest_srs = osr.SpatialReference()
    _ = dest_srs.ImportFromEPSG(epsg)

    # Set up a progress bar if the user wants one
    if show_progress:
        progress_bar = tqdm.tqdm(desc="Calculating zonal statistics", total=len(gpd.read_file(vector_path)), leave=False, dynamic_ncols=True)

    # Iterate through each polygon in the shapefile (vector feature)
    zonal_statistics = {}
    vector_feature = vector_layer.GetNextFeature()
    while vector_feature:
        if vector_feature.GetGeometryRef() is not None:
            # Create a new driver
            if os.path.exists("temp"):
                _ = mem_driver.DeleteDataSource("temp")
            temporary_dataset = mem_driver.CreateDataSource("temp")
            
            # Create a new layer of just the one feature
            temporary_layer = temporary_dataset.CreateLayer('polygons', dest_srs, ogr.wkbPolygon)
            _ = temporary_layer.CreateFeature(vector_feature.Clone())
            
            # Determine the offsets
            offsets = _boundingBoxToOffsets(vector_feature.GetGeometryRef().GetEnvelope(), raster_geotransform)
            
            # Transform from the offsets
            new_geotransform = _geotFromOffsets(offsets[0], offsets[2], raster_geotransform)
            
            # Create a blank transformed dataset
            transformed_dataset = mem_driver_gdal.Create("", offsets[3] - offsets[2], offsets[1] - offsets[0], 1, gdal.GDT_Byte)
            _ = transformed_dataset.SetGeoTransform(new_geotransform)
            
            # Rasterise the transformed dataset to the temporary layer where the array is 1 = touches, 0 = does not touch
            _= gdal.RasterizeLayer(transformed_dataset, [1], temporary_layer, burn_values=[1], options=[f'ALL_TOUCHED={str(allow_touching_pixels).upper()}'])
            transformed_array = transformed_dataset.ReadAsArray()
            
            # Grab the values of the raster that intersect the vector geometry
            raster_array = _get_raster_array(raster_dataset, offsets, raster_x_size, raster_y_size, raster_band, raster_nodata)
            
            id = vector_feature.GetFID()
            if raster_array is not None and len(raster_array) > 0:
                # Mask the raster to only cover the vector geometry (transformed array)
                raster_values_over_vector_feature = raster_array[~np.logical_or(raster_array==raster_nodata, np.logical_not(transformed_array))]
                if raster_values_over_vector_feature is not None and len(raster_values_over_vector_feature) > 0:
                    # Then there are some values over the vector feature!!
                    zonal_statistics[id] = {
                        "min": raster_values_over_vector_feature.min(),
                        "max": raster_values_over_vector_feature.max(),
                        "mean": raster_values_over_vector_feature.mean(),
                        "median": np.median(raster_values_over_vector_feature),
                        "std": raster_values_over_vector_feature.std(),
                        "sum": raster_values_over_vector_feature.sum(),
                        "count": len(raster_values_over_vector_feature),
                        "90th_percentile": np.percentile(raster_values_over_vector_feature, 90),
                        "10th_percentile": np.percentile(raster_values_over_vector_feature, 10)
                        }      
                else:
                    # There are no raster cells overlapping the vector feature
                    zonal_statistics[id] = {"min": None, "max": None, "mean": None, "median": None, "std": None, "sum": None, "count": None, "90th_percentile": None, "10th_percentile": None}     
            else:
                # There is no raster?
                zonal_statistics[id] = {"min": None, "max": None, "mean": None, "median": None, "std": None, "sum": None, "count": None, "90th_percentile": None, "10th_percentile": None}
            
            # Clear some memory
            temporary_dataset = None
            temporary_layer = None
            transformed_dataset = None
            # Repeat with the next polygon geometry
            vector_feature = vector_layer.GetNextFeature()
        
        if show_progress: 
            _ = progress_bar.update(1)

    return zonal_statistics  
