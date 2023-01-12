import cv2 as cv

class GetMatrix():

    def __init__(self, address):

        self.matrix = cv.imread(address)
        #self.matrix = cv.resize(self.image, (0, 0), fx = 0.5, fy = 0.5)
        return

    def save(self, filename, matrix):
        self.filename = filename
        cv.imwrite(filename, matrix)
        #(Image.fromarray(matrix)).save(filename)
        print('Image saved successfully.')
        self.verify = cv.imread(filename)
        return self.verify

