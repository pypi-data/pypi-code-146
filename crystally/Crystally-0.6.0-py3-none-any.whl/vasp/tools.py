from crystally.core.lattice import *
import numpy as np

__all__ = ["make_neb", "get_element_number_list"]


def make_neb(lattice1: Lattice, lattice2: Lattice, image_numbers=1, tolerance=None):
    """ Linearly interpolate the atom list two lattices and new lattices according to the number of images.

    :param lattice1: first :class:`~crystally.core.lattice.Lattice`
    :param lattice2: second :class:`~crystally.core.lattice.Lattice`
    :param image_numbers: number of images for the NEB algorithm
    :param tolerance: the tolerance in angstrom which is used to compare atoms and sort the lattices
    :return: list of new :class:`~crystally.core.lattice.Lattice`. This includes the lattices for the initial and
    final state.
    """

    if len(lattice1.atoms) != len(lattice2.atoms):
        raise ValueError("lattices must have the same number of atoms!")

    # make copies of original lattices
    lattice1 = Lattice.from_lattice(lattice1)
    lattice2 = Lattice.from_lattice(lattice2)

    # sort lattices to each other
    lattice1.sort(lattice2, tolerance=tolerance)
    lattice2.sort(lattice1, tolerance=tolerance)

    neb_lattices = [lattice1]

    # the weighting for the interpolation is determined by the number of images
    for weighting in np.linspace(0, 1, image_numbers+2)[1:image_numbers+1]:
        new_lattice = Lattice(vectors=lattice1.vectors, atoms=[])
        for atom1, atom2 in zip(lattice1, lattice2):
            new_position = atom1.position + atom2.position.diff(atom1.position) * weighting
            new_atom = Atom(element=atom1.element, position=new_position)
            new_lattice.atoms.append(new_atom)
        neb_lattices.append(new_lattice)

    neb_lattices.append(lattice2)
    return neb_lattices


def get_element_number_list(lattice):
    """Get a two dimensional list with the sort order of the elements within the lattice.

    The first column specifies the element name and the second column the number of adjacent atoms with this
    element. This information can be used for VASP Input files.
    For instance if the sort order of the atoms is as follows:

    X, X, Y, Y, Y, X, X

    (where X and Y are the elements of the atoms)
    the function would return the following table:

    =============  =============================
    Element Name   Number of repeating elements
    =============  =============================
    X              2
    Y              4
    X              2
    =============  =============================

    :return: two dimensional list - the first column is an int, the second a string

    Examples
    --------
    >>> #lattice = generate_from_crystal(ceria(),2,2,2).sort("position")
    >>> #print(lattice.get_element_number_list())
    [['Ce', 1], ['O', 1], ['Ce', 3], ['O', 7]]
    """
    element_number_list = []
    for atom in lattice.atoms:
        if not element_number_list:
            element_number_list.append([atom.element, 1])
        elif element_number_list[-1][0] == atom.element:
            element_number_list[-1][1] += 1
        else:
            element_number_list.append([atom.element, 1])
    return element_number_list
