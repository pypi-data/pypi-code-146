import os # To delete the temp file
import numpy as np

from skimage.filters import gaussian # Implementing the image sharpening filter

import matplotlib.pyplot as plt # Plotting
from matplotlib.colors import LogNorm # Look up table
from matplotlib.colors import PowerNorm # Look up table

try:
    from ipywidgets import interact
    import ipywidgets as widgets
    has_widgets = True
except:
    has_widgets = False

try:
    import k3d
    from k3d.factory import *
    has_k3d = True
except:
    print("K3D is not install, you won't be able to visualise the 3D scene using k3D")
    has_k3d = False

try:
    import PIL
    has_PIL = True
except:
    print("PIL is not install, you won't be able to visualise the X-ray image in the 3D scene using k3D")
    has_PIL = False

try:
    import matplotlib.pyplot as plt # Plotting
    has_MPL = True
except:
    print("Matplotlib is not install, you won't be able to visualise the X-ray image in the 3D scene using Matplotlib")
    has_MPL = False

try:
    import spekpy as sp
    has_spekpy = True
except:
    print("spekpy is not install, you won't be able to load a beam spectrum using spekpy")
    has_spekpy = False

try:
    from xpecgen import xpecgen as xg
    has_xpecgen = True
except:
    print("xpecgen is not install, you won't be able to load a beam spectrum using xpecgen")
    has_xpecgen = False

import math
from gvxrPython3 import gvxr # Simulate X-ray images


def standardisation(img: np.array) -> np.array:
    """
    Standardisation on an image, also known as zero-mean, unit-variance normalisation.
    The average pixel value of the new image is 0, the standard deviation 1.

    @param img: the image to standardise
    @return: the image after standardisation
    """
    return (img - img.mean()) / img.std()

def logImage(xray_image: np.array, min_val: float, max_val: float) -> np.array:
    """
    Apply the log tranformation on the image.
    """

    log_epsilon = 1.0e-9

    shift_filter = -math.log(min_val + log_epsilon)

    if min_val != max_val:
        scale_filter = 1.0 / (math.log(max_val + log_epsilon) - math.log(min_val + log_epsilon))
    else:
        scale_filter = 1.0

    corrected_image = np.log(xray_image + log_epsilon)

    return (corrected_image + shift_filter) * scale_filter

def applyLogScaleAndNegative(image: np.array) -> np.array:
    temp = logImage(image, image.min(), image.max())
    return 1.0 - temp

def sharpen(image, ksize, alpha):
    details = image - gaussian(image, ksize)

    return image + alpha * details

def rgb2k3d(R, G, B):
    k3d_color = 0;
    k3d_color |= (R & 255) << 16;
    k3d_color |= (G & 255) << 8;
    k3d_color |= (B & 255);
    return k3d_color

def plotScreenshot():

    """
    Display the 3D scene (offscreen rendering may be used in the background) using Matplotlib.
    """

    if has_MPL:
        gvxr.displayScene()
        screenshot = gvxr.takeScreenshot()
        plt.figure(figsize=(10, 10))
        plt.imshow(screenshot)
        plt.title("Screenshot of the X-ray simulation environment")
        plt.axis('off')

