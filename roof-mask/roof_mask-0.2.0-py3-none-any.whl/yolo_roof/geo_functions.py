import argparse
import os
import io
import sys
import json 
import numpy as np
import pandas as pd
import math
import cv2
import platform
import requests
import logging
from datetime import datetime
import shutil

# plot
from PIL import Image
from matplotlib import pyplot as plt

### coco mask to polygon ###
import base64
from pycocotools.coco import COCO
from skimage import measure
from io import BytesIO

### parallel download images ###
import uuid
from joblib import Parallel, delayed
from concurrent import futures

#### shapely ###
import shapely
import shapely.wkt
from shapely.ops import unary_union
from shapely.geometry import Polygon, MultiPoint
from shapely.geometry import Polygon

class Ecopia_Geocoding:
    '''
    Aquire building boundary lat long from giving address
    '''
    def __init__(self, address, Ecopia_Api_Key = 'cKr6EbB2YxXtNobPfBrB5'):
        self.address = address
        self.Ecopia_Api_Key = Ecopia_Api_Key

    def ecopia_addr_API(self,addr):
        '''
        Returns the API request result.
        @addr is a string of the full address.
        '''
        url = 'https://geocoding.ecopiatech.com/v4/geocoding_wkt?api_key=' + self.Ecopia_Api_Key + '&address=' + addr
        return requests.get(url, verify=True) # verify=False is necessary due to the security setting in Zscaler; when moving to Azure/production, switch to verify=True

    def ecopia_parcel_detail_API(self, parcel_id):
        '''
        Returns the API request result.
        @addr is a string of the parcel ID.
        '''
        url = 'https://geocoding.ecopiatech.com/v4/parcel_details?api_key=' + self.Ecopia_Api_Key + '&parcel_id=' + parcel_id
        return requests.get(url, verify=True) # verify=False is necessary due to the security setting in Zscaler; when moving to Azure/production, switch to verify=True

    def ecopia_best_full_ftpts(self, addr):
        '''
        Returns a tuple of a flag, a json object, and a list. 
        The flag is whether the geocoding is the most accurate level results.
        The json object is the results from the address inquiry.
        The list is a list of footprints, each of which is a dictionary with 3 keys: 'id', 'wkt', and 'location'. The first two values are strings. The location value is a dictionary with two keys, 'lat' and 'lon'.
        The first item in the list is from the geocoding app, where most likely the input address is, while the others are buildings (fully or partially) on the same parcel.
        The first item contains 'wkt', which is the 'orig_wkt' from the address API, and 'clipped_wkt', which is the wkt from the address API, so it's consistent with the rest of ftpts from the parcel API.
        @addr is a string of the full address.
        '''
        self.address = addr
        r1 = self.ecopia_addr_API(self.address)
        result1 = r1.json()

        ftpt1 = dict()
        ftpt1['id'] = result1['result']['id']
        ftpt1['wkt'] = result1['result']['orig_wkt']
        ftpt1['clipped_wkt'] = result1['result']['wkt']
        ftpt1['location'] = result1['result']['location']

        ftpts = [ftpt1]
        accuracy_flag = False
        r2 = ''
        confi_level = 0 

        # if ecopia can find the best footprint return it
        if result1['status'] == True and result1['result']["approximation"] == "":
            accuracy_flag = True
            confi_level = int(result1['result']['confi_level'])
            # Geocoding result is at the most accurate level
            if len(result1['result']['wkt'])>0:
                return (accuracy_flag, result1, ftpts, r2, confi_level)
            # Geocoding result is not accurate enough
            else:
                parcel_id = result1['result']['parcel_id']
                r2 = self.ecopia_parcel_detail_API(parcel_id).json()
                if 'footprints' in r2.keys(): # In some cases, the returned results have no 'footprints', e.g. when the parcle is too big and the result will show some error message
                    r2_result = r2['footprints'] 
                    if isinstance(r2_result, list): # in some cases, there is no footprints returned and the value can be None rather than a list (even an empty list)
                        ftpts.extend(r2_result)
                return (accuracy_flag, result1, ftpts, r2, confi_level)
        else: 
            return (accuracy_flag, result1, ftpts, r2, confi_level)
    
    def get_ftpts_box(self, ftpts):
        '''
        @ftpts is a list of dictionaries, in which key 'wkt' points to building ftpt polygons in (long, lat) coordinates.
        Returns a bounding box to get image that should contain all footprints from @ftpts in the format: (min_lat, min_long,  max_lat, max_long) 
        '''

        wkt_list = [ftpt['wkt'] for ftpt in ftpts if not isinstance(ftpt['wkt'], list)] # address API wkt value is a list, while parcel API wkt value is a string (only one polygon)
        wkt_list.extend([wkt for ftpt in ftpts for wkt in ftpt['wkt'] if isinstance(ftpt['wkt'], list)])

        polys = [shapely.wkt.loads(wkt) for wkt in wkt_list]
        bounds = [poly.bounds for poly in polys]
        longs = [b[0] for b in bounds]
        longs.extend([b[2] for b in bounds])
        lats = [b[1] for b in bounds]
        lats.extend([b[3] for b in bounds])

        if len(lats) < 2: return None # sometimes there are no wkts in Ecopia results

        min_lat = min(lats)
        max_lat = max(lats)
        min_long = min(longs)
        max_long = max(longs)
        # print([min_lat,min_long,  max_lat, max_long]) 
        return [min_lat, min_long, max_lat, max_long]

    
    def boundary_to_lat_lon_with_buffer(self, polyBounds, flag = 0):
        '''
        Returns a bounding box with a buffer to current polyBounds to get image
        polyBounds is in the format: (min_lat, min_long, max_lat, max_long) 
        output formate is format: (min_lat, min_long, max_lat, max_long) 
        flag = 0:
        buffer is a abslute value 0.00002 degrees
        flag = 1:
        buffer is either the 10% of the bounding box or 0.00002 degrees which is min
        '''
        if flag == 0:
            buffer_w = 0.00003 # 0.00002
            buffer_h = 0.00003 # 0.00002
        elif flag == 1: 
            buffer_percentage = 0.1
            abs_buffer = 0.00002
            # width and height
            width = abs(polyBounds[2]-polyBounds[0])
            height = abs(polyBounds[3]-polyBounds[1])

            buffer_w = min(buffer_percentage * width, abs_buffer)
            buffer_h = min(buffer_percentage * height, abs_buffer)

        # new corners lat and long
        top_left_lat = polyBounds[0] - buffer_h
        top_left_lon = polyBounds[1] - buffer_w
        bottom_right_lat = polyBounds[2] + buffer_h
        bottom_right_lon = polyBounds[3] + buffer_w

        # print(top_left_lat,top_left_lon,bottom_right_lat,bottom_right_lon)
        return [top_left_lat,top_left_lon,bottom_right_lat,bottom_right_lon]
    
    def address2boundary_lat_long_with_buffer(self):
        accuracy_flag, result1, ftpts, r2, confi_level = self.ecopia_best_full_ftpts(self.address)
        # print(ftpts)
        self.result1 = result1
        self.ftpts = ftpts
        self.r2 = r2
        if accuracy_flag:
            lat_lon_boundary_no_buffer = self.get_ftpts_box(ftpts)
            lat_lon_coord= self.boundary_to_lat_lon_with_buffer(lat_lon_boundary_no_buffer)
            return lat_lon_coord
        else:
            return []

    def address2boundary_lat_long_with_buffer_and_confi_level(self):
        accuracy_flag, result1, ftpts, r2, confi_level = self.ecopia_best_full_ftpts(self.address)
        # print(ftpts)
        self.result1 = result1
        self.ftpts = ftpts
        self.r2 = r2
        if confi_level > 6:
            lat_lon_boundary_no_buffer = self.get_ftpts_box(ftpts)
            lat_lon_coord= self.boundary_to_lat_lon_with_buffer(lat_lon_boundary_no_buffer)
            return lat_lon_coord, confi_level
        else:
            return []

