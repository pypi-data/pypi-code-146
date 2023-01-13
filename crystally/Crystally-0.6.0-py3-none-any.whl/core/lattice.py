from crystally.core.vectors import *
import copy
from crystally.core.constants import *
from typing import Union as Union
import warnings
import numpy as np
from collections import Counter, namedtuple

__all__ = ["Atom", "Lattice", "concat_lattices", "generate_rdf"]


class Atom:
    """An entry within a :class:`Lattice`.

    The Atom has two propertiers. An element and fractional coordinates ion form f a
    :class:`~crystally.core.vectors.PeriodicVector`.

    :param element: string of element name
    :param position: fractional position of the atom
    :return: Atom object
    """

    def __init__(self, element: str = "", position=(0, 0, 0)):
        self.element = str(element)
        if len(position) != 3:
            raise ValueError("Position needs three entries!")
        self._position = PeriodicVector(position)

    def __str__(self):
        string_representation = "Atom:"
        string_representation += f" {self.element:4s} "
        string_representation += f"[ {', '.join([f'{coord:.10f}' for coord in self.position.value])} ]"
        return string_representation

    def __repr__(self):
        rep = "Atom("
        rep += repr(self.element) + ", "
        rep += repr(self.position.value.tolist()) + ")"
        return rep

    def __eq__(self, other):
        return self.element == other.element        \
           and self.position == other.position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        if len(new_position) != 3:
            raise ValueError("Position needs three entries!")
        self._position = PeriodicVector(new_position)