def visualize(use_log: bool=False, use_negative: bool=False, sharpen_ksize:int=1, sharpen_alpha:float=0.0):

    """
    Display the 3D scene using K3D (see https://github.com/K3D-tools/K3D-jupyter).

    @param use_log: Display the X-ray image using a log scale (default: False)
    @param use_negative: Display the X-ray image in negative (default: False)
    @sharpen_ksize: the radius of the Gaussian kernel used in the sharpening filter (default: 1)
    @sharpen_alpha: the alpha value used in the sharpening filter (default: 0.0)
    """

    if has_k3d:
        up_x,up_y, up_z = gvxr.getDetectorUpVector()
        src_x_pos, src_y_pos, src_z_pos = gvxr.getSourcePosition("mm")
        det_x_pos, det_y_pos, det_z_pos = gvxr.getDetectorPosition("mm")
        sdd = math.sqrt(math.pow(src_x_pos - det_x_pos, 2) + math.pow(src_y_pos - det_y_pos, 2) + math.pow(src_z_pos - det_z_pos, 2))

        w, h = gvxr.getDetectorSize("mm")
        half_w = w / 2
        half_h = h / 2

        half_view_angle_rad = math.atan(half_w / sdd)
        half_view_angle_deg = half_view_angle_rad * 180 / math.pi
        fov = 2.0 * half_view_angle_deg

        view_vec_x = src_x_pos - det_x_pos
        view_vec_y = src_y_pos - det_y_pos
        view_vec_z = src_z_pos - det_z_pos

        camera = [
            src_x_pos + view_vec_x, src_y_pos + view_vec_y, src_z_pos + view_vec_z, # position of the camera in xyz space
            det_x_pos, det_y_pos, det_z_pos, # the point where camera is currently looking at
            -up_x, -up_y, -up_z  # orientation (up direction), this vector cannot be [0,0,0])
        ]

        plot = k3d.plot()
        plot.background_color = 0xffffff

        # Add the X-ray source
        sphere = points(
                positions=[src_x_pos, src_y_pos, src_z_pos],
                color=rgb2k3d(255, 0, 0),
                point_size=10,
                shader="mesh",
                name="X-ray source",
        )

        plot += sphere

        # Add the X-ray detector
        detector_vertices = np.array(gvxr.getDetectorVertices()).astype(np.single)
        faces = np.array([[0,1,2], [3,4,5]]).astype(np.uint32)

        # Create the STL file
        # quad = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        # for i, f in enumerate(faces):
        #     for j in range(3):
        #         quad.vectors[i][j] = detector_vertices[f[j],:]

        # # Write the mesh to file "detector.stl"
        # fname = "detector.stl"
        # quad.save(fname)

        # Create the texture
        file_content = None
        texture_file_format = None

        # Create an image using PIL
        if has_PIL:
            xray_image = np.array(gvxr.computeXRayImage()).astype(np.single)
            total_energy_in_MeV = gvxr.getTotalEnergyWithDetectorResponse()
            white = np.ones(xray_image.shape) * total_energy_in_MeV
            dark = np.zeros(xray_image.shape)
            xray_image_flat = ((xray_image - dark) / (white - dark)).astype(np.single)

            if use_log:
                xray_image_flat = logImage(xray_image_flat, 0.0, 1.0)
                xray_image_flat = (xray_image_flat - xray_image_flat.min()) / (xray_image_flat.max() - xray_image_flat.min())

            if use_negative:
                xray_image_flat = 1.0 - xray_image_flat

            xray_image_flat = sharpen(xray_image_flat, sharpen_ksize, sharpen_alpha)
            xray_image_flat[xray_image_flat<0] = 0
            xray_image_flat[xray_image_flat>1] = 1

            # save a image using extension
            pil_img = PIL.Image.fromarray((255 * xray_image_flat).astype(np.uint8))

            if pil_img.mode != 'RGB':
                pil_img = pil_img.convert('L')

            pil_img.save("temp_texture.png")

            with open("temp_texture.png", mode='rb') as file: # b is important -> binary
                file_content = file.read()

            texture_file_format = "png"

            # Delete the file, it's no longer needed
            os.remove("temp_texture.png")

        # Create the geometry
        detector_geometry = k3d.mesh(detector_vertices,
                              faces,
                              color=rgb2k3d(255, 255, 255),
                              # wireframe=False,
                              # flat_shading=False,
                              name="X-ray detector (front)",
                              opacity=1,
                              texture=file_content,
                              texture_file_format=texture_file_format,
                              uvs=[0, 0,
                                   1, 0,
                                   1, 1,
                                   0, 0,
                                   1, 1,
                                   0, 1],
                              side="front"
                                    )

        plot += detector_geometry

        detector_geometry = k3d.mesh(detector_vertices,
                              faces,
                              color=rgb2k3d(255, 255, 255),
                              # wireframe=False,
                              # flat_shading=False,
                              name="X-ray detector (back)",
                              opacity=1,
                              texture=file_content,
                              texture_file_format=texture_file_format,
                              uvs=[0, 0,
                                   1, 0,
                                   1, 1,
                                   0, 0,
                                   1, 1,
                                   0, 1],
                              side="back"
                                    )

        plot += detector_geometry

        # Add the scanned object
        nodes_to_be_processed = ["root"]

        while len(nodes_to_be_processed) > 0:

            # Get the last node
            node = nodes_to_be_processed[-1]
            nodes_to_be_processed.pop()

            for i in range(gvxr.getNumberOfChildren(node)):
                nodes_to_be_processed.append(gvxr.getChildLabel(node, i))

            # Get the triangles
            vertex_set = gvxr.getVertexSet(node)
            index_set = gvxr.getIndexSet(node)

            if len(index_set) == 0:
                index_set = range(int(len(vertex_set) / 3))

            # The node is empty
            if len(vertex_set):
                # Get the colour
                r, g, b, a = gvxr.getAmbientColour(node)
                R = math.floor(255*r)
                G = math.floor(255*g)
                B = math.floor(255*b)

                if node.upper() == "MUSCLE" or node.upper() == "MUSCLES":
                    opacity = 0.3
                elif node.upper() == "SKIN":
                    opacity = 0.2
                else:
                    opacity = 1

                # Create the geometry
                geometry = k3d.mesh(vertex_set,
                                      index_set,
                                      color=rgb2k3d(R, G, B),
                                      wireframe=False,
                                      flat_shading=False,
                                      name=node,
                                      opacity=opacity)

                # Add the geometry to the plot
                plot += geometry
        return plot
    else:
        print("K3D was not found.")
        return None


