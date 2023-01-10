"""
Geospatialutils - a Python library for processing coordinate system data.
"""

from xmlrpc.client import Boolean
# from osgeo import gdal #conda install gdal
# from osgeo import osr
# from osgeo import ogr

import xml.etree.ElementTree as ET 
import math
from typing import List
import matplotlib

import ifcopenshell
import ifcopenshell.geom as geom
import ifcopenshell.util
from scipy.spatial.transform import Rotation as R

import trimesh
import fcl

#IMPORT MODULES
import geomapi.utils as ut


def belgian_datum_to_wgs84(latBel:float,lngBel:float) -> tuple:
    """
    Input parameters : Lat, Lng : latitude / longitude in decimal degrees and in Belgian 1972 datum
    Output parameters : LatWGS84, LngWGS84 : latitude / longitude in decimal degrees and in WGS84 datum
    source: http://zoologie.umons.ac.be/tc/algorithms.aspx
    """
    Haut = 0.0   
        
    #conversion to radians
    Lat = (math.pi / 180.0) * latBel
    Lng = (math.pi / 180.0) * lngBel
    
    SinLat = math.sin(Lat)
    SinLng = math.sin(Lng)
    CoSinLat = math.cos(Lat)
    CoSinLng = math.cos(Lng)
    
    dx = -125.8
    dy = 79.9
    dz = -100.5
    da = -251.0
    df = -0.000014192702
    
    LWf = 1.0 / 297.0
    LWa = 6378388
    LWb = (1.0 - LWf) * LWa
    LWe2 = (2.0 * LWf) - (LWf * LWf)
    Adb = 1.0 / (1.0 - LWf)
    
    Rn = LWa / math.sqrt(1.0 - LWe2 * SinLat * SinLat)
    Rm = LWa * (1.0 - LWe2) / (1 - LWe2 * Lat * Lat) ** 1.5
    
    DLat = -dx * SinLat * CoSinLng - dy * SinLat * SinLng + dz * CoSinLat
    DLat = DLat + da * (Rn * LWe2 * SinLat * CoSinLat) / LWa
    DLat = DLat + df * (Rm * Adb + Rn / Adb) * SinLat * CoSinLat
    DLat = DLat / (Rm + Haut)
    
    DLng = (-dx * SinLng + dy * CoSinLng) / ((Rn + Haut) * CoSinLat)
    Dh = dx * CoSinLat * CoSinLng + dy * CoSinLat * SinLng + dz * SinLat
    Dh = Dh - da * LWa / Rn + df * Rn * Lat * Lat / Adb
    
    LatWGS84 = ((Lat + DLat) * 180.0) / math.pi
    LngWGS84 = ((Lng + DLng) * 180.0) / math.pi
    return LatWGS84,LngWGS84

def wgs84_to_belgian_datum(LatWGS84: float,LngWGS84:float) -> tuple:
    """
    Input parameters : Lat, Lng : latitude / longitude in decimal degrees and in WGS84 datum
    Output parameters : LatBel, LngBel : latitude / longitude in decimal degrees and in Belgian datum
    source: http://zoologie.umons.ac.be/tc/algorithms.aspx
    """
    Haut = 0.0 
    
    #conversion to radians
    Lat = (math.pi / 180.0) * LatWGS84
    Lng = (math.pi / 180.0) * LngWGS84
    
    SinLat = math.sin(Lat)
    SinLng = math.sin(Lng)
    CoSinLat = math.cos(Lat)
    CoSinLng = math.cos(Lng)
    
    dx = 125.8
    dy = -79.9
    dz = 100.5
    da = 251.0
    df = 0.000014192702
    
    LWf = 1.0 / 297.0
    LWa = 6378388.0
    LWb = (1.0 - LWf) * LWa
    LWe2 = (2.0 * LWf) - (LWf * LWf)
    Adb = 1.0 / (1.0 - LWf)
    
    Rn = LWa / math.sqrt(1 - LWe2 * SinLat * SinLat)
    Rm = LWa * (1.0 - LWe2) / (1 - LWe2 * Lat * Lat) ** 1.5
    
    DLat = -dx * SinLat * CoSinLng - dy * SinLat * SinLng + dz * CoSinLat
    DLat = DLat + da * (Rn * LWe2 * SinLat * CoSinLat) / LWa
    DLat = DLat + df * (Rm * Adb + Rn / Adb) * SinLat * CoSinLat
    DLat = DLat / (Rm + Haut)
    
    DLng = (-dx * SinLng + dy * CoSinLng) / ((Rn + Haut) * CoSinLat)
    Dh = dx * CoSinLat * CoSinLng + dy * CoSinLat * SinLng + dz * SinLat
    Dh = Dh - da * LWa / Rn + df * Rn * Lat * Lat / Adb
    
    latBel = ((Lat + DLat) * 180.0) / math.pi
    lngBel = ((Lng + DLng) * 180.0) / math.pi
    return  latBel,lngBel

