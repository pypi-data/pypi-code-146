import copy
import math
import os
from pathlib import Path
import shutil
import time
import unittest
from multiprocessing.sharedctypes import Value

import cv2
import geomapi.utils.geometryutils as gt
import ifcopenshell
import numpy as np
import open3d as o3d
import pye57
import pytest
from ifcopenshell.util.selector import Selector
from rdflib import Graph

 ################################## SETUP/TEARDOWN MODULE ######################

# def setUpModule():
#     #execute once before the module 
#     print('-----------------Setup Module----------------------')

# def tearDownModule():
#     #execute once after the module 
#     print('-----------------TearDown Module----------------------')

class TestGeometryutils(unittest.TestCase):

 ################################## SETUP/TEARDOWN CLASS ######################
  
    @classmethod
    def setUpClass(cls):
        #execute once before all tests
        print('-----------------Setup Class----------------------')
        st = time.time()
        cls.path= Path.cwd() / "test" / "testfiles" 
        
        #POINTCLOUD1
        cls.e57Path1=cls.path / 'PCD' / "week22 photogrammetry - Cloud.e57"     
        #POINTCLOUD2
        cls.e57Path2=cls.path / 'PCD' / "week 22 - Lidar.e57"     
       
        #POINTCLOUD3
        cls.pcdPath1=cls.path / 'PCD' / "academiestraat week 22 a 20.pcd"     
        cls.pcd= o3d.io.read_point_cloud(str(cls.pcdPath1)) 

        #MESH
        cls.meshPath=cls.path / 'MESH' / "week22.obj"  
        cls.mesh= o3d.io.read_triangle_mesh(str(cls.meshPath))
    
        #IMG
        cls.image1Path=cls.path / 'IMG' / "IMG_2173.JPG"  
        cls.image1=cv2.imread(str(cls.image1Path))
        cls.image1CartesianTransform= np.array([[-0.0544245051021791, 0.089782180920334, 0.994473294379276, -8.94782374621677],
                                                [-0.783686718502243, -0.621016494566922, 0.0131772804097903 ,11.2531401937057],
                                                [0.618767404189627, -0.778638345745315, 0.104159618122526, 6.5428452363933],
                                                [0,0,0,1]])
        cls.image2Path=cls.path / 'IMG' / "IMG_2174.JPG"  
        cls.image2=cv2.imread(str(cls.image1Path))
        cls.image2CartesianTransform= np.array([[-0.046509031201878, 0.0485391010476459, 0.99773787423659, -8.63657982153356],
                                                [-0.714937318920729, -0.699188212147553, 0.00068848264200394 ,9.21354145067747],
                                                [0.697639978807912, -0.713288020131696, 0.0672209811405822,6.57082854991429],
                                                [0,0,0,1]])
        #IFC1
        cls.ifcPath1=cls.path / 'IFC' / "Academiestraat_building_1.ifc" 
        cls.classes= '.IfcBeam | .IfcColumn | .IfcWall | .IfcSlab'
        ifc1 = ifcopenshell.open(str(cls.ifcPath1))   
        selector = Selector() 
        cls.bimMeshes=[gt.ifc_to_mesh(ifcElement) for ifcElement in selector.parse(ifc1, cls.classes)]     
        cls.bimBoxes=[mesh.get_oriented_bounding_box() for mesh in cls.bimMeshes if mesh]

        #IFC2
        cls.ifcPath2=cls.path / 'IFC' / "Academiestraat_parking.ifc" 
        ifc2 = ifcopenshell.open(str(cls.ifcPath2))   
        ifcSlab=ifc2.by_guid('2qZtnImXH6Tgdb58DjNlmF')
        ifcWall=ifc2.by_guid('06v1k9ENv8DhGMCvKUuLQV')
        ifcBeam=ifc2.by_guid('05Is7PfoXBjhBcbRTnzewz' )
        ifcColumn=ifc2.by_guid('23JN72MijBOfF91SkLzf3a')
        # ifcWindow=ifc.by_guid(cls.slabGlobalid) 
        # ifcDoor=ifc.by_guid(cls.slabGlobalid)

        cls.slabMesh=gt.ifc_to_mesh(ifcSlab)
        cls.wallMesh=gt.ifc_to_mesh(ifcWall)
        cls.beamMesh=gt.ifc_to_mesh(ifcBeam)
        cls.columnMesh=gt.ifc_to_mesh(ifcColumn)
        # cls.windowMesh=gt.ifc_to_mesh(ifcWindow)
        # cls.doorMesh=gt.ifc_to_mesh(ifcDoor)

        #RESOURCES
        cls.resourcePath=os.path.join(cls.path,"resources")
        if not os.path.exists(cls.resourcePath):
            os.mkdir(cls.resourcePath)
   
        et = time.time()
        print("startup time: "+str(et - st))
        print('{:50s} {:5s} '.format('tests','time'))
        print('------------------------------------------------------')


    @classmethod
    def tearDownClass(cls):
        #execute once after all tests
        print('-----------------TearDown Class----------------------')
        if os.path.exists(cls.resourcePath):
            shutil.rmtree(cls.resourcePath)      

