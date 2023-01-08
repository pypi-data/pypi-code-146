#!/usr/bin/env python

import asd.mpi.mpi_tools as mt
import mpi4py.MPI as MPI
import numpy


rank_group = range(4,7)
comm,size,rank,node = mt.get_mpi_handles()
group_comm,group_size,group_rank = mt.get_group_handles(rank_group)

if group_rank==0:
    print ('Info from rank {}, {} ranks working\n'.format(rank,group_size))
comm.barrier()
fmt = 'Global rank = {}, local rank = {}, empty comm : {}'
print (fmt.format(rank,group_rank,group_comm==MPI.COMM_NULL))
