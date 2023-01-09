import osgeo.ogr

from pyhelpers.settings import gdal_configurations

gdal_configurations()


def stream_osm_pbf(path_to_osm_pbf, as_object=False):
    """
    :param path_to_osm_pbf: [str] path to the *.osm.pbf file you wish to parse and stream
    :param as_object: [bool] (default: False)
    :return: [generator] allowing for streaming the *.osm.pbf data of the given layer

    Testing e.g.
        import pydriosm as dri

        subregion_name = 'Rutland'
        dri.download_subregion_osm_file(subregion_name, osm_file_format='.osm.pbf', download_dir="tests", update=True)
        path_to_osm_pbf = dri.get_file_path(subregion_name, data_dir="tests")

        subregion_name = 'London'
        dri.download_subregion_osm_file(subregion_name, osm_file_format='.osm.pbf', download_dir="tests", update=True)
        path_to_osm_pbf = dri.get_file_path(subregion_name, data_dir="tests")

        data = stream_osm_pbf(path_to_osm_pbf)
        for x in data:
            print(x)
            break
    """
    raw_osm_pbf = osgeo.ogr.Open(path_to_osm_pbf)
    layer_count = raw_osm_pbf.GetLayerCount()
    # Loop through all available layers
    for i in range(layer_count):
        # Get the data and name of the i-th layer
        layer = raw_osm_pbf.GetLayerByIndex(i)
        layer_name = layer.GetName()
        for feat in layer:
            yield layer_name, feat.ExportToJson(as_object=as_object)
