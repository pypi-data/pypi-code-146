import numpy as np
import scipy as sc
import spiceypy as spy

from radiocc.model import ProcessType


#   Variable  I/O  Description
#   --------  ---  --------------------------------------------------
#   method     I   Computation method.
#   target     I   Name of target body.
#   et         I   Epoch in TDB seconds past J2000 TDB.
#   fixref     I   Body-fixed, body-centered target body frame.
#   abcorr     I   Aberration correction flag.
#   obsrvr     I   Name of observing body.
#   spoint     O   Sub-observer point on the target body.
#   trgepc     O   Sub-observer point epoch.
#   srfvec     O   Vector from observer to sub-observer point.




def long_lat(N_data, pos_MEX, vel_MEX, ET, ET_MEX_Mars,Ref_Frame, FOLDER_TYPE: ProcessType):

##    	    Look up the target body's radii. We'll use these to
##          convert Cartesian to planetographic coordinates. Use
##          the radii to compute the flattening coefficient of
##          the reference ellipsoid.

    radii = spy.bodvrd('Mars', 'RADII', 3)

#Let 're' and 'rp' be, respectively, the equatorial and polar radii of the target.

    re = radii[1][0]

    rp = radii[1][2]

    f = (re-rp)/re

    odist     = np.zeros((N_data,))

    xabsSC    = np.zeros((N_data,))

    spglat_SC = np.zeros((N_data,))

    spglon_SC = np.zeros((N_data,))

    spgalt_SC = np.zeros((N_data,))

    spcrad_SC = np.zeros((N_data,))

    spclon_SC = np.zeros((N_data,))

    spclat_SC = np.zeros((N_data,))

    #Compute sub-observer point using light time (LT) and stellar (S) aberration corrections. Using ellipsoid
    #shape models,"intercept" sub-observer point definitions.

    for i in range(N_data):

        [spoint, trgepc, srfvec] = spy.subpnt('Intercept: ellipsoid', 'Mars', ET_MEX_Mars[i], 'IAU_MARS', 'LT+S', FOLDER_TYPE.name)

	# For target shapes modeled by ellipsoids, the
        # sub-observer point is defined either as the point on
        # the target body that is closest to the observer, or
        # the target surface intercept of the line from the
        # observer to the target's center. The components of `spoint' have units of km and are in Cartesian coordinates.
	#  'trgepc' is expressed as seconds past J2000 TDB.

        odist[i] = np.linalg.norm(srfvec) #Compute the MEX's distance from the "spoint" vector. Using the Frobenius norm.

        xabsSC[i] = np.linalg.norm(spoint) # Compute the distance from the center of Mars of the spoint.

	#Convert the sub-observer point's Cartesian coordinates to planetographic longitude, latitude and altitude.

        [spglon, spglat, spgalt] = spy.recpgr('Mars', spoint, re, f)

        spglon *= 180./sc.pi #Convert radians to degrees.

        spglat *= 180./sc.pi #Convert radians to degrees.

        spglon_SC[i] = spglon

        spglat_SC[i] = spglat

        spgalt_SC[i] = spgalt

	# Convert sub-observer point's Cartesian coordinates to planetocentric radius, longitude, and latitude.
        [spcrad, spclon, spclat] = spy.reclat(spoint)

        spclon *= 180./sc.pi #Convert radians to degrees.

        spclat *= 180./sc.pi #Convert radians to degrees.

        spcrad_SC[i] = spcrad

        spclon_SC[i] = spclon

        spclat_SC[i] = spclat


    pos_MEX_Earth = np.full((N_data,3),np.nan)#np.array([[np.nan for j in range(3)] for i in range( N_data )], dtype = float)

    for i in range(N_data):

	#Return the state (position and velocity) of MEX relative to EARTH, optionally corrected for light time (planetary aberration) and stellar  aberration.

	#[position, lt ] = spy.spkezr(target, time, reference_frame, aberration_correction, observing_body)
        [ position, lt ] = spy.spkezr( FOLDER_TYPE.name, ET_MEX_Mars[i], 'IAU_MARS', 'none', 'EARTH' )

	#lt is the one-way light time between the observer and target in seconds.

        pos_MEX_Earth[i] = position[:3]

	# Take the 3 first components of position corresponding to the -x -y and -z of the target's position; the last three components form the corresponding velocity vector. They are expressed with respect to the MARS's frame.

    ray_MEX_Earth = np.full((N_data,3),np.nan)#np.array([[np.nan for j in range(3)] for i in range( N_data )], dtype = float)

    for i in range(N_data):

        ray_MEX_Earth[i] = -pos_MEX_Earth[i]/np.linalg.norm(pos_MEX_Earth)

    A = radii[1][0] # Length of ellipsoid’s semi-axis in the x direction

    B = radii[1][1] # Length of ellipsoid’s semi-axis in the y direction

    C = radii[1][2] # Length of ellipsoid’s semi-axis in the z direction

    pnear_ray = np.full((N_data,3),np.nan)#np.array([[np.nan for j in range(3)] for i in range( N_data )], dtype = float)

    dist_ray = np.zeros((N_data,))


    for i in range(N_data):

        LINEPT = pos_MEX[i] *1e-3

        LINEDR = ray_MEX_Earth[i]


        [pnear, dist] = spy.npedln(A, B, C, LINEPT, LINEDR)

        pnear_ray[i] = pnear # point on the ellipsoid that is closest to the line if the line doesn't intersect the ellipsoid.

        dist_ray[i] = dist # distance of the line from the ellipsoid. Minimum distance between any point on the line and any point on the ellipsoid

    d_lon    = np.zeros((N_data,))

    d_lat    = np.zeros((N_data,))

    d_radius = np.zeros((N_data,))

    local_solar_time = []

    SZA = np.zeros((N_data,))

    d_phase = np.zeros((N_data,))

    for i in range(N_data):

	# Convert from rectangular coordinates to latitudinal coordinates (radians).

        [radius, lon, lat] = spy.reclat(pnear_ray[i])

        lon *= 180./sc.pi

        lat *= 180./sc.pi

        d_lon [i] = lon

        d_lat[i] = lat

        d_radius[i] = radius

	# Given an ephemeris epoch, compute the local solar time for an object on the surface of a body at a specified longitude.

        [hr, minute, secend, timee, ampm] = spy.et2lst( ET_MEX_Mars[i], 499, lon, 'PLANETOCENTRIC')

        local_solar_time.append(timee)

# Find the illumination angles at a specified surface point of a target body.

        [phase, solar, emission] = spy.illum('Mars', ET_MEX_Mars[i], 'None', FOLDER_TYPE.name, pnear_ray[i])

        d_phase[i] = phase

        sza = solar * 180./sc.pi

        SZA[i] = sza

    ang_MEX_LoS = np.zeros((N_data,))

    for i in range(N_data):

        vsep = spy.vsep(vel_MEX[i],pos_MEX_Earth[i])

        ang_MEX_LoS[i] = vsep


    dist_Mars_Sun = np.zeros((N_data,))

    for i in range(N_data):

        [ position, lt ] = spy.spkpos( 'Mars', ET[i], 'IAU_MARS', 'none', 'Sun' )

        dist_Mars_Sun[i] = np.linalg.norm(position)*6.68459e-9 # why this factor, (km)-(AU)? Seems so...


    #print('')
    #print('')
    #print('\tR6: Done')
    #print('')
    #print('')

    return d_lat, d_lon, dist_Mars_Sun, spclon_SC, spclat_SC, re, f
