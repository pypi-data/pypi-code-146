import pandas as pd
import numpy as np
import scipy.ndimage as nd
from skimage import segmentation, draw, measure
from matplotlib import animation, colors
import matplotlib.pyplot as plt
from ct_analyser.cta import Scan, _open_scan
from ct_analyser.mask import MaskedScan, median_filter, bimodal_threshold

class ContouredScan():
    """
    Class to store the information of object contours.
    
    Attributes
    ----------
        scan_obj: ct_analyser.cta.Scan
            The scan that the contour is from with all of the 
            associated information.
        contours: list
            A list of pandas DataFrames, each containing contour
            coordinates.
        scan: numpy.ndarray
            The original scan array before any processing.
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
        n_contours: list
            A list of the number of contours in each DataFrame of 
            contours.
    """

    def __init__(self, contours: pd.core.frame.DataFrame, 
                 scan: Scan):
        """
        Builds the class and sets the attributes.
        
        Parameters
        ----------
            contours: pandas.core.frame.DataFrame
                A DataFrame containing the coordinates of each contour.
            scan: ct_analyser.cta.Scan
                The scan that the contour is from with all of the 
                associated scan information.
        """
        self.scan_obj = scan
        self.contours = [contours]
        self.scan = scan.scan
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
        self.n_contours = [self.contours[0].columns.levshape[1]]

    def __repr__(self):
        """
        Returns a string representation of the class.
        
        Returns
        -------
            description: str
                A string representation of the class.
        """
        description = "Contoured_scan: \n"
        description +="_______________\n"
        description += f"Date: {self.date} \nTime: {self.time} \n"
        description += f"Patient: \n\tName: {self.patient_name} \n\tID: " + \
            f"{self.patient_id} \n\tBirth Date: {self.patient_birth_date} \n"
        description += f"Number of contours: {self.n_contours}\n"
        description += f"Scan ID: {self.scan_id} \n"
        return description
    
    def add_contours(self, contours: pd.core.frame.DataFrame or ContouredScan):
        """
        Adds a set of contours.
        
        Parameters
        ----------
            contours: pandas.core.frame.DataFrame or 
                    ct_analyser.segment.ContouredScan
                The DataFrame or contour class containing the contour 
                coordinates to be added.
        """
        if type(contours) == ContouredScan:
            contours = contours.contours
            for i in range(len(contours)):
                self.contours.append(contours[i])
                self.n_contours.append(contours[i].columns.levshape[1])
        elif type(contours) == pd.core.frame.DataFrame:
            self.contours.append(contours)
            self.n_contours.append(contours.columns.levshape[1])
        else:
            raise TypeError('Contours must be a pandas DataFrame or ' + \
                            'ct_analyser.segment.ContouredScan object.')

        
