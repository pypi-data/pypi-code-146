"""
Library of SPAM functions for plotting orientations in 3D
Copyright (C) 2020 SPAM Contributors

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
"""


#
# Edward Ando 17/11/2011
#
# Attempt at programming rose plots myself.

# Assuming that the contacts are kind of flat, and so the normal vector pointing up from them is correct
# which means using Visilog's Orientation 2 vectors.

# Modified in order to allow vector components to be taken as input directly

# 2012.08.27 - adding ability to output projected components, in order to allow plotting
#   with gnuplot

# Completely new version with objective of:
#   - reading in different formats (3D coordinates (x,y,z,), Spherical Coordinates, Cylindrical)
#   - outputting any other format
#   - Different projections onto the plane (Lambert, Stereo, direct, etc...)
#   - Possibility to colour the negative part of the projected sphere in a different colour
#   - Projection point-by-point or binned with Hugues Talbot and Clara's code, which
#       gives the very convenient cutting of the circle into in equal area parts:
#         Jaquet, C., Andò, E., Viggiani, G., & Talbot, H. (2013).
#         Estimation of separating planes between touching 3D objects using power watershed.
#         In Mathematical Morphology and Its Applications to Signal and Image Processing (pp. 452-463).
#         Springer Berlin Heidelberg.

# Internal data format will be x,y,z sphere, with x-y defining the plane of projection.

# 2015-07-24 -- EA and MW -- checking everything, there were many bugs -- the points were only plotted to an extent of 1 and not radiusMax
#               created plotting function, which allows radius labels to be updated.

# 2016-11-08 -- MW -- binning was still erroneous. an angularBin (lines 348ff) was usually put to the next higher bin, so not rounded correctly
#               rounding now with numpy.rint and if the orientation doesn't belong to the last bin, it has to be put in the first one
#                 as the first bin extends to both sides of 0 Degrees. -> check validation example in lines 227ff

# 2017-06-01 -- MW -- updating for the current numpy version 1.12.1 and upgrading matplotlib to 2.0.2

# 2017-06-26 -- MW -- there still was a small bug in the binning: for the angular bin numpy.rint was used -- replaced it with numpy.floor (line 375)
#                     benchmarking points are in lines 217ff.

# 2018-02-19 -- EA -- changes in the new matplot version revealed a problem. Eddy solved it for the spam client, MW modified this one here.

# 2018-04-20 -- MW -- adding relative bin counts -- to normalise the bincounts by the average overall bin count.
#                     enables to plot many states with the same legend!

import math
import multiprocessing
import os
import random
import sys

import matplotlib
import matplotlib.colors as mcolors
import matplotlib.pyplot
import numpy
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection

import orientationpy

nProcessesDefault = multiprocessing.cpu_count()

VERBOSE = False

# ask numpy to print 0.000 without scientific notation
numpy.set_printoptions(suppress=True)
numpy.set_printoptions(precision=3)


