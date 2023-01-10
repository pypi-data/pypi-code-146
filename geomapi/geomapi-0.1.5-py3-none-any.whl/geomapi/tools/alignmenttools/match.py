import math
import cv2
from geomapi.nodes import Node, ImageNode
import geomapi.tools.alignmenttools.params as params
import numpy as np

class Match:
    """The generic match object to determine the relation between 2 geomapi.Node objects"""

    _matchType = "" # Defines the type of match

    def __init__(self, node1: Node, node2: Node) -> None:
        """The default constructor

        Args:
            node1 (Node): The first node, defines the transfrom from
            node2 (Node): The second node, defines the transformation to
        """
        self.node1: Node = node1                    #: The first node, defines the transfrom from
        self.node2: Node = node2                    #: The second node, defines the transformation to

        self.matches = None
        self.matchError: float = math.inf           #: A single value indicating the quality of the match, lower is better
        self.matchAmount: float = 0                 #: The number of good matches
        self.transformation: np.array = np.ones(4)  #: The 4x4 transformationmatrix defined from 1 to 2
        pass
    
    # The initial matching to evaliaute the quality of the match
    def get_matches(self):
        """Finds the matches between 2 objects"""
        print("WARNING: Calling 'get_matches()' on a generic Match object, please use a 2D or 3D match instead")

    # The full transormation calculation
    def get_transformation(self):
        """Returns the estimated transformation between the 2 objects"""
        print("WARNING: Calling 'get_transformation()' on a generic Match object, please use a 2D or 3D match instead")

class Match2d (Match):

    _matchType = "2d"

    def __init__(self, imageNode1: ImageNode, imageNode2: ImageNode) -> None:
        """The default constructor

        Args:
            imageNode1 (ImageNode): The first node, defines the transfrom from
            imageNode2 (ImageNode): The second node, defines the transformation to
        """
        super().__init__(imageNode1, imageNode2)

        self.image1 = None
        self.image2 = None
    
    def get_matches(self):
        """Finds matches between the 2 images"""

        # Inherit the super functionality
        super().get_matches()

        if(self.matches is None):
            # get cv2 ORb features
            self.image1 = self.node1.get_resource()
            self.image2 = self.node2.get_resource()

            if(not (self.image1 & self.image2)):
                print("Node 1 or 2 do not have an image resource to get matches from")
                return None

            #image1.get_cv2_features(params.MAX_2D_FEATURES)

            # Match features.
            matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = matcher.match(self.image1.descriptors, self.image2.descriptors, None)
            # Sort matches by score
            matches = sorted(matches, key = lambda x:x.distance)
            # only use the best features
            if(len(matches) < params.MAX_2D_MATCHES):
                print("only found", len(matches), "good matches")
                matchError = math.inf
            else:
                matches = matches[:params.MAX_2D_MATCHES]
                # calculate the match score
                # right now, it's just the average distances of the best points
                matchError = 0
                for match in matches:
                    matchError += match.distance
                matchError /= len(matches)
            self.matches = matches
            self.matchError = matchError
            self.matchAmount = len(matches)
        return self.matches


class Match3d (Match):
    
    _matchType = "3d"
    
    def __init__(self) -> None:
        #create a new 3d match instance
        pass