def contour(scan: np.ndarray or Scan or MaskedScan, filtered: bool=False, 
            median_filter_size: int=3 , slice_no: int=0):
    """
    Parameters
    ----------
        scan: numpy.ndarray, ct_analyser.cta.Scan or 
                ct_analyser.cta.MaskedScan
            A 2D or 3D image or class object.
        filtered: bool, optional
            Whether the image has been filtered or not. The default is 
            False.
        median_filter_size: int, optional
            The size of the median filter to be applied to the image if
            not already filtered.
        slice_no: int, optional
            The slice number in the scan if image is 2D (index of image 
            in the scan + 1).
            
    Returns
    -------
         df: pandas.core.frame.DataFrame
            A dataframe containing the contour coordinates within the 
            image. Only returned if image is a numpy.ndarray.
        cont_class: ct_analyser.segment.Contour
            A segment.ContouredScan object containing the contour 
            coordinates. Only returned if image is a cta.MaskedScan or
            cta.Scan.
    """
    # Check image is a numpy array, Scan or MaskedScan.
    if type(scan) == np.ndarray:
        image = scan
    elif type(scan) == MaskedScan:
        image = scan.masked_scan
    elif type(scan) == Scan:
        image = scan.scan
    else:
        raise TypeError('Scan must be a numpy array, ' + \
                        'ct_analyser.cta.Scan or ' + \
                        f'ct_analyser.cta.MaskedScan, not {type(image)}')
    # Check slice_no is an int.
    if type(slice_no) != int:
        raise TypeError(f'slice_no must be an int, not {type(slice_no)}')
    # Check median_filter_size is an int.
    if type(median_filter_size) != int:
        raise TypeError(f'median_filter_size must be an int, ' + \
                        f'not {type(median_filter_size)}')
    
    if not filtered:
        # Apply median filter.
        image = median_filter(image, median_filter_size)

    # Apply bimodal thresholding.
    image = bimodal_threshold(image)

    # List of all contours.
    conts_all = None
    
    # If image is 2D.
    if image.ndim == 2:
        if slice_no == 0:
            raise ValueError('slice_no must be specified for 2D images.')
        # Watershed image.
        # Create seeds.
        xm, ym = np.ogrid[0:image.shape[0]:int(image.shape[0]/8), 
                              0:image.shape[1]:int(image.shape[1]/8)]
        markers = np.zeros_like(image).astype(np.int16)
        markers[xm, ym] = np.arange(xm.size*ym.size).reshape((xm.size,
                                                              ym.size))
        # Implement watershedding.
        watershed = nd.watershed_ift(image.astype(np.uint8), markers)
        # Remove the seeds.
        watershed[xm, ym] = watershed[xm-1, ym-1] 
        # Label image.
        # Find most commonly occuring pixel value, the background.
        pixels, counts = np.unique(watershed, return_counts=True)
        background_val = pixels[counts.argmax()]
        # Label each segment.
        label_img = measure.label(watershed, background=background_val,
                                  return_num=True, connectivity = 2)
        
        # List of appropriately sized contours.
        contours = []
        # Contour each of the labelled sections.
        for i in range(label_img[1]):
            label_size = label_img[0] == i
            # Only contour large labelled segements.
            if label_size.sum() > 1000:
                # List of all contours within a section.
                section_contours = []
                # Find contours.
                pre_section_contours = measure.find_contours(label_img[0], 
                                                             level=i)
                # Remove small contours.
                for contour in pre_section_contours:
                    if contour.size > 25:
                        section_contours.append(contour)
                contours.append(section_contours)
                
        # Converting contours into a dataframe.
        # Unpacking.
        conts_im_unpack = []
        for conts in contours:
            conts_im_unpack.extend(conts)
        # Check if there are any contours.
        if len(conts_im_unpack) == 0:
            raise ValueError('No contours found.')
        # Make the dimensions of each contour array equal.
        # Find length of longest contour.
        longest = max(len(i) for i in conts_im_unpack)
        conts_all = None
        # Loop through each contour.
        for cont in conts_im_unpack:
            # Fill shorter arrays with NaN values to make arrays the 
            # same shape.
            if len(cont) < longest:
                diff = longest - len(cont)
                empties = np.empty((diff, 2))
                empties[:] = np.nan
                # Concatenate each contour array.
                if conts_all is None:
                    conts_all = np.append(cont, empties, axis = 0)
                else:
                    conts_all = np.concatenate(([conts_all, 
                        np.append(cont, empties, axis = 0)]), axis=1)
            # Don't extend the longest contour array.
            if len(cont) == longest:
                # Concatenate the contour array.
                if conts_all is None:
                    conts_all = cont
                else:
                    conts_all = np.concatenate(([conts_all, cont]), axis=1)
        # Define dataframe column titles.
        cont_label = []
        for i in range(int(len(conts_all.T)/2)):
            cont_label.extend([f'Contour {i+1}']*2)
        row_col_label = ['row', 'col'] * int(len(cont_label)/2)
        slice_label = [f'Slice {slice_no}'] * len(cont_label)
        # Create and add columns to dataframe.
        df = pd.DataFrame(conts_all.T)
        df['  '] = slice_label
        df[' '] = row_col_label
        df[''] = cont_label
        # Set multi indicies/
        df = df.set_index(['  ', '', ' ']).T
        # Create class instance if tyoe is MaskedScan.
        if type(scan) == MaskedScan:
            cont_class = ContouredScan(df, scan.scan_obj)
            return cont_class
        elif type(scan) == Scan:
            cont_class = ContouredScan(df, scan)
            return cont_class
        else:
            return df
             
    # If image is 3D.
    elif image.ndim == 3:
        # Watershed image.
        # Create seeds.
        xm, ym, zm = np.ogrid[0:image.shape[0]:1,
                              0:image.shape[1]:int(image.shape[1]/8), 
                              0:image.shape[2]:int(image.shape[2]/8)]
        markers = np.zeros_like(image).astype(np.int16)
        markers[xm, ym, zm] = np.arange(xm.size*ym.size*zm.size) \
                                .reshape((xm.size, ym.size,zm.size))
        # Implement watershedding.
        watershed = nd.watershed_ift(image.astype(np.uint8), markers)
        # Remove the seeds.
        watershed[xm, ym, zm] = watershed[xm-1, ym-1, zm-1] 
        # Label image.
        # Find most commonly occuring pixel value, the background.
        pixels, counts = np.unique(watershed, return_counts=True)
        background_val = pixels[counts.argmax()]
        # Label each segment.
        label_img = measure.label(watershed, background=background_val,
                                  return_num=True, connectivity = 3)
        
        # Contouring.
        # List of contuors for each slice in the CT.
        contours = []
        # Number of large labelled sections.
        # for each of the labelled sections
        for i in range(label_img[1] + 1):
            label_size = label_img[0] == i
            # Only contour large labelled segements.
            if label_size.sum() > 5000:
                # Loop through each slice.
                for j in range(len(label_img[0])):
                    # List of contours for this specific slice.
                    section_contours = []
                    # Find contours.
                    pre_section_contours = \
                        measure.find_contours(label_img[0][j], level=i)
                    # Remove small contours.
                    for contour in pre_section_contours:
                        if contour.size > 25:
                            section_contours.append(contour)
                    contours.append(section_contours)
                    
        # Converting contours into a dataframe.
        # Unpacked contours.
        conts_im_unpack_scan = []
        # Which slice in the CT each contour belongs to.
        slice_label = []
        for i in range(len(image)):
            cont_per_im = contours[i::len(image)]
            # Unpack.
            for cont in cont_per_im:
                conts_im_unpack_scan.extend(cont)
                # Add titles to list.
                slice_label.extend([f'Slice {i+1}'] * len(cont) * 2)
        # Check if there are any contours.
        if len(conts_im_unpack_scan) == 0:
            raise ValueError('No contours found.')
        # Find longest contour array.
        longest = max(len(i) for i in conts_im_unpack_scan)
        conts_all = None
        # Loop through unpacked contours.
        for cont in conts_im_unpack_scan:
            # Add NaN values to short contour arrays to ensure they all 
            # have the same dimensions.
            if len(cont) < longest:
                diff = longest - len(cont)
                empties = np.empty((diff, 2))
                empties[:] = np.nan
                # concatenate each contour array
                if conts_all is None:
                    conts_all = np.append(cont, empties, axis=0)
                else:
                    conts_all = np.concatenate(([conts_all, 
                                                 np.append(cont, empties, 
                                                           axis = 0)]), axis=1)
            # Keep the longest contour array at the same size.
            if len(cont) == longest:
                # Concatenate the longest array to the rest.
                if conts_all is None:
                    conts_all = cont
                else:
                    conts_all = np.concatenate(([conts_all, cont]), axis=1)
        # Define dataframe column titles.
        cont_label = []
        for i in range(int(len(slice_label)/2)):
            cont_label.extend([f'Contour {i+1}'] * 2)
        row_col_label = ['row', 'col'] * int(len(cont_label)/2)
        # Create and add columns to the dataframe.
        df = pd.DataFrame(conts_all.T)
        df['  '] = slice_label
        df[' '] = row_col_label
        df[''] = cont_label
        df = df.set_index(['  ', '', ' ']).T
        # Create class instance if type is MaskedScan.
        if type(scan) == MaskedScan:
            cont_class = ContouredScan(df, scan.scan_obj)
            return cont_class
        elif type(scan) == Scan:
            cont_class = ContouredScan(df, scan)
            return cont_class
        else:
            return df

    # If the image is not of the correct dimensions.
    else:
        raise TypeError(f'Image must be 2D or 3D, not {image.ndim}D.')

        