def visualise(use_log=False, use_negative=False, sharpen_ksize=1, sharpen_alpha=0.0):

    """
    Display the 3D scene using K3D (see https://github.com/K3D-tools/K3D-jupyter).

    @param use_log: Display the X-ray image using a log scale (default: False)
    @param use_negative: Display the X-ray image in negative (default: False)
    @sharpen_ksize: the radius of the Gaussian kernel used in the sharpening filter (default: 1)
    @sharpen_alpha: the alpha value used in the sharpening filter (default: 0.0)
    """

    return visualize(use_log, use_negative, sharpen_ksize, sharpen_alpha)


def saveProjections(x_ray_image: np.array, fname: str=None, gamma=0.5, figsize=(17, 7.5)):

    """
    Use Matplotlib to display (and save) the X-ray image using i) a linear scale, ii) a log scale, and iii) a power law.

    @param x_ray_image: The image to display
    @param fname: The file name to save the plot (default: None)
    @gamma: the gamma value used in the Power law (default: 0.5)
    @gamma figsize: the size of the figure (default: (17, 7.5))
    """

    plt.figure(figsize=figsize)

    plt.suptitle("Image simulated with gVirtualXray visualised", y=0.75)

    plt.subplot(131)
    plt.imshow(x_ray_image, cmap="gray")
    plt.colorbar(orientation='horizontal')
    plt.title("using a linear colour scale")

    plt.subplot(132)
    plt.imshow(x_ray_image, norm=LogNorm(), cmap="gray")
    plt.colorbar(orientation='horizontal')
    plt.title("using a logarithmic colour scale")

    plt.subplot(133)
    plt.imshow(x_ray_image, norm=PowerNorm(gamma=1.0 / gamma), cmap="gray")
    plt.colorbar(orientation='horizontal');
    plt.title("using a Power-law colour scale ($\gamma=" + str(gamma) +"$)")

    plt.tight_layout()
    plt.margins(0,0)

    if fname is not None:
        plt.savefig(fname, bbox_inches='tight');

