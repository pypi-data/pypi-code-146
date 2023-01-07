class Train():
    def __init__(self, dm, m, config):
        self.dm=dm
        self.m=m
        self.config = config

    def run_training(self, save_result: bool = True):

        (new_x_train, new_y_train), _, (x_val, y_val) = self.dm.load_data()

        train_dataset = self.dm.make_datasets(new_x_train, new_y_train.reshape(-1), is_train=True)
        val_dataset = self.dm.make_datasets(x_val, y_val.reshape(-1))       

        model = self.m.cnn_model(self.config)
        model.summary()

        model.fit(
            train_dataset,
            validation_data=val_dataset,
            epochs=self.config.EPOCHS,
            callbacks=[self.m.callbacks_list(self.config.MODEL_PATH)],
        )

        if save_result:
            self.dm.save_pipeline_keras(self.m)

if __name__ == '__main__':
    from config import Config
    import model as m
    from processing.data_management import DataService

    c = Config()
    dm = DataService(c.IMAGE_SIZE, c.BATCH_SIZE,c.TRAINED_MODEL_DIR, c.MODEL_PATH)

    t=Train(dm, m, c)
    t.run_training(save_result=True)