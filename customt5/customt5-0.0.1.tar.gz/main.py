# -*- coding: utf-8 -*-

import pandas as pd

from TrainingDataCreation import create_training_data as createData
from custom_t5_model import CustomT5
from sklearn.model_selection import train_test_split

use_gpu = False
model_path = f"outputs/trained-epoch-2-train-loss-0.1147-val-loss-0.0633"
path = f"datasets/generated_training.csv"


def trainModel():
    model = CustomT5()
    df = pd.read_csv(path).dropna()
    df.head()

    df = df.rename(columns={"UseCase": "target_text", "Sentences": "source_text"})
    df = df[['source_text', 'target_text']]

    train_df, test_df = train_test_split(df, test_size=0.25)
    test_df, unseen_df = train_test_split(test_df, test_size=0.3)
    unseen_df = pd.DataFrame(data=unseen_df)
    unseen_df.to_csv(f"datasets/unseen_data.csv", mode='w', index=False)
    model.from_pretrained(model_type="t5", model_name="t5-base")
    model.train(train_df=train_df,
                eval_df=test_df,
                source_max_token_len=128,
                target_max_token_len=50,
                batch_size=8, max_epochs=3, use_gpu=use_gpu)


def loadModel(sentences):
    model = CustomT5()
    # let's load the trained model for inferencing:
    model.load_model("t5", model_path, use_gpu=use_gpu)
    return model.predict(sentences)[0]


def testAccuracy():
    unseen_df = pd.read_csv(r"datasets/unseen_data.csv")
    report = pd.DataFrame(data={"sentence": [None], "Predicted": [None], "Expected": [None], "Result": [None]})
    for ind in unseen_df.index:

        sentence = unseen_df['source_text'][ind]
        target = unseen_df['target_text'][ind]
        use_case = loadModel(sentence)
        if use_case != target:
            df1 = pd.DataFrame(
                data={"sentence": [sentence], "Predicted": [use_case], "Expected": [target], "Result": ["Fail"]})
        else:
            df1 = pd.DataFrame(
                data={"sentence": [sentence], "Predicted": [use_case], "Expected": [target], "Result": ["Pass"]})
        if len(report.dropna()) == 0:
            report = df1
        report = report.append(df1, ignore_index=True)
    report.to_csv("report/report.csv", mode='w', index=False)


def controller(val=0, sentence=""):
    if val == 0:
        use_case = {"UseCase": loadModel(sentence)}
        print(use_case)
    elif val == 1:
        createData()
    elif val == 2:
        trainModel()
    elif val == 3:
        testAccuracy()


if __name__ == '__main__':
    """
    controller(sentence="x is null") It means it will run usecase.
    controller(val=1) It means it will create training dataset.
    controller(val=2) It means it will start training with created dataset.
    controller(val=3) It means it will start Testing accuracy with unseen data.   
    Note: Before running 
    controller(sentence="x is null")
    controller(val=3) 
    Have to change trained model path.
    """
    sentence = "Expiration Date must be of type date"
    # controller(sentence=sentence)
    controller(1)
    controller(2)
