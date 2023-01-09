
# if egress: distance increasing, from surface to atmosphere
# if ingress: distance decreasing, from atmosphere to surface

from pudb import set_trace as bp  # noqa:F401

import radiocc


def occultation_info(planet,ground,epoch,frame,sc,DATA_ID,DATA_DIR,Threshold_Surface,EPHE_DIR):
    import os

    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import spiceypy
    from mpl_toolkits.mplot3d import Axes3D
    from PIL import Image
    
    ang = np.zeros(len(epoch))
    utc = []
    emissn= np.zeros(len(epoch))
    phase = np.zeros(len(epoch)) 
    lat_centric = np.zeros(len(epoch))
    lon_centric = np.zeros(len(epoch))  
    ssl_lat = np.zeros(len(epoch))
    ssl_lon = np.zeros(len(epoch))
    MARS_LS = np.zeros(len(epoch))
    pnear_radius = np.zeros(len(epoch))
    v_mnp_sp = np.zeros((len(epoch),3))
    dist_planet_sc = np.zeros(len(epoch))
    ampm = []
    hr_ang = []
    solar  = np.zeros(len(epoch))
    vsep   = np.zeros(len(epoch))
    ssc_lon = np.zeros(len(epoch))
    ssc_lat = np.zeros(len(epoch))
    distance1 = np.zeros(len(epoch))
    distance = np.zeros(len(epoch))
    
    stop_index = -999      
    for index in range(len(epoch)):
        
        # ground  = NAIF_GS
        # planet  = NAIF_Planet
        # sc      = NAIF_SC
        # epoch = UTC  [-1]
        # frame = Ref_Frame  
        frame    = 'IAU_MARS'  #'MARSIAU ' #'J2000' IAU_MARS
        abcorr   = 'CN+S' # 'LT+S'
        
       # Convert time to et     
        et = epoch[index]
        #et = spiceypy.spiceypy.utc2et(epoch[index])

        
        #returns the position of a target body relative  to an observing body     
        [pos , ltime] = spiceypy.spiceypy.spkpos( 'Sun', et,frame, abcorr, sc )
        
        Dist_sun_MVN =np.linalg.norm(pos)
            
        
        #returns the position of a target body relative  to an observing body
        [pos , ltime] = spiceypy.spiceypy.spkpos( 'Earth', et,frame, abcorr, sc )

        Dist_MVN_earth=np.linalg.norm(pos)
       
       #Compute the Ls (Solar longitude)
        MARS_LS[index] = spiceypy.spiceypy.lspcn(planet , et, 'none' )*spiceypy.spiceypy.dpr()
        
        
        # saisons 0 ==> PRINTEMPS hemisphere nord, 90 ==> ETE ..... 
       
        
         # get spacecraft position with respect to Earth in IAU_PLANET
        [sp_pos_earth_iau_planet , ltime2] = spiceypy.spiceypy.spkpos(sc, et,
                                           frame, abcorr, ground) 

        
        # get spacecraft position with respect to Planet in IAU_PLANET. spiceypy.spiceypy.spkpos returns the position of a target body relative to an observing body, optionally corrected for light t (planetary aberration) and stellar aberration.
        et = et-ltime2    
        [sp_pos_planet_iau, ltime] = spiceypy.spiceypy.spkpos(sc, et, 
                                           frame, 'NONE', planet) 
                                       
        
               
        ray = spiceypy.spiceypy.unorm(sp_pos_earth_iau_planet)  # direct ray path without perturbations bw sc and earth

        #ray = spiceypy.spiceypy.unorm(sp_pos_planet_iau)
        #ray2 = spiceypy.spiceypy.unorm(sp_pos_earth_iau_planet2)
        # print(ray,ray2)
        for i in range(len(ray[0])) : ray[0][i] = -ray[0][i]
        dist_planet_sc[index]=np.linalg.norm(sp_pos_earth_iau_planet)
        
        # Get ellipsoid radii in body fixed reference frame (IAU_PLANET)
    
        radii = spiceypy.spiceypy.bodvar(int(planet), 'RADII', 3 ) # MARS RADIUS
                                               
        # Get ray direction needed to compute the planet nearest point: that's the line joining the spacecraft and the Earth center
               
        
       # Get nearest point on ellipsoid to the ray  
       # NOTE: dist is here the distance between the line and the MNP point. 
          
        [ pnear, dist ] = spiceypy.spiceypy.npedln(radii[0], radii[1], radii[2], sp_pos_planet_iau, ray[0])

        # If geometrical occultation detected get the moment at which it occurs : 
        if np.logical_and(dist==0,stop_index==-999)==True:
            stop_index = index-1
            break
        # If no geometrical occultation detected then take the last index : 
        
        if np.logical_and(index==len(epoch)-1,stop_index==-999)==True:
            stop_index = index
        
        
        # print(np.sqrt(sp_pos_planet_iau[0]**2+sp_pos_planet_iau[1]**2+sp_pos_planet_iau[2]**2))
        # print(radii)
         
        distance1[index] = dist
        distance = distance1*1e3 + Threshold_Surface
        #print(distance)


       # get Earth position with respect to Sun in J2000
        [Sun_Earth_j2000 , ltime] = spiceypy.spiceypy.spkpos( 'Sun', et,
                                           'J2000', abcorr, 'Earth')  
       
        sunEarthdir =  spiceypy.spiceypy.unorm(Sun_Earth_j2000) 
        #for i in range(len(sunEarthdir[0])-1) : sunEarthdir[0][i] = -sunEarthdir[0][i]
    
        # get S.c position with respect to Sun in J2000
        [earth_sc_j2000 , ltime] = spiceypy.spiceypy.spkpos( 'Earth', et,
                                           'J2000', abcorr, sc)  
       
        Earthspdir =  spiceypy.spiceypy.unorm(earth_sc_j2000) 
       
       
       #angle between SUN-Erath and S/C 
       
        vsep[index] = spiceypy.spiceypy.vsep(sunEarthdir[0], Earthspdir[0])*spiceypy.spiceypy.dpr()
          



        #longitude_sol[index] = pnear
        # approximation impact parameter 
        #[ pnear, dist ] = spiceypy.spiceypy.npedln( rr, rr, rr, sp_pos_planet_iau, ray) ##circular

 
       
       # Compute the lat/lon of the Planet nearest point 
       #spiceypy.spiceypy.recgeo converts rectangular coordinates to geodetic coordinates.
       #spiceypy.spiceypy.reclat converts rectangular (Cartesian) coordinates to Planetocentric / latitudinal coordinates. \
       #All coordinates are expressed as double precision values.
        [pnear_radius[index], longitude, latitude] = spiceypy.spiceypy.reclat(pnear) 
        
        flat = (radii[0] - radii[2])/radii[0]
        [lon, lat, alt] = spiceypy.spiceypy.recgeo(pnear, radii[1], flat)
          
        lon_centric[index]  = longitude * spiceypy.spiceypy.dpr()
        lat_centric[index]   = latitude  * spiceypy.spiceypy.dpr()
        
        lon_geodetic=lon*spiceypy.spiceypy.dpr()
        lat_geodetic=lat*spiceypy.spiceypy.dpr()
        
        if lon_centric[index] <0 :
            lon_centric[index] =360+lon_centric[index] 
        
        if lon_geodetic<0 :
            lon_geodetic=360+lon_geodetic
       
      
      # Compute illumination conditions at planet nearest point
      
        [ phase[index], solar[index], emissn[index]] = spiceypy.spiceypy.illum( planet, et, 'NONE',
                                                   sc, pnear)
    
        #
        # Convert the et value to UTC for human comprehension.
        #
        utc1    = spiceypy.spiceypy.et2utc( et, 'C', 3 )
        utc=np.append(utc,utc1)
        phase[index]  = phase[index]  * spiceypy.spiceypy.dpr()
        solar[index]  = solar[index]  * spiceypy.spiceypy.dpr()
        emissn[index] = emissn[index] * spiceypy.spiceypy.dpr()
          
     
         # Compute the local time from longitude of planet nearest point
         
        [hr, minu, sec, loctime, ampm1] = spiceypy.spiceypy.et2lst( et,   \
                                                      int(planet),  \
                                                      lon_centric[index]/spiceypy.spiceypy.dpr(),'PLANETOCENTRIC')  #'PLANETOGRAPHIC')
        
        ampm = np.append(ampm,ampm1)
        hr_ang1 = hr + minu/60. + sec/3600.
        hr_ang = np.append(hr_ang,hr_ang1)  
        
        #get spacecraft distance to mars nearest point (mnp_dist)
        
        # dist2mnp = spiceypy.spiceypy.unorm(pnear - sp_pos_planet_iau)
             
       
        # mnp_dist = dist2mnp
        # mnp_ls = MARS_LS
        # mnp_sza = solar[index]
        # mnp_phase = phase
        # mnp_loctime = loctime
        # mnp_hour_ang = hr_ang[index]
        
        
        # mnp_lon = longitude  
        # mnp_lat = latitude
        
        
           #Get sub-solar information
           
        [spoint, trgepc, srfvec] = spiceypy.spiceypy.subslr('Near point: ellipsoid', planet, et, frame, 'none', sc)
       
                          
        [ssl_radius, ssl_lon[index], ssl_lat[index]] = spiceypy.spiceypy.reclat(spoint)   #Planetocentric 
        ssl_lon[index]                    = ssl_lon[index] * spiceypy.spiceypy.dpr()
        ssl_lat[index]                    = ssl_lat[index]  * spiceypy.spiceypy.dpr()
    
        if  ssl_lon[index] <0 :
            ssl_lon[index]  =360+ ssl_lon[index]
           
                          
        #Get Spacecraft sub-point information
        
       
        [ssp_pos, ssc_alt] = spiceypy.spiceypy.subpt( 'near point', planet, et, 'none', sc)      
        
        #Convert sub-solar point's rectangular coordinates to
        # planetocentriic  longitude, latitude and altitude. Convert radians
       # to degrees.
           
        [ssc_radius, ssc_lon[index], ssc_lat[index]] = spiceypy.spiceypy.reclat(ssp_pos)   #Planetocentric 
        ssc_lon[index]                    = ssc_lon[index] * spiceypy.spiceypy.dpr()
        ssc_lat[index]                  = ssc_lat[index]  * spiceypy.spiceypy.dpr()
        
        #fprintf( 'Spacecraft sub-point logitude: #s\n: ', ssc_lon[index] )
        #fprintf( 'Spacecraft sub-point latitude: #s\n: ', ssc_lat[index] )
       
       
        #Get angular separation between line-of-sight (ray) and SUN at et
        
        #get SC-SUN direction
       
        [sp_pos_sun , ltime] = spiceypy.spiceypy.spkpos( sc, et,
                                            frame, abcorr, 'SUN')  
                                        
        #sun_dir = spiceypy.spiceypy.unorm(-sp_pos_sun)
       #get angle between +X (ray) and sun_dir
       
        # ang_los_sun = spiceypy.spiceypy.vsep(sun_dir[0], ray[0])* spiceypy.spiceypy.dpr()
           
        
        #Transform these vectors in J2000
       
        
        rotate  = spiceypy.spiceypy.pxform( frame , 'J2000', et )
      
        sp_x_j2000 = rotate.dot(ray[0])
         
         
        #pole = reshape(rotate(:,3,:), 3,[] )
           
          # Get the RADEC coordinates of these vectors
          
          
        [radius, ra, dec] = spiceypy.spiceypy.recrad(sp_x_j2000)
       
        ra  = ra * spiceypy.spiceypy.dpr()
        dec = dec * spiceypy.spiceypy.dpr()
        sp_x_j2000_radec=[]
        sp_x_j2000_radec.append(ra)
        sp_x_j2000_radec.append(dec)
       
        
       
        #Finally, very important: test whether this occultation
        #is a true one: we need to have the MNP point between
        #the spacecraft and the Earth. The case were the spacecraft
        #is between the MNP and the EARTH (no occultation) is
        #not rejected at the efinder level, because it uses
        #only the distance of the Earth/spacecraft line to Mars surface
        #as a criterion
        
        # We really have an occultation only if the MNP is located
            #'between' the Earth  and the spacecraft
            
        #get vector MNP-sp
        #sp_pos_iau = pos_mars
        
        [sp_pos_planet_iau , ltime] = spiceypy.spiceypy.spkpos( sc, et, 
                                            frame, abcorr, planet)  
                                        
         
        [earth_pos_planet_iau, ltime] = spiceypy.spiceypy.spkpos( ground, et,
                                          frame, abcorr, planet)  
      
     
      #get vector MNP-sp
        v_mnp_sp[index]   = -pnear + sp_pos_planet_iau
      
      #get vector MNP-Earth
      
        v_mnp_earth   = -pnear + earth_pos_planet_iau
      
      #get angular separation between MNP-sp and MNP-sun
      # for genuine occultations ang ~ 180 deg.
      #we have to reject the cases where ang ~ 0 deg
      #(here we take 5 deg for the limit, but
      #ang is of the order of 0.01 or 179.9)
        ang[index] = spiceypy.spiceypy.vsep (v_mnp_sp[index], v_mnp_earth) * spiceypy.spiceypy.dpr()
        
    print(f"check sphere {pnear} {longitude * 180/np.pi} {latitude * 180/np.pi} {solar[stop_index]}")
    
    ################### FICHIER INFO_MVN......
                
    FILE_OUT = 'INFO_'+DATA_ID+'.txt'
    output = []
    
    
    output.append("Angular separation between MNP-sp and MNP-sun: %s" %(ang[stop_index]))
    
    output.append('UTC                       : %s' % utc[stop_index])

    #output.append('Epoch          : %s' %epoch)
    
    output.append('MAVEN Sun Distance : %f' %Dist_sun_MVN)
    
    output.append('MAVEN EARTH Distance : %f'   %Dist_MVN_earth)
     
    output.append( 'Emission angle       [deg]: %f' %emissn[stop_index])
    
    output.append( 'Phase angle          [deg]: %f' %phase[stop_index]  )
    
    output.append( 'Lat geocentric       [deg]: %f' %lat_centric[stop_index]  )
    
    output.append( 'Lon geocentric       [deg]: %f' %lon_centric[stop_index] )
    
   
    output.append( 'Sub-Solar Latitude   [deg]: %f' %ssl_lat[stop_index] )
    
    output.append( 'Sub-Solar Longitude  [deg]: %f' %ssl_lon[stop_index] )
    
    
    
    output.append( 'Ls                   [deg]: %f' %MARS_LS[stop_index] )
    
    
    output.append( 'Radius                [km]: %f' %pnear_radius[stop_index] )
    
    output.append( 'S/C to Limb Dist      [km]: %f'   %np.linalg.norm(v_mnp_sp[stop_index]))
    
    output.append( 'S/C to G/S Dist  [10^6 km]: %f' %(dist_planet_sc[stop_index]*1E-6))
    
    output.append( 'local solar time          : %s' %ampm[stop_index] )
    
    output.append( 'local hour angle      [hr]:  %s' %hr_ang[stop_index] )
    
    output.append( 'Solar Zenith angle    [deg]: %f' %solar[stop_index]  )

    output.append( 'Sun-Earth-S/C-Angle   [deg]: %f' %vsep[stop_index]   )
    
    output.append( 'S/C sub-point lon  : %f' %ssc_lon[stop_index] )
   
    output.append( 'S/C sub-point lat  : %f' %ssc_lat[stop_index] )
   
    np.savetxt(EPHE_DIR+'/'+FILE_OUT,output,fmt="%s")
   
    """
    path  = DATA_DIR + '/INFORMATION/mars_magnetism_scale.png'
    path2 = EPHE_DIR + '/trajectory.png'
    
    
    image = Image.open(path)
    fig, ax = plt.subplots()
    ax.imshow(image, extent=(0,360,-90,90))
    ax.set_xlabel("Longitude E [°]")
    ax.set_ylabel("Latitude N [°]")
    x = lon_centric[0:stop_index]
    y = lat_centric[0:stop_index]
    plt.scatter(x[0], y[0], label = 'Start',c='g',s=4,zorder=1)
    plt.scatter(x[-1], y[-1], c='r',s=4, label = 'End',zorder=2)
    plt.plot(x,y,label='Data Trajectory',c='k',zorder=3)

    dimx_box = 60
    dimy_box = 20
    
    if x[0] < 180 : xtext0 = x[0]+ 1*dimx_box
    else : xtext0 = x[0]- 1*dimx_box
    
    if y[0] < 0 : ytext0 = y[0]+ 1*dimy_box
    else : ytext0 = y[0]-1*dimy_box
    
    if x[-1] < 180 : xtext1 = x[-1]+1*dimx_box
    else : xtext1 = x[-1]-1*dimx_box
    
    if y[-1] < 0 : ytext1 = y[-1]+dimy_box
    else : ytext1 = y[-1]-dimy_box

    if xtext0<xtext1:

        if xtext0+1/2*dimx_box > xtext1 - 1/2*dimx_box:
            ecart = abs(xtext0+1/2*dimx_box-(xtext1-1/2*dimx_box))
            if xtext0-ecart > 0 :
                xtext0= xtext0-ecart+5
            else : 
                xtext1 = xtext1+ecart+5
        
        if ytext0+1/2*dimy_box > ytext1 - 1/2*dimy_box:
            ecart = abs(ytext0+1/2*dimy_box-(ytext1-1/2*dimy_box))
            if ytext0-ecart > 0 :
                ytext0=ytext0-ecart+5
            else : 
                ytext1 = ytext1+ecart+5
        
    else :         

        if xtext1+1/2*dimx_box > xtext0 - 1/2*dimx_box:
            ecart = abs(xtext1+1/2*dimx_box-(xtext0-1/2*dimx_box))
            if xtext0-ecart > 0 :
                xtext1= xtext1-ecart+5
            else : 
                xtext0 = xtext0+ecart+5
        
        if ytext1+1/2*dimy_box > ytext0 - 1/2*dimy_box:
            ecart = abs(ytext1+1/2*dimy_box-(ytext0-1/2*dimy_box))
            if ytext1-ecart > 0 :
                ytext1=ytext1-ecart+5
            else : 
                ytext0 = ytext0+ecart+5
        
    ax.annotate('SZ=%0.2f'%solar[0],
            xy=(x[0], y[0]),
            xytext=(xtext0,ytext0),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0',color='k'),
            ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.5),
            color = 'k')
    
    ax.annotate('SZ=%0.2f'%solar[stop_index],
            xy=(x[-1], y[-1]),
            xytext=(xtext1,ytext1),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0',color='k'),
            ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.5),
            color = 'k')
    
    plt.legend(prop={'size': 4})    
    plt.savefig(path2,dpi=200)
    plt.close()
    

    """
    if distance[1] - distance[0] > 0:
        DATA_TYPE = radiocc.model.RadioDataType.EGRESS
    else:
        DATA_TYPE = radiocc.model.RadioDataType.INGRESS

    return distance, DATA_TYPE

 #Profile file name                                  :  "M65RSR0L04_AIX_041391512_05.TAB"
 #Start time                                   [GRT] :  2004-05-18T15:26:42.558
 #Stop time                                    [GRT] :  2004-05-18T15:27:05.598
 #Measurement time (lowest sample)      [GRT - OWLT] :  2004-05-18T15:08:04.584
 #Orbit Number                                       :        414
 #DSN antenna number                                 :         65
 #Ray path direction of geometrical OCC point  [deg] :      81.42
 #Angle from Diametric of geom. OCC point      [deg] :     151.50
 #Latitude (lowest sample)                     [deg] :      52.51
 #Longitude (lowest sample)                    [deg] :     271.95
