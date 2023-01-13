from functools import reduce
from itertools import cycle
from fractions import Fraction
from collections import namedtuple
import numpy as np
from scipy.cluster.hierarchy import ward, cut_tree
from scipy.linalg import block_diag, solve_banded, pinvh
from sympy.physics.quantum.cg import CG
from . import utils as ut

def apply_unary(func, a, *args, **kwargs):
    return [None if x is None else func(x, *args, **kwargs) for x in a]
        
def apply_binary(func, a, b, *args, **kwargs):
    return [None if x is None and y is None else
            (x if y is None else
                (y if x is None else func(x, y, *args, **kwargs)))
            for x, y in zip(a, b)]

def apply_subset(idx, a):
    return apply_unary(lambda x: x[idx], a)

def sf2ws(sf_op, sf_smult):

    def sf2ws_comp(op):
        return np.block([[
            op[idx1, idx2] * np.identity(smult1) if smult1 == smult2 else
            np.zeros((smult1, smult2))
            for idx2, smult2 in enumerate(sf_smult)]
            for idx1, smult1 in enumerate(sf_smult)])

    if sf_op is None:
        ws_op = None

    else:
        if len(sf_op.shape) > 2:  # e.g. cartesian operators
            ws_op = np.array([sf2ws_comp(op) for op in sf_op])
        else:
            ws_op = sf2ws_comp(sf_op)

    return ws_op

def sf2ws_spin(sf_op, sf_smult):

    def me(s1, ms1, sf1, s2, ms2, sf2):
        if np.abs(s1 - s2) <= 2 and np.abs(ms1 - ms2) <= 2:
            return coeff(s1, ms1, s2, ms2) * op(s1, ms1, sf1, s2, ms2, sf2)
        else:
            return 0.0

    def op(s1, ms1, sf1, s2, ms2, sf2):

        if np.abs(s1 - s2) <= 2:
            if ms1 == ms2:
                return sf_op[2, sf1, sf2]
            elif ms1 + 2 == ms2:
                return (+ sf_op[0, sf1, sf2] + 1.j * sf_op[1, sf1, sf2])
            elif ms1 - 2 == ms2:
                return (- sf_op[0, sf1, sf2] + 1.j * sf_op[1, sf1, sf2])
            else:
                return 0.0
        else:
            return 0.0

    def coeff(s1, ms1, s2, ms2):
        # double integer figures and extra "/ 2" factor in common factor due 2
        # double quantum number convention

        if s1 == s2:
            if s1 == 0:
                return 0.0
            elif ms1 == ms2:
                c = ms1
            elif ms1 + 2 == ms2:
                c = + np.sqrt((s1 - ms1) * (s1 + ms1 + 2)) / 2
            elif ms1 - 2 == ms2:
                c = - np.sqrt((s1 + ms1) * (s1 - ms1 + 2)) / 2
            else:
                c = 0.0
            return c / np.sqrt(s1 * (s1 + 2) * (2 * s1 + 2) / 2)

        elif s1 + 2 == s2:
            if ms1 == ms2:
                c = np.sqrt((s1 + 2)**2 - ms1**2)
            elif ms1 + 2 == ms2:
                c = - np.sqrt((s1 + ms1 + 2) * (s1 + ms1 + 4)) / 2
            elif ms1 - 2 == ms2:
                c = - np.sqrt((s1 - ms1 + 2) * (s1 - ms1 + 4)) / 2
            else:
                c = 0.0
            return c / np.sqrt((s1 + 1) * (2 * s1 + 1) * (2 * s1 + 3) / 2)
        
        elif s1 - 2 == s2:
            if ms1 == ms2:
                c = np.sqrt(s1**2 - ms1**2)
            elif ms1 + 2 == ms2:
                c = np.sqrt((s1 - ms1) * (s1 - ms1 - 2)) / 2
            elif ms1 - 2 == ms2:
                c = np.sqrt((s1 + ms1) * (s1 + ms1 - 2)) / 2
            else:
                c = 0.0
            return c / np.sqrt(s1 * (2 * s1 - 1) * (2 * s1 + 1) / 2)

        else:
            return 0.0

    if sf_op is None:
        ws_op = None

    else:
        ws_op = np.array([
            [me(s1, ms1, sf1, s2, ms2, sf2) for s2, ms2, sf2 in zip(
                [m - 1 for m in sf_smult for _ in range(m)],
                [- (m - 1) + 2 * i for m in sf_smult for i in range(m)],
                [i for i, m in enumerate(sf_smult) for _ in range(m)])
             ] for s1, ms1, sf1 in zip(
                [m - 1 for m in sf_smult for _ in range(m)],
                [- (m - 1) + 2 * i for m in sf_smult for i in range(m)],
                [i for i, m in enumerate(sf_smult) for _ in range(m)])
            ])

    return ws_op


