# Standard library imports.
import os
from typing import Union
import glob

# Third party imports.
import pydicom as pdc
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import pygame as pg
from slugify import slugify as slug


class Scan():
    """
    A class that stores a scan and its associated data.

    Attributes
    ----------
        data: list or pydicom.dataset.FileDataset
            The DICOM data.
        threshold: dict
            The threshold values for different tissue types.            
        path: string
            The path to the directory containing the scan.
        filenames: list or string
            The filename(s) of the DICOM files.
        scan_id: string
            The ID of the scan.
        date: string
            The date of the scan.
        time: string
            The time of the scan.
        patient_name: string
            The name of the patient.
        patient_id: string
            The ID of the patient.
        patient_birth_date: string
            The birth date of the patient.
        scan: numpy.ndarray
            The images of the scan.
        pixel_size: [float, float]
            The pixel size of the scan in mm.
        slice_thickness: float
            The slice thickness of the scan in mm.
        spacing_between_slices: float
            The spacing between the centres of two adjacent slices in 
            mm.
        
        
    """
    def __init__(self, scan_list: Union[list, pdc.dataset.FileDataset]):
        """
        The constructor for the Scan class.

        Parameters
        ----------
            scan_list: list or pydicom.dataset.FileDataset
                A list of DICOM files or a single DICOM file.
        """
        self.data = scan_list
        self.threshold ={
                        'Air': [-2000, -801],
                        'Lung': [-800, -300],
                        'Fat': [-120, -60],
                        'Fluid': [-10, 20],
                        'Soft Tissue': [21, 300],
                        'Bone': [301, 1500],
                        'Foreign Object': [1501, 30000]
                        }
        # If the scan_list is a list of DICOM files.
        if type(scan_list) == list:
            self.path = os.path.dirname(scan_list[0].filename)
            self.filenames = [os.path.basename(file.filename) for file 
                                in scan_list]
            self.scan_id = scan_list[0].SeriesInstanceUID
            self.date = scan_list[0].StudyDate
            self.time = scan_list[0].StudyTime
            self.patient_name = scan_list[0].PatientName
            self.patient_id = scan_list[0].PatientID
            self.patient_birth_date = scan_list[0].PatientBirthDate
            self.scan = np.array([self._reset_image_intensity(
                                                image.pixel_array, 
                                                image.RescaleSlope,
                                                image.RescaleIntercept) 
                                            for image in scan_list])
            self.pixel_size = scan_list[0].PixelSpacing
            self.slice_thickness = float(scan_list[0].SliceThickness)
            # Checks if the spacing between slices is stored in the 
            # DICOM files
            if 'SpacingBetweenSlices' in scan_list[0].dir():
                self.spacing_between_slices = float(scan_list[0]\
                                                .SpacingBetweenSlices)
            # If not, it is calculated from the slice positions
            else:
                self.spacing_between_slices = \
                                    abs(\
                                        np.mean(\
                                            np.diff(\
                                                np.array(\
                                                    [image.SliceLocation for 
                                                    image in scan_list]))))
        # If a single DICOM file is passed
        elif type(scan_list) == pdc.dataset.FileDataset:
            self.path = os.path.dirname(scan_list.filename)
            self.filenames = os.path.basename(scan_list.filename)
            self.scan_id = scan_list.SeriesInstanceUID
            self.date = scan_list.StudyDate
            self.time = scan_list.StudyTime
            self.patient_name = scan_list.PatientName
            self.patient_id = scan_list.PatientID
            self.patient_birth_date = scan_list.PatientBirthDate
            self.scan = self._reset_image_intensity(scan_list.pixel_array, 
                                            scan_list.RescaleSlope,
                                            scan_list.RescaleIntercept)
            self.pixel_size = scan_list.PixelSpacing
            self.slice_thickness = float(scan_list.SliceThickness)
            # Checks if the spacing between slices is stored in the 
            # DICOM files
            if 'SpacingBetweenSlices' in scan_list.dir():
                self.spacing_between_slices = float(scan_list\
                                                        .SpacingBetweenSlices)
            # If not, it is calculated set as the slice thickness
            else:
                self.spacing_between_slices = self.slice_thickness
        # If DICOM files are not passed
        else:
            raise TypeError("The scan_list parameter must be a list of " +
                            "pdc.dataset.FileDatasets or a single " + 
                            "pdc.dataset.FileDataset")
        
    def __repr__(self):
        """
        Returns a string representation of the Scan class.

        Returns
        -------
            string
                A string representation of the Scan class.
        """
        description = "Scan: \n"
        description +=  "__________\n"
        description += f"Date: {self.date} \nTime: {self.time} \n"
        description += (f"Patient: \n\tName: {self.patient_name} \n\tID: " +
            f"{self.patient_id} \n\tBirth Date: {self.patient_birth_date} \n")
        description += f"Scan ID: {self.scan_id} \n"
        description += f"Path: {self.path} \n"
        return description

    def _reset_image_intensity(self, image: np.ndarray, slope: float, 
                                intercept: float):
        """
        Resets the intensity of an imported image to the original 
        Hounsfield units.
        
        Parameters
        ----------
            image: numpy.ndarray
                The image to be reset.
            slope: float
                The slope of the image.
            intercept: float
                The intercept of the image.
        
        Returns
        -------
            image: numpy.ndarray
                The image with the intensity reset.
        """
        # Checks the type of the image
        if type(image) != np.ndarray:
            raise TypeError("The image parameter must be a numpy.ndarray.")
        # Checks the type of the slope
        try: 
            slope_float = float(slope)
        except:
            raise TypeError("The slope parameter must be a float.")
        # Checks the type of the intercept
        try:
            intercept_float = float(intercept)
        except:
            raise TypeError("The intercept parameter must be a float.")
        
        return image * slope_float + intercept_float

    def change_threshold(self, threshold: dict):
        """
        Changes the threshold values for different tissue types. The 
        keys of the dictionary must at least contain an entry for 'Air' 
        to act as a background as well as 'Lung' and 'Soft Tissue'.

        Parameters
        ----------
            threshold: dict
                The new threshold values for different tissue types in 
                the form:
                {'Tissue Type': [lower bound, upper bound]}.
        """
        # Checks the type of the threshold
        if type(threshold) != dict:
            raise TypeError("The threshold parameter must be a dictionary.")
        # Checks the keys of the threshold
        if 'Air' in threshold.keys() and 'Lung' in threshold.keys()\
                and  'Soft Tissue' in threshold.keys():
            # Checks the type of the values
            for key in threshold.keys():
                if type(threshold[key]) != list:
                    raise TypeError("The values of the threshold " +
                        "dictionary must be in lists.")
                # Checks the length of the values
                if len(threshold[key]) != 2:
                    raise ValueError("The values of the threshold " +
                        "dictionary must be lists of length 2.")
                # Checks the type of the values
                for ind, value in enumerate(threshold[key]):
                    try:
                        threshold[key][ind] = int(value)
                    except:
                        raise TypeError("The values of the threshold " +
                            "dictionary must be lists of integers.")
            self.threshold = threshold
        else:
            raise ValueError("The threshold dictionary must contain an "+
                "entry for 'Air' 'Lung' and 'Soft Tissue'.")


