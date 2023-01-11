import numpy as np
import scipy.ndimage as nd
import matplotlib.pyplot as plt
from skimage import morphology, measure, filters
from matplotlib import animation, colors
from ct_analyser.cta import Scan, _open_scan, MaskedScan, _apply_mask


            
def median_filter(image: np.ndarray or Scan or MaskedScan, sz: int=3):
    """
    Applies a median filter to smooth image data while retaining clear 
    edges.
    
    Parameters
    ----------
        image: numpy.ndarray or ct_analyser.cta.Scan or 
                ct_analyser.cta.MaskedScan
            The image to be filtered.
        sz: int
            The size of the median filter.
            
    Returns
    -------
        filtered: numpy.ndarray or None
            The filtered image.
    """
    # Check size is an integer input.
    try:
        size = int(sz)
    except:
        raise ValueError('Size must be an integer value.')
    # Check image type.
    if type(image) == np.ndarray:
        image = image
    elif type(image) == Scan:
        image = image.scan
    elif type(image) == MaskedScan:
        image = image.masked_scan
    else:
        raise TypeError('Image must be a numpy array, ' + \
                        'ct_analyser.cta.Scan or ' + \
                        'ct_analyser.cta.MaskedScan')

    dims = image.ndim
    
    # If image is 2D.
    if dims == 2:
        try:
            # Filter the image.
            filtered = nd.median_filter(image, [size, size])
        except MemoryError:
            raise MemoryError('Not enough memory for filtering. Try ' + \
                                'reducing the value of size.')
            
    # If image is 3D.
    elif dims == 3:
        try:
            # Filter the image.
            filtered = nd.median_filter(image, [size, size, size])
        except MemoryError:
            raise MemoryError('Not enough memory for filtering. Try ' + \
                                'reducing the value of size.')
        
    # If the image has the wrong dimensions.
    else:
        raise ValueError('Image must be 2D or 3D.')

    return filtered


def bimodal_threshold(image: np.ndarray or Scan or MaskedScan, 
                        threshold: int or float=None, keep_higher: bool=True):
    """
    Binarises an image. If no threshold is input, this will done using 
    the Otsu method, assuming the image pixel intensities are bimodal.
    
    Parameters
    ----------
        image: numpy.ndarray, ct_analyser.cta.Scan or 
                ct_analyser.cta.MaskedScan
            The image (2D or 3D) to be filtered.
        threshold: int or float or None, optional
            The threshold by which to binarise the image.
        keep_higher: bool, optional
            If True, the values above the threshold will be set to 1.
            If False, the values below the threshold will be set to 1.
            
    Returns
    -------
        binarised: numpy.ndarray
            The binarised image (2D or 3D).
    """
    # Check image is a usable data type.
    if type(image) != np.ndarray and type(image) != Scan \
        and type(image) != MaskedScan:
        raise ValueError('Image must be a numpy array, ' + \
            'ct_analyser.cta.Scan or ct_analyser.cta.MaskedScan')
    # Check any input threshold is either a float.
    if threshold != None:
        try:
            thresh = float(threshold)
        except:
            raise TypeError('Threshold must be a float.')
    # Check keep_higher is a bool.
    if type(keep_higher) != bool:
        raise ValueError('keep_higher must be a bool')
    # Convert image to a numpy array if it is a Scan or MaskedScan.
    if type(image) == Scan:
        image = image.scan
    elif type(image) == MaskedScan:
        image = image.masked_scan
    
    # Set the Otsu threshold if none is given.
    if threshold == None:
        if type(image) == MaskedScan:
            mask = image.mask
            masked_im = image[np.where(mask==1)]
            thresh = filters.threshold_otsu(masked_im.ravel())
        else:
            thresh = filters.threshold_otsu(image.ravel())
    
    # Check which values to keep.
    if keep_higher:
        # Set values above the threshold to 1.
        binarised = image > thresh
    else:
        # Set values below the threshold to 1.
        binarised = image < thresh
    
    return binarised 


