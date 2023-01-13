import argparse
import os
import io
import sys
import json 
import numpy as np
import pandas as pd
import math
import cv2
import platform
import requests
import logging

import time
import timeit
from datetime import datetime

# from pathlib import Path
# plot
from PIL import Image
from matplotlib import pyplot as plt

### coco mask to polygon ###
import base64
from pycocotools.coco import COCO
from skimage import measure
from io import BytesIO

### parallel download images ###
import uuid
from joblib import Parallel, delayed
from concurrent import futures

#### shapely ###
import shapely
import shapely.wkt
from shapely.ops import unary_union
from shapely.geometry import Polygon, MultiPoint
from shapely.geometry import Polygon

### torch ###
import torch
import torch.backends.cudnn as cudnn

### detectron2 ###
from detectron2.data import DatasetCatalog
from detectron2.data.datasets.coco import register_coco_instances 
from detectron2.data.detection_utils import read_image
from detectron2.data import detection_utils as utils
from detectron2.utils.logger import setup_logger
from detectron2.utils.visualizer_new import Visualizer
from detectron2.utils.visualizer_new import ColorMode
from detectron2.engine.defaults import DefaultPredictor
from detectron2.data import MetadataCatalog

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

import yolo_roof.export

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


def mask_prediction(yolo_model, input_files, trainingDataset , output_folder, cut_image = False,tile_len = 800,tile_overlap = 0):
    '''
    Saved models do NOT contain prediction category descriptions or names, but only a category number. 
    To make sure the labels are correct, we need to use the metadata from the training dataset for this model.
    '''
    logger = setup_logger()    
    tile_image_length = tile_len
    overlap = tile_overlap
    boundary_shift = 0
    
    metadata = MetadataCatalog.get(trainingDataset)
    logging.info('training classes:')
    logging.info(metadata.get("thing_classes", None))

    categories = [{'id': idx, 'name': value,"supercategory": trainingDataset} for idx, value in enumerate(metadata.thing_classes)]
    logging.info(categories)
    
    model_folder = os.path.join(output_folder,'prediction_' + trainingDataset)
    if not(os.path.isdir(model_folder)):
        os.makedirs(model_folder)
        
    new_json_file = trainingDataset + '_all_in_one.json'
    new_annotations = []
    new_images = []
    ann_id = 1
    new_image_id = 1
    
    if input_files:
        for image_path in input_files:
            image_folder = os.path.splitext(image_path)[0]
            if not(os.path.isdir(image_folder)):
                os.makedirs(image_folder)

            img = read_image(image_path, format="BGR")
            
            if os.path.isdir(output_folder):
                out_filename = os.path.join(image_folder,trainingDataset +'.jpg')
                out_filename2 = os.path.join(model_folder, os.path.basename(image_path))
                out_filename2_extension = os.path.splitext(out_filename2)[1]
            
            image_name = os.path.basename(image_path)
            
            all_masks = []
            all_scores = []
            all_labels = []

            start_time = time.time()
            
            if cut_image:
                # slice cutting on the raw image
                raw_image = img.copy()
                output_image = img.copy()
                
                # compute total tiles
                #for corner case 1500 tilelength 800 overlap 100 should be 2 tiles while 1501 should be 3
                if raw_image.shape[0]<=tile_image_length:
                    total_i = 0
                else:
                    total_i = int((raw_image.shape[0]-1 - tile_image_length)  / (tile_image_length - overlap))+1
                if raw_image.shape[1]<=tile_image_length:
                    total_j = 0
                else:
                    total_j = int((raw_image.shape[1]-1 - tile_image_length) / (tile_image_length - overlap))+1


                total_instances = 0
                # loop for each tile i for width and j for longth
                for j in range(total_j + 1):
                    for i in range(total_i + 1):
                        idx = j * (total_i + 1) + i
                        # start of shape[0], end of shape[0], start of shape[1], end of shape[1]
                        if i == total_i:
                            shape0_start = max(boundary_shift, raw_image.shape[0] - tile_image_length)
                            shape0_end = raw_image.shape[0] - boundary_shift
                        else:
                            shape0_start = boundary_shift + (tile_image_length - overlap) * i
                            shape0_end = shape0_start + tile_image_length

                        if j == total_j:
                            shape1_start = max(boundary_shift, raw_image.shape[1] - tile_image_length)
                            shape1_end = raw_image.shape[1] - boundary_shift
                        else:
                            shape1_start = boundary_shift + (tile_image_length - overlap) * j
                            shape1_end = shape1_start + tile_image_length

                        # shape0_start, shape0_end, shape1_start, shape1_end = tile_image_coordinate[idx]
                        tile_image = (raw_image[shape0_start: shape0_end, shape1_start:shape1_end, :]).copy()

                        # visualized_output, polygonTuple = predVisSingleImage(predictor, tile_image, metadata)
                        scaled_masks_poly, scores, classes, im0 = yolo_predict_one_image(yolo_model,tile_image,imgsz=(tile_image.shape[0],tile_image.shape[1]))
                        
                        output_image[shape0_start: shape0_end, shape1_start:shape1_end, :] = im0
                        
                        total_polygons = len(scores)
                        if total_polygons:
                            for idx in range(total_polygons):
                                mask = scaled_masks_poly[:,:,idx]
                                segmentation = binary_mask_to_polygon(mask.astype(int), tolerance=0)
                                for item in segmentation:
                                    if len(item) > 6:
                                        list1 = []
                                        for point_i in range(0, len(item), 2):
                                            list1.append([shape1_start + item[point_i], shape0_start + item[point_i + 1]])

                                        current_polygon = np.array(list1)

                                        all_masks.append(Polygon(list1))
                                        all_scores.append(scores[idx])
                                        all_labels.append(int(classes[idx]))                                            
                                                                   

                        total_instances += total_polygons
                logger.info(
                    "{}: detected {} instances in {:.2f}s".format(
                        image_path, total_instances, time.time() - start_time
                    )
                )

                for each_class_id in set(all_labels):
                    each_class_masks = [each_mask for each_mask, each_label in zip(all_masks, all_labels) if each_label == each_class_id and each_mask.is_valid]
                    union_masks = unary_union(each_class_masks)
                    label_names = metadata.get("thing_classes", None)
                    # print(type(union_masks))
                    if union_masks.geom_type == 'MultiPolygon':
                        for current_mask in union_masks:
                            current_polygon_list = current_mask.exterior.coords
                            current_polygon_list_xy = current_mask.exterior.coords.xy

                            coco_segmentation_format = np.array(current_mask.exterior.coords).reshape(1, len(current_mask.exterior.coords) * 2).tolist()
                            # append annotation to coco jason file list
                            new_annotations.append({"id": ann_id,
                                                    "image_id": new_image_id,
                                                    "category_id": each_class_id,
                                                    "iscrowd": 0,
                                                    "segmentation": coco_segmentation_format
                                                    })
                            # get new annotation id
                            ann_id += 1
                            
                    else:
                        current_polygon_list = union_masks.exterior.coords
                        current_polygon_list_xy = union_masks.exterior.coords.xy

                        coco_segmentation_format = np.array(current_polygon_list).reshape(1, len(union_masks.exterior.coords) * 2).tolist()
                        # append annotation to coco jason file list
                        new_annotations.append({"id": ann_id,
                                                "image_id": new_image_id,
                                                "category_id": each_class_id,
                                                "iscrowd": 0,
                                                "segmentation": coco_segmentation_format
                                                })
                        # get new annotation id
                        ann_id += 1
                
                # append image information to coco jason file list
                new_images.append({"file_name": image_name,
                                   "id": new_image_id,
                                   "height": raw_image.shape[0],
                                   "width": raw_image.shape[1]})
                # get new image id
                new_image_id += 1               
                
                # save output image
                # cv2.imwrite(out_filename,output_image) #replace by the merge_polygones
                cv2.imwrite(out_filename2,output_image) 
            
            else:
                # visualized_output, polygonTuple = predVisSingleImage(predictor, img, metadata)
                scaled_masks_poly, scores, classes, im0 = yolo_predict_one_image(yolo_model, img,imgsz=(tile_len, tile_len))
                
                total_polygons = len(scores)
                if total_polygons:
                    for idx in range(total_polygons):
                        mask = scaled_masks_poly[:,:,idx]
                        segmentation = binary_mask_to_polygon(mask.astype(int), tolerance=0)
                        for item in segmentation:
                            if len(item) > 6:
                                list1 = []
                                for point_i in range(0, len(item), 2):
                                    list1.append([item[point_i], item[point_i + 1]])

                                current_polygon = np.array(list1)

                                all_masks.append(Polygon(list1))
                                all_scores.append(scores[idx])
                                all_labels.append(int(classes[idx]))
                    
                for each_class_id in set(all_labels):
                    each_class_masks = [each_mask for each_mask, each_label in zip(all_masks, all_labels) if each_label == each_class_id and each_mask.is_valid]
                    union_masks = unary_union(each_class_masks)
                    label_names = metadata.get("thing_classes", None)
                    # print(type(union_masks))
                    if union_masks.geom_type == 'MultiPolygon':
                        for current_mask in union_masks:
                            if current_mask.area < 100:
                                continue
                            current_polygon_list = current_mask.exterior.coords
                            current_polygon_list_xy = current_mask.exterior.coords.xy

                            coco_segmentation_format = np.array(current_mask.exterior.coords).reshape(1, len(current_mask.exterior.coords) * 2).tolist()
                            # append annotation to coco jason file list
                            new_annotations.append({"id": ann_id,
                                                    "image_id": new_image_id,
                                                    "category_id": each_class_id,
                                                    "iscrowd": 0,
                                                    "segmentation": coco_segmentation_format
                                                    })
                            # get new annotation id
                            ann_id += 1
                    else:
                        if union_masks.area < 100:
                            continue
                        current_polygon_list = union_masks.exterior.coords
                        current_polygon_list_xy = union_masks.exterior.coords.xy

                        coco_segmentation_format = np.array(current_polygon_list).reshape(1, len(union_masks.exterior.coords) * 2).tolist()
                        # append annotation to coco jason file list
                        new_annotations.append({"id": ann_id,
                                                "image_id": new_image_id,
                                                "category_id": each_class_id,
                                                "iscrowd": 0,
                                                "segmentation": coco_segmentation_format
                                                })
                        # get new annotation id
                        ann_id += 1
                # save output image
                cv2.imwrite(out_filename,im0) 
                cv2.imwrite(out_filename2,im0) 
                # visualized_output.save(out_filename)
                # visualized_output.save(out_filename2) 

                # append image information to coco jason file list
                new_images.append({"file_name": image_name,
                                   "id": new_image_id,
                                   "height": img.shape[0],
                                   "width": img.shape[1]})
                # get new image id
                new_image_id += 1 

                # output_image = visualized_output.get_image()[:, :, ::-1]
  
            
        info = {"year": 2022,
                "version": "1.0",
                "description": "Cutting the large image into small pieces and selecting desired classes",
                "contributor": "Ruixu Liu, Delin Shen, Aaron Lee and Qiang Wang",
                }

        json_data = {"info": info,
                     "categories": categories,
                     "images": new_images,
                     "annotations": new_annotations
                     }

        with open(os.path.join(model_folder,new_json_file), "w") as jsonfile:
            json.dump(json_data, jsonfile, sort_keys=True, indent=4)
        
        vis_out = merge_polygones(output_folder,os.path.join(model_folder,new_json_file),trainingDataset)
        output_image = vis_out.get_image()[:, :, ::-1]
        return output_image