############################################### Near Map
class Nearmap_Image:
    '''
    Aquire image giving boundary(min_long, min_lat, max_long, max_lat)
    and check date '%Y-%m-%d' '2022-05-01'
    '''
    def __init__(self, boundary, zoom_level = None, date=datetime.today().strftime('%Y-%m-%d'),
                 Nearmap_Api_Key = 'NGZkNzZmNTUtYWQ3Ny00NTdmLWIzMGEtZTIwZjk1OGZjNDM4'):
        self.boundary = boundary
        self.check_date = date
        self.zoom_level = zoom_level
        self.Nearmap_Api_Key = Nearmap_Api_Key
        # self.Today_date = datetime.today().strftime('%Y-%m-%d')
        # Today_date = '2022-05-01'
        # print(f'Today is: {self.date}.')

    def lat_lon_to_tile_coords(self, lat_deg, lon_deg, zoom):
        # From: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return [xtile, ytile]

    def tile_coords_to_lat_lon(self, xtile, ytile, zoom, flag = 0):
        '''
        flag = 0 : NW-corner of the square
        flag = 1 : center
        flag = 2 : Other corner
        '''
        if flag == 1:
            xtile+=0.5
            ytile+=0.5

        if flag ==2:
            xtile+=1
            ytile+=1

        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return [lat_deg, lon_deg]
    
    def check_the_best_zoom_level_through_date(self):
        '''
        Return the best zoom level from the most closest date until the check date
        zoom_level: Uses the Google Maps Tile Coordinates.
        '''
        lat_deg =(self.boundary[0] + self.boundary[2])/2 #42.04508791988566
        lon_deg =(self.boundary[1] + self.boundary[3])/2 #-88.0559192506656
        
        url = 'https://api.nearmap.com/coverage/v2/point/'+str(lon_deg) +',' + str(lat_deg)+'?apikey='+ self.Nearmap_Api_Key +'&limit=1' + '&until=' + self.check_date
        # print(url)
        zoom_request = requests.get(url, verify=True)
        nearmap_meta = zoom_request.json()
        self.image_date = nearmap_meta['surveys'][0]['captureDate']
        # print(nearmap_meta['surveys'])
        
        if self.zoom_level is None:
            # obtain the best scale
            if isinstance(nearmap_meta['surveys'][0]['resources']['tiles'][0]['scale'], int):
                for tile_meta in nearmap_meta['surveys'][0]['resources']['tiles']:
                    if tile_meta['type']=='Vert':
                        zoom_level = tile_meta['scale']
                        break
                    else:
                        zoom_level = tile_meta['scale']
            else:
                zoom_level = 21
            self.zoom_level = zoom_level
        return self.zoom_level, self.image_date

    def parallelize_download_tiles(self, i, j):
        url = 'https://api.nearmap.com/tiles/v3/Vert/'+ str(self.zoom_level)+ '/' + str(i) + '/' + str(j) + '.jpg?apikey=' + self.Nearmap_Api_Key + '&until=' + self.image_date
        # print(url)
        r = requests.get(url, verify=True) # verify=False is necessary due to the security setting in Zscaler; when moving to Azure/production, switch to verify=True
        # bytes to image
        plt_image = Image.open(BytesIO(r.content))

        # transfer to opencv format
        opencvImage = cv2.cvtColor(np.array(plt_image), cv2.COLOR_RGB2BGR)
        return i,j,opencvImage
    
    def multithread_download_tiles(self, i, j):
        url = 'https://api.nearmap.com/tiles/v3/Vert/'+ str(self.zoom_level)+ '/' + str(i) + '/' + str(j) + '.jpg?apikey=' + self.Nearmap_Api_Key + '&until=' + self.image_date
        # print(url)
        r = requests.get(url, verify=True) # verify=False is necessary due to the security setting in Zscaler; when moving to Azure/production, switch to verify=True
        # bytes to image
        plt_image = Image.open(BytesIO(r.content))

        # transfer to opencv format
        self.new_image_multithread[(j-self.y0)*256: (j-self.y0)*256+256, (i-self.x0)*256: (i-self.x0)*256+256, :] = cv2.cvtColor(np.array(plt_image), cv2.COLOR_RGB2BGR)

    
    def lat_lon_to_opencv_image(self):
        '''
        lat_long_coor is boundary(min_long, min_lat, max_long, max_lat)
        
        Return a reconstructe Nearmap tile images. Each tile image is 256*256.
        Based on the lat_long, we compute the number of tiles need to be used.
        
        tile_resource_type:
            The resource type for the requested tiles. The available values are:
            Vert - for vertical imagery
            North - for North panorama imagery
            South - for South panorama imagery
            East - for East panorama imagery
            West - for West panorama imagery
            Note: the tileResourceType values are case sensitive.
        '''
        format = "jpg"
        tile_resource_type = "Vert"
 
        # Convert lat, lon and zoom to x,y,z
        x0, y1 = self.lat_lon_to_tile_coords(lat_deg = self.boundary[0], lon_deg=self.boundary[1], zoom= self.zoom_level)
        x1, y0 = self.lat_lon_to_tile_coords(lat_deg = self.boundary[2], lon_deg=self.boundary[3], zoom= self.zoom_level)
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1
        self.y0 = y0
        logging.info(f"x:{x0},y:{y1}")
        logging.info(f"x:{x1},y:{y0}")
        self.nw_lat_long = self.tile_coords_to_lat_lon(x0,y0,self.zoom_level, flag=0)
        self.se_lat_long = self.tile_coords_to_lat_lon(x1,y1,self.zoom_level, flag=2)  

        self.new_image_multithread = np.zeros((256*(y1-y0+1),256*(x1-x0+1),3), np.uint8)
        with futures.ThreadPoolExecutor(max_workers=100) as executor:
            task_list = [executor.submit(self.multithread_download_tiles, i, j) for i in range(x0,x1+1) for j in range(y0,y1+1)]

        return self.new_image_multithread
    
    def boundary2image(self):
        zoom, date = self.check_the_best_zoom_level_through_date()
        full_image = self.lat_lon_to_opencv_image()
        return full_image, zoom, date