def histogram(scan: np.ndarray or Scan or MaskedScan, fig_size: tuple or 
                list=(5,5), plot_type: str='hist', cmap: str='plasma'):
    """
    Plots a histogram of pixel intensities in the given image. Uses the 
    Freedman Diaconis rule to find the optimal number of bins to use. 
    
    If a 2D image is input, a standard 2D histogram is returned. With a 
    3D image, a 3D histogram is returned by default. If plot_type is set
    to 'surf', a 3D surface plot is returned instead.
    
    Parameters
    ----------
        image: numpy.ndarray or ct_analyser.cta.Scan or 
                ct_analyser.cta.MaskedScan
            The image (2D or 3D) for which a histogram is to be plotted.
        fig_size: tuple or list 
            Desired size of the produced figure..
        plot_type: str
            Type of plot to be produced. Options are 'hist' for a 
            standard 3D histogram, and 'surf' for a 3D surface plot 
            (only applicable for 3D images).
        cmap: str
            Colourmap of plot (only applicable for 3D images with 
            plot_type 'surf')
            
    Returns
    -------
        ax: matplotlib.axes._subplots.AxesSubplot,
            matplotlib.axes._subplots.Axes3DSubplot
            Axes containing the plotted figure elements. 
    """
    # Check image type.
    if type(scan) == np.ndarray:
        image = scan
    elif type(scan) == Scan:
        image = scan.scan
    elif type(scan) == MaskedScan:
        image = scan.masked_scan
    else:
        raise ValueError('Input scan must be a numpy array, ' + \
                        'ct_analyser.cta.Scan or ' +\
                        'ct_analyser.cta.MaskedScan')
    # Check fig_size is a tuple or list of the correct size.
    if type(fig_size) != tuple and type(fig_size) != list:
        raise ValueError('Input fig_size must be a list or tuple of the ' + \
                        'figure width and height')
    elif len(fig_size) != 2:
        raise ValueError('Input fig_size must be of length 2')
    else:
        # Convert fig_size to a tuple of floats
        try:
            figsize = (float(fig_size[0]), float(fig_size[1]))
        except:
            raise ValueError('Input fig_size must be a list or tuple of ' + \
                            'floats')

    # Check cmap is a string.
    if type(cmap) != str:
        raise ValueError('Input cmap must be a string')

    # If image is 2D.
    if image.ndim == 2:
        # Only use the pixels that are not masked.
        if type(image) ==  MaskedScan:
            mask = scan.mask
            data = image[np.where (mask > 0)]
        else:
            data = image.ravel()
        # Finding optimal number of bins.
        bins, width = _find_optimal_bins(data)
        
        # PLotting histogram.
        fig, ax = plt.subplots(figsize=figsize)
        ax.hist(data, bins, width=width)
        ax.set_xlabel('Pixel intensity (Hounsfield Units)')
        ax.set_ylabel('Pixel frequency density')

        plt.show()
        
    # If image is 3D.
    elif image.ndim == 3:
        # Initialise a list of data to be plotted.
        to_plot = []
        # Loop throughe the list of images.
        for i in range(len(image)):
            # Only use the pixels that are not masked.
            if type(image) ==  MaskedScan:
                mask = scan.mask
                data = image[i][np.where (mask[i] > 0)]
            else:
                data = image[i].ravel()
            # Finding optimal number of bins.
            bins, width = _find_optimal_bins(data)
            # Extract histogram data.
            hist, bin_edges = np.histogram(data, bins=bins)
            # Add to list of data to be plotted.
            for j in range(len(hist)):
                to_plot.append([bin_edges[j], i, hist[j], width])
                
        to_plot = np.array(to_plot)
        fig = plt.figure(figsize=figsize)
        ax = plt.axes(projection='3d')
        
        if plot_type == 'surf':
            # Plot the 3D surface histogram.
            trisurf = ax.plot_trisurf(to_plot[:,0], to_plot[:,1], to_plot[:,2], 
                                    cmap=cmap)
        if plot_type == 'hist':
            # Plot the 3D bar histogram.
            x, y = np.meshgrid(to_plot[:,0].astype(np.float32), 
                               to_plot[:,1].astype(np.float32), 
                               copy=False, sparse=True) 
            x_flat, y_flat = x.ravel(), y.ravel()
            z = np.zeros_like(x).ravel()
            bar = ax.bar3d(x_flat, y_flat, z, to_plot[:,3], 1, to_plot[:,2], 
                           shade=True)
        ax.set_xlabel('Pixel intensity (Hounsfield Units)')
        ax.set_ylabel('Slice in scan')
        ax.set_zlabel('Pixel frequency density')

        plt.show()
    # If the image is not of the correct dimensions.
    else:
        raise ValueError('Scan must be 2D or 3D')  

    return ax