class Lattice:
    """A crystal lattice with atoms and crystal vectors

    :param atoms: string of element name
    :param vectors: fractional position of the atom
    :return: Lattice object
    """

    def __init__(self, vectors=np.identity(3), atoms=None):
        self._vectors = None
        self.atoms = list(atoms) if atoms is not None else list()
        self.vectors = vectors

    def __iter__(self):
        return iter(self.atoms)

    def __str__(self):
        string_rep = "Lattice:\n" \
                     + " "*5 + "Vectors:\n"
        for vec in self.vectors:
            components = ["{:13.10f}".format(i) for i in vec]
            string_rep += "{:>23s} {} {}\n".format(*tuple(components))
        string_rep += " "*5 + "Positions:\n"
        for i in range(0, len(self.atoms)):
            string_rep += " "*10
            string_rep += "{: <5d}".format(i)
            string_rep += str(self.atoms[i])
            string_rep += "\n"
        return string_rep

    def __repr__(self):
        rep = "Lattice("
        rep += repr(self.vectors.tolist()) + ", \n"
        rep += "["
        for atom in self:
            rep += repr(atom) + ", \n"
        rep += "])"
        return rep

    def __getitem__(self, item):
        return self.atoms[item]

    def __setitem__(self, key, value):
        self.atoms[key] = value

    def __delitem__(self, key):
        del(self.atoms[key])

    @property
    def vectors(self):
        return self._vectors

    @vectors.setter
    def vectors(self, vec):
        new = np.array(vec)
        if new.shape != (3, 3):
            raise ValueError("The lattice vectors have to be represented as a 3x3 matrix.")
        self._vectors = np.array(vec)

    @property
    def volume(self):
        """ Calculates the volume of the lattice.

        :return: volume of lattice
        """
        return np.cross(self.vectors[0], self.vectors[1]).dot(self.vectors[2])

    def sort(self, key=None, *, tolerance=None, ignore_element=False):
        """ Sort the lattice in-place with a given key.

        :param key: sorting argument which is used to sort the lattice. The following aruments can be used:

                    1. "element" - will sort according to the atoms element names
                    2. "position" - will sort according to the atoms absolute distance to the lattice origin
                    3. :class:`Lattice` - this will sort this lattice according to a different lattice. Atoms are
                        compared for their position and element. The latter can be deactivated.

        :param tolerance: tolerance parameter which will be used when sorting this lattice with another lattice. If
                          None is specified the default value of constants.ABS_VEC_COMP_TOL is used.

        :param ignore_element: ignores the element when the lattice is sorted with a different lattice

        :return: None
        """
        if key is None:
            self.atoms.sort(key=lambda atom: (atom.element, self.distance(atom, [0.0, 0.0, 0.0])))
        elif key == "element":
            self.atoms.sort(key=lambda atom: atom.element)
        elif key == "position":
            self.atoms.sort(key=lambda atom: self.distance(atom, [0.0, 0.0, 0.0]))
        elif isinstance(key, Lattice):
            self._sort_with_other_lattice(key, tolerance, ignore_element)
        else:
            self.atoms.sort(key=key)
        return None

    def find(self, position=None, *, tolerance=None):
        """ Search the atom list for an atom at the specified location

        :param position: position of the atoms to get within a tolerance (can be specified)
        :param tolerance: tolerance of positional search in angstrom.
        :return: :class:`Atoms <.Atom>` or `None` if no atoms satisfy the criteria.
        """

        tolerance = ABS_VEC_COMP_TOL if not tolerance else tolerance

        for atom in self.atoms:
            if self.distance(atom, position) < tolerance:
                return atom

    def remove(self, atom: Atom):
        """ Removes an atom from the atom list.

        :param atom: :class:`Atoms <.Atom>` that should be removed. This atom has to come from the atom list in the
                     first place.
        :return: None
        """
        for i, a in enumerate(self):
            if id(a) == id(atom):
                del(self[i])
                break
        else:
            raise ValueError("The specified atom is not in the atom list of this lattice.")

    def to_cartesian(self, position):
        """ Translates fractional coordinates to cartesian coordinates.

        :param position: fractional coordinates
        :return: cartesian coordinates
        """
        position = self._prepare_position(position, False)
        return self.vectors.dot(np.array(position))

    def to_fractional(self, position, *, periodic=False):
        """ Translates cartesian coordinates to fractional coordinates.

        :param position: cartesian coordinates
        :param periodic: if periodic is set to `True`. The fractional coordinates are translated
                         to a value between 0 and 1.
        :return: fractional coordinates
        """
        position = self._prepare_position(position, False)
        frac_position = np.linalg.inv(self.vectors) @ position
        if periodic:
            return PeriodicVector(frac_position).value
        else:
            return frac_position

    def get_in_radius(self, center: Union[list, Atom], max_radius: float, min_radius: float = 0.0):
        """ Get all :class:`.Atom` that are in range to a provided position.

        :param center: Search center in fractional coordinates. This can either be a coordinates as a list
                        or a :class:`.Atom`. Mind that positions outside of the cell are placed within.
        :param max_radius: maximal radius in angstrom, that is searched
        :param min_radius: minimal radius in angstrom, that is searched. Default is 0 angstrom.

        :return: List of :class:`.Atom`
        """
        def condition(atom):
            return min_radius <= self.distance(atom, center) <= max_radius
        atom_list = [atom for atom in self.atoms if condition(atom)]
        atom_list.sort(key=lambda atom: self.distance(atom, center))
        return atom_list

    def index(self, position, *, tolerance=1e-3):
        """ Get the index within the atom list of the :class:`.Atom` at the provided position

        :param position: Position or Atom whose index is searched for
        :param tolerance: Tolerance in angstrom
        :return: index of :class:`.Atom`
        """
        for i, atom in enumerate(self.atoms):
            if self.distance(atom, position) < tolerance:
                return i
        return None

    def get_element_names(self):
        """ Get all occuring :attr:`Atom.element` names

        :return: List of strings
        """
        element_names = set()
        [element_names.add(x.element) for x in self.atoms]
        return list(element_names)

    def distance(self, position1, position2, *, periodic=True) -> float:
        """ Get the distance between two points

        :param position1: fractional coordinate as list or atom
        :param position2: fractional coordinate as list or atom
        :param periodic: bool, flag that indicates if the distance should be calculated under consideration of
                                periodic boundaries
        :return: distance in Angstrom
        """

        position1 = self._prepare_position(position1, periodic)
        position2 = self._prepare_position(position2, periodic)

        if periodic is True:
            diff_vector = position1.diff(position2)
        else:
            diff_vector = position2 - position1

        diff_vector_cartesian = diff_vector.dot(self.vectors)
        return np.sqrt(diff_vector_cartesian.dot(diff_vector_cartesian))

    def angle(self, position1, center, position2, *, periodic=True) -> float:
        """ Get the angle between two positions and a center.

        :param position1: fractional coordinate as list or atom
        :param center: fractional coordinate as list or atom
        :param position2: fractional coordinate as list or atom
        :param periodic: flag that indicates if the distance should be calculated under consideration of
                                periodic boundaries
        :return: angle in rad
        """

        position1 = self._prepare_position(position1, periodic)
        position2 = self._prepare_position(position2, periodic)
        center = self._prepare_position(center, periodic)

        if periodic is True:
            vec1 = position1.diff(center)
            vec2 = position2.diff(center)
        else:
            vec1 = position1 - center
            vec2 = position2 - center

        vec_cart1 = vec1.dot(self.vectors)
        vec_cart2 = vec2.dot(self.vectors)
        magn1 = np.sqrt(vec_cart1.dot(vec_cart1))
        magn2 = np.sqrt(vec_cart2.dot(vec_cart2))
        return np.arccos(vec_cart1.dot(vec_cart2)/(magn1*magn2))

    def polyhedron_volume(self, vertices, *, periodic=True) -> float:
        """ Lets you calculate the volume of a convex polyhedron (a body with no dents).

        :param vertices: List of fractional coordinates representing the vertices of the polyhedron.
                         Number of points must be equal or greater than 4!
        :param periodic: flag that indicates if the periodic boundary should be considered for the
                         distance between the vertices
        :return: The volume of the polyhedron
        """
        from scipy.spatial import ConvexHull

        if len(vertices) < 4:
            raise IndexError("Number of vertices is too small!")

        vertices = [getattr(x, "position", x) for x in vertices]

        if periodic is True:
            vertices = [PeriodicVector(x) for x in vertices]
            reference = vertices[0]
            vertices = [self.to_cartesian(x.diff(reference)) for x in vertices]
        else:
            vertices = [self.to_cartesian(x) for x in vertices]

        convex_hull = ConvexHull(vertices)
        if len(convex_hull.points) != len(convex_hull.vertices):
            warnings.warn("Points do not form a convex polyhedron", UserWarning)
        return convex_hull.volume

    def polyhedron_area(self, vertices, *, periodic=True) -> float:
        """ Lets you calculate the area of a convex polyhedron (a body with no dents).

        :param vertices: List of fractional coordinates representing the vertices of the polyhedron.
                         Number of points must be equal or greater than 4!
        :param periodic: flag that indicates if the periodic boundary should be considered for the
                         distance between the vertices
        :return: The volume of the polyhedron
        """
        from scipy.spatial import ConvexHull

        if len(vertices) < 4:
            raise IndexError("Number of vertices is too small!")

        vertices = [getattr(x, "position", x) for x in vertices]

        if periodic is True:
            vertices = [PeriodicVector(x) for x in vertices]
            reference = vertices[0]
            vertices = [self.to_cartesian(x.diff(reference)) for x in vertices]
        else:
            vertices = [self.to_cartesian(x) for x in vertices]

        convex_hull = ConvexHull(vertices)
        if len(convex_hull.points) != len(convex_hull.vertices):
            raise UserWarning("Points do not form a convex polyhedron")
        return convex_hull.area

    def increase_distance_rel(self, center, position, rel_increase):
        """ Function to easily manipulate lattices. A center and second position need to be provided. The second
        position is then shifted away from the center position by a provided percentage. The new position is then returned.
        Mind that no variables are changed by this function.

        :param center: fractional coordinates of the center position. Can be a list of coordinates or a :class:`.Atom`.
        :param position: fractional coordinates of the second position. Can be a list of coordinates or a :class:`.Atom`.
        :param rel_increase: distance increase in percent
        :return: new position as :class:`~crystally.core.vectors.PeriodicVector`
        """
        # First check if atoms were passed to the function
        center = self._prepare_position(center, True)
        position = self._prepare_position(position, True)

        # check if center and position are identical
        if self.distance(center, position) < ABS_VEC_COMP_TOL:
            raise ValueError("Center and Position are too close together")

        # calculate the distance in fractional coordinates from center to position
        diff_vector = position.diff(center)

        # convert everything to cartesian coordinates
        center = self.vectors.dot(center.value)
        diff_vector = self.vectors.dot(diff_vector)

        # calculate the new position in cartesian coordinates
        new_position = center + diff_vector * (1+rel_increase)

        # convert the new position to fractional coordinates
        return PeriodicVector(np.linalg.inv(self.vectors).dot(new_position))

    def increase_distance_abs(self, center, position, abs_increase):
        """ Function to easily manipulate lattices. A center and second position need to be provided. The second
        position is then shifted away from the center position by a provided value. The new position is then returned.
        Mind that no variables are changed by this function.

        :param center: fractional coordinates of the center position. Can be a list of coordinates or a :class:`.Atom`.
        :param position: fractional coordinates of the second position. Can be a list of coordinates or a :class:`.Atom`.
        :param abs_increase: Shift in angstrom
        :return: new position as :class:`~crystally.core.vectors.PeriodicVector`
        """
        distance = self.distance(center, position)
        rel_distance = abs_increase/distance
        return self.increase_distance_rel(center, position, rel_distance)

    def diff(self, other, *, tolerance=None, ignore_element=False):
        """ Find the atomic differences between this and another lattice. Atoms are compared according to element
            and position. Mind that the fractional position of this and the other lattice are converted
            to cartesian coordinates with the vectors of this lattice.

        :param other: other :class:`.Lattice`.
        :param ignore_element: Ignore elements of lattices during comparison. Must be set to True or False.
        :param tolerance: tolerance in angstrom with which the atoms position are compared.
        :return: tuple with two lists, the first list consists of the atoms that were in this lattice, but were not
                 found in the other lattice. The second list contains the atoms that were in the other lattice, but not
                 found in this lattice.
        """

        if not tolerance:
            tolerance = ABS_VEC_COMP_TOL

        self_not_found = []
        other_not_found = list(other.atoms)

        for atom1 in self:
            for atom2_id, atom2 in enumerate(other_not_found):
                if self._compare_atoms(atom1, atom2, tolerance, ignore_element):
                    del(other_not_found[atom2_id])
                    break
            else:
                self_not_found.append(atom1)

        return self_not_found, other_not_found

    def _sort_with_other_lattice(self, other, tolerance=None, ignore_element=False):
        if tolerance is None:
            tolerance = ABS_VEC_COMP_TOL

        old_order = list(self.atoms)
        new_order = []
        for atom1 in other:
            for atom2_id, atom2 in enumerate(old_order):
                if self._compare_atoms(atom1, atom2, tolerance, ignore_element):
                    new_order.append(atom2)
                    del(old_order[atom2_id])
        new_order += old_order
        self.atoms = new_order

    def _compare_atoms(self, atom1, atom2, dist_tolerance, ignore_element):
        if atom1.element != atom2.element and ignore_element is False:
            return False
        if self.distance(atom1, atom2) > dist_tolerance:
            return False
        return True

    @staticmethod
    def _prepare_position(position, periodic):
        """ Helper function to prepare positions, which were given as arguments.

        :param position: Either an Atom or a Vector (e.g. list / np.array / PeriodicVector)
        :param periodic: decides if an PeriodicVector or an np.array is returned
        :return:
        """
        position = getattr(position, "position", position)
        if periodic is True:
            position = PeriodicVector(position)
        else:
            position = np.array(position)
        return position

    @staticmethod
    def from_lattice(lattice, size_x: int = 1, size_y: int = 1, size_z: int = 1):
        """ Create a new lattice with an already existing one. You can also provide size values to expand the lattice.

        :param lattice: the :class:`.Lattice` on which the new lattice is based on
        :param size_x: int, multiplier by which the base lattice is expanded in x direction
        :param size_y: int, see size_x
        :param size_z: int, see size_x
        :return: new :class:`.Lattice`
        """

        new_lattice_size = np.array([size_x, size_y, size_z])
        new_lattice_positions = []

        def reorientate_position(pos, x, y, z): return PeriodicVector((pos + np.array([x, y, z])) / new_lattice_size)

        lattice_expansion = ((x, y, z) for x in range(size_x) for y in range(size_y) for z in range(size_z))
        new_lattice_positions += [Atom(element=atom.element,
                                       position=reorientate_position(atom.position.value, *coord))
                                  for coord in lattice_expansion for atom in lattice.atoms]

        lattice_vectors = lattice.vectors * new_lattice_size
        new_lattice = Lattice(lattice_vectors, new_lattice_positions)
        new_lattice.sort("element")
        return new_lattice