# Sub-Solar Latitude (lowest sample)           [deg] :      14.15
# Sub-Solar Longitude (lowest sample)          [deg] :     196.66
# Solar Longitude                              [deg] :      35.07
# MOLA Radius (lowest sample)                   [km] :    3383.14
# MOLA Areoid (lowest sample)                   [km] :    3384.90
# Radius (lowest sample)                        [km] :    3384.41
# Sigma Radius (lowest sample)                  [km] :    -999.99
# Pressure (lowest sample)                      [Pa] :     623.12
# Sigma Pressure (lowest sample)                [Pa] :       0.65
# Temperature (lowest sample)                    [K] :     225.33
# Sigma Temperature (lowest sample)              [K] :       0.15
# Upper Boundary Condition for T (low)           [K] :     130.00
# Upper Boundary Condition for T (medium)        [K] :     165.00
# Upper Boundary Condition for T (high)          [K] :     200.00
# S/C to Limb Distance (lowest sample)          [km] :      7681.
# S/C to G/S Distance (lowest sample)     [*10^6 km] : 342.382231
# Local True Solar Time (lowest sample)      [hours] :      17.02
# Solar Zenith Angle (lowest sample)           [deg] :      69.88
# Sun-Earth-S/C-Angle (lowest sample)          [deg] :      39.15
# G/S Elevation Angle (lowest sample)          [deg] :      73.92']
   