def isolate_pt(scan: Scan, morph_rad: int=3,
                med_filter: bool=True, med_filt_sz: int=3):
    """
    Isolates the patient from the image by thresholding to remove air 
    and then creating a mask.

    Parameters
    ----------
        image: ct_analyser.cta.Scan
            The scan to be filtered.    
        morph_rad: int, optional
            The radius of the morphological operations as a positive 
            integer.
        med_filter: bool, optional
            Whether or not to apply a median filter to the mask.
        med_filt_sz: int, optional
            The size of the median filter as a positive integer.
        
    Returns
    -------
        pt_mask: ct_analyser.cta.MaskedScan
            The masked scan with the patient isolated.
    """
    # Check the type of the scan.
    if type(scan) != Scan:
        raise TypeError("The scan must be of type " + \
                        "ct_analyser.cta.Scan" + \
                        f"not  {str(type(scan))}")
    # Check the type of the morph_rad.
    try:
        morphological_radius = int(morph_rad)
    except:
        raise TypeError("The morph_rad must be of type int not " +
                        str(type(morph_rad)))
    # Check the type of the med_filter.
    if type(med_filter) != bool:
        raise TypeError("The med_filter must be of type bool not " +
                        str(type(med_filter)))
    # Check the type of the median_filter_size.
    try:
        median_filter_size = int(med_filt_sz)
    except:
        raise TypeError("The med_filt_sz must be of type int not " +
                        str(type(med_filt_sz)))
    # Check the value of the morphological_radius.
    if morphological_radius <= 0:
        raise ValueError("The morphological_radius must be greater than 0 not " 
                        + str(morphological_radius))
    images = np.array(scan.scan)
    mask = np.zeros_like(images)
    # Check dimensions of image.
    if images.ndim == 2:
        air_threshold = scan.threshold['Air']
        # Define thresholds.
        air_mask = ~np.logical_and(images > air_threshold[0], \
                                    images < air_threshold[1])
        # Morphological operations.
        diamond = morphology.diamond(morphological_radius)
        air_mask_morph = morphology.opening(air_mask, diamond)
        air_mask_morph = morphology.closing(air_mask_morph, diamond)
        # Label regions with unique numbers.
        labels = measure.label(air_mask_morph.astype(int))
        regions = measure.regionprops(labels)
        # Find largest region.
        largest_region = max(regions, key=lambda x: x.area)
        # Create mask of largest region.
        isolated_patient = np.zeros_like(images)
        isolated_patient[tuple(largest_region.coords.T)] = 1
        # Fill in holes.
        isolated_patient = nd.binary_fill_holes(isolated_patient)
        mask = isolated_patient

    elif images.ndim == 3:
        for i in range(images.shape[0]):
            image = images[i]
            air_threshold = scan.threshold['Air']
            # Define thresholds.
            air_mask = ~np.logical_and(image > air_threshold[0], \
                                        image < air_threshold[1])
            # Morphological operations.
            diamond = morphology.diamond(morphological_radius)
            air_mask_morph = morphology.opening(air_mask, diamond)
            air_mask_morph = morphology.closing(air_mask_morph, diamond)
            # Label regions with unique numbers.
            labels = measure.label(air_mask_morph.astype(int))
            regions = measure.regionprops(labels)
            # Find largest region.
            largest_region = max(regions, key=lambda x: x.area)
            # Create mask of largest region.
            isolated_patient = np.zeros_like(image)
            isolated_patient[tuple(largest_region.coords.T)] = 1
            isolated_patient_filled = nd.binary_fill_holes(isolated_patient)
            mask[i] = isolated_patient_filled
    else:
        raise ValueError('Scan must be 2D or 3D')

    # Check if the median filter should be applied and apply it if it 
    # should.
    if med_filter:
        mask = median_filter(mask, median_filter_size)
    # Create the segment object with the mask.
    seg = MaskedScan(mask, scan)

    return seg


