#!/usr/bin/env python

#=========================================
# Some functions for mpi implementation
# Using mpi4py
# Author: Shunhong Zhang
# Email: szhang2@ustc.edu.cn
# Date: Feb 24, 2020
#==========================================


from __future__ import print_function
try: import mpi4py.MPI as MPI
except: raise ImportError('mpi4py')
import numpy as np

def get_mpi_handles():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    node_name = MPI.Get_processor_name()
    return comm, size, rank, node_name


# free root means that the root process will not
# take over computational tasks, usually
# it will instead serves as a communicator
def assign_task(ntask,size,rank,free_root=False):
    if free_root:
        if rank==0:
            start = last = 0
        else:
            ave, res = divmod(ntask, size-1)
            ntask_local = [ave+1]*res + [ave]*(size-1-res)
            start = np.append(0,np.cumsum(ntask_local)[:-1])[rank-1]
            last = np.cumsum(ntask_local)[rank-1]
    else:
        ave, res = divmod(ntask, size)
        ntask_local = [ave+1]*res + [ave]*(size-res)
        start = np.append(0,np.cumsum(ntask_local)[:-1])[rank]
        last = np.cumsum(ntask_local)[rank]
    return start, last


def pprint(string="", end='', comm=MPI.COMM_WORLD):
    if not comm.Get_rank(): print (string+end)


def get_group_handles(rank_group):
    comm,size,rank,node = get_mpi_handles()
    if rank_group is None:
        group_comm,group_size,group_rank,node = get_mpi_handles()
    else:
        group1 = comm.group.Incl(rank_group)
        group_comm = comm.Create_group(group1)
        if group_comm != MPI.COMM_NULL:
            group_size = group_comm.Get_size()
            group_rank = group_comm.Get_rank()
        else:
            group_size=None
            group_rank=None
    return group_comm,group_size,group_rank


def inter_node_check(comm,node,rank):
    all_nodes = comm.gather(node)
    if rank==0:
        if len(set(all_nodes))>1:
            print ('Multi-node invoked')
            print ('Please make sure that inter-node communication works well')
            print ('Sometimes you need to add the following command to your job-submission script')
            print ('export I_MPI_FABRICS=shm:tcp')


if __name__=='__main__':
    comm, size, rank, node_name = get_mpi_handles()
    pprint ('some functions for mpi parallelization')
    pprint ('running on {0} cores'.format(size))
    comm.barrier()
    print ('Here is rank {0}, node {1}'.format(rank,node_name))
