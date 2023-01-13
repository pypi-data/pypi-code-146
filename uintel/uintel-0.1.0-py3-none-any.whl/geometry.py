"""
Tools related to geometric items:
    - Quickly convert a GeoDataFrame to a simplified topojson file
    - Calculate statistics of raster files over a polygon geometry ("zonal statistics")
"""

__all__ = ["save_geodataframe_as_topojson", "calculate_zonal_statistics"]

import tempfile, warnings, geopandas as gpd, numpy as np, pandas as pd, os, topojson as tp, typing, rasterio as rio, tqdm, osgeo

def save_geodataframe_as_topojson(gdf: gpd.GeoDataFrame, save_path: str, simplify_factor: typing.Optional[float], crs: typing.Optional[int]) -> None:
    """
    Convert a [multi-geometry type or single-geometry type] geodataframe to a topojson file, optimised for the web by simplyfing geometries in EPSG:4326. If the inputted geodataframe does not have an associated crs, please input it as crs=2193, for example.
    """
    
    # Make a temporary directory to save shapefile and topojsons to
    temp_dir = tempfile.TemporaryDirectory()
    warnings.filterwarnings("ignore")
    
    # Drop duplicates and prepare the dataset
    gdf.drop_duplicates(inplace=True)
    gdf.reset_index(drop=True, inplace=True)
    if not gdf.crs:
        gdf = gdf.set_crs(crs)
    gdf.to_crs("EPSG:4326", inplace=True)
    
    # Split the GeoDataFrame into the 3 main geometry types
    points = gdf[gdf.geom_type.isin(["Point", "MultiPoint"])]
    polylines = gdf[gdf.geom_type.isin(["Polyline", "LineString"])]
    polygons = gdf[gdf.geom_type.isin(["Polygon", "MulitPolygon"])]
    
    # Make a geojson dictionary to add all the features to
    final_shp = gpd.GeoDataFrame()

    for (geom_type, shapefile) in [("point", points), ("polyline", polylines), ("polygon", polygons)]:
        if len(shapefile) > 0:           
            # Make sure all geometry is good! You can't use pass to topojson if there is invalid geometry!
            valid_geometry = shapefile.is_valid
            if not valid_geometry.all():
                if geom_type == "polyline":
                    # An error occurs "too few points in geometry component" and this is as the line is clipped and there is no length to it! We can't buffer it and there isn't a nice way to fix it unfortunately. Revisit: ST_MakeValid in SQL could be a go?. Hence, only retain the good geometry
                    warnings.warn(f"{len(valid_geometry)-valid_geometry.sum()} LineString geometries could not be saved to the topojson file as they are invalid. The cause of this may be due to a very small line length. These geometries have been skipped in the meantime.")
                    shapefile = shapefile[valid_geometry]
                else:
                    # Usually a polygon asset doesn't have any errors when buffer is used!
                    shapefile.loc[~valid_geometry, "geometry"] = shapefile.loc[~valid_geometry, "geometry"].buffer(0)

            # Simplify the geometry
            if simplify_factor == None or type(simplify_factor) not in (float, int) or geom_type == "point":
                shapefile = tp.Topology(shapefile, prequantize=False).to_gdf(crs="EPSG:4326")
            else:
                shapefile = tp.Topology(shapefile, prequantize=False, toposimplify=simplify_factor, prevent_oversimplify=True).to_gdf(crs="EPSG:4326")
                        
            # A stupid error occurs in opening topojsons in the website where there are NaN values! They occur in the id column which has been dropped, but just in case, replace them with none values.
            if "id" in shapefile.columns:
                shapefile.drop(columns="id", inplace=True)
            
            # Change the dtypes of the columns
            for column_name in shapefile.columns.tolist():
                if column_name == "asset_id":
                    # Reduce dtypes
                    if shapefile["asset_id"].max() < 127:
                        shapefile["asset_id"] = shapefile["asset_id"].astype('uint8')
                    elif shapefile["asset_id"].max() < 32767:
                        shapefile["asset_id"] = shapefile["asset_id"].astype('uint16')
                    else:
                        shapefile["asset_id"] = shapefile["asset_id"].astype('uint32')
                elif column_name == "geometry":
                    continue
                else:
                    # Assume every other column is categorical
                    shapefile[column_name] = shapefile[column_name].astype('object')
            
            # Replace any bad geometries after the simplification procedure, with the original unsimplified geometry. Perhaps we could use a different (like a backup) simplification factor that is less, but seeing as its only a few geometries then we may as well use the original geometry. 
            geometry_is_valid = np.logical_and(shapefile.is_valid, ~shapefile.is_empty)
            gdf_geometry_is_valid = np.logical_and(gdf.is_valid, ~gdf.is_empty)
            if geometry_is_valid.sum() != len(geometry_is_valid):
                # Then there is at least one geometry that is invalid after simplification.
                shapefile = pd.concat([shapefile[geometry_is_valid], gdf[~gdf_geometry_is_valid]]).sort_index()
            # Add to the overall shapefile
            final_shp = pd.concat([final_shp, shapefile], ignore_index=False).sort_index()

    # Remove all the temporary files made
    temp_dir.cleanup()
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    # Convert the overall shapefile to a Topology object and save it
    tp.Topology(final_shp, prequantize=False).to_json(save_path)



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
    mem_driver = osgeo.ogr.GetDriverByName("Memory")
    mem_driver_gdal = osgeo.gdal.GetDriverByName("MEM")

    # Open datasets
    vector_dataset = osgeo.ogr.Open(vector_path)
    vector_layer = vector_dataset.GetLayer()
    raster_dataset = osgeo.gdal.Open(raster_path)

    # Get information about the raster dataset
    raster_geotransform = raster_dataset.GetGeoTransform()
    raster_nodata = raster_dataset.GetRasterBand(raster_band).GetNoDataValue()
    raster_x_size = raster_dataset.RasterXSize
    raster_y_size = raster_dataset.RasterYSize
    dest_srs = osgeo.osr.SpatialReference()
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
            temporary_layer = temporary_dataset.CreateLayer('polygons', dest_srs, osgeo.ogr.wkbPolygon)
            _ = temporary_layer.CreateFeature(vector_feature.Clone())
            
            # Determine the offsets
            offsets = _boundingBoxToOffsets(vector_feature.GetGeometryRef().GetEnvelope(), raster_geotransform)
            
            # Transform from the offsets
            new_geotransform = _geotFromOffsets(offsets[0], offsets[2], raster_geotransform)
            
            # Create a blank transformed dataset
            transformed_dataset = mem_driver_gdal.Create("", offsets[3] - offsets[2], offsets[1] - offsets[0], 1, osgeo.gdal.GDT_Byte)
            _ = transformed_dataset.SetGeoTransform(new_geotransform)
            
            # Rasterise the transformed dataset to the temporary layer where the array is 1 = touches, 0 = does not touch
            _= osgeo.gdal.RasterizeLayer(transformed_dataset, [1], temporary_layer, burn_values=[1], options=[f'ALL_TOUCHED={str(allow_touching_pixels).upper()}'])
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
