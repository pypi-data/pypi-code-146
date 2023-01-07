# for the convolutional network
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten,BatchNormalization
from keras.callbacks import ModelCheckpoint

def cnn_model(config,
              kernel_size = (3,3),
              pool_size= (2,2),
              first_filters = 64,
              second_filters = 128,
              third_filters = 64,
              dropout_dense = 0.2):
        
    model = Sequential()

    #Layer1
    model.add(Conv2D(first_filters, kernel_size,strides=1, activation = 'relu', 
                    input_shape = (config.IMAGE_SIZE, config.IMAGE_SIZE, 3)))
    model.add(BatchNormalization(momentum=0.15, axis=-1))
    model.add(Conv2D(first_filters, kernel_size, activation = 'relu', 
                    input_shape = (config.IMAGE_SIZE, config.IMAGE_SIZE, 3)))
    model.add(BatchNormalization(momentum=0.15, axis=-1))
    model.add(MaxPooling2D(pool_size = pool_size, strides=2)) 

    #Layer2
    model.add(Conv2D(second_filters, kernel_size,strides=1, activation = 'relu', 
                    input_shape = (config.IMAGE_SIZE, config.IMAGE_SIZE, 3)))
    model.add(BatchNormalization(momentum=0.15, axis=-1))
    model.add(Conv2D(second_filters, kernel_size, activation = 'relu', 
                    input_shape = (config.IMAGE_SIZE, config.IMAGE_SIZE, 3)))
    model.add(BatchNormalization(momentum=0.15, axis=-1))
    model.add(MaxPooling2D(pool_size = pool_size, strides=2)) 

    #Layer3
    model.add(Conv2D(third_filters, kernel_size,strides=1, activation = 'relu', 
                    input_shape = (config.IMAGE_SIZE, config.IMAGE_SIZE, 3))) 
    model.add(BatchNormalization(momentum=0.15, axis=-1))
    model.add(Conv2D(third_filters, kernel_size, activation = 'relu', 
                    input_shape = (config.IMAGE_SIZE, config.IMAGE_SIZE, 3)))
    model.add(BatchNormalization(momentum=0.15, axis=-1))
    model.add(MaxPooling2D(pool_size=(1,1), strides=1))

    model.add(Flatten())
    model.add(Dense(1024, activation = "relu"))
    model.add(Dropout(dropout_dense))
    model.add(Dense(512, activation = "relu"))
    model.add(Dropout(dropout_dense))
    model.add(Dense(10, activation = "relu"))

    model.compile(
        optimizer=config.OPTIMIZER,
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    return model

def callbacks_list(model_path, moitor_mod = "val_accuracy", save_best=True, save_weights=True):

    return [ModelCheckpoint(
        model_path,
        monitor=moitor_mod,
        save_best_only=save_best,
        save_weights_only=save_weights,
    )]         

                              
if __name__ == '__main__':

    #Loading config module.
    from config import Config
    c = Config()
    model = cnn_model(c)
    model.summary()
    
    from processing.data_management import DataService
    dm = DataService(c.IMAGE_SIZE, c.BATCH_SIZE,c.TRAINED_MODEL_DIR, c.MODEL_PATH)
    (new_x_train, new_y_train), (x_test, y_test), (x_val, y_val) = dm.load_data()

    print(f"Training data samples: {len(new_x_train)}")
    print(f"Validation data samples: {len(x_val)}")
    print(f"Test data samples: {len(x_test)}")

    train_dataset = dm.make_datasets(new_x_train, new_y_train.reshape(-1), is_train=True)
    val_dataset = dm.make_datasets(x_val, y_val.reshape(-1))
    test_dataset = dm.make_datasets(x_test, y_test.reshape(-1))

    model = cnn_model(c)
    model.summary()
    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=c.EPOCHS,
        callbacks=[callbacks_list(c.MODEL_PATH)],
    )
