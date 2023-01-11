# The following module allows for the transformation of files for use and analysis in vasp and other codes such as molcas
# The module will include the transfor from .cif file to poscar file and then poscar to .xyz file 
"""
A module for the transformation of file type for use in vasp and other codes such as molcas
"""
# Imports
import numpy as np
import os
from gemmi import cif

# Functions
def convert_cif(cif_file):
    """
    Converts a .cif file to a POSCAR file for use in vasp.
    KNOWN BUGS
    ----------
    - The program doesnt work for .cif files containig "(number)" in the positions of the atoms and the lattice vectors
    - View the .cif file in a text editor to see if this is the case

    Parameters
    ----------
    cif_file : str 

    Returns
    -------
    POSCAR 
    """

    cif_doc =  cif.read_file(cif_file)
    cif_block = cif_doc.sole_block()
    name = cif_file.strip(".cif")
    # Get the lattice vectors
    a = cif_block.find_value("_cell_length_a")
    b = cif_block.find_value("_cell_length_b")
    c = cif_block.find_value("_cell_length_c")
    a, b, c = float(a), float(b), float(c)
    alpha = cif_block.find_value("_cell_angle_alpha")
    beta = cif_block.find_value("_cell_angle_beta")
    gamma = cif_block.find_value("_cell_angle_gamma")
    alpha, beta, gamma = float(alpha), float(beta), float(gamma)
    alpha, beta, gamma = np.radians(alpha), np.radians(beta), np.radians(gamma)
    # Get the atom positions
    xpos, ypos, zpos = list(cif_block.find_loop("_atom_site_fract_x")), list(cif_block.find_loop("_atom_site_fract_y")), list(cif_block.find_loop("_atom_site_fract_z"))
    # Get the atom labels
    atom_labels = list(cif_block.find_loop("_atom_site_label"))
    # Get the atom types
    atom_types = list(cif_block.find_loop("_atom_site_type_symbol"))
    
    # Transform the lattice vectors and angles into a matix
    a_vector = np.array([a, 0, 0])
    b_vector = np.array([b*np.cos(gamma), b*np.sin(gamma), 0])
    c_vector = np.array([np.cos(beta), c*((np.cos(alpha) - np.cos(beta)*np.cos(gamma))/np.sin(gamma)), c*np.sqrt(1 - np.cos(beta)**2 - ((np.cos(alpha) - np.cos(beta)*np.cos(gamma))/np.sin(gamma))**2)])

    # Create the atom position matirx
    position_matrix = [] 
    for i in zip(xpos, ypos, zpos):
        position = np.array([float(i[0]), float(i[1]), float(i[2])])
        position_matrix.append(position)
    position_matrix = np.array(position_matrix)
    
    # Create a list of tuples containing the atom and the number of that atom (atom, number)
    atom_list = []
    for i in atom_types:
        if i not in atom_list:
            atom_list.append(i)
    atom_list = sorted(atom_list)
    atom_number_list = []
    for i in atom_list:
        atom_number_list.append(atom_types.count(i))
    atom_number_list = tuple(atom_number_list)
    atom_list = tuple(atom_list)
    atom_list = list(zip(atom_list, atom_number_list))

    atom_list_string = ""
    for i in atom_list:
        atom_list_string += i[0] + " "
    atom_number_list_string = ""
    for i in atom_list:
        atom_number_list_string += str(i[1]) + " "

    # Generate the POSCAR file
    with open('POSCAR', 'w') as f:
        f.write(f'''{name}
1.0
        {a_vector[0]} {a_vector[1]} {a_vector[2]}
        {b_vector[0]} {b_vector[1]} {b_vector[2]}
        {c_vector[0]} {c_vector[1]} {c_vector[2]}
{atom_list_string}
  {atom_number_list_string}
Direct
''')
        for i in position_matrix:
            f.write(f"    {i[0]}     {i[1]}      {i[2]}\n")


def convert_xyz():
    """
    Converts a POSCAR file to a .xyz file for use in molcas

    Parameters
    ----------
    None

    Returns
    -------
    .xyz file
    """
    with open('POSCAR','r') as f:
            poscar = []
            for lines in f:
                stripped_lines = lines.strip()
                split_lines = stripped_lines.split()
                poscar.append(split_lines)
    lattice_matrix = np.float_(poscar[2:5])
    frac_coord = np.float_(poscar[8:])
    name = ''.join(poscar[0])
    cart_coord = []
    for i in range(len(frac_coord)):
        cart_coord.append(np.matmul(frac_coord[i],lattice_matrix))
    element = poscar[5]
    element_num = poscar[6]
    element_num = [int(x) for x in element_num]
    cumsum_element = list(np.cumsum(element_num))
    element_list =[]
    for i in range(len(element)):
        element_list.append(f'{element[i]} '*int(element_num[i]))
    for i in range(len(element_list)):
        element_list[i] = ' '.join(element_list[i].split())
    element_list = ' '.join(element_list)
    element_list = element_list.split()

    with open('POSCAR.xyz','w') as f:
        f.write(f'''{len(cart_coord)}
{name}
''')
        for i in range(len(cart_coord)):
            f.write(f'''{element_list[i]}    {float(cart_coord[i][0])}    {float(cart_coord[i][1])}    {float(cart_coord[i][2])}   
''')  

