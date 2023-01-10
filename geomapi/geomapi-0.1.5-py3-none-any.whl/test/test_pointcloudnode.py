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

        #GRAPH 
        cls.graphPath=cls.path / 'pcdGraph.ttl'
        cls.graph=Graph().parse(cls.graphPath)
                
        #PCD1 (PCD)
        pye57.e57.SUPPORTED_POINT_FIELDS.update({'nor:normalX' : 'd','nor:normalY': 'd','nor:normalZ': 'd'})

        cls.path1=cls.path / 'PCD' / "academiestraat week 22 a 20.pcd"  
        cls.pcd1= o3d.io.read_point_cloud(str(cls.path1))
        cls.subject1=next(s for s in cls.graph.subjects(RDF.type) if "file:///academiestraat_week_22_a_20" in s.toPython())

        #E57_2 (SfM)
        cls.path2=cls.path / 'PCD'/"week22 photogrammetry - Cloud.e57"
        cls.e57_2 = pye57.E57(str(cls.path2))
        cls.e57_scan2=cls.e57_2.read_scan_raw(0) 
        cls.e57_header2=cls.e57_2.get_header(0)  
        cls.pcd2=gt.e57_to_pcd(cls.e57_2)  
        cls.subject2=next(s for s in cls.graph.subjects(RDF.type) if "file:///week22_photogrammetry_-_Cloud" in s.toPython())

        #E57_3 (TLS)
        cls.path3=cls.path / 'PCD'/"week 22 - Lidar.e57"
        cls.e57_3 = pye57.E57(str(cls.path3))  
        cls.e57_scan3=cls.e57_3.read_scan_raw(0)    
        cls.e57_header3=cls.e57_3.get_header(0)  
        cls.pcd3=gt.e57_to_pcd(cls.e57_3)  
        cls.subject3=next(s for s in cls.graph.subjects(RDF.type) if "file:///academiestraat_week_22_19" in s.toPython())
        
        #RESOURCES
        cls.resourcePath=cls.path / "resources"
        if not os.path.exists(cls.resourcePath):
            os.mkdir(cls.resourcePath)

        #FILES
        cls.files=ut.get_list_of_files( cls.path)

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
        if os.path.exists(os.path.join(os.getcwd(),'PCD') ):
            shutil.rmtree(os.path.join(os.getcwd(),'PCD') )
        if os.path.exists(os.path.join(os.getcwd(),'resources') ):
            shutil.rmtree(os.path.join(os.getcwd(),'resources') )

################################## SETUP/TEARDOWN ######################

    def setUp(self):
        #execute before every test
        self.startTime = time.time()   

    def tearDown(self):
        #execute after every test
        t = time.time() - self.startTime
        print('{:50s} {:5s} '.format(self._testMethodName,str(t)))