class MaskedScan():
    """
    Class to store the information of a segment.

    Attributes
    ----------
        scan_obj: ct_analyser.cta.Scan
            The scan that the segment is from with all of the associated
            information.
        mask: numpy.ndarry
            The binary array containing the segment.
        scan: numpy.ndarry
            The original scan array before any processing.
        masked_scan: numpy.ndarry
            The scan with the segments applied as a mask.
        date: str
            The date of the scan.
        time: str
            The time of the scan.
        scan_id: str
            The ID of the scan.
        patient_name: str
            The name of the patient.
        patient_id: str
            The ID of the patient.
        patient_birth_date: str
            The birth date of the patient.
        pixel_size: float
            The pixel size of the scan.
        slice_thickness: float
            The slice thickness of the scan.
        spacing_between_slices: float
            The spacing between slices of the scan.
        threshold: dict
            The thresholds of different tissues in the scan.
    """

    def __init__(self, mask: np.ndarray, scan: Scan):
        """
        Builds the class and sets the attributes.
        
        Parameters
        ----------
            mask: numpy.ndarry
                The binary array containing the segment.
            scan: ct_analyser.cta.Scan
                The scan that the segment is from with all of the 
                associated scan information.
        """
        # Check the type of the mask.
        if type(mask) != np.ndarray:
            raise TypeError("The mask must be of type numpy.ndarry not " + 
                            str(type(mask)))
        # Check size of the mask.
        elif mask.shape != scan.scan.shape:
            raise ValueError("The mask must be the same size as the scan.")
        # Check the type of the scan.
        if type(scan) != Scan:
            raise TypeError("The scan must be of type Scan not " + 
                            str(type(scan)))
        # Assign the attributes.
        self.scan_obj = scan
        self.mask = mask
        self.scan = scan.scan
        self.masked_scan = _apply_mask(scan.scan, mask)
        self.date = scan.date
        self.time = scan.time
        self.scan_id = scan.scan_id
        self.patient_name = scan.patient_name
        self.patient_id = scan.patient_id
        self.patient_birth_date = scan.patient_birth_date
        self.pixel_size = scan.pixel_size
        self.slice_thickness = scan.slice_thickness
        self.spacing_between_slices = scan.spacing_between_slices
        self.threshold = scan.threshold

    def __repr__(self):
        """
        Returns a string representation of the class.
        
        Returns
        -------
            str:
                A string representation of the class.
        """
        description = "MaskedScan: \n"
        description += '__________\n'
        description += f"Date: {self.date} \nTime: {self.time} \n"
        description += f"Patient: \n\tName: {self.patient_name} \n\tID: " + \
            f"{self.patient_id} \n\tBirth Date: {self.patient_birth_date} \n"
        description += f"Scan ID: {self.scan_id} \n"

        return description
        
    def intersect_mask(self, mask: np.ndarray, start: int=None):
        """
        Intersects a mask with the segment.
        
        Parameters
        ----------
            mask: numpy.ndarry
                The binary mask to intersect with the segment.
            start: int, optional
                The start slice of the mask to intersect with the 
                segment.
        """
        # Check the type of the mask.
        if type(mask) != np.ndarray:
            raise TypeError("The mask must be of type numpy.ndarry not " + 
                            str(type(mask)))
        # Check the type of the start index.
        if start is not None:
            try:
                # Convert to int.
                start_ind = int(start)
            except:              
                raise TypeError("The start index must be of type int not " + 
                            str(type(start)))
        if mask.shape == self.mask.shape:
            self.mask = np.logical_and(self.mask, mask)
            self.masked_scan = _apply_mask(self.scan, self.mask)
        else:
            if start is None:
                raise ValueError("Mask shape does not match segment shape.")
            else:
                # Check dimensions of mask.
                if np.ndim(mask) == 2:
                    # Check the start index is within the mask.
                    if start_ind < 0:
                        raise ValueError("The start index must be within " + 
                                        "the mask.")
                    # Combine the mask.
                    else:
                        # If self.mask is 3d
                        if np.ndim(self.mask) == 3:
                            self.mask = np.logical_and(\
                                                        self.mask[start_ind], 
                                                        mask)
                            self.masked_scan = _apply_mask(
                                                        self.scan[start_ind], 
                                                        self.mask)
                        # If self.mask is 2d
                        elif np.ndim(self.mask) == 2:
                            self.mask = np.logical_and(self.mask, mask)
                            self.masked_scan = _apply_mask(self.scan, 
                                                            self.mask)
                        else:
                            raise ValueError("MaskedScan.mask must be " +
                                            "2D or 3D.")
                elif np.ndim(mask) == 3:
                    # Check that the index is within the mask and the
                    # mask is not larger than the segment.
                    if start_ind < 0 or start_ind > self.mask.shape[0] or \
                            start_ind + mask.shape[0] > self.mask.shape[0]:
                        raise ValueError("The start index must be within " + 
                                        "the mask.")
                    # Combine the mask.
                    else:
                        self.mask = \
                            np.logical_and(self.mask[start_ind:\
                                start_ind+mask.shape[0]], mask)
                        self.masked_scan = _apply_mask(\
                                self.scan[start_ind:start_ind+mask.shape[0]], 
                                self.mask)
                else:
                    raise ValueError("The mask must be 2D or 3D.")
        
    def combine_mask(self, mask: np.ndarray, start: int = None):
        """
        Combines a mask with the segment.
        
        Parameters
        ----------
            mask: numpy.ndarry
                The binary mask to combine with the segment.
            start: int, optional
                The start slice of the mask to combine with the segment.
                Used if the mask is a different size to the segment.
        """
        # Check the type of the mask.
        if type(mask) != np.ndarray:
            raise TypeError("The mask must be of type numpy.ndarry not " + 
                            str(type(mask)))
        # Check the type of the start index.
        # Check the type of the start index.
        if start is not None:
            try:
                # Convert to int.
                start_ind = int(start)
            except:              
                raise TypeError("The start index must be of type int not " + 
                            str(type(start)))
        if mask.shape == self.mask.shape:
            self.mask = np.logical_or(self.mask, mask)
            self.masked_scan = _apply_mask(self.scan, self.mask)
        else:
            if start is None:
                raise ValueError("Mask shape does not match segment shape.")
            else:
                # Check dimensions of mask.
                if np.ndim(mask) == 2:
                    # Check the start index is within the mask.
                    if start_ind < 0:
                        raise ValueError("The start index must be within " + 
                                        "the mask.")
                    # Combine the mask.
                    else:
                        # If self.mask is 3d
                        if np.ndim(self.mask) == 3:
                            self.mask[start_ind] = np.logical_or(\
                                                        self.mask[start_ind], 
                                                        mask)
                            self.masked_scan[start_ind] = _apply_mask(
                                                        self.scan[start_ind], 
                                                        self.mask)
                        # If self.mask is 2d
                        elif np.ndim(self.mask) == 2:
                            self.mask = np.logical_or(self.mask, mask)
                            self.masked_scan = _apply_mask(self.scan, 
                                                            self.mask)
                        else:
                            raise ValueError("MaskedScan.mask must be " +
                                                    "2D or 3D.")
                elif np.ndim(mask) == 3:
                    # Check that the index is within the mask and the
                    # mask is not larger than the segment.
                    if start_ind < 0 or start_ind > self.mask.shape[0] or \
                            start_ind + mask.shape[0] > self.mask.shape[0]:
                        raise ValueError("The start index must be within " + 
                                        "the mask.")
                    # Combine the mask.
                    else:
                        self.mask[start_ind:start_ind+mask.shape[0]] = \
                            np.logical_or(self.mask[start_ind:\
                                start_ind+mask.shape[0]], mask)
                        self.masked_scan[start_ind:start_ind+mask.shape[0]] = \
                            _apply_mask(self.scan[start_ind:\
                                start_ind+mask.shape[0]], 
                                self.mask[start_ind:start_ind+mask.shape[0]])
                else:
                    raise ValueError("The mask must be 2D or 3D.")

           

