"""
This class implements the YoloDetector. It is used to detect elements in a
given image or batch of images. It uses YOLOv6 as the backbone of the detector.

Author: Eric Canas.
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 09-07-2022
"""

import numpy as np

import os
import torch
import torch.nn.functional as F
import yaml

from vid2info.inference.segmentation.config import WEIGTHS_PATH, PARAMS_YAML, \
    MODEL_NAME, PIDNET_SCALE_FACTOR
from vid2info.inference.config import INFERENCE_DEVICE, CLASS_NAMES_LIST, SEGMENTATION_MASK, BACKGROUND_CLASS_IDX
from vid2info.inference.utils import image_to_float_tensor, get_l_r_pad

from third_party.pidnet.pidnet import get_pred_model

UINT8_TO_FLOAT = 1/255

class PidNetSegmenter:
    def __init__(self, weights : str = WEIGTHS_PATH, params_yml : str = PARAMS_YAML,
                 model_name = MODEL_NAME, inference_device : str = INFERENCE_DEVICE):
        """
        Initialize the segmenter. Load the model and the parameters.

        :param weights: str. Path to the weights file. It must be the .pt file generated during
                        the training of PIDNet.
        :param params_yml: str. Path to the yaml file with the model parameters. It must contain the following
                             parameters:
                                - mean : list of 3 elements. The channel-wise mean of the dataset. Set on the training
                                        to normalize the input.
                                - std : list of 3 elements. The channel-wise standard deviation of the dataset. Set on
                                        the training to normalize the input.
                                - class_names : list of strings. The class names of the dataset.
                                - background_class : string. The name of the background class.
        :param model_name: str ending with small, medium or large. Ex: pidnet_small. The version of the
                        pidnet model to load.
        :param inference_device: str. The device to use for inference. Must be 'cpu', 'cuda' or 'cuda:i'.
        """
        assert os.path.isfile(weights), f'Weights file {weights} not found.'
        if inference_device.startswith('cuda'):
            assert torch.cuda.is_available(), 'CUDA is not available.'
        else:
            assert inference_device == 'cpu', f'Inference device must be cpu or cuda. Got {inference_device}.'

        self.scale_factor = PIDNET_SCALE_FACTOR

        self.inference_device = torch.device(inference_device)

        self.load_params(params_yaml=params_yml)

        self.model = self.build_model(model_name=model_name, weights=weights).to(self.inference_device)
        # Warm the model up (Don't set in self to let the garbage collector free the memory)
        input_sample = torch.zeros(1, len('RGB'), self.scale_factor*2, self.scale_factor*2, dtype=torch.float32,
                                   device=self.inference_device)
        self.model(input_sample)

    def load_params(self, params_yaml : str = PARAMS_YAML):
        """
        Load the parameters from the given yml file. That params are mean, std and class_names.

        :param params_yaml: str. Path to the yaml file.
        """
        assert os.path.isfile(params_yaml), f'Dataset yml file {params_yaml} not found.'

        with open(params_yaml, 'r') as f:
            params = yaml.load(f, Loader=yaml.FullLoader)

        self.class_names = tuple(params['class_names'])
        self.num_classes = len(self.class_names)
        self.background_class = params['background_class']
        self.background_class_idx = self.class_names.index(self.background_class)
        assert self.background_class_idx >= 0, f'Background class {self.background_class} not found in class names.'

        self.mean = torch.tensor(data=params['mean'], dtype=torch.float32, device=self.inference_device)
        self.std = torch.tensor(data=params['std'], dtype=torch.float32, device=self.inference_device)

        assert len(self.mean) == len(self.std) == 3, f'Mean and std must be a list of 3 elements (RGB). ' \
                                                     f'Got {len(self.mean)} and {len(self.std)}.'
        assert self.num_classes > 1, f'There must be at least 2 classes to segment. Got {self.num_classes}.'

    def build_model(self, model_name : str = MODEL_NAME, weights : str = WEIGTHS_PATH) -> torch.nn.Module:
        """
        Build the model, loading the given weights.

        :param model_name: str ending with small, medium or large. Ex: pidnet_small. The version of the
                        pidnet model to load.
        :param weights: str. Path to the weights file.
        :param inference_device: str. The device to use for inference. Must be 'cpu' or 'cuda'.
        """
        assert os.path.isfile(weights), f'Weights file {weights} not found.'
        # Get the model
        model = get_pred_model(name=model_name, num_classes=self.num_classes).to('cpu')
        # Load the weights
        state_dict = torch.load(f=weights, map_location='cpu')
        state_dict = state_dict['state_dict'] if 'state_dict' in state_dict else state_dict

        # Adapt the weights to the prediction model
        layers_offset = 'model.'
        model_dict = model.state_dict()
        layers_have_offset = all(k.startswith(layers_offset) for k in state_dict.keys() if not k.endswith('criterion.weight'))
        name_offset = len(layers_offset) if layers_have_offset else 0

        state_dict = {layer_name[name_offset:]: state for layer_name, state in state_dict.items()
                      if (layer_name[name_offset:] in model_dict and
                          state.shape == model_dict[layer_name[name_offset:]].shape)}
        assert len(state_dict) == len(model_dict), f'Weights file {weights} has different layers than the model.' \
                                                   f'Got {len(state_dict)} layers, expected {len(model_dict)}.' \
                                                   f'Are you sure you are using the correct weights file?'
        # Load them to the model
        model.load_state_dict(state_dict=state_dict, strict=True)
        model.eval()

        return model

    def segment(self, image: np.ndarray | torch.Tensor, is_bgr : bool = False,
                prediction_as_tensor : bool = False, return_as_dict: bool = True) -> np.ndarray | torch.Tensor | dict:
        """
        Infer the segmentation map of the given image

        :param image: np.ndarray or torch.tensor as uint8 (0, 255) or float32 (0., 1.). The image to segment,
                      in format (H, W, C). Channels must be 3, RGB or BGR.
        :param is_bgr: bool. If True, the image is in BGR format. If False, the image is in RGB format.
        :param prediction_as_tensor: bool. If True, the output is a torch.tensor. If False, the output is a np.ndarray.
        :param return_as_dict: bool. If True, the output is a dict containing the segmenter meta-information.
                               If False, the output is directly the prediction.

        :return: np.ndarray or torch.Tensor in format uint8. The segmentation map, in format (H, W). Each pixel value
                 corresponds to the index of the inferred class. Names for those classes are stored in self.class_names.
        """
        assert image.ndim == 3, f'Image must be in format (H, W, 3). Got {image.ndim} dimensions.'
        original_h, original_w = image.shape[:2]
        image = self.preprocess_image(image=image, input_is_bgr=is_bgr)

        prediction = self.model(image[None,...])[0]
        prediction = self.postprocess_prediction(prediction=prediction, original_h=original_h, original_w=original_w,
                                                 prediction_as_tensor=prediction_as_tensor)
        if return_as_dict:
            prediction = self.build_prediction_dict(prediction=prediction)
        return prediction

    def preprocess_image(self, image: np.ndarray | torch.Tensor, input_is_bgr = False) -> torch.Tensor:
        """
        Preprocess the image to be used for inference. It means to transform it to a tensor, normalize it,
        and convert it to the right model input format (C, H, W) with channels in RGB. Ensuring that the image
        size is a multiple of the model's scale factor.

        :param image: np.ndarray or torch.tensor as uint8 (0, 255) or float32 (0., 1.). The image to segment,
                      in format (H, W, C). Channels must be 3, RGB or BGR.
        :param input_is_bgr: bool. If True, the image is in BGR format. If False, the image is in RGB format.
        :return: torch.Tensor in format (C, H, W). The image in the right format for the model.
        """
        assert image.ndim == 3, f'Image must be 3D. Got {image.shape}.'
        assert image.shape[-1] == 3, f'Image must have 3 channels (Format (H, W, C)). Got {image.shape}.'

        # Convert the image to the right format. Making sure it is a Tensor
        image = image_to_float_tensor(image=image, is_bgr=input_is_bgr, device=self.inference_device)

        # Normalize the image
        image = (image - self.mean) / self.std

        # Convert from HWC to CHW
        h, w, _ = image.shape
        image = image.permute((2, 0, 1))

        # Pad it if needed to make sure it is multiple of scale_factor
        h_scale_diff, w_scale_diff = h % self.scale_factor, w % self.scale_factor
        if h_scale_diff != 0 or w_scale_diff != 0:
            (r_w, l_w), (r_h, l_h) = get_l_r_pad(value=w_scale_diff), get_l_r_pad(value=h_scale_diff)
            image = F.pad(input=image, pad=(l_w, r_w, l_h, r_h), mode='symmetric')

        return image

    def postprocess_prediction(self, prediction: torch.Tensor, original_h: int, original_w: int,
                               prediction_as_tensor: bool = False) -> np.ndarray:
        """
        Postprocess the prediction to get the segmentation map.
        :param prediction: torch.Tensor of shape (N_CLASSES, H, W). The raw predictions of the model.
        :param original_h: int. The original height of the image.
        :param original_w: int. The original width of the image.
        :param prediction_as_tensor: bool. If True, the output is a torch.tensor. If False, the output is a np.ndarray.

        :return: np.ndarray or torch.Tensor of shape (H, W) with type uint8. Inside a dict with the segmenter
                 meta-information if return_as_dict is True. The segmentation map, with values in the range
                 [0, N_CLASSES-1]. Each pixel value corresponds to the index of the inferred class.
        """
        assert prediction.ndim == 3, f'Prediction must be 3D. Got {prediction.shape}.'
        assert prediction.shape[0] == self.num_classes, f'Prediction must have {self.num_classes} channels. ' \
                                                        f'Got {prediction.shape}.'

        prediction = F.interpolate(input=prediction[None], scale_factor=self.scale_factor,
                                   mode='bilinear', align_corners=True)[0]
        pred_h, pred_w = prediction.shape[1:]

        if pred_h != original_h or pred_w != original_w:
            assert pred_h >= original_h and pred_w >= original_w, \
                f'Prediction must be at least as large as the original image. ' \
                f'Got {pred_h}x{pred_w} instead of {original_h}x{original_w}.'
            (l_h, r_h), (l_w, r_w) = get_l_r_pad(value=pred_h - original_h), get_l_r_pad(value=pred_w - original_w)
            prediction = prediction[:, l_h:pred_h-r_h, l_w:pred_w-r_w]

        prediction = prediction.argmax(dim=0).type(torch.uint8)

        if prediction_as_tensor:
            return prediction

        if self.inference_device.type.startswith('cuda'):
            prediction = prediction.cpu()
        prediction = prediction.numpy()
        assert prediction.dtype == np.uint8, f'Prediction must be uint8. Got {prediction.dtype}.'
        return prediction

    def build_prediction_dict(self, prediction: np.ndarray) -> dict:
        """
        Build a dictionary with the prediction, containing the segmentation map and the class name correspondences
        so that the segmenter meta information can be directly used

        :param prediction: np.ndarray of shape (H, W). The segmentation map, with values in the range [0, N_CLASSES-1].
        :return: dict. The dictionary with the prediction.
        """

        assert prediction.ndim == 2, f'Prediction must be 2D. Got {prediction.shape}.'
        assert prediction.dtype == np.uint8, f'Prediction should be uint8. Got {prediction.dtype}.'

        prediction_dict = {SEGMENTATION_MASK: prediction,
                           CLASS_NAMES_LIST: self.class_names,
                           BACKGROUND_CLASS_IDX: self.background_class_idx}

        return prediction_dict
