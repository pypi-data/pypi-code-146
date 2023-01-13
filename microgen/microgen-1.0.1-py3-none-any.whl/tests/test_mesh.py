from microgen import Rve, mesh, meshPeriodic, Box, Phase

import cadquery as cq
import numpy as np

import pytest

import vtk
from vtk.util.numpy_support import vtk_to_numpy

def mesh_to_numpy(filename: str):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()

    nodes_vtk_array = reader.GetOutput().GetPoints().GetData()
    return vtk_to_numpy(nodes_vtk_array)


def is_periodic(crd: np.ndarray, tol: float=1e-8, dim: int=3):
    
    # bounding box
    xmax = np.max(crd[:, 0]) ; xmin = np.min(crd[:, 0])
    ymax = np.max(crd[:, 1]) ; ymin = np.min(crd[:, 1])
    if dim == 3:                        
        zmax = np.max(crd[:, 2]) ; zmin = np.min(crd[:, 2])
    
    
    # extract face nodes
    left  = np.where(np.abs(crd[:, 0] - xmin) < tol)[0]
    right = np.where(np.abs(crd[:, 0] - xmax) < tol)[0]
    
    if dim > 1:
        bottom = np.where(np.abs(crd[:, 1] - ymin) < tol)[0]
        top    = np.where(np.abs(crd[:, 1] - ymax) < tol)[0]
    
    if dim > 2: #or dim == 3 
        back  = np.where(np.abs(crd[:, 2] - zmin) < tol)[0]
        front = np.where(np.abs(crd[:, 2] - zmax) < tol)[0] 
        
        
    # sort adjacent faces to ensure node correspondance
    if crd.shape[1] == 2: #2D mesh
        left  = left [np.argsort(crd[left , 1])]
        right = right[np.argsort(crd[right, 1])]
        if dim > 1:
            bottom = bottom[np.argsort(crd[bottom, 0])]
            top    = top   [np.argsort(crd[top   , 0])]
        
    elif crd.shape[1] > 2: 
        decimal_round = int(-np.log10(tol) - 1)
        left  = left [np.lexsort((crd[left , 1], crd[left , 2].round(decimal_round)))]
        right = right[np.lexsort((crd[right, 1], crd[right, 2].round(decimal_round)))]
        if dim > 1:
            bottom = bottom[np.lexsort((crd[bottom, 0], crd[bottom, 2].round(decimal_round)))]
            top    = top   [np.lexsort((crd[top   , 0], crd[top   , 2].round(decimal_round)))]
        if dim > 2: 
            back  = back [np.lexsort((crd[back, 0], crd[back, 1].round(decimal_round)))]
            front = front[np.lexsort((crd[front, 0], crd[front, 1].round(decimal_round)))]
    
    #==========================
    # test if mesh is periodic:
    #==========================
    
    # test if same number of nodes in adjacent faces
    if len(left) != len(right):
        return False
    if dim > 1 and len(bottom) != len(top):
        return False
    if dim > 2 and (len(back) != len(front)):
        return False
    
    # check nodes position
    if (crd[right, 1:] - crd[left, 1:] > tol).any():
        return False
    if dim > 1 and (crd[top, ::2] - crd[bottom, ::2] > tol).any():
        return False
    if dim > 2 and (crd[front, :2] - crd[back, :2] > tol).any():
        return False
    
    return True

def test_periodic_mesh():
    dim_x = 2
    dim_y = 1
    dim_z = 4

    mesh_size = 0.1
    mesh_order = 1

    dim=1

    box = Box(center=(5, 2, -5),
              dim_x=dim_x, dim_y=dim_y, dim_z=dim_z)
    shape = box.generate()
    shape.exportStep(fileName="box.step")

    mesh(mesh_file="box.step", 
         listPhases=[Phase(shape)], 
         size=mesh_size, 
         order=mesh_order, 
         output_file="mesh.vtk")

    numpy_mesh = mesh_to_numpy("mesh.vtk")
    print(is_periodic(crd=numpy_mesh, dim=dim))

    meshPeriodic(mesh_file="box.step",
                 rve=Rve(dim_x, dim_y, dim_z), 
                 listPhases=[Phase(shape)], 
                 size=mesh_size, 
                 order=mesh_order, 
                 output_file="periodic_mesh.vtk")

    
    numpy_periodic_mesh = mesh_to_numpy("periodic_mesh.vtk")
    print(is_periodic(crd=numpy_periodic_mesh, tol=1.e-8, dim=dim))

if __name__ == "__main__":
    test_periodic_mesh()


