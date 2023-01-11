"""
Tools related to geometric items:
    - Quickly convert a GeoDataFrame to a simplified topojson file
"""

__all__ = ["save_geodataframe_as_topojson"]

import tempfile, warnings, geopandas as gpd, numpy as np, pandas as pd, os, topojson as tp, typing

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