import json
import os
import pathlib
from typing import Dict, Any, Union

from tensorflow import keras
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

import cinnaroll

# https://towardsdatascience.com/a-complete-step-by-step-tutorial-on-sentiment-analysis-in-keras-and-tensorflow-ea420cc8913f
# dataset taken from kaggle and divided by 6


# model constants
vocab_size = 40000
embedding_dim = 16
max_length = 120
trunc_type = 'post'
oov_tok = '<OOV>'
padding_type = 'post'
sentiment = {-1: 'Negative', 0: 'Neutral', 1: 'Positive'}

script_dir = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

# load data
df = pd.read_csv(script_dir / "data_for_models" / "amazon_baby_product_reviews.csv")
# rating to sentiment
df['sentiments'] = df.rating.apply(lambda x: 0 if x in [1, 2] else 1)

# train-test split
split = round(len(df) * 0.8)
train_reviews = df['review'][:split]
train_label = df['sentiments'][:split]
test_reviews = df['review'][split:]
test_label = df['sentiments'][split:]
training_sentences = [str(row) for row in train_reviews]
training_labels = [row for row in train_label]
testing_sentences = [str(row) for row in test_reviews]
testing_labels = [row for row in test_label]

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(training_sentences)

# prep data
sequences = tokenizer.texts_to_sequences(training_sentences)
padded = pad_sequences(sequences, maxlen=max_length, truncating=trunc_type)
testing_sentences = tokenizer.texts_to_sequences(testing_sentences)
testing_padded = pad_sequences(testing_sentences, maxlen=max_length)
training_labels_final = np.array(training_labels)
testing_labels_final = np.array(testing_labels)


# create and compile model
model = keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(6, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


class MyRolloutConfig(cinnaroll.RolloutConfig):
    @staticmethod
    def train_eval(
            model_object: Any,
    ) -> Dict[str, Union[str, float]]:  # training and evaluation with metric extraction
        num_epochs = 1
        model.fit(padded, training_labels_final, epochs=num_epochs, validation_data=(
            testing_padded, testing_labels_final)
        )

        # evaluate
        test_loss, test_accuracy = model.evaluate(testing_padded, test_label)

        # metrics dict
        metrics = {"dataset": "amazon baby product reviews from kaggle", "loss": test_loss, "accuracy": test_accuracy}

        return metrics

    @staticmethod
    def infer(model_object: keras.Sequential, input_data: str) -> Dict[str, str]:
        # text from json
        text = json.loads(input_data)["review"]
        sequences = tokenizer.texts_to_sequences(text)
        padded = pad_sequences(sequences, maxlen=max_length, truncating=trunc_type)
        rounded = np.around(model_object.predict(padded), decimals=0).argmax(axis=1)[0]
        predicted_sentiment = sentiment[rounded]

        # to json
        output_json = {"sentiment": predicted_sentiment}
        return output_json


if __name__ == "__main__":
    if 'PROJECT_ID' in os.environ:
        project_id = os.environ['PROJECT_ID']
    else:
        project_id = "8ed8a20a-5f4e-46aa-ae71-dfbea78cf6b1"

    infer_func_input_sample = json.dumps({"review": "wouldn't recommend to anybody"})
    model_input_sample = pad_sequences(
        tokenizer.texts_to_sequences("wouldn't recommend to anybody"), maxlen=max_length, truncating=trunc_type
    )

    rollout_config = MyRolloutConfig(
        project_id=project_id,  # project's unique identifier
        model_name="reviews sentiment analysis",
        model_object=model,
        model_input_sample=model_input_sample,  # sample you can pass to model object's predict function
        infer_func_input_format="json",  # "json", "img" or "file"
        infer_func_output_format="json",  # "json" or "img" currently supported
        infer_func_input_sample=infer_func_input_sample,  # note - for file or img just pass file path
    )

    cinnaroll.rollout(rollout_config)