def unitary_transform(op, Umat, op_dx=None, Umat_dx=None):

    _op = Umat.conj().T @ op @ Umat

    if not (op_dx is None and Umat_dx is None):
        _op_dx = (
                (0.0 if Umat_dx is None else Umat_dx.conj().T @ op @ Umat) +
                (0.0 if op_dx is None else Umat.conj().T @ op_dx @ Umat) +
                (0.0 if Umat_dx is None else Umat.conj().T @ op @ Umat_dx))
    else:
        _op_dx = None

    return _op, _op_dx

def cartesian_op_squared(op, op_dx=None):

    op2 = np.sum([op[comp] @ op[comp] for comp in range(3)], axis=0)

    if op_dx is not None:
        op2_dx = np.sum([op_dx[comp] @ op[comp] + op[comp] @ op_dx[comp]
                         for comp in range(3)], axis=0)
    else:
        op2_dx = None

    return op2, op2_dx


def op_multiply(op1, op2, op1_dx=None, op2_dx=None):

    op = op1 @ op2

    if op1_dx is None and op2_dx is None:
        op_dx = None
    elif op1_dx is None:
        op_dx = op1_dx @ op2
    elif op1_dx is None:
        op_dx = op1 @ op2_dx
    else:
        op_dx = op1_dx @ op2 + op1 @ op2_dx

    return op, op_dx


def extract_blocks(data, *blk_labs):

    if all(labs is None for labs in blk_labs):
        data_blks = [data]

    elif not all([len(blk_labs[0]) == len(labs) for labs in blk_labs]):
        raise ValueError("Lists of block labels need to have the same length.")

    else:
        blk_idc = [[np.flatnonzero((labs == lab).all(axis=1))
                    for lab in np.unique(labs, axis=0)] for labs in blk_labs]

        data_blks = [None if data is None else np.array(data)[np.ix_(*idc)]
                     for idc in zip(*blk_idc)]

    return data_blks


def from_blocks(data_blks, *blk_labs):
    blk_idc = [[np.flatnonzero((labs == lab).all(axis=1))
                for lab in np.unique(labs, axis=0)] for labs in blk_labs]

    shape = [len(labs) for labs in blk_labs]
    blk_data = np.zeros(shape, dtype=data_blks[0].dtype)

    for idc, data in zip(zip(*blk_idc), data_blks):
        blk_data[np.ix_(*idc)] = data

    return blk_data


def find_blks_nclust(nclust):

    def make_find_blks(count):
        def find_blks(vals):
            clust = ward(vals[:, np.newaxis])
            labs = cut_tree(clust, n_clusters=count).flatten()
            # adjust block labels/idc to follow an ascending order by vals
            _, blk_labs = np.unique([np.mean(vals[labs == lab])
                                     for lab in labs], return_inverse=True)
            return blk_labs
        return find_blks

    for count in nclust:
        yield make_find_blks(count)


def find_no_blks():

    def make_find_blks():
        def find_blks(vals):
            return np.zeros(len(vals))
        return find_blks

    while True:
        yield make_find_blks()


def find_blks_thresh(thresh):

    def make_find_blks(height):
        def find_blks(vals):
            clust = ward(vals[:, np.newaxis])
            labs = cut_tree(clust, height=height).flatten()
            # adjust block labels/idc to follow an ascending order by vals
            _, blk_labs = np.unique([np.mean(vals[labs == lab])
                                     for lab in labs], return_inverse=True)
            return blk_labs
        return find_blks

    for height in thresh:
        yield make_find_blks(height)