def import_dicom (path: str):
    """
    Imports a DIICOM file from a given path. If the path is to a 
    directory, then all of the DICOMS are loaded in (provided that they 
    are of the same scan). Any subdirectories will be excluded. If the 
    path is to a  single file, then the file is loaded in. 

    Parameters
    ----------
        path: string
            The path to the DICOM file or directory.
    
    Returns
    -------
        data: ct_analyser.cta.Scan
            The DICOM data.
    """
    # Check if path is a string.
    if type(path) != str:
        # raise error if path is not a string.
        raise TypeError(f'The path must be a string, not {type(path)}.')
    if os.path.isdir(path):
        scan_list = []
        # get list of files in directory with .dcm extension.
        file_list = np.sort(glob.glob(os.path.join(path, "*.dcm")))
        for ind, file in enumerate(file_list):
        # set first file as reference
            if ind == 0:
                ref_file = pdc.dcmread(file)
                ref_pt_id = ref_file.PatientID
                ref_series_id = ref_file.SeriesInstanceUID
                # append reference file to list.
                scan_list.append(ref_file)
            else:
                file = pdc.dcmread(file)
                # check that file metadata matches reference.
                if file.PatientID == ref_pt_id and \
                        file.SeriesInstanceUID == ref_series_id:
                    scan_list.append(file)
                else:
                    # raise error if metadata does not match reference file.
                    raise ValueError("The directory contains DICOM files " + \
                                    "from multiple scans.")
        # check if list is empty
        if len(scan_list) > 0:
            # get the order of the images in the series.
            scan_order = [image.InstanceNumber for image in scan_list]
            # sort the list by ascending order
            sorted_scan_list = [scan_list[i] for i in np.argsort(scan_order)]
            # check that the order does not contain any repeats and is 
            # sequential.
            rep, non_consec = _check_consecutiveness(\
                                                np.sort(scan_order).tolist())
            # raise error if there are repeats and non-consecutive 
            # slices.
            if rep and non_consec:
                # create error message.
                rep_err_msg = 'The following files have the same slice' + \
                                'location:\n\t'
                for i in rep:
                    for j in i:
                        # get the filename.
                        rep_err_msg += os.path.basename(\
                                                sorted_scan_list[j].filename)
                        if j != i[-1]:
                            rep_err_msg += ', '
                        elif i != rep[-1]:
                            rep_err_msg += ';\n\t'
                        else:
                            rep_err_msg += '.\n'
                # create error message.
                non_consec_err_msg = 'The following files have are not ' + \
                                        'consecutive:\n\t'
                for i in non_consec:
                    for j in i:
                        # get the filename.
                        non_consec_err_msg += \
                                            os.path.basename(\
                                                sorted_scan_list[j].filename)
                        if j != i[-1]:
                            non_consec_err_msg += ', '
                        elif i != non_consec[-1]:
                            non_consec_err_msg += ';\n\t'
                        else:
                            non_consec_err_msg += '.\n'
                # raise error.
                raise ValueError(rep_err_msg + non_consec_err_msg)
            # raise error if there are only repeats.
            elif rep:
                # create error message.
                rep_err_msg = 'The following files have the same slice' + \
                                'location:\n\t'
                for i in rep:
                    for j in i:
                        # get the filename.
                        rep_err_msg += os.path.basename(\
                                                sorted_scan_list[j].filename)
                        if j != i[-1]:
                            rep_err_msg += ', '
                        elif i != rep[-1]:
                            rep_err_msg += ';\n\t'
                        else:
                            rep_err_msg += '.\n'
                # raise error.
                raise ValueError(rep_err_msg)
            # raise error if there are only non-consecutive slices.
            elif non_consec:
                # create error message.
                non_consec_err_msg = 'The following files have are not ' + \
                                        'consecutive:\n\t'
                for i in non_consec:
                    for j in i:
                        # get the filename.
                        non_consec_err_msg += os.path.basename(\
                                                sorted_scan_list[j].filename)
                        if j != i[-1]:
                            non_consec_err_msg += ', '
                        elif i != non_consec[-1]:
                            non_consec_err_msg += ';\n\t'
                        else:
                            non_consec_err_msg += '.\n'
                # raise error.
                raise ValueError(non_consec_err_msg)
            # return the a scan object if there are no repeats or 
            # non-consecutive slices.
            else:
                return Scan(sorted_scan_list)
        else:
            # raise error if list is empty.
            raise FileNotFoundError("The directory does not contain any " + \
                                    "DICOM files.")
    # check if path is to a file
    elif os.path.isfile(path):
        # check if file is a DICOM file
        if path.endswith(".dcm"):
            return Scan(pdc.dcmread(path))
        else:
            # raise error if file is not a DICOM file.
            raise TypeError("The file must be a DICOM file.")
    # raise error if path does not exist.
    else:
        # raise error if path is not a string.
        if type(path) != str:
            raise TypeError("The path must be a string.")
        else:
            # raise error if path does not exist.
            raise FileNotFoundError("The path does not exist.")


def display_scan(scan: np.ndarray or Scan or MaskedScan,
            disp_type: str = 'gif', fig_size: tuple or list=(5,5), 
            interval_time=50):
    """
    Creates and displays an animation of the scan (or displays a static 
    image if the scan is 2D).
    
    Parameters
    ----------
        scan: numpy.ndarray or ct_analyser.cta.Scan or 
                ct_analyser.mask.MaskedScan
            2D or 3D array of the scan or a Scan object or a MaskedScan
            object. If a MaskedScan object is passed, the masked scan 
            will be displayed (not the original scan).
        disp_type: str
            The type of animation to create (either 'gif' or 'scroll' 
            or 'off')
        fig_size: tuple or list, optional
            The size of the figure.
        interval_time: int, optional
            The interval between frames in milliseconds.
        
    Returns
    -------
        animation: matplotlib.animation.ArtistAnimation or None
            The animation of the scan (or None if the scan is 2D).
    """
    # Check the type of scan.
    if type(scan) == np.ndarray:
        # Do nothing.
        disp_scan = np.array(scan)
    elif type(scan) == Scan:
        # Get the scan.
        disp_scan = np.array(scan.scan)
    elif type(scan) == MaskedScan:
        # Get the masked scan.
        disp_scan = np.array(scan.masked_scan)
    else:
        # Raise an error if the type of scan is invalid.
        raise TypeError('Scan must be a numpy array, a Scan object, '+
                        f'or a MaskedScan object and not a {type(scan)}.')
    # Check the type of disp_type.
    if type(disp_type) != str:
        # Raise an error if disp_type is not a string.
        raise TypeError('disp_type must be a string and not a ' + \
                        f'{type(disp_type)}.')
    # Check the type of figsize.
    if type(fig_size) != tuple and type(fig_size) != list:
        # Raise an error if figsize is not a tuple.
        raise TypeError('fig_size must be a tuple and not a ' +
                            f'{type(fig_size)}.')
    else:
        # Check the length of figsize.
        if len(fig_size) != 2:
            raise ValueError(f'figsize must be a tuple of length 2 and ' + \
                            f'not a tuple of length {len(fig_size)}.')
        else:
            # Check the type of the elements of figsize.
            for i in fig_size:
                try:
                    figsize = tuple(float(i) for i in fig_size)
                except:
                    raise TypeError(f'fig_size must be a tuple of floats '+ \
                                    f'and not a tuple of {type(i)}s.')

    # Check the type of interval.
    try:
        interval = int(interval_time)
    except:
        raise TypeError('interval_time must be an int and not a ' + \
                        f'{type(interval_time)}.')
    # Create the figure and axes.
    fig, ax = plt.subplots(figsize=figsize)
    # Remove the axes
    ax.axis('off')
    # Check if the scan is 2D or 3D.
    if disp_scan.ndim == 2:
        # Display the scan
        ax.imshow(disp_scan, cmap='gray')
        # Set the animation to None.
        ani = None
    elif disp_scan.ndim == 3:
        # Initialize the frames.
        frames = []
        # Loop through the frames.
        for i in range(disp_scan.shape[0]):
            # Create and append the frame.
            frame = ax.imshow(disp_scan[i], cmap='gray')
            frames.append([frame])
        # Determine the type of animation to create.
        if disp_type == 'gif':
            # Show the animation as a gif.
            ani = animation.ArtistAnimation(fig, frames, interval=interval, 
                                                    blit=True)
            plt.show()
        elif disp_type == 'scroll':
            # Display the animation as a scrollable image.
            ani = animation.ArtistAnimation(fig, frames, interval=interval, 
                                                    blit=True, repeat=False)
            plt.pause(interval*len(frames)/1000)
            plt.close(fig)
            # Show the animation as a scrollable image.
            _open_scan(disp_scan, True)
        elif disp_type == 'off':
            # Make the animation and immediately close the figure.
            ani = animation.ArtistAnimation(fig, frames, interval=interval, 
                                                    blit=True, repeat=False)
            plt.pause(interval*len(frames)/1000)
            # Close the figure.
            plt.close(fig)
        else:
            # Raise an error if the disp_type is invalid.
            raise ValueError('disp_type must be either "gif", "scroll", or "off"'+
                            f' not {disp_type}.')
        # Return the animation.
        return ani
    else:
        # Raise an error if the scan is not 2D or 3D.
        raise ValueError('Scan must be 2D or 3D and not ' + \
                        f'{disp_scan.ndim}D.')


