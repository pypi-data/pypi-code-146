



def Mosaic(Path_to_WorkingDir=r"", output_MosaicDir=r"" , img_mode=(0,1)):
    import glob
    from pathlib import Path
    import os
    from glob import glob
    from osgeo import gdal
    import glob

    
    mypath=r"zip_folders"

#5851965_1062413_2022-08-12_24a4_BGRN_SR_clip.tif
#5851965_1062413_2022-08-12_24a4_udm2_clip.tif
    
    Working_Dir=Path_to_WorkingDir
    output_MosaicDir=output_MosaicDir
    if img_mode==1:
        ext="*.tif"
        count_left=16
        count_right=-22
    elif img_mode==0:
        ext="*udm2*.tif"
        count_left=16
        count_right=-19
    else:
        print("""image mode is invalide 
        please enter 1 to process image data or 
        enter 0 to processes UDM2 Mask data""")

    imglist = glob.glob(Working_Dir +"/"+ ext)
    imglist.sort(key=os.path.getctime)
    counter=len(Working_Dir)+1
    if not os.path.exists(Working_Dir):
        os.makedirs(Working_Dir)

    if not os.path.exists(output_MosaicDir):
        os.makedirs(output_MosaicDir)

    outputfolder=output_MosaicDir
    
    for idx, item1 in enumerate( imglist):
        for item2 in imglist[idx+1:]:
            img_similar_datesList=[]
            
            filepath1, filename1 = os.path.split(imglist[idx])
            filepath2, filename2 = os.path.split(imglist[idx+1])
            track_dates1=filename1[count_left:count_right]
            track_dates2=filename2[count_left:count_right]
            print("item1: ", track_dates1 )
            print("item2: ", track_dates2)

            if track_dates1 == (track_dates2):
                #merged_name= dest + "/" + item1[9:]
                img_similar_datesList=[imglist[idx] , imglist[idx+1]]
                merged_name= outputfolder + "/" + str(track_dates1 )  + ".tif"
                print("Mosaic file Name: " , merged_name )
                vrt = gdal.BuildVRT("merged1.vrt", img_similar_datesList)
                gdal.Translate(merged_name, vrt, xRes = 3.125, yRes = -3.125)
                vrt = None  
            elif track_dates1 != track_dates2:
                name= outputfolder + "/" + str(track_dates1 ) + ".tif"
                path_to_file = name
                path = Path(path_to_file)

                if path.is_file():
                    print(f'The file dates {path_to_file} exists and already merged')
                else:
                    print(f'The file {path_to_file} does not exist copied to merged folder')
                    vrt = gdal.BuildVRT("merged2.vrt", [imglist[idx]])
                    gdal.Translate(name, vrt, xRes = 3.125, yRes = -3.125)
                    vrt = None


def rasterClip(rasterpath, aoi, outfilename):
    import geopandas as gpd
    import rioxarray 
    import fiona
    rds1 = rioxarray.open_rasterio(str(rasterpath))
    crop_extent = gpd.read_file(aoi)
    rds1 = rds1.rio.reproject(crop_extent.crs)
    with fiona.open(str(aoi)) as src:
        geom_crs = src.crs_wkt
        geoms = [feature["geometry"] for feature in src]
    raster_clipped = rds1.rio.clip(geoms, geom_crs)
    #raster_clipped = raster_clipped.rio.reproject(raster_clipped.rio.crs, shape=(mask.shape[1], mask.shape[0]), resampling=Resampling.cubic_spline)
    raster_clipped.rio.to_raster(str(outfilename))

def Crop_to_AOI(Path_to_WorkingDir=r'', Path_to_AOI_shapefile=r"", output_CroppedDir=r"" ):
    import os 
    import glob
    from pathlib import Path
    
    if not os.path.exists(output_CroppedDir):
        os.makedirs(output_CroppedDir)
        
    Path_to_WorkingDir=Path_to_WorkingDir
    output_CroppedDir=output_CroppedDir

    cropped_dest=output_CroppedDir
    imglist=glob.glob(Path_to_WorkingDir+ "/"+ '*.tif')
    imglist.sort(key=os.path.getctime)
    Path_to_AOI_shapefile=Path_to_AOI_shapefile
    
    for  idx, item in enumerate(imglist):
        item=imglist[idx]
        filepath1, filename = os.path.split(item)
        name= cropped_dest + '/' + filename
        raster_path=item
        print(name, " index: ", idx)
        path_to_file = name
        path = Path(path_to_file)
        rasterClip(raster_path, Path_to_AOI_shapefile ,name )
        
