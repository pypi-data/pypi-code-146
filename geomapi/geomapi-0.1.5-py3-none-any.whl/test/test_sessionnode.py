import copy
import math
import os
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
from PIL import Image
from rdflib import RDF, RDFS, Graph, Literal, URIRef


class TestNode(unittest.TestCase):

################################## SETUP/TEARDOWN CLASS ######################
    @classmethod
    def setUpClass(cls):
        #execute once before all tests
        print('-----------------Setup Class----------------------')
        st = time.time()
        cls.path=os.path.join(os.getcwd(), "test","testfiles") 

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
       
        #sessionGraph (single)
        cls.sessionGraphPath=os.path.join(cls.path,'sessionGraph.ttl')
        cls.sessionGraph=Graph().parse(cls.sessionGraphPath)
        cls.sessionPath=os.path.join(cls.path,'SESSION',"17dc31bc-17f2-11ed-bdae-c8f75043ce59.ply")  
        cls.sessionMesh= o3d.io.read_triangle_mesh(cls.sessionPath)
        cls.subject=next(s for s in cls.sessionGraph.subjects(RDF.type))
        
        #resourceGraph (data)
        cls.resourceGraphPath=os.path.join(cls.path,'resourceGraph.ttl')
        cls.resourceGraph=Graph().parse(cls.resourceGraphPath)
        cls.linkedSubjects=[s for s in cls.resourceGraph.subjects(RDF.type)]

        #combinedGraph (combined)
        cls.combinedGraphPath=os.path.join(cls.path,'combinedGraph.ttl')
        cls.combinedGraph=Graph().parse(cls.combinedGraphPath)
        
        #NODES
        cls.meshNode=MeshNode(path=os.path.join(cls.path,'Mesh','Basic Wall_211_WA_Ff1_Glued brickwork sandlime 150mm_1095339.obj'),getResource=True)
        cls.imgNode=ImageNode(xmpPath=os.path.join(cls.path,'IMG','IMG_2174.xmp'),getResource=True)
        cls.pcdNode=PointCloudNode(path=os.path.join(cls.path,'PCD','week22 photogrammetry - Cloud.pcd'),getResource=True)
        cls.bimNode=BIMNode(graphPath=os.path.join(cls.path,'bimGraph1.ttl'),subject='file:///Basic_Wall_211_WA_Ff1_Glued_brickwork_sandlime_150mm_1118860_0KysUSO6T3_gOJKtAiUE7d',getResource=True)
        cls.nodeList=[cls.meshNode,cls.imgNode,cls.pcdNode,cls.bimNode]
        cls.resources=[cls.meshNode.resource,cls.imgNode.resource,cls.pcdNode.resource,cls.bimNode.resource]

        #RESOURCES
        cls.resourcePath=os.path.join(cls.path,"resources")
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
        if os.path.exists(os.path.join(os.getcwd(),'SESSION') ):
            shutil.rmtree(os.path.join(os.getcwd(),'SESSION') )
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

    def test_SessionNode_creation_from_subject(self):
        #subject
        subject='myNode'
        node= SessionNode(subject=subject)
        self.assertEqual(node.subject.toPython(),'file:///'+subject)

        #http://
        subject='http://session_2022_05_20'
        node= SessionNode(subject=subject)
        self.assertEqual(node.subject.toPython(),subject)
        
        #erroneous char       
        subject='[[http://ses>sion_2022_<05_20]]'
        node= SessionNode(subject=subject)
        self.assertEqual(node.subject.toPython(),'http://__ses_sion_2022__05_20__')

    def test_SessionNode_creation_from_single_graph(self):
        node= SessionNode(graph=self.sessionGraph)
        self.assertEqual(node.subject,self.subject)
        
    def test_SessionNode_creation_from_data_graph(self):
        node= SessionNode(graph=self.resourceGraph)
        self.assertEqual(len(node.linkedNodes),len(self.linkedSubjects))

    def test_SessionNode_creation_from_combined_graph(self):
        node= SessionNode(graph=self.combinedGraph)
        self.assertEqual(node.subject,self.subject)
        self.assertEqual(len(node.linkedNodes),len(self.linkedSubjects))

    def test_SessionNode_creation_from_graph_path(self):
        subject=next(self.sessionGraph.subjects(RDF.type))
        node= SessionNode(graphPath=self.sessionGraphPath, subject=subject)
        self.assertEqual(node.subject,subject)
        
    def test_get_linked_nodes_from_self_linked_subjects(self):
        node= SessionNode(graph=self.sessionGraph)
        self.assertEqual(len(node.linkedSubjects),len(self.linkedSubjects))
        self.assertEqual(len(node.linkedNodes),0)
        node.get_linked_nodes(self.resourceGraph)
        self.assertEqual(len(node.linkedNodes),len(self.linkedSubjects))
        
    def test_get_linked_nodes_from_other_linked_subjects(self):
        node= SessionNode(graph=self.sessionGraph)
        self.assertEqual(len(node.linkedSubjects),len(self.linkedSubjects))
        self.assertEqual(len(node.linkedNodes),0)
        node.get_linked_nodes(self.resourceGraph,self.linkedSubjects)
        self.assertEqual(len(node.linkedNodes),len(self.linkedSubjects))

    def test_add_linked_nodes(self):
        node= SessionNode(graph=self.combinedGraph)
        node.linkedNodes.append(Node())
        self.assertEqual(len(node.linkedNodes),len(self.linkedSubjects)+1)
        self.assertEqual(len(node.linkedSubjects),len(self.linkedSubjects)+1)

    def test_SessionNode_creation_from_linked_nodes(self):
        node= SessionNode(linkedNodes=self.nodeList)
        self.assertEqual(len(node.linkedNodes),len(self.nodeList))

    def test_add_linked_nodes(self):
        node= SessionNode(linkedNodes=self.nodeList)
        nodelist2=[MeshNode(),Node()]
        node.add_linked_nodes(nodelist2)
        self.assertEqual(len(node.linkedNodes),len(self.linkedSubjects)+2)
    
    def test_add_linked_nodes_with_doubles(self):
        node= SessionNode(linkedNodes=self.nodeList)
        nodelist2=[MeshNode(),self.nodeList[0]]
        node.add_linked_nodes(nodelist2)
        self.assertEqual(len(node.linkedNodes),len(self.linkedSubjects)+1)

    def test_SessionNode_creation_from_resources(self):
        node= SessionNode(linkedResources=self.resources)
        containsMesh = False
        for newNode in node.linkedNodes:
            if('Mesh' in str(type(newNode))): containsMesh = True
        self.assertTrue(containsMesh)
        self.assertGreater(len(node.linkedNodes),0)

    def test_save_linked_resources(self):        
        node= SessionNode(graph=self.combinedGraph)
        node.save_linked_resources(self.resourcePath)

    def test_get_linked_resources(self):
        node= SessionNode(graphPath=self.combinedGraphPath)
        resources=node.get_linked_resources()
        self.assertEqual(len(resources),len(node.linkedNodes))

    def test_get_linked_resources_multiprocessing(self):
        node= SessionNode(graphPath=self.combinedGraphPath)
        resources=node.get_linked_resources_multiprocessing()
        self.assertEqual(len(resources),len(node.linkedNodes))

    def test_get_metadata_from_linked_nodes(self):
        node= SessionNode(graph=self.resourceGraph)
        node.get_metadata_from_linked_nodes()
        self.assertIsNotNone(node.orientedBoundingBox)

    def test_creation_from_subject_and_graph_and_graphPath(self):        
        subject=next(self.resourceGraph.subjects(RDF.type))
        node= SessionNode(subject=subject,graph=self.resourceGraph,graphPath=self.resourceGraphPath)
        self.assertEqual(node.subject,subject)

    def test_linked_nodes_to_graph(self):        
        node= SessionNode(graph=self.combinedGraph)
        node.linked_nodes_to_graph(os.path.join(self.resourcePath,'linkednodesGraph.ttl'))

    
    def test_session_to_graph(self):        
        node= SessionNode(graph=self.combinedGraph)
        node.session_to_graph(os.path.join(self.resourcePath,'combinedGraph.ttl'))


if __name__ == '__main__':
    unittest.main()