def save(image: np.ndarray or animation.ArtistAnimation or \
        animation.FuncAnimation, full_path: str = None, 
        overwrite:bool=False, framerate: int = 10):
    """
    Saves an image or animation to the specified path. The save format 
    will be determined by the image type. If the image is a 2D array, 
    it will be saved as a png. If the image is an animation, it will be 
    saved as a gif.
    
    Parameters
    ----------
        image: numpy.ndarray or matplotlib.animation.ArtistAnimation or
                matplotlib.animation.FuncAnimation
            The image or animation to save.
        full_path: str, optional
            The full path to save the image or animation to. If None is 
            passed, the image or animation will be saved to the current 
            directory with a name of the form 'scan_#', where # is the 
            first number that is not already taken.
        overwrite: bool, optional
            If True, the image or animation will be overwritten if it 
            already exists. If False, the image or animation will not be 
            overwritten and a number will be appended to the end of the 
            file name.
        framerate: int, optional
            The framerate of the animation in frames per second. This
            parameter is only used if the image is an animation.
    """
    # Check the type of full_path and raise an error if it is not a 
    # string or None.
    if full_path is not None:
        if type(full_path) != str:
            raise TypeError('full_path must be a string or None and a '+
                                f'{type(full_path)} was passed')
    # Check the type of overwrite and raise an error if it is not a
    # boolean.
    if type(overwrite) != bool:
        raise TypeError('overwrite must be a boolean and a '+
                        f'{type(overwrite)} was passed')
    # Check the type of framerate and raise an error if it is not an
    # integer.
    try:
        fps = int(framerate)
    except:
        raise TypeError('framerate must be an integer and a '+
                        f'{type(framerate)} was passed')
    # Check if full_path was passed.
    if full_path is not None:
        # Get the file name from the full path.
        file_name = os.path.basename(full_path)
        # Get the file directory from the full path.
        file_dir = os.path.dirname(full_path)
        # Check if the file directory exists.
        if file_dir != '':
            if not os.path.exists(file_dir):
                # Raise an error if the file directory does not exist.
                raise ValueError(f'{file_dir} is not a valid directory')
        # Check if the file name is valid.
        sluggified_file_name = slug(file_name)
        if sluggified_file_name != file_name:
            # Print a warning if the file name is not valid.
            print( file_name +"  is is not a valid file name." + 
                    "It will be changed to: \n" + sluggified_file_name + 
                    '\n')
        # Create the save path.
        save_path = os.path.join(file_dir, sluggified_file_name)
    # if full_path was not passed.
    else:
        # Initialize the index.
        ind = 1
        # Create the save path.
        save_path = f'scan_{ind}'
        # Check if the save path already exists while incrementing the 
        # index until it does not already exist.
        while os.path.exists(save_path):
            ind += 1
            save_path = f'scan_{ind}'
    # Check the type of image and save it accordingly.
    if type(image) == np.ndarray:
        # Check if the image is 2D.
        if image.ndim == 2:
            png_path = save_path+'.png'
            # Check if the image already exists.
            if not overwrite:
                i = 1
                # Increment the index until the path does not already 
                # exist.
                while os.path.exists(png_path):
                    png_path = save_path+f'_{i}.png'
                    i += 1
                if png_path != save_path+'.png':
                    # Print a warning if the image already exists.
                    print(f'{save_path}.png already exists. It will be ' + \
                            f'saved as '+ f'{png_path}')
            # Save the image
            plt.imsave(png_path, image, cmap='gray', format='png')
        else:
            # Raise an error if the image is not 2D.
            raise ValueError('Only 2D images arrays or animations can be ' +
                                f'saved, and a {image.ndim}D array was passed')
    elif type(image) == animation.ArtistAnimation or \
            type(image) == animation.FuncAnimation:
        gif_path = save_path+'.gif'
        # Check if the animation path already exists.
        if not overwrite:
            i = 1
            # Increment the index until the path does not already exist.
            while os.path.exists(gif_path):
                gif_path = save_path+f'_{i}.gif'
                i += 1
            if gif_path != save_path+'.gif':
                # Print a warning if the animation already exists.
                print(f'{save_path}.gif already exists. It will be saved as '+
                        f'{gif_path}')
        # Save the animation
        image.save(gif_path, fps=fps)
    else:
        # Raise an error if the image is not a numpy array or animation.
        raise ValueError('Only 2D images arrays or animations can be' +
                                f'saved, and a {type(image)} was passed')


def load_example(single_image: bool = False):
    """ 
    Imports an example scan.

    Parameters
    ----------
        single_image: bool, optional
            If True, only a single image will be imported. If False, the
            entire scan will be imported.
    
    Returns
    -------
        scan: ct_analyser.cta.Scan
            An example scan.
    """
    # Get type of single_image
    if type(single_image) != bool:
        raise TypeError('single_image must be a boolean and a ' + 
                        f'{type(single_image)} was passed')
    # Get the path to the current file.
    path = os.path.dirname(os.path.abspath(__file__))
    # Check if a single image should be imported.
    if single_image:
        # Get the path to the example image.
        path = os.path.join(path, 'Data', 'Patients', 'Chest_CT', '1-32.dcm')
    else:
        # Get the path to the example scan.
        path = os.path.join(path, 'Data', 'Patients', 'Chest_CT')
    # Import the scan.
    scan = import_dicom(path)
    # Return the scan.
    return scan


class _Runnning():
    """ 
    Class to keep track of the status of the main loop.
    
    Attributes
    ----------
        running: bool
            The status of the main loop.
    """
    def __init__(self):
        """ Builds the class and sets running to true."""
        self.running = True

    def _set_false(self):
        """ Sets running to false."""
        self.running = False