def heart_isolate(scan: np.ndarray or Scan or MaskedScan, 
                  heart_info_dict: dict or None=None, 
                  filtered: bool=False, alpha: int or float=5, 
                  beta: int or float=0.01, gamma: int or float=0.65, 
                  max_px_move: int or float=0.6):
    """
    Uses the information from heart_isolate popup to create a mask for 
    the heart by selecting the regions of interest (ROIs). This works 
    best with heavily filtered images (high size in the median_filter 
    function).
    
    Parameters
    ----------
        scan: numpy.ndarray or ct_analyser.cta.Scan or 
                ct_analyser.cta.MaskedScan
            The scan from which the heart is to be isolated. 
        heart_info_dict: dict or None, optional
            A dictionary containing the coordinates of the ROI(s). In 
            the form:
            {
            "Index": np.array([top frame index, bottom frame index]),
            "Primary ROI": np.array([x, y of the centre of the primary 
                                     ROI]),
            "Secondary ROI": np.array([x, y of the centre of the 
                                       secondary ROI]), or None
            "Radius": radius
            }
            If None, the user will be prompted to select the ROI(s) in 
            a popup.
        filtered: bool, optional
            Whether the input image has already been filtered. If False,
            a median filter will be applied to the image. The default is 
            False.
        alpha: int or float, optional
            Snake length shape parameter for heart isolation. Higher 
            values make more contracted estimates of the heart shape.
        beta: int or float, optional
            Snake smoothness shape parameter. Higher values makes snake 
            smoother.
        gamma: int or float, optional
            Explicit time stepping parameter for snake making.
        max_num_iter: int or float, optional
            Maximum pixel distance to move per iteration during snake 
            making.
            
    Returns
    -------
        mask: numpy.ndarray
            3D array indicating which pixels belong to the heart.
        df: pandas.core.frame.DataFrame or None
            Dataframe containing the contours of the heart. Only 
            returned if image is a numpy.ndarray.
        cont_class: ct_analyser.segment.Contour or None
            A contour class object containing the contour coordinates.
            Only returned if image is a ct_analyser.cta.MaskedScan or a 
            ct_analyser.cta.Scan object.
        heart_info: dict or None
            A dictionary containing the coordinates of the ROI(s) if a 
            dictionary is not provided. In the form:
            {
            "Index": np.array([top frame index, bottom frame index]),
            "Primary ROI": np.array([x, y of the centre of the primary
                                        ROI]),
            "Secondary ROI": np.array([x, y of the centre of the
                                        secondary ROI]), or None        
            "Radius": radius
            }
    """
    
   # Check image is a usable data type.
    if type(scan) != np.ndarray and type(scan) != Scan \
        and type(scan) != MaskedScan:
        raise TypeError('scan must be a numpy array, ' + \
            'ct_analyser.cta.Scan or ct_analyser.cta.MaskedScan, ' + \
            f'not {type(scan)}')

    # Check active_contour parameters are ints or floats.
    if type(alpha)!=int and type(alpha)!=float:
        raise TypeError('Any input alpha must be either an int or float, ' + \
                        f'not {type(alpha)}')
    if type(beta)!=int and type(beta)!=float:        
        raise TypeError('Any input beta must be either an int or float, ' +\
                        f'not {type(beta)}')    
    if type(gamma)!=int and type(gamma)!=float:        
        raise TypeError('Any input gamma must be either an int or float, ' +\
                        f'not {type(gamma)}')
    if type(max_px_move)!=int and type(max_px_move)!=float:
        raise TypeError('Any input max_px_move must be either an int or ' +\
                        f'float, not {type(max_px_move)}')
    # Convert scan to a numpy array if it is a Scan or MaskedScan.
    if type(scan) == Scan:
        image = scan.scan
    elif type(scan) == MaskedScan:
        image = scan.masked_scan
    else:
        image = scan

    # If heart_info is None, prompt user to select ROI(s).
    if heart_info_dict is None:
        heart_info = _open_scan(scan = image, scroll = False)
    else:
        heart_info = heart_info_dict
    # Filter image if not already filtered.
    if not filtered:
        print('Filtering....', end='\r')
        image = median_filter(image, 15)
        print('Filtering.... Done!')

    # Define variables from the dictionary.
    heart_start = min(heart_info["Index"])
    heart_end = max(heart_info["Index"])
    heart_mid_start = heart_info["Primary ROI"]
    radius = heart_info["Radius"]
    # If a secondary ROI is defined.
    if heart_info["Secondary ROI"] is not None:
        heart_mid_end = heart_info["Secondary ROI"]
        # Arrays of x and y coordinates of heart centres.
        heart_mid_x = np.linspace(heart_mid_start[0], 
                              heart_mid_end[0], 
                              heart_end-heart_start).astype('int')
        heart_mid_y = np.linspace(heart_mid_start[1], 
                                  heart_mid_end[1], 
                                  heart_end-heart_start).astype('int')
    else:
        if heart_start != heart_end:
            heart_mid_x = np.ones(heart_end-heart_start, 
                                dtype='int') * heart_mid_start[0]
            heart_mid_y = np.ones(heart_end-heart_start, 
                                dtype='int') * heart_mid_start[1]
        else:
            heart_mid_x = np.array([heart_mid_start[0]])
            heart_mid_y = np.array([heart_mid_start[1]])
    # Define the slices where the heart is present.
    if image.ndim == 3:
        # Crop to isolate slices with the heart present.
        heart_scan = image[heart_start:heart_end,:,:]
    elif image.ndim == 2:
        heart_scan = [image]
    else:
        raise ValueError("Image must be 2D or 3D.")
    
    # Finding contours.
    heart_conts = []
    all_masked = []
    # Loop through heart_scan.
    for i in range(len(heart_scan)):
       # Initialising circle.
        s = np.linspace(0, 2*np.pi, 400)
        y = heart_mid_y[i] + radius*np.sin(s)
        x = heart_mid_x[i] + radius*np.cos(s)
        init = np.array([y, x]).T
        snake = segmentation.active_contour(heart_scan[i], init, alpha=alpha,
                                            beta=beta, gamma=gamma, 
                                            max_px_move=max_px_move)
        heart_conts.append(snake)
        # Make mask.
        masked = np.zeros_like(heart_scan[i])
        rr, cc = draw.polygon(snake[:,0].astype('int'), 
                              snake[:,1].astype('int'), heart_scan[i].shape)
        masked[rr, cc] = 1
        all_masked.append(masked)
        print(f'Slice: {i+1} out of {len(heart_scan)}', end='\r')
    print('\n')
    # Reshape mask.
    mask = np.dstack(all_masked)
    mask = np.swapaxes(mask.T, 1, 2)

    # Making dataframe of contours.
    contours = None
    for cont in heart_conts:
        if contours is None:
            contours = cont
        else: 
            contours = np.concatenate(([contours, cont]), axis=1)
    contours = np.array(contours)
    # Make labels for multi-indexed dataframe.
    slice_label = []
    for i in range(int(len(contours.T)/2)):
        slice_label.extend([f'Slice {heart_start+i+1}']*2)
    cont_label = [[f'Contour {i+1}']*2 for i in range(int(len(slice_label)/2))]
    cont_label = [item for sublist in cont_label for item in sublist]
    row_col_label = ['row', 'col'] * int(len(slice_label)/2)
    # Creating dataframe.
    df = pd.DataFrame(contours.T)
    df['  '] = slice_label
    df[' '] = row_col_label
    df[''] = cont_label
    df = df.set_index(['  ', '', ' ']).T

    # Create class instance if type is MaskedScan.
    if type(scan) == MaskedScan:
        cont_class = ContouredScan(df, scan.scan_obj)
        if heart_info_dict is None:
            return mask, cont_class, heart_info
        else:
            return mask, cont_class
    elif type(scan) == Scan:
        cont_class = ContouredScan(df, scan)
        if heart_info_dict is None:
            return mask, cont_class, heart_info
        else:
            return mask, cont_class
    else:
        if heart_info_dict is None:
            return mask, df, heart_info 
        else:
            return mask, df
    

