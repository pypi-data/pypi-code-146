def extract_large_buildings(gdf):
    large_buildings_gdf = gdf[gdf.area > 50]
    return large_buildings_gdf

def add_column_to_gdf(gdf, column_name, data):
    if column_name in gdf.columns:
        raise ValueError(f"'{column_name}' cannot be added because GDF already contains a column with name!")
    gdf[column_name] = data