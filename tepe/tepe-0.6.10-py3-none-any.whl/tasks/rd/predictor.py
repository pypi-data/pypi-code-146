import os
from typing import Optional, Callable
from scipy import ndimage as ndi
import cv2
import numpy as np
import torch
import torchvision
from loguru import logger
from matplotlib import pyplot as plt
from scipy.ndimage import gaussian_filter

from skimage.feature import peak_local_max
from skimage import data, img_as_float, morphology

from tepe.core import Predictor as BasePredictor
from tepe.core.predictor.anomaly_detector import AnomalyDetector
from tepe.tasks.cfa.utils import denormalization
from tepe.tasks.rd.utils import rectMerge_sxf, check_rect_contain_point
from tepe.utils import increment_path


class Predictor(BasePredictor, AnomalyDetector):
    def __init__(
            self,
            model: torch.nn.Module,
            input_size: int or tuple or list,
            resize_fn: Optional[Callable] = None,
            threshold: float = 0.5,
            transform: Optional[torchvision.transforms.Compose] = None,
            save_path: str = None,
            onnx_inf: bool = False,
            num_slice: int = 1,
            save_result: bool = False,
            img_thr: float = 0.4,
            use_peak: bool = False,
            peak_min_distance: int = 15,
            peak_threshold_rel: float = 0.5,
            **kwargs
    ) -> None:
        super(Predictor, self).__init__(
            save_result=save_result, save_dir=save_path, **kwargs
        )
        self.model = model
        self.input_size = input_size
        self.resize_fn = resize_fn

        self.img_thr = img_thr
        self.use_peak = use_peak
        self.peak_min_distance = peak_min_distance
        self.peak_threshold_rel = peak_threshold_rel
        self.threshold = threshold

        self.transform = transform
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.onnx_inf = onnx_inf
        self.num_slice = num_slice
        detect_people = getattr(self, 'detect_people', False)
        if detect_people:
            from configs.yolox_nano_person import PeopleDetectConfig
            people_config = PeopleDetectConfig()
            self.people_detector = people_config.get_predictor()
        else:
            self.people_detector = None

    def __call__(self, img_meta):
        results = self.run(img_meta)
        if not getattr(self, 'no_draw', False):
            results['dst'] = self.draw(img_meta['img'], results)

        return results

    def infer(self, img):
        if isinstance(self.input_size, int):
            self.input_size = [self.input_size, self.input_size]

        inp = img
        ratio = (1, 1)
        dwh = (0, 0)
        if self.resize_fn:
            inp, ratio, dwh = self.resize_fn(img)
        if self.transform:
            inp = self.transform(inp)

        if self.onnx_inf:
            anomaly_map = self.model.run(
                None,
                {'images': inp.unsqueeze(0).numpy().astype('float32')}
            )[0]
        else:
            with torch.no_grad():
                anomaly_map = self.model(inp.unsqueeze(0).to(self.device))
            anomaly_map = anomaly_map.squeeze(0).cpu().detach().numpy()

        anomaly_map = gaussian_filter(anomaly_map, sigma=4)

        return anomaly_map

    def postprocess(self, anomaly_map, img_shape,
                    min_anomaly_value=None, max_anomaly_value=None):
        if isinstance(self.input_size, int):
            self.input_size = [self.input_size, self.input_size]

        src_area = self.input_size[1] * self.input_size[0]
        area_limit = int(src_area * 0.12 * 0.5 * 0.01)
        length_limit = int(pow(area_limit, 0.5) * 0.5)  # 6

        img_h, img_w = img_shape[:2]
        if (np.max(anomaly_map) > self.img_thr):
            anomaly_map = self.min_max_norm(anomaly_map, min_anomaly_value, max_anomaly_value)
            anomaly_map = gaussian_filter(anomaly_map, sigma=4)
            anomaly_map = cv2.resize(anomaly_map, self.input_size)

            # image_max = ndi.maximum_filter(im, size=10, mode='constant')
            # Comparison between image_max and im to find the coordinates of local maxima
            if (self.use_peak):
                gray_map = np.uint8(anomaly_map * 255)
                im = img_as_float(gray_map)
                coordinates = peak_local_max(im, min_distance=self.peak_min_distance,
                                             threshold_rel=self.peak_threshold_rel, exclude_border=False)  # 返回[行，列]，即[y, x]
            # coordinates = coordinates[anomaly_map[coordinates[:, 0], coordinates[:, 1]] > 0.8 * np.max(anomaly_map)]
            else:
                coordinates = []
            mask = anomaly_map.copy()
            mask[mask > self.threshold] = 1
            mask[mask <= self.threshold] = 0
            kernel = morphology.disk(4)
            mask = morphology.opening(mask, kernel)
            mask *= 255
            mask = mask.astype(np.uint8)
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            anomaly_area = []
            for contour in contours:
                contour = cv2.approxPolyDP(contour, len(contours), True)
                x, y, w, h = cv2.boundingRect(contour)

                if w < length_limit or h < length_limit or w * h < area_limit:
                    continue

                x1, y1 = x, y
                x2, y2 = x + w, y + h
                # x1, y1 = round((x - dwh[0]) / ratio[0]), round((y - dwh[1]) / ratio[1])
                # x2, y2 = round(x1 + w / ratio[0]), round(y1 + h / ratio[1])
                anomaly_area.append([x1, y1, x2, y2])
        else:
            anomaly_map = cv2.resize(anomaly_map, self.input_size)
            anomaly_area = []
            coordinates = []

        # ------filter-------
        complete, filter_anomaly_area = rectMerge_sxf(anomaly_area)
        # print("filter_anomaly_area:", filter_anomaly_area)
        if len(coordinates) and self.use_peak:
            filter_anomaly_area = check_rect_contain_point(filter_anomaly_area, coordinates)
        anomaly_area = filter_anomaly_area

        scale_h, scale_w = float(img_h) / self.input_size[0], float(img_w) / self.input_size[1]
        bboxes, points = [], []
        for rect in anomaly_area:
            x1, y1, x2, y2 = rect
            x1, y1 = round(x1 * scale_w), round(y1 * scale_h)
            x2, y2 = round(x2 * scale_w), round(y2 * scale_h)
            bboxes.append([x1, y1, x2, y2])
        for point in coordinates:
            y, x = point
            x, y = round(x * scale_w), round(y * scale_h)
            points.append([x, y])
        del anomaly_area, coordinates

        return dict(
            anomaly_area=bboxes,
            anomaly_point=points
        )

    def min_max_norm(self, image,  min_anomaly_value=None, max_anomaly_value=None):
        a_min = image.min() if min_anomaly_value is None else min_anomaly_value
        a_max = image.max() if max_anomaly_value is None else max_anomaly_value
        return (image - a_min) / (a_max - a_min)

    def run(self, img_meta):
        img, path, is_vid, idx = img_meta['img'], img_meta['path'], img_meta['is_vid'], img_meta['idx']

        anomaly_map = self.infer(img)

        results = self.postprocess(anomaly_map, img.shape)

        if self.people_detector is not None:
            people_results = self.people_detector.run(img_meta)
            results.update({'people_detection': people_results})

        if getattr(self, 'show_heatmap', True):
            if is_vid:
                logger.warning('Source is video, can not plot figure.')
            else:
                basename = os.path.basename(path)
                name, suffix = os.path.splitext(basename)
                save_path = f'{self.save_dir}/{name}_heatmap{suffix}'
                self.plot_fig(img, anomaly_map, results['anomaly_area'], results['anomaly_point'], save_path)

        if getattr(self, 'save_xml', False):
            if is_vid:
                logger.warning('Source is video, can not save results to xml.')
            else:
                save_xml_dir = os.path.join(self.save_dir, 'xml_predict')
                self.save_xml_dir = save_xml_dir if save_xml_dir is not None \
                    else os.path.join(self.save_dir, 'predict')
                os.makedirs(self.save_xml_dir, exist_ok=True)
                self.save_result_to_xml(path, img.shape, results['anomaly_area'], self.save_xml_dir)

        return results

    def draw(self, img: np.ndarray, results) -> np.ndarray:
        for rect in results['anomaly_area']:
            x1, y1, x2, y2 = rect
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        if self.people_detector is not None:
            img = self.people_detector.draw({'img': img}, results['people_detection'])
        return img

    def plot_fig(self, img, anomaly_map, anomaly_area, anomaly_point, save_path=None):

        r = anomaly_map.shape[1] / img.shape[1], anomaly_map.shape[0] / img.shape[0]
        resize_img = cv2.resize(img, (anomaly_map.shape[1], anomaly_map.shape[0]))[:, :, ::-1]  # RGB

        fig = plt.figure()
        ax0 = fig.add_subplot(221)
        ax0.axis('off')
        ax0.imshow(resize_img)
        ax0.title.set_text('Image')

        ax2 = fig.add_subplot(222)
        ax2.axis('off')
        ax2.imshow(resize_img, cmap='gray', interpolation='none')
        ax2.imshow(anomaly_map, cmap='jet', alpha=0.5, interpolation='none')
        ax2.title.set_text('Predicted heatmap')

        ax3 = fig.add_subplot(223)
        ax3.axis('off')
        ax3.imshow(resize_img)
        if len(anomaly_point):
            anomaly_point = np.array(anomaly_point, dtype=np.float64)
            anomaly_point[:, 0] *= r[0]
            anomaly_point[:, 1] *= r[1]
            anomaly_point.round()
            ax3.plot(anomaly_point[:, 0], anomaly_point[:, 1], 'r.')
        ax3.title.set_text('Predicted key point')

        ax4 = fig.add_subplot(224)
        ax4.axis('off')
        ax4.imshow(resize_img)
        for rect in anomaly_area:
            x1, y1, x2, y2 = rect
            x1, y1 = round(x1 * r[0]), round(y1 * r[1])
            x2, y2 = round(x2 * r[0]), round(y2 * r[1])
            ax4.add_patch(plt.Rectangle((x1, y1), x2 - x1, y2 - y1, color='red', fill=False, linewidth=1))
        ax4.title.set_text('Predicted box')

        fig.tight_layout()

        if self.view_result:
            plt.show()

        # self.save_result = True
        if self.save_result and save_path is not None:
            if not os.path.exists(os.path.dirname(save_path)):
                os.makedirs(os.path.dirname(save_path))
            fig.savefig(save_path, dpi=100)

        plt.close()