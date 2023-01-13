from crystally.core.lattice import *
import numpy as np
from crystally.vasp.tools import get_element_number_list


__all__ = ("write_poscar", "read_poscar",)


def write_poscar(lattice: Lattice, file: str, poscar_description: str):
    """ Write a lattice to a file in the vasp POSCAR format.

    :param lattice: a :class:`~crystally.core.lattice.Lattice` object
    :param file: the file name
    :param poscar_description: the description that is written to the head of the file
    :return: None
    """
    header = "{:s} \n" \
             "1.00 \n" \
             "{:19.16f} {:19.16f} {:19.16f} \n" \
             "{:19.16f} {:19.16f} {:19.16f} \n" \
             "{:19.16f} {:19.16f} {:19.16f} \n" \
            .format(poscar_description, *tuple(lattice.vectors.flatten()))

    element_numbers = get_element_number_list(lattice)
    elements = [x[0] for x in element_numbers]
    numbers = [x[1] for x in element_numbers]
    for element in elements:
        header += f"{element} "
    header += "\n"
    for number in numbers:
        header += f"{number} "
    header += "\n"

    header += "Direct\n"

    with open(file, "w") as f:
        f.write(header)
        for atom in lattice:
            f.write(" ".join(f"{c:19.16f}" for c in atom.position) + "\n")


def read_poscar(file):
    """ Reads the lattice from a file in vasp POSCAR style.

    :param file: the file that should be read
    :return: a :class:`~crystally.core.lattice.Lattice` object
    """
    lattice = Lattice(atoms=[])

    with open(file, 'r') as f:
        f.readline()
        multiplier = float(f.readline())

        lattice_vectors = [np.array(list(map(float, f.readline().split()[:3])))*multiplier for _ in range(3)]

        lattice.vectors = lattice_vectors

        atom_names = f.readline().split()
        atom_numbers = list(map(int, f.readline().split()))
        element_list = [elem for i in range(len(atom_numbers)) for elem in [atom_names[i]]*atom_numbers[i]]

        option = f.readline()
        if option[0].lower() == "s":
            option = f.readline()

        for i in range(sum(atom_numbers)):
            position = np.array(list(map(float, f.readline().split()[:3])))
            if option[0].lower() == "c" or option[0].lower() == "k":
                position = position.dot(np.linalg.inv(lattice.vectors))
            lattice.atoms.append(Atom(element=element_list[i],
                                      position=position))
        return lattice
