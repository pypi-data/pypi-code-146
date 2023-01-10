"""
ImageNode - a Python Class to govern the data and metadata of image data (JPG,PNG,XML,XMP)
"""
#IMPORT PACKAGES
from distutils import extension
import xml.etree.ElementTree as ET
import cv2
import PIL
from rdflib import Graph, URIRef
import numpy as np
import os
import open3d as o3d
import math

#IMPORT MODULES
from geomapi.nodes import Node
import geomapi.utils as ut
import geomapi.utils.geometryutils as gt


class OrthoNode(Node):
    # class attributes
    
    def __init__(self,  graph : Graph = None, 
                        graphPath:str=None,
                        subject : URIRef = None,
                        path : str=None, 
                        xmpPath: str = None,
                        xmlPath: str = None,
                        xmlIndex: int = None,
                        getResource : bool = False,
                        image : np.ndarray  = None, 
                        **kwargs): 
        """
        Creates an OrthoNode. Overloaded function.

        Args:
            0.graph (RDFlib Graph) : Graph with a single subject (if multiple subjects are present, only the first will be used to initialise the MeshNode)
            
            1.graphPath (str):  Graph file path with a single subject (if multiple subjects are present, only the first will be used to initialise the MeshNode)

            2.path (str) : path to .jpg or .png file (Note that this node will also contain the data)

            3.orthomosaic (ndarray) : OpenCV image as numpy ndarray (Note that this node will also contain the data)
                
        Returns:
            A OrthoNode with metadata (if you also want the data, call node.get_resource() method)
        """  
        self.path=path
        self.image = image
        self.xResolution = None # (Float) 
        self.yResolution = None # (Float) 
        self.resolutionUnit = None # (string)
        self.imageWidth = None # (int) number of pixels
        self.imageHeight = None  # (int) number of pixels
        super().__init__(   graph= graph,
                            graphPath= graphPath,
                            subject= subject,
                            **kwargs) 
        
        
        #self.gsd =gsd?
 