def mask_threshold(scan: Scan or MaskedScan,
                    threshold_key: str):
    """
    Mask the scan with a threshold value.
    
    Parameters
    ----------
        scan: ct_analyser.cta.Scan or ct_analyser.cta.MaskedScan
            An object containing the scan to be masked.
        threshold_key: str
            The key in the threshold dictionary within the cta.Scan.scan
            or cta.MaskedScan.masked_scan object for the tissue type to 
            be masked.

    Returns
    -------
        mask: numpy.ndarray
            A Boolean array of the same shape as the scan with True
            values where the desired tissue type exists. 
    """
    # Check the threshold key is a string.
    if type(threshold_key) != str:
        raise TypeError('Threshold key must be a string not a ' + \
                            f'{type(threshold_key)}.')
    if threshold_key in scan.threshold:
        # Get the threshold value.
        threshold = scan.threshold[threshold_key]
    else:
        raise ValueError('Threshold key not found in scan.')
    
    # Get the scan data.
    if type(scan) == Scan:
        scan_array = scan.scan
    elif type(scan) == MaskedScan:
        scan_array = scan.masked_scan
    else:
        raise TypeError('Scan must be a ct_analyser.cta.Scan or a ' +\
                        f'ct_analyser.cta.MaskedScan object not a ' + \
                        f'{type(scan)}')
    
    # Create a mask.
    mask = np.zeros_like(scan_array)
    # If the scan is 2D.
    if np.ndim(scan_array) == 2:
        # Mask the scan.
        mask = np.logical_and(scan_array >= threshold[0], 
                                scan_array <= threshold[1])
    # If the scan is 3D
    elif np.ndim(scan_array) == 3:
        # Cycle through the slices
        for i in range(scan_array.shape[0]):
            # Mask the scan
            mask[i,:,:] = np.logical_and(scan_array[i,:,:] >= threshold[0],
                                           scan_array[i,:,:] <= threshold[1])
    else:
        raise ValueError('Scan must be 2D or 3D.')
    
    return mask