################################## TEST FUNCTIONS ######################

    def test_PointCloudNode_creation_from_subject(self):
        #subject
        subject='myNode'
        node= PointCloudNode(subject=subject)
        self.assertEqual(node.subject.toPython(),'file:///'+subject)

        #http://
        subject='http://session_2022_05_20'
        node= PointCloudNode(subject=subject)
        self.assertEqual(node.subject.toPython(),subject)
        
        #erroneous char       
        subject='[[http://ses>sion_2022_<05_20]]'
        node= PointCloudNode(subject=subject)
        self.assertEqual(node.subject.toPython(),'http://__ses_sion_2022__05_20__')

    def test_PointCloudNode_creation_from_graph(self):
        subject=next(self.graph.subjects(RDF.type))
        node= PointCloudNode(graph=self.graph, subject=subject)
        self.assertEqual(node.subject.toPython(),subject.toPython())
        object=self.graph.value(subject,self.e57['pointCount'])
        self.assertEqual(node.pointCount,object.toPython())
        
    def test_PointCloudNode_creation_from_graph_path(self):
        subject=next(self.graph.subjects(RDF.type))
        node= PointCloudNode(graphPath=self.graphPath, subject=subject)
        self.assertEqual(node.subject.toPython(),subject.toPython())
        object=self.graph.value(subject,self.e57['pointCount'])
        self.assertEqual(node.pointCount,object.toPython())
        
    def test_PointCloudNode_creation_from_path(self):
        #path1 without getResource
        node= PointCloudNode(path=self.path1)
        self.assertEqual(node.name,ut.get_filename(self.path1))

        #path2 with getResource
        node= PointCloudNode(path=self.path2,getResource=True)        
        self.assertEqual(node.name,ut.get_filename(self.path2))
        self.assertEqual(node.pointCount,len(self.pcd2.points))

        #path3 
        node= PointCloudNode(path=self.path3,getResource=True)
        self.assertEqual(node.pointCount,len(self.pcd3.points))

    def test_PointCloudNode_creation_from_resource(self):
        #pcd1
        node= PointCloudNode(resource=self.pcd1)
        self.assertEqual(node.pointCount,len(self.pcd1.points))

        #pcd2 -> e57 file
        node= PointCloudNode(resource=self.e57_2)
        self.assertEqual(node.pointCount,len(self.pcd2.points))

        #pcd3 -> e57 scan 
        self.assertRaises(ValueError,PointCloudNode,resource=self.e57_scan3)

    def test_creation_from_subject_and_graph_and_graphPath(self):        
        subject=next(self.graph.subjects(RDF.type))
        node= PointCloudNode(subject=subject,graph=self.graph,graphPath=self.graphPath)
        self.assertEqual(node.subject.toPython(),subject.toPython())
        node.to_graph()
        self.assertTrue((subject, self.e57['pointCount'], Literal(node.pointCount)) in self.graph)

    def test_creation_from_subject_and_path(self):        
        node= PointCloudNode(subject=self.subject2,path=self.path2,getResource=True)
        self.assertEqual(node.subject.toPython(),self.subject2.toPython())
        #box= self.pcd2.get_oriented_bounding_box()
        #min=np.asarray(box.get_box_points())
        #self.assertAlmostEqual(node.orientedBounds[0,0],min[0,0],delta=0.01)

    def test_creation_from_subject_and_path_and_graph(self):        
        node= PointCloudNode(subject=self.subject3,path=self.path3,graph=self.graph,getResource=True)
        self.assertEqual(node.subject.toPython(),self.subject3.toPython())
        node.to_graph()
        initialGraph=ut.get_subject_graph(self.graph,subject=self.subject3)
        self.assertEqual(len(node.graph),len(initialGraph))

    def test_creation_from_resource_and_path(self):        
        node= PointCloudNode(resource=self.pcd1,path=self.path1)
        self.assertEqual(node.subject.toPython(),'file:///'+ut.validate_string(ut.get_filename(self.path1)) )

    def test_creation_from_subject_resource_and_path(self):        
        node= PointCloudNode(subject=self.subject2,resource=self.pcd2,path=self.path2)
        self.assertEqual(node.subject.toPython(),self.subject2.toPython() )
        
    def test_creation_from_subject_resource_and_path_and_graph(self):        
        node= PointCloudNode(subject=self.subject3,resource=self.pcd3,path=self.path3, graph=self.graph)
        self.assertEqual(node.subject.toPython(),self.subject3.toPython() )
        node.to_graph()
        object=node.graph.value(node.subject,self.v4d['path'])
        self.assertEqual(ut.parse_path(object.toPython()) ,(Path("PCD") / (ut.get_filename(self.path3)+'.e57')).as_posix() )

    def test_node_creation_with_get_resource(self):
        #pcd
        node= PointCloudNode(resource=self.pcd1)
        self.assertIsNotNone(node.resource)

        #path without getResource
        node= PointCloudNode(path=self.path2)
        self.assertIsNone(node._resource)

        #path with getResource
        node= PointCloudNode(path=self.path3,getResource=True)
        self.assertIsNotNone(node.resource)

        #graph with get resource
        node= PointCloudNode(subject=self.subject2,graph=self.graph,getResource=True)
        self.assertIsNone(node.resource)
        
        #graphPath with get resource
        node= PointCloudNode(subject=self.subject3,graphPath=self.graphPath,getResource=True)
        self.assertIsNotNone(node.resource)

    def test_delete_resource(self):
        #pcd
        node= PointCloudNode(resource=self.pcd1)
        self.assertIsNotNone(node._resource)
        del node.resource
        self.assertIsNone(node._resource)

    def test_save_resource(self):
        #no pcd -> False
        node= PointCloudNode()
        self.assertFalse(node.save_resource())

        #directory
        node= PointCloudNode(resource=self.pcd2)
        self.assertTrue(node.save_resource(self.resourcePath))

        # #graphPath        
        # node= PointCloudNode(resource=self.pcd2,graphPath=self.graphPath)
        # self.assertTrue(node.save_resource())

        # #no path or graphPath
        # node= PointCloudNode(resource=self.pcd2)        
        # self.assertTrue(node.save_resource())

        ##invalid extension -> error
        #node= PointCloudNode(resource=self.pcd1)
        #self.assertRaises(ValueError,node.save_resource,self.resourcePath,'.kjhgfdfg')
