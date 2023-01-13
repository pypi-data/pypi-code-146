"""
Vertex analysis
"""
import numpy as np
from numpy.linalg import norm
from skimage.util import view_as_windows

def find_vertices(grid, pos, angle, win_size):
    """
    Find the vertices of a geometry

    Parameters
    ----------
    grid : Grid object
        The grid of the spin positions
    angle : 1D array
        The angles of each spin
    win_size : (height, width)
        The window size to scan the grid

    Returns a tuple (vi, vj, indices) where vi, vj are the vertex indices
    and indices is a list of spin indices corresponding to each vertex
    index.
    """

    # Map indices onto grid
    index_grid = grid.map_values(np.arange(len(angle)), -1)

    # Sliding window over index grid
    index_window = view_as_windows(index_grid, win_size)

    # Map of vertex candidates in index_window
    is_vertex = np.zeros(index_window.shape[:2], dtype=bool)

    # Average distance from magnets to vertex center
    vertex_dist = np.zeros(index_window.shape[:2])

    # Find all windows where all spins point either towards or away from the
    # window center
    mag = np.column_stack((np.cos(angle), np.sin(angle)))
    for i in np.ndindex(index_window.shape[:2]):
        inds = index_window[i].flatten()
        inds = inds[inds >= 0]

        if len(inds) == 0:
            continue

        vertex_pos = np.mean(pos[inds], axis=0)
        pos_vec = pos[inds] - vertex_pos
        vec_dirs = [np.dot(p, m) for (p,m) in zip(pos_vec, mag[inds])]
        is_vertex[i] = np.all(np.abs(vec_dirs) > 1e-8)
        vertex_dist[i] = np.mean(norm(pos_vec, axis=1))


    # For some geometries, e.g., kagome, the above search will produce vertex
    # candiates with different numbers of spins
    # Assume all vertices have the same number of spins, and keep only the
    # candidates with the most spins

    # Find number of spins in each vertex candidate
    vertex_size = index_window >= 0
    vertex_size = vertex_size.reshape(vertex_size.shape[:2] + (-1,))
    vertex_size = np.count_nonzero(vertex_size, axis=-1)

    # Keep only the vertices with the most spins
    max_size = np.max(vertex_size[is_vertex])
    is_vertex = np.logical_and(is_vertex, vertex_size == max_size)

    # Keep only the most compact vertices
    vertex_dist = np.round(vertex_dist, 12)
    min_dist = np.min(vertex_dist[is_vertex])
    is_vertex = np.logical_and(is_vertex, vertex_dist == min_dist)

    # The vertex indices (vi, vj) are based on the grid
    vertex_indices = is_vertex.nonzero()

    # Extract the spin indices for each vertex
    spin_indices = index_window[is_vertex]
    spin_indices = [i[i>=0] for i in spin_indices]

    return vertex_indices + (spin_indices,)

def vertex_type_ising(spin, pos, angle):
    if spin[0] == spin[1]:
        return 1
    return 2

def vertex_dir(pos, angle):
    """
    Calculate the direction of spins in a vertex

    Determines whether spins point towards or away from the vertex center

    Returns an array containing 1 if the spin points towards, and -1 if the
    spin points away from the vertex center, respectively """

    vertex_pos = np.mean(pos, axis=0)
    pos_vec = pos - vertex_pos
    mag_vec = np.column_stack((np.cos(angle), np.sin(angle)))
    dir_in = [np.dot(p, m) < 0 for (p,m) in zip(pos_vec, mag_vec)]
    dir_in = np.where(dir_in, 1, -1)

    return dir_in


def vertex_type_square(spin, pos, angle):
    dir_in = vertex_dir(pos, angle)
    spin = spin * dir_in
    if spin[0] == -1:
        # flipping the spins in a vertex won't change its type
        spin *= -1
    num_in = np.count_nonzero(spin == 1)

    if num_in == 2:
        if tuple(spin) == (1, -1, -1, 1):
            # Type I
            return 1
        # Type II
        return 2

    if num_in == 3 or num_in == 1:
        # Type III
        return 3

    # Type IV
    return 4

def vertex_type_tri(spin, pos, angle):
    dir_in = vertex_dir(pos, angle)
    spin *= dir_in
    if spin[0] == -1:
        # flipping the spins in a vertex won't change its type
        spin *= -1

    num_in = np.count_nonzero(spin == 1)
    if num_in == 3:
        # Type II
        return 2

    # Type I
    return 1

def vertex_type(spin, pos, angle):
    """ Determine the type of a vertex given its spins and angles """
    if len(spin) == 2:
        return vertex_type_ising(spin, pos, angle)
    elif len(spin) == 3:
        return vertex_type_tri(spin, pos, angle)
    elif len(spin) == 4:
        return vertex_type_square(spin, pos, angle)

    raise NotImplementedError(f"Don't know about vertices of size {len(spin)}, sorry.")

def vertex_pos(pos, vertices):
    return np.array([pos[v].mean(axis=0) for v in vertices])

def vertex_mag(mag, vertices):
    return np.array([mag[v].sum(axis=0) for v in vertices])

