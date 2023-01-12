# Copyright 2016 to 2021, Cisco Systems, Inc., all rights reserved.
from django.conf.urls import url
from . import views

app_name = 'yscoverage'
urlpatterns = [
    url(r'^coverage/', views.render_main_page, name="main"),
    url(r'^getconfig/', views.getconfig, name="getconfig"),
    url(r'^getreleases/', views.getreleases, name="getreleases"),
    url(r'^getcoverage/', views.getcoverage, name='getcoverage'),
    url(r'^datasets/', views.render_datasets_page, name='datasets'),
    url(r'^getdataset/', views.get_dataset, name='getdataset'),
    url(r'^getdiff/', views.get_diff, name='getdiff'),
    url(r'^yangsnmp/', views.yang_snmp, name='yangsnmp'),
    url(r'^getdevices/', views.get_devices, name='devices'),
    url(r'^getmodules/', views.get_yang_modules, name='getmodules'),
    url(
        r'^matchoidstoxpaths/',
        views.match_oids_to_xpaths,
        name='matchoidstoxpaths'
    ),
    url(r'^savemapping', views.save_mapping, name='savemapping'),
    url(r'^deletemapping', views.delete_mapping, name='deletemapping'),
    url(r'^importmappings', views.import_mappings, name='importmappings'),
    url(
        r'^importshowmappingsfile',
        views.import_show_mappings_file,
        name='importshowmappingsfile'
    ),
    url(r'^getoidresult', views.get_oid_result, name='getoidresult'),
    url(r'^getmapresult', views.get_map_result, name='getmapresult'),
    url(
        r'^getmappingfilenames',
        views.get_mapping_filenames,
        name='getmappingfilenames'
    ),
    url(
        r'^exportmappingfile',
        views.export_mapping_file,
        name='exportmappingfile'
    ),
]
