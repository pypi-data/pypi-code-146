import yaml
import numpy as np
import tensorflow as tf

from src.image_extraction import ImageExtraction
from src.question_extraction import QuestionExtraction
from src.model import Model
from src.annotation_setup import AnnotationSetup

class AnswerGeneration():
    def __init__(self) -> None:
        
        self.image_extractor = ImageExtraction()
        self.annotation_setup = AnnotationSetup()
        self.question_extractor = QuestionExtraction()
        self.model = Model()
        self.model.compile()
        self.model.load()
        
    def answer_generation(self, image_dir, question):
        vit_feature, detectron2_feature = self.image_extractor.image_extraction(image_dir)
        question = self.annotation_setup.text_preprocessing(question)
        mbert_feature = self.question_extractor.question_extraction(question)
        merge_feature = np.vstack([vit_feature, mbert_feature])
        merge_feature = np.expand_dims(merge_feature, axis = 0)
        
        detectron2_feature = np.expand_dims(detectron2_feature, axis = 0)
        detectron2_feature = np.expand_dims(detectron2_feature, axis = 0)

        encoded_img = self.model.encoder(merge_feature, detectron2_feature, training=False)
        decoded_caption = "<start>"
        for i in range(58):
            tokenized_caption = self.annotation_setup.answer_embedding(decoded_caption)
            # print(decoded_caption)
            tokenized_caption = np.expand_dims(tokenized_caption, axis = 0)
            mask = tf.math.not_equal(tokenized_caption, 0)
            predictions = self.model.decoder(
                tokenized_caption, encoded_img, training=False, mask=mask
            )
            sampled_token_index = np.argmax(predictions[0, i, :])
            sampled_token = self.annotation_setup.restore_dictionary[sampled_token_index]
            if sampled_token == "<end>":
                # print("END")
                break
            decoded_caption += " " + sampled_token

        decoded_caption = decoded_caption.replace("<start> ", "")
        decoded_caption = decoded_caption.replace("<unk> ", "")
        decoded_caption = decoded_caption.replace(" <unk>", "")
        decoded_caption = decoded_caption.replace(" <end>", "").strip()
        if self.annotation_setup.language_check(decoded_caption) == "ja":
            decoded_caption = decoded_caption.replace(" ", "")
        return decoded_caption