def concat_lattices(lattice1: Lattice, lattice2: Lattice, direction: int):
    for i in range(lattice1.vectors.shape[0]):
        if i == direction:
            continue
        if not np.allclose(lattice1.vectors[i], lattice2.vectors[i], atol=FLOAT_ROUNDING):
            raise ValueError("shape of lattices does not match: "
                             "lattice1: {} lattice2: {}".format(str(lattice1.vectors[i]), lattice2.vectors[i]))
    new_lattice = Lattice(vectors=lattice1.vectors, atoms=[])
    new_lattice.vectors[direction] = lattice1.vectors[direction] + lattice2.vectors[direction]
    for atom in lattice1.atoms:
        new_atom = copy.copy(atom)
        new_atom.position = PeriodicVector(atom.position.value.dot(lattice1.vectors).dot(np.linalg.inv(new_lattice.vectors)))
        new_lattice.atoms.append(new_atom)

    for atom in lattice2.atoms:
        new_atom = copy.copy(atom)
        shift = new_atom.position.value * 0
        shift[direction] = 1
        shift_cart = shift.dot(lattice1.vectors)
        new_position = new_atom.position.value.dot(lattice2.vectors) + shift_cart
        new_position = new_position.dot(np.linalg.inv(new_lattice.vectors))
        new_atom.position = PeriodicVector(new_position)
        new_lattice.atoms.append(new_atom)

    return new_lattice