def spherical_coordinates_to_lambert72(latBel :float,lngBel:float) -> tuple:
    """
    Conversion from spherical coordinates to Lambert 72
    Input parameters : lat, lng (spherical coordinates)
    Spherical coordinates are in decimal degrees converted to Belgium datum!
    source: http://zoologie.umons.ac.be/tc/algorithms.aspx
    """
     
    LongRef  = 0.076042943        #'=4°21'24"983
    bLamb  = 6378388 * (1 - (1 / 297))
    aCarre  = 6378388 ** 2
    eCarre  = (aCarre - bLamb ** 2) / aCarre
    KLamb  = 11565915.812935
    nLamb  = 0.7716421928
 
    eLamb = math.sqrt(eCarre)
    eSur2 = eLamb / 2.0
    
    #conversion to radians
    lat = (math.pi / 180.0) * latBel
    lng = (math.pi / 180.0) * lngBel
 
    eSinLatitude  = eLamb * math.sin(lat)
    TanZDemi  = (math.tan((math.pi / 4) - (lat / 2))) * (((1 + (eSinLatitude)) / (1 - (eSinLatitude))) ** (eSur2))
       
 
    RLamb = KLamb * ((TanZDemi) ** nLamb)
 
    Teta = nLamb * (lng - LongRef)
 
    x = 150000 + 0.01256 + RLamb * math.sin(Teta - 0.000142043)
    y = 5400000 + 88.4378 - RLamb * math.cos(Teta - 0.000142043)
    return x,y

def lambert72_to_spherical_coordinates(x :float ,y:float) -> tuple: 
    """"
    Belgian Lambert 1972---> Spherical coordinates
    Input parameters : X, Y = Belgian coordinates in meters
    Output : latitude and longitude in Belgium Datum!
    source: http://zoologie.umons.ac.be/tc/algorithms.aspx
    """
    LongRef = 0.076042943  #      '=4°21'24"983
    nLamb  = 0.7716421928 #
    aCarre = 6378388 ** 2 #
    bLamb = 6378388 * (1 - (1 / 297)) #
    eCarre = (aCarre - bLamb ** 2) / aCarre #
    KLamb = 11565915.812935 #
    
    eLamb = math.sqrt(eCarre)
    eSur2 = eLamb / 2
    
    Tan1  = (x - 150000.01256) / (5400088.4378 - y)
    Lambda = LongRef + (1 / nLamb) * (0.000142043 + math.atan(Tan1))
    RLamb = math.sqrt((x - 150000.01256) ** 2 + (5400088.4378 - y) ** 2)
    
    TanZDemi = (RLamb / KLamb) ** (1 / nLamb)
    Lati1 = 2 * math.atan(TanZDemi)
    
    eSin=0.0
    Mult1=0.0
    Mult2=0.0
    Mult=0.0
    LatiN=0.0
    Diff=1     

    while abs(Diff) > 0.0000000277777:
        eSin = eLamb * math.sin(Lati1)
        Mult1 = 1 - eSin
        Mult2 = 1 + eSin
        Mult = (Mult1 / Mult2) ** (eLamb / 2)
        LatiN = (math.pi / 2) - (2 * (math.atan(TanZDemi * Mult)))
        Diff = LatiN - Lati1
        Lati1 = LatiN
    
    latBel = (LatiN * 180) / math.pi
    lngBel = (Lambda * 180) / math.pi
    return latBel,lngBel

# def wgs84_to_l72(lat:float,long:float) -> tuple:
#     SourceEPSG = 4326  
#     TargetEPSG = 31370

#     source = osr.SpatialReference()
#     source.ImportFromEPSG(SourceEPSG)

#     target = osr.SpatialReference()
#     target.ImportFromEPSG(TargetEPSG)


#     transform = osr.CoordinateTransformation(source, target)
#     point = ogr.Geometry(ogr.wkbPoint)
#     point.SetPoint_2D(0, float(Long), float(Lat))
#     point.Transform(transform)
    
#     x=point.GetX()
#     y=point.GetY()
    
#     return x,y 