def projectOrientations3d(vector, coordSystem, projectionSystem):
    """
    This functions projects a 3D vector from a given coordinate system into a 2D plane given by a defined projection.

    Parameters
    ----------
        vector: 1x3 array of floats
            Vector to be projected
            For cartesian system: ZYX
            For spherical system: r, theta (inclination), phi (azimuth) in Radians

        coordSystem: string
            Coordinate system of the vector
            Either "cartesian" or "spherical"

        projectionSystem : string
            Projection to be used
            Either "lambert", "stereo" or "equidistant"

    Returns
    -------
        projection_xy: 1x2 array of floats
            X and Y coordinates of the projected vector

        projection_theta_r: 1x2 array of floats
            Theta and R coordinates of the projected vector in radians

    """

    projection_xy_local = numpy.zeros(2)
    projection_theta_r_local = numpy.zeros(2)

    # Reshape the vector and check for errors in shape
    try:
        vector = numpy.reshape(vector, (3, 1))
    except:
        print("\n projectOrientations3d: The vector must be an array of 1x3")
        return

    if coordSystem == "spherical":
        # unpack vector

        r, theta, phi = vector

        x = r * math.sin(theta) * math.cos(phi)
        y = r * math.sin(theta) * math.sin(phi)
        z = r * math.cos(theta)

    elif coordSystem == "cartesian":

        # unpack vector
        z, y, x = vector
        # we're in cartesian coordinates, (x-y-z mode) Calculate spherical coordinates
        # passing to 3d spherical coordinates too...
        # From: https://en.wikipedia.org/wiki/Spherical_coordinate_system
        #  Several different conventions exist for representing the three coordinates, and for the order in which they should be written.
        #  The use of (r, θ, φ) to denote radial distance, inclination (or elevation), and azimuth, respectively, is common practice in physics, and is specified by ISO standard 80000-2 :2009, and earlier in ISO 31-11 (1992).
        r = numpy.sqrt(x**2 + y**2 + z**2)
        theta = math.acos(z / r)  # inclination
        phi = math.atan2(y, x)  # azimuth

    else:
        print("\n projectOrientations3d: Wrong coordinate system")
        return

    if projectionSystem == "lambert":  # dividing by sqrt(2) so that we're projecting onto a unit circle
        projection_xy_local[0] = x * (math.sqrt(2 / (1 + z)))
        projection_xy_local[1] = y * (math.sqrt(2 / (1 + z)))

        # sperhical coordinates -- CAREFUL as per this wikipedia page: https://en.wikipedia.org/wiki/Lambert_azimuthal_equal-area_projection
        #   the symbols for inclination and azimuth ARE INVERTED WITH RESPEST TO THE SPHERICAL COORDS!!!
        projection_theta_r_local[0] = phi
        #                                                  HACK: doing math.pi - angle in order for the +z to be projected to 0,0
        projection_theta_r_local[1] = 2 * math.cos((math.pi - theta) / 2)

        # cylindrical coordinates
        # projection_theta_r_local[0] = phi
        # projection_theta_r_local[1] = math.sqrt( 2.0 * ( 1 + z ) )

    elif projectionSystem == "stereo":
        projection_xy_local[0] = x / (1 - z)
        projection_xy_local[1] = y / (1 - z)

        # https://en.wikipedia.org/wiki/Stereographic_projection uses a different standard from the page on spherical coord Spherical_coordinate_system
        projection_theta_r_local[0] = phi
        #                                        HACK: doing math.pi - angle in order for the +z to be projected to 0,0
        #                                                                             HACK: doing math.pi - angle in order for the +z to be projected to 0,0
        projection_theta_r_local[1] = numpy.sin(math.pi - theta) / (1 - numpy.cos(math.pi - theta))

    elif projectionSystem == "equidistant":
        # https://en.wikipedia.org/wiki/Azimuthal_equidistant_projection
        # TODO: To be checked, but this looks like it should -- a straight down projection.
        projection_xy_local[0] = math.sin(phi)
        projection_xy_local[1] = math.cos(phi)

        projection_theta_r_local[0] = phi
        projection_theta_r_local[1] = numpy.cos(theta - math.pi / 2)

    else:
        print("\n projectOrientations3d: Wrong projection system")
        return

    return projection_xy_local, projection_theta_r_local


