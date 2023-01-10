from asyncio import as_completed
import multiprocessing
import os.path
from typing import Tuple
import open3d as o3d
import numpy as np
#IMPORT MODULES
from context import geomapi 
from geomapi.nodes import *
import geomapi.utils as ut
from geomapi.utils import geometryutils as gt
from geomapi.tools import linkeddatatools as ld
import pye57 #conda install xerces-c  =>  pip install pye57
import time
import concurrent.futures
from pathlib import Path


def arrays_to_pcd(tuple) -> o3d.geometry.PointCloud:
    """Returns PointCloud from e57 arrays.\n

    tuple (Tuple): pointArray:np.array,colorArray:np.array,normalArray:np.array

    Returns:
        o3d.geometry.PointCloud
    """
        
    pointcloud = o3d.geometry.PointCloud()
    pointcloud.points = o3d.utility.Vector3dVector(tuple[0])
    if tuple[1] is not None:
        pointcloud.colors = o3d.utility.Vector3dVector(tuple[1])
    if tuple[2] is not None:
        pointcloud.normals = o3d.utility.Vector3dVector(tuple[2])
    return pointcloud

def e57_to_arrays(e57Path:str,e57Index : int = 0)->Tuple[np.array,np.array,np.array]:

    e57 = pye57.E57(e57Path)
    header = e57.get_header(e57Index)
    raw_data = e57.read_scan_raw(e57Index)    
    if all(elem in header.point_fields  for elem in ['cartesianX', 'cartesianY', 'cartesianZ']):   
        x_ndarray=raw_data.get('cartesianX')
        y_ndarray=raw_data.get('cartesianY')
        z_ndarray=raw_data.get('cartesianZ')  
        pointArray=np.reshape(np.vstack(( x_ndarray,y_ndarray,z_ndarray)).flatten('F'),(len(x_ndarray),3))
        np.random.choice(pointArray)

    #get color or intensity
    colorArray=None
    if (all(elem in header.point_fields  for elem in ['colorRed', 'colorGreen', 'colorBlue'])
        or 'intensity' in header.point_fields ): 
        
        colorRed=raw_data.get('colorRed')
        colorGreen=raw_data.get('colorGreen')
        colorBlue=raw_data.get('colorBlue')
        intensity=raw_data.get('intensity')

        if colorRed is not None and colorGreen is not None and colorBlue is not None:
            if np.amax(colorRed)<=1:
                colors=np.c_[colorRed , colorGreen,colorBlue ]  
            elif np.amax(colorRed) <=255:
                colors=np.c_[colorRed/255 , colorGreen/255,colorBlue/255 ]  
            else:
                colorRed=(colorRed - np.min(colorRed))/np.ptp(colorRed)
                colorGreen=(colorGreen - np.min(colorGreen))/np.ptp(colorGreen)
                colorBlue=(colorBlue - np.min(colorBlue))/np.ptp(colorBlue)
                colors=np.c_[colorRed , colorGreen,colorBlue ]  
            colorArray=np.reshape(colors.flatten('F'),(len(x_ndarray),3))

        elif intensity is not None:
            if np.amax(intensity) <=1:
                colors=np.c_[intensity , intensity,intensity ]  
            else:
                intensity=(intensity - np.min(intensity))/np.ptp(intensity)
                colors=np.c_[intensity , intensity,intensity ]  
            colorArray=np.reshape(colors,(len(x_ndarray),3))

    #get normals
    normalArray=None
    if all(elem in header.point_fields  for elem in ['nor:normalX', 'nor:normalY', 'nor:normalZ']): 
        nx_ndarray=raw_data.get('nor:normalX')
        ny_ndarray=raw_data.get('nor:normalY')
        nz_ndarray=raw_data.get('nor:normalZ')
        normalArray= np.reshape(np.vstack(( nx_ndarray,ny_ndarray,nz_ndarray)).flatten('F'),(len(x_ndarray),3))
    
    return pointArray,colorArray,normalArray

if __name__ == '__main__':
    
    path= os.path.join(os.getcwd(),"tests",'Samples11')
    
    # e57Path=os.path.join('D:/','Data','2018-06 Werfopvolging Academiestraat Gent','week 22','PCD','week 22 lidar_CC.e57')
    e57Path=os.path.join('C:/','Users','u0094523','Documents','week 22 lidar_CC.e57')
    # "C:\Users\u0094523\Documents\week 22 lidar_CC.e57"
    # e57Path= os.path.join(path,'week 22 lidar_CC.e57' )    
    print(e57Path)
   
    e57 = pye57.E57(e57Path)
    st = time.time()

    # # problem with passing point clouds. can't pickle them
    with concurrent.futures.ProcessPoolExecutor() as executor:
        subsample=0.5
        # results=[executor.submit(e57_to_arrays,e57Path=e57Path,e57Index=s) for s in range(e57.scan_count)]
        results=[executor.submit(e57_to_arrays,e57Path=e57Path,e57Index=s) for s in range(2)]

    
        for r in concurrent.futures.as_completed(results):
            print(len(r.result()[0]))
            pcd=arrays_to_pcd(r.result())
            # print(len(pcd.points))
            

    et = time.time()
    print("import time: "+str(et - st))

    # st = time.time()
    # # array=results[0].result()
    # # print(array[0])
    # # pointcloud = o3d.geometry.PointCloud()
    # # pointcloud.points = o3d.utility.Vector3dVector(array)
    # pcd=arrays_to_pcd(results[0].result())   
    # print(len(pcd.points)) 
    # et = time.time()
    # print("conversion time: "+str(et - st))
