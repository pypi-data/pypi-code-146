import os
from sklearn.model_selection import train_test_split
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras import layers
from keras.models import load_model


class DataService():
    def __init__(self, image_size,batch_size,trained_model_dir,model_path):
        self.image_size = image_size
        self.batch_size = batch_size
        self.trained_model_dir = trained_model_dir
        self.model_path = model_path

    def load_data(self):    
        (x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
        new_x_train,  x_val, new_y_train, y_val = train_test_split(x_train, y_train, test_size=.2)
        return (new_x_train, new_y_train), (x_test, y_test), (x_val, y_val)

    def make_datasets(self,images, labels, is_train=False):
        data_augmentation = keras.Sequential(
            [layers.RandomCrop(self.image_size, self.image_size), 
            layers.RandomFlip("horizontal"),],
            name="data_augmentation",
        )

        dataset = tf.data.Dataset.from_tensor_slices((images, labels))
        if is_train:
            dataset = dataset.shuffle(self.batch_size * 10)
        dataset = dataset.batch(self.batch_size)
        if is_train:
            dataset = dataset.map(
                lambda x, y: (data_augmentation(x), y), num_parallel_calls=tf.data.AUTOTUNE
            )
        return dataset.prefetch(tf.data.AUTOTUNE)

    def save_pipeline_keras(self,model):   
        path =  os.path.join(self.trained_model_dir, self.model_path)
        model.save(path)

    def load_pipeline_keras(self):
        path =  os.path.join(self.trained_model_dir, self.model_path)
        return load_model(path)

if __name__ == '__main__':
            
    ds = DataService(32,128,"","")
    (new_x_train, new_y_train), (x_test, y_test), (x_val, y_val) = ds.load_data()

    print(f"Training data samples: {len(new_x_train)}")
    print(f"Validation data samples: {len(x_val)}")
    print(f"Test data samples: {len(x_test)}")

    train_dataset = ds.make_datasets(new_x_train, new_y_train.reshape(-1), is_train=True)
    val_dataset = ds.make_datasets(x_val, y_val.reshape(-1))
    test_dataset = ds.make_datasets(x_test, y_test.reshape(-1))
   
