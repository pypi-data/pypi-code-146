from typing import Optional, Dict, Callable
import os
import cv2
import numpy as np
import torch
import torchvision
from matplotlib import pyplot as plt
from scipy.ndimage import gaussian_filter
from skimage.segmentation import mark_boundaries

from tepe.core import Predictor as BasePredictor
from .utils import upsample, gaussian_smooth, rescale, denormalization


class Predictor(BasePredictor):
    """
    CFA异常检测的预测类

    """
    def __init__(
            self,
            model: torch.nn.Module,
            input_size: int or tuple or list,
            resize_fn: Optional[Callable] = None,
            threshold: float = 0.5,
            transform: Optional[torchvision.transforms.Compose] = None,
            save_path: str = None,
            onnx_inf: bool = False
    ) -> None:
        super(Predictor, self).__init__(save_dir=save_path)
        self.model = model
        self.input_size = input_size
        self.resize_fn = resize_fn
        self.threshold = threshold
        self.transform = transform
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.show_heatmap = True
        self.onnx_inf = onnx_inf

    def __call__(self, img_meta) -> np.ndarray:
        results = self.run(img_meta)
        dst = self.draw(img_meta['img'], results)
        return dst

    def run(self, img_meta) -> Dict:
        """
        执行CFA前处理、前向推理、后处理
        Args:
            img_meta(dict): 包含img, path等信息

        Returns:

        """
        img, path, is_vid = img_meta['img'], img_meta['path'], img_meta['is_vid']
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
            outs = self.model.run(None, {'images': inp.unsqueeze(0).numpy().astype('float32')})
            heatmap = outs[0]
        else:
            with torch.no_grad():
                _, outs = self.model(inp.unsqueeze(0).to(self.device))
                heatmap = outs.cpu().detach().numpy()

        heatmap = heatmap[0][0]
        # sigmoid
        heatmap = 1 / (1 + np.exp(-heatmap))
        heatmap = rescale(heatmap)
        heatmap = cv2.resize(heatmap, self.input_size)
        score = gaussian_filter(heatmap, sigma=4)

        mask = score.copy()
        mask[mask > self.threshold] = 1
        mask[mask <= self.threshold] = 0

        mask *= 255
        mask = mask.astype(np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        inp = inp.numpy() if isinstance(inp, torch.Tensor) else inp
        resized_img = denormalization(inp)
        # #-------计算距离,确定前景对象--------------------
        # dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)   #float32的浮点型数组，dist.shape返回(312, 252),dist是一个灰度图像
        # th, sure_fg = cv2.threshold(dist, 0.5*dist.max(), 255, cv2.THRESH_BINARY) #把dist阈值化处理，变成一个0和255的二值图像，此时就是我们要的确定前景
        # sure_fg = np.uint8(sure_fg)
        #
        # #-----计算确定背景、计算未知区域------------------
        # sure_bg = cv2.dilate(mask, kernel=np.ones((3,3), np.uint8), iterations=3) #对前景膨胀来确定背景
        # unknown = cv2.subtract(sure_bg, sure_fg)  #确定背景图-确定前景图，生成未知区域图
        #
        # #------标注确定前景图,调整标注规则---------------------------
        # ret, labels = cv2.connectedComponents(sure_fg)  #有24个硬币，ret返回是25, labels是一个形状是(312, 252)的int32的数组
        # labels = labels+1  #把背景标为1，前景对象依次为2，3，，，26
        # labels[unknown==255]=0  #0代表未知区域
        #
        # #------------使用分水岭算法对图像进行分割---------------

        # markers = cv2.watershed(resized_img, labels)
        #
        # markers[markers>1] = 255
        # markers[markers<=1] = 0
        # markers = np.uint8(markers)
        markers = mask

        if self.show_heatmap and not is_vid:
            self.plot_fig(resized_img, score, markers, path)

        contours, hierarchy = cv2.findContours(markers, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        anomaly_area = []
        for contour in contours:
            contour = cv2.approxPolyDP(contour, len(contours), True)
            x, y, w, h = cv2.boundingRect(contour)
            # if w < self.input_size[1] * 0.05 or h < self.input_size[0] * 0.05:
            #     continue
            x1, y1 = round((x - dwh[0]) / ratio[0]), round((y - dwh[1]) / ratio[1])
            x2, y2 = round(x1 + w / ratio[0]), round(y1 + h / ratio[1])
            anomaly_area.append([x1, y1, x2, y2])

        return dict(
            anomaly_area=anomaly_area
        )

    def draw(self, img, results) -> np.ndarray:
        for rect in results['anomaly_area']:
            x1, y1, x2, y2 = rect
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        return img

    def plot_fig(self, resize_img, score, mask, path):
        vis_img = mark_boundaries(resize_img, mask, color=(1, 0, 0), mode='thick')

        fig = plt.figure()
        ax0 = fig.add_subplot(221)
        ax0.axis('off')
        ax0.imshow(resize_img)
        ax0.title.set_text('Image')

        ax1 = fig.add_subplot(222)
        ax1.axis('off')
        ax1.imshow(mask, cmap='gray')
        ax1.title.set_text('Mask')

        ax2 = fig.add_subplot(223)
        ax2.axis('off')
        ax2.imshow(resize_img, cmap='gray', interpolation='none')
        ax2.imshow(score, cmap='jet', vmin=0, vmax=1, alpha=0.5, interpolation='none')
        ax2.title.set_text('Predicted heat map')

        ax3 = fig.add_subplot(224)
        ax3.axis('off')
        ax3.imshow(vis_img)
        ax3.title.set_text('Segmentation result')

        fig.tight_layout()

        if self.view_result:
            plt.show()

        if self.save_result:
            basename = os.path.basename(path)
            name, suffix = os.path.splitext(basename)
            fig.savefig(f'{self.save_dir}/{name}_heatmap{suffix}', dpi=100)

        plt.close()