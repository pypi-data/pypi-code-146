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
from PIL import Image
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
       
        #IMGGRAPH
        cls.imgGraphPath= cls.path / 'sampleImgGraph.ttl' #cls.path / 'imgGraph.ttl'
        cls.imgGraph=Graph().parse(cls.imgGraphPath)

        #IMG1 (image)
        cls.path1= cls.path / 'IMG' / "DJI_0067.JPG"        
        cls.img1=cv2.imread(str(cls.path1))          
        cls.subject1=next(s for s in cls.imgGraph.subjects(RDF.type) if "file:///DJI_0067" in s.toPython())
        
        #IMG2 (PIL Image)
        cls.path2= cls.path / 'IMG' / "DJI_0070.JPG"        
        cls.img2=Image.open(cls.path2)     
        cls.subject2=next(s for s in cls.imgGraph.subjects(RDF.type) if "file:///DJI_0070" in s.toPython())
        
        #IMG3 (XMP file)
        cls.path3= cls.path / 'IMG' / "IMG_2173.JPG" 
        cls.xmpPath3= cls.path / 'IMG' / "IMG_2173.xmp"     
        cls.img3=Image.open(cls.path3)     
        cls.subject3=next(s for s in cls.imgGraph.subjects(RDF.type) if "file:///IMG_2173" in s.toPython())
         
        #IMG3 (XML large file)
        cls.path4= cls.path / 'IMG' / "101_0366_0036.jpg" 
        cls.xmlPath4= cls.path / 'IMG' / "ReferenceLAMBERT08_TAW.xml"    
        cls.img4=Image.open(cls.path4)     
        cls.subject4=next(s for s in cls.imgGraph.subjects(RDF.type) if "file:///101_0366_0036" in s.toPython())
        
        #IMG5 (XML large file)
        cls.path5= cls.path / 'IMG' / "IMG_202200706_00_ (1).jpg" 
        cls.xmlPath5=  cls.path / 'IMG' / "camera_position.xml"  
        cls.img5=Image.open(cls.path5)
        cls.subject5=next(s for s in cls.imgGraph.subjects(RDF.type) if "file:///IMG_202200706_00___1_" in s.toPython())

        #RESOURCES
        cls.resourcePath= cls.path / "resources"
        if not os.path.exists(cls.resourcePath):
            os.mkdir(cls.resourcePath)

        #FILES
        cls.files=ut.get_list_of_files(cls.path)

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
        if os.path.exists(os.path.join(os.getcwd(),'IMG') ):
            shutil.rmtree(os.path.join(os.getcwd(),'IMG') )
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

    def test_ImageNode_creation_from_subject(self):
        #subject
        subject='myNode'
        node= ImageNode(subject=subject)
        self.assertEqual(node.subject.toPython(),'file:///'+subject)

        #http://
        subject='http://session_2022_05_20'
        node= ImageNode(subject=subject)
        self.assertEqual(node.subject.toPython(),subject)
        
        #erroneous char       
        subject='[[http://ses>sion_2022_<05_20]]'
        node= ImageNode(subject=subject)
        self.assertEqual(node.subject.toPython(),'http://__ses_sion_2022__05_20__')

    def test_ImageNode_creation_from_graph(self):
        subject=next(self.imgGraph.subjects(RDF.type))
        node= ImageNode(graph=self.imgGraph, subject=subject)
        self.assertEqual(node.subject,subject)
        
    def test_ImageNode_creation_from_graph_path(self):
        subject=next(self.imgGraph.subjects(RDF.type))
        node= ImageNode(graphPath=self.imgGraphPath, subject=subject)
        self.assertEqual(node.subject,subject)
        
    def test_ImageNode_creation_from_path(self):
        #path1 without getResource
        node= ImageNode(path=self.path1)
        self.assertEqual(node.name,ut.get_filename(self.path1))
        self.assertIsNone(node._resource)

        #path2 with getResource
        node= ImageNode(path=self.path2,getResource=True)        
        self.assertEqual(node.name,ut.get_filename(self.path2))
        self.assertEqual(node.imageHeight,self.img2.height)

        #path3 
        node= ImageNode(path=self.path3,getResource=True)
        self.assertEqual(node.name,ut.get_filename(self.path3))
        self.assertEqual(node.imageHeight,self.img3.height)

    def test_ImageNode_creation_from_xmpPath(self):
        #path without extra info 
        node= ImageNode(xmpPath=self.xmpPath3)
        self.assertIsNotNone(node.name)

        #path with getResource without extra info 
        node= ImageNode(xmpPath=self.xmpPath3,getResource=True)        
        self.assertIsNotNone(node.name)
        self.assertIsNotNone(node.resource)


    def test_ImageNode_creation_from_xmlPath(self):
        
        
        #path without extra info 
        node= ImageNode(xmlPath=self.xmlPath4,subject='101_0366_0037')
        self.assertIsNotNone(node.name)

        #path with subject
        node= ImageNode(xmlPath=self.xmlPath4,subject='101_0366_0037',getResource=True)        
        self.assertIsNotNone(node.name)
        self.assertIsNotNone(node.resource)

    def test_ImageNode_creation_from_resource(self):
        #img1
        node= ImageNode(resource=self.img1)
        self.assertEqual(node.imageHeight,self.img1.shape[0])
        #img2
        node= ImageNode(resource=self.img2)
        self.assertEqual(node.imageHeight,self.img1.shape[0])
        #img3
        node= ImageNode(resource=self.img3)
        self.assertEqual(node.imageHeight,self.img3.height)

    def test_creation_from_subject_and_graph_and_graphPath(self):        
        subject=next(self.imgGraph.subjects(RDF.type))
        node= ImageNode(subject=subject,graph=self.imgGraph,graphPath=self.imgGraphPath)
        self.assertEqual(node.subject,subject)
        
    def test_creation_from_subject_and_path(self):        
        node= ImageNode(subject=self.subject2,path=self.path2,getResource=True)
        self.assertEqual(node.subject,self.subject2)
        node.to_graph()
        self.assertEqual(node.imageHeight,self.img2.height)
        
    def test_creation_from_subject_and_path_and_graph(self):      
        node= ImageNode(subject=self.subject3,path=self.path3,graph=self.imgGraph,getResource=True)
        self.assertEqual(node.subject,self.subject3)
        node.to_graph()
        initialGraph=ut.get_subject_graph(self.imgGraph,subject=self.subject3)
        self.assertEqual(len(node.graph),len(initialGraph))

    def test_creation_from_resource_and_path (self):      
        node= ImageNode(resource=self.img5,path=self.path5)
        self.assertEqual(node.subject,self.subject5)

    def test_creation_from_subject_and_resource_and_path_and_graph(self):      
        node= ImageNode(subject=self.subject3,resource=self.img3,path=self.path3, graph=self.imgGraph)
        self.assertEqual(node.subject,self.subject3)
        node.to_graph()
        object=node.graph.value(node.subject,self.v4d['path'])
        self.assertEqual(str(Path(object.toPython())),os.path.join("IMG",ut.get_filename(self.path3)+'.JPG') )

    def test_creation_from_subject_resource_path_xmpPath_graph(self):      
        node= ImageNode(subject=self.subject3,resource=self.img3,path=self.path3, xmpPath=self.xmpPath3, graph=self.imgGraph)
        self.assertEqual(node.subject,self.subject3)
        node.to_graph()
        object=node.graph.value(node.subject,self.v4d['path'])
        self.assertEqual(str(Path(object.toPython())),os.path.join(self.path,"IMG",ut.get_filename(self.path3)+'.JPG') )

    def test_node_creation_with_get_resource(self):
        #mesh
        node= ImageNode(resource=self.img1)
        self.assertIsNotNone(node._resource)

        #path without getResource
        node= ImageNode(path=self.path2)
        self.assertIsNone(node._resource)

        #path with getResource
        node= ImageNode(path=self.path5,getResource=True)
        self.assertIsNotNone(node._resource)

        #graph with get resource
        node= ImageNode(subject=self.subject2,graph=self.imgGraph,getResource=True)
        self.assertIsNone(node._resource)
        
        #graphPath with get resource
        node= ImageNode(subject=self.subject3,graphPath=self.imgGraphPath,getResource=True)
        self.assertIsNotNone(node._resource)

    def test_clear_resource(self):
        #mesh
        node= ImageNode(resource=self.img1)
        self.assertIsNotNone(node._resource)
        del node.resource
        self.assertIsNone(node._resource)

    def test_save_resource(self):
        #no mesh -> False
        node= ImageNode()
        self.assertFalse(node.save_resource())

        #directory
        node= ImageNode(resource=self.img2)
        self.assertTrue(node.save_resource(os.path.join(self.path,'resources')))

        #graphPath        
        node= ImageNode(resource=self.img2,graphPath=self.imgGraphPath)
        self.assertTrue(node.save_resource())

        #no path or graphPath
        node= ImageNode(resource=self.img4)        
        self.assertTrue(node.save_resource())

        #path -> new name
        node= ImageNode(subject=URIRef('myImg'),path=self.path2,getResource=True)
        self.assertTrue(node.save_resource())
        self.assertTrue( node.path in self.files)
        
        #graphPath with directory
        node=ImageNode(subject=self.subject5,graphPath=self.imgGraphPath, resource=self.img5)
        self.assertTrue(node.save_resource(os.path.join(self.path,'resources')))

        #graph with new subject
        node=ImageNode(subject=self.subject4,graph=self.imgGraph, resource=self.img4)
        node.subject='myImg'
        self.assertTrue(node.save_resource())

    def test_get_resource(self):
        #mesh
        node=ImageNode(resource=self.img3)  
        self.assertIsNotNone(node.get_resource())

        #no mesh
        del node.resource
        self.assertIsNone(node.get_resource())

        #graphPath with getResource
        node=ImageNode(graphPath=self.imgGraphPath,subject=self.subject2,getResource=True)
        self.assertIsNotNone(node.get_resource())

    def test_set_path(self):
        #valid path
        node=ImageNode()
        node.path= self.path1
        self.assertEqual(node.path,self.path1.as_posix())

        #preexisting
        node=ImageNode(path=self.path4)
        self.assertEqual(node.path,self.path4.as_posix())

        #graphPath & name
        node=ImageNode(subject=self.subject5,graphPath=self.imgGraphPath)
        node.get_path()
        self.assertEqual(node.path,self.path5.as_posix())

    def test_set_xmp_path(self):
        #valid path
        node=ImageNode(xmpPath=self.xmpPath3)
        self.assertEqual(node.xmpPath,self.xmpPath3.as_posix())

        #invalid
        self.assertRaises(ValueError,ImageNode,xmpPath='qsffqsdf.dwg')

    def test_set_xml_path(self):
        #valid path
        node=ImageNode()
        node.xmlPath=self.xmlPath4
        self.assertEqual(node.xmlPath,self.xmlPath4.as_posix())

        #invalid
        self.assertRaises(ValueError,ImageNode,xmlPath='qsffqsdf.dwg')

if __name__ == '__main__':
    unittest.main()
