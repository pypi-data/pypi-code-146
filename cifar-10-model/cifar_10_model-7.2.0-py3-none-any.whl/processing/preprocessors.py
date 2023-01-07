import cv2
import tensorflow as tf

class Preprocessor():
  def __init__(self,image_size):
    self.image_size = image_size
    
  def im_resize(self,im):
      im = cv2.resize(im, (self.image_size, self.image_size))
      return im

  def convert_to_tensor(self,im):
    return tf.expand_dims(tf.convert_to_tensor(im, dtype=tf.float32), axis=0)


