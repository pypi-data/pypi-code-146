import numpy as np
### torch ###
import torch
import torch.backends.cudnn as cudnn

### yolo ###
from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, save_one_box
from utils.plots import colors as yolo_colors
from utils.segment.general import process_mask, scale_masks
from utils.segment.plots import plot_masks
from utils.torch_utils import select_device, smart_inference_mode
from utils.augmentations import letterbox

################################################### yolo model
def load_yolo_model(
        weights='best.pt',  # model.pt path(s)
        data='None',  # dataset.yaml path
        device='cpu',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
):
    # Load model
    device = select_device(device)
    print(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    return model


def yolo_predict_one_image(
    yolo_predict_model,
    im0,
    imgsz=(1984, 1984),  # inference size (height, width)
    conf_thres=0.3,  # confidence threshold
    iou_thres=0.45,  # NMS IOU threshold
    max_det=100,  # maximum detections per image
    device='cpu',  # cuda:0 cuda device, i.e. 0 or 0,1,2,3 or cpu
    view_img=False,  # show results
    save_txt=False,  # save results to *.txt
    save_conf=False,  # save confidences in --save-txt labels
    save_crop=False,  # save cropped prediction boxes
    nosave=False,  # do not save images/videos
    classes=None,  # filter by class: --class 0, or --class 0 2 3
    agnostic_nms=False,  # class-agnostic NMS
    augment=True,  # augmented inference
    visualize=False,  # visualize features
    update=False,  # update all models
    project='runs/predict-seg',  # save results to project/name
    name='exp',  # save results to project/name
    exist_ok=True,  # existing project/name ok, do not increment
    line_thickness=3,  # bounding box thickness (pixels)
    hide_labels=False,  # hide labels
    hide_conf=False,  # hide confidences
    half=False,  # use FP16 half-precision inference
    dnn=False,  # use OpenCV DNN for ONNX inference
):
    stride, names, pt = yolo_predict_model.stride, yolo_predict_model.names, yolo_predict_model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    bs = 1
    im = letterbox(im0, imgsz, stride=stride, auto=pt)[0]  # padded resize
    im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
    im = np.ascontiguousarray(im)
    # Run inference
    yolo_predict_model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup

    im = torch.from_numpy(im).to(device)
    im = im.half() if yolo_predict_model.fp16 else im.float()  # uint8 to fp16/32
    im /= 255  # 0 - 255 to 0.0 - 1.0
    if len(im.shape) == 3:
        im = im[None]  # expand for batch dim

    # Inference
    pred, out = yolo_predict_model(im, augment=False, visualize=False)
    proto = out[1]

    # NMS
    pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det, nm=32)

    # Second-stage classifier (optional)
    # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

    # Process predictions
    # for i, det in enumerate(pred):  # per image
    det = pred[0]
    im0 = im0.copy()
    annotator = Annotator(im0, line_width=line_thickness, example=str(names))
    scaled_masks_poly= []
    scores = []
    classes= []

    if len(det):
        masks = process_mask(proto[0], det[:, 6:], det[:, :4], im.shape[2:], upsample=True)  # HWC
        masks_poly = torch.as_tensor(masks, dtype=torch.uint8)
        masks_poly = masks_poly.permute(1, 2, 0).contiguous()
        masks_poly = masks_poly.cpu().numpy()
        scaled_masks_poly = scale_masks(im.shape[2:], masks_poly, im0.shape)

        total_masks = scaled_masks_poly.shape[2]
        # for idx in range(total_masks):
        #     mask = scaled_masks_poly[:,:, idx]
        #     segmentation = binary_mask_to_polygon(mask, tolerance=3)

        # Rescale boxes from img_size to im0 size
        # det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

        scores = det[:, 4].cpu().numpy()
        classes = det[:, 5].cpu().numpy()

        # Mask plotting ----------------------------------------------------------------------------------------
        mcolors = [yolo_colors(int(cls), True) for cls in classes]
        im_masks = plot_masks(im[0], masks, mcolors)  # image with masks shape(imh,imw,3)
        annotator.im = scale_masks(im.shape[2:], im_masks, im0.shape)  # scale to original h, w
        # Mask plotting ----------------------------------------------------------------------------------------


        # # Write results
        # for *xyxy, conf, cls in reversed(det[:, :6]):
        #     c = int(cls)  # integer class
        #     label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
            # annotator.box_label(xyxy, label, color=colors(c, True))
            # # Stream results

        im0 = annotator.result()
        # cv2.imwrite('aaa.jpg',im0)
    return scaled_masks_poly, scores, classes, im0