################################## SETUP/TEARDOWN ######################

    def setUp(self):
        #execute before every test
        self.startTime = time.time()   

    def tearDown(self):
        #execute after every test
        t = time.time() - self.startTime
        print('{:50s} {:5s} '.format(self._testMethodName,str(t)))

################################## FIXTURES ######################
    # # @pytest.fixture(scope='module')
    # # @pytest.fixture
    # def test_data(*args):
    #     here = os.path.split(__file__)[0]
    #     return os.path.join(here, "testfiles", *args)

    # @pytest.fixture
    # def e57Path1():
    #     return test_data("pointcloud.e57")

    # @pytest.fixture
    # def ifcData():
    #     ifcPath=os.path.join(os.getcwd(),"testfiles", "ifcfile.ifc")
    #     classes= '.IfcBeam | .IfcColumn | .IfcWall | .IfcSlab'
    #     ifc = ifcopenshell.open(ifcPath)   
    #     selector = Selector()
    #     dataList=[]
    #     for ifcElement in selector.parse(ifc, classes): 
    #         dataList.append(ifcElement)
    #     return dataList

################################## TEST FUNCTIONS ######################

    def test_arrays_to_mesh_and_mesh_to_arrays(self):
        #mesh_to_arrays
        tuple=gt.mesh_to_arrays(self.meshPath)
        self.assertEqual(len(tuple[0]),len(self.mesh.vertices))
        self.assertEqual(len(tuple[1]),len(self.mesh.triangles))
        self.assertEqual(len(tuple[2]),len(self.mesh.vertex_colors))
        self.assertEqual(tuple[3],None)
        self.assertEqual(tuple[4],0)

        #arrays_to_mesh
        mesh=gt.arrays_to_mesh(tuple)
        self.assertEqual(len(mesh.vertices),len(self.mesh.vertices))
        self.assertEqual(len(mesh.triangles),len(self.mesh.triangles))
        self.assertEqual(len(mesh.vertex_colors),len(self.mesh.vertex_colors))

    def test_arrays_to_pcd(self):
        #pcd_to_arrays
        tuple=gt.pcd_to_arrays(self.pcdPath1)
        self.assertEqual(len(tuple[0]),len(self.pcd.points))
        self.assertEqual(len(tuple[1]),len(self.pcd.colors))
        self.assertEqual(tuple[2],None)
        self.assertEqual(tuple[3],0)
     
        #arrays_to_mesh
        pcd=gt.arrays_to_pcd(tuple)
        self.assertEqual(len(pcd.points),len(self.pcd.points))
        self.assertEqual(len(pcd.colors),len(self.pcd.colors))
        self.assertEqual(len(pcd.normals),len(self.pcd.normals))

    def test_create_identity_point_cloud(self):
        # 1 geometry
        identityPointCloud, indentityArray=gt.create_identity_point_cloud(self.slabMesh)
        self.assertEqual(len(identityPointCloud.points),len(indentityArray))

        #multiple geometries
        list=[self.slabMesh, self.wallMesh]
        identityPointCloud2, indentityArray2=gt.create_identity_point_cloud(list)
        self.assertEqual(len(identityPointCloud2.points),len(indentityArray2))

    def test_create_visible_point_cloud_from_meshes(self):
        referenceMesh1= copy.deepcopy(self.slabMesh)
        referenceMesh1.translate([1,0,0])
        referenceMesh2= copy.deepcopy(self.slabMesh)
        referenceMesh2.translate([0,1,0])
        
        # 1 geometry
        identityPointClouds1, percentages1=gt.create_visible_point_cloud_from_meshes(geometries=self.slabMesh,
                                                references=referenceMesh1)
        self.assertEqual(len(identityPointClouds1),1)
        self.assertGreater(len(identityPointClouds1[0].points),10)
        self.assertEqual(len(percentages1),1)        
        self.assertLess(percentages1[0],0.2)

        # multiple geometries 
        list=[self.slabMesh,self.wallMesh]
        references=[referenceMesh1,referenceMesh2]
        identityPointClouds2, percentages2=gt.create_visible_point_cloud_from_meshes(geometries=list,
                                                references=references)
        self.assertEqual(len(identityPointClouds2),2)
        self.assertLess(len(identityPointClouds2[0].points),len(identityPointClouds1[0].points))
        self.assertEqual(len(percentages2),2)        
        self.assertLess(percentages2[0],percentages1[0])
    
        

    def test_cap_mesh(self):
        print('test_cap_mesh NOT IMPLEMENTED')
        self.assertEqual(0,0)
        
    def test_box_to_mesh(self):
        box=o3d.geometry.TriangleMesh.create_box(width=1.0, height=1.0, depth=1.0)
        boundingBox=box.get_oriented_bounding_box()
        mesh =gt.box_to_mesh(boundingBox) 
        self.assertIsInstance(mesh,o3d.geometry.TriangleMesh)
       
    def test_ifc_to_mesh(self):
        ifc = ifcopenshell.open(self.ifcPath1)   
        selector = Selector()
        ifcCounter=0
        meshCounter =0
        for ifcElement in selector.parse(ifc, self.classes): 
            ifcCounter+=1
            mesh=gt.ifc_to_mesh(ifcElement)
            self.assertIsInstance(mesh,o3d.geometry.TriangleMesh)
            if len(mesh.vertices) !=0:
                meshCounter +=1
            if ifcCounter==20:
                break
        self.assertEqual(meshCounter,ifcCounter)
      
    def test_get_oriented_bounding_box(self):     
        #cartesianBounds
        boxGt=self.mesh.get_axis_aligned_bounding_box()
        boxPointsGt=np.asarray(boxGt.get_box_points())
        cartesianBounds=gt.get_cartesian_bounds(self.mesh)
        box=gt.get_oriented_bounding_box(cartesianBounds)
        boxPoints=np.asarray(box.get_box_points())

        for i in range(0,7):
            for j in range(0,2):
                self.assertAlmostEqual(boxPointsGt[i][j],boxPoints[i][j],delta=0.01)

        #orientedBounds
        boxGt=self.mesh.get_oriented_bounding_box()
        boxPointsGt=np.asarray(boxGt.get_box_points())
        box=gt.get_oriented_bounding_box(boxPointsGt)
        boxPoints=np.asarray(box.get_box_points())
        
        for i in range(0,7):
            for j in range(0,2):
                self.assertAlmostEqual(boxPointsGt[i][j],boxPoints[i][j],delta=0.01)

    def test_generate_visual_cone_from_image(self):
        cartesianTransform=np.array([[-4.65090312e-02,  4.85391010e-02,  9.97737874e-01, -8.63657982e+00],
                                    [-7.14937319e-01, -6.99188212e-01,  6.88482642e-04,  9.21354145e+00],
                                    [ 6.97639979e-01, -7.13288020e-01 , 6.72209811e-02,  6.57082855e+00],
                                    [ 0.00000000e+00 , 0.00000000e+00,  0.00000000e+00 , 1.00000000e+00]])
        mesh=gt.generate_visual_cone_from_image(cartesianTransform)
        self.assertIsInstance(mesh,o3d.geometry.TriangleMesh)
      
    def test_get_cartesian_transform(self):
        cartesianBounds=np.array([-1.0,1,-0.5,0.5,-5,-4])       
        translation=np.array([1, 2, 3])
        rotation=np.array([1,0,0,5,2,6,4,7,8])

        #no data
        cartesianTransform=gt.get_cartesian_transform()
        self.assertEqual(cartesianTransform.shape[0],4)
        self.assertEqual(cartesianTransform.shape[1],4)
        self.assertEqual(cartesianTransform[1,1],1)
        self.assertEqual(cartesianTransform[2,3],0)

        #rotation + translation
        cartesianTransform=gt.get_cartesian_transform(rotation=rotation,translation=translation)
        self.assertEqual(cartesianTransform[1,1],2)
        self.assertEqual(cartesianTransform[0,3],1)

        #cartesianBounds
        cartesianTransform=gt.get_cartesian_transform(cartesianBounds=cartesianBounds)
        self.assertEqual(cartesianTransform[1,1],1)
        self.assertEqual(cartesianTransform[2,3],-4.5)
        
    def test_get_oriented_bounds(self):        
        box=self.mesh.get_axis_aligned_bounding_box()
        boxPoints=np.asarray(box.get_box_points())
        cartesianBounds=gt.get_cartesian_bounds(self.mesh)
        boundingPoints=np.asarray(gt.get_oriented_bounds(cartesianBounds)) 

        for i in range(0,7):
            for j in range(0,2):
                self.assertAlmostEqual(boundingPoints[i][j],boxPoints[i][j],delta=0.01)
        
    def test_get_box_inliers(self):
        mesh=self.wallMesh.translate([0,0,3])
        wallBox=mesh.get_oriented_bounding_box()

        wallInliers= gt.get_box_inliers(sourceBox=wallBox, testBoxes=self.bimBoxes) 
        self.assertEqual(len(wallInliers),8)
        
    def test_get_box_intersections(self):
        mesh=self.wallMesh.translate([0,0,3])
        wallBox=mesh.get_oriented_bounding_box()
        wallInliers= gt.get_box_intersections(sourceBox=wallBox, testBoxes=self.bimBoxes)
        self.assertEqual(len(wallInliers),41)
        
    def test_get_cartesian_bounds(self):
        #box
        box=self.mesh.get_oriented_bounding_box()
        minBounds=box.get_min_bound()
        maxBounds=box.get_max_bound()
        cartesianBounds=gt.get_cartesian_bounds(box)
        self.assertEqual(minBounds[0],cartesianBounds[0])
        self.assertEqual(maxBounds[2],cartesianBounds[5])

        #mesh
        cartesianBounds=gt.get_cartesian_bounds(self.mesh)
        minBounds=self.mesh.get_min_bound()
        maxBounds=self.mesh.get_max_bound()
        self.assertEqual(minBounds[0],cartesianBounds[0])
        self.assertEqual(maxBounds[2],cartesianBounds[5])

        #pointcloud
        cartesianBounds=gt.get_cartesian_bounds(self.pcd)
        minBounds=self.pcd.get_min_bound()
        maxBounds=self.pcd.get_max_bound()
        self.assertEqual(minBounds[0],cartesianBounds[0])
        self.assertEqual(maxBounds[2],cartesianBounds[5])
        
    def test_get_triangles_center(self):
        mesh=self.mesh      
        triangleIndices=[0,1,2]    
        centers=gt.get_triangles_center(mesh,triangleIndices)
        self.assertEqual(centers.size,9)
        self.assertAlmostEqual(centers[0][0],4.48127794,delta=0.01)
        self.assertAlmostEqual(centers[2][2],5.12661028,delta=0.01)
        
    def test_mesh_to_pcd(self):
        pcd=gt.mesh_to_pcd(self.mesh)
        self.assertIsInstance(pcd,o3d.geometry.PointCloud)
        self.assertGreater(len(pcd.points),3)
        
