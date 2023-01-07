import numpy as np

class Predict():
    def __init__(self, dm, p):
        self.cifar10_classes = {
            0: 'airplane',
            1: 'automobile',
            2: 'bird',
            3: 'cat',
            4: 'deer',
            5: 'dog',
            6: 'frog',
            7: 'horse',
            8: 'ship',
            9: 'truck',
        }
        self.dm = dm
        self.p = p

    def make_prediction(self,x_test):
        """Make a prediction using the saved model pipeline."""
    
        model = self.dm.load_pipeline_keras()

        # make a prediction
        predictions= np.argmax(model.predict(x_test),axis=1)
        return predictions

    def get_image_results(self,img):   
        img = self.p.convert_to_tensor(self.p.im_resize(img))
        predictions = self.make_prediction(img)
        unique, counts = np.unique(predictions, return_counts=True)
        sums = np.sum(counts)
        results = { self.cifar10_classes[i[0]] : ((i[1]/sums)*100) for i  in zip(unique, counts)}
        return results
  
if __name__ == '__main__': 

    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import confusion_matrix,accuracy_score,classification_report

    from config import Config
    import model as m
    from processing.data_management import DataService
    from processing.preprocessors import Preprocessor

    c = Config()
    dm = DataService(c.IMAGE_SIZE, c.BATCH_SIZE,c.TRAINED_MODEL_DIR, c.MODEL_PATH)
    p = Preprocessor(c.IMAGE_SIZE)
    pred = Predict(dm,p)
    (new_x_train, new_y_train), (x_test, y_test), (x_val, y_val) = dm.load_data()
    predictions = pred.make_prediction(x_test)
    encoder = LabelEncoder()
    encoder.fit(new_y_train)
    encoder.transform(y_test)

    print(classification_report(encoder.transform(y_test), predictions))
    print(accuracy_score(encoder.transform(y_test), predictions, normalize=True, sample_weight=None))

  