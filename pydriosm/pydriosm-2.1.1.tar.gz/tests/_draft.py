import os
import time

import osgeo.ogr
import pandas as pd
from pyhelpers.ops import split_list
from pyhelpers.settings import gdal_configurations

from pydriosm.downloader import BBBikeDownloader, GeofabrikDownloader
from pydriosm.reader import PBFReadParse, VarReadParse

gdal_configurations()

gfd = GeofabrikDownloader()
bbd = BBBikeDownloader()

download_dir = "tests\\osm_data"

gfd.download_osm_data('Rutland', ".pbf", download_dir, verbose=True)
gfd.download_osm_data('Rutland', ".bz2", download_dir, verbose=True)
gfd.download_osm_data('Rutland', ".shp", download_dir, verbose=True)
gfd.download_osm_data('London', ".shp", download_dir, verbose=True)
bbd.download_osm_data('Birmingham', ".csv.xz", download_dir, verbose=True)
bbd.download_osm_data('Leeds', ".geojson.xz", download_dir, verbose=True)

path_to_rutland_pbf = gfd.data_paths[0]
path_to_rutland_bz2 = gfd.data_paths[1]
path_to_rutland_shp = gfd.data_paths[2]
path_to_london_shp = gfd.data_paths[3]

readable = True
expand = True
parse_geometry = True
parse_properties = True
parse_other_tags = True
number_of_chunks = None

start = time.time()

PBFReadParse.get_pbf_layer_names(path_to_rutland_pbf)

data = PBFReadParse.read_pbf(
    path_to_rutland_pbf, readable, expand, parse_geometry, parse_properties, parse_other_tags,
    number_of_chunks)

print(time.time() - start)

# ==================================================================================================

raw_pbf = osgeo.ogr.Open(path_to_rutland_pbf)

# i = 0

dfs = []
for i in range(raw_pbf.GetLayerCount()):
    try:
        layer = raw_pbf.GetLayerByIndex(i)
        # layer_name = layer.GetName()
        # expand=True:
        #   layer_data = pd.DataFrame(f.ExportToJson(as_object=True) for f in layer)
        # expand=False:
        #   dat = [[f.ExportToJson(as_object=True)] for f in layer]
        # layer_data = pd.Series(data=dat, name=layer_name)
        df = PBFReadParse.read_pbf_layer(
            layer, readable, expand, parse_geometry, parse_properties, parse_other_tags)
        dfs.append(df)
    except Exception as e:
        print(e)
        break

# layer = raw_pbf.GetLayerByIndex(0)
# lyr_dat = pd.DataFrame(f.ExportToJson(as_object=True) for f in layer)
#
# layer = raw_pbf.GetLayerByIndex(1)
# lyr_dat = pd.DataFrame(f.ExportToJson(as_object=True) for f in layer)
#
# layer = raw_pbf.GetLayerByIndex(2)
# lyr_dat = pd.DataFrame(f.ExportToJson(as_object=True) for f in layer)
#
# layer = raw_pbf.GetLayerByIndex(3)
# lyr_dat = pd.DataFrame(f.ExportToJson(as_object=True) for f in layer)
#
layer = raw_pbf.GetLayerByIndex(4)
lyr_dat = pd.DataFrame(f.ExportToJson(as_object=True) for f in layer)


for i, prop in enumerate(lyr_dat['properties']):
    try:
        PBFReadParse.transform_other_tags(prop['other_tags'])
    except Exception as e:
        print(e)
        break

# func_args_ = [readable, reformat_geom, parse_properties, parse_other_tags, number_of_chunks]
# func_args = [(raw_pbf.GetLayerByIndex(i), *func_args_) for i in range(raw_pbf.GetLayerCount())]
#
# # processes = []
# # for args in func_args:
# #     p = multiprocessing.Process(target=read_pbf_layer, args=args)
# #     processes.append(p)
# #     p.start()
# #
# # for process in processes:
# #     process.join()
#
# rslt = []
#
# t1 = threading.Thread(target=read_pbf_layer, args=(func_args[0], rslt))
# t2 = threading.Thread(target=read_pbf_layer, args=func_args[1])
# t1.start()
# t2.start()
# t1.join()
# t2.join()
#
# start = time.time()
#
# # Create a list of threads
# threads = []
#
# for i, args in enumerate(func_args):
#     process = threading.Thread(target=read_pbf_layer, args=args)
#     process.start()
#     threads.append(process)
#
# for process in threads:
#     process.join()
#
# print(time.time() - start)