def lung_body_isolate(scan: Scan or MaskedScan, filtered: bool=False, 
                        median_filter_size: int=5, part: str='lungs', 
                        slice_no: int=0):
    """
    Isolates either the main body segment or the lungs.
    
    Parameters
    ----------
        scan: ct_analyser.cta.Scan or ct_analyser.cta.MaskedScan
            The scan from which the heart is to be isolated.
        filtered: bool, optional
            Whether the scan has been filtered or not. If False, a 
            median filter will be applied to the image. The default is 
            False.
        median_filter_size: int, optional
            The size of the median filter to be applied to the scan.
        part: str, optional
            Determines whether the 'lungs' or the 'body' are to be 
            isolated.
        slice_no: int, optional
            If ct_analyser.cta.Scan.scan or 
            ct_analyser.cta.MaskedScan.masked_scan is 2D, the slice 
            number in the sequence of images in the CT.
            
    Returns
    -------
        mask: numpy.ndarray
            3D array indicating which pixels belong to the desired body 
            part.
        df: pandas.core.frame.DataFrame or None
            Dataframe containing the contours of the desired body part.
            Only returned if image is a numpy.ndarray.
        cont_class: ct_analyser.segment.Contour or None
            A contour class object containing the contour coordinates.
            Only returned if image is a ct_analyser.cta.MaskedScan or a
            ct_analyser.cta.Scan object.
    """
    # Check image is a Scan or MaskedScan.
    if type(scan) == MaskedScan:
        if part == 'lungs':
            image = scan.masked_scan
        elif part == 'body':
            image = scan.mask
    elif type(scan) == Scan:
        image = scan.scan
    else:
        raise TypeError('Image must be ct_analyser.cta.Scan or ' +\
                        f'ct_analyser.cta.MaskedScan, not {type(scan)}')
    # Check plot_type is a correct input type. 
    if type(part) != str:
        raise TypeError(f'plot_type must be a string, not {type(part)}')
    if part != 'lungs' and part != 'body':
        raise ValueError('plot_type must be either "sliced" or "3D", not ' +\
                         f'{part}')
    # Check slice_no is an int.
    if type(slice_no)!=int:
        raise TypeError(f'slice_no must be an int, not {type(slice_no)}')
    # Check median_filter_size is an int.
    if type(median_filter_size)!=int:
        raise TypeError('median_filter_size must be an int, not ' +\
                        f'{type(median_filter_size)}')

    # Filter image if not already filtered.
    if filtered == False:
        image = median_filter(image, median_filter_size)

    # Apply bimodal thresholding to image.
    image = bimodal_threshold(image)
    
    # If image is 2D.
    if image.ndim == 2:
        # Watershed image.
        # Create seeds.
        xm, ym = np.ogrid[0:image.shape[0]:int(image.shape[0]/8), 
                              0:image.shape[1]:int(image.shape[1]/8)]
        markers = np.zeros_like(image).astype(np.int16)
        markers[xm, ym] = np.arange(xm.size*ym.size).reshape((xm.size,
                                                              ym.size))
        # Implement watershedding.
        watershed = nd.watershed_ift(image.astype(np.uint8), markers)
        # Remove the seeds.
        watershed[xm, ym] = watershed[xm-1, ym-1] 
        # Identify different watershed sections.
        unique_pixels = np.unique(watershed)
        for idx, val in enumerate(unique_pixels):
            # Make the background and small sections equal zero.
            if np.count_nonzero(watershed == val) < 300 or val==watershed[0,0]:
                unique_pixels[idx] = 0
        # Remove zero values.
        unique_pixels = [i for i in unique_pixels if i != 0]
        # Final list of contours.
        conts_to_plot = []
        # Initialise mask.
        all_masks = np.zeros(image.shape)
        
        # Loop through each unique section in the watershed.
        for section in unique_pixels:
            mask = (watershed==section)
            masked = mask * scan.scan[slice_no-1]
            # To find average pixel intensities of each section.
            masked[mask==0] = np.nan
            # Find average pixel intensity for that section.
            pixel_intensity = np.nanmean(masked)
            if part == 'lungs':
                # Threshold for air and lungs.
                if scan.threshold['Air'][0] <= pixel_intensity \
                    <=scan.threshold['Air'][1] or scan.threshold['Lung'][0] \
                    <= pixel_intensity <= scan.threshold['Lung'][1]:
                    # Add contours to list.
                    contour_section = measure.find_contours(mask, 
                                                        fully_connected='high')
                    conts_to_plot.append(contour_section)
                # Layer masks.
                all_masks = all_masks + mask
            if part == 'body':
                # Threshold for soft tissue.
                if scan.threshold['Soft Tissue'][0] <= pixel_intensity \
                    <=scan.threshold['Soft Tissue'][1]:
                    contour_section = measure.find_contours(mask,
                                                        fully_connected='high')
                    conts_to_plot.append(contour_section)
                    # Layer masks.
                    all_masks = all_masks + mask
        # Create binary mask.
        all_masks = all_masks > 0
        
        # Put contours into dataframe.
        conts_im_unpack = []
        for conts in conts_to_plot:
            conts_im_unpack.extend(conts)
        # Check if there are any contours.
        if len(conts_im_unpack) == 0:
            raise ValueError('No contours found.')
        # Make the dimensions of each contour array equal.
        # Find length of longest contour.
        longest = max(len(i) for i in conts_im_unpack)
        conts_all=None
        # Make contours equal lengths and add to the same dataframe.
        for cont in conts_im_unpack:
            if len(cont) < longest:
                diff = longest - len(cont)
                empties = np.empty((diff, 2))
                empties[:] = np.nan
                # Concatenate each contour array.
                if conts_all is None:
                    conts_all = np.append(cont, empties, axis = 0)
                else:
                    conts_all = np.concatenate(([conts_all, 
                                np.append(cont, empties, axis = 0)]), axis=1)
            # Don't extend the longest contour array.
            if len(cont) == longest:
                # Concatenate the contour array.
                if conts_all is None:
                    conts_all = cont
                else:
                    conts_all = np.concatenate(([conts_all, cont]), axis=1)
        # Define dataframe column titles.
        cont_label = []
        for i in range(int(len(conts_all.T)/2)):
            cont_label.extend([f'Contour {i+1}']*2)
        row_col_label = ['row', 'col'] * int(len(cont_label)/2)
        slice_label = [f'Slice {slice_no}'] * len(cont_label)
        # Create and add columns to dataframe.
        df = pd.DataFrame(conts_all.T)
        df['  '] = slice_label
        df[' '] = row_col_label
        df[''] = cont_label
        # Set multi indicies.
        df = df.set_index(['  ', '', ' ']).T
        # Create class instance if type is MaskedScan.
        if type(scan) == MaskedScan:
            cont_class = ContouredScan(df, scan.scan_obj)
            return all_masks, cont_class
        elif type(scan) == Scan:
            cont_class = ContouredScan(df, scan)
            return all_masks, cont_class
        else:
            return all_masks, df
    
    # For a 3D image.
    elif image.ndim == 3:
        # Watershed image.
        # Create seeds.
        xm, ym, zm = np.ogrid[0:image.shape[0]:1,
                              0:image.shape[1]:int(image.shape[1]/8), 
                              0:image.shape[2]:int(image.shape[2]/8)]
        markers = np.zeros_like(image).astype(np.int16)
        markers[xm, ym, zm] = np.arange(xm.size*ym.size*zm.size) \
                                .reshape((xm.size, ym.size, zm.size))
        # Implement watershedding.
        watershed = nd.watershed_ift(image.astype(np.uint8), markers)
        # Remove the seeds.
        watershed[xm, ym, zm] = watershed[xm-1, ym-1, zm-1] 
        # Identify different watershed sections.
        unique_pixels = np.unique(watershed)
        for idx, val in enumerate(unique_pixels):
            # Make the background and small sections equal zero.
            if np.count_nonzero(watershed == val) < 300 or \
             val==watershed[0,0,0]:
                unique_pixels[idx] = 0
        # Remove zero values.
        unique_pixels = [i for i in unique_pixels if i != 0]
        # Final list of contours.
        conts_to_plot = []
        # Initalise mask.
        all_masks = np.zeros(image.shape)

        # Loop though each slice in the scan.
        for i in range(len(image)):
            print(f'Slice {i+1} of {len(image)}', end='\r')
            for section in unique_pixels:
                # Isolate each unique section in the watershed.
                mask = (watershed[i] == section)
                masked = mask * scan.scan[i]
                masked[mask==0] = np.nan
                if np.all(np.isnan(masked)):
                    continue
                # Find average pixel intensity for that section.
                pixel_intensity = np.nanmean(masked)
                if part == 'lungs':
                    # Threshold for air and lungs.
                    if scan.threshold['Air'][0] <= pixel_intensity \
                    <=scan.threshold['Air'][1] or scan.threshold['Lung'][0] \
                    <= pixel_intensity <= scan.threshold['Lung'][1]:
                        contour_section = measure.find_contours(mask,
                                                     fully_connected='high')
                        conts_to_plot.append(contour_section)
                        # Layer masks.
                        all_masks[i] = all_masks[i] + mask
                if part == 'body':
                    # Threshold for soft tissue.
                    # if scan.threshold['Soft Tissue'][0] <= pixel_intensity \
                    #     <=scan.threshold['Soft Tissue'][1]:
                    contour_section = measure.find_contours(mask, 
                                                    fully_connected='high')
                    conts_to_plot.append(contour_section)
                    # Layer masks.
                    all_masks[i] = all_masks[i] + mask
        print('\n')
        all_masks = all_masks > 0
        
        # Put contours into dataframe.
        # Unpacked contours.
        conts_im_unpack_scan = []
        # Which slice in the CT each contour belongs to.
        slice_label = []
        for i in range(len(image)):
            cont_per_im = conts_to_plot[i::len(image)]
            # Unpack.
            for cont in cont_per_im:
                conts_im_unpack_scan.extend(cont)
                # Add titles to list.
                slice_label.extend([f'Slice {i+1}'] * len(cont) * 2)
        # Check if there are any contours.
        if len(conts_im_unpack_scan) == 0:
            raise ValueError('No contours found.')
        # Find longest contour array.
        longest = max(len(i) for i in conts_im_unpack_scan)
        conts_all = None
        # Loop through unpacked contours.
        for cont in conts_im_unpack_scan:
            # Add NaN values to short contour arrays to ensure they all 
            # have the same dimensions.
            if len(cont) < longest:
                diff = longest - len(cont)
                empties = np.empty((diff, 2))
                empties[:] = np.nan
                # Concatenate each contour array.
                if conts_all is None:
                    conts_all = np.append(cont, empties, axis=0)
                else:
                    conts_all = np.concatenate(([conts_all, 
                                np.append(cont, empties, axis = 0)]), axis=1)
            # Keep the longest contour array at the same size.
            if len(cont) == longest:
                # Concatenate the longest array to the rest.
                if conts_all is None:
                    conts_all = cont
                else:
                    conts_all = np.concatenate(([conts_all, cont]), axis=1)
        # Define dataframe column titles.
        cont_label = []
        for i in range(int(len(slice_label)/2)):
            cont_label.extend([f'Contour {i+1}'] * 2)
        row_col_label = ['row', 'col'] * int(len(cont_label)/2)
        # Create and add columns to the dataframe.
        df = pd.DataFrame(conts_all.T)
        df['  '] = slice_label
        df[' '] = row_col_label
        df[''] = cont_label
        df = df.set_index(['  ', '', ' ']).T
        # Create class instance if type is MaskedScan.
        if type(scan) == MaskedScan:
            cont_class = ContouredScan(df, scan.scan_obj)
            return all_masks, cont_class
        elif type(scan) == Scan:
            cont_class = ContouredScan(df, scan)
            return all_masks, cont_class
        else:
            return all_masks, df
        
        
