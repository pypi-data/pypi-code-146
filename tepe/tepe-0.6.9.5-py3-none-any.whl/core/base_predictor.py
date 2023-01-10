import os
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Any, Dict, Union, Optional

import cv2
import numpy as np
import torch.backends.cudnn as cudnn
from loguru import logger
from tepe.data.infer_datasets import LoadStreams, LoadImages
from tepe.data.utils import IMG_FORMATS, VID_FORMATS
from tepe.utils.general import check_file, check_imshow, increment_path
from tepe.utils.torch_utils import time_synchronized


class Predictor(metaclass=ABCMeta):
    # TODO: opencv-dnn, tensorRT support
    def __init__(self,
                 save_dir: str = None,
                 save_result: bool = False,
                 **kwargs) -> None:

        self.save_dir = save_dir
        self.save_result = save_result
        self._mkdir_flag = False
        self.view_result = False
        for flag, value in kwargs.items():
            setattr(self, flag, value)

    @abstractmethod
    def __call__(self, img_meta: Union[np.ndarray, Dict]) -> Optional[Union[np.ndarray, Dict]]:
        """
        Examples:
            result = self.run(img)
            draw_img = self.draw(img, result)

        Args:
            img_meta: source image dict, include img, path and other fields

        Returns: destination image or None
        """
        pass

    @abstractmethod
    def run(self, img_meta: Union[np.ndarray, Dict]) -> Dict:
        """
        run once forward
        Args:
            img_meta: source image dict, include img, path and other fields

        Returns: network inference results
        """
        pass

    @abstractmethod
    def draw(self, img: np.ndarray, results: Dict) -> np.ndarray:
        """
        visualize the inference results.
        Args:
            img: source image
            results: dict of results from self.run function

        Returns: destination image
        """
        pass

    def predict(self, source: str or Path,
                view_img: bool = True,
                save_img: bool = True,
                **kwargs) -> None:
        """
        source: file/dir/URL/glob, 0 for webcam
        """
        self._check_flag(view_img, save_img, kwargs)
        dataset = self._parse_source(source)

        vid_writer = None
        infer_time = 0
        num_img = 0
        for path, img0, vid_cap, idx in dataset:
            """
            img0: BRG image, HWC
            """
            if not vid_cap:
                logger.info("file: " + path)

            img_meta = dict(img=img0, path=path, is_vid=dataset.mode != 'image', idx=idx)
            start_time = time_synchronized()
            results = self(img_meta)
            infer_time += time_synchronized() - start_time

            num_img += 1

            if isinstance(results, np.ndarray):
                result_image = results
            elif isinstance(results, dict):
                result_image = results['dst']
            else:
                continue

            # Save results (image with detections)
            if self.save_result:
                basename = os.path.basename(path)
                name, suffix = os.path.splitext(basename)
                save_path = os.path.join(self.save_dir, f'{name}_result{suffix}')  # img.jpg
                if dataset.mode == 'image':
                    self.save_result_image(result_image, save_path)
                else:  # 'video' or 'stream'
                    if vid_writer is None:
                        if vid_cap:  # video
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, result_image.shape[1], result_image.shape[0]
                            save_path += '.mp4'
                        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                        logger.info(f'Save video...')
                    vid_writer.write(result_image)

            # Show results
            if self.view_result:
                cv2.namedWindow(str(path), cv2.WINDOW_FREERATIO)
                cv2.imshow(str(path), result_image)

                if dataset.mode == 'image':
                    key = cv2.waitKey(0)
                    cv2.destroyWindow(str(path))
                else:
                    key = cv2.waitKey(1)
                if key & 0xFF == 27:
                    break
            
        if num_img > 0:
            logger.info("Average prediction time: {:.4f}s".format(infer_time / num_img))
        if self.save_result:
            logger.info(f'Result save in {self.save_dir}')

    @staticmethod
    def save_result_image(result_image, save_path):
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        cv2.imwrite(save_path, result_image)
    
    def _check_flag(self, view_img, save_img, kwargs):
        """
        检查是否绘制结果，是否显示、保存结果图像
        """
        self.view_result |= (view_img and check_imshow())
        self.save_result |= save_img
        for flag, value in kwargs.items():
            setattr(self, flag, value)
        if self.save_result and not self._mkdir_flag:
            if self.save_dir is None:
                logger.warning("Not specified 'save_dir'")
                self.save_result = False
            else:
                self.save_dir = increment_path(
                    os.path.join(self.save_dir, 'predict'), mkdir=True,
                    increment=False
                )
                self._mkdir_flag = True

    def _parse_source(self, source):
        """
        解析路径的格式: file/dir/URL/glob, 0 for webcam，返回可迭代对象dataset
        """
        source = str(source)
        is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
        is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
        webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)
        if is_url and is_file:
            source = check_file(source)  # download

        # Dataloader
        if webcam:
            cudnn.benchmark = True  # set True to speed up constant image size inference
            dataset = LoadStreams(source)
        else:
            dataset = LoadImages(source)
        return dataset