def compareWithGroundTruth(groundTruth: np.array, testImage: np.array, fname: str=None, figsize=(17, 7.5)):

    """
    Use Matplotlib to display (and save) the X-ray image using i) a linear scale, ii) a log scale, and iii) a power law.

    @param groundTruth: The image corresponding to the ground truth
    @param testImage: The test image
    @param fname: The file name to save the plot (default: None)
    @gamma figsize: the size of the figure (default: (17, 7.5))
    """

    plt.figure(figsize=figsize)

    # Relative error in %
    comp_equalized = 100 * ((groundTruth).astype(np.single) - (testImage).astype(np.single)) / (groundTruth).astype(np.single)

    vmin = np.min(groundTruth)
    vmax = np.max(groundTruth)

    plt.subplot(131)
    plt.imshow(groundTruth, cmap="gray", vmin=vmin, vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.title("Ground truth")

    plt.subplot(132)
    plt.imshow(testImage, cmap="gray", vmin=vmin, vmax=vmax)
    plt.colorbar(orientation='horizontal')
    plt.title("gVirtualXRay")

    plt.subplot(133)
    plt.imshow(comp_equalized, cmap="RdBu", vmin=-5, vmax=5)
    plt.colorbar(orientation='horizontal');
    plt.title("Relative error (in %)")

    plt.tight_layout()
    plt.margins(0,0)

    if fname is not None:
        plt.savefig(fname, bbox_inches = 'tight')

def interactPlotPowerLaw(xray_image: np.array, gamma:float=0.5, figsize=(10, 5)):

    """
    Use Matplotlib and a Jupyter widget to display the X-ray image using a power law.
    The gamma value can be change interactively.

    @param xray_image: The image to display
    @gamma: the gamma value used in the Power law (default: 0.5)
    @gamma figsize: the size of the figure (default: (10, 5))
    """

    fig_plot = plt.figure(figsize=figsize)
    ax_img = plt.subplot(111)
    img = plt.imshow(xray_image, norm=PowerNorm(gamma=1./gamma), cmap="gray")
    cbar = fig_plot.colorbar(img, orientation='vertical')
    title_str = "Using a Power-law colour scale ($\gamma=" + str(gamma) + "$)"
    ax_img.set_title(title_str)
    plt.tight_layout()
    plt.margins(0,0)

    if has_widgets:
        plt.close()

    ## Callback function: plot y=Acos(x+phi)
    def update_plot(gamma):
        img = ax_img.imshow(xray_image, norm=PowerNorm(gamma=1./gamma), cmap="gray")
        title_str = "Using a Power-law colour scale ($\gamma=" + str(gamma) + "$)"
        ax_img.set_title(title_str)
        fig_plot.colorbar(img, cax=cbar.ax, orientation='vertical')

        display(fig_plot)

    if has_widgets:
        interact(update_plot,
                 gamma=widgets.FloatSlider(value=gamma, min=0.09, max=5.0, step=0.1, description="gamma"))







def getSpectrumSpekpy(kvp_in_kV, filters=None, th_in_deg=12):

    unit = "keV"
    k = []
    f = []

    # Spekpy is installed
    if has_spekpy:

        # Generate a spectrum
        s = sp.Spek(kvp=kvp_in_kV, th=th_in_deg)

        #Inherent filtration: 1.2mm Al + 100cm Air
        s.filter("Al", 1.2)
        # s.filter("air", 1000)

        # Additional filters
        if filters is not None:
            for beam_filter in filters:
                filter_material = beam_filter[0]
                filter_thickness_in_mm = beam_filter[1]

                s.filter(filter_material, filter_thickness_in_mm)

        # Get the spectrum
        k, f = s.get_spectrum(edges=True)

        # Normalise the area under the curve
        area = 0.0
        prev_bin = None
        for energy, count in zip(k, f):
            if prev_bin is not None:
                area += count * (energy - prev_bin)
            prev_bin = energy

        f = np.array(f) / area

    return k, f, unit


def getSpekpySpectrum(kvp_in_kV, filters=None, th_in_deg=12):
    return getSpectrumSpekpy(kvp_in_kV, filters, th_in_deg)


def getSpectrumXpecgen(kvp_in_kV, filters=None, th_in_deg=12):

    unit = "keV"
    k = []
    f = []

    # xpecgen is installed
    if has_xpecgen:

        # Generate a spectrum
        xrs = xg.calculate_spectrum(kvp_in_kV, th_in_deg, 1, 100, epsrel=0.5, monitor=None, z=74)

        #Inherent filtration: 1.2mm Al + 100cm Air
        mu_Al = xg.get_mu(13)
        xrs.attenuate(0.12,mu_Al)
        # xrs.attenuate(100,xg.get_mu("air"))

        # Additional filters
        if filters is not None:
            for beam_filter in filters:
                filter_material = beam_filter[0]
                filter_thickness_in_mm = beam_filter[1]

                if type(filter_material) == str:
                    mu = xg.get_mu(gvxr.getElementAtomicNumber(filter_material))
                else:
                    mu = xg.get_mu(filter_material)

                xrs.attenuate(filter_thickness_in_mm / 10, mu)

        # Get the spectrum
        (k,f) = xrs.get_points()

        # Normalise the area under the curve
        area = 0.0
        prev_bin = None
        for energy, count in zip(k, f):
            if prev_bin is not None:
                area += count * (energy - prev_bin)
            prev_bin = energy

        f = np.array(f) / area

    return k, f, unit


def getXpecgenSpectrum(kvp_in_kV, filters=None, th_in_deg=12):
    return getSpectrumXpecgen(kvp_in_kV, filters, th_in_deg)


def getSpectrumTextFile(fname: str, units: str):

    gate_macro_file = open(fname, 'r')

    # Read the file
    lines = gate_macro_file.readlines()

    # Process every line
    for line in lines:
        # Check if this is a comment or not
        comment = True
        index_first_non_space_character = len(line) - len(line.lstrip())

        if index_first_non_space_character >= 0 and index_first_non_space_character < len(line):
            if line[index_first_non_space_character] != '#':
                comment = False

        # This is not a comment
        if not comment:
            x = line.split()

        # The first column is an index
        if len(x) == 3:
            energy = float(x[1])
            count = float(x[2])
        elif len(x) == 2:
            energy = float(x[0])
            count = float(x[1])
        else:
            raise ValueError("The number of columns in " + fname + " is " + str(len(x)) + ", which is invalid. We expected 2 or 3 columns.")

        spectrum[energy] = count

        if verbose > 0:
            if count == 1:
                print("\t", str(count), "photon of", energy, units);
            else:
                print("\t", str(count), "photons of", energy, units);

        k.append(energy)
        f.append(count)

    k = np.array(k)
    f = np.array(f)

    return k, f, units


def getTextFileSpectrum(fname):
    return getSpectrumTextFile(fname)


def loadSpectrum(k, f, unit):

    gvxr.resetBeamSpectrum()

    spectrum = {}

    for energy, count in zip(k, f):

        if count > 1.0e-6:

            if energy in spectrum.keys():
                spectrum[energy] += count
            else:
                spectrum[energy] = count

    for energy in spectrum.keys():
        count = spectrum[energy]
        gvxr.addEnergyBinToSpectrum(energy, unit, count);

    return spectrum


def loadSpectrumSpekpy(kvp_in_kV, filters=None, th_in_deg=12):
    k, f, unit = getSpectrumSpekpy(kvp_in_kV, filters, th_in_deg)
    return loadSpectrum(k, f, unit), k, f, unit


def loadSpectrumXpecgen(kvp_in_kV, filters=None, th_in_deg=12):
    k, f, unit = getSpectrumXpecgen(kvp_in_kV, filters, th_in_deg)
    return loadSpectrum(k, f, unit), k, f, unit


def loadSpectrumTextFile(fname: str, units: str):
    k, f, unit = getSpectrumTextFile(fname, units)
    return loadSpectrum(k, f, unit), k, f, unit


def loadSpekpySpectrum(kvp_in_kV, filters=None, th_in_deg=12):
    return loadSpectrumSpekpy(kvp_in_kV, filters, th_in_deg)


def loadXpecgenSpectrum(kvp_in_kV, filters=None, th_in_deg=12):
    return loadSpectrumXpecgen(kvp_in_kV, filters, th_in_deg)


def loadTextFileSpectrum(kvp_in_kV, filters=None, th_in_deg=12):
    return loadSpectrumTextFile(kvp_in_kV, filters, th_in_deg)