### Functions for ground sample distance computation  ###  
def pixels_to_meters(latitude=40, zoom_level=21):
    equatorial_circumference = 2 * math.pi * 6378137
    meter_per_pixels = equatorial_circumference * math.cos(math.radians(latitude)) / math.pow(2,zoom_level+8)
    return meter_per_pixels

def image_download(input_address):
    excel_file_path = 'roof_score_new_20230101.csv'
    image_folder_name = os.path.splitext(os.path.basename(excel_file_path))[0]
    demoFolder = image_folder_name
    # make a image folder by excel name
    if not(os.path.isdir(image_folder_name)):
        os.makedirs(image_folder_name)
    else:
        shutil.rmtree(image_folder_name)
        os.makedirs(image_folder_name)
        

    # load the excel file
    excel_file = pd.read_csv(excel_file_path)
    # updating address value
    excel_file.loc[0, 'location_Address'] = input_address
    excel_file.to_csv(excel_file_path, index=False)

    full_address = excel_file["location_Address"].tolist()
    insured_name = excel_file["InsuredName"].tolist()
    policy_expiration_date = excel_file["PolicyExpirationDate"].tolist()
    Today_date = datetime.today().strftime('%Y-%m-%d')
    
    # go through each address name
    image_name_list = []
    csv_image_boundary = []
    csv_image_info = []
    csv_image_level = []
    csv_image_date = []
    csv_gsd = []
    # output_address = []
    for i in range(len(full_address)):
        image_text = ''
        address = full_address[i]
        # geocoding
        Ecopia_API = Ecopia_Geocoding(address)
        try:
            address_boundary = Ecopia_API.address2boundary_lat_long_with_buffer()
        except:
            # image_name = address + '_'+ Today_date
            image_name = address
            logging.info(f'index:{i}, address:{address}')
            image_text += 'The Ecopia Geocoding is not avaliable.'
            logging.info(image_text)
            image_name_list.append(image_name)
            csv_image_boundary.append('')
            csv_image_info.append(image_text)
            csv_image_level.append('')
            csv_image_date.append('')
            csv_gsd.append('')
            continue
        if address_boundary == []:
            # image_name = address + '_'+ Today_date
            image_name = address
            logging.info(f'index:{i}, address:{address}')
            image_text += 'Ecopia Geocoding is not accurate.'
            logging.info(image_text)
            image_name_list.append(image_name)
            csv_image_boundary.append('')
            csv_image_info.append(image_text)
            csv_image_level.append('')
            csv_image_date.append('')
            csv_gsd.append('')
            continue

        # image acquire
        check_date = Today_date

        # zoom level 21 is better than others because the training set almost all level21
        Nearmap_API = Nearmap_Image(address_boundary,zoom_level=21, date=check_date)
        try:
            # 0	1.0	111 km
            # 1	0.1	11.1 km
            # 2	0.01	1.11 km
            # 3	0.001	111 m
            # 4	0.0001	11.1 m
            # 5	0.00001	1.11 m
            # 6	0.000001	0.111 m
            # 7	0.0000001	1.11 cm
            # 8	0.00000001	1.11 mm
            if address_boundary[2] - address_boundary[0] > 0.003 or address_boundary[3] - address_boundary[1] > 0.003:
                # image_name = address + '_'+ Today_date
                image_name = address
                logging.info(f'index:{i}, address:{address}')
                image_text += f'image is too big {address_boundary}. Human check!'
                logging.info(image_text)
                image_name_list.append(image_name)
                csv_image_boundary.append(address_boundary)
                csv_image_info.append(image_text)
                csv_image_level.append('')
                csv_image_date.append('')
                csv_gsd.append('')
                continue

            image, zoom_level, date = Nearmap_API.boundary2image()
            # image_name = address + '_' + str(zoom_level)+ '_'+ date
            image_name = address
            logging.info(f'index:{i}, address:{address}')
            image_text = image_text + f'[{Nearmap_API.x0}, {Nearmap_API.y1}, {Nearmap_API.x1}, {Nearmap_API.y0}]'
            logging.info(image_text)
            cv2.imwrite(os.path.join(image_folder_name, image_name) + '.jpg', image)
            image_name_list.append(image_name)
            csv_image_boundary.append(address_boundary)
            csv_image_info.append(image_text)
            csv_image_level.append(int(zoom_level))
            csv_image_date.append(date)
            gsd = pixels_to_meters(latitude = (address_boundary[2] + address_boundary[0])/2, zoom_level = zoom_level)
            csv_gsd.append(gsd)
            continue
            
        # # image = np.zeros((100,100,3), np.uint8) 
        except:
            logging.info(f'index:{i}, address:{address}')
            # image_name = address + '_'+ Today_date
            image_name = address
            image_text += 'Nearmap image is not available here.'
            logging.info(image_text)
            image_name_list.append(image_name)
            csv_image_boundary.append(address_boundary)
            csv_image_info.append(image_text)
            csv_image_level.append('')
            csv_image_date.append('') 
            csv_gsd.append('')
    # logging.info(image_name_list)
    # logging.info(insured_name)
    # logging.info(policy_expiration_date)
    # logging.info(csv_image_date)
    # logging.info(csv_image_level)
    # logging.info(csv_image_boundary)
    # logging.info(csv_image_info)
    # logging.info(csv_gsd)
    out_csv = pd.DataFrame({'Address':image_name_list,
                            'InsuredName':insured_name,
                            'PolicyExpirationDate':policy_expiration_date,
                            'Image date': csv_image_date,
                            'Image level': csv_image_level,
                            'Image boundary': csv_image_boundary,
                            'Image info': csv_image_info,
                            'Image gsd (meters/pixels)': csv_gsd})
    out_csv.to_csv(os.path.join(image_folder_name,'image.csv'), index=False, header=True) 