def close_contour(contour):
    if not np.array_equal(contour[0], contour[-1]):
        contour = np.vstack((contour, contour[0]))
    return contour

def binary_mask_to_polygon(binary_mask, tolerance=0):
    """Converts a binary mask to COCO polygon representation
    Args:
        binary_mask: a 2D binary numpy array where '1's represent the object
        tolerance: Maximum distance from original points of polygon to approximated
            polygonal chain. If tolerance is 0, the original coordinate array is returned.
    """
    polygons = []
    # pad mask to close contours of shapes which start and end at an edge
    padded_binary_mask = np.pad(binary_mask, pad_width=1, mode='constant', constant_values=0)
    contours = measure.find_contours(padded_binary_mask, 0.5)
    contours = np.subtract(contours, 1)
    for contour in contours:
        contour = close_contour(contour)
        contour = measure.approximate_polygon(contour, tolerance)
        if len(contour) < 3:
            continue
        contour = np.flip(contour, axis=1)
        segmentation = contour.ravel().tolist()
        # after padding and subtracting 1 we may get -0.5 points in our segmentation
        segmentation = [0 if i < 0 else i for i in segmentation]
        polygons.append(segmentation)
    return polygons

def img_tobyte(im_cv):
    im_rgb = cv2.cvtColor(im_cv, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(im_rgb)
    ENCODING = 'utf-8'
    img_byte = io.BytesIO()
    img_pil.save(img_byte, format='JPEG')
    binary_str2 = img_byte.getvalue()
    imageData = base64.b64encode(binary_str2)
    base64_string = imageData.decode(ENCODING)
    return base64_string

def merge_polygones(image_folder,json_file,trainingDataset):
    allColors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255), (75,125,255), (125,75,255), (75,255,125), (125,255,75), (255,125,75), (255,75,125)]*8
    filename = str(uuid.uuid4())
    register_coco_instances(filename, {'thing_colors':allColors}, json_file, image_folder)
    metadata = MetadataCatalog.get(filename)
    dicts = DatasetCatalog.get(filename)
    model_folder = os.path.join(image_folder,'prediction_' + trainingDataset)
    logging.info(f"Merging {trainingDataset} polygons")
    for dic in dicts:
        img = utils.read_image(dic["file_name"], "RGB")
        visualizer = Visualizer(img, metadata=metadata, instance_mode=ColorMode.SEGMENTATION)
        vis = visualizer.draw_dataset_dict(dic)
        out_filename = os.path.join(os.path.splitext(os.path.basename(dic["file_name"]))[0],trainingDataset +'_merged.jpg')
        
        out_filename2_extention = os.path.splitext(os.path.basename(dic["file_name"]))[1]
        out_filename2 = os.path.basename(dic["file_name"]).replace(out_filename2_extention,'_merged'+out_filename2_extention)
        vis.save(os.path.join(image_folder,out_filename))
        # vis.save(os.path.join(model_folder,out_filename2)) # model folder is not necessary
    logging.info("Merging Finished.")
    return vis

