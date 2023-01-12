import cv2 as cv

class GetMatrix():

    def __init__(self, address):
        self.matrix = cv.imread(address)
        