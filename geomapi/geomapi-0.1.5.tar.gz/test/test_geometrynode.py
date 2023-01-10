# import resource
import copy
import math
import os
from pathlib import Path
import shutil
import time
import unittest
from multiprocessing.sharedctypes import Value

import cv2
import geomapi.utils as ut
import geomapi.utils.geometryutils as gt
import ifcopenshell
import numpy as np
import open3d as o3d
import PIL
import pye57
import rdflib
from geomapi.nodes import *
from ifcopenshell.util.selector import Selector
from rdflib import RDF, RDFS, Graph, Literal, URIRef


class TestNode(unittest.TestCase):

################################## SETUP/TEARDOWN CLASS ######################
    @classmethod
    def setUpClass(cls):
        #execute once before all tests
        print('-----------------Setup Class----------------------')
        st = time.time()
        cls.path= Path.cwd() / "test" / "testfiles" 

        #ONTOLOGIES
        cls.exif = rdflib.Namespace('http://www.w3.org/2003/12/exif/ns#')
        cls.geo=rdflib.Namespace('http://www.opengis.net/ont/geosparql#') #coordinate system information
        cls.gom=rdflib.Namespace('https://w3id.org/gom#') # geometry representations => this is from mathias
        cls.omg=rdflib.Namespace('https://w3id.org/omg#') # geometry relations
        cls.fog=rdflib.Namespace('https://w3id.org/fog#')
        cls.v4d=rdflib.Namespace('https://w3id.org/v4d/core#')
        cls.openlabel=rdflib.Namespace('https://www.asam.net/index.php?eID=dumpFile&t=f&f=3876&token=413e8c85031ae64cc35cf42d0768627514868b2f#')
        cls.e57=rdflib.Namespace('http://libe57.org#')
        cls.xcr=rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        cls.ifc=rdflib.Namespace('http://ifcowl.openbimstandards.org/IFC2X3_Final#')

        #PCDGRAPH
        cls.graphPath1=cls.path / 'pcdGraph.ttl'
        cls.graph1=Graph().parse(cls.graphPath1)

        #MESHGRAPH
        cls.graphPath2=cls.path / 'meshGraph.ttl'
        cls.graph2=Graph().parse(cls.graphPath2)
                
        #PCD1 
        cls.path1=cls.path / 'PCD' / "academiestraat week 22 a 20.pcd" 
        # cls.pcd1= o3d.io.read_point_cloud(cls.path1)
        cls.subject1=next(s for s in cls.graph1.subjects(RDF.type) if "file:///academiestraat_week_22_a_20" in s.toPython())

        #MESH2 
        cls.path2=cls.path / 'MESH' / "Precast Stair_Stair_1181900 Landing 1.obj"
        cls.mesh2 = o3d.io.read_triangle_mesh(str(cls.path2))
        cls.box2=cls.mesh2.get_oriented_bounding_box()
        cls.cartesianTransform2=gt.get_cartesian_transform(translation=cls.box2.get_center())
        cls.subject2=next(s for s in cls.graph2.subjects(RDF.type) if "file:///Precast_Stair_Stair_1181900_Landing_1" in s.toPython())

        #RESOURCES
        cls.resourcePath=cls.path / "resources"
        if not os.path.exists(cls.resourcePath):
            os.mkdir(cls.resourcePath)

        #TIME TRACKING           
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
################################## TEST FUNCTIONS ######################

    def test_Node_creation_from_subject(self):
        #subject
        subject='myNode'
        node= GeometryNode(subject=subject)
        self.assertEqual(node.subject.toPython(),'file:///'+subject)

    def test_Node_creation_with_cartesianBounds(self):
        #None
        cartesianBounds=None
        node= GeometryNode(cartesianBounds=cartesianBounds)
        self.assertIsNone(node.cartesianBounds)

        #np.array(6x1)
        cartesianBounds=np.array([1,2,3,4,5,6])
        node= GeometryNode(cartesianBounds=cartesianBounds)
        self.assertEqual(node.cartesianBounds.size,6)   

        #list
        cartesianBounds=[1,2,3,4,5,6]
        node= GeometryNode(cartesianBounds=cartesianBounds)
        self.assertEqual(node.cartesianBounds.size,6)   

        #np.array(other)
        cartesianBounds=np.array([[1,2],[3,4],[5,6]])
        node= GeometryNode(cartesianBounds=cartesianBounds)
        self.assertEqual(node.cartesianBounds.size,6)   

        #orientedBoundingBox
        node= GeometryNode(cartesianBounds=self.box2)
        self.assertEqual(node.cartesianBounds.size,6)   

        #Vector3dVector
        cartesianBounds=gt.get_oriented_bounds(np.array([1,2,3,4,5,6]) )
        node= GeometryNode(cartesianBounds=cartesianBounds)
        self.assertEqual(node.cartesianBounds.size,6)   

        #orientedBounds
        cartesianBounds=np.asarray(gt.get_oriented_bounds(np.array([1,2,3,4,5,6]) ))
        node= GeometryNode(cartesianBounds=cartesianBounds)
        self.assertEqual(node.cartesianBounds.size,6)   

        #error
        self.assertRaises(ValueError,GeometryNode,cartesianBounds='thisisnotacartesianbound')


    def test_Node_creation_with_orientedBounds(self):
        #None
        orientedBounds=None
        node= GeometryNode(orientedBounds=orientedBounds)
        self.assertIsNone(node.orientedBounds)

        #np.array(8x3)
        orientedBounds=np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15],[16,17,18],[19,20,21],[22,23,24]])
        node= GeometryNode(orientedBounds=orientedBounds)
        self.assertEqual(node.orientedBounds.size,24)   

        #list
        orientedBounds=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        node= GeometryNode(orientedBounds=orientedBounds)
        self.assertEqual(node.orientedBounds.size,24)   

        #np.array(other)
        orientedBounds=np.array([[1,4,7,10,13,16,19,22],
                                  [2,5,8,11,14,17,20,23],
                                  [3,6,9,12,15,18,21,24]])
        node= GeometryNode(orientedBounds=orientedBounds)
        self.assertEqual(node.orientedBounds.size,24)   

        #orientedBoundingBox
        node= GeometryNode(orientedBounds=self.box2)
        self.assertEqual(node.orientedBounds.size,24)   

        #Vector3dVector
        points=o3d.utility.Vector3dVector(np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15],[16,17,18],[19,20,21],[22,23,24]]))   
        node= GeometryNode(orientedBounds=points)
        self.assertEqual(node.orientedBounds.size,24)   

        #error
        self.assertRaises(ValueError,GeometryNode,orientedBounds='thisisnotaorientedbound')


    def test_Node_creation_with_orientedBoundingBox(self):
        #None
        orientedBoundingBox=None
        node= GeometryNode(orientedBoundingBox=orientedBoundingBox)
        self.assertIsNone(node.orientedBoundingBox)

        #box
        node= GeometryNode(orientedBoundingBox=self.box2)
        self.assertAlmostEqual(node.orientedBoundingBox.get_min_bound()[0],self.box2.get_min_bound()[0],delta=0.01)   

        #np.array(nx3)
        orientedBoundingBox=self.mesh2.get_oriented_bounding_box()
        points=np.asarray(orientedBoundingBox.get_box_points())
        node= GeometryNode(orientedBoundingBox=points)
        self.assertAlmostEqual(node.orientedBoundingBox.get_min_bound()[0],orientedBoundingBox.get_min_bound()[0],delta=0.01)   

        #geometry
        node= GeometryNode(orientedBoundingBox=self.mesh2)
        self.assertAlmostEqual(node.orientedBoundingBox.get_min_bound()[0],orientedBoundingBox.get_min_bound()[0],delta=0.01)   

        #Vector3dVector
        orientedBoundingBox=self.mesh2.get_oriented_bounding_box()
        points=orientedBoundingBox.get_box_points()
        node= GeometryNode(orientedBoundingBox=points)
        self.assertAlmostEqual(node.orientedBoundingBox.get_min_bound()[0],orientedBoundingBox.get_min_bound()[0],delta=0.01)   

    def test_Node_creation_with_cartesianTransform(self):
        #None
        cartesianTransform=None
        node= GeometryNode(cartesianTransform=cartesianTransform)
        self.assertIsNone(node.cartesianTransform)

        #center np.array(1x3)        
        center=self.box2.get_center()
        node= GeometryNode(cartesianTransform=center)
        self.assertAlmostEqual(node.cartesianTransform[0,3],center[0],delta=0.01)   

        #cartesianBounds np.array(1x6)
        cartesianBounds=gt.get_cartesian_bounds(self.box2)
        node= GeometryNode(cartesianTransform=cartesianBounds)
        self.assertAlmostEqual(node.cartesianTransform[0,3],(cartesianBounds[0]+cartesianBounds[1])/2,delta=0.01)   

        #orientedBounds np.array(8x3)
        orientedBounds=np.asarray(self.box2.get_box_points())
        node= GeometryNode(cartesianTransform=orientedBounds)
        self.assertAlmostEqual(node.cartesianTransform[0,3],center[0],delta=0.01)   

        #np.ndarray(nx3)
        array=np.concatenate((orientedBounds,orientedBounds),0)
        node= GeometryNode(cartesianTransform=array)
        self.assertAlmostEqual(node.cartesianTransform[0,3],center[0],delta=0.01)   

        #geometry
        node= GeometryNode(cartesianTransform=self.mesh2)
        self.assertAlmostEqual(node.cartesianTransform[0,3],self.mesh2.get_center()[0],delta=0.01)   

        #Vector3dVector
        points=self.box2.get_box_points()
        node= GeometryNode(cartesianTransform=points)
        self.assertAlmostEqual(node.cartesianTransform[0,3],center[0],delta=0.01)   

    def test_get_oriented_bounding_box(self):

        #empty
        node=GeometryNode()        
        self.assertIsNone(node.get_oriented_bounding_box())

        #orientedBoundingBox
        node= GeometryNode(orientedBoundingBox=self.box2)
        self.assertAlmostEqual(node.get_oriented_bounding_box().get_min_bound()[0],self.box2.get_min_bound()[0],delta=0.01)   

        #cartesianBounds
        cartesianBounds=gt.get_cartesian_bounds(self.mesh2)
        node= GeometryNode(cartesianBounds=cartesianBounds)
        self.assertAlmostEqual(node.get_oriented_bounding_box().get_min_bound()[0],self.mesh2.get_axis_aligned_bounding_box().get_min_bound()[0],delta=0.01)   

        #orientedBounds
        orientedBounds=gt.get_oriented_bounds(cartesianBounds)
        node= GeometryNode(orientedBounds=orientedBounds)
        self.assertAlmostEqual(node.get_oriented_bounding_box().get_min_bound()[0],self.mesh2.get_axis_aligned_bounding_box().get_min_bound()[0],delta=0.01)   

    def test_get_cartesian_transform(self):

        #emtpy
        node=GeometryNode()        
        self.assertIsNone(node.get_cartesian_transform())

        #cartesianTransform
        node=GeometryNode(cartesianTransform=self.cartesianTransform2)
        self.assertEqual(node.get_cartesian_transform()[0,3], self.cartesianTransform2[0,3])

        #cartesianBounds
        cartesianBounds=gt.get_cartesian_bounds(self.mesh2)
        node=GeometryNode(cartesianBounds=cartesianBounds)
        self.assertEqual(node.get_cartesian_transform()[0,3], (cartesianBounds[0]+cartesianBounds[1])/2)

        #orientedBounds
        orientedBounds=np.asarray(self.box2.get_box_points())
        node=GeometryNode(orientedBounds=orientedBounds)
        self.assertEqual(node.get_cartesian_transform()[0,3], np.mean(orientedBounds,0)[0])

        #orientedBoundingBox
        node=GeometryNode(orientedBoundingBox=self.box2)
        self.assertEqual(node.get_cartesian_transform()[0,3], np.mean(orientedBounds,0)[0])

        #resource
        node=GeometryNode(resource=self.mesh2)
        self.assertEqual(node.get_cartesian_transform()[0,3],  self.mesh2.get_center()[0])

    def test_get_cartesian_bounds(self):
        #emtpy
        node=GeometryNode()        
        self.assertIsNone(node.get_cartesian_bounds())

        #cartesianBounds
        cartesianBounds=gt.get_cartesian_bounds(self.mesh2)
        node=GeometryNode(cartesianBounds=cartesianBounds)
        self.assertEqual(node.get_cartesian_bounds()[0], cartesianBounds[0])

        #orientedBounds
        orientedBounds=np.asarray(self.box2.get_box_points())
        node=GeometryNode(orientedBounds=orientedBounds)
        self.assertAlmostEqual(node.get_cartesian_bounds()[0], self.box2.get_min_bound()[0],delta=0.01)

        #orientedBoundingBox
        node=GeometryNode(orientedBoundingBox=self.box2)
        self.assertEqual(node.get_cartesian_bounds()[0],  self.box2.get_min_bound()[0])

        #resource
        node=GeometryNode(resource=self.mesh2)
        self.assertEqual(node.get_cartesian_bounds()[0],  self.mesh2.get_min_bound()[0])


    def test_get_oriented_bounds(self):
        #emtpy
        node=GeometryNode()        
        self.assertIsNone(node.get_oriented_bounds())

        #cartesianBounds
        cartesianBounds=gt.get_cartesian_bounds(self.mesh2)
        node=GeometryNode(cartesianBounds=cartesianBounds)
        self.assertEqual(node.get_oriented_bounds()[0,0], cartesianBounds[0])

        #orientedBounds
        orientedBounds=np.asarray(self.box2.get_box_points())
        node=GeometryNode(orientedBounds=orientedBounds)
        self.assertEqual(node.get_oriented_bounds()[2,2], orientedBounds[2,2])

        #orientedBoundingBox
        node=GeometryNode(orientedBoundingBox=self.box2)
        self.assertEqual(node.get_oriented_bounds()[2,2],  np.asarray(self.box2.get_box_points())[2,2])

        #resource
        node=GeometryNode(resource=self.mesh2)
        self.assertEqual(node.get_oriented_bounds()[2,2],  np.asarray(self.box2.get_box_points())[2,2])

    def test_get_center(self):
        #emtpy
        node=GeometryNode()        
        self.assertIsNone(node.get_center())

        #cartesianBounds
        cartesianBounds=gt.get_cartesian_bounds(self.mesh2)
        node=GeometryNode(cartesianBounds=cartesianBounds)
        self.assertEqual(node.get_center()[0], (cartesianBounds[0]+cartesianBounds[1])/2)

        #orientedBounds
        orientedBounds=np.asarray(self.box2.get_box_points())
        node=GeometryNode(orientedBounds=orientedBounds)
        self.assertEqual(node.get_center()[0], np.mean(orientedBounds,0)[0])

        #orientedBoundingBox
        node=GeometryNode(orientedBoundingBox=self.box2)
        self.assertEqual(node.get_center()[0],  self.box2.get_center()[0])

        #resource
        node=GeometryNode(resource=self.mesh2)
        self.assertEqual(node.get_center()[0],  self.mesh2.get_center()[0])


if __name__ == '__main__':
    unittest.main()