def plot_contours(contourscan: ContouredScan or pd.core.frame.DataFrame, 
                  figsize: tuple or list=(5,5), plot_type='sliced', 
                  background: np.ndarray or Scan or MaskedScan or None=None, 
                  transparency:float or int=0.4, slice_no: int=0):
    """
    Plots the contours of a ContouredScan object.
    
    Parameters
    ----------
        contourscan: ct_analyser.segment.ContouredScan or 
                pandas.core.frame.DataFrame
            The scan with associated contours or a dataframe of 
            contours.
        figsize: tuple or list, optional
            The figure size.
        plot_type: str, optional
            The type of contour plot. 'sliced' will display each slice 
            of scan with the contours superimposed. '3D' returns a  
            rotating plot of the contours on a 3D axis. The default is 
            'sliced'.
        background: numpy.ndarray or ct_analyser.cta.Scan or 
                ct_analyser.cta.MaskedScan or None, optional
            The background on which the contours are plotted. If None 
            and contours is a ContouredScan object, the background will 
            be extracted from the class as the scan_obj attribute. If
            None and for other contour data types, an error will be 
            raised.
        transparency: float or int, optional
            The degree of transparency on lines plotted with '3D'.
        slice_no: int, optional
            The number of the slice in the scan to be displayed if the 
            contours are for a single slice (index of slice in the scan 
            + 1).
            
    Returns
    -------
        ani: matplotlib.animation.ArtistAnimation or 
                matplotlib.animation.FuncAnimation
            The displayed plot. 
    """
    # Check fig_size is a correct input type.
    if type(figsize) != tuple and type(figsize) != list:
        raise TypeError('figsize must be a tuple or list, not ' +\
                        f'{type(figsize)}')
    # Check plot_type is a correct input type. 
    if type(plot_type) != str:
        raise TypeError(f'plot_type must be a string, not {type(plot_type)}')
    if plot_type != 'sliced' and plot_type != '3D':
        raise ValueError('plot_type must be either "sliced" or "3D", not ' + \
                         f'{plot_type}')
    # Check transparency is a correct input type.
    if type(transparency) != float and type(transparency) != int:
        raise TypeError('transparency must be a float or int, not ' + \
                        f'{type(transparency)}')
    # Define contourscan and backgrond to be plotted and the background 
    # from input data type.
    if type(contourscan) == pd.core.frame.DataFrame:
        if background is None:
            raise ValueError('background must be provided if contours is ' +\
                              'a dataframe')
        elif type(background) == Scan:
            background = background.scan
            contours = contourscan
        elif type(background) == MaskedScan:
            background = background.masked_scan
            contours = contourscan
        elif type(background) == np.ndarray:
            background = background
            contours = contourscan
        else:
            raise TypeError('background must be a numpy array, a ' +\
                            'ct_analyser.cta.Scan object or a ' +\
                            'ct_analyser.maskMaskedScan object, not ' +\
                            f'{type(background)}')
    elif type(contourscan) == ContouredScan:
        contours = contourscan.contours
        if background is None:
            background = contourscan.scan_obj.scan
        elif type(background) == Scan:
            background = background.scan
        elif type(background) == MaskedScan:
            background = background.masked_scan
        elif type(background) == np.ndarray:
            background = background
        else:
            raise TypeError('background must be a numpy array, a ' +\
                            'ct_analyser.cta.Scan object or a ' +\
                            'ct_analyser.cta.MaskedScan object, not ' +\
                            f'{type(background)}')
    else:
        raise TypeError('contourscan must be a ' +\
                        'ct_analyser.segment.ContouredScan ' + \
                         f'object or a dataframe, not {type(contourscan)}')

    colour_list = list(colors.TABLEAU_COLORS)
                       
    # Making an animated object.
    if plot_type == 'sliced':
        # Find the maximum number of slices contours are present for.
        max_len = 0
        for cont in contours:
            if len(np.unique(cont.columns.get_level_values(0))) > max_len:
                max_len = len(np.unique(cont.columns.get_level_values(0)))

        if max_len == 1 and background.ndim != 2:
            raise ValueError('The contours are for a single slice, ' +\
                             'but the background is not 2D. Try ' +\
                             'changing the background.')

        fig, ax = plt.subplots(figsize=figsize)
        # Check colour list is long enough.
        if len(contours) > len(colour_list):
            multiplier = -(-len(contours)//len(colour_list))
            colour_list = colour_list * multiplier
        # Final list of images to be displayed.
        ims_contours = []

        if background.ndim == 2:
            if slice_no == 0:
                raise ValueError('slice_no must be provided if contours is ' +\
                                 'for a single slice')
            background = np.array([background])
            

        for i in range(background.shape[0]):
            # List of contours for a single slice of the scan.
            conts_plot_section = []
            for j in range(len(contours)):
                df = contours[j]
                slices = pd.unique(df.columns.get_level_values(0))
                # Determine which slices of the scan to plot.
                first = [int(x) for x in slices[0].split() if 
                            x.isdigit()][0]-1
                last = [int(x) for x in slices[-1].split() if 
                            x.isdigit()][0]-1
                # For multiple slices.
                if i >= first and i < last:
                    section = ax.imshow(background[i], cmap='gray')
                    # Extract and plot contours from the dataframe.
                    slice_name = slices[i-first]
                    sub_contours = np.unique(df[slice_name].
                                                columns.get_level_values(0))
                    for cont_name in sub_contours:
                        line_plot = ax.plot(df[slice_name][cont_name]['col'], 
                                            df[slice_name][cont_name]['row'], 
                                            c=colour_list[j], 
                                            linewidth=1.5)
                        conts_plot_section.append(line_plot)
                # For a single slice.
                elif first==last:
                    section = ax.imshow(background[i], cmap='gray')
                    slice_name = f'Slice {slice_no}'
                    sub_contours = np.unique(df.columns.get_level_values(1))
                    for cont_name in sub_contours:
                        line_plot = ax.plot(df[slice_name][cont_name]['col'], 
                                            df[slice_name][cont_name]['row'], 
                                            c=colour_list[j], 
                                            linewidth=1.5)
                        conts_plot_section.append(line_plot)
            to_plot = [section]
            for ind, val in enumerate(conts_plot_section):
                to_plot.append(val[0])
            ims_contours.append(to_plot)
        # Create animation.
        ani = animation.ArtistAnimation(fig, ims_contours, interval=100, 
                                        blit=True, repeat = True)
        plt.show()

        return ani

    if plot_type == '3D':
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        # Initialise plotting contour lines.
        def init():
            for j in range(len(contours)):
                df = contours[j]
                slices = pd.unique(df.columns.get_level_values(0))
                first = [int(x) for x in slices[0].split() if x.isdigit()][0]-1
                last = [int(x) for x in slices[-1].split() if x.isdigit()][0]-1
                ims = np.arange(first, last+1)
                for i in range(len(slices)):
                    slice_name = slices[i]
                    sub_contours = np.unique(df[slice_name].
                                                columns.get_level_values(0))
                    for cont_name in sub_contours:
                        ax.plot(df[slice_name][cont_name]['col'], 
                                df[slice_name][cont_name]['row'], 
                                ims[i],
                                c=colour_list[j], 
                                linewidth=3.5, alpha=0.5)
            return fig,
        ax.set_xlim([0, background.shape[1]])
        ax.set_ylim([0, background.shape[2]])
        ax.set_axis_off()
        ax.view_init(170, 0)
        # Animate to see plot from multiple angles.
        def animate(i):
            ax.view_init(elev=170, azim=i*60)
            return fig,
        ani = animation.FuncAnimation(fig, animate, init_func=init, 
                                       frames=6, interval=500, blit=True)
        plt.show()

        return ani