def plotOrientations3d(
    orientations_zyx,
    projection="lambert",
    plot="both",
    binValueMin=None,
    binValueMax=None,
    binNormalisation=False,
    numberOfRings=9,
    pointMarkerSize=8,
    cmap=matplotlib.pyplot.cm.RdBu_r,
    title="",
    subtitle={"points": "", "bins": ""},
    saveFigPath=None,
):
    """
    Main function for plotting 3D orientations.
    This function plots orientations (described by unit-direction vectors) from a sphere onto a plane.

    One useful trick for evaluating these orientations is to project them with a "Lambert equal area projection", which means that an isotropic distribution of angles is projected as equally filling the projected space.

    Parameters
    ----------
        orientations : Nx3 numpy array of floats
            Z, Y and X components of direction vectors.
            Non-unit vectors are normalised.

        projection : string, optional
            Selects different projection modes:
                **lambert** : Equal-area projection, default and highly reccommended. See https://en.wikipedia.org/wiki/Lambert_azimuthal_equal-area_projection

                **equidistant** : equidistant projection

        plot : string, optional
            Selects which plots to show:
                **points** : shows projected points individually
                **bins** : shows binned orientations with counts inside each bin as colour
                **both** : shows both representations side-by-side, default

        title : string, optional
            Plot main title. Default = ""

        subtitle : dictionary, optional
            Sub-plot titles:
                **points** : Title for points plot. Default = ""
                **bins** : Title for bins plot. Default = ""

        binValueMin : int, optional
            Minimum colour-bar limits for bin view.
            Default = None (`i.e.`, auto-set)

        binValueMax : int, optional
            Maxmum colour-bar limits for bin view.
            Default = None (`i.e.`, auto-set)

        binNormalisation : bool, optional
            In binning mode, should bin counts be normalised by mean counts on all bins
            or absolute counts?

        cmap : matplotlib colour map, optional
            Colourmap for number of counts in each bin in the bin view.
            Default = ``matplotlib.pyplot.cm.RdBu_r``

        numberOfRings : int, optional
            Number of rings (`i.e.`, radial bins) for the bin view.
            The other bins are set automatically to have uniform sized bins using an algorithm from Jacquet and Tabot.
            Default = 9 (quite small bins)

        pointMarkerSize : int, optional
            Size of points in point view (5 OK for many points, 25 good for few points/debugging).
            Default = 8 (quite big points)

        saveFigPath : string, optional
            Path to save figure to -- stops the graphical plotting.
            Default = None

    Returns
    -------
        None -- A matplotlib graph is created and show()n

    Note
    ----
        Authors: Edward Andò, Hugues Talbot, Clara Jacquet and Max Wiebicke
    """
    import matplotlib.pyplot

    # ========================================================================
    # ==== Reading in data, and formatting to x,y,z sphere                 ===
    # ========================================================================
    numberOfPoints = orientations_zyx.shape[0]

    # ========================================================================
    # ==== Check that all the vectors are unit vectors                     ===
    # ========================================================================
    if VERBOSE:
        print("\t-> Normalising all vectors in x-y-z representation..."),

    # from http://stackoverflow.com/questions/2850743/numpy-how-to-quickly-normalize-many-vectors
    norms = numpy.apply_along_axis(numpy.linalg.norm, 1, orientations_zyx)
    orientations_zyx = orientations_zyx / norms.reshape(-1, 1)

    if VERBOSE:
        print("done.")

    # ========================================================================
    # ==== At this point we should have clean x,y,z data in memory         ===
    # ========================================================================
    if VERBOSE:
        print("\t-> We have %i orientations in memory." % (numberOfPoints))

    # Since this is the final number of vectors, at this point we can set up the
    #   matrices for the projection.
    projection_xy = numpy.zeros((numberOfPoints, 2))

    # TODO: Check if there are any values less than zero or more that 2*pi
    projection_theta_r = numpy.zeros((numberOfPoints, 2))

    # ========================================================================
    # ==== Projecting from x,y,z sphere to the desired projection          ===
    # ========================================================================
    # TODO: Vectorise this...
    for vectorN in range(numberOfPoints):
        # unpack 3D x,y,z
        z, y, x = orientations_zyx[vectorN]
        # print "\t\txyz = ", x, y, z

        # fold over the negative half of the sphere
        #     flip every component of the vector over
        if z < 0:
            z = -z
            y = -y
            x = -x

        projection_xy[vectorN], projection_theta_r[vectorN] = projectOrientations3d([z, y, x], "cartesian", projection)

    # get radiusMax based on projection
    #                                    This is only limited to sqrt(2) because we're flipping over the negative side of the sphere
    if projection == "lambert":
        radiusMax = numpy.sqrt(2)
    elif projection == "stereo":
        radiusMax = 1.0
    elif projection == "equidistant":
        radiusMax = 1.0

    if VERBOSE:
        print("\t-> Biggest projected radius (r,t) = {}".format(numpy.abs(projection_theta_r[:, 1]).max()))

    # print "projection_xy\n", projection_xy
    # print "\n\nprojection_theta_r\n", projection_theta_r

    if plot == "points" or plot == "both":
        fig = matplotlib.pyplot.figure()
        fig.suptitle(title)
        if plot == "both":
            ax = fig.add_subplot(121, polar=True)
        else:
            ax = fig.add_subplot(111, polar=True)

        ax.set_title(subtitle["points"] + "\n")

        # set the line along which the numbers are plotted to 0°
        # ax.set_rlabel_position(0)
        matplotlib.pyplot.axis((0, math.pi * 2, 0, radiusMax))

        # set radius grids to 15, 30, etc, which means 6 numbers (r=0 not included)
        radiusGridAngles = numpy.arange(15, 91, 15)
        radiusGridValues = []
        for angle in radiusGridAngles:
            #                        - project the 15, 30, 45 as spherical coords, and select the r part of theta r-
            #               - append to list of radii -

            radiusGridValues.append(projectOrientations3d([0, angle * math.pi / 180.0, 1], "spherical", projection)[1][1])
        #                                       --- list comprehension to print 15°, 30°, 45° ----------
        ax.set_rgrids(radiusGridValues, labels=[r"%02i$^\circ$" % (x) for x in numpy.arange(15, 91, 15)], angle=None, fmt=None)
        ax.plot(projection_theta_r[:, 0], projection_theta_r[:, 1], ".", markersize=pointMarkerSize)

        if plot == "points":
            matplotlib.pyplot.show()

    if plot == "bins" or plot == "both":
        # ========================================================================
        # ==== Binning the data -- this could be optional...                   ===
        # ========================================================================
        # This code inspired from Hugues Talbot and Clara Jaquet's developments.
        # As published in:
        #   Identifying and following particle-to-particle contacts in real granular media: an experimental challenge
        #   Gioacchino Viggiani, Edward Andò, Clara Jaquet and Hugues Talbot
        #   Keynote Lecture
        #   Particles and Grains 2013 Sydney
        #
        # ...The number of radial bins (numberOfRings)
        # defines the radial binning, and for each radial bin starting from the centre,
        # the number of angular bins is  4(2n + 1)
        #
        import matplotlib.collections

        # from matplotlib.colors import Normalize
        import matplotlib.colorbar
        import matplotlib.patches

        if plot == "both":
            ax = fig.add_subplot(122, polar=True)
        if plot == "bins":
            fig = matplotlib.pyplot.figure()
            ax = fig.add_subplot(111, polar=True)

        if VERBOSE:
            print("\t-> Starting Data binning...")

        # This must be an integer -- could well be a parameter if this becomes a function.
        if VERBOSE:
            print("\t-> Number of Rings (radial bins) = ", numberOfRings)

        # As per the publication, the maximum number of bins for each ring, coming from the inside out is 4(2n + 1):
        numberOfAngularBinsPerRing = numpy.arange(1, numberOfRings + 1, 1)
        numberOfAngularBinsPerRing = 4 * (2 * numberOfAngularBinsPerRing - 1)

        if VERBOSE:
            print("\t-> Number of angular bins per ring = ", numberOfAngularBinsPerRing)

        # defining an array with dimensions numberOfRings x numberOfAngularBinsPerRing
        binCounts = numpy.zeros((numberOfRings, numberOfAngularBinsPerRing[-1]))

        # ========================================================================
        # ==== Start counting the vectors into bins                            ===
        # ========================================================================
        for vectorN in range(numberOfPoints):
            # unpack projected angle and radius for this point
            angle, radius = projection_theta_r[vectorN, :]

            # Flip over negative angles
            if angle < 0:
                angle += 2 * math.pi
            if angle > 2 * math.pi:
                angle -= 2 * math.pi

            # Calculate right ring number
            ringNumber = int(numpy.floor(radius / (radiusMax / float(numberOfRings))))

            # Check for overflow
            if ringNumber > numberOfRings - 1:
                if VERBOSE:
                    print("\t-> Point with projected radius = {:f} is a problem (radiusMax = {:f}), putting in furthest  bin".format(radius, radiusMax))
                ringNumber = numberOfRings - 1

            # Calculate the angular bin
            angularBin = int(numpy.floor((angle) / (2 * math.pi / float(numberOfAngularBinsPerRing[ringNumber])))) + 1

            # print "numberOfAngularBinsPerRing", numberOfAngularBinsPerRing[ringNumber] - 1
            # Check for overflow
            #  in case it doesn't belong in the last angularBin, it has to be put in the first one!
            if angularBin > numberOfAngularBinsPerRing[ringNumber] - 1:
                if VERBOSE:
                    print("\t-> Point with projected angle = %f does not belong to the last bin, putting in first bin" % (angle))
                angularBin = 0

            # now that we know what ring, and angular bin you're in add one count!
            binCounts[ringNumber, angularBin] += 1

        # ========================================================================
        # === Plotting binned data                                             ===
        # ========================================================================

        plottingRadii = numpy.linspace(radiusMax / float(numberOfRings), radiusMax, numberOfRings)
        # print "Plotting radii:", plottingRadii

        # ax  = fig.add_subplot(122, polar=True)
        # matplotlib.pyplot.axis()
        # ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
        bars = []

        # add two fake, small circles at the beginning so that they are overwritten
        #   they will be coloured with the min and max colour
        #              theta   radius    width
        bars.append([0, radiusMax, 2 * math.pi])
        bars.append([0, radiusMax, 2 * math.pi])
        # bars.append(ax.bar(0,   radiusMax,    2*math.pi, bottom=0.0))
        # bars.append(ax.bar(0,   radiusMax,    2*math.pi, bottom=0.0))

        # --- flatifiying binned data for colouring wedges                    ===
        flatBinCounts = numpy.zeros(numpy.sum(numberOfAngularBinsPerRing) + 2)

        # Bin number as we go through the bins to add the counts in order to the flatBinCounts
        # This is two in order to skip the first to fake bins which set the colour bar.
        binNumber = 2

        # --- Plotting binned data, from the outside, inwards.                 ===
        if binNormalisation:
            avg_binCount = float(numberOfPoints) / numpy.sum(numberOfAngularBinsPerRing)
            # print "\t-> Number of points = ", numberOfPoints
            # print "\t-> Number of bins   = ", numpy.sum(numberOfAngularBinsPerRing)
            if VERBOSE:
                print("\t-> Average binCount = ", avg_binCount)

        for ringNumber in range(numberOfRings)[::-1]:
            deltaTheta = 360 / float(numberOfAngularBinsPerRing[ringNumber])
            deltaThetaRad = 2 * math.pi / float(numberOfAngularBinsPerRing[ringNumber])

            # --- Angular bins                                                 ---
            for angularBin in range(numberOfAngularBinsPerRing[ringNumber]):
                # ...or add bars
                #                           theta                             radius                  width
                bars.append([angularBin * deltaThetaRad - deltaThetaRad / 2.0, plottingRadii[ringNumber], deltaThetaRad])
                # bars.append(ax.bar(angularBin*deltaThetaRad - deltaThetaRad/2.0, plottingRadii[ ringNumber ], deltaThetaRad, bottom=0.0))

                # Add the number of vectors counted for this bin
                if binNormalisation:
                    flatBinCounts[binNumber] = binCounts[ringNumber, angularBin] / avg_binCount
                else:
                    flatBinCounts[binNumber] = binCounts[ringNumber, angularBin]

                # Add one to bin number
                binNumber += 1

        del binNumber

        # figure out auto values if they're requested.
        if binValueMin is None:
            binValueMin = flatBinCounts[2::].min()
        if binValueMax is None:
            binValueMax = flatBinCounts[2::].max()

        # Add two flat values for the initial wedges.
        flatBinCounts[0] = binValueMin
        flatBinCounts[1] = binValueMax

        ##                           theta                   radius                          width
        barsPlot = ax.bar(numpy.array(bars)[:, 0], numpy.array(bars)[:, 1], width=numpy.array(bars)[:, 2], bottom=0.0)

        for binCount, bar in zip(flatBinCounts, barsPlot):
            bar.set_facecolor(cmap((binCount - binValueMin) / float(binValueMax - binValueMin)))

        # matplotlib.pyplot.axis([ 0, radiusMax, 0, radiusMax ])
        matplotlib.pyplot.axis([0, numpy.deg2rad(360), 0, radiusMax])

        # colorbar = matplotlib.pyplot.colorbar(barsPlot, norm=matplotlib.colors.Normalize(vmin=minBinValue, vmax=maxBinValue))
        # Set the colormap and norm to correspond to the data for which
        # the colorbar will be used.

        norm = matplotlib.colors.Normalize(vmin=binValueMin, vmax=binValueMax)

        # ColorbarBase derives from ScalarMappable and puts a colorbar
        # in a specified axes, so it has everything needed for a
        # standalone colorbar.  There are many more kwargs, but the
        # following gives a basic continuous colorbar with ticks
        # and labels.
        ax3 = fig.add_axes([0.9, 0.1, 0.03, 0.8])
        cb1 = matplotlib.colorbar.ColorbarBase(ax3, cmap=cmap, norm=norm, label="Number of vectors in bin")

        # set the line along which the numbers are plotted to 0°
        # ax.set_rlabel_position(0)

        # set radius grids to 15, 30, etc, which means 6 numbers (r=0 not included)
        radiusGridAngles = numpy.arange(15, 91, 15)
        radiusGridValues = []
        for angle in radiusGridAngles:
            #                        - project the 15, 30, 45 as spherical coords, and select the r part of theta r-
            #               - append to list of radii -
            radiusGridValues.append(projectOrientations3d([0, angle * math.pi / 180.0, 1], "spherical", projection)[1][1])
        #                                       --- list comprehension to print 15°, 30°, 45° ----------
        ax.set_rgrids(radiusGridValues, labels=[r"%02i$^\circ$" % (x) for x in numpy.arange(15, 91, 15)], angle=None, fmt=None)

        fig.subplots_adjust(left=0.05, right=0.85)
        # cb1.set_label('Some Units')

        if saveFigPath is not None:
            matplotlib.pyplot.savefig(saveFigPath)
            matplotlib.pyplot.close()
        else:
            matplotlib.pyplot.show()


