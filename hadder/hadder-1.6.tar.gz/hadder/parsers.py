# Copyright 2022 Dechin Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
from .constants import resdict, atom_types
from .constants import atom14_order_dict


atom_order = {atom_type: i for i, atom_type in enumerate(atom_types)}
atom_type_num = len(atom_types)  # := 37.


def read_pdb(pdb_name, ignoreh=False):
    """Read a pdb file and return atom information with numpy array format.
    Args:
        pdb_name(str): The pdb file name, absolute path is suggested.
    Returns:
        atom_names(list): 1-dimension list contain all atom names in each residue.
        res_names(list): 1-dimension list of all residue names.
        res_ids(numpy.int32): Unique id for each residue names.
        crds(list): The list format of coordinates.
        res_pointer(numpy.int32): The pointer where the residue starts.
        flatten_atoms(numpy.str_): The flatten atom names.
        flatten_crds(numpy.float32): The numpy array format of coordinates.
        init_res_names(list): The residue name information of each atom.
        init_res_ids(list): The residue id of each atom.
    """
    with open(pdb_name, 'r') as pdb:
        lines = pdb.readlines()
    atom_names = []
    atom_group = []
    res_names = []
    res_ids = []
    init_res_names = []
    init_res_ids = []
    crds = []
    crd_group = []
    res_pointer = []
    flatten_atoms = []
    flatten_crds = []
    atom14_positions = []
    atom14_atom_exists = []
    residx_atom14_to_atom37 = []
    for index, line in enumerate(lines):
        if 'END' in line or 'TER' in line:
            atom_names.append(atom_group)
            crds.append(crd_group)
            atom14_positions.append(atom_pos)
            break
        if not line.startswith('ATOM'):
            continue
        atom_name = line[12:16].strip()
        if ignoreh and atom_name.startswith('H'):
            continue
        res_name = line[17:20].strip()
        res_id = int(line[22:26].strip())
        crd = [float(line[30:38]),
               float(line[38:46]),
               float(line[46:54])]
        pointer = int(line[6:11].strip()) - 1
        flatten_atoms.append(atom_name)
        flatten_crds.append(crd)
        init_res_names.append(res_name)
        init_res_ids.append(res_id)
        if res_ids == []:
            res_ids.append(res_id)
            res_names.append(res_name)
            atom_group.append(atom_name)
            crd_group.append(crd)
            res_pointer.append(0)
            atom_pos = np.zeros((14, 3))
            if not atom_name.startswith('H') and atom_name != 'OXT':
                atom_pos[atom14_order_dict[res_name]
                         [atom_name]] = np.array(crd)
        elif res_id != res_ids[-1]:
            atom14_positions.append(atom_pos)
            atom_pos = np.zeros((14, 3))
            if not atom_name.startswith('H') and atom_name != 'OXT':
                atom_pos[atom14_order_dict[res_name]
                         [atom_name]] = np.array(crd)
            atom_names.append(atom_group)
            crds.append(crd_group)
            atom_group = []
            crd_group = []
            res_ids.append(res_id)
            res_names.append(res_name)
            atom_group.append(atom_name)
            crd_group.append(crd)
            res_pointer.append(pointer)
        else:
            atom_group.append(atom_name)
            crd_group.append(crd)
            if not atom_name.startswith('H') and atom_name != 'OXT':
                atom_pos[atom14_order_dict[res_name]
                         [atom_name]] = np.array(crd)
        if index == len(lines) - 1:
            atom_names.append(atom_group)
            crds.append(crd_group)
            atom14_positions.append(atom_pos)
    atom_names = atom_names
    res_names = res_names
    res_ids = np.array(res_ids, np.int32)
    crds = crds
    flatten_atoms = np.array(flatten_atoms, np.str_)
    flatten_crds = np.array(flatten_crds, np.float32)
    init_res_names = np.array(init_res_names)
    init_res_ids = np.array(init_res_ids, np.int32)
    res_pointer = np.array(res_pointer, np.int32)
    # Violation loss parameters
    residue_index = np.arange(res_pointer.shape[0])
    aatype = np.zeros_like(residue_index)
    for i in range(res_pointer.shape[0]):
        aatype[i] = resdict[res_names[i]]
    atom14_atom_exists = np.array(atom14_atom_exists, np.float32)

    atom14_positions = np.array(atom14_positions, np.float32)

    return atom_names, res_names, res_ids, crds, res_pointer, flatten_atoms, flatten_crds, init_res_names, init_res_ids,\
        residue_index, aatype, atom14_positions, atom14_atom_exists, residx_atom14_to_atom37


def gen_pdb(crd, atom_names, res_names, res_ids, pdb_name='temp.pdb'):
    """Write protein crd information into pdb format files.
    Args:
        crd(numpy.float32): The coordinates of protein atoms.
        atom_names(numpy.str_): The atom names differ from aminos.
        res_names(numpy.str_): The residue names of amino names.
        res_ids(numpy.int32): A unique mask each same residue.
        pdb_name(str): The path to save the pdb file, absolute path is suggested.
    """
    success = 1
    with open(pdb_name, 'w') as pdb:
        # pdb.write('REMARK    1 Generated By MindSponge (Molecule)\n')
        pdb.write('MODEL     1\n')
        for i, c in enumerate(crd[0]):
            pdb.write('ATOM'.ljust(6))
            pdb.write('{}'.format(i + 1).rjust(5))
            if len(atom_names[i]) < 4:
                pdb.write('  ')
                pdb.write(atom_names[i].ljust(3))
            else:
                pdb.write(' ')
                pdb.write(atom_names[i].ljust(4))
            pdb.write(res_names[i].rjust(4))
            pdb.write('A'.rjust(2))
            pdb.write('{}'.format(res_ids[i]).rjust(4))
            pdb.write('    ')
            pdb.write('{:.3f}'.format(c[0]).rjust(8))
            pdb.write('{:.3f}'.format(c[1]).rjust(8))
            pdb.write('{:.3f}'.format(c[2]).rjust(8))
            pdb.write('1.0'.rjust(6))
            pdb.write('0.0'.rjust(6))
            pdb.write('{}'.format(atom_names[i][0]).rjust(12))
            pdb.write('\n')
        pdb.write('TER\n')
        pdb.write('ENDMDL\n')
        pdb.write('END\n')
    return success