def preview(scan: np.ndarray or Scan or MaskedScan, mask: np.ndarray, 
                    disp_type: str = 'gif', fig_size: tuple or list=(5,5), 
                    interval_time=50, normalize: bool = True):
    """
    Displays an animation of the masked scan (or displays a static image 
    if the scan is 2D).
    
    Parameters
    ----------
        scan: numpy.ndarray or ct_analyser.cta.Scan or 
                ct_analyser.cta.MaskedScan
            2D or 3D array of the scan or a Scan object or a MaskedScan 
            object. If a MaskedScan object is passed, the masked scan 
            will be displayed (not the original scan).
        mask: numpy.ndarray
            Binary mask (of the same shape as scan) to be applied to the
            scan.
        disp_type: str, optional
            The type of animation to create (either 'gif' or 'scroll').
        fig_size: tuple or list, optional
            The size of the figure.
        interval_time: int, optional
            The interval between frames in milliseconds.
        normalize: bool, optional
            Whether to normalize the scans being shown. If disp_type is
            'gif'. The default is True.
        
    Returns
    -------
        ani: matplotlib.animation.ArtistAnimation or None
            The animation of the masked scan (or None if the scan is 2D 
            or is disp_type was 'scroll').
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
    # Check the type of mask.
    if type(mask) != np.ndarray:
        # Raise an error if the type of mask is invalid.
        raise TypeError('Mask must be a numpy array and not a '+
                        f'{type(mask)}.')
    # Check the type of disp_type.
    if type(disp_type) != str:
        # Raise an error if the type of disp_type is invalid.
        raise TypeError('disp_type must be a string and not a '+
                        f'{type(disp_type)}.')
    # Check fig_size is a tuple or list of the correct size.
    if type(fig_size) != tuple and type(fig_size) != list:
        raise ValueError('Input fig_size must be a list or tuple of the ' + \
                        'figure width and height')
    elif len(fig_size) != 2:
        raise ValueError('Input fig_size must be of length 2')
    else:
        # Convert fig_size to a tuple of floats
        try:
            figsize = (float(fig_size[0]), float(fig_size[1]))
        except:
            raise ValueError('Input fig_size must be a list or tuple of ' + \
                            'floats')
    # Check the type of interval.
    try:
        interval = int(interval_time)
    except:
        raise TypeError('interval_time must be an int and not a ' + \
                        f'{type(interval_time)}.')
    # Check the value of interval.
    if interval < 0:
        raise ValueError('interval must be positive.')
    # Check the type of normalize.
    if type(normalize) != bool:
        raise TypeError('normalize must be a boolean and not a '+
                        f'{type(normalize)}.')

    masked_scan = _apply_mask(disp_scan, mask)

    # Create the figure and axes.
    fig, axs = plt.subplots(1, 2, figsize=figsize)
    # Remove the axes
    axs[0].axis('off')
    axs[1].axis('off')
    # Check if the scan is 2D or 3D.
    if disp_scan.ndim == 2:
        # Display the scan.
        axs[0].imshow(disp_scan, cmap='gray')
        # Set title.
        axs[0].set_title('Original Image')
        # Display the masked scan.
        axs[1].imshow(masked_scan, cmap='gray')
        # Set title.
        axs[1].set_title('Masked Image')

    elif disp_scan.ndim == 3:
        if disp_type == 'gif':
            # Initialize the frames.
            frames = []
            if normalize:
                # Create a normalize object.
                normalize = colors.Normalize(vmin=np.min(disp_scan),
                                            vmax=np.max(disp_scan))
                                            
            # Loop through the frames.
            for i in range(disp_scan.shape[0]):
                # set title
                axs[0].set_title('Original Scan')
                axs[1].set_title('Masked Scan')
                if normalize:
                    # Create and append the frame.
                    frame1 = axs[0].imshow(disp_scan[i], cmap='gray', 
                                            animated=True, norm=normalize)
                    frame2 = axs[1].imshow(masked_scan[i], cmap='gray', 
                                            animated=True, norm=normalize)
                else:
                    # Create and append the frame.
                    frame1 = axs[0].imshow(disp_scan[i], cmap='gray', 
                                            animated=True)
                    frame2 = axs[1].imshow(masked_scan[i], cmap='gray', 
                                            animated=True)
                frames.append([frame1, frame2])
            # Create the animation.
            ani = animation.ArtistAnimation(fig, frames, interval=interval,
                                            blit=True)
            # Show and return the animation as a gif.
            plt.show()
            return ani
        elif disp_type == 'scroll':
            plt.close()
            # Show the animation as a scrollable image.
            _open_scan(masked_scan, True)
        else:
            # Raise an error if the type of disp_type is invalid.
            raise ValueError('disp_type must be "gif" or "scroll" and not '+
                             f'{disp_type}.')
    else:
        # Raise an error if the scan is not 2D or 3D.
        raise ValueError('Scan must be 2D or 3D and not '+
                         f'{disp_scan.ndim}D.')


def invert(mask: np.ndarray):
    """
    Invert a mask.

    Parameters
    ----------
        mask: numpy.ndarray
            The Boolean mask to invert.

    Returns
    -------
        inv_mask: numpy.ndarray
            The inverted mask.
    """
    # Check the type of mask.
    if type(mask) != np.ndarray:
        # Raise an error if the type of mask is invalid.
        raise TypeError('Mask must be a numpy array and not a '+
                        f'{type(mask)}.')
    # Check mask can be changed to boolean
    try:
        bool_mask = mask.astype(bool)
    except:
        # Raise an error if the mask cannot be changed to boolean.
        raise ValueError('Mask cannot be changed to boolean.')
    # Invert the mask.
    inv_mask = np.invert(bool_mask)
    # Return the inverted mask.
    return inv_mask


def analyse(masked_scan: MaskedScan):
    """
    Analyses the mak of a MaskedScan object and returns a dictionary 
    containing the results.
    
    Parameters
    ----------
        masked_scan: ct_analyser.cta.MaskedScan
            The MaskedScan object to analyse.
    
    Returns
    -------
        mask_atr: dict
            A dictionary containing the results of the analysis 
            including the patient ID, patient name, patient birth date, 
            date, time, volume, dimensions, pixel intensity information 
            and percentage of each tissue in the mask. It is in the 
            form:
            {
            'Patient ID': patient_id (str),
            'Patient Name': patient_name (str),
            'Patient Birth Date': patient_birth_date (str),
            'Date': date (str),
            'Time': time (str),
            'Volume': volume (float, in mm^3),
            'Dimensions': dimensions (dict with keys 'x', 'y' and 'z' 
                                        and values as floats in mm),
            'Pixel Intensity Info': pixel_info (dict with keys 'Maximum 
                                    Pixel Intensity', 'Minimum Pixel 
                                    Intensity', 'Mean Pixel Intensity', 
                                    'Median Pixel Intensity' and 
                                    'Standard Deviation of Pixel 
                                    Intensities' and values as floats),
            'Percentage Tissue': perc_tissue (dict with keys from the 
                                MaskedScan object's threshold attribute,
                                default is 'Air', 'Lung', 'Fat', 
                                'Fluid', 'Soft Tissue', 'Bone' and
                                'Foreign Object' and values as floats 
                                indicating the percentage of each tissue
                                in the mask).
            }
        """
    # Check the type of the masked_scan
    if type(masked_scan) != MaskedScan:
        raise TypeError("The masked_scan must be of type MaskedScan not " + 
                        str(type(masked_scan)))
    # Get all attributes of the masked_scan.
    volume = _find_volume(masked_scan)
    dimensions = _find_dimensions(masked_scan)
    pixel_info = _get_pixel_info(masked_scan)
    perc_tissue = _find_perc_tissue(masked_scan)
    # Create a dictionary to store the results.
    mask_atr = {
                'Patient ID': masked_scan.patient_id,
                'Patient Name': masked_scan.patient_name,
                'Patient Birth Date': masked_scan.patient_birth_date,
                'Date': masked_scan.date,
                'Time': masked_scan.time,
                'Volume': volume,
                'Dimensions': dimensions,
                'Pixel Intensity Info': pixel_info,
                'Percentage Tissue': perc_tissue
                }
    return mask_atr


def _find_optimal_bins(data: np.ndarray or list):
    """
    Finds the optimal number of bins to use to plot a histogram 
    using the general equation to the Freedman Diaconis rule. First 
    the ideal bin width is found, which is then used to divide by 
    the data range.
    
        Parameters
        ----------
        data: numpy.ndarray or list
            The data to be plotted in the histogram in a 1D array or 
            list.
            
        Returns
        -------
        bins: int
            The optimal number of bins.
    """
    # Finding values.
    iqr = np.subtract(*np.percentile(data, [75, 25]))
    n = len(data)
    # Solving general equation.
    width = 2*iqr/n**(1/3)
    # finding number of bins
    bins = int((max(data)-min(data)) / width) + 1
    return bins, width


def _find_volume (masked_scan: MaskedScan):
    """
    Finds the volume of a MaskedScan object.
    
    Parameters
    ----------
        masked_scan: ct_analyser.cta.MaskedScan
            The MaskedScan object to find the volume of.
            
    Returns
    -------
        volume: float
            The volume of the MaskedScan object.
    """
    # Get pixel size and slice thickness.
    pixel_size = masked_scan.pixel_size
    slice_thickness = masked_scan.slice_thickness
    # Get the number of pixels.
    num_pixels = np.sum(masked_scan.mask)
    # Calculate the volume.
    volume = num_pixels * pixel_size[0] * pixel_size[1] * slice_thickness
    # Return the volume.
    return volume


def _find_dimensions(seg: MaskedScan):
    """
    Finds the dimensions of the mask.
    
    Parameters
    ----------
        seg: ct_analyser.cta.MaskedScan
            The MaskedScan object to find the dimensions of.
    
    Returns
    -------
        dimensions: dict
            A dictionary containing the dimensions of the mask in the 
            form: {dimension: value}.
    """
    mask_loc = np.where(seg.mask != 0)
    # Get pixel size and slice thickness.
    pixel_size = seg.pixel_size
    slice_thickness = seg.slice_thickness
    # Check the dimensions of the mask.
    if np.ndim(seg.mask) == 2:
        # The mask is 2D.
        max_x = np.max(mask_loc[1])
        min_x = np.min(mask_loc[1])
        x_dim = (max_x - min_x) * pixel_size[0]
        max_y = np.max(mask_loc[0])
        min_y = np.min(mask_loc[0])
        y_dim = (max_y - min_y) * pixel_size[1]
        z_dim = slice_thickness
    elif np.ndim(seg.mask) == 3:
        # find the maximum and minimum x, y and z values.
        max_x = np.max(mask_loc[2])
        min_x = np.min(mask_loc[2])
        x_dim = (max_x - min_x) * pixel_size[0]
        max_y = np.max(mask_loc[1])
        min_y = np.min(mask_loc[1])
        y_dim = (max_y - min_y) * pixel_size[1]
        max_z = np.max(mask_loc[0])
        min_z = np.min(mask_loc[0])
        z_dim = (max_z - min_z) * slice_thickness
    else:
        raise ValueError("Mask must be 2D or 3D.")
    # Find the dimensions of the mask.
    dimensions = {
        'x': x_dim,
        'y': y_dim,
        'z': z_dim
    }
    return dimensions


def _get_pixel_info(seg: MaskedScan):
    """
    Finds the maximum, minimum, mean, median and standard deviation of 
    the pixel intensities within the mask.

    Parameters
    ----------
        seg: ct_analyser.cta.MaskedScan
            The MaskedScan object to find the pixel information of.

    Returns
    -------
        pixel_info: dict
            A dictionary containing the maximum, minimum, mean, median 
            and standard deviation of the pixel intensities.
    """
    masked_pixels = seg.masked_scan[seg.mask != 0]
    # Find the maximum pixel intensity.
    max_pixel = np.max(masked_pixels)
    # Find the minimum pixel intensity.
    min_pixel = np.min(masked_pixels)
    # Find the mean pixel intensity.
    mean_pixel = np.mean(masked_pixels)
    # Find the median pixel intensity.
    median_pixel = np.median(masked_pixels)
    # Find the standard deviation of the pixel intensities.
    std_pixel = np.std(masked_pixels)
    # Create a dictionary containing the information.
    pixel_info = {'Maximum Pixel Intensity': max_pixel,
                'Minimum Pixel Intensity': min_pixel,
                'Mean Pixel Intensity': mean_pixel,
                'Median Pixel Intensity': median_pixel,
                'Standard Deviation of Pixel Intensities': std_pixel}
    return pixel_info


def _find_perc_tissue(seg: MaskedScan):
    """
    Finds the percentage of each tissue within the mask.
    
    Parameters
    ----------
        seg: ct_analyser.cta.MaskedScan
            The MaskedScan object to find the percentage of each tissue 
            in.
        
    Returns
    -------
        perc_tissue_dict: dict
            A dictionary containing the percentage of each tissue in the 
            mask in the form {tissue: percentage}.
    """
    # Get the thresholds.
    thresholds = seg.threshold
    # Get the masked pixels.
    masked_pixels = seg.masked_scan[seg.mask != 0]
    # Find the number of pixels in each tissue.
    num_pixels = np.zeros(len(thresholds))
    for i, key in enumerate(thresholds.keys()):
        # Find the number of pixels within the bounds of each threshold.
        num_pixels[i] = np.sum(np.logical_and(masked_pixels >= \
                    thresholds[key][0], masked_pixels <= thresholds[key][1]))
    # Find the percentage each tissue makes up.
    perc_tissue = num_pixels / np.sum(num_pixels) * 100
    # Create a dictionary containing the information.
    perc_tissue_dict = {}
    for i, key in enumerate(thresholds.keys()):
        perc_tissue_dict[key] = perc_tissue[i]
    
    return perc_tissue_dict