def distributionDensity(F, step=50, lim=None, color=None, viewAnglesDeg=[25, 45], title=None, saveFigPath=None):
    """
    Creates the surface plot of the distribution density of the deviatoric fabric tensor F

    Parameters
    ----------
        F : 3x3 array of floats
            deviatoric fabric tensor. Usually obtained from spam.label.fabricTensor

        step : int, optional
            Number of points for the surface plot
            Default = 50

        lim : float, optional
            Limit for the axes of the plot
            Default = None

        color : colormap class, optional
            Colormap class from matplotlib module
            See 'https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html' for options
            Example : matplotlib.pyplot.cm.viridis
            Default = matplotlib.pyplot.cm.Reds

        viewAnglesDeg : 2-component list, optional
            Set initial elevation and azimuth for this 3D plot

        title : str, optional
            Title for the graph
            Default = None

        saveFigPath : string, optional
            Path to save figure to.
            Default = None

    Returns
    -------
        None -- A matplotlib graph is created and shown

    Note
    ----
        see [Kanatani, 1984] for more information on the distribution density function for the deviatoric fabric tensor

    """
    # Create array of angles
    theta, phi = numpy.linspace(0, 2 * numpy.pi, step), numpy.linspace(0, numpy.pi, step)
    # Create meshgrid
    THETA, PHI = numpy.meshgrid(theta, phi)
    # Create radius array
    R = numpy.zeros(THETA.shape)
    # Copmute the radius for each angle
    for r in range(0, step, 1):
        for s in range(0, step, 1):
            vect = numpy.array((numpy.cos(phi[r]), numpy.sin(phi[r]) * numpy.sin(theta[s]), numpy.cos(theta[s]) * numpy.sin(phi[r])))
            R[r, s] = (1 / (4 * numpy.pi)) * (1 + numpy.dot(numpy.dot(F, vect), vect))
    # Change to cartesian coordinates
    X = R * numpy.sin(PHI) * numpy.cos(THETA)
    Y = R * numpy.sin(PHI) * numpy.sin(THETA)
    Z = R * numpy.cos(PHI)
    # Create figure
    import matplotlib

    matplotlib.rcParams.update({"font.size": 10})
    fig = matplotlib.pyplot.figure()
    ax = fig.add_subplot(111, projection="3d")
    # Set limits
    if lim == None:
        lim = round(numpy.max(R), 2)
    ax.set_xlim3d(-lim, lim)
    ax.set_ylim3d(-lim, lim)
    ax.set_zlim3d(-lim, lim)

    ax.view_init(viewAnglesDeg[0], viewAnglesDeg[1])
    # Set ticks
    ax.set_xticks((-lim, 0, lim))
    ax.set_yticks((-lim, 0, lim))
    ax.set_zticks((-lim, 0, lim))
    ax.set_box_aspect((1, 1, 1))
    # set axis titles
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_zlabel("Z axis")
    # Title
    if title is not None:
        ax.set_title(str(title) + "\n")
    # Colormap
    if color == None:
        cmap = matplotlib.pyplot.get_cmap(matplotlib.pyplot.cm.Reds)
    else:
        cmap = matplotlib.pyplot.get_cmap(color)
    norm = mcolors.Normalize(vmin=0, vmax=Z.max())
    # Plot
    ax.plot_surface(
        X,
        Y,
        Z,
        rstride=1,
        cstride=1,
        # facecolors = cmap(norm(numpy.abs(Z))),
        # coloring by max extension
        facecolors=cmap((R - numpy.amin(R)) / numpy.amax(R - numpy.amin(R))),
        linewidth=0,
        antialiased=True,
        alpha=1,
    )

    matplotlib.pyplot.tight_layout()
    if saveFigPath is not None:
        matplotlib.pyplot.savefig(saveFigPath)
    else:
        matplotlib.pyplot.show()