def find_blks_nclust_angm_qn(nclust):

    def make_find_blks(count):
        def find_blks(vals):
            # adjust quadratically scaling eigenvalues of square angm operators
            clust = ward(np.sqrt(vals)[:, np.newaxis])
            labs = cut_tree(clust, n_clusters=count).flatten()
            # adjust block labels/idc to follow an ascending order by vals
            _, blk_labs = np.unique([np.mean(vals[labs == lab])
                                     for lab in labs], return_inverse=True)
            return blk_labs
        return find_blks

    for count in nclust:
        yield make_find_blks(count)


def find_blks_nclust_angm_proj(nclust):

    def make_find_blks(count):
        def find_blks(vals):
            clust = ward(vals[:, np.newaxis])
            labs = cut_tree(clust, n_clusters=count).flatten()
            # adjust block labels/idc to follow an ascending order by vals
            _, blk_labs = np.unique([np.mean(vals[labs == lab])
                                     for lab in labs], return_inverse=True)
            return blk_labs
        return find_blks

    for count in nclust:
        yield make_find_blks(count)


def block_transformation(ops, ops_dx, find_blks=find_no_blks(), blks=None):

    def eigh_in_blks(op_blks, op_dx_blks):

        if op_dx_blks is not None:
            eigs, vecs, eigs_dx, vecs_dx = zip(
                *[eigh_perturbation(b, bdx)
                  for b, bdx in zip(op_blks, op_dx_blks)])
        else:
            eigs, vecs = zip(*[np.linalg.eigh(b) for b in op_blks])
            eigs_dx, vecs_dx = None, None

        return eigs, vecs, eigs_dx, vecs_dx

    op_blks, op_dx_blks = \
        apply_unary(extract_blocks, [ops[0], ops_dx[0]], blks, blks)
    eigs, vecs, eigs_dx, vecs_dx = eigh_in_blks(op_blks, op_dx_blks)

    eig, eig_dx = apply_unary(np.concatenate, [eigs, eigs_dx])
    vec, vec_dx = apply_unary(lambda x: block_diag(*x), [vecs, vecs_dx])

    # find blocks of (near) equal eigenvalue preserving existing blocks
    new_blks = next(find_blks)(eig)
    merged_blks = [(n,) for n in new_blks] if blks is None \
        else [b + (n,) for b, n in zip(blks, new_blks)]

    if len(ops) == 1:
        return merged_blks, (vec, vec_dx)

    else:
        _ops, _ops_dx = zip(*[unitary_transform(o, vec, o_dx, vec_dx)
                              for o, o_dx in zip(ops[1:], ops_dx[1:])])

        _blks, (_vec, _vec_dx) = block_transformation(
            _ops, _ops_dx, find_blks=find_blks, blks=merged_blks)

        return _blks, op_multiply(vec, _vec, vec_dx, _vec_dx)


def block_phase(op, op_dx, blks, sgn="pos"):
    op_blks, op_dx_blks = apply_unary(extract_blocks, [op, op_dx], blks, blks)
    if op_dx_blks is not None:
        ph_blks, ph_dx_blks = zip(
            *[phase(o, o_dx) for o, o_dx in zip(op_blks, op_dx_blks)])
        return apply_unary(from_blocks, [ph_blks, ph_dx_blks], blks, blks)
    else:
        ph_blks, ph_dx_blks = zip(*[phase(o, None) for o in op_blks])
        return from_blocks(ph_blks, blks, blks), None


def phase(op, op_dx, sgn="pos"):

    op_diag = np.diag(op, k=-1)
    angles = np.angle(op_diag)

    Amat = np.array([
        np.concatenate([[0], -np.ones(angles.size)]),
        np.ones(angles.size + 1)])

    phase_ang = solve_banded((0, 1), Amat, np.append(-angles, 0))
    phase = np.diag(np.exp(1.j * phase_ang))

    if op_dx is not None:
        op_dx_diag = np.diag(op_dx, k=-1)
        angles_dx = (
                np.imag(op_dx_diag) * np.real(op_diag) -
                np.imag(op_diag) * np.real(op_dx_diag)
                ) / np.abs(op_diag)**2
        phase_ang_dx = solve_banded((0, 1), Amat, np.append(-angles_dx, 0))
        phase_dx = 1.j * np.diag(np.exp(1.j * phase_ang) * phase_ang_dx)
    else:
        phase_dx = None

    return phase, phase_dx


