"""Various functions for processing device matrices.
"""

import copy
import numpy as np
import cv2


def binarize(device, eta=0.5, beta=np.inf):
    """Binarize a greyscale device using sigmoid function.
    """
    num = np.tanh(beta*eta) + np.tanh(beta*(device - eta))
    den = np.tanh(beta*eta) + np.tanh(beta*(1 - eta))
    device = num/den
    return device


def binarize_hard(device, eta=0.5):
    """Binarize a greyscale device using step function.
    """
    device[device < eta] = 0
    device[device >= eta] = 1
    return device


def binarize_sem(sem, limit=150, blur=9):
    """Adaptive threshold binarization of SEM image.
    """
    sem[sem > limit] = limit
    sem = cv2.GaussianBlur(sem, (blur, blur), 0)
    _, sem = cv2.threshold(sem.astype("uint8"), 0, 255,
                           cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return sem


def trim(device):
    """Trim whitespace of a device matrix.
    """
    x_range, y_range = np.nonzero(device)
    return device[x_range.min():x_range.max()+1, y_range.min():y_range.max()+1]


def clip(device, margin):
    """Manual trimming of device matrix edges.
    """
    mask = np.zeros_like(device)
    mask[margin:-margin, margin:-margin] = 1
    device = mask*device
    return device


def pad(device, slice_length, padding=1):
    """Pad device matrix to multiple of slice_length
    """
    pady = (slice_length*np.ceil(device.shape[0]/slice_length) -
            device.shape[0])/2 + slice_length*(padding - 1)/2
    padx = (slice_length*np.ceil(device.shape[1]/slice_length) -
            device.shape[1])/2 + slice_length*(padding - 1)/2
    device = np.pad(device, [(int(np.ceil(pady)), int(np.floor(pady))),
                    (int(np.ceil(padx)), int(np.floor(padx)))],
                    mode='constant')
    return device


def autoscale(device, slice_length, device_length, res):
    """Autoscale device matrix to standardized profile.
    """
    device = trim(device)
    scale = 1/(res/(device_length/device.shape[1]))
    device = cv2.resize(device, (0, 0), fx=scale, fy=scale)
    device = binarize(device)
    device = pad(device, slice_length=slice_length, padding=2)
    return device


def get_contour(device, linewidth=None):
    """Get the contour of a device matrix.
    """
    if linewidth is None:
        linewidth = int(device.shape[0]/100)
    _, thresh = cv2.threshold(device.astype(np.uint8), 0.5, 1, 0)
    contours, _ = cv2.findContours(thresh, 2, 1)
    overlay = np.zeros_like(device)
    cv2.drawContours(overlay, contours, -1, (255, 255, 255), linewidth)
    overlay = np.ma.masked_where(overlay == 0, overlay)
    return overlay


def get_uncertainty(prediction):
    """Get uncertainty profile of a prediction.
    """
    uncertainty = 1 - 2*np.abs(0.5 - prediction)
    return uncertainty


def design_rule_check(device, min_feature, min_gap, scan_step=5):
    """Simple design rule checker (DRC).
    """
    _, thresh = cv2.threshold(device.astype(np.uint8), 0.5, 1, 0)
    contours, _ = cv2.findContours(thresh, 2, 1)

    error_locations = []
    drc = copy.deepcopy(device)

    for contour in contours:
        for idx, _ in enumerate(contour[scan_step:-scan_step-1]):
            delta_y = (contour[idx-scan_step][0][1] -
                       contour[idx+scan_step][0][1])/2/scan_step
            delta_x = (contour[idx-scan_step][0][0] -
                       contour[idx+scan_step][0][0])/2/scan_step
            current_y = contour[idx][0][1]
            current_x = contour[idx][0][0]
            in_y = np.clip(current_y + int(delta_x*min_feature), 0,
                           device.shape[0]-1)
            in_x = np.clip(current_x - int(delta_y*min_feature), 0,
                           device.shape[1]-1)
            out_y = np.clip(current_y - int(delta_x*min_gap), 0,
                            device.shape[0]-1)
            out_x = np.clip(current_x + int(delta_y*min_gap), 0,
                            device.shape[1]-1)

            # boundary exclusion
            if device.shape[1]-1 in [in_x, in_y, out_x, out_y]:
                continue
            if device.shape[0]-1 in [in_x, in_y, out_x, out_y]:
                continue
            if 0 in [in_x, in_y, out_x, out_y]:
                continue

            # "paint" the DRC pattern
            if device[out_y, out_x] == 1:
                error_locations.append([current_y, current_x])
                drc[current_y, current_x] = 20
            if device[in_y, in_x] == 0:
                error_locations.append([current_y, current_x])
                drc[current_y, current_x] = 10

    print('There were ' + str(len(error_locations)) + ' error pixels found')

    return drc, error_locations