def plotSphericalHistogram(orientations, subDiv=3, reflection=True, maxVal=None, verbose=True, color=None, viewAnglesDeg=[25, 45], title=None, saveFigPath=None):
    """
    Generates a spherical histogram for vectorial data, binning the data into regions defined by the faces of an icosphere (convex polyhedron made from triangles).

    The icosphere is built from starting from an icosahedron (polyhedron with 20 faces) and then making subdivision on each triangle.
    The number of faces is  20*(4**subDiv).

    Parameters
    ----------
        orientations : Nx3 numpy array
            Vectors to be plotted

        subDiv : integer, optional
            Number of times that the initial icosahedron is divided.
            Default: 3

        reflection : bool, optional
            If true, the histogram takes into account the reflection of the vectors
            Default = True.

        maxVal : int, optional
            Maximum colour-bar limits for bin view.
            Default = None (`i.e.`, auto-set)

        verbose : bool, optional
            Print the evolution of the plot
            Defautl = False

        color : colormap class, optional
            Colormap class from matplotlib module
            See 'https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html' for options
            Example : matplotlib.pyplot.cm.viridis
            Default = matplotlib.pyplot.cm.viridis_r

        viewAnglesDeg : 2-component list, optional
            Set initial elevation and azimuth for this 3D plot

        title : str, optional
            Title for the graph
            Default = None

        saveFigPath : string, optional
            Path to save figure to, including the name and extension of the file.
            If it is not given, the plot will be shown but not saved.
            Default = None


    Returns
    -------
        None -- A matplotlib graph is created and shown

    """
    # Internal function for binning data into the icosphere faces

    def binIcosphere(data, icoVectors, verbose):
        # Create counts array
        counts = numpy.zeros(len(icoVectors))
        global computeAngle

        def computeAngle(i):
            # Get the orientation vector
            orientationVect = data[i]
            # Exchange Z and X position - for plotting
            orientationVect = [orientationVect[2], orientationVect[1], orientationVect[0]]
            # Create the result array
            angle = []
            for i in range(len(icoVectors)):
                # Compute the angle between them
                angle.append(numpy.arccos(numpy.clip(numpy.dot(orientationVect, icoVectors[i]), -1, 1)))
            # Get the index
            minIndex = numpy.argmin(angle)
            return minIndex

        # Create progressbar
        finishedOrientations = 0
        # Run multiprocessing
        with multiprocessing.Pool(processes=nProcessesDefault) as pool:
            for returns in pool.imap_unordered(computeAngle, range(len(data))):
                # Update the progressbar
                finishedOrientations += 1
                # Get the results
                index = returns
                # Add the count
                counts[index] += 1

        return counts

    # Get number of points
    numberOfPoints = orientations.shape[0]
    # Check that they are 3D vectors
    if orientations.shape[1] != 3:
        print("\nspam.helpers.orientationPlotter.plotSphericalHistogram: The input vectors are not 3D")
        return
    # from http://stackoverflow.com/questions/2850743/numpy-how-to-quickly-normalize-many-vectors
    norms = numpy.apply_along_axis(numpy.linalg.norm, 1, orientations)
    orientations = orientations / norms.reshape(-1, 1)
    # Check if we can reflect the vectors
    if reflection:
        orientations = numpy.vstack([orientations, -1 * orientations])
    # Create the icosphere
    if verbose:
        print("\nspam.helpers.orientationPlotter.plotSphericalHistogram: Creating the icosphere")
    icoVerts, icoFaces, icoVectors = orientationpy.generateIcosphere(subDiv)
    # Bin the data
    if verbose:
        print("\nspam.helpers.orientationPlotter.plotSphericalHistogram: Binning the data")
    counts = binIcosphere(orientations, icoVectors, verbose=verbose)
    # Now we are ready to plot
    if verbose:
        print("\nspam.helpers.orientationPlotter.plotSphericalHistogram: Plotting")

    # Create the figure
    fig = matplotlib.pyplot.figure()
    ax = fig.add_subplot(projection="3d")
    # ax = fig.gca(projection="3d")

    if color is None:
        cmap = matplotlib.pyplot.cm.viridis_r
    else:
        cmap = color
    norm = matplotlib.pyplot.Normalize(vmin=0, vmax=1)
    if maxVal is None:
        maxVal = numpy.max(counts)

    # Don't do it like this, make empty arrays!
    # points = []
    # connectivityMatrix = []

    # Loop through each of the faces
    for i in range(len(icoFaces)):
        # Get the corresponding radius
        radii = counts[i] / maxVal
        if radii != 0:
            # Get the face
            face = icoFaces[i]
            # Get the vertices
            P1 = numpy.asarray(icoVerts[face[0]])
            P2 = numpy.asarray(icoVerts[face[1]])
            P3 = numpy.asarray(icoVerts[face[2]])
            # Extend the vertices as needed by the radius
            P1 = radii * P1 / numpy.linalg.norm(P1)
            P2 = radii * P2 / numpy.linalg.norm(P2)
            P3 = radii * P3 / numpy.linalg.norm(P3)
            # Combine the vertices
            vertices = numpy.asarray([numpy.array([0, 0, 0]), P1, P2, P3])

            # for vertex in vertices:
            # points.append(vertex)
            # connectivityMatrix.append([len(points)-1, len(points)-2, len(points)-3, len(points)-4])

            # Add the points to the scatter3D
            ax.scatter3D(vertices[:, 0], vertices[:, 1], vertices[:, 2], s=0)
            # Create each face
            face1 = numpy.array([vertices[0], vertices[1], vertices[2]])
            face2 = numpy.array([vertices[0], vertices[1], vertices[3]])
            face3 = numpy.array([vertices[0], vertices[3], vertices[2]])
            face4 = numpy.array([vertices[3], vertices[1], vertices[2]])

            # Plot each face!
            ax.add_collection3d(Poly3DCollection([face1, face2, face3, face4], facecolors=cmap(norm(radii)), linewidths=0.5, edgecolors="k"))

    # Extra parameters for the axis
    ax.set_box_aspect([1, 1, 1])
    matplotlib.pyplot.xlim(-1.1, 1.1)
    matplotlib.pyplot.ylim(-1.1, 1.1)
    ax.set_zlim(-1.1, 1.1)
    ax.view_init(viewAnglesDeg[0], viewAnglesDeg[1])
    # Set the colorbar
    norm = matplotlib.colors.Normalize(vmin=0, vmax=maxVal)
    sm = matplotlib.pyplot.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    matplotlib.pyplot.colorbar(sm, label="Number of vectors in bin")

    hideAxes = False
    if hideAxes:
        ax.xaxis.set_ticklabels([])
        ax.yaxis.set_ticklabels([])
        ax.zaxis.set_ticklabels([])

    else:
        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")
        ax.set_zlabel("Z axis")
        ax.xaxis.set_ticks([-1, 0, 1])
        ax.yaxis.set_ticks([-1, 0, 1])
        ax.zaxis.set_ticks([-1, 0, 1])
        # ax.xaxis.set_ticklabels([-1, 0, 1])
        # ax.yaxis.set_ticklabels([-1, 0, 1])
        # ax.zaxis.set_ticklabels([-1, 0, 1])

    # Remove the ticks labels and lines
    ax = matplotlib.pyplot.gca()
    # for line in ax.xaxis.get_ticklines():
    # line.set_visible(False)
    # for line in ax.yaxis.get_ticklines():
    # line.set_visible(False)
    # for line in ax.zaxis.get_ticklines():
    # line.set_visible(False)
    # Title
    if title is not None:
        ax.set_title(str(title) + "\n")
    matplotlib.pyplot.tight_layout()
    if saveFigPath is not None:
        matplotlib.pyplot.savefig(saveFigPath)
    else:
        matplotlib.pyplot.show()
