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
        
        cls.bimGraphPath = cls.path / 'sampleBimGraph.ttl'

        #IFC1 (IfcWall)
        cls.bimGraphPath1= cls.bimGraphPath #cls.path / 'bimGraph1.ttl'
        cls.bimGraph1=Graph().parse(cls.bimGraphPath1)
        cls.ifcPath1=cls.path / 'IFC' / "Academiestraat_building_1.ifc"  
        cls.ifc1=ifcopenshell.open(str(cls.ifcPath1))   
        cls.ifcElement1= cls.ifc1.by_guid('0KysUSO6T3_gOJKtAiUE7d')
        cls.path1=cls.path / 'BIM' / "Basic_Wall_211_WA_Ff1_Glued_brickwork_sandlime_150mm_1118860_0KysUSO6T3_gOJKtAiUE7d.ply"
        cls.mesh1=gt.ifc_to_mesh(cls.ifcElement1)
        cls.subject1=next(s for s in cls.bimGraph1.subjects(RDF.type) if "file:///Basic_Wall_211_WA_Ff1_Glued_brickwork_sandlime_150mm_1118860_0KysUSO6T3_gOJKtAiUE7d" in s.toPython())
        
        #IFC2 (IfcSite)
        cls.bimGraphPath2= cls.bimGraphPath #cls.path / 'bimGraph2.ttl'
        cls.bimGraph2=Graph().parse(cls.bimGraphPath2)
        cls.ifcPath2=cls.path / 'IFC' / "Mariakerke_AWV_Conform_3D_BT_l72.ifc"
        cls.ifc2=ifcopenshell.open(str(cls.ifcPath2))   
        cls.ifcElement2= cls.ifc2.by_guid('3dzlFaOIb0bx0z6uxD96Sz')
        cls.path2=cls.path / 'BIM' / "BT1_Bodembedekking_WSV10_3dzlFaOIb0bx0z6uxD96Sz.ply"
        cls.mesh2=gt.ifc_to_mesh(cls.ifcElement2) 
        cls.subject2=next(s for s in cls.bimGraph2.subjects(RDF.type) if "file:///BT1_Bodembedekking_WSV10_3dzlFaOIb0bx0z6uxD96Sz" in s.toPython())
        
        #IFC3 (IfcSlab)
        cls.bimGraphPath3= cls.bimGraphPath #cls.path / 'bimGraph3.ttl'
        cls.bimGraph3=Graph().parse(cls.bimGraphPath3)
        cls.ifcPath3= cls.path / 'IFC' / "Academiestraat_parking.ifc"
        cls.ifc3=ifcopenshell.open(str(cls.ifcPath3))   
        cls.ifcElement3= cls.ifc3.by_guid('3fuhig3Pv7AexdYIkSgcdp')
        cls.path3= cls.path / 'BIM' / "174_SFO_Pile_type_1_CS_800kN_TS_250kN_1341745_3fuhig3Pv7AexdYIkSgcdp.ply"
        cls.mesh3=gt.ifc_to_mesh(cls.ifcElement3) 
        cls.subject3=next(s for s in cls.bimGraph3.subjects(RDF.type) if "file:///174_SFO_Pile_type_1_CS_800kN_TS_250kN_1341745_3fuhig3Pv7AexdYIkSgcdp" in s.toPython())
        
        #IFC4 (IfcDoor)
        cls.bimGraphPath4= cls.bimGraphPath #cls.path / 'bimGraph4.ttl'
        cls.bimGraph4=Graph().parse(cls.bimGraphPath4)
        cls.ifcPath4= cls.path / 'IFC' / "B1_ALG_Model.ifc"
        cls.ifc4=ifcopenshell.open(str(cls.ifcPath4))   
        cls.ifcElement4= cls.ifc4.by_guid('3M6cRe8S51TfU811R8bxHi')
        cls.path4= cls.path / 'BIM' / "2RA_doors_single_omlijsting_omlijsting_-_85_x_217_1855492_3M6cRe8S51TfU811R8bxHi.ply"
        cls.mesh4=gt.ifc_to_mesh(cls.ifcElement4) 
        cls.subject4=next(s for s in cls.bimGraph4.subjects(RDF.type) if "file:///2RA_doors_single_omlijsting_omlijsting_-_85_x_217_1855492_3M6cRe8S51TfU811R8bxHi" in s.toPython())
       
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
        if os.path.exists(os.path.join(os.getcwd(),'BIM') ):
            shutil.rmtree(os.path.join(os.getcwd(),'BIM') )
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

    def test_bimnode_creation_from_subject(self):
        #subject
        subject='myNode'
        node= BIMNode(subject=subject)
        self.assertEqual(node.subject.toPython(),'file:///'+subject)

        #http://
        subject='http://session_2022_05_20'
        node= BIMNode(subject=subject)
        self.assertEqual(node.subject.toPython(),subject)
        
        #erroneous char       
        subject='[[http://ses>sion_2022_<05_20]]'
        node= BIMNode(subject=subject)
        self.assertEqual(node.subject.toPython(),'http://__ses_sion_2022__05_20__')

    def test_bimnode_creation_from_graph(self):
        subject=next(self.bimGraph1.subjects(RDF.type))
        node= BIMNode(graph=self.bimGraph1, subject=subject)
        self.assertEqual(node.subject.toPython(),subject.toPython())
        object=self.bimGraph1.value(subject,self.v4d['faceCount'])
        self.assertEqual(node.faceCount,object.toPython())
        
    def test_bimnode_creation_from_graph_path(self):
        subject=next(self.bimGraph2.subjects(RDF.type))
        node= BIMNode(graphPath=self.bimGraphPath2, subject=subject)
        self.assertEqual(node.subject.toPython(),subject.toPython())
        object=self.bimGraph2.value(subject,self.v4d['faceCount'])
        self.assertEqual(node.faceCount,object.toPython())
        
    def test_bimnode_creation_from_path(self):
        #path1 without getResource
        node= BIMNode(path=self.path1)
        self.assertEqual(node.name,ut.get_filename(self.path1))
        self.assertIsNone(node._resource)

        #path2 with getResource
        node= BIMNode(path=self.path2,getResource=True)        
        self.assertEqual(node.name,ut.get_filename(self.path2))
        self.assertIsNotNone(node._resource)

        #path3 
        node= BIMNode(path=self.path3,getResource=True)
        self.assertEqual(node.name,ut.get_filename(self.path3))
        self.assertIsNotNone(node._resource)

    def test_bimnode_creation_from_ifcpath(self):
        #path1 without extra info -> take first IfcElement
        node= BIMNode(ifcPath=self.ifcPath3)
        self.assertIsNotNone(node.name)

        #path2 with getResource without extra info -> take first IfcElement
        node= BIMNode(ifcPath=self.ifcPath4,getResource=True)        
        self.assertIsNotNone(node.name)
        self.assertIsNotNone(node.resource)

 
    def test_bimnode_creation_from_ifcElement(self):        
        #ifcElement
        node= BIMNode(resource=self.ifcElement1)
        self.assertEqual(node.subject.toPython(),self.subject1.toPython())

        #ifcElement + getResource
        node= BIMNode(resource=self.ifcElement2,ifcPath=self.ifcPath2)
        self.assertEqual(node.subject,self.subject2)
        self.assertIsNotNone(node.resource)
        self.assertIsNotNone(node.ifcPath)

    def test_bimnode_creation_from_mesh(self):
        #mesh1
        node= BIMNode(resource=self.mesh1)
        self.assertEqual(node.faceCount,len(self.mesh1.triangles))
        #mesh2
        node= BIMNode(resource=self.mesh2)
        self.assertEqual(node.faceCount,len(self.mesh2.triangles))
        #mesh3
        node= BIMNode(resource=self.mesh3)
        self.assertEqual(node.faceCount,len(self.mesh3.triangles))

    def test_bimnode_creation_from_trimesh(self):
        myTrimesh=gt.mesh_to_trimesh(self.mesh2)
        node= BIMNode(resource=myTrimesh)
        self.assertEqual(node.faceCount,len(self.mesh2.triangles))

    def test_creation_from_subject_and_graph_and_graphPath(self):        
        subject=next(self.bimGraph3.subjects(RDF.type))
        node= BIMNode(subject=subject,graph=self.bimGraph3,graphPath=self.bimGraphPath3)
        self.assertEqual(node.subject.toPython(),subject.toPython())
        node.to_graph()
        self.assertTrue((subject, self.v4d['faceCount'], Literal(node.faceCount)) in self.bimGraph3)
   
    def test_creation_from_subject_and_path(self):        
        node= BIMNode(subject=self.subject2,path=self.path2,getResource=True)
        self.assertEqual(node.subject.toPython(),self.subject2.toPython())
        node.to_graph()        
        self.assertAlmostEqual(np.asarray(node.orientedBounds)[0,0],np.asarray(self.mesh2.get_oriented_bounding_box().get_box_points())[0,0],delta=0.01)
        
    def test_creation_from_subject_and_path_and_graph(self):      
        node= BIMNode(subject=self.subject3,path=self.path3,graph=self.bimGraph3,getResource=True)
        self.assertEqual(node.subject,self.subject3)
        node.to_graph()
        initialGraph=ut.get_subject_graph(self.bimGraph3,subject=self.subject3)
        self.assertAlmostEqual(node.cartesianBounds[0],self.mesh3.get_min_bound()[0],delta=0.01)

    def test_creation_from_mesh_and_path (self):      
        node= BIMNode(resource=self.mesh4,path=self.path4)
        self.assertEqual(node.subject,self.subject4)

    def test_creation_from_subject_and_mesh_and_path_and_graph(self):      
        node= BIMNode(subject=self.subject3,resource=self.mesh3,path=self.path3, graph=self.bimGraph3)
        self.assertEqual(node.subject,self.subject3)
        node.to_graph()
        object=node.graph.value(node.subject,self.v4d['path'])
        self.assertEqual(ut.parse_path(object.toPython()),(Path("BIM") / (ut.get_filename(self.path3) + '.ply')).as_posix() )

    def test_creation_from_subject_mesh_path_ifcPath_graph(self):      
        node= BIMNode(subject=self.subject4,resource=self.mesh4,path=self.path4, ifcPath=self.ifcPath4, graph=self.bimGraph4)
        self.assertEqual(node.subject,self.subject4 )
        node.to_graph()
        object=node.graph.value(node.subject,self.v4d['path'])
        self.assertEqual(ut.parse_path(object.toPython()),(Path("BIM") / (ut.get_filename(self.path4) + '.ply')).as_posix() )

    def test_creation_from_subject_mesh_path_ifcPath_globalId_graph(self):      
        node= BIMNode(subject=self.subject1,resource=self.mesh1,path=self.path1, ifcPath=self.ifcPath1, globalId=self.ifcElement1.GlobalId, graph=self.bimGraph1)
        self.assertEqual(node.subject,self.subject1)
        node.to_graph()
        object=node.graph.value(node.subject,self.v4d['path'])
        self.assertEqual(ut.parse_path(object.toPython()),(Path("BIM") / (ut.get_filename(self.path1) + '.ply')).as_posix() )

    def test_node_creation_with_get_resource(self):
        #mesh
        node= BIMNode(resource=self.mesh1)
        self.assertIsNotNone(node._resource)

        #path without getResource
        node= BIMNode(path=self.path2)
        self.assertIsNone(node._resource)

        #path with getResource
        node= BIMNode(path=self.path3,getResource=True)
        self.assertIsNotNone(node._resource)

        #graph with get resource
        node= BIMNode(subject=self.subject2,graph=self.bimGraph2,getResource=True)
        self.assertIsNone(node._resource)
        
        #graphPath with get resource
        node= BIMNode(subject=self.subject3,graphPath=self.bimGraphPath3,getResource=True)
        self.assertIsNotNone(node._resource)

    def test_clear_resource(self):
        #mesh
        node= BIMNode(resource=self.mesh1)
        self.assertIsNotNone(node.resource)
        del node.resource
        self.assertIsNone(node.resource)

    # def test_save_resource(self):
    #     #no mesh -> False
    #     node= BIMNode()
    #     self.assertFalse(node.export_resource())

    #     #directory
    #     node= BIMNode(mesh=self.mesh2)
    #     self.assertTrue(node.export_resource(os.path.join(self.path,'resources')))

    #     #graphPath        
    #     node= BIMNode(mesh=self.mesh2,graphPath=self.bimGraphPath2)
    #     self.assertTrue(node.export_resource())

    #     #no path or graphPath
    #     node= BIMNode(mesh=self.mesh4)        
    #     self.assertTrue(node.export_resource())

    #     #invalid extension -> error
    #     node= BIMNode(mesh=self.mesh3)
    #     self.assertRaises(ValueError,node.export_resource,os.path.join(self.path,'resources'),'.kjhgfdfg')

    #     #.ply -> ok
    #     node= BIMNode(mesh=self.mesh2)
    #     self.assertTrue(node.export_resource(os.path.join(self.path,'resources'),'.ply'))
    #     self.assertEqual(node.path,os.path.join(self.path,'resources',node.name+'.ply'))

    #     #.obj -> ok
    #     node= BIMNode(mesh=self.mesh3)
    #     self.assertTrue(node.export_resource(os.path.join(self.path,'resources'),'.obj'))
    #     self.assertEqual(node.path,os.path.join(self.path,'resources',node.name+'.obj'))
        
    #     #path -> new name
    #     node= BIMNode(subject=URIRef('myMesh'),path=self.path2,getResource=True)
    #     self.assertTrue(node.export_resource())
    #     files=ut.get_list_of_files(ut.get_folder(node.path))
    #     self.assertTrue( node.path in files)
        
    #     #graphPath with directory
    #     node=BIMNode(subject=self.subject2,graphPath=self.bimGraphPath2, mesh=self.mesh3)
    #     self.assertTrue(node.export_resource(os.path.join(self.path,'resources')))
    #     files=ut.get_list_of_files(ut.get_folder(node.path))
    #     self.assertTrue(node.path in files)

    #     #graph with new subject
    #     node=BIMNode(subject=self.subject4,grap=self.bimGraph4, mesh=self.mesh4)
    #     node.name='myMesh'
    #     self.assertTrue(node.export_resource())
    #     files=ut.get_list_of_files(ut.get_folder(node.path))
    #     self.assertTrue(node.path in files)

    def test_get_resource(self):
        #mesh
        node=BIMNode(resource=self.mesh3)  
        self.assertIsNotNone(node.get_resource())

        #no mesh
        del node.resource
        self.assertIsNone(node.get_resource())

        #graphPath with getResource
        node=BIMNode(graphPath=self.bimGraphPath2,subject=self.subject2,getResource=True)
        self.assertIsNotNone(node.get_resource())

    def test_get_metadata_from_resource(self):
        #mesh
        node=BIMNode(resource=self.mesh3)  
        self.assertIsNotNone(node.orientedBounds)
        self.assertIsNotNone(node.cartesianBounds)
        self.assertIsNotNone(node.cartesianTransform)
        self.assertIsNotNone(node.faceCount)
        self.assertIsNotNone(node.pointCount)

        #ifcElement
        node=BIMNode(resource=self.ifcElement4)  
        self.assertIsNotNone(node.orientedBounds)
        self.assertIsNotNone(node.cartesianBounds)
        self.assertIsNotNone(node.cartesianTransform)
        self.assertIsNotNone(node.faceCount)
        self.assertIsNotNone(node.pointCount)

        #ifcPath and globalId
        node=BIMNode(ifcPath=self.ifcPath1,globalId=self.ifcElement1.GlobalId, getResource=True)  
        self.assertIsNotNone(node.orientedBounds)
        self.assertIsNotNone(node.cartesianBounds)
        self.assertIsNotNone(node.cartesianTransform)
        self.assertIsNotNone(node.faceCount)
        self.assertIsNotNone(node.pointCount)

        #graphPath
        node=BIMNode(graphPath=self.bimGraphPath4,subject=self.subject4,getResource=True)
        self.assertIsNotNone(node.orientedBounds)
        self.assertIsNotNone(node.cartesianBounds)
        self.assertIsNotNone(node.cartesianTransform)
        self.assertIsNotNone(node.faceCount)
        self.assertIsNotNone(node.pointCount)

    def test_set_path(self):
        #valid path
        node=BIMNode()
        node.path= self.path1
        self.assertEqual(node.path,self.path1.as_posix())

        #preexisting
        node=BIMNode(path=self.path4)
        self.assertEqual(node.path,self.path4.as_posix())

        #graphPath & name
        node=BIMNode(subject=self.subject4,graphPath=self.bimGraphPath4)
        node.get_path()
        self.assertEqual(node.path,self.path4.as_posix())

    def test_set_ifc_path(self):
        #valid path
        node=BIMNode(ifcPath=self.ifcPath2)
        self.assertEqual(node.ifcPath,self.ifcPath2.as_posix())

        #invalid
        self.assertRaises(ValueError,BIMNode,ifcPath='qsffqsdf.dwg')

    def get_metadata_from_ifc_path(self):
        #ifc1
        a=0
        selector = Selector()
        for ifcElement in selector.parse(self.ifc1, '.ifcObject'):
            a+=1
            node=BIMNode(ifcPath=self.ifcPath1,globalId=ifcElement.GlobalId)            
            self.assertEqual(node.className,ifcElement.is_a())
            if a==100:
                break
        
        #check error no global id in ifc
        node= BIMNode()
        self.assertRaises(ValueError,BIMNode,ifcPath=self.ifcPath4,globalId='kjhgfdfg')

    def test_get_metadata_from_ifcElement(self):
        #ifc3
        a=0
        selector = Selector()
        for ifcElement in selector.parse(self.ifc3, '.ifcObject'):
            a+=1
            node=BIMNode(resource=ifcElement)
            self.assertEqual(node.className,ifcElement.is_a())
            if a==100:
                break

        #ifc4
        a=0
        selector = Selector()
        for ifcElement in selector.parse(self.ifc4, '.ifcObject'):
            a+=1
            node=BIMNode(resource=ifcElement)
            self.assertEqual(node.className,ifcElement.is_a())
            if a==100:
                break

if __name__ == '__main__':
    unittest.main()
