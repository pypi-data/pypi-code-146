import os
from loguru import logger
import numpy as np
import tifffile as tiff


class AnomalyDetector(object):

    @staticmethod
    def save_result_to_xml(image_path, image_shape,
                           anomaly_area, save_dir=None):
        """
        将预测结果以voc格式写入到xml文件中
        Args:
            image_path: 图像路径
            image_shape: 原图大小，[h, w, c]
            anomaly_area: 异物检测的包围框, [[left, top, right, bottom], ...]

        Returns:

        """
        if save_dir is None:
            save_dir = os.path.abspath(os.path.dirname(image_path))

        from tepe.data.voc_xml import PascalVocWriter
        img_name = os.path.basename(image_path)
        writer = PascalVocWriter('VOC2007', img_name, image_shape)
        for r in anomaly_area:
            left, top, right, bottom = r
            writer.add_bnd_box(int(left), int(top), int(right), int(bottom), name='abnormal')
        name, suffix = os.path.splitext(img_name)
        save_xml_path = os.path.join(save_dir, name + '.xml')
        writer.save(target_file=save_xml_path)
        # logger.info(f'Detections save in {save_xml_path}')

    @staticmethod
    def save_heatmap(heatmap: np.ndarray, save_path: str):
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        tiff.imwrite(save_path, heatmap)