#    def test_generate_virtual_images(self):
#        cartesianTransforms= [self.image1CartesianTransform,self.image2CartesianTransform]
#        image=gt.generate_virtual_images(self.mesh, cartesianTransforms)
#        self.assertEqual(len(image),2)
#        self.assertIsInstance(image[0],o3d.cpu.pybind.geometry.Image)
        
#    def test_generate_virtual_image(self):
#        width=640
#        height=480
#        fx=400
#        fy=400
#        cx=width/2-0.5
#        cy=height/2-0.5
#        pinholeCamera=o3d.camera.PinholeCameraParameters
#        pinholeCamera.extrinsic=np.linalg.inv(self.image1CartesianTransform)
#        pinholeCamera.intrinsic=o3d.camera.PinholeCameraIntrinsic(width,height,fx,fy,cx,cy)
#        image=gt.generate_virtual_image(self.mesh, pinholeCamera)
#        self.assertIsInstance(image,o3d.cpu.pybind.geometry.Image)
        
    def test_e57path_to_pcd(self):
        e57=pye57.E57(str(self.e57Path1)) 
        header = e57.get_header(0)
        pcd=gt.e57path_to_pcd(e57Path=self.e57Path1, e57Index=0) 
        self.assertEqual(len(pcd.points) , header.point_count)

    def test_e57_to_arrays(self):
        e57=pye57.E57(str(self.e57Path1)) 
        header = e57.get_header(0)
        tuple=gt.e57_to_arrays(self.e57Path1)
        self.assertEqual(len(tuple),5)
        self.assertEqual(len(tuple[0]),header.point_count)
        self.assertEqual(len(tuple[1]),header.point_count)
        #self.assertEqual(len(tuple[2]),header.point_count)

    def test_e57_to_pcd(self):
        e57=pye57.E57(str(self.e57Path1)) 
        header = e57.get_header(0)
        pcd=gt.e57_to_pcd(e57, percentage=0.5)
        self.assertEqual(len(pcd.points),int(header.point_count*0.5))

        e57=pye57.E57(str(self.e57Path2)) 
        header = e57.get_header(1)
        pcd=gt.e57_to_pcd(e57, percentage=0.5)
        self.assertLess(len(pcd.points),6000000)

    def test_e57path_to_pcds_multiprocessing(self):
        e57=pye57.E57(str(self.e57Path1)) 
        header1 = e57.get_header(0)
        pcds=gt.e57path_to_pcds_multiprocessing(self.e57Path1, percentage=0.5)
        self.assertEqual(len(pcds),1)        
        self.assertEqual(len(pcds[0].points),int(header1.point_count*0.5))

        #e57=pye57.E57(self.e57Path2) 
        #header1 = e57.get_header(1)
        #header2 = e57.get_header(2) # Header 2 is not found
        #pcds=gt.e57path_to_pcds_multiprocessing(self.e57Path2, percentage=0.5)
        #self.assertEqual(len(pcds[0].points),int(header1.point_count*0.5))
        #self.assertEqual(len(pcds[1].points),int(header2.point_count*0.5))

    def test_pcd_to_arrays(self):
        tuple=gt.pcd_to_arrays(self.pcdPath1, percentage=0.5)
        self.assertEqual(len(tuple),4)
        self.assertEqual(len(tuple[0]),int(len(self.pcd.points)*0.5))
        self.assertEqual(len(tuple[1]),int(len(self.pcd.points)*0.5))
        self.assertEqual(tuple[2],None)

    def test_mesh_to_arrays(self):
        tuple=gt.mesh_to_arrays(self.meshPath)
        self.assertEqual(len(tuple),5)
        self.assertEqual(len(tuple[0]),len(self.mesh.vertices))
        self.assertEqual(len(tuple[1]),len(self.mesh.triangles))
        self.assertEqual(len(tuple[2]),len(self.mesh.vertex_colors))
        self.assertEqual(tuple[3],None)

    def test_e57_get_colors(self):
        e57=pye57.E57(str(self.e57Path1)) 
        gt.e57_update_point_field(e57)
        raw_data = e57.read_scan_raw(0)  
        header = e57.get_header(0)
        self.assertEqual(len(raw_data["cartesianX"]) , header.point_count)

        colors=gt.e57_get_colors(raw_data)
        self.assertEqual(len(colors),len(raw_data["cartesianX"]))
        self.assertEqual(len(colors),header.point_count)
        
    def test_crop_geometry_by_box(self):
        #test point cloud
        box=self.mesh.get_oriented_bounding_box()
        pcd=gt.crop_geometry_by_box(self.pcd, box) 
        self.assertIsInstance(pcd,o3d.geometry.PointCloud)
        self.assertGreater(len(pcd.points),10000000)

        #test mesh
        box=self.pcd.get_oriented_bounding_box()
        mesh=gt.crop_geometry_by_box(self.mesh, box, subdivide = 0)
        self.assertIsInstance(mesh,o3d.geometry.TriangleMesh)
        self.assertGreater(len(mesh.vertices),100000)

    def test_get_mesh_representation(self):
        #mesh
        mesh=gt.get_mesh_representation(self.mesh)
        self.assertEqual(len(mesh.triangles),len(self.mesh.triangles))

        #point cloud
        mesh=gt.get_mesh_representation(self.pcd)
        self.assertGreater(len(mesh.triangles),3)

        #invalid input
        self.assertRaises(ValueError,gt.get_mesh_representation,self.mesh.get_oriented_bounding_box())

    def test_get_mesh_inliers(self):
        #mesh
        sources=[self.slabMesh,self.wallMesh]
        indices=gt.get_mesh_inliers(sources=sources,reference=self.mesh)
        self.assertEqual(len(indices),len(sources))
        
        #pcd
        sources=[self.slabMesh,self.wallMesh]
        indices=gt.get_mesh_inliers(sources=sources,reference=self.pcd)
        self.assertEqual(len(indices),len(sources))

        #invalid sources
        self.assertRaises(ValueError,gt.get_mesh_inliers,self.mesh.get_oriented_bounding_box(),self.mesh.get_oriented_bounding_box())

    def test_expand_box(self):
        cartesianBounds=np.array([0,10,7,8.3,-2,2])       
        box=gt.get_oriented_bounding_box(cartesianBounds)
        #positive expansion
        expandedbox1=gt.expand_box(box,u=5,v=3,w=1)
        self.assertEqual(expandedbox1.extent[0],box.extent[0]+5)
        self.assertEqual(expandedbox1.extent[1],box.extent[1]+3)
        self.assertEqual(expandedbox1.extent[2],box.extent[2]+1)
        
        #negate expansion
        expandedbox2=gt.expand_box(box,u=-1,v=-1,w=-1)
        self.assertEqual(expandedbox2.extent[0],box.extent[0]-1)
        self.assertEqual(expandedbox2.extent[1],box.extent[1]-1)
        self.assertEqual(expandedbox2.extent[2],box.extent[2]-1)

        #impossible expansion
        self.assertRaises(ValueError,gt.expand_box,box=box,u=-55 )
            
    def test_join_geometries(self):
        #TriangleMesh
        mesh1=self.mesh
        mesh2=copy.deepcopy(mesh1)
        mesh2.translate([5,0,0])
        joinedMeshes= gt.join_geometries([mesh1,mesh2]) 
        self.assertEqual(len(joinedMeshes.triangles), (len(mesh1.triangles)+len(mesh2.triangles)))
        self.assertTrue(joinedMeshes.has_vertex_colors())

        #PointCloud
        pcd1=self.pcd
        pcd2=copy.deepcopy(pcd1)
        pcd2.translate([5,0,0])
        joinedpcd= gt.join_geometries([pcd1,pcd2]) 
        self.assertEqual(len(joinedpcd.points), (len(pcd1.points)+len(pcd2.points)))
        self.assertTrue(joinedpcd.has_colors())
        
    def test_crop_geometry_by_distance(self):
        sourcepcd=self.pcd
        sourceMesh=self.mesh
        cutterMeshes=[self.slabMesh,self.wallMesh,self.columnMesh,self.beamMesh]
        # mesh + [mesh]
        result1=gt.crop_geometry_by_distance(source=sourceMesh,cutters=cutterMeshes)
        self.assertGreater(len(result1.vertices),1900 )

        # pcd + [mesh]
        result2=gt.crop_geometry_by_distance(source=sourcepcd,cutters=cutterMeshes)
        self.assertGreater(len(result2.points),350000 ) 

        # mesh + pcd
        result3=gt.crop_geometry_by_distance(source=sourceMesh,cutters=sourcepcd)
        self.assertGreater(len(result3.vertices),5000 ) 

        # pcd + mesh
        result4=gt.crop_geometry_by_distance(source=sourcepcd,cutters=sourceMesh)
        self.assertLess(len(result4.points),1200000 ) 
    
    def test_determine_percentage_of_coverage(self):
        reference=self.pcd
        sources=[self.slabMesh,self.wallMesh,self.columnMesh,self.beamMesh]
        percentages=gt.determine_percentage_of_coverage(sources=sources,reference=reference)
        self.assertEqual(len(percentages), len(sources))
        self.assertLess(percentages[0],0.005)
        self.assertLess(percentages[1],0.001)
        self.assertLess(percentages[2],0.5)
        self.assertLess(percentages[3],0.001)

    def test_show_geometries(self):
        # gt.show_geometries((self.bimMeshes + [self.pcd, self.mesh]), color = True)
        self.assertEqual(0,0)
        
    def test_create_3d_camera(self):
        cam=gt.create_3d_camera()
        self.assertIsInstance(cam,o3d.geometry.TriangleMesh)
        
    # def test_save_view_point(self):
    #     print("test_save_view_point")
    #     filename=os.path.join(self.resourcePath,'myView.png')
    #     gt.save_view_point(self.pcd, filename)
    #     self.assertTrue(os.path.exists(filename))

    def test_crop_geometry_by_convex_hull(self):
        sourceMesh=gt.mesh_to_trimesh(self.mesh)
        meshes=[self.slabMesh,self.wallMesh,self.columnMesh,self.beamMesh]
        cutters=[gt.mesh_to_trimesh(mesh) for mesh in meshes]

        innerCrop=gt.crop_mesh_by_convex_hull(source=sourceMesh, cutters=cutters, inside = True )
        self.assertEqual(len(innerCrop),4)
        self.assertGreater(len(innerCrop[0].vertices),12000)
        self.assertGreater(len(innerCrop[1].vertices),800)
        self.assertGreater(len(innerCrop[2].vertices),1000)
        self.assertGreater(len(innerCrop[3].vertices),1000)

        outerCrop=gt.crop_mesh_by_convex_hull(source=sourceMesh, cutters=cutters[0], inside = False ) 
        self.assertGreater(len(outerCrop[0].vertices),255000)         
        