class _Image():
    """
    Class to display the images.
    
    Attributes
    ----------
        image: numpy.ndarray
            The image to be displayed.
        current_image: int
            The index of the current image.
        num_images: int
            The number of images in the scan.
        WIN_SIZE: int
            The size of the window.
        array_size: tuple
            The size of the image.
        im_loc: list
            The location of the image.
        im_surface: pygame.Surface
            The surface of the image.
        rect: pygame.Rect
            A box that defines the image size and shape.
    """
    def __init__(self, images: np.ndarray, WIN_SIZE: int):
        """
        Builds the class.
        
        Parameters
        ----------
            images: numpy.ndarray
                The image to be displayed (can be 2D or 3D).
            WIN_SIZE: int
                The size of the window.
        """
        # Convert to 8 bit format.
        self.image = self._convert_to_8bit(images)
        # Set the current image to 0.
        self.current_image = 0
        #  check if the image is 3D or 2D and set the number of images.
        if images.ndim == 3:
            self.num_images = images.shape[0]
        else:
            self.num_images = 1
        # Define the window size.
        self.WIN_SIZE = WIN_SIZE
        # Get the size of the image.
        self.array_size = self._convert_RGB().shape
        # Get the location for the image and create a surface and 
        # rectangle.
        self.im_loc = [WIN_SIZE//2 - self.array_size[0]//2, 
                        WIN_SIZE//2 - self.array_size[1]//2]
        self.im_surface = pg.Surface((self.array_size[0], 
                                        self.array_size[1]))
        self.rect = pg.Rect((self.im_loc[0], self.im_loc[1]), 
                                (self.array_size[0], self.array_size[1]))

    def _get_image_num(self):
        """ Returns the index of the current image."""
        return self.current_image
    
    def _get_num_images(self):
        """ Returns the number of images in the scan."""
        return self.num_images

    def _get_image(self):
        """ Returns the current image array."""
        # Check if current image is out of range.
        if self.current_image >= self.num_images:
            # Raise error if out of range.
            raise ValueError("Index out of range.")
        else:
            # Check if image is 3D or 2D and return the image.
            if self.image.ndim == 3:
                image = self.image[self.current_image]
            else:
                image =  self.image
        return image

    def _convert_to_8bit (self, images: np.ndarray):
        """
        Converts the image (or list of images) to 8 bit format.
        
        Parameters
        ----------
            images: numpy.ndarray
                The image to be converted (can be 2D or 3D).
            
        Returns
        -------
            images: numpy.ndarray
                The image in 8 bit format.
        """
        # Find the minimum and maximum intensity throughout the whole 
        # scan.
        min_intensity = min(images.flatten())
        
        # Shift the intensity so that the minimum is 0.
        if min_intensity < 0.:
            images += abs(min_intensity)
            max_intensity = max(images.flatten())
        else:
            images -= min_intensity
            max_intensity = max(images.flatten())
        # Adjust the intensity so that the maximum is 255.
        images *= 255/max_intensity
        return images

    def _convert_RGB (self):
        """
        Converts the image to RGB format.
        
        Returns
        -------
            array: numpy.ndarray
                The image in RGB format (where all of the channels are the 
                same).
        """
        # Get the array to be displayed.
        array = self._get_image()
        # Convert array to 3D array (to fit into RGB format).
        array = np.array([array]*3).transpose()
        return array
        
    def _draw (self, win: pg.Surface):
        """
        Draws the image to the window.
        
        Parameters
        ----------
            win: pygame.Surface
                The window to draw the image to.
        """
        # get the array to be displayed.
        array = self._convert_RGB()
        # Blit the array to the surface.
        pg.surfarray.blit_array(self.im_surface, array)
        # Blit the surface to the window.
        win.blit(self.im_surface, self.im_loc)

    def _prev_image(self):
        """ Sets the current image index to the previous image."""
        # Check if the current image is the first image.
        if self.current_image > 0:
            # Set the current image to the previous image.
            self.current_image -= 1
        else:
            # Set the current image to the last image.
            self.current_image = self.num_images - 1

    def _next_image(self):
        """ Sets the current image index to the next image."""
        # Check if the current image is the last image.
        if self.current_image < self.num_images - 1:
            # Set the current image to the next image.
            self.current_image += 1
        else:
            # Set the current image to the first image.
            self.current_image = 0

    def _check_clicked(self, pos: tuple):
        """ Checks if the image has been clicked."""
        return self.rect.collidepoint(pos)
    
    def _is_selected(self, pos: tuple):
        """ 
        Returns the coordinates of the click relative to the 
        image.
        """
        return (pos[0] - self.im_loc[0], pos[1] - self.im_loc[1])


class _Circle_Annotation():
    """
    Class for drawing a circle on an image.
    
    Attributes
    ----------
        image: _Image
            The image to draw the circle on.
        center: tuple
            The center of the circle.
        radius: int
            The radius of the circle.
        draw_surface: pygame.Surface
            The surface to draw the circle on.
        im_loc: tuple
            The location of the image (top left corner).
        colour: tuple
            The colour of the circle.
        thickness: int
            The thickness of the circle.
        is_drawing: bool
            Whether the circle is being drawn.
    """
    def __init__(self, image: _Image, colour: tuple = (255, 0, 0)):
        """ 
        Builds the class and sets the image to be displayed.
        
        Parameters
        ----------
            image: _Image
                The image to draw the circle on.
            colour: tuple
                The colour of the circle.
        """
        # Set the image that is being displayed.
        self.image = image
        # Initialise the circle attributes.
        self.center = None
        self.radius = None
        # Set the surface to draw the circle on.
        self.draw_surface = image.im_surface
        # Set the image location.
        self.im_loc = self.image.im_loc
        # Set the colour and thickness of the circle.
        self.colour = colour
        self.thickness = 2
        # Initialise the drawing attribute.
        self.is_drawing = False

    def _set_centre(self, center: tuple):
        """ 
        Sets the center of the circle.
        
        Parameters
        ----------
            center: tuple
                The center of the circle.
        """
        self.center = center

    def _set_radius(self, radius: int):
        """ 
        Sets the radius of the circle.
        
        Parameters
        ----------
            radius: int
                The radius of the circle.
        """
        self.radius = radius

    def _find_radius(self, pos: tuple):
        """
        Finds the distance between the center of the circle and the 
        mouse.
        
        Parameters
        ----------
            pos: tuple
                The position of the mouse.
        
        Returns
        -------
            hypotenuse: int
                The distance between the center of the circle and the mouse.
        """
        # Check if the circle centre has been defined
        if self.center is not None:
            # Find the distance between the centre of the circle and 
            # the mouse.
            distance = np.array(self.center)- (np.array(pos))
            hypotenuse = np.linalg.norm(distance).astype(int)
            return hypotenuse

            

    def _draw(self, win: pg.Surface):
        """ 
        Draws the circle on the window.
        
        Parameters
        ----------
            win: pygame.Surface
                The window to draw the circle on.
        """
        # Check if the circle is being drawn.
        if self.center is not None and self.radius is not None:
            # Draw the circle on the surface.
            pg.draw.circle(self.draw_surface, self.colour, self.center, 
                                self.radius, self.thickness)
            # Blit the surface to the window.
            win.blit(self.draw_surface, self.im_loc)
    
    def _start_drawing(self):
        """ Sets the circle to be drawn."""
        self.is_drawing = True

    def _stop_drawing(self):
        """ Stops the circle from being drawn."""
        self.is_drawing = False

    def _clear_circle(self):
        """ Clears the circle attributes."""
        self.center = None
        self.radius = None
        self._stop_drawing()
    
    def _get_radius(self):
        """ Returns the radius of the circle."""
        return self.radius
    
    def _get_centre(self):
        """ Returns the center of the circle."""
        return self.center


class _Img_Coordinates():
    """
    Class for storing the coordinates of the selected region of the 
    image.
    
    Attributes
    ----------
        top_ind: int
            The index of the top image.
        bot_ind: int
            The index of the bottom image.
        coord: tuple
            The coordinates of the centre of the primary circle.
        coord2: tuple
            The coordinates of the centre of the secondary
        radius: int    
            The radius of the circle.
    """
    def __init__(self):
        """ Builds the class and sets all the coordinates to None."""
        self.top_ind = None
        self.bot_ind = None
        self.coord = None
        self.coord2 = None
        self.radius = None

    def _set_top_ind(self, top_ind: int):
        """ Sets the index of the top image."""
        self.top_ind = top_ind

    def _set_bot_ind(self, bot_ind: int):
        """ Sets the index of the bottom image."""
        self.bot_ind = bot_ind

    def _set_coord (self, coord: tuple):
        """ Sets the coordinates of the centre of the primary circle."""
        self.coord = coord
    
    def _set_coord2 (self, coord2: tuple):
        """ Sets the coordinates of the centre of the secondary circle."""
        self.coord2 = coord2

    def _set_radius (self, radius: int):
        """ Sets the radius of the circle."""
        self.radius = radius

    def _clear (self):
        """ Clears all the coordinates."""
        self.top_ind = None
        self.bot_ind = None
        self.coord = None
        self.radius = None

    def _clear_secondary (self):
        """ Clears the secondary coordinates."""
        self.coord2 = None

    def _is_complete (self):
        """ 
        Checks if all the coordinates have been set.
        
        Returns
        -------
        bool
            True if all the coordinates have been set, False otherwise.
        """
        if self.top_ind is None or self.bot_ind is None or \
                self.coord is None or self.radius is None:
            return False
        else:
            return True
        
    def _get_coord(self):
        """ 
        Returns a dictionary of the coordinates of the ROI(s)).
        
        Returns
        -------
            scan_coord: dict  
                A dictionary containing the coordinates of the ROI(s). 
                In the form:
                {
                "Index": np.array([top_ind, bot_ind]),
                "Primary ROI": np.array([coord]),
                "Secondary ROI": np.array([coord2]) or None,
                "Radius": radius
                } 
        """
        if self.coord2 is not None:
            scan_coord = {
                            "Index": np.array([self.top_ind, self.bot_ind]),
                            "Primary ROI": np.array(self.coord),
                            "Secondary ROI": np.array(self.coord2),
                            "Radius": self.radius
                            }
            
        else:
            scan_coord = {
                            "Index": np.array([self.top_ind, self.bot_ind]),
                            "Primary ROI": np.array(self.coord),
                            "Secondary ROI": None,
                            "Radius": self.radius
                        }
        return scan_coord


class _TextButton():
    """
    Class for creating a button with text.
    
    Attributes
    ----------
        text: str
            The text of the button.
        font: pygame.font.Font
            The font of the text.
        x: int
            The x coordinate of the top left corner of the button.
        y: int
            The y coordinate of the top left corner of the button.
        width: int
            The width of the button.
        height: int
            The height of the button.
        colour1: tuple
            The primary colour of the button.
        colour2: tuple
            The secondary colour of the button.
        colour: tuple
            The current colour of the button.
        rect: pygame.Rect
            The rectangle of the button.
        eventID: int
            The event ID of the button.
        selected: bool
            True if the button is selected, False otherwise.
    """

    def __init__(self, x: int, y: int, width: int, height: int, 
                 colour1: tuple, colour2: tuple, text: str, 
                 font: pg.font.Font, event_id: int):
        """
        Builds the class and sets the attributes.
        
        Parameters
        ----------
            x: int
                The x coordinate of the top left corner of the button.
            y: int
                The y coordinate of the top left corner of the button.
            width: int
                The width of the button.
            height: int
                The height of the button.
            colour1: tuple
                The primary colour of the button.
            colour2: tuple
                The secondary colour of the button.
            text: str
                The text of the button.
            font: pygame.font.Font
                The font of the text.
            event_id: int
                The event ID of the button.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour1 = colour1
        self.colour2 = colour2
        self.colour = colour1
        # Create the rectangle of the button.
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        # Assign the text and font.
        self.text = text
        self.font = font
        # Assign the event ID.
        self.eventID = event_id
        # Set the selected attribute to False.
        self.selected = False

    def _draw(self, win: pg.Surface):
        """
        Draws the button on the window.
        
        Parameters
        ----------
            win: pygame.Surface
                The window to draw the button on.
        """
        # Check if the button is selected and change the colour 
        # accordingly.
        if self.selected:
            self.colour = self.colour2
        else:
            self.colour = self.colour1
        # Draw the button.
        pg.draw.rect(win, self.colour, self.rect)
        # Draw the text on the button.
        text = self.font.render(self.text, True, (0, 0, 0))
        win.blit(text, (self.x + self.width//2 - text.get_width()//2, 
                        self.y + self.height//2 - text.get_height()//2))
    
    def _is_clicked(self):
        """ Posts the event of the button."""
        event = pg.event.Event(self.eventID)
        pg.event.post(event)
    
    def _check_click(self, pos: tuple):
        """
        Checks if the button has been clicked.
        
        Parameters
        ----------
            pos: tuple
                The position of the mouse click.
        
        Returns
        -------
            bool
                True if the button has been clicked, False otherwise.
        """
        return self.rect.collidepoint(pos)
    
    def _is_selected(self):
        """ Sets the selected attribute to True."""
        self.selected = True

    def _is_deselected(self):
        """ Sets the selected attribute to False."""
        self.selected = False        


class _Text():
    """
    Class for creating text.

    Attributes
    ----------
        text: str
            The text to be displayed.
        font: pygame.font.Font
            The font of the text.
        loc: dict
            A dictionary containing the location of the text in accordance 
            with pygame.Rect parameters. for example: {"center": (x, y)}
        text_rend: pygame.Surface
            The rendered text.
        text_rect: pygame.Rect
            A rectangle around the text.
    """
    def __init__(self,font: pg.font.Font, loc: dict, text: str=""):
        """
        Builds the class and sets the attributes.
        
        Parameters
        ----------
            font: pygame.font.Font
                The font of the text.
            loc: dict
                A dictionary containing the location of the text in 
                accordance with pygame.Rect parameters. for example: 
                {"center": (x, y)}
            text: str
                The text to be displayed.
        """
        # Assign the attributes.
        self.text = text
        self.font = font
        self.loc = loc
        # Render the text.
        self.text_rend = self.font.render(self.text, True, (0, 0, 0))
        # Get the rectangle of the text.
        self.text_rect = self.text_rend.get_rect(**self.loc)

    def _draw(self, win: pg.Surface):
        """
        Draws the text on the window.
        
        Parameters
        ----------
            win: pygame.Surface
                The window to draw the text on.
        """
        # Update the text render and rectangle.
        self.text_rend = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_rend.get_rect(**self.loc)
        # Draw the text.
        win.blit(self.text_rend, self.text_rect)

    def _get_width(self):
        """
        Returns the width of the text.
        
        Returns
        -------
            int
                The width of the text."""
        return self.text_rect.width

    def _update_text(self, text: str):
        """
        Updates the text attribute.
        
        Parameters
        ----------
            text: str
                The new text.
        """
        self.text = text


def _check_consecutiveness(num_list: list):
    """
    Checks if a list of numbers is consecutive and/or has repeats.
    
    Parameters
    ----------
        num_list: list
            A sorted list of numbers to be checked.
    
    Returns
    -------
        repeats: list
            A list of lists containing the indices of the repeats.
        non_consecutive: list
            A list of lists containing the indices of the 
            non-consecutive numbers. If one (or both) non-consecutive 
            numbers are also repeats, then the index will be of the 
            first occurrence of the repeat.
    """
    # get unique numbers in list.
    unique_num = np.unique(num_list)
    # find repeats
    repeats = []
    # cycle through each element of list and record the index for each 
    # occurrence.
    for i in range(len(unique_num)):
        indexes = []
        for j in range(len(num_list)):
            if unique_num[i] == num_list[j]:
                indexes.append(j)
        # if there is more than one index, then there is a repeat.
        if len(indexes) > 1:
            repeats.append(indexes)
    # find non-consecutive numbers (that are not repeats)
    non_consecutive = []
    # cycle through each element of the unique list and check if the 
    # next element is consecutive.
    for i in range(len(unique_num)-1):
        # if the next element is not consecutive, then record the 
        # indices of the two elements.
        if unique_num[i] != unique_num[i+1]-1:
            non_consecutive.append([num_list.index(unique_num[i]), 
                                        num_list.index(unique_num[i+1])])
    return repeats, non_consecutive


def _apply_mask(image: np.ndarray, mask: np.ndarray):
    """
    Applies a mask to an image.
    
    Parameters
    ----------
        image : numpy.ndarray
            The image (2D or 3D) to be masked.
        mask : numpy.ndarray
            Binary mask (of the same shape as image) to be applied to 
            the image.
    
    Returns
    -------
        masked_image : numpy.ndarray
            The masked image.
    """
    # Check that image is numpy array.
    if type(image) != np.ndarray:
        raise TypeError("Image must be a numpy array.")
    # Check that mask is numpy array.
    if type(mask) != np.ndarray:
        raise TypeError("Mask must be a numpy array.")
    
    # Check that the image and mask have the same shape.
    if image.shape != mask.shape:
        raise ValueError("Image and mask must have the same shape.")
    masked_image = image * mask
    # Set the background to the minimum value of the image.
    masked_image[mask == 0] = np.min(image)
    return masked_image


def _open_scan(scan: Scan or MaskedScan or np.ndarray,
              scroll: bool= True, title: str="Scan"):
    """
    Opens a pygame window displaying the scan or segment. the 'Start' 
    and 'Stop' buttons can be used to record the start and stop of a 
    region of interest in the scan. Clicking and dragging the mouse will 
    draw a circle on the image, defining the region of interest. Once 
    the region of interest has been defined (Start, Stop and drawing a 
    circle), the user can press the 'OK' button to return the 
    coordinates of the region of interest. The user can also press 
    'Clear' to clear the region of interest. When the first region of 
    interest has been defined, the user can define a secondary region of
    interest by right clicking and dragging the mouse. The radius of the
    secondary region of interest will be the same as the first. This 
    allows for drift correction.

    Parameters
    ----------
        scan: ct_analyser.cta.Scan or 
                ct_analyser.mask.MaskedScan or numpy.ndarray
            The scan or segment to be displayed (or the scan array as a 
            2D or 3D numpy array)
        scroll: bool, optional
            Whether to just scroll through the images or allow the user 
            to select ROIs. True limits the user to scrolling through 
            the images. False allows the user to select ROIs. The 
            default is True.
        title: str, optional
            The title of the window. The default is "Scan".

    Returns
    -------
        dict or None
            A dictionary containing the coordinates of the ROI(s). In 
            the form:
            {
            "Index": np.array([top frame index, bottom frame index]),
            "Primary ROI": np.array([x, y of the centre of the primary 
                                    ROI]),
            "Secondary ROI": np.array([x, y of the secondary ROI]), or 
                                None,
            "Radius": radius
            } 
            If scroll is True, returns None.
    """
    # Define colours
    WHITE = (255, 255, 255)
    LGRAY = (200, 200, 200)
    DGRAY = (100, 100, 100)
    # Define maximum frame rate
    FPS = 30
    # Get the scan array from either a Scan or MaskedScan object.
    if type(scan) == MaskedScan:
        scan_array = np.array(scan.masked_scan)
    elif type(scan) == Scan:
        scan_array = np.array(scan.scan)
    elif type(scan) == np.ndarray:
        if np.ndim(scan) == 2 or np.ndim(scan) == 3:
            scan_array = np.array(scan)
        else:
            raise TypeError("Scan must be a 2D or 3D numpy array not a " +
                            f"{np.ndim(scan)}D array.")
    # Check type of scroll.
    if type(scroll) != bool:
        raise TypeError("Scroll must be a boolean.")
    # Check type of title.
    if type(title) != str:
        raise TypeError("Title must be a string.")
    # Initialise pygame window.
    pg.init()
    # Check if the window is just for scrolling or should contain more
    # text and buttons.
    if not scroll:
        WIN_SIZE = _get_optimum_win_size(scan_array)
    else:
        WIN_SIZE = _get_optimum_win_size(scan_array, padding=80)
    # Define font.
    font = pg.font.SysFont('Arial', WIN_SIZE//25)
    # Create a window.
    win = pg.display.set_mode((WIN_SIZE, WIN_SIZE))
    # Set the title of the window.
    pg.display.set_caption(title)
    # Get file path
    file_path = os.path.dirname(os.path.abspath(__file__))
    # Set the icon of the window.
    pg.display.set_icon(pg.image.load(os.path.join( file_path, 'Assets', 
                                                    'icon.png')))
    # Create a clock object
    CLOCK = pg.time.Clock()
    # Current status of main loop.
    running = _Runnning()
    # Get the images.
    images = _Image(scan_array, WIN_SIZE)
    # Get the shape of the image.
    array_shape = images._get_image().shape
    # Get the location of the image in the form [y, x] of the top 
    # left corner.
    im_loc = [WIN_SIZE//2 - array_shape[0]//2, WIN_SIZE//2 - array_shape[1]//2]
    # Initialise the index text
    im_index_text = _Text(font, {'topright': (im_loc[0]+array_shape[0], 
                im_loc[1]+array_shape[1])},
                f'Image: {images._get_image_num()+1}/' + \
                            f'{images._get_num_images()}')
    # Check if the user wants to scroll through the images or select 
    # a region of interest.
    if not scroll:
        # Initialise the coordinates of the region of interest.
        coordinates = _Img_Coordinates()
        # Initialise user events.
        START = pg.USEREVENT + 1
        STOP = pg.USEREVENT + 2
        OK = pg.USEREVENT + 3
        CLEAR = pg.USEREVENT + 4
        # Initialise the buttons.
        btn_xloc = np.linspace(25, WIN_SIZE-25, 5)
        btn_w = np.diff(btn_xloc)[0]//1.2
        # Adjust the x locations of the buttons so that they are 
        # centred.
        btn_xloc = btn_xloc + (WIN_SIZE- btn_xloc[-1])//2
        # Define the height of the buttons.
        btn_h = 30
        # Create the buttons.
        start_button = _TextButton(btn_xloc[0],20, btn_w, btn_h, LGRAY, DGRAY,
                                'Start', font, START)
        stop_button = _TextButton(btn_xloc[1], 20, btn_w, btn_h, LGRAY, DGRAY,
                                'Stop',font, STOP)
        ok_button = _TextButton(btn_xloc[2],20, btn_w, btn_h, LGRAY, DGRAY, 
                                'Ok', font, OK)
        clear_button = _TextButton(btn_xloc[3], 20, btn_w, btn_h, LGRAY, DGRAY, 
                                'Clear', font, CLEAR)
        # Create a list of the buttons.
        buttons = [start_button, stop_button, ok_button, clear_button]
        #  Initialise the rest of the text.
        start_frame_text = _Text(font, {'topleft': (75, 75 + array_shape[1])},
                                    "Start Frame: ")
        stop_frame_text = _Text(font, {'topleft': 
                                            (75, 75 + array_shape[1] + 30)},
                                "Stop Frame: ")
        radius_text = _Text(font, 
                            {'topleft':
                                (75 + start_frame_text._get_width() + 50, 
                                75 + array_shape[1])},"Radius: ")
        loc_text = _Text(font, {'topleft': 
                                    (75 + stop_frame_text._get_width() + 50, 
                                    75 + array_shape[1] + 30)}, "Loc: ")
        # Create a list of the text.
        text = [im_index_text, start_frame_text, stop_frame_text, radius_text, 
                loc_text]
        # Initialise primary circle.
        circle = _Circle_Annotation(images)
        # Initialise secondary circle.
        circle2 = _Circle_Annotation(images, colour = (50, 50, 255))
        # Make list of circles.
        circles = [circle, circle2]

        # Main loop.
        while running.running:
            # Update clock.
            CLOCK.tick(FPS)
            # Update window.
            _update_win(win, images, text, scroll, buttons, circles, WHITE)
            pg.display.update()
            # Check for events.
            for event in pg.event.get():
                _check_event(event, running, images, text, scroll, buttons, 
                    circles, coordinates, START, STOP, OK, CLEAR)
    else:
        # Make list of text.
        text = [im_index_text]
        # Main loop.
        while running.running:
            # Update clock.
            CLOCK.tick(FPS)
            # Update window.
            _update_win(win, images, text, scroll, colour=WHITE)
            pg.display.update()
            # Check for events.
            for event in pg.event.get():
                _check_event(event, running, images, text, scroll)

    # Close pygame window.
    pg.display.quit()
    pg.quit()
    if not scroll:
        # Return the coordinates if they are complete.
        if coordinates._is_complete():
            return coordinates._get_coord()
    else:
        return None


def _update_win(window: pg.Surface, images: _Image,text: list, 
        scroll: bool=True, buttons: list=None, circles: list=None, 
        colour: tuple=(255, 255, 255)):
    """
    Updates the window with the new images and text.
    
    Parameters
    ----------
        window: pygame.Surface
            The window to be updated.
        images: _Image
            The images to be drawn.
        text: list of _Text
            The text to be drawn.
        scroll: bool, optional
            Whether to just scroll through the images or allow the user 
            to select ROIs. True limits the user to scrolling through 
            the images. False allows the user to select ROIs. The 
            default is True.
        buttons: list of _Button not needed if scroll is True
            The buttons to be drawn.
        circle: list of _Circle_Annotation not needed if scroll is True
            The circle to be drawn.
        colour: tuple, optional
            The colour of the background. The default is white 
            (255, 255, 255).
    """
    
    # Draw background.
    window.fill(colour)
    # Draw the image.
    images._draw(window)
    # Draw the text.
    for txt in text:
        txt._draw(window)
    if not scroll:
        # Draw the buttons.
        for button in buttons:
            button._draw(window)
        # Draw the circle.
        for circle in circles:
            circle._draw(window)


def _get_optimum_win_size(scan_array: np.ndarray, padding: int = 150):
    """
    Gets the optimum size of the window. The optimum size is the maximum 
    size of the scan plus padding, provided that the scan is not larger 
    than 90% of the screen. Otherwise an error is raised.

    Parameters
    ----------
        scan_array: numpy.ndarray
            The array of the scan.
        padding: int, optional
            The amount of padding to add to the scan. The default is 
            150.

    Returns
    -------
        WIN_SIZE: int
            The size of the window.
    """
    # Get the resolution of the monitor.
    info = pg.display.Info()
    resolution = np.array([info.current_h, info.current_w])
    # Get the size of the scan.
    scan_size = np.array(scan_array.shape[-2:])
    # Check that scan is not larger than the screen.
    if any(np.floor(resolution*0.9).astype(int) < scan_size+padding):
        # raise error if scan (plus padding) is larger than the screen.
        raise Exception('Scan is larger than the screen. Screen size: ' + 
                        f'{resolution} Scan size: {scan_size}. Increase ' +
                        'monitor resolution or decrease the scale in your '
                        'display settings.')
    else:
        # Set the size of (square) window to the maximum size of the 
        # scan plus padding.
        WIN_SIZE = max(np.array(scan_size))+padding
        return WIN_SIZE


def _check_event(event: pg.event, running: _Runnning, images: _Image, 
                text: list=None, scroll: bool=True, 
                buttons: list=None, circles: list=None, 
                coordinates: _Img_Coordinates=None, START = pg.USEREVENT+1,
                STOP = pg.USEREVENT+2, OK = pg.USEREVENT+3, 
                CLEAR = pg.USEREVENT+4):
    """
    Checks for events and performs the appropriate action.
    
    Parameters
    ----------
        event: pygame.event
            The event to be checked.
        running: ct_analyser.cta._Running
            The running object controlling the main loop.
        images: ct_analyser.cta._Image
            The images object of the images being displayed.
        scroll: bool, optional
            Whether to just scroll through the images or allow the user 
            to select ROIs. True limits the user to scrolling through 
            the images. False allows the user to select ROIs. The 
            default is True.
        text: list of ct_analyser.cta._Text, not required if 
                scroll is True
            The text objects to be updated.
        buttons: list of ct_analyser.cta._Button, not required 
                    if scroll is True
            The buttons to be updated.
        circles: list of _Circle_Annotation, not required if scroll is 
                    True
            The circles to be updated.
        coordinates: _Img_Coordinates, not required if scroll is True
            The coordinates object to be updated.
        START: int, optional
            The event number for the start button. The default is 
            pygame.USEREVENT+1.
        STOP: int, optional
            The event number for the stop button. The default is 
            pygame.USEREVENT+2.
        OK: int, optional
            The event number for the ok button. The default is 
            pygame.USEREVENT+3.
        CLEAR: int, optional
            The event number for the clear button. The default is 
            pygame.USEREVENT+4.
    """
    # Check for quit event.
    if event.type == pg.QUIT:
        # Set running to false to exit main loop.
        running._set_false()
    #  Check for scrolling event.
    elif event.type == pg.MOUSEWHEEL:
        # Check if scrolling up or down.
        if event.y < 0:
            # display next image.
            images._next_image()
            # Update the image number text.
            text[0]._update_text(f'Image: {images._get_image_num()+1}/' +\
                                    f'{images._get_num_images()}')
        elif event.y > 0:
            # display previous image.
            images._prev_image()
            # Update the image number text.
            text[0]._update_text(f'Image: {images._get_image_num()+1}/' + \
                                            f'{images._get_num_images()}')
    # Check to see if the window is not just a scroll-scan window.
    if not scroll:
        # Check for left mouse button down event.
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Get mouse coordinates.
                mouse_pos = pg.mouse.get_pos()
                # Check if mouse is over a button.
                for button in buttons:
                    if button._check_click(mouse_pos):
                        # Call the button selection function (changes 
                        # the colour of the button).
                        button._is_selected()
                    else:
                        # Reset the button selection.
                        button._is_deselected()
                # Check if mouse is over the image.
                if images._check_clicked(mouse_pos):
                    # Get the location of the mouse.
                    loc = images._is_selected(mouse_pos)
                    # Update the coordinates of the region of interest.
                    coordinates._set_coord(loc)
                    # Update the text.
                    text[4]._update_text(f'Loc: {loc}')
                    text[3]._update_text(f"Radius: 0")
                    # Start drawing the primary circle.
                    circles[0]._start_drawing()
                    # Set the centre of the primary circle.
                    circles[0]._set_centre(loc)
                    # Set the initial radius of the primary circle.
                    circles[0]._set_radius(1)
            # Check for the right mouse button being pressed.
            elif event.button == 3:
                # Get mouse coordinates.
                mouse_pos = pg.mouse.get_pos()
                # check if the primary circle exists.
                if circles[0]._get_radius() is not None:
                    # Check if mouse is over the image.
                    if images._check_clicked(mouse_pos):
                        # Get the location of the mouse.
                        loc = images._is_selected(mouse_pos)
                        # Start drawing the secondary circle.
                        circles[1]._start_drawing()
                        # Set the centre of the secondary circle.
                        circles[1]._set_centre(loc)
                        # Set the initial radius of the secondary circle.
                        circles[1]._set_radius(circles[0]._get_radius())
                        # Update the text.
                        text[4]._update_text('Loc: ' + \
                                            f'{circles[0]._get_centre},{loc}')
                        

        # Check for the left mouse button being held down and the 
        # primary circle is being drawn.
        elif pg.mouse.get_pressed()[0] and circles[0].is_drawing:
            # Get the radius of the circle.
            rad = circles[0]._find_radius(\
                                    images._is_selected(pg.mouse.get_pos()))
            # Set the radius of the circle.
            circles[0]._set_radius(rad)
            # Update the text.
            text[3]._update_text(f"Radius: {rad}")
        # Check for the right mouse button being held down and the 
        # secondary circle is being drawn.
        elif pg.mouse.get_pressed()[2] and circles[1].is_drawing:
            # Get the radius of the circle.
            circles[1]._set_centre(images._is_selected(pg.mouse.get_pos()))
            # Update the text.
            text[4]._update_text(f'Loc: {circles[0]._get_centre()},'+
                                f'{circles[1]._get_centre()}')
        
        # Check for the left mouse button being released.
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                # Get mouse coordinates.
                mouse_pos = pg.mouse.get_pos()
                # Check that a circle is not currently being drawn.
                if not circles[0].is_drawing:
                    for button in buttons:
                        # Reset the button selection.
                        button._is_deselected()
                        # Check if mouse is over a button.
                        if button._check_click(mouse_pos):
                            # Call the button's function.
                            button._is_clicked()
                # Check if the mouse is over the image.
                else:
                    # Get the radius of the circle.
                    rad = circles[0]._find_radius(images._is_selected(\
                                                        pg.mouse.get_pos()))
                    # Set the radius of the circle.
                    circles[0]._set_radius(rad)
                    # Stop drawing the circle.
                    circles[0]._stop_drawing()
                    # Update the text.
                    text[3]._update_text(f"Radius: {rad}")
                    text[4]._update_text(f'Loc: {circles[0]._get_centre()}')
                    # Update the coordinates of the region of interest.
                    coordinates._set_radius(rad)
                    # Clear the secondary circle.
                    circles[1]._clear_circle()
                    # Clear secondary circle coordinates.
                    coordinates._clear_secondary()

            # Check for the right mouse button being released.
            elif event.button == 3:
                # Get mouse coordinates.
                mouse_pos = pg.mouse.get_pos()
                # Check that the secondary circle is  currently being 
                # drawn.
                if  circles[1].is_drawing:
                    # Get the radius of the circle.
                    circles[1]._set_centre(images._is_selected(\
                                                    pg.mouse.get_pos()))
                    # Stop drawing the circle.
                    circles[1]._stop_drawing()
                    # Update the text.
                    text[4]._update_text(f'Loc: {circles[0]._get_centre()},'+
                        f'{circles[1]._get_centre()}')
                    # Update the coordinates of the region of interest.
                    coordinates._set_coord2(circles[1]._get_centre())
        # Check for the start button being clicked.
        elif event.type == START:
            # Update the text and set the top index of the region of 
            # interest.
            text[1]._update_text(f'Start Frame: {images._get_image_num()+1}')
            coordinates._set_top_ind(images._get_image_num())
        # Check for the stop button being clicked.
        elif event.type == STOP:
            # Update the text and set the bottom index of the region of 
            # interest.
            text[2]._update_text(f'Stop Frame: {images._get_image_num()+1}')
            coordinates._set_bot_ind(images._get_image_num())
        # Check for the clear button being clicked.
        elif event.type == CLEAR:
            # Update the text and clear the circles and coordinates.
            text[1]._update_text(f'Start Frame: ')
            text[2]._update_text(f'Stop Frame: ')
            text[3]._update_text(f'Radius: ')
            text[4]._update_text(f'Loc: ')
            coordinates._clear()
            for circle in circles:
                circle._clear_circle()
        # Check for the ok button being clicked.
        elif event.type == OK:
            # Check if the coordinates are complete.
            if coordinates._is_complete():
                # Set running to false to exit main loop.
                running._set_false()