def generate_rdf(lattice: Lattice, max_radius, *, min_radius=0.001, binning_fineness=1e-10):
    """ Generate a rdf for a given :class:`.Lattice`. The neighbors are grouped by their element and distance.

    :param lattice: the :class:`.Lattice` on which the rdf is performed
    :param max_radius: maximum radius to which neighbors are searched for
    :param min_radius: minimum radius from which neighbors are searched
    :param binning_fineness: fineness of binning for the distance of neighbors
    :return: list of namedtuples with the following fields: center, neighbor, distance, average_occurrence
    """

    def calculate_distances(center, neighbors):
        diff_vectors = neighbors - center
        diff_vectors = diff_vectors - (np.abs(diff_vectors) > 0.5) * np.sign(diff_vectors)
        diff_vectors = np.dot(diff_vectors, lattice.vectors)
        distances = np.linalg.norm(diff_vectors, axis=1)
        return distances

    def generate_position_array():
        position_list = []
        for atom in lattice:
            position_list.append(atom.position.value)
        positions = np.stack(position_list)
        return positions

    def count_elements():
        element_count = Counter()
        for atom in lattice:
            element_count[atom.element] += 1
        return element_count

    def index_of_neighbors_in_range(distances):
        return ((min_radius <= distances) & (distances <= max_radius)).nonzero()[0]

    def bin_distance(dist):
        dist = dist // binning_fineness * binning_fineness
        return round(dist, 10)

    positions = generate_position_array()
    element_count = count_elements()
    rdf_entry = namedtuple("rdf_entry", ["center", "neighbor", "distance", "average_occurrence"])

    # generate rdf
    rdf = Counter()
    for atom in lattice:
        distance_to_neighbors = calculate_distances(atom.position.value, positions)
        for index in index_of_neighbors_in_range(distance_to_neighbors):
            distance, neighbor = distance_to_neighbors[index], lattice[index]
            distance = bin_distance(distance)
            mean_addition = 1 / element_count[atom.element]
            key = (atom.element, neighbor.element, distance)
            rdf[key] += mean_addition

    # sort rdf
    sorted_rdf_keys = sorted(rdf.keys(), key=lambda x: (x[0], x[1], x[2]))
    sorted_rdf = []
    for key in sorted_rdf_keys:
        entry = rdf_entry(center=key[0], neighbor=key[1], distance=key[2], average_occurrence=rdf[key])
        sorted_rdf.append(entry)

    return sorted_rdf