def eigh_perturbation(op, op_dx, atol=1e-10, rtol=1e-8):

    eig, vec = np.linalg.eigh(op)

    if op_dx is not None:

        eig_dx = np.real([v.conj() @ op_dx @ v for v in vec.T])

        vec_dx = np.column_stack([
            pinvh(e * np.identity(op.shape[0]) - op, atol=atol, rtol=rtol)
            @ op_dx @ v for e, v in zip(eig, vec.T)])
    else:
        eig_dx = vec_dx = None

    return eig, vec, eig_dx, vec_dx


def calc_ang_mom_ops(J):
    """
    Calculates the angular momentum operators jx jy jz jp jm j2

    Parameters
    ----------
    J : float
        J quantum number

    Returns
    -------
    np.array
        Matrix representation of jx angular momentum operator
    np.array
        Matrix representation of jy angular momentum operator
    np.array
        Matrix representation of jz angular momentum operator
    np.array
        Matrix representation of jp angular momentum operator
    np.array
        Matrix representation of jm angular momentum operator
    np.array
        Matrix representation of j2 angular momentum operator
    """

    # Create vector of mj values
    mj = np.arange(-J, J + 1, 1, dtype=np.complex128)
    # calculate number of states
    n_states = int(2 * J + 1)

    # jz operator - diagonal in jz basis- entries are mj
    jz = np.diag(mj)

    # jp and jm operators
    jp = np.zeros([n_states, n_states], dtype=np.complex128)
    jm = np.zeros([n_states, n_states], dtype=np.complex128)
    for it1, mjp in enumerate(mj):
        for it2, mjq in enumerate(mj):
            jp[it1, it2] = np.sqrt(J * (J + 1) - mjq * (mjq + 1))
            jp[it1, it2] *= ut.krodelta(mjp, mjq + 1)
            jm[it1, it2] = np.sqrt(J * (J + 1) - mjq * (mjq - 1))
            jm[it1, it2] *= ut.krodelta(mjp, mjq - 1)

    # jx, jy, and j2
    jx = 0.5 * (jp + jm)
    jy = 1. / (2. * 1j) * (jp - jm)
    j2 = jx @ jx + jy @ jy + jz @ jz

    return jx, jy, jz, jp, jm, j2


def make_angmom_ops_from_mult(mult):
    """
    Calculates the angular momentum operators jx jy jz jp jm j2 for a manifold
    of multiplicities. The resulting operator take block diagonal shape.

    Parameters
    ----------
    mult : list
        Array of multiplicities.

    Returns
    -------
    np.array
        Matrix representation of jx angular momentum operator
    np.array
        Matrix representation of jy angular momentum operator
    np.array
        Matrix representation of jz angular momentum operator
    np.array
        Matrix representation of jp angular momentum operator
    np.array
        Matrix representation of jm angular momentum operator
    np.array
        Matrix representation of j2 angular momentum operator
    """

    j = np.block([[
        np.array(calc_ang_mom_ops((smult1 - 1) / 2)[0:3]) if idx1 == idx2 else
        np.zeros((3, smult1, smult2))
        for idx2, smult2 in enumerate(mult)]
        for idx1, smult1 in enumerate(mult)])

    j2 = cartesian_op_squared(j)

    return j[0], j[1], j[2], j[0] + 1.j * j[1], j[0] - 1.j * j[1], j2


