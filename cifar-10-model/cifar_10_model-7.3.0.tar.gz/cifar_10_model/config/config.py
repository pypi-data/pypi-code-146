# The Keras model loading function does not play well with
# Pathlib at the moment, so we are using the old os module
# style
import os

class Config():
    def __init__(self):        
        self.PWD = os.path.dirname(os.path.abspath(__file__))
        self.PACKAGE_ROOT = os.path.abspath(os.path.join(self.PWD, '..'))
        self.TRAINED_MODEL_DIR = os.path.join(self.PACKAGE_ROOT, 'trained_models')
        self.TESTING_IMAGES = os.path.join(self.PACKAGE_ROOT, 'testing_images')

        # MODEL FITTING
        self.IMAGE_SIZE = 32 # 32 for testing, 150 for final model

        #Hyperparameters
        self.BATCH_SIZE = 128
        self.OPTIMIZER = "adam"
        self.EPOCHS = 10  # 1 for testing, 10 for final model

        # MODEL PERSISTING
        self.MODEL_NAME = 'cnn_model'
        self.MODEL_PATH = "cnn_model.h5"
