from pickle import TRUE
import warnings
import traceback
from pathlib import Path
from ._codetemplate import code
from ._arcgis_model import ArcGISModel, _get_device

HAS_FASTAI = TRUE

try:
    import json
    import os
    import math
    import torch
    import PIL
    from PIL import Image
    from .._utils.pascal_voc_rectangles import ObjectDetectionCategoryList
    from .._video_utils import VideoUtils
    from .._utils.env import raise_fastai_import_error
    from .._utils.common import (
        get_multispectral_data_params_from_emd,
        _get_emd_path,
        read_image,
    )
    from .._image_utils import _draw_predictions
    from .._utils.env import is_arcgispronotebook
    from .._utils.object_tracking_data import get_image_for_tracking
    import matplotlib
    import matplotlib.pyplot as plt

    HAS_FASTAI = True
except Exception as e:
    import_exception = "\n".join(
        traceback.format_exception(type(e), e, e.__traceback__)
    )
    HAS_FASTAI = False


try:
    import cv2

    HAS_OPENCV = TRUE
except Exception:
    HAS_OPENCV = False


class EfficientDet(ArcGISModel):
    """
    Creates a EfficientDet model for Object Detection. Supports RGB -JPEG imagery. Based on TFLite Model Maker

    =====================   =====================================================
    **Argument**            **Description**
    ---------------------   -----------------------------------------------------
    data                    Required fastai Databunch. Returned data object from
                            :meth:`~arcgis.learn.prepare_data`  function.
    ---------------------   -----------------------------------------------------
    backbone                Optional String. Backbone convolutional neural network
                            model used for EfficientDet.
    ---------------------   -----------------------------------------------------
    pretrained_path         Optional String. Path where a compatible pre-trained
                            model is saved. Accepts a Deep Learning Package
                            (DLPK) or Esri Model Definition(EMD) file.
    =====================   =====================================================

    :return: :class:`~arcgis.learn.EfficientDet` Object
    """

    def __init__(
        self,
        data,
        backbone=None,
        pretrained_path=None,
        *args,
        **kwargs,
    ):
        if not HAS_FASTAI:
            raise_fastai_import_error(import_exception=import_exception)
        self._check_tf()

        from ._efficientdet_utils import (
            EfficientDetTrainer,
            check_data_sanity,
            _get_tf_data_loader,
        )

        self._learn_version = kwargs.get("ArcGISLearnVersion", "1.9.1")

        if self._learn_version >= "1.9.0":
            if pretrained_path is not None:
                pretrained_backbone = False
            else:
                pretrained_backbone = True
            kwargs["pretrained_backbone"] = pretrained_backbone
        else:
            del kwargs["ArcGISLearnVersion"]

        if not check_data_sanity(data, self.supported_datasets):
            raise Exception("\nInvalid data format\n")

        super().__init__(data, backbone, pretrained_path=pretrained_path, **kwargs)

        self._check_dataset_support(data)
        self._backend = "tensorflow"

        class BackBone:
            def __init__(self, default_name, backbone_name=None):
                if backbone_name is None or not type(backbone_name) is str:
                    self.__name__ = default_name
                else:
                    self.__name__ = backbone_name
                self._keras_api_names = [self.__name__]

            def get_name(self):
                return self.__name__

        self._backbone = BackBone(self._get_default_backbone(), backbone)

        if not self._check_backbone_support(self._backbone):
            raise Exception(
                f"Enter only compatible backbones from {', '.join(self.supported_backbones)}"
            )

        self._tf_data_loader = _get_tf_data_loader(data)
        self._trainer = EfficientDetTrainer.create(data, self._backbone.get_name())
        self._tf_dataset = self._trainer.get_tf_dataset(
            self._tf_data_loader, self._data.batch_size
        )
        self._setup_backend(data, pretrained_path)

        self._code = code

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<%s>" % (type(self).__name__)

    @property
    def supported_datasets(self):
        """Supported dataset types for this model."""
        return EfficientDet._supported_datasets()

    @staticmethod
    def _supported_datasets():
        return ["PASCAL_VOC_rectangles"]

    @staticmethod
    def _supported_backbones():
        return [
            "efficientdet_lite0",
            "efficientdet_lite1",
            "efficientdet_lite2",
            "efficientdet_lite3",
            "efficientdet_lite4",
        ]

    @property
    def supported_backbones(self):
        """Supported torchvision backbones for this model."""
        return EfficientDet._supported_backbones()

    def _get_default_backbone(self):
        return EfficientDet._supported_backbones()[0]

    def _setup_backend(self, data, pretrained_path):
        from ._efficientdet_utils import EfficientDetLearner
        from .._utils.fastai_tf_fit import TfLearner
        import tensorflow as tf
        from tensorflow.keras.models import Model
        from fastai.basics import defaults

        if data._is_multispectral:
            raise Exception("Multispectral data is not supported with efficientdet")

        self._device = torch.device("cpu")
        self._data = data
        self._trainer.setup_model()
        self._opt_func = self._trainer.get_opt_func()
        self._model = self._trainer.model

        self.learn = EfficientDetLearner(
            data,
            self._model,
            opt_func=self._opt_func,
            loss_func=None,
            true_wd=True,
            bn_wd=True,
            wd=defaults.wd,
            train_bn=True,
            tf_dataset=self._tf_dataset,
            _trainer=self._trainer,
        )

        if pretrained_path is not None:
            self.load(pretrained_path)

    @classmethod
    def from_model(cls, emd_path, data=None):
        """
        Creates a :class:`~arcgis.learn.EfficientDet` object from an Esri Model Definition (EMD) file.

        =====================   ===========================================
        **Argument**            **Description**
        ---------------------   -------------------------------------------
        emd_path                Required string. Path to Deep Learning Package
                                (DLPK) or Esri Model Definition(EMD) file.
        ---------------------   -------------------------------------------
        data                    Required fastai Databunch or None. Returned data
                                object from :meth:`~arcgis.learn.prepare_data`  function or None for
                                inferencing.

        =====================   ===========================================

        :return: :class:`~arcgis.learn.EfficientDet` Object
        """
        if not HAS_FASTAI:
            raise_fastai_import_error(import_exception=import_exception)

        emd_path = _get_emd_path(emd_path)

        with open(emd_path) as f:
            emd = json.load(f)

        model_file = Path(emd["ModelFile"])

        if not model_file.is_absolute():
            model_file = emd_path.parent / model_file

        backbone = emd["ModelParameters"]["backbone"]
        dataset_type = emd.get("DatasetType", "PASCAL_VOC_rectangles")
        chip_size = emd["ImageWidth"]
        resize_to = emd.get("resize_to", None)
        kwargs = emd.get("Kwargs", {})
        if isinstance(resize_to, list):
            resize_to = (resize_to[0], resize_to[1])

        try:
            class_mapping = {i["Value"]: i["Name"] for i in emd["Classes"]}
            color_mapping = {i["Value"]: i["Color"] for i in emd["Classes"]}
        except KeyError:
            class_mapping = {i["ClassValue"]: i["ClassName"] for i in emd["Classes"]}
            color_mapping = {i["ClassValue"]: i["Color"] for i in emd["Classes"]}

        data_passed = True
        if data is None:
            data_passed = False
            train_tfms = []
            val_tfms = []
            ds_tfms = (train_tfms, val_tfms)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                sd = ImageList([], path=emd_path.parent.parent.parent).split_by_idx([])
                data = (
                    sd.label_const(
                        0,
                        label_cls=ObjectDetectionCategoryList,
                        classes=list(class_mapping.values()),
                    )
                    .transform(ds_tfms)
                    .databunch(device=_get_device())
                    .normalize(imagenet_stats)
                )
            # Add 1 for background class
            data.c += 1
            data.chip_size = chip_size
            data.class_mapping = class_mapping
            data.color_mapping = color_mapping
            data.classes = ["background"] + list(class_mapping.values())
            data._is_empty = True
            data.emd_path = emd_path
            data.emd = emd
            data = get_multispectral_data_params_from_emd(data, emd)
            data.dataset_type = dataset_type
            data.orig_path = None

        data.resize_to = resize_to
        efficientdet = cls(data, backbone, pretrained_path=str(model_file), **kwargs)

        if not data_passed:
            efficientdet.learn.data.single_ds.classes = efficientdet._data.classes
            efficientdet.learn.data.single_ds.y.classes = efficientdet._data.classes

        return efficientdet

    def _save_tflite(self, name, post_processed=True, quantized=False):
        return self.learn._save_tflite(name, post_processed, quantized)

    def _get_emd_params(self, save_inference_file):
        import random

        _emd_template = {}
        _emd_template["Framework"] = "arcgis.learn.models._inferencing"
        _emd_template["ModelType"] = "ObjectDetection"
        _emd_template["ModelName"] = type(self).__name__
        bckbn_name = self._backbone.__name__
        _emd_template["backbone"] = bckbn_name
        _emd_template["Classes"] = []

        class_data = {}
        for i, class_name in enumerate(self._data.classes[1:]):
            inverse_class_mapping = {v: k for k, v in self._data.class_mapping.items()}
            class_data["Value"] = inverse_class_mapping[class_name]
            class_data["Name"] = class_name
            color = [random.choice(range(256)) for i in range(3)]
            class_data["Color"] = color
            _emd_template["Classes"].append(class_data.copy())
        return _emd_template

    @property
    def _model_metrics(self):
        return self.learn.compute_metrics()

    @staticmethod
    def _available_metrics():
        return ["valid_loss"]

    def predict(
        self,
        image_path,
        threshold=0.5,
        nms_overlap=0.1,
        return_scores=True,
        visualize=False,
        resize=False,
        **kwargs,
    ):
        """
        Predicts and displays the results of a trained model on a single image.
        This method is only supported for RGB images.

        =====================   ===========================================
        **Argument**            **Description**
        ---------------------   -------------------------------------------
        image_path              Required. Path to the image file to make the
                                predictions on.
        ---------------------   -------------------------------------------
        thresh                  Optional float. The probability above which
                                a detection will be considered valid.
        ---------------------   -------------------------------------------
        nms_overlap             Optional float. The intersection over union
                                threshold with other predicted bounding
                                boxes, above which the box with the highest
                                score will be considered a true positive.
        ---------------------   -------------------------------------------
        return_scores           Optional boolean.
                                Will return the probability scores of the
                                bounding box predictions if True.
        ---------------------   -------------------------------------------
        visualize               Optional boolean. Displays the image with
                                predicted bounding boxes if True.
        ---------------------   -------------------------------------------
        resize                  Optional boolean. Resizes the image to the
                                same size (chip_size parameter in prepare_data)
                                that the model was trained on, before detecting
                                objects. Note that if resize_to parameter was
                                used in prepare_data, the image is resized to
                                that size instead.

                                By default, this parameter is false and the
                                detections are run in a sliding window fashion
                                by applying the model on cropped sections of
                                the image (of the same size as the model was
                                trained on).
        =====================   ===========================================

        :return: 'List' of xmin, ymin, width, height, labels, scores, of predicted bounding boxes on the given image
        """

        if not HAS_OPENCV:
            raise Exception(
                "This function requires opencv 4.0.1.24. Install it using pip install opencv-python==4.0.1.24"
            )

        if isinstance(image_path, str):
            image = Image.open(image_path)
            orig_frame = cv2.imread(image_path)
        else:
            image = image_path
            orig_frame = image

        predictions, labels, scores = self.learn.predict(image, threshold, nms_overlap)

        if visualize:
            image = _draw_predictions(orig_frame, predictions, labels)
            import matplotlib.pyplot as plt

            plt.xticks([])
            plt.yticks([])
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            plt.imshow(PIL.Image.fromarray(image))

        if return_scores:
            return predictions, labels, scores
        else:
            return predictions, labels

    def predict_video(
        self,
        input_video_path,
        metadata_file,
        threshold=0.5,
        nms_overlap=0.1,
        track=False,
        visualize=False,
        output_file_path=None,
        multiplex=False,
        multiplex_file_path=None,
        tracker_options={
            "assignment_iou_thrd": 0.3,
            "vanish_frames": 40,
            "detect_frames": 10,
        },
        visual_options={
            "show_scores": True,
            "show_labels": True,
            "thickness": 2,
            "fontface": 0,
            "color": (255, 255, 255),
        },
        resize=False,
    ):

        """
        Runs prediction on a video and appends the output VMTI predictions in the metadata file.
        This method is only supported for RGB images.

        =====================   ===========================================
        **Argument**            **Description**
        ---------------------   -------------------------------------------
        input_video_path        Required. Path to the video file to make the
                                predictions on.
        ---------------------   -------------------------------------------
        metadata_file           Required. Path to the metadata csv file where
                                the predictions will be saved in VMTI format.
        ---------------------   -------------------------------------------
        threshold               Optional float. The probability above which
                                a detection will be considered.
        ---------------------   -------------------------------------------
        nms_overlap             Optional float. The intersection over union
                                threshold with other predicted bounding
                                boxes, above which the box with the highest
                                score will be considered a true positive.
        ---------------------   -------------------------------------------
        track                   Optional bool. Set this parameter as True to
                                enable object tracking.
        ---------------------   -------------------------------------------
        visualize               Optional boolean. If True a video is saved
                                with prediction results.
        ---------------------   -------------------------------------------
        output_file_path        Optional path. Path of the final video to be saved.
                                If not supplied, video will be saved at path input_video_path
                                appended with _prediction.
        ---------------------   -------------------------------------------
        multiplex               Optional boolean. Runs Multiplex using the VMTI detections.
        ---------------------   -------------------------------------------
        multiplex_file_path     Optional path. Path of the multiplexed video to be saved.
                                By default a new file with _multiplex.MOV extension is saved
                                in the same folder.
        ---------------------   -------------------------------------------
        tracking_options        Optional dictionary. Set different parameters for
                                object tracking. assignment_iou_thrd parameter is used
                                to assign threshold for assignment of trackers,
                                vanish_frames is the number of frames the object should
                                be absent to consider it as vanished, detect_frames
                                is the number of frames an object should be detected
                                to track it.
        ---------------------   -------------------------------------------
        visual_options          Optional dictionary. Set different parameters for
                                visualization.
                                show_scores boolean, to view scores on predictions,
                                show_labels boolean, to view labels on predictions,
                                thickness integer, to set the thickness level of box,
                                fontface integer, fontface value from opencv values,
                                color tuple (B, G, R), tuple containing values between
                                0-255.
        ---------------------   -------------------------------------------
        resize                  Optional boolean. Resizes the image to the
                                same size (chip_size parameter in prepare_data)
                                that the model was trained on, before detecting
                                objects. Note that if resize_to parameter was
                                used in prepare_data, the image is resized to
                                that size instead.

                                By default, this parameter is false and the
                                detections are run in a sliding window fashion
                                by applying the model on cropped sections of
                                the image (of the same size as the model was
                                trained on).
        =====================   ===========================================

        """

        VideoUtils.predict_video(
            self,
            input_video_path,
            metadata_file,
            threshold,
            nms_overlap,
            track,
            visualize,
            output_file_path,
            multiplex,
            multiplex_file_path,
            tracker_options,
            visual_options,
            resize,
        )

    def plot_losses(self, show=True):
        """
        Plot training and validation losses.

        =====================   ===========================================
        **Argument**            **Description**
        ---------------------   -------------------------------------------
        show                    Optional bool. Defaults to True
                                If set to False, figure will not be plotted
                                but will be returned, when set to True function
                                will plot the figure and return nothing.
        =====================   ===========================================

        :return: `matplotlib.figure.Figure <https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure>`_
        """
        self._check_requisites()

        if not len(self.learn.recorder.losses):  # return none if the recorder is empty
            raise Exception("Model needs to be fitted, before saving.")
        import numpy as np
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(1, 1)
        N = max(1, len(self.learn.recorder.losses) // 10)  # smooth with a factor of N
        ax.plot(
            np.convolve(self.learn.recorder.losses, np.ones((N,)) / N, mode="valid"),
            label="Train",
        )
        ax.plot(
            np.convolve(self.learn.recorder.val_loss, np.ones((N,)) / N, mode="valid"),
            label="Validation",
        )
        ax.set_ylabel("Loss")
        ax.set_xlabel("Epochs")
        ax.legend()

        if not show:
            plt.close()
            return fig
        else:
            plt.show()

    def average_precision_score(self, mean=False):
        """
        Computes average precision on the validation set for each class.

        =====================   ===========================================
        **Argument**            **Description**
        ---------------------   -------------------------------------------
        mean                    Optional bool. If False returns class-wise
                                average precision otherwise returns mean
                                average precision.
        =====================   ===========================================

        :return: `dict` if mean is False otherwise `float`
        """
        metrics = self._model_metrics
        if mean is False:
            ap_dict = dict()
            for value in metrics:
                if value.startswith("AP_/"):
                    class_name = value[4:]
                    ap_dict[class_name] = metrics[value]
            return dict
        else:
            return metrics["AP"]

    def show_results(
        self,
        rows=4,
        box_threshold=0.7,
        imsize=5,
        cmap="tab20",
        **kwargs,
    ):
        """
        Displays the results of a trained model on a part of the validation set.

        =====================   ===========================================
        **Argument**            **Description**
        ---------------------   -------------------------------------------
        ---------------------   -------------------------------------------
        nrows                   Optional int. Number of rows of results
                                to be displayed.
        ---------------------   -------------------------------------------
        box_threshold           Optional float. The probability above which
                                a detection will be considered valid.
        =====================   ===========================================
        """
        self._check_requisites()

        # Get Number of items
        nrows = rows
        ncols = 2

        type_data_loader = kwargs.get(
            "data_loader", "validation"
        )  # options : traininig, validation

        return_fig = kwargs.get("return_fig", False)

        x_batch = self.learn.get_gt_batches(nrows, type_data_loader)
        nrows = min(nrows, len(x_batch))

        title_font_size = 16
        if kwargs.get("top", None) is not None:
            top = kwargs.get("top")
        else:
            top = 1 - (math.sqrt(title_font_size) / math.sqrt(100 * nrows * imsize))

        fig, ax = plt.subplots(
            nrows=nrows, ncols=ncols, figsize=(ncols * imsize, nrows * imsize)
        )

        fig.suptitle("Ground Truth / Predictions", fontsize=title_font_size)
        for i in range(nrows):
            if nrows == 1:
                ax_i = ax
            else:
                ax_i = ax[i]

            for j in range(2):
                image = get_image_for_tracking(x_batch[i][0])
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                if j == 0:
                    bboxes = x_batch[i][1]
                else:
                    bboxes, _, _ = self.predict(x_batch[i][0], box_threshold)
                for bbox in bboxes:
                    cv2.rectangle(
                        image,
                        (int(bbox[0]), int(bbox[1])),
                        (int(bbox[2]) + int(bbox[0]), int(bbox[3] + int(bbox[1]))),
                        (255, 0, 0),
                        2,
                    )

                ax_i[j].imshow(image)  # image
                ax_i[j].axis("off")

        plt.subplots_adjust(top=top)
        if self._device == torch.device("cuda"):
            torch.cuda.empty_cache()
        if is_arcgispronotebook():
            plt.show()
        if return_fig:
            return fig