#
        ##.pcd 
        #node= PointCloudNode(resource=self.pcd2)
        #self.assertTrue(node.save_resource(self.resourcePath,'.pcd'))
        #self.assertEqual(node.path,os.path.join(self.resourcePath,node.name+'.pcd'))
#
        ##.ply 
        #node= PointCloudNode(resource=self.pcd3)
        #self.assertTrue(node.save_resource(self.resourcePath,'.ply'))
        #self.assertEqual(node.path,os.path.join(self.resourcePath,node.name+'.ply'))
        #
        ##.e57 
        #node= PointCloudNode(resource=self.e57_2)
        #self.assertTrue(node.save_resource(self.resourcePath,'.e57'))
        #self.assertEqual(node.path,os.path.join(self.resourcePath,node.name+'.e57'))
        #
        ##path -> new name
        #node= PointCloudNode(subject=URIRef('mypcd'),path=self.path2,getResource=True)
        #self.assertTrue(node.save_resource())
        #
        ##graphPath with directory
        #node=PointCloudNode(subject=self.subject2,graphPath=self.graphPath, resource=self.pcd3)
        #self.assertTrue(node.save_resource(self.resourcePath))

        # #graph with new subject
        # node=PointCloudNode(subject=self.subject3,grap=self.graph, resource=self.pcd3)
        # node.name='mypcd'
        # self.assertTrue(node.save_resource())

    def test_get_resource(self):
        #pcd
        node=PointCloudNode(resource=self.pcd3)  
        self.assertIsNotNone(node.get_resource())

        #no pcd
        del node.resource
        self.assertIsNone(node.get_resource())

        #graphPath with getResource
        node=PointCloudNode(graphPath=self.graphPath,subject=self.subject2,getResource=True)
        self.assertIsNotNone(node.get_resource())

    def test_get_metadata_from_resource(self):
        #pcd
        node=PointCloudNode(resource=self.pcd3)  
        self.assertIsNotNone(node.orientedBounds)
        self.assertIsNotNone(node.cartesianBounds)
        self.assertIsNotNone(node.cartesianTransform)
        self.assertIsNotNone(node.pointCount)

        #graphPath
        node=PointCloudNode(graphPath=self.graphPath,subject=self.subject2,getResource=True)
        self.assertIsNotNone(node.orientedBounds)
        self.assertIsNotNone(node.cartesianBounds)
        self.assertIsNotNone(node.cartesianTransform)
        self.assertIsNotNone(node.pointCount)

if __name__ == '__main__':
    unittest.main()
