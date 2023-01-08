#!/usr/bin/env python


try: from ovf import ovf
except: raise Exception ('Cannot import ovf library')
import numpy as np
from asd.utility.ovf_tools import *
from asd.core.random_vectors import *

nx = 3
ny = 4
nz = 2

# which loop order is favored?
shape = (nz,ny,nx,3)
shape = (nx,ny,nz,3)

fil_ovf = 'ovf_for_test.ovf'


if __name__=='__main__':
    print ('Making and writing OVF')
    with ovf.ovf_file(fil_ovf) as ovf_file:
        # Write one segment
        segment = ovf.ovf_segment(title = 'SEG 1',comment='The first segment',
        n_cells=[nx,ny,nz],valuedim=3,meshunits='Angstrom',valuelabels='Sx Sy Sz',valueunits='1 1 1')
        data1 = np.random.rand(*tuple(shape))
        if ovf_file.write_segment(segment, data1) != -1:
            print("write_segment failed: ", ovf_file.get_latest_message())

        # Add a second segment to the same file
        segment = ovf.ovf_segment(title = 'SEG 2',comment='The second segment',
        n_cells=[nx,ny,nz],valuedim=3,meshunits='Angstrom',valuelabels='Sx Sy Sz',valueunits='1 1 1')
        data2 = np.random.rand(*tuple(shape))
        if ovf_file.append_segment(segment, data2) != -1:
            print("append_segment failed: ", ovf_file.get_latest_message())


    # Parsing OVF
    datas = [data1,data2]
    with ovf.ovf_file(fil_ovf) as ovf_file:
        print ('{} segments found'.format(ovf_file.n_segments))
        for iseg in range(ovf_file.n_segments):
            print ('\n{0}\nReading segment {1}\n{0}\n'.format('-'*30,iseg))
            segment = ovf.ovf_segment()
            ovf_file.read_segment_header(iseg,segment)

            print ('Address',segment)
            print (segment.title)
            print (segment.comment)
            print (segment.valuedim)
            print (segment.valueunits)
            print (segment.valuelabels)
            print (segment.meshtype)
            print (segment.meshunits)
            print (segment.pointcount)
            print (segment.origin[:])
            print (segment.N)
            print (segment.n_cells[:])
            print (segment.bounds_min[:])
            print (segment.bounds_max[:])
            print (segment.step_size[:])

            params = props(segment)
            #print ('\nHeader presented as a dictionary')
            #print ('\n'.join(['Key = {}, value = {}'.format(key,value) for key,value in params.items()])+'\n')

            # read the segment data and pass it to data
            ovf_file.read_segment_data(iseg,segment,datas[iseg])
            print ('Data shape: {}'.format(datas[iseg].shape))

    print ('Testing ovf_tools')
    params,spins = parse_ovf_1(fil_ovf)
    flag = np.allclose(spins[0],data1.reshape(-1,3))
    print (flag)
    flag = np.allclose(spins[1],data2.reshape(-1,3))
    print (flag)