def find_basis(ops, blk_count_qn, blk_count_proj=None, blks=None):
    """Finds the transformation to an angular momentum basis.
    The ordering corresponds to "S2SzL2Lz...".

    Parameters
    ----------
    ops : dict of np.array
        Dictionaries of the angular momentum operators J.
    blk_count_qn : list of ints
        Block counts for the J2 operators in ops.
    blk_count_proj : list of ints (optional)
        Block counts for the Jz operators in ops.
    -------
    tuple
        Transformation matrix from initial to angular momentum basis and its
        first derivative.
    """
    if not len(ops) == len(blk_count_qn) or not (
            blk_count_proj is None or len(ops) == len(blk_count_proj)):
        raise ValueError("Arguments have different length.")

    # carry out block diagonalisation
    # 1. angular momentum quantum number
    blk_qn, (vec_qn, vec_qn_dx) = block_transformation(
        *zip(*[cartesian_op_squared(*op) for op in ops.values()]),
        find_blks=find_blks_nclust_angm_qn(blk_count_qn),
        blks=blks
    )

    if blk_count_proj is None:
        return blk_qn, (vec_qn, vec_qn_dx)

    # 2. z-projection quantum number
    blk_proj, (vec_proj, vec_proj_dx) = block_transformation(
        *zip(*[apply_subset(2, unitary_transform(op, vec_qn, op_dx, vec_qn_dx))
               for op, op_dx in ops.values()]),
        find_blks=find_blks_nclust_angm_proj(blk_count_proj),
        blks=blk_qn
    )

    vec, vec_dx = op_multiply(vec_qn, vec_proj, vec_qn_dx, vec_proj_dx)

    # carry out phase correction
    for idx, (op_lab, (_op, _op_dx)) in enumerate(ops.items()):
        # subset by all other blk ids then proj qn
        ph_blks = [tuple(q for i, q in enumerate(labs)
                   if i != len(labs) - len(ops) + idx) for labs in blk_proj]

        ph, ph_dx = apply_subset(0, [_op, _op_dx])
        ph_vec, ph_vec_dx = block_phase(
            *unitary_transform(ph, vec, ph_dx, vec_dx), ph_blks, sgn="pos")
        vec, vec_dx = op_multiply(vec, ph_vec, vec_dx, ph_vec_dx)

        op, op_dx = unitary_transform(_op, vec, _op_dx, vec_dx)

    return blk_proj, (vec, vec_dx)


