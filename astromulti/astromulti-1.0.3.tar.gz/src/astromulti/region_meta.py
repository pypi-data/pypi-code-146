import numpy as np, collections
from astropy import units as u
from astropy.coordinates import SkyCoord
from regions import Regions, PolygonSkyRegion


def get_extent( reg ):
    '''
    Returns the max extent of a sky region (in the given quantity)
    The skyregion must be rectangle/circle/ellipse/polygon
    '''

    if reg.__module__=='regions.shapes.rectangle':
        return np.sqrt( reg.height**2 + reg.width**2 )
    elif reg.__module__=='regions.shapes.circle':
        return reg.radius*2
    elif reg.__module__=='regions.shapes.ellipse':
        return np.max(reg.width,reg.height)
    elif reg.__module__=='regions.shapes.polygon':
        # measure the distances across the vertices
        vertc = reg.vertices
        distances = []
        for i in range(len(vertc)):
            distances.append(vertc[i].separation(vertc))
        # make a numpy array, get its max and units and make a proper quantity
        return distances[0].unit *np.max(np.array(distances).flatten())
    else:
        raise RuntimeError('Region not supported!')
        return


def get_center( reg, mode='minmax' ):
    '''
    Returns the center of a region
    '''

    # first check if it has center, and then if it has vertices
    try:
        return reg.center.galactic
    except:
        vertc = reg.vertices.galactic

    # just calculate mean/median of l and b
    if mode=='median':
        c_l = np.median(vertc.l).value
        c_b = np.median(vertc.b).value
    elif mode=='mean':
        c_l = np.mean(vertc.l).value
        c_b = np.mean(vertc.b).value
    elif mode=='minmax':
        c_l = (np.max(vertc.l)+np.min(vertc.l)) /2
        c_b = (np.max(vertc.b)+np.min(vertc.b)) /2
    else:
        raise RuntimeError('mode must be only either median or mode!')
        return

    return SkyCoord( c_l, c_b, unit=vertc[0].l.unit, frame='galactic' )


def region_dict( regionfile ):
    '''
    give a DS9 region file path, it will return a dictionary with the region labels as keys and the region itself as the key-value.
    Error will be raised if even a single region exists without a label, or if duplicates exist.
    '''

    ds9regs = Regions.read( regionfile )

    labels = []     # not using list comprehension because printing region details is easier this way
    for rg in range(len(ds9regs)):
        try:
            labels.append(ds9regs[rg].meta['label'])
        except:
            print("The following region cannot be appended,")
            print("  likely because no label exists for it.")
            print("Check your DS9 region file!")
            print("file: "+regionfile+"; idx: "+rg)

    duplicates = [ item for item, count in collections.Counter(labels).items() if count > 1 ]
    if not duplicates==[]:
        print(duplicates)
        raise RuntimeError("Duplicates exist! The duplicated labels are printed above for your reference.")

    regdict = {}
    for r1 in ds9regs:
        regdict[r1.meta['label']] = r1

    return regdict


def rot_PolySkyReg( reg, angl ):
    """
    Rotates 'reg' by the given 'angl'
    'reg' must be a PolygonSkyRegion
    'angl' must be an angle quantity (like 10*u.degree)
    """

    # raise error if it is not a polygon
    if type(reg) != PolygonSkyRegion:
        raise TypeError( "Must be PolygonSkyRegion, but it is: " + str(type(reg)) )

    # get center and initialize new vertices l,b arrays
    regcenter = get_center( reg )
    new_vertices_l = []
    new_vertices_b = []

    # iterate over each old vertex and get its corresponding new vertex
    for vertx in reg.vertices.galactic:
        pos_angle = regcenter.position_angle(vertx) + 90*u.degree               # position angle (new direction from the old vertex to new vertex)
        cent2vert = regcenter.separation(vertx)                                 # angular separation from old vertex to center
        n2o_v_sep = np.arctan( np.sin(angl.to(u.radian).value) *
                               np.sin(cent2vert.to(u.radian).value) )           # angular separation from old to new vertex
        new_vertx = vertx.directional_offset_by( pos_angle, n2o_v_sep)          # finally we get the new vertex
        new_vertices_l.append(new_vertx.galactic.l)
        new_vertices_b.append(new_vertx.galactic.b)

    return PolygonSkyRegion(SkyCoord( new_vertices_l, new_vertices_b, frame='galactic' ))


#aaa  = PolygonSkyRegion(SkyCoord( np.array([28.9,28.9,28.6,28.6])*u.degree, np.array([-0.4,-0.5,-0.5,-0.4])*u.degree, frame='galactic' ))
#aaa1 = rot_PolySkyReg( aaa, 30*u.degree )
#aaa2 = rot_PolySkyReg( aaa, -30*u.degree )
#aaa.write('orig.reg',format='ds9',overwrite=True)
#aaa1.write('plus30.reg',format='ds9',overwrite=True)
#aaa2.write('minus30.reg',format='ds9',overwrite=True)