def translate(classes, scores, class_names):
    labels = None
    if classes is not None:
        if class_names is not None and len(class_names) > 0:
            labels = [class_names[i] for i in classes]
        else:
            labels = [str(i) for i in classes]
    if scores is not None:
        if labels is None:
            labels = ["{:.0f}%".format(s * 100) for s in scores]
        else:
            labels = ["{} {:.0f}%".format(l, s * 100) for l, s in zip(labels, scores)]
    return labels

def inputimage_list(input_folder):
    files = os.listdir(input_folder)
    input_files = [os.path.join(input_folder, x) for x in files if os.path.splitext(x)[1] in ['.jpg','.png']]
    return input_files


def roof_predict(yolo_roof_model, yolo_damage_model, yolo_equipment_model, folder):
    demoFolder = folder
    ############################################ input Image
    input_files = inputimage_list(input_folder = demoFolder)
    logging.info(input_files)
    
    ########################################## dataset config
    imgsetUrl = 'test_360.jpg'

    cocoJsonPairs = {
        'Roof_boundary' : 'roof_boundary.json',
        'Roof_damage' : 'roof_damage.json',
        'Roof_equipment' : 'roof_equipment.json',
    }

    for datasetName, jsonURL in cocoJsonPairs.items():     
        if datasetName not in DatasetCatalog:
            # there is a way to load the labels from the detectron2 datasets. should replace this piece.
            with open(jsonURL) as f:
                cocoFile = json.load(f)
            catMap = {str(cat['id']): cat['name'] for cat in cocoFile['categories']}  # coco file category ID starts from 1
            logging.info(catMap)
            catIDs = [int(key) for key in catMap.keys()] # when detectron2 load a coco dataset, the categories are sorted by IDs, and mapped to [1, lengthOfCatetories] as a subset of [1,80).

            # To make sure the labels are in the same order as the IDs when passed to register the dataset
            catIDs.sort() 
            labels = [catMap[str(catID)] for catID in catIDs]
            allColors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255), (75,125,255), (125,75,255), (75,255,125), (125,255,75), (255,125,75), (255,75,125)]*8 
            # 12 colors; repeat 8 times in case there are more labels than 12; need a better way to assign the colors
            colors = allColors[:len(labels)]
            logging.info('dataset: %s has %i labels and %i colors ' % (datasetName, len(labels), len(colors)))
            register_coco_instances(datasetName, {'thing_classes':labels, 'thing_colors':colors}, jsonURL, imgsetUrl) 
            # the 2nd parameter is metadata, in this case we pass over thing_classes for Visualizer to use    
        else: 
            logging.info('%s already registered!' % datasetName)

    ############################################# Models
    last_roof_boundary_result = mask_prediction(yolo_roof_model, input_files, trainingDataset='Roof_boundary', output_folder=demoFolder,  cut_image = False, tile_len = 1984, tile_overlap = 500)
    last_damage_result = mask_prediction(yolo_damage_model, input_files, trainingDataset='Roof_damage', output_folder=demoFolder,  cut_image = True, tile_len = 800, tile_overlap = 100)
    last_equipment_result = mask_prediction(yolo_equipment_model, input_files, trainingDataset='Roof_equipment', output_folder=demoFolder,  cut_image = True, tile_len = 800, tile_overlap = 100)