def find_angm_basis(spin, angm, space, verbose=False, comp_thresh=0.05,
                    spin_dx=None, angm_dx=None, **ext_ops):
    """Finds the transformation to a specific angular momentum basis.

    Parameters
    ----------
    spin : np.array
        Array containing the spin operators in the initial basis.
    angm : np.array
        Array containing the orbital angular momentum operators in the initial
        basis.
    space : list of obj
        List of Symbol objects specifing the input space, e.g. terms/levels.
    verbose : bool
        Turn on plotting of angular momentum and tranformation matrices.
    comp_thresh : float
        Maximum amplitude of a given angular momentum state to be printed in
        the composition section.
    spin_dx : np.array, default=None
        Array containing the spin operator derivatives.
    angm_dx : np.array, default=None
        Array containing the orbital angular momentum operator derivatives.
    ext_ops : dict
        Dictionary of extra angular momentum operators with a single letter key
        which is referenced in the basis label. Use K, k or l for orbital
        angular momentum operators (quantum number element of natural numbers)
        and avoid S, L, J and M which are reserved for the common spin and
        orbital angular momentum operators as well as total angular momentum
        and magnetic moment operators in the basic usage of this function.

    Returns
    -------
    list of np.arrays
        1st element: Angular momentum basis labels.
        2nd element: Pair of transformation matrix from initial to angular
            momentum basis and its first derivative.
    """

    spin = [spin, spin_dx]
    angm = [angm, angm_dx]

    ops = {'S': spin, 'L': angm, **ext_ops}

    cpld_ops = {lab: ops[lab] for _, j1j2 in space[0].coupling.items()
                if j1j2 is not None for lab in j1j2}

    uncpld_ops = {j: ops[j] if j1j2 is None else
                  apply_binary(lambda x, y: x + y, ops[j1j2[0]], ops[j1j2[1]])
                  for j, j1j2 in space[0].coupling.items()}

    basis_labs = sorted([state for symbol in space for state in symbol.states])
    out_basis = space[0].basis

    if cpld_ops:
        blk_cpld, (vec_cpld, vec_cpld_dx) = find_basis(
            cpld_ops,
            [len(set(symbol.qn[op] for symbol in space)) for op in cpld_ops]
        )
    else:
        blk_cpld = None
        vec_cpld, vec_cpld_dx = np.identity(len(basis_labs)), None

    blk_uncpld, (vec_uncpld, vec_uncpld_dx) = find_basis(
        {lab: unitary_transform(op, vec_cpld, op_dx, vec_cpld_dx)
         for lab, (op, op_dx) in uncpld_ops.items()},
        [len(set(symbol.qn[op] for symbol in space)) for op in uncpld_ops],
        [max(int(symbol.mult[op]) for symbol in space) for op in uncpld_ops],
        blk_cpld
    )

    vec, vec_dx = op_multiply(vec_cpld, vec_uncpld, vec_cpld_dx, vec_uncpld_dx)

    if verbose:
        op_dict = {lab: unitary_transform(op, vec, op_dx, vec_dx)
                   for lab, (op, op_dx) in {**cpld_ops, **uncpld_ops}.items()}

        # plot angmom matrices and transformation

        ut.plot_op([vec], "vec.pdf")

        for lab, (op, op_dx) in op_dict.items():
            titles = [comp + "-component" for comp in ["x", "y", "z"]]
            ut.plot_op(op, lab + ".pdf", sq=True, titles=titles)

            if op_dx is not None:
                ut.plot_op(op_dx, lab + "_dx.pdf", sq=True, titles=titles)

        if vec_dx is not None:
            ut.plot_op([vec_dx], "vec_dx.pdf")

        # print angmom basis and composition of input states

        qn_dict = {op + comp: np.sqrt(
            1/4 + np.diag(cartesian_op_squared(op_dict[op][0])[0].real)) - 1/2
            if comp == '2' else np.diag(op_dict[op][0][2]).real
            for op, comp in out_basis}

        def form_frac(rat, signed=True):
            return ('+' if rat > 0 and signed else '') + str(Fraction(rat))

        print("Angular momentum basis:")
        hline = 12 * "-" + "----".join([13 * "-"] * len(out_basis))

        print(hline)
        print(12 * " " + " || ".join(
            ["{:^13}".format(op) for op in out_basis]))

        print(hline)
        for idx, vals in enumerate(basis_labs, start=1):
            print(f"state {idx:4d}: " + " || ".join(
                ["{:>5} ({:5.2f})".format(
                    form_frac(getattr(basis_labs[idx-1], op),
                              signed=False if op[1] == '2' else True),
                    qn_dict[op][idx-1])
                 for op in out_basis]))

        print(hline)
        print("Basis labels - state N: [[<theo qn> (<approx qn>)] ...]")

        print()

        print("------------------------")
        print("Input basis composition:")
        print("------------------------")

        composition = np.real(vec * vec.conj())

        for idx, comp in enumerate(composition, start=1):

            # generate states and sort by amplitude
            super_position = sorted(
                ((amp * 100,
                  tuple(form_frac(
                      getattr(basis_labs[adx], op),
                      signed=False if op[1] == '2' else True)
                        for op in out_basis))
                 for adx, amp in enumerate(comp) if amp > comp_thresh),
                key=lambda item: item[0],
                reverse=True)

            print(f"input state {idx:4d}:  " +
                  '  +  '.join("{:.2f}% |{}>".format(amp, ', '.join(state))
                               for amp, state in super_position))

        print("------------------------")
        print("angular momentum kets - " + "|{}>".format(
            ', '.join(''.join(op) for op in out_basis)))
        print()

    return basis_labs, (vec, vec_dx)


def block_cg_trafo(uncpld_qn, cpld_qn, *blks):

    uncpld_blks = extract_blocks(uncpld_qn, blks[0])
    cpld_blks = extract_blocks(cpld_qn, blks[1])

    vec_blks = [cg_trafo(*blk) for blk in zip(uncpld_blks, cpld_blks)]
    vec = from_blocks(vec_blks, *blks)

    return vec


def cg_trafo(uncpld_qn, cpld_qn):
    """Clebsch-Gordan addition of uncoupled angular momentum operators.

    Parameters
    ----------
    uncpld_qn : list of tuples
        List containing the J1^2, J1z, J2^2, J2z uncoupled quantum numbers.
    cpld_qn : list of tuples
        List containing pairs of J^2, Jz coupled quantum numbers.

    Returns
    -------
    np.array
        Clebsch-Gordan transformation matrix.
    """

    vec = np.array([[CG(*j1j2, *j).doit() for j in cpld_qn]
                    for j1j2 in uncpld_qn]).astype(float)

    return vec