layer = raw_pbf.GetLayerByIndex(0)
raw_layer_data = [f for _, f in enumerate(layer)]


num_of_threads = int(os.cpu_count() / 2)

raw_layer_data_ = list(split_list(raw_layer_data, num_of_threads))


path_to_geojson_xz = bbd.data_paths[0]
geojson_xz = VarReadParse.read_geojson_xz(path_to_geojson_xz, parse_geometry=True)

path_to_csv_xz = bbd.data_paths[1]
csv_xz = VarReadParse.read_csv_xz(path_to_csv_xz, col_names=None)


# ==================================================================================================

from pyhelpers.settings import gdal_configurations, pd_preferences

from pydriosm.downloader import GeofabrikDownloader

pd_preferences()

gdal_configurations()

gfd = GeofabrikDownloader()

download_dir = "tests\\osm_data"

gfd.download_osm_data('Rutland', ".shp", download_dir, verbose=True)
gfd.download_osm_data('London', ".shp", download_dir, verbose=True)

path_to_rutland_shp = gfd.data_paths[0]
path_to_london_shp = gfd.data_paths[1]


# ==================================================================================================

from pyhelpers.text import find_similar_str
from pydriosm.reader import GeofabrikReader
import os
import re
import glob
import shutil

gfr = GeofabrikReader()

subregion_names = ['London', 'Kent', 'Surrey']
layer_name = 'transport'
data_dir = "tests\\osm_data"

# Make sure all the required shape files are ready
layer_name_ = find_similar_str(x=layer_name, lookup_list=gfr.SHP.LAYER_NAMES)
subregion_names_ = [gfr.downloader.validate_subregion_name(x) for x in subregion_names]

osm_file_format = ".shp.zip"

update = False
verbose = True
download_confirmation_required = True

# Download the files (if not available)
paths_to_shp_zip_files = gfr.downloader.download_osm_data(
    subregion_names_, osm_file_format=osm_file_format, download_dir=data_dir,
    update=update, confirmation_required=download_confirmation_required,
    deep_retry=True, interval=None, verbose=verbose, ret_download_path=True)

shp_zip_pathnames = paths_to_shp_zip_files.copy()

engine = 'pyshp'

path_to_extract_dirs = []
for zfp in shp_zip_pathnames:
    extract_dir = gfr.SHP.unzip_shp_zip(
        shp_zip_pathname=zfp, layer_names=layer_name, verbose=verbose, ret_extract_dir=True)
    path_to_extract_dirs.append(extract_dir)

region_names = [
    re.search(r'.*(?=\.shp\.zip)', os.path.basename(x).replace("-latest-free", "")).group(0)
    for x in shp_zip_pathnames]

# Specify a directory that stores files for the specific layer
path_to_data_dir = os.path.commonpath(shp_zip_pathnames)
suffix = "_temp"
# prefix = "_".join([x.lower().replace(' ', '-') for x in region_names]) + "_"
prefix = "_".join(["".join([y[0] for y in re.split(r'[- ]', x)]) for x in region_names]) + "_"
merged_dirname_temp = f"{prefix}{layer_name}{suffix}"
path_to_merged_dir_temp = os.path.join(path_to_data_dir, merged_dirname_temp)
os.makedirs(path_to_merged_dir_temp, exist_ok=True)

# Copy files into a temp directory
paths_to_temp_files = []
for subregion_name, path_to_extract_dir in zip(region_names, path_to_extract_dirs):
    orig_filename_list = glob.glob1(path_to_extract_dir, f"*{layer_name}*")
    for orig_filename in orig_filename_list:
        orig = os.path.join(path_to_extract_dir, orig_filename)
        dest = os.path.join(
            path_to_merged_dir_temp,
            f"{subregion_name.lower().replace(' ', '-')}_{orig_filename}")
        shutil.copyfile(orig, dest)
        paths_to_temp_files.append(dest)

# Get the paths to the target .shp files
paths_to_shp_files = [x for x in paths_to_temp_files if x.endswith(".shp")]

# try:
output_dir = None

from pyhelpers.dirs import validate_dir

if output_dir:
    path_to_merged_dir = validate_dir(path_to_dir=output_dir)
else:
    path_to_merged_dir = os.path.join(
        path_to_data_dir, merged_dirname_temp.replace(suffix, "", -1))
os.makedirs(path_to_merged_dir, exist_ok=True)

#
shp_pathnames = paths_to_shp_files.copy()

emulate_gpd = True

