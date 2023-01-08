"""Functions to handle loading and saving devices, designs, SEMs, etc.
"""

import matplotlib.image as img
import numpy as np
import gdspy
import cv2
from prefab.processor import autoscale


def load_device_img(path, slice_length, device_length, res):
    """Load device in from an image file.
    """
    device = img.imread(path)[:, :, 1]
    device = autoscale(device, slice_length, device_length, res)
    return device


def load_device_gds(path, cell_name, coords=None):
    """Load device in from GDS file.
    """
    gds = gdspy.GdsLibrary(infile=path)
    cell = gds.cells[cell_name]
    polygons = cell.get_polygons(by_spec=(1, 0))
    bounds = 1000*cell.get_bounding_box()
    device = np.zeros((int(bounds[1][1] - bounds[0][1]),
                       int(bounds[1][0] - bounds[0][0])))

    # this needs a better method
    contours = []
    for k, _ in enumerate(polygons):
        contour = []
        for j, _ in enumerate(polygons[k]):
            contour.append([[int(1000*polygons[k][j][0] - bounds[0][0]),
                             int(1000*polygons[k][j][1] - bounds[0][1])]])
        contours.append(np.array(contour))
    cv2.drawContours(device, contours, -1, (255, 255, 255), -1)

    if coords is not None:
        device = device[int(coords[0][1] - bounds[0][1]):
                        int(coords[1][1] - bounds[0][1]),
                        int(coords[0][0] - bounds[0][0]):
                        int(coords[1][0] - bounds[0][0])]

    device = np.flipud(device)
    return device


def load_sem(path, res, res_sem=None):
    """Load SEM image from TIF file.
    """
    sem = img.imread(path)[:, :, 1]
    if res_sem is None:
        res_sem = get_sem_resolution(path)
    scale = res_sem/res
    sem = cv2.resize(sem, (0, 0), fx=scale, fy=scale)
    return sem


def load_device_sem(sem, x1, x2, y1, y2):
    """Load specific device from SEM TIF file.
    """
    device = sem[y1:y2, x1:x2]
    # device = binarize_sem(device)
    # device = trim(device)
    # device = pad(device, slice_length=128, padding=2)
    # device = device/255
    return device


def get_sem_resolution(path):
    """Get resolution of SEM from TIF file.
    """
    with open(path, 'rb') as tif:
        for line in tif:
            if 'Image Pixel Size' in str(line):
                res = float(str(line[19:24])[2:7])
    return res


def device_to_cell(device, cell_name, library, res, layer=1):
    """Convert device matrix to gdspy reference cell.
    """
    device = np.flipud(device)
    _, thresh = cv2.threshold(device.astype(np.uint8), 0.5, 1, 0)
    contours = cv2.findContours(thresh, cv2.RETR_CCOMP,
                                cv2.CHAIN_APPROX_SIMPLE)

    outers = []
    inners = []
    for idx, contour in enumerate(contours[0]):
        if len(contour) > 2:
            contour = contour/1000  # μm to nm
            points = contour.squeeze().tolist()
            points = list(tuple(sub) for sub in points)
            if contours[1][0][idx][3] == -1:
                outers.append(points)
            else:
                inners.append(points)

    poly = gdspy.boolean(outers, inners, 'xor', layer=layer)
    poly = poly.scale(res, res)
    cell = library.new_cell(cell_name)
    cell.add(poly)
    return gdspy.CellReference(cell)
