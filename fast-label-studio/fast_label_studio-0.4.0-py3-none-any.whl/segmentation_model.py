from collections.abc import Callable
from io import BytesIO
from typing import List, Tuple

import numpy as np
import PIL.Image
import requests
from fastai.vision.all import Image, L, Learner, SaveModelCallback, shutil, tensor
from label_studio_ml.model import LabelStudioMLBase

from fast_label_studio import brush


class SegmentationModel(LabelStudioMLBase):
    def __init__(
        self,
        labels: List[str],
        input_shape: Tuple[int, int],
        best_model_name: str,
        load_predict_model: Callable[[], Learner],
        load_train_model: Callable[[L], Learner],
        epochs,
        **kwargs,
    ):
        """Segmentation Model Wrapper for LabelStudioMLBase

        Args:
            labels (List[str]): list of labels (must include background)
            input_shape (Tuple[int, int]): input shape (height, width)
            best_model_name (str): model name (used to store to model file after train)
            load_predict_model (Callable[[], Learner]): callback to load prediction model
            load_train_model (Callable[[L], Learner]): callback to load training model
            epochs (_type_): number of epochs
        """
        super(SegmentationModel, self).__init__(**kwargs)
        self.labels = labels
        self.input_shape = input_shape
        self.load_predict_model = load_predict_model
        self.load_train_model = load_train_model
        self.best_model_name = best_model_name
        self.epochs = epochs

    def read_img(self, p):
        response = requests.get(
            f"{self.hostname}{p}",
            headers={"Authorization": f"Token {self.access_token}"},
        )
        image = PIL.Image.open(BytesIO(response.content))
        return tensor(image)

    def predict(self, tasks, **kwargs):
        model = self.load_predict_model()
        from_name, schema = list(self.parsed_label_config.items())[0]
        to_name = schema["to_name"][0]
        print(from_name, to_name, len(tasks))
        images = []
        for task in tasks:
            p = task["data"]["image"]
            images.append(self.read_img(p))

        test_dl = model.dls.test_dl(images, num_workers=0)
        preds = model.get_preds(dl=test_dl)
        results = []
        for pred in preds[0]:
            predictions = []
            mask = pred.argmax(dim=0)
            for i in range(pred.shape[0]):
                new_mask = np.zeros(self.input_shape, dtype=np.uint8)
                new_mask[mask == i] = 100
                rle = brush.mask2rle(new_mask)
                predictions.append(
                    {
                        "from_name": from_name,
                        "to_name": to_name,
                        "type": "brushlabels",
                        "original_width": self.input_shape[1],
                        "original_height": self.input_shape[0],
                        "image_rotation": 0,
                        "value": {
                            "brushlabels": [self.labels[i]],
                            "format": "rle",
                            "rle": rle,
                        },
                        "score": 0.5,
                    }
                )

            results.append({"result": predictions})

        return results

    def fit(self, tasks, workdir=None, **kwargs):

        images = L([])
        masks = L([])

        for task in tasks:
            p = task["data"]["image"]
            images.append(self.read_img(p))
            layers = {}
            final_mask = np.zeros(self.input_shape)
            results = task["annotations"][0]["result"]
            for result in results:
                result["rle"] = result["value"]["rle"]

                key = "brushlabels"

                if key not in result["value"]:
                    continue

                if "rle" not in result["value"]:
                    continue

                result[key] = result["value"][key]

                rle = result["value"]["rle"]
                width = result["original_width"]
                height = result["original_height"]
                ls = result["value"][key] if key in result["value"] else ["no_label"]
                name = ls[0]

                image = brush.decode_rle(rle)

                m = np.reshape(image, [height, width, 4])[:, :, 3]
                m[m > 0] = 255
                if name in layers:
                    layers[name][m > 0] = 255
                else:
                    layers[name] = m

            for layer in layers.keys():
                id = self.labels.index(layer)
                final_mask[layers[layer] > 0] = (id) * 1

            img = Image.fromarray(final_mask)
            img = img.convert("L")
            masks.append(tensor(img))

        items = L(zip(images, masks))

        model = self.load_train_model(items)

        model.fine_tune(self.epochs, cbs=SaveModelCallback(fname=self.best_model_name))
        model.to_onnx(fname=self.best_model_name)
        shutil.copyfile(
            f"models/{self.best_model_name}.pth",
            f"{workdir}/{self.best_model_name}.pth",
        )
        shutil.copyfile(
            f"models/{self.best_model_name}.onnx",
            f"{workdir}/{self.best_model_name}.onnx",
        )
        shutil.move("history.csv", f"{workdir}")

        return {}
