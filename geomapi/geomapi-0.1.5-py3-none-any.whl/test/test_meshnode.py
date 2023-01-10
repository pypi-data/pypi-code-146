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
        cls.meshGraphPath=cls.path / 'meshGraph.ttl'
        cls.meshGraph=Graph().parse(cls.meshGraphPath)
                
        #MESH1
        cls.path1=cls.path / 'MESH' / "week22.obj"
        cls.mesh1= o3d.io.read_triangle_mesh(str(cls.path1))
        cls.subject1=next(s for s in cls.meshGraph.subjects(RDF.type) if "week22" in s.toPython())
        
        #MESH2
        cls.path2=cls.path / "MESH" / "Basic Wall_211_WA_Ff1_Glued brickwork sandlime 150mm_1095339.obj"  
        cls.mesh2= o3d.io.read_triangle_mesh(str(cls.path2))
        cls.subject2=next(s for s in cls.meshGraph.subjects(RDF.type) if "Basic_Wall_211_WA_Ff1_Glued_brickwork_sandlime_150mm_1095339" in s.toPython())

        #MESH3
        cls.path3=cls.path / "MESH" / "Precast Stair_Stair_1181900 Landing 1.obj" 
        cls.mesh3= o3d.io.read_triangle_mesh(str(cls.path3))
        cls.subject3=next(s for s in cls.meshGraph.subjects(RDF.type) if "Precast_Stair_Stair_1181900_Landing_1" in s.toPython())

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
        if os.path.exists(os.path.join(os.getcwd(),'MESH') ):
            shutil.rmtree(os.path.join(os.getcwd(),'MESH') )
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

    def test_meshnode_creation_from_subject(self):
        #subject
        subject='myNode'
        node= MeshNode(subject=subject)
        self.assertEqual(node.subject.toPython(),'file:///'+subject)

        #http://
        subject='http://session_2022_05_20'
        node= MeshNode(subject=subject)
        self.assertEqual(node.subject.toPython(),subject)
        
        #erroneous char       
        subject='[[http://ses>sion_2022_<05_20]]'
        node= MeshNode(subject=subject)
        self.assertEqual(node.subject.toPython(),'http://__ses_sion_2022__05_20__')

    def test_meshnode_creation_from_graph(self):
        subject=next(self.meshGraph.subjects(RDF.type))
        node= MeshNode(graph=self.meshGraph, subject=subject)
        self.assertEqual(node.subject.toPython(),subject.toPython())
        object=self.meshGraph.value(subject,self.v4d['faceCount'])
        self.assertEqual(node.faceCount,object.toPython())
        
    def test_meshnode_creation_from_graph_path(self):
        subject=next(self.meshGraph.subjects(RDF.type))
        node= MeshNode(graphPath=self.meshGraphPath, subject=subject)
        self.assertEqual(node.subject.toPython(),subject.toPython())
        object=self.meshGraph.value(subject,self.v4d['faceCount'])
        self.assertEqual(node.faceCount,object.toPython())
        
    def test_meshnode_creation_from_path(self):
        #path1 without getResource
        node= MeshNode(path=self.path1)
        self.assertEqual(node.name,ut.get_filename(self.path1))
        #path2 with getResource
        node= MeshNode(path=self.path2,getResource=True)        
        self.assertEqual(node.name,ut.get_filename(self.path2))
        self.assertEqual(node.faceCount,len(self.mesh2.triangles))
        #path3 
        node= MeshNode(path=self.path3,getResource=True)
        self.assertEqual(node.name,ut.get_filename(self.path3))
        self.assertEqual(node.faceCount,len(self.mesh3.triangles))

    def test_meshnode_creation_from_resource(self):
        #mesh1
        node= MeshNode(resource=self.mesh1)
        self.assertEqual(node.faceCount,len(self.mesh1.triangles))
        #mesh2
        node= MeshNode(resource=self.mesh2)
        self.assertEqual(node.faceCount,len(self.mesh2.triangles))
        #mesh3
        node= MeshNode(resource=self.mesh3)
        self.assertEqual(node.faceCount,len(self.mesh3.triangles))

    def test_creation_from_subject_and_graph_and_graphPath(self):        
        subject=next(self.meshGraph.subjects(RDF.type))
        node= MeshNode(subject=subject,graph=self.meshGraph,graphPath=self.meshGraphPath)
        self.assertEqual(node.subject.toPython(),subject.toPython())
        node.to_graph()
        self.assertTrue((subject, self.v4d['faceCount'], Literal(node.faceCount)) in self.meshGraph)

    def test_creation_from_subject_and_path(self):        
        node= MeshNode(subject=self.subject2,path=self.path2,getResource=True)
        self.assertEqual(node.subject.toPython(),self.subject2.toPython())
        node.to_graph()
        box= self.mesh2.get_oriented_bounding_box()
        min=box.get_min_bound()
        self.assertAlmostEqual(np.asarray(node.orientedBounds)[0,0],min[0],delta=0.01)

    def test_creation_from_subject_and_path_and_graph(self):        
        node= MeshNode(subject=self.subject3,path=self.path3,graph=self.meshGraph,getResource=True)
        self.assertEqual(node.subject.toPython(),self.subject3.toPython())
        node.to_graph()
        initialGraph=ut.get_subject_graph(self.meshGraph,subject=self.subject3)
        self.assertEqual(len(node.graph),len(initialGraph))
        box= self.mesh3.get_axis_aligned_bounding_box()
        min=box.get_min_bound()
        self.assertAlmostEqual(node.cartesianBounds[0],min[0],delta=0.01)

    def test_creation_from_resource_and_path(self):        
        node= MeshNode(resource=self.mesh1,path=self.path1)
        self.assertEqual(node.subject.toPython(),'file:///'+ut.get_filename(self.path1) )

    def test_creation_from_subject_resource_and_path(self):        
        node= MeshNode(subject=self.subject2,resource=self.mesh2,path=self.path2)
        self.assertEqual(node.subject.toPython(),self.subject2.toPython() )
        
    def test_creation_from_subject_resource_and_path_and_graph(self):        
        node= MeshNode(subject=self.subject3,resource=self.mesh3,path=self.path3, graph=self.meshGraph)
        self.assertEqual(node.subject.toPython(),self.subject3.toPython() )
        node.to_graph()
        object=node.graph.value(node.subject,self.v4d['path'])
        self.assertEqual(ut.parse_path(object.toPython()),(Path("MESH") / (ut.get_filename(self.path3) +'.obj')).as_posix())

    def test_node_creation_with_get_resource(self):
        #mesh
        node= MeshNode(resource=self.mesh1)
        self.assertIsNotNone(node._resource)

        #path without getResource
        node= MeshNode(path=self.path2)
        self.assertIsNone(node._resource)

        #path with getResource
        node= MeshNode(path=self.path3,getResource=True)
        self.assertIsNotNone(node._resource)

        #graph with get resource
        node= MeshNode(subject=self.subject2,graph=self.meshGraph,getResource=True)
        self.assertIsNone(node._resource)

        #graphPath with get resource
        node= MeshNode(subject=self.subject3,graphPath=self.meshGraphPath,getResource=True)
        self.assertIsNotNone(node._resource)

    def test_delete_resource(self):
        node= MeshNode(resource=self.mesh1)
        self.assertIsNotNone(node._resource)
        del node.resource
        self.assertIsNone(node._resource)

    def test_save_resource(self):
        #no mesh -> False
        node= MeshNode()
        self.assertFalse(node.save_resource())

        #directory
        node= MeshNode(resource=self.mesh2)
        self.assertTrue(node.save_resource(os.path.join(self.path,'resources')))

        # #graphPath        
        # node= MeshNode(resource=self.mesh2,graphPath=self.meshGraphPath)
        # self.assertTrue(node.save_resource())

        #no path or graphPath
        node= MeshNode(resource=self.mesh2)        
        self.assertTrue(node.save_resource())

        #invalid extension -> error
        node= MeshNode(resource=self.mesh1)
        self.assertRaises(ValueError,node.save_resource,os.path.join(self.path,'resources'),'.kjhgfdfg')

        #.ply -> ok
        node= MeshNode(resource=self.mesh2)
        self.assertTrue(node.save_resource(os.path.join(self.path,'resources'),'.ply'))
        self.assertEqual(node.path,(self.path / 'resources' / (node.name+'.ply')).as_posix())

        #.obj -> ok
        node= MeshNode(resource=self.mesh3)
        self.assertTrue(node.save_resource(os.path.join(self.path,'resources'),'.obj'))
        self.assertEqual(node.path,(self.path / 'resources' / (node.name+'.obj')).as_posix())

        
        #path -> new name
        node= MeshNode(subject=URIRef('myMesh'),path=self.path2,getResource=True)
        self.assertTrue(node.save_resource())
        
        #graphPath with directory
        node=MeshNode(subject=self.subject2,graphPath=self.meshGraphPath, resource=self.mesh3)
        self.assertTrue(node.save_resource(os.path.join(self.path,'resources')))

        #graph with new subject
        node=MeshNode(subject=self.subject3,graph=self.meshGraph, resource=self.mesh3)
        node.name='myMesh'
        self.assertTrue(node.save_resource())

    def test_get_resource(self):
        #mesh
        node=MeshNode(resource=self.mesh3)  
        self.assertIsNotNone(node.get_resource())

        #no mesh
        node=MeshNode()
        self.assertIsNone(node.get_resource())

        #graphPath with getResource
        node=MeshNode(graphPath=self.meshGraphPath,subject=self.subject2,getResource=True)
        self.assertIsNotNone(node.get_resource())

    def test_get_metadata_from_resource(self):
        #mesh
        node=MeshNode(resource=self.mesh3)  
        self.assertIsNotNone(node.orientedBounds)
        self.assertIsNotNone(node.cartesianBounds)
        self.assertIsNotNone(node.cartesianTransform)
        self.assertIsNotNone(node.faceCount)
        self.assertIsNotNone(node.pointCount)

        #graphPath
        node=MeshNode(graphPath=self.meshGraphPath,subject=self.subject2,getResource=True)
        self.assertIsNotNone(node.orientedBounds)
        self.assertIsNotNone(node.cartesianBounds)
        self.assertIsNotNone(node.cartesianTransform)
        self.assertIsNotNone(node.faceCount)
        self.assertIsNotNone(node.pointCount)

if __name__ == '__main__':
    unittest.main()