shp_data = gfr.SHP.read_layer_shps(shp_pathnames, emulate_gpd=emulate_gpd)
if 'geometry' in shp_data.columns:
    k = shp_data['geometry'].map(lambda x: x.geom_type)
else:
    k = 'shape_type'

for geo_typ, dat in shp_data.groupby(k):
    if isinstance(k, str):
        geo_typ = gfr.SHP.SHAPE_TYPE_GEOM_NAME[geo_typ]
    out_fn = os.path.join(path_to_merged_dir, f"{geo_typ.lower()}.shp")
    gfr.SHP.write_to_shapefile(data=dat, write_to=out_fn)

    # Write .cpg
    with open(out_fn.replace(".shp", ".cpg"), mode="w") as cpg:
        cpg.write(gfr.SHP.ENCODING)
    # Write .prj
    with open(out_fn.replace(".shp", ".prj"), mode="w") as prj:
        prj.write(gfr.SHP.EPSG4326_WGS84_ESRI_WKT)


# ==================================================================================================

from pydriosm.ios import PostgresOSM
from pydriosm.reader import PBFReadParse
from pyhelpers._cache import _check_dependency
from pyhelpers.ops import get_number_of_chunks, split_list
import gc
import pandas as pd


osmdb = PostgresOSM(database_name='osmdb_test')

osmdb.data_source = 'BBBike'
subregion_name = 'London'
osm_file_format = '.osm.pbf'

subregion_names = ['London']
data_dir = "tests\\osm_data"
update_osm_pbf = False
if_exists = 'replace'
chunk_size_limit = 50
confirmation_required = True
verbose = True

expand = True
parse_geometry = True
parse_properties = True
parse_other_tags = True
pickle_pbf_file = True
rm_pbf_file = True


path_to_osm_pbf = osmdb.downloader.download_osm_data(
    subregion_names=subregion_name, osm_file_format=osm_file_format,
    download_dir=data_dir, update=update_osm_pbf, confirmation_required=False,
    verbose=verbose, ret_download_path=True)[0]

read_pbf_args = {
    'expand': expand,
    'parse_geometry': parse_geometry,
    'parse_properties': parse_properties,
    'parse_other_tags': parse_other_tags,
}
import_args = {
    'subregion_name': subregion_name,
    'osm_file_format': osm_file_format,
    'path_to_osm_pbf': path_to_osm_pbf,
    'chunk_size_limit': chunk_size_limit,
    'if_exists': if_exists,
    'pickle_pbf_file': pickle_pbf_file,
    'verbose': verbose
}
import_args.update(read_pbf_args)

osgeo_ogr = _check_dependency(name='osgeo.ogr')

raw_osm_pbf = osgeo_ogr.Open(path_to_osm_pbf)
layer_count = raw_osm_pbf.GetLayerCount()

layer_names, layer_data_list = [], []

osgeo_gdal = _check_dependency(name='osgeo.gdal')
# Stop GDAL printing both warnings and errors to STDERR
osgeo_gdal.PushErrorHandler('CPLQuietErrorHandler')
# Make GDAL raise python exceptions for errors (warnings won't raise an exception)
osgeo_gdal.UseExceptions()

for i in range(layer_count):

    layer = raw_osm_pbf.GetLayerByIndex(i)  # Hold the i-th layer
    layer_name = layer.GetName()

    layer_dat_list = []

    features = [feat for feat in layer]

    count_of_features = len(features)
    number_of_chunks = get_number_of_chunks(path_to_osm_pbf, chunk_size_limit)
    list_of_chunks = split_list(lst=features, num_of_sub=number_of_chunks)

    del features
    gc.collect()

    for chunk in list_of_chunks:  # Loop through all chunks
        if expand:
            lyr_dat = pd.DataFrame(f.ExportToJson(as_object=True) for f in chunk)
        else:
            lyr_dat = pd.DataFrame([f.ExportToJson() for f in chunk], columns=[layer_name])

        layer_dat = PBFReadParse.transform_pbf_layer_field(
            layer_data=lyr_dat, layer_name=layer_name, parse_geometry=parse_geometry,
            parse_properties=parse_properties, parse_other_tags=parse_other_tags)

        if_exists_ = if_exists if if_exists == 'fail' else 'append'
        # self.import_osm_layer(
        #     layer_data=layer_dat, table_name=subregion_name, schema_name=layer_name,
        #     if_exists=if_exists_, confirmation_required=False, **kwargs)

        if pickle_pbf_file:
            layer_dat_list.append(layer_dat)

        print("Done.")

        del layer_dat
        gc.collect()


# ==================================================================================================