#    def test_crop_geometry_by_raycasting(self):
#        pcd=self.pcd
#        mesh=self.mesh
#        hull, _ = pcd.compute_convex_hull()
#
#        innerCrop=gt.crop_geometry_by_raycasting(source=mesh, cutter=hull, inside=True, strict =True ) 
#        self.assertLess(len(innerCrop.vertices),200000 )
#
#        innerCrop=gt.crop_geometry_by_raycasting(source=mesh, cutter=hull, inside=True, strict =False ) 
#        self.assertLess(len(innerCrop.vertices),200000 )
#
#        outerCrop=gt.crop_geometry_by_raycasting(source=mesh, cutter=hull, inside=False, strict =True ) 
#        self.assertLess(len(outerCrop.vertices),200000 )
        
    def test_get_translation(self):
        box=self.mesh.get_oriented_bounding_box()
        centerGt=box.get_center()

        #cartesianBounds
        cartesianBounds=gt.get_cartesian_bounds(box)
        center=gt.get_translation(cartesianBounds)
        self.assertAlmostEqual(math.dist(centerGt,center),0,delta=0.01)

        #orientedBounds
        orientedBounds= np.asarray(box.get_box_points())
        center=gt.get_translation(orientedBounds)
        self.assertAlmostEqual(math.dist(centerGt,center),0,delta=0.01)

        #cartesianTransform
        center=gt.get_translation(self.image2CartesianTransform)
        self.assertAlmostEqual(self.image2CartesianTransform[0][3],center[0],delta=0.01)

    def test_get_mesh_collisions_open3d(self):
        #NOT IMPLEMENTED
        pass
        # meshes=[self.slabMesh,self.wallMesh,self.columnMesh,self.beamMesh]
        # slabCollisions= gt.get_mesh_collisions_open3d(sourceMesh=self.slabMesh, meshes=meshes,t_d=0.5)
        # self.assertEqual(len(slabCollisions),23)

        # wallCollisions= gt.get_mesh_collisions_open3d(sourceMesh=self.wallMesh, meshes=self.bimBoxes)
        # self.assertEqual(len(wallCollisions),1)

        # ColumnCollisions= gt.get_mesh_collisions_open3d(sourceMesh=self.columnMesh, meshes=self.bimBoxes)
        # self.assertEqual(len(ColumnCollisions),23)
       
    def test_get_mesh_collisions_trimesh(self):

        inliers=gt.get_mesh_collisions_trimesh(sourceMesh=self.mesh , geometries =self.bimMeshes) 
        self.assertEqual(len(inliers),66 )

    def test_get_pcd_collisions(self):
        inliers=gt.get_pcd_collisions(sourcePcd=self.pcd, geometries =self.bimMeshes)
        self.assertLess(len(inliers),150 )

    def test_get_rotation_matrix(self):        
        rotationGt=np.array([[ 0.95891633, -0.28368445,  0.00161308],
                            [-0.28365413, -0.95887203, -0.01023566],
                            [ 0.00445043,  0.00935758 ,-0.99994631]])

        #cartesianTransform
        r1=gt.get_rotation_matrix(self.image2CartesianTransform)
        self.assertAlmostEqual(r1[0][0],self.image2CartesianTransform[0][0], delta=0.01)

        #Euler angles
        r2=gt.get_rotation_matrix(np.array([-121.22356551,   83.97341873,   -7.21021157]))
        self.assertAlmostEqual(r2[0][0],self.image2CartesianTransform[0][0], delta=0.01)
        
        #quaternion
        r3=gt.get_rotation_matrix(np.array([ 0.60465535, -0.28690085 , 0.66700836 ,-0.32738304]))
        self.assertAlmostEqual(r3[0][0],self.image2CartesianTransform[0][0], delta=0.01)

        #orientedBounds
        box=self.mesh.get_oriented_bounding_box()
        r4=gt.get_rotation_matrix(np.asarray(box.get_box_points()))
        self.assertAlmostEqual(r4[0][0],rotationGt[0][0], delta=0.01)

    def test_mesh_to_trimesh(self):
        triMesh=gt.mesh_to_trimesh(self.mesh)
        mesh2=triMesh.as_open3d
        self.assertEqual(len(self.mesh.triangles),len(mesh2.triangles))

if __name__ == '__main__':
    unittest.main()
