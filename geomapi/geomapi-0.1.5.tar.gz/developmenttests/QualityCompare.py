# %% [markdown]
# ## Import needed modules and packages
# 

# %%
#import the geomapi package
import importlib
import numpy as np 

import os
import ifcopenshell
import ifcopenshell.geom as geom
import open3d as o3d

from context import geomapi
import geomapi.linkeddatatools as ld
import geomapi.validationtools as val
import geomapi.geometryutils as geo1

import time
import copy
import math
from scipy.spatial.transform import Rotation as R
from PIL import Image, ImageDraw
import shutil

# %% [markdown]
# ## Set needed global parameters

# %%
#INPUT parameters

def main(current_values):
    projectPath = current_values['projectPath']
    ifcPath = current_values['ifcPath']

    pcdPath = current_values['pcdPath']

    outputPath = current_values['outputPath']


    saveMeshes = current_values['saveMeshes']
    saveMeshPcd = current_values['saveMeshPcd']
    saveCroppedPcd = current_values['saveCroppedPcd']
    saveFilteredPcd = current_values['saveFilteredPcd']

    saveCSV = current_values['saveCSV']
    saveExcel = current_values['saveExcel']
    saveColloredBIM = current_values['saveColloredBIM']
    saveColloredPcd = current_values['saveColloredPcd']
    #PARAMETER ADDED
    saveReports = True
    saveResultPcd = True

    resolution = current_values['resolution']

    

    #AVANCED
    key = [('Wall', ["IfcWall", "IfcWindow","IfcDoor"]), ('Column', ["IfcColumn"] ), ('Beam', ["IfcBeam"]), ('Slab', ["IfcSlab","IfcCovering"]), ('Roof', ['IfcRoof']), ('Clutter', [])]
    tempPath = None

    t30 = 0.015 #LOA30 Treshold
    t20 = 0.05 #LOA20 Treshold
    t10 = 0.1 #LOA10 Treshold
    t00 =1 #Total distance treshold
    abs = True # use absolute values for percentages

    distanceTreshold = 0.1 #distance trechold for filtering
    searchRadius=0.1 #Seach radius treshold for normal matching
    dotTreshold = 0.8 #treshhold for normal matching 

    p10 = 0.68 #cumulative percentage treshold LOA10
    p20 = 0.68 #cumulative percentage treshold LOA20
    p30 = 0.68 #cumulative percentage treshold LOA30

    nodelist = []
    storeynodelist = []
    bimnodelist = []
    meshpcdnodelist = []
    pointcloudnodelist = []
    croppedpcdnodelist = []
    filteredpcdnodelist = []



    if not tempPath:
        projectProcessingPath = os.path.join(projectPath, "PROCESSING")
    else:
        projectProcessingPath = tempPath

    if not os.path.isdir(projectProcessingPath): #check if the folder exists
        os.mkdir(projectProcessingPath)


    meshProcessingPath = os.path.join(projectProcessingPath, "MESH")
    if not os.path.isdir(meshProcessingPath):
        os.mkdir(meshProcessingPath)

    meshPcdProcessingPath = os.path.join(projectProcessingPath, "MESHPCD")
    if not os.path.isdir(meshProcessingPath):
        os.mkdir(meshProcessingPath)

    croppedPcdProcessingPath = os.path.join(projectProcessingPath, 'CROPPEDPCD')
    if not os.path.isdir(croppedPcdProcessingPath):
        os.mkdir(croppedPcdProcessingPath)

    filteredPcdProcessingPath = os.path.join(projectProcessingPath, 'FILTEREDPCD')
    if not os.path.isdir(filteredPcdProcessingPath):
        os.mkdir(filteredPcdProcessingPath)

    if not outputPath:
        projectResultsPath = os.path.join(projectPath, "RESULTS")
    else:
        projectResultsPath = outputPath

    if not os.path.isdir(projectResultsPath): #check if the folder exists
        os.mkdir(projectResultsPath)

    resultsName = "session_" + time.strftime("%Y%m%d-%H%M%S")
    resultsPath = os.path.join(projectResultsPath, resultsName)
    if not os.path.exists(resultsPath):
        os.makedirs(resultsPath)

    if not ifcPath:
        ifcPath = os.path.join(projectPath, "MODELS") #Construct the data Modelsfolder path
        if os.path.isdir(ifcPath): #Check if the folder exists
            ifc2x3Path = os.path.join(ifcPath, "IFC2x3") #Construct the IFC2x3 folder path
            if os.path.isdir(ifc2x3Path): #check if ther is an IFC2x3 folder present in the project
                content_ifc_dir = os.listdir(ifc2x3Path) #get the content of the folder
                if len(content_ifc_dir) > 0: #check if the folder is not empty
                    #Loop over all IFC files in the current directory
                    ifcFiles = []
                    for ifcfile in content_ifc_dir: #for every ifc model in the folder
                        
                        if ifcfile.endswith(".ifc"):
                            ifcFiles.append(ifcfile)
                        else:
                            print("ERROR: Select an IFC file")
                    if len(ifcFiles) > 1:
                        print("ERROR: Specify one IFC file to be processed")
                    else:
                        ifcPath = os.path.join(ifc2x3Path, ifcFiles[0])
                        print("Using IFC file: %s" % ifcPath)
                else:
                    print("ERROR: Selected Directory is empty %s" % ifc2x3Path)
            else:
                print("ERROR: No such directory %s" % ifc2x3Path)
        else:
            print("ERROR: No such directory %s" % ifcPath)
    else:
        if ifcPath.endswith(".ifc"):
            print("Using IFC file: %s" % ifcPath)
        else:
            print("ERROR: Select an IFC file")


    if pcdPath:
        
        if os.path.isdir(pcdPath):
            dir = pcdPath
            print("All pointclouds in %s will be processed" %dir)
            pcds = os.listdir(dir)
            if len(pcds) > 0:
                pcdPath = []
                for pcd in pcds:
                    pcdPath.append(os.path.join(dir,pcd))

        elif os.path.isfile(pcdPath):
            if pcdPath.endswith(".pcd") or pcdPath.endswith(".pts"):
                print("Pointcloud %s will be processed" % pcdPath)
                pcdPath = [pcdPath]
            else:
                print("ERROR: only PCD and PTS format are currently supported")
        else:
            print("ERROR: Please provide an existing path")
        
    else:
        dataPath = os.path.join(projectPath, "DATA")
        if os.path.exists(dataPath):
            pcdPath = os.path.join(dataPath, "PCD")
            if os.path.exists(pcdPath):
                dir = pcdPath
                print("All pointclouds in %s will be processed" %dir)
                pcds = os.listdir(dir)
                if len(pcds) > 0:
                    pcdPath = []
                    for pcd in pcds:
                        if pcd.endswith(".pcd"):
                            pcdPath.append(os.path.join(dir,pcd))
                    if not len(pcdPath) > 0:
                        print("ERROR: No PCD Files found")
                        ptsPath = os.path.join(dataPath, "PTS")
                        if os.path.exists(ptsPath):
                            dir = ptsPath
                            print("All pointclouds in %s will be processed" %dir)
                            pcds = os.listdir(dir)
                            if len(pcds) > 0:
                                pcdPath = []
                                for pcd in pcds:
                                    if pcd.endswith(".pts"):
                                        pcdPath.append(os.path.join(dir,pcd))
                                if not len(pcdPath) > 0:
                                    print("ERROR: No PTS Files found")
            else:
                ptsPath = os.path.join(dataPath, "PTS")
                if os.path.exists(ptsPath):
                    dir = ptsPath
                    print("All pointclouds in %s will be processed" %dir)
                    pcds = os.listdir(dir)
                    if len(pcds) > 0:
                        pcdPath = []
                        for pcd in pcds:
                            if pcd.endswith(".pts"):
                                pcdPath.append(os.path.join(dir,pcd))
                        if not len(pcdPath) > 0:
                            print("ERROR: No PTS Files found")
        else:
            print("ERROR: Provide a pointcloud")
            
    print(pcdPath)

    # %% [markdown]
    # Additional settings to export the results to excel or csv

    # %%
    #CSV

    if saveCSV:
        import csv

        csvFilename = "LOA_Report.csv"
        csvPath = os.path.join(resultsPath, csvFilename)
        header = ['Name','Id', 'Class','LOA', 'LOA10', 'LOA20', 'LOA30']
        csvFile = open(csvPath, 'w')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(header)

    if saveExcel:
        import xlsxwriter

        xlsxFilename = "LOA_Report.xlsx"
        xlsxPath = os.path.join(resultsPath, xlsxFilename)
        workbook = xlsxwriter.Workbook(xlsxPath)
        worksheet = workbook.add_worksheet()
        worksheet.write(0,0,'Name')
        worksheet.write(0,1,'Id')
        worksheet.write(0,2,'Class')
        worksheet.write(0,3,'LOA')
        worksheet.write(0,4, 'LOA10')
        worksheet.write(0,5, 'LOA20')
        worksheet.write(0,6, 'LOA30')
        row = 1


    # %% [markdown]
    # ## Create the nodes
    # 
    # Session node

    # %%
    #SESSiONNODE

    #Derive al other parameters such as paths
    projectString = projectPath.split("\\")[-1] #Split the relevant last part of the path off to extract project infomation
    projectId = projectString.split("-")[0] + "-" + projectString.split("-")[1] #Get the project number existing of 2 numbers split by a "-"
    projectType = projectString.split("-")[2] #Get the type of project
    projectName = projectString.split("-")[3] #Get the project name

    sessionnode=geomapi.node.Node()
    nodelist.append(sessionnode)
    sessionnode.name= projectName
    sessionnode.projectNumber = projectId
    sessionnode.projectType = projectType
    sessionnode.path = projectPath

    # %% [markdown]
    # BIM nodes

    # %%
    #BIMNODE & MESHPCDNODE

    prct_count = 5


    ifc = ifcopenshell.open(ifcPath) #read the ifc file

    if ifc.schema == 'IFC2X3':
        products = ifc.by_type("IfcProduct") #Get all elements from the model
        i=0
        print("FOUND %s BIM objects" %len(products))
        level = 0
        
        for ifc_storey in ifc.by_type("IfcBuildingStorey"):
            # print(str(ifc_storey.Name))
            #Create a folder to store al ellements refering to a storey
            storeyPath = os.path.join(meshProcessingPath, ifc_storey.Name)
            if not os.path.exists(storeyPath):
                os.mkdir(storeyPath)

            storeynode=geomapi.node.Node()
            nodelist.append(storeynode)
            storeynode.name= ifc_storey.Name
            storeynode.path = storeyPath

            storeynodelist.append(storeynode)
            bimnodelist.append([])
            meshpcdnodelist.append([])
            pointcloudnodelist.append([])
            croppedpcdnodelist.append([])
            filteredpcdnodelist.append([])
            
            for reference in ifc.get_inverse(ifc_storey):
                if reference.is_a("IfcRelContainedInSpatialStructure"):
                    # print(reference)
                    # print(reference.RelatedElements)
                    for product in reference.RelatedElements:
                        if product.is_a("IfcProduct"):         
                            # Loop over al IfcProducts
                            # for product in products:    #Loop over all the products found in the model
                            #     #Only proceed when the IfcProduct contains an actual geometry representation
                                    
                            # for reference in ifc.get_inverse(product):
                            #     if reference.is_a("IfcBuildingStorey"):
                            #         print(reference.Name)
                            if not product.get_info().get("Representation") == None and not "nulpunt" in product.Name: #Check if the product has a geometry representation
                                # try:
                                    # If a geometry is present, A BIMNode will be created
                                        bimnode=geomapi.bimnode.BIMNode()
                                        bimnode.ifcPath = ifcPath
                                        bimnode.globalId = product.GlobalId
                                        print(product.Name)
                                                    
                                        #Assign the correct class to the BIM element according to the key provided                    
                                        found = False #Initialize a found attribute to stop the following search when a result has been found
                                        while not found:
                                            for segmentationclass in key: #search the segmentation class that contains the ifc element
                                                for ifcclass in segmentationclass[1]:
                                                    #Check if the ifc element is part of one of the classes attatched to the segmentation class
                                                    if product.is_a(ifcclass): #If a the ifc class corresponding to the element is part of a segmentation class both the segmentation class and the ifc class are assigned to the element.
                                                        bimnode.label = segmentationclass[0]
                                                        bimnode.className = ifcclass
                                                        found = True
                                            if not found: #if no match has been found
                                                key[-1][1].append(product.is_a())
                                                
                                                bimnode.label = key[-1][0] #The object has segmentation class Clutter
                                                bimnode.className = product.is_a()#The ifc class is added to the list of clutter, this enables the possibility to check which classes are labeled as clutter
                                                found = True
                                        bimnode.name = bimnode.label + "-" + bimnode.globalId #crteate a name for the modelelement containing the class and the object iD

                                        #If no meshgeometry of the element is already present, create one from the ifc
                                        meshFilename = bimnode.name + "-MESH.ply" #construct the filename for the obj file
                                        bimnode.meshPath = os.path.join(storeyPath, meshFilename) #construct the path of the obj file
                                        if not os.path.exists(bimnode.meshPath):
                                            bimnode.mesh = geo1.ifc_to_mesh(product)
                                            if bimnode.mesh:
                                                o3d.io.write_triangle_mesh(bimnode.meshPath,bimnode.mesh)
                                        else:
                                            bimnode.mesh = o3d.io.read_triangle_mesh(bimnode.meshPath)
                                        bimnode.sessionPath = (projectPath)
                                        bimnode.get_metadata_from_mesh()
                                        bimnodelist[level].append(bimnode)

                                        #If there is no sampled pointcloud of the mesh available, sample one from the provided mesh
                                        mechpcdFilename= bimnode.name + "-MESHPCD.pcd" #construct the filename for the obj file
                                        meshpcdFilePath = os.path.join(storeyPath, mechpcdFilename)
                                        if not os.path.exists(meshpcdFilePath):
                                            MeshpcdNode = val.create_meshpcd(element=bimnode, path=meshpcdFilePath, sampleSize=resolution)
                                        else:
                                            MeshpcdNode = geomapi.pointcloudnode.PointCloudNode()
                                            MeshpcdNode.pcd = o3d.io.read_point_cloud(meshpcdFilePath)
                                            MeshpcdNode.get_metadata_from_pcd()
                                            MeshpcdNode.name = bimnode.name + "-MESHPCD"
                                            MeshpcdNode.sensor = "Sampled"
                                            MeshpcdNode.path = meshpcdFilePath

                                        meshpcdnodelist[level].append(MeshpcdNode)
                                        croppedpcdnodelist[level].append(None)
                                        filteredpcdnodelist[level].append(None)

                                        #All computations on the mesh geometry are done so the mesh geometry itself can be exposed, when needed the mesh can be loaded from the path.
                                        bimnode.mesh = None
                                        bimnode.Done = False
                                # except:
                                #     print("FAILED TO CREATE A MESH REPRESENTATION")
                                        
                            prct = i/len(products)*100
                            if prct > prct_count:
                                print("PROGRES: %s %%" % np.round(prct))
                                prct_count += 5
                            i +=1
            level += 1
    else:
        print("ERROR: Please provide an IFC2X3 file not %s" % ifc.schema)
    print("PROGRES: 100.0 %%")
    print("SUCCESFULLY CONVERTED BIM TO MESHES AND POINTCLOUDS FOR %s ELEMENTS" % len(bimnodelist))

    # %%
    ERROR = False
    if len(storeynodelist) == len(bimnodelist) == len(meshpcdnodelist):
        print("LEVELS OK")
    else:
        print("Number of levels %s / %s / %s" %(len(storeynodelist), len(bimnodelist),len(meshpcdnodelist)))
        ERROR = True
    levelindex = 0
    for level in storeynodelist:
        print(level.name)
        if len(bimnodelist[levelindex]) == len(meshpcdnodelist[levelindex]):
            print("ELEMENTS OKE")
        else:
            print("Number of elements %s / %s" %(len(bimnodelist[levelindex]),len(meshpcdnodelist[levelindex])))
            ERROR = True
        levelindex += 1

    if ERROR:
        print("ERROR: Something went wrong")
    else:
        print("ALL OK")

    # %%
    if saveReports:
        levelindex = 0
        while levelindex < len(storeynodelist):
            elementindex = 0
            storey = storeynodelist[levelindex]

            #Determine bounding box of the enitre floor
            points = []      
            for element in bimnodelist[levelindex]:
                try:
                    box = np.asarray(geo1.get_bounding_points(element.cartesianBounds))
                except:
                    print("ERROR")
                for point in box:
                    points.append(point)

            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points)
            # print(pcd)
            bbbox = pcd.get_oriented_bounding_box()
            #Create images
            imageResultDirectory = os.path.join(resultsPath, "IMAGES")
            if not os.path.isdir(imageResultDirectory):
                os.mkdir(imageResultDirectory)
            
                
            fov = np.pi / 3 #60 #degrees
                
            #determine extrinsic camera parameters
            extrinsic = np.empty((1,3), dtype=float)
        
            c = bbbox.get_center()
            u = bbbox.extent[0]
            d_w = math.cos(fov/2)*u

            #determine c_i
            rotation_matrix = bbbox.R
            pcd2 = o3d.geometry.PointCloud()
            array = np.array([[c[0],c[1],c[2]+d_w]])
            pcd2.points = o3d.utility.Vector3dVector(array)
            c_i = np.asarray(pcd2.points[0])

            #generate scene
            width = 640
            height = 480
            render = o3d.visualization.rendering.OffscreenRenderer(width,height)

            #Create different materials for visualization
            mtl = o3d.visualization.rendering.MaterialRecord()
            mtl.base_color = [1.0, 1.0, 1.0, 0.5]  # RGBA
            mtl.shader = "defaultUnlit"

            mtlhighlight = o3d.visualization.rendering.MaterialRecord()
            mtlhighlight.base_color = [1.0, 0.0, 0.0, 1.0]  # RGBA
            mtlhighlight.shader = "defaultUnlit"

            mtlline = o3d.visualization.rendering.MaterialRecord()
            mtlline.base_color = [0.0, 0.0, 0.0, 0.2]  # RGBA
            mtlline.shader = "defaultUnlit"

            #set camera
            # Look at the origin from the front (along the -Z direction, into the screen), with Y as Up.
            center = c  # look_at target
            eye = c_i  # camera position
            up = [0, 0, 1]  # camera orientation
            render.scene.camera.look_at(center, eye, up)
            
            #add geometries
            #Geometries for the overview
            for element in bimnodelist[levelindex]:
                if not element.mesh:
                    element.get_geometry()
                if element.mesh:
                    render.scene.add_geometry(element.name,element.mesh,mtl)
                    
                    #Add the wireframes to the image
                    wireframe = o3d.geometry.LineSet.create_from_triangle_mesh(element.mesh)
                    wireframeName = "lines" + element.name
                    render.scene.add_geometry(wireframeName, wireframe, mtlline)

            #Highligth each element and save a seperate picture of it       
            for element in bimnodelist[levelindex]:
                if element.mesh:

                    #Determine path to save the created image
                    overviewImageResultName = storey.name + "_" + element.name
                    overviewImageResultFileName = overviewImageResultName + ".png"
                    overviewImageResultPath = os.path.join(imageResultDirectory, overviewImageResultFileName)
                    
                    mtlhighlight = o3d.visualization.rendering.MaterialRecord()
                    mtlhighlight.base_color = [1.0, 0.0, 0.0, 1.0]  # RGBA
                    mtlhighlight.shader = "defaultUnlit"
                    
                    #Change the appearence of the focused mesh
                    render.scene.modify_geometry_material(element.name, mtlhighlight)

                    boundingbox = geo1.oriented_bounds_to_open3d_oriented_bounding_box(element.orientedBounds)
                    expandedBoundingbox = geo1.expand_box(boundingbox,  u=1,v=1, w=1)
                    boundingboxWireframe = o3d.geometry.LineSet.create_from_oriented_bounding_box(expandedBoundingbox)
                    boundingboxName = "bb" + element.name
                    render.scene.add_geometry(boundingboxName, boundingboxWireframe, mtlhighlight)
                    render.scene.modify_geometry_material(boundingboxName, mtlhighlight)


                    #Take the image
                    img = render.render_to_image()
                    o3d.io.write_image(overviewImageResultPath, img)

                    #Change back the appearnence of the mesh to the initial settings
                    render.scene.modify_geometry_material(element.name, mtl)
                    render.scene.remove_geometry(boundingboxName)            
                
            levelindex += 1
            
    # %%
    for pointcloud in pcdPath:
        #Extract all needed information of the point cloud object
        pointcloudnode = geomapi.pointcloudnode.PointCloudNode()
        nodelist.append(pointcloudnode)
        pointcloudnode.path = pointcloud
        pointcloudnode.name = pointcloud.split(".")[0]
        pointcloudnode.get_pcd()
        pointcloudnode.get_metadata_from_pcd()
        pointcloudnodelist.append(pointcloudnode)
        print(pointcloudnode.name)
        for storey in storeynodelist:
            levelindex = 0
            while levelindex < len(storeynodelist):
                elementindex = 0
                storey = storeynodelist[levelindex]  
                if storey:

                    #Determine the products needed for further processing are stored
                    croppedPcdStoreyPath = os.path.join(croppedPcdProcessingPath, storey.name)
                    if not os.path.isdir(croppedPcdStoreyPath):
                        os.mkdir(croppedPcdStoreyPath)
                
                    filteredPcdStoreyPath = os.path.join(filteredPcdProcessingPath, storey.name)
                    if not os.path.isdir(filteredPcdStoreyPath):
                        os.mkdir(filteredPcdStoreyPath)
                    
                    
                    #process all the objects of a floor 
                    while elementindex < len(bimnodelist[levelindex]):
                        bimnode = bimnodelist[levelindex][elementindex]
                        meshpcdnode = meshpcdnodelist[levelindex][elementindex]
                        if meshpcdnode:
                            #Extract the bounds of the BIM object
                            bimOrientedBoundingBox = geo1.oriented_bounds_to_open3d_oriented_bounding_box(bimnode.orientedBounds)
                            #determine a region around the object to be cropped from the point cloud
                            expandedBimOrientedBoundingBox = geo1.expand_box(bimOrientedBoundingBox,  u=0.2,v=0.2, w=0)
                            pcdOrientedBoundingBox = o3d.geometry.OrientedBoundingBox.create_from_points(geo1.get_bounding_points(pointcloudnode.cartesianBounds))

                            #Check if the acquired boundingbox fals within the pointcloud
                            if not bimnode.Done and len(pcdOrientedBoundingBox.get_point_indices_within_bounding_box(expandedBimOrientedBoundingBox.get_box_points())) > 0:

                                #If it fals completly inside the point cloud boundingbox the objext should not be prcessed for other point clouds
                                if len(pcdOrientedBoundingBox.get_point_indices_within_bounding_box(expandedBimOrientedBoundingBox.get_box_points())) == 8:
                                    bimnode.Done = True
                                cropped = False
                                Filtered = False

                                #Determine the location toi store the intermediate results of the computations        
                                croppedpcd=  bimnode.name + "-CROPPEDPCD.pcd" #construct the filename for the obj file
                                croppedpcdFilePath = os.path.join(croppedPcdStoreyPath, croppedpcd) #construct the path of the obj file
                                CroppedpcdNode = None
                                print("CROPING: %s" %bimnode.name)

                                #If there already is a cropped point cloud for this element, the new part must be added to the already existing part
                                if croppedpcdnodelist[levelindex][elementindex]:
                                    existingCroppedpcdNode = croppedpcdnodelist[levelindex][elementindex]
                                    CroppedpcdNode = val.create_croppedpcd(element= bimnode, target = pointcloudnode, path = None, sampleSize=resolution)
                                    existingCroppedpcdNode.get_pcd()
                                    existingCroppedpcdNode.pcd.__iadd__(CroppedpcdNode.pcd)
                                    print("MERGED TWO CROPPED CLOUDS")
                                    existingCroppedpcdNode.pcd.voxel_down_sample(resolution)
                                    CroppedpcdNode = existingCroppedpcdNode
                                    o3d.io.write_point_cloud(CroppedpcdNode.path, CroppedpcdNode.pcd)

                                #If there is a cropped point cloud for this elment already available from previous processings, it can beloaded from memory instead of creating a new one    
                                elif os.path.exists(croppedpcdFilePath):
                                    CroppedpcdNode = geomapi.pointcloudnode.PointCloudNode()
                                    CroppedpcdNode.pcd = o3d.io.read_point_cloud(croppedpcdFilePath)
                                    print("LOADED CROPPED CLOUD FROM MEMORY")
                                    CroppedpcdNode.name = bimnode.name + "-CROPPEDPCD"
                                    CroppedpcdNode.get_metadata_from_pcd()
                                    # CroppedpcdNode.sensor = "Cropped"
                                    CroppedpcdNode.path = croppedpcdFilePath
                                
                                #If non of the above, a completly new cropped pointcloud will be created and stored
                                else:
                                    CroppedpcdNode = val.create_croppedpcd(element= bimnode, target = pointcloudnode, path = croppedpcdFilePath, sampleSize=resolution)
                                        
                                if CroppedpcdNode:
                                    #Store the cropped pointcloud in a list so is the boundingbox does not fall completly inside the current pointcloud, missing parts can be added when processing other adjacent point clouds
                                    croppedpcdnodelist[levelindex][elementindex] = CroppedpcdNode
                                                
                                    print("SUCCESFULLY CROPPED %s A POINTCLOUD" %bimnode.name)

                                    filteredpcd=  bimnode.name + "-FILTERED.pcd" #construct the filename for the obj file
                                    filteredpcdFilePath = os.path.join(filteredPcdStoreyPath, filteredpcd) #construct the path of the obj file
                                    FilteredpcdNode = None

                                    print("FILTERING: %s" %bimnode.name)

                                    if filteredpcdnodelist[levelindex][elementindex]:
                                        existingFilteredpcdNode = filteredpcdnodelist[levelindex][elementindex]
                                        FilteredpcdNode = val.filter_pointcloud(target = CroppedpcdNode, reference = meshpcdnode, path = None, normals=True)
                                        existingFilteredpcdNode.get_pcd()
                                        existingFilteredpcdNode.pcd.__iadd__(FilteredpcdNode.pcd)
                                        print("MERGED TWO FILTERED CLOUDS")
                                        existingFilteredpcdNode.pcd.voxel_down_sample(resolution)
                                        FilteredpcdNode = existingFilteredpcdNode
                                        o3d.io.write_point_cloud(FilteredpcdNode.path, FilteredpcdNode.pcd)

                                    elif os.path.exists(filteredpcdFilePath):
                                        FilteredpcdNode = geomapi.pointcloudnode.PointCloudNode()
                                        FilteredpcdNode.pcd = o3d.io.read_point_cloud(filteredpcdFilePath)
                                        print("LOADED FILTERED CLOUD FROM MEMORY")
                                        FilteredpcdNode.name = meshpcdnode.name.split("-")[0] + "-FILTERED"
                                        FilteredpcdNode.get_metadata_from_pcd()
                                        FilteredpcdNode.path = filteredpcdFilePath
                                    else:
                                        FilteredpcdNode = val.filter_pointcloud(target = CroppedpcdNode, reference = meshpcdnode, path = filteredpcdFilePath, normals=True)

                                    if FilteredpcdNode:        
                                        CroppedpcdNode.pcd = None
                                        filteredpcdnodelist[levelindex][elementindex] = FilteredpcdNode
                                        print("SUCCESFULLY FILTERED THE CROPPED POINTCLOUD OF %s" %bimnode.name)

                                        #Determine the folder where colored pcds indicating the deviations ca   n be stored
                                        
                                        if saveColloredPcd or saveResultPcd:
                                            pcdResultDirectory = os.path.join(resultsPath, "PCD")
                                            if not os.path.isdir(pcdResultDirectory): #check if the folder exists
                                                os.mkdir(pcdResultDirectory)
                                            pcdResultName = bimnode.name
                                            pcdResultFileName = pcdResultName + ".pcd"
                                            pcdResultPath = os.path.join(pcdResultDirectory, pcdResultFileName)
                                        else:
                                            pcdResultPath = None
                                        
                                        if not saveCSV:
                                            csvWriter = None
                                        
                                        if not saveExcel:
                                            worksheet = None
                                              
                                        #Compute the LOAs of the element
                                        LOAs = val.compute_LOA(FilteredpcdNode.pcd, meshpcdnode.pcd, abs = True, path=pcdResultPath)
                                        #STore the LOAs insied the BIMNode
                                        bimnode.LOAs = LOAs[0]

                                        #Report the LOAs        
                                        val.report_LOAs(bimnode, path=resultsPath, csvWriter = csvWriter, xlsxWorksheet = worksheet, xlsxRow= elementindex+1, p10 = p10, p20 = p20, p30 = p30, mesh = saveColloredBIM)
                                        print("ELEMENT %s ACCURACY: %s" %(bimnode.name, bimnode.accuracy))

                                        if saveReports:
                                            #Create an image of the collored pointcloud indicating the deviations of the object
                                            imageResultDirectory = os.path.join(resultsPath, "IMAGES")
                                            if not os.path.isdir(imageResultDirectory):
                                                os.mkdir(imageResultDirectory)
                                            detailImageResultName = bimnode.name
                                            detailImageResultFileName = detailImageResultName + ".png"
                                            detailImageResultPath = os.path.join(imageResultDirectory, detailImageResultFileName)

                                            fov = np.pi / 3 #60 #degrees

                                            #determine extrinsic camera parameters
                                            extrinsic = np.empty((1,3), dtype=float)
                                            if getattr(bimnode,"orientedBounds",None) is not None:
                                                box=bimnode.get_bounding_box()
                                                c =box.get_center()
                                                u=box.extent[0]

                                                d_w=math.cos(fov/2)*u
                                                #determine c_i
                                                rotation_matrix=box.R
                                                pcd = o3d.geometry.PointCloud()
                                                array=np.array([[c[0],c[1],c[2]+d_w]])
                                                pcd.points = o3d.utility.Vector3dVector(array)
                                                pcd.rotate(rotation_matrix, center =c)
                                                c_i=np.asarray(pcd.points[0])
                                            #generate scene
                                            width=640
                                            height=480
                                            render = o3d.visualization.rendering.OffscreenRenderer(width,height)

                                            #Determine the materials for visualization 
                                            mtl=o3d.visualization.rendering.MaterialRecord()
                                            mtl.base_color = [1.0, 1.0, 1.0, 1.0]  # RGBA
                                            mtl.shader = "defaultUnlit"

                                            mtlline=o3d.visualization.rendering.MaterialRecord()
                                            mtlline.base_color = [0.0, 0.0, 0.0, 0.0]  # RGBA
                                            mtlline.shader = "defaultUnlit"

                                            #set camera
                                            # Look at the origin from the front (along the -Z direction, into the screen), with Y as Up.
                                            center = c  # look_at target
                                            eye = c_i  # camera position
                                            up = [0, 0, 1]  # camera orientation
                                            render.scene.camera.look_at(center, eye, up)
                                            #add geometries
                                            if not bimnode.mesh:
                                                bimnode.get_geometry()

                                            #Add the BIM elements wireframe to the scene to have a bether understanding of the object
                                            wireframe = o3d.geometry.LineSet.create_from_triangle_mesh(bimnode.mesh)
                                            wireframe.paint_uniform_color([0,0,0])
                                            render.scene.add_geometry("test",LOAs[1],mtl)
                                            render.scene.add_geometry("lines", wireframe, mtlline)

                                            #render the image
                                            img = render.render_to_image()
                                            o3d.io.write_image(detailImageResultPath, img)

                                            #Determine the location where the overview image of the object made before is stored and load it to generate the report
                                            overviewImageResultName = storey.name + "_" + bimnode.name
                                            overviewImageResultFileName = overviewImageResultName + ".png"
                                            overviewImageResultPath = os.path.join(imageResultDirectory, overviewImageResultFileName)
                                            
                                            #Load both the detail and overview image of the object
                                            detail = Image.open(detailImageResultPath)
                                            overview = Image.open(overviewImageResultPath)

                                            #determine where the reports can be stored
                                            reportResultDirectory = os.path.join(resultsPath, "REPORTS")
                                            if not os.path.isdir(reportResultDirectory):
                                                os.mkdir(reportResultDirectory)
                                            reportName = bimnode.name
                                            reportFileName = reportName + ".png"
                                            reportPath = os.path.join(reportResultDirectory, reportFileName)


                                            #Create a report in the form of a PNG per BIM element. 
                                            val.create_report(detail, overview, bimnode.name, bimnode.LOAs,p10 = p10, p20 = p20, p30 = p30, project = sessionnode,t30 = t30,t20 = t20,t10 =t10,t00 =t00).save(reportPath)
                                            
                                        

                                    else:
                                        print("FAILED TO FILTER THE POINTCLOUD")
                                        print("NO LOA COMPUTED FOR %s" %bimnode.name)
                                else:
                                    print("NO CROPPED POINTCLOUD CREATED")              

                        elementindex += 1
                levelindex += 1

                    

    # %%
    print("Nodelist: %s" % len(nodelist))
    print("BIMnodelist: %s" % len(bimnodelist))
    print("Meshpcdnodelist: %s" % len(meshpcdnodelist))

    # %%
    if saveCSV:
        csvFile.close()
    if not saveExcel:
        workbook.close()

    if saveResultPcd:
        resultPcd = o3d.geometry.PointCloud()
        pcdfiles = os.listdir(pcdResultDirectory)
        for file in pcdfiles:
            pcd = o3d.io.read_point_cloud(os.path.join(pcdResultDirectory, file))
            resultPcd.__iadd__(pcd)
        resultPcdFileName = "Result.pcd"
        resultpcdFilePath = os.path.join(resultsPath, resultPcdFileName)
        o3d.io.write_point_cloud(resultpcdFilePath, resultPcd)
        if not saveColloredPcd:
            shutil.rmtree(pcdResultPath, ignore_errors=True)

        
            

    if not saveMeshes:
        dir = meshProcessingPath
        shutil.rmtree(dir, ignore_errors=True)
    if not saveMeshPcd:
        dir = meshPcdProcessingPath
        shutil.rmtree(dir, ignore_errors=True)
    if not saveCroppedPcd:
        dir = croppedPcdProcessingPath
        shutil.rmtree(dir, ignore_errors=True)
    if not saveFilteredPcd:
        dir = filteredPcdProcessingPath
        shutil.rmtree(dir, ignore_errors=True)
    if saveReports:
        shutil.rmtree(imageResultDirectory, ignore_errors=True)


    print('Quality compare is finished')


