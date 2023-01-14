from detectron2.utils.logger import setup_logger
setup_logger()

import torch
import numpy as np
from PIL import Image

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultPredictor

#ViT
from transformers import ViTFeatureExtractor, ViTModel


class Detectron2Extraction():
    def __init__(self) -> None:
            
        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml"))
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml")
        # self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
        self.cfg.MODEL.DEVICE='cpu'
        self.object_predictor = DefaultPredictor(self.cfg)

        stuff_classes = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).as_dict()["stuff_classes"]
        thing_classes = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).as_dict()["thing_classes"]
        self.segment_classes = [*thing_classes, *stuff_classes]

    def detectron2_processing(self, image_dir):
        image = np.array(Image.open(image_dir).convert("RGB"))
        panoptic_seg, segments_info = self.object_predictor(image)["panoptic_seg"]
        results = np.zeros((len(self.segment_classes)))
        for segment in segments_info:
            if segment["isthing"]:
                results[segment["category_id"]]+=1
            else:
                results[segment["category_id"] + 80]+=1
        return results

class ViTExtraction():
    def __init__(self) -> None:
            
        self.feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch32-224-in21k")
        self.vit_model = ViTModel.from_pretrained("google/vit-base-patch32-224-in21k")

    def vit_processing(self, image_dir):
        image = Image.open(image_dir).convert("RGB")
        inputs = self.feature_extractor(image, return_tensors="pt")
        with torch.no_grad():
            outputs = self.vit_model(**inputs)

        last_hidden_states = outputs.last_hidden_state
        return last_hidden_states.numpy()[0]
    
class ImageExtraction():
    def __init__(self) -> None:
        self.detectron2_extraction = Detectron2Extraction()
        self.vit_extraction = ViTExtraction()
    
    def image_extraction(self, image_dir):
        detectron2_feature = self.detectron2_extraction.detectron2_processing(image_dir)
        vit_feature = self.vit_extraction.vit_processing(image_dir)
        return vit_feature, detectron2_feature