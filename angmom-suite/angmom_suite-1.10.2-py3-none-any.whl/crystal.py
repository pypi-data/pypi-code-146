"""
This module contains functions for working with crystal field Hamiltonians
"""

from functools import reduce, lru_cache
from itertools import product
from collections import namedtuple
import numpy as np
import numpy.linalg as la
from sympy.physics.wigner import wigner_3j, wigner_6j
import scipy.special as ssp
from . import utils as ut
from .basis import apply_unary, apply_subset, apply_binary, \
    unitary_transform, cartesian_op_squared, find_angm_basis, \
    calc_ang_mom_ops, find_blks_thresh, block_transformation, \
    eigh_perturbation
from .multi_electron import Term, Level  # , Symbol


N_TOTAL_CFP_BY_RANK = {2: 5, 4: 14, 6: 27}
RANK_BY_N_TOTAL_CFP = {val: key for key, val in N_TOTAL_CFP_BY_RANK.items()}


@lru_cache(maxsize=None)
def recursive_a(k, q, m):
    """
    Given k,q,m this function
    calculates and returns the a(k,q-1,m)th
    Ryabov coefficient by recursion

    Parameters
    ----------
    k : int
        k value (rank)
    q : int
        q value (order)
    m : int
        m value

    Returns
    -------
    np.ndarray
        a(k,q,m) values for each power of X=J(J+1) (Ryabov) up to k+1
    """

    coeff = np.zeros(k+1)

    # Catch exceptions/outliers and end recursion
    if k == q-1 and m == 0:
        coeff[0] = 1
    elif q-1 + m > k:
        pass
    elif m < 0:
        pass
    else:
        # First and second terms
        coeff += (2*q+m-1)*recursive_a(k, q+1, m-1)
        coeff += (q*(q-1) - m*(m+1)/2) * recursive_a(k, q+1, m)

        # Third term (summation)
        for n in range(1, k-q-m+1):
            # First term in sum of third term
            coeff[1:] += (-1)**n * (
                            ut.binomial(m+n, m) * recursive_a(k, q+1, m+n)[:-1]
                        )
            # Second and third term in sum
            coeff += (-1)**n * (
                        - ut.binomial(m+n, m-1) - ut.binomial(m+n, m-2)
                    ) * recursive_a(k, q+1, m+n)

    return coeff


def get_ryabov_a_coeffs(k_max):

    """
    Given k_max this function calculates all possible values
    of a(k,q,m) for each power (i) of X=J(J+1)

    Parameters
    ----------
    k_max : int
        maximum k (rank) value

    Returns
    -------
    np.ndarray
        All a(k,q,m,i)
    np.ndarray
        Greatest common factor of each a(k,q,:,:)
    """

    a = np.zeros([k_max, k_max+1, k_max+1, k_max+1])
    f = np.zeros([k_max, k_max+1])

    # Calculate all a coefficients
    for k in range(1, k_max + 1):
        for qit, q in enumerate(range(k, -1, -1)):
            for m in range(k-q + 1):
                a[k-1, qit, m, :k+1] += recursive_a(k, q+1, m)

    # Calculate greatest common factor F for each a(k,q) value
    for k in range(1, k_max + 1):
        for qit, q in enumerate(range(k, -1, -1)):
            allvals = a[k-1, qit, :, :].flatten()
            nzind = np.nonzero(allvals)
            if np.size(nzind) > 0:
                f[k-1, qit] = reduce(ut.GCD, allvals[nzind])

    return a, f


def calc_stev_ops(k_max, J, jp, jm, jz):
    """
    Calculates all Stevens operators Okq with k even and odd from k=1 to k_max
    k_max must be <= 12 (higher rank parameters require quad precision floats)

    Parameters
    ----------
    k_max : int
        maximum k value (rank)
    J : int
        J quantum number
    jp : np.array
        Matrix representation of angular momentum operator
    jm : np.array
        Matrix representation of angular momentum operator
    jz : np.array
        Matrix representation of angular momentum operator

    Returns
    -------
    np.ndarray
        Stevens operators shape = (n_k, n_q, (2J+1), (2J+1))
            ordered k=1 q=-k->k, k=2 q=-k->k ...
    """

    # Only k <= 12 possible at double precision
    k_max = min(k_max, 12)

    # Get a(k,q,m,i) coefficients and greatest common factors
    a, f = get_ryabov_a_coeffs(k_max)

    # Sum a(k,q,m,i) coefficients over powers of J to give a(k,q,m)
    a_summed = np.zeros([k_max, k_max+1, k_max+1])

    for i in range(0, k_max+1):
        a_summed += a[:, :, :, i] * (J*(J+1))**i

    _jp = np.complex128(jp)
    _jm = np.complex128(jm)
    _jz = np.complex128(jz)

    n_states = int(2*J+1)

    okq = np.zeros([k_max, 2*k_max+1, n_states, n_states], dtype=np.complex128)

    # Calulate q operators both + and - at the same time
    for kit, k in enumerate(range(1, k_max + 1)):
        # New indices for q ordering in final okq array
        qposit = 2*k + 1
        qnegit = -1
        for qit, q in enumerate(range(k, -1, -1)):
            qposit -= 1
            qnegit += 1
            if k % 2:  # Odd k, either odd/even q
                alpha = 1.
            elif q % 2:  # Even k, odd q
                alpha = 0.5
            else:  # Even k, even q
                alpha = 1.

            # Positive q
            for m in range(k-q + 1):
                okq[kit, qposit, :, :] += a_summed[kit, qit, m]*(
                    (
                        la.matrix_power(_jp, q)
                        + (-1.)**(k-q-m)*la.matrix_power(_jm, q)
                    ) @ la.matrix_power(_jz, m)
                )

            okq[kit, qposit, :, :] *= alpha/(2*f[kit, qit])

            # Negative q
            if q != 0:
                for m in range(k-q + 1):
                    okq[kit, qnegit, :, :] += a_summed[kit, qit, m]*(
                        (
                            la.matrix_power(_jp, q)
                            - (-1.)**(k-q-m)*la.matrix_power(_jm, q)
                        ) @ la.matrix_power(_jz, m)
                    )

                okq[kit, qnegit, :, :] *= alpha/(2j*f[kit, qit])

    return okq


def load_CFPs(f_name, style="phi", k_parity="even"):
    """
    Loads Crystal Field Parameters (CFPs) from file

    Parameters
    ----------
    f_name : str
        file name to load CFPs from
    style : str {'phi','raw'}
        Style of CFP file:
            Phi = Chilton's PHI Program input file
            raw = list of CFPs arranged starting with smallest value of k
                  following the scheme k=k_min q=-k->k, k=k_min+1 q=-k->k ...
    k_parity : str {'even', 'odd', 'both'}
        Indicates type of k values
            e.g. k=2,4,6,... or k=1,3,5,... or k=1,2,3...

    Returns
    -------
    np.ndarray
        CFPs with shape = (n_k, n_q)
            ordered k=k_min q=-k->k, k=k_min+mod q=-k->k ...
            where mod is 1 or 2 depending upon k_parity
    """

    _CFPs = []
    if style == "phi":
        # PHI does not support odd rank cfps
        k_parity = "even"
        # Read in CFPs, and k and q values
        kq = []
        # site, k, q, Bkq
        with open(f_name, 'r') as f:
            for line in f:
                if '****crystal' in line.lower():
                    line = next(f)
                    while "****" not in line:
                        kq.append(line.split()[1:3])
                        _CFPs.append(line.split()[3])
                        line = next(f)
                    break
        kq = [[int(k), int(q)] for [k, q] in kq]
        _CFPs = np.array([float(CFP) for CFP in _CFPs])

        # Include zero entries for missing CFPs
        # and reorder since PHI files might be in wrong order

        # find largest k and use to set size of array
        k_max = np.max(kq[0])
        n_cfps = np.sum([2*k + 1 for k in range(k_max, 0, -1)])
        CFPs = np.zeros([n_cfps])
        if k_parity == "even":
            for CFP, [k, q] in zip(_CFPs, kq):
                CFPs[_even_kq_to_num(k, q)] = CFP
        elif k_parity == "odd":
            for CFP, [k, q] in zip(_CFPs, kq):
                CFPs[_odd_kq_to_num(k, q)] = CFP
        else:
            for CFP, [k, q] in zip(_CFPs, kq):
                CFPs[_kq_to_num(k, q)] = CFP

    elif style == "raw":
        CFPs = np.loadtxt(f_name)

    return CFPs


def calc_HCF(J, cfps, stev_ops, k_max=False, oef=[]):
    """
    Calculates and diagonalises crystal field Hamiltonian (HCF)
    using CFPs Bkq and Stevens operators Okq, where k even and ranges 2 -> 2j

    Hamiltonian is sum_k (sum_q (oef_k*Bkq*Okq))

    Parameters
    ----------
    J : float
        J quantum number
    cfps : np.array
        Even k crystal Field parameters, size = (n_k*n_q)
        ordered k=2 q=-k->k, k=4 q=-k->k ...
    np.ndarray
        Stevens operators, shape = (n_k, n_q, (2J+1), (2J+1))
        ordered k=2 q=-k->k, k=4 q=-k->k ...
    k_max : int, default = 2*J
        Maximum value of k to use in summation
    oef : np.ndarray, optional
        Operator equivalent factors for each CFP i.e. 27 CFPs = 27 OEFs
        size = (n_k*n_q), ordered k=2 q=-k->k, k=4 q=-k->k ...

    Returns
    -------
    np.array
        Matrix representation of Crystal Field Hamiltonian (HCF)
    np.array
        Eigenvalues of HCF (lowest eigenvalue is zero)
    np.array
        Eigenvectors of HCF
    """

    if not k_max:
        k_max = int(2*J)
        k_max -= k_max % 2
        k_max = min(k_max, 12)

    if not len(oef):
        oef = np.ones(cfps.size)

    # calculate number of states
    n_states = int(2 * J + 1)

    # Form Hamiltonian
    HCF = np.zeros([n_states, n_states], dtype=np.complex128)
    for kit, k in enumerate(range(2, k_max+1, 2)):
        for qit, q in enumerate(range(-k, k+1)):
            HCF += stev_ops[kit, qit, :, :] * cfps[_even_kq_to_num(k, q)] \
                    * oef[_even_kq_to_num(k, q)]

    # Diagonalise
    CF_val, CF_vec = la.eigh(HCF)

    # Set ground energy to zero
    CF_val -= CF_val[0]

    return HCF, CF_val, CF_vec


def calc_oef(n, J, L, S):
    """
    Calculate operator equivalent factors for Stevens Crystal Field
    Hamiltonian in |J, mJ> basis

    Using the approach of
    https://arxiv.org/pdf/0803.4358.pdf

    Parameters
    ----------
    n : int
        number of electrons in f shell
    J : float
        J Quantum number
    L : int
        L Quantum number
    S : float
        S Quantum number

    Returns
    -------
    np.ndarray
        operator equivalent factors for each parameter, size = (n_k*n_q)
        ordered k=2 q=-k->k, k=4 q=-k->k ...
    """

    def _oef_lambda(p, J, L, S):
        lam = (-1)**(J+L+S+p)*(2*J+1)
        lam *= wigner_6j(J, J, p, L, L, S)/wigner_3j(p, L, L, 0, L, -L)
        return lam

    def _oef_k(p, k, n):
        K = 7. * wigner_3j(p, 3, 3, 0, 0, 0)
        if n <= 7:
            n_max = n
        else:
            n_max = n-7
            if k == 0:
                K -= np.sqrt(7)

        Kay = 0
        for j in range(1, n_max+1):
            Kay += (-1.)**j * wigner_3j(k, 3, 3, 0, 4-j, j-4)

        return K*Kay

    def _oef_RedJ(J, p):
        return 1./(2.**p) * (ssp.factorial(2*J+p+1)/ssp.factorial(2*J-p))**0.5

    # Calculate OEFs and store in array
    # Each parameter Bkq has its own parameter
    oef = np.zeros(27)
    k_max = np.min([6, int(2*J)])
    shift = 0
    for k in range(2, k_max+2, 2):
        oef[shift:shift + 2*k+1] = float(_oef_lambda(k, J, L, S))
        oef[shift:shift + 2*k+1] *= float(_oef_k(k, k, n) / _oef_RedJ(J, k))
        shift += 2*k + 1

    return oef


def calc_order_strength(params: list[float]) -> list[float]:
    """
    Calculates per-order strength parameter S_q for a set of Stevens parameters
    up to rank 6
    """

    max_rank = get_max_rank(params)

    # Convert Stevens parameters to Wybourne scheme
    wparams = abs(stevens_to_wybourne(params, max_rank))

    square_params = wparams ** 2

    # Calculate strength within order (S_q)

    sq = np.zeros(len(params))

    # Rank 2 contributions
    sq[0] = 1./5. * square_params[2]
    sq[1] = 1./5. * square_params[3]
    sq[2] = 1./5. * square_params[4]

    # Rank 4 contributions
    if max_rank > 2:
        sq[0] += 1./9. * square_params[9]
        sq[1] += 1./9. * square_params[10]
        sq[2] += 1./9. * square_params[11]
        sq[3] += 1./9. * square_params[12]
        sq[4] += 1./9. * square_params[13]

    # Rank 6 contributions
    if max_rank > 4:
        sq[6] += 1./13. * square_params[26]
        sq[5] += 1./13. * square_params[25]
        sq[4] += 1./13. * square_params[24]
        sq[3] += 1./13. * square_params[23]
        sq[2] += 1./13. * square_params[22]
        sq[1] += 1./13. * square_params[21]
        sq[0] += 1./13. * square_params[20]

    sq = np.sqrt(sq)

    return sq


def calc_rank_strength(params: list[float]) -> list[float]:
    """
    Calculates per-rank strength parameter S^k for a set of Stevens parameters
    up to rank 6
    """

    max_rank = get_max_rank(params)

    # Convert Stevens parameters to Wybourne scheme
    wparams = abs(stevens_to_wybourne(params, max_rank))

    # Calculate strength within rank (S^k)
    sk2 = np.sqrt(np.sum(wparams[:5]**2) / 5.)
    sk4 = np.sqrt(np.sum(wparams[5:14]**2) / 9.)
    sk6 = np.sqrt(np.sum(wparams[14:]**2) / 13.)

    sk = np.array([sk2, sk4, sk6])

    return sk


def calc_total_strength(params: list[float]) -> float:
    """
    Calculates strength parameter S for a set of Stevens parameters up to
    rank 6
    """

    sk = calc_rank_strength(params)

    # Calculate overall strength as weighted sum of S^k values
    S = np.array(np.sqrt(1./3.*(sk[0]**2 + sk[1]**2 + sk[2]**2)))

    return S


def get_max_rank(params):
    """
    Finds maximum rank in a set of parameters, assumes parameters are ordered
    k=2, q=-2...2, k=4, q=-4, ..., 4...
    """

    try:
        max_rank = RANK_BY_N_TOTAL_CFP[len(params)]
    except ValueError:
        raise ValueError("Incorrect number of CFPs")

    return max_rank


def stevens_to_wybourne(CFPs, k_max):
    """
    Transforms Crystal Field parameters from Wybourne notation to
    Stevens notation

    Assumes only even Ranks (k) are present

    Parameters
    ----------
        CFPs : np.ndarray
            CFPs in Stevens notation, shape = (n_k, n_q)
            ordered k=1 q=-k->k, k=2 q=-k->k ...
        k_max : int
            maximum value of k (rank)

    Returns
    -------
        np.ndarray, dtype=complex128
            CFPs in Wybourne notation, shape = (n_k, n_q)
    """

    if k_max > 6:
        raise ValueError("Cannot convert k>6 parameters to Wybourne")

    # Taken from Mulak and Gajek
    lmbda = [
        np.sqrt(6.)/3.,
        -np.sqrt(6.)/6.,
        2.,
        -np.sqrt(6.)/6.,
        np.sqrt(6.)/3.,
        4.*np.sqrt(70.)/35.,
        -2.*np.sqrt(35.)/35.,
        2.*np.sqrt(10.)/5.,
        -2*np.sqrt(5.)/5.,
        8.,
        -2.*np.sqrt(5.)/5.,
        2.*np.sqrt(10.)/5.,
        -2.*np.sqrt(35.)/35.,
        4.*np.sqrt(70.)/35.,
        16.*np.sqrt(231.)/231.,
        -8.*np.sqrt(77.)/231.,
        8.*np.sqrt(14.)/21.,
        -8.*np.sqrt(105.)/105.,
        16.*np.sqrt(105.)/105.,
        -4.*np.sqrt(42.)/21.,
        16.,
        -4.*np.sqrt(42.)/21.,
        16.*np.sqrt(105.)/105.,
        -8.*np.sqrt(105.)/105.,
        8.*np.sqrt(14.)/21.,
        -8.*np.sqrt(77.)/231.,
        16.*np.sqrt(231.)/231.
    ]

    w_CFPs = np.zeros(N_TOTAL_CFP_BY_RANK[k_max], dtype=np.complex128)

    for k in range(2, k_max + 2, 2):
        for q in range(-k, k + 1):
            ind = _even_kq_to_num(k, q)
            neg_ind = _even_kq_to_num(k, -q)
            if q == 0:
                w_CFPs[ind] = lmbda[ind] * CFPs[ind]
            elif q > 0:
                w_CFPs[ind] = lmbda[ind]*(CFPs[ind] + 1j*CFPs[neg_ind])
            elif q < 0:
                w_CFPs[ind] = lmbda[ind]*(-1)**q*(CFPs[neg_ind] - 1j*CFPs[ind])

    return w_CFPs


def _even_kq_to_num(k, q):
    """
    Converts Rank (k) and order (q) to array index
    Assuming that only even ranks are present

    Parameters
    ----------
        k : int
            Rank k
        q : int
            Order q

    Returns
    -------
        int
            Array index
    """

    index = k + q
    for kn in range(1, int(k/2)):
        index += 2*(k-2*kn) + 1

    return index


def _odd_kq_to_num(k, q):
    """
    Converts Rank (k) and order (q) to array index
    Assuming that only odd ranks are present

    Parameters
    ----------
        k : int
            Rank k
        q : int
            Order q

    Returns
    -------
        int
            Array index
    """

    index = 0
    for kn in range(1, k, 2):
        index += 2*kn + 1

    index += q + k + 1

    return index


def _kq_to_num(k, q):
    """
    Converts Rank (k) and order (q) to array index
    Assuming that all ranks are present

    Parameters
    ----------
        k : int
            Rank k
        q : int
            Order q

    Returns
    -------
        int
            Array index
    """

    index = -1
    for kn in range(1, k):
        index += 2*kn + 1
    index += q + k + 1

    return index


K_MAX = 15

stevens_kq_indices = tuple(
        (k, q)
        for k in range(2, K_MAX, 2)
        for q in range(-k, k+1)
)


def rotate_angm(op, quax):
    return np.einsum('ij,imn', quax.T, op)


class SpinHamiltonian:
    """Set up model spin Hamiltonian to be fitted to ab initio Hamiltonian in
    angular momentum basis.
    The model might be composed of: H = V_0 + H_so + H_ex + H_cf + H_zee
    (V_0: diagonal shift, H_so: spin-orbit coupling, H_ex: exchange coupling,
    H_cf: CF interaction, H_zee: Zeeman effect).

    Parameters
    ----------
    symbol : obj
        Symbol object specifying the angular momentum space.
    angm_ops : dict, default = None
        Dictionary of angm operators. Keys are the angm operator labels. If
        omitted, exact operators are used.
    k_max : int, default = 6
        Maximum Stevens operator rank used in crystal field Hamiltonian.
    theta : bool, default = False
        If True, factor out operator equivalent factors theta.
    iso_soc : bool
        If True, SOC interaction is described by isotropic operator.
    time_reversal_symm : ["even", "odd"], default "even"
        If "even" ("odd"), only include exchange terms which are "even" ("odd")
        under time reversal.
    ion : object, default = None
        Ion object for operator equivalent factor lookup.
    **terms: keyword arguments
        Terms to include in the model Hamiltonian specified as:
            spin-orbit coupling: soc=[("L", "S")]
            crystall field: cf=["L"]
            exchange: ex=[("R", "S"), ("R", "L"), ("R", "S", "L")]
            Zeeman: NOT IMPLEMENTED YET!

    Attributes
    ----------
    symbol : obj
        Symbol object specifying the angular momentum space.
    angm : dict
        Dictionary of angm operators. Keys are the angm operator labels.
    k_max : int
        Maximum Stevens operator rank used in crystal field Hamiltonian.
    theta : bool, default = False
        If true, factor out operator equivalent factors theta.
    ion : object, default = None
        Ion object for operator equivalent factor lookup.
    term_dict : dict of dicts
        Dictionary of terms. Each entry of sub-dict is a contribution to the
        model Hamiltonian associated with a parameter.
    term_len : dict
        Dictionary of number of parameter of each term in model Hamiltonian.
    """

    def __init__(self, symbol, angm_ops=None, ion=None, k_max=6, theta=False,
                 iso_soc=True, time_reversal_symm="even", **terms):

        self.symbol = symbol
        self.ion = ion

        self.angm = \
            {o: tuple(angm_ops[o]) + (angm_ops[o][0] + 1.j * angm_ops[o][1],
                                      angm_ops[o][0] - 1.j * angm_ops[o][1],
                                      cartesian_op_squared(angm_ops[o])[0])
             if angm_ops is not None and o in angm_ops else
             calc_ang_mom_ops(qn) for o, qn in self.symbol.qn.items()}

        self.k_max = k_max
        self.theta = theta
        self.iso_soc = iso_soc
        self.time_reversal_symm = time_reversal_symm

        print(f"Including time-reversal {self.time_reversal_symm} terms.")

        # build model Hamiltonian
        self.term_dict = {"diag": self._build_diag()}
        self.term_len = {"diag": 1}

        resolve = {
            "soc": self._build_soc,
            "cf": self._build_cf,
            "ex": self._build_ex
        }

        for term, sub in terms.items():
            for ops in sub:
                new_term = resolve[term](ops)
                self.term_len[(term, ops)] = len(new_term)
                self.term_dict[(term, ops)] = new_term

    def print_basis(self):
        print(self.symbol.states)

    def _build_diag(self):
        return {"shift": reduce(
            np.kron, [np.identity(m) for m in self.symbol.mult.values()])}

    def _build_soc(self, ops):

        if self.iso_soc:
            Key = namedtuple('Order', 'power')
            return {Key(i+1): np.linalg.matrix_power(
                np.sum([reduce(np.kron,
                               [self.angm[o][c] if o in ops else np.identity(m)
                                for o, m in self.symbol.mult.items()])
                       for c in range(3)], axis=0), i + 1)
                    for i in range(self.symbol.mult[ops[1]] - 1)}
        else:
            return {(i, c): np.linalg.matrix_power(
                [reduce(np.kron,
                        [self.angm[o][c] if o in ops else np.identity(m)
                         for o, m in self.symbol.mult.items()])],
                i + 1)
                    for i in range(self.symbol.mult[ops[1]] - 1)
                    for c in range(3)}

    def _build_cf(self, op):
        # todo: add operator eq factors

        Okq = \
            calc_stev_ops(self.k_max, (self.symbol.mult[op] - 1) / 2,
                          self.angm[op][3], self.angm[op][4], self.angm[op][2])

        Key = namedtuple('O', 'k q')
        return {Key(k, q):
                reduce(np.kron,
                       [Okq[k - 1, k + q, ...] *
                        (self.ion.theta(o.lower())[k] if self.theta else 1.0)
                        if o == op else np.identity(m)
                        for o, m in self.symbol.mult.items()])
                for k in range(2, self.k_max + 1, 2) for q in range(-k, k + 1)}

    def _build_ex(self, ops):

        def time_rev_symm(ranks):
            if self.time_reversal_symm == "even":
                return not sum(ranks) % 2
            elif self.time_reversal_symm == "odd":
                return sum(ranks) % 2
            else:
                return True

        Okqs = {o: calc_stev_ops(
            self.symbol.mult[o] - 1, self.symbol.qn[o],
            self.angm[o][3], self.angm[o][4], self.angm[o][2]) for o in ops}

        kdc = (dict(zip(ops, idc))
               for idc in product(*(range(1, self.symbol.mult[o])
                                    for o in ops)))

        # generator of orders
        def qdc(kdx):
            return (dict(zip(ops, idc))
                    for idc in product(
                        *(range(-k, k + 1) for k in kdx.values())))

        # filter even sums of ranks
        Key = namedtuple('O', 'k q')
        return {tuple(Key(*key) for key in zip(k.values(), q.values())):
                (-1) * reduce(np.kron,
                              [Okqs[o][k[o] - 1, k[o] + q[o], ...] /
                               (1.0 if o.upper() == 'R' else
                                Okqs[o][k[o] - 1, k[o], -1, -1])  # IC scalar
                               if o in ops else np.identity(m)
                               for o, m in self.symbol.mult.items()])
                for k in kdc for q in qdc(k) if time_rev_symm(k.values())}

    def project(self, H_ai, verbose=False):
        """Project ab initio Hamiltonian onto model.

        Parameters
        ----------
        H_ai : np.array
            Ab initio Hamiltonian in the appropiate basis. (Ordering according
            to basis_mult argument of constructor.)
        verbose : bool
            Flag for printing information from least squares fit and plot
            original and fitted Hamiltonian matrices.

        Returns
        -------
        dict of dicts
            Dictionary of terms. Each term is a dictionary itself listing all
            projected model parameters. Sub-keys are Stevens operator rank
            order pairs in the same order as defined in the **terms parameters.
        """

        hartree2invcm = 219474.6

        # vectorise and stack
        Amat = np.column_stack([term.flatten()
                                for terms in self.term_dict.values()
                                for term in terms.values()])

        # convert ab initio Hamiltonian to cm^-1 and carry out proj́ection
        _H_ai = H_ai * hartree2invcm
        bvec = _H_ai.flatten()
        param, res_err, rnk, _ = np.linalg.lstsq(Amat, bvec, rcond=None)

        if verbose:
            print("Linear system of {} equations and {} unknowns".format(
                *Amat.shape))

            if Amat.shape[1] != rnk:
                print(f"Warning: Rank-deficiency detected, rank = {rnk}")

            elif not res_err:
                print("Warning: over-determined system")

            else:
                print("Absolute err (RMSD, i.e. sqrt[1/N^2 * sum of squared "
                      "residuals])\n{:10.4f}".format(
                          np.sqrt(res_err[0] / bvec.size)))
                print("Relative err (sqrt[sum of squared residuals] / "
                      "norm of ab initio Hamiltonian)\n{:10.4%}".format(
                          np.sqrt(res_err[0]) / np.linalg.norm(bvec)))

            H_ai_fit = (Amat @ param).reshape(H_ai.shape)

            ut.plot_op([_H_ai, H_ai_fit], "h_ai.pdf",
                       titles=["Ab initio Hamiltonian", "Model fit"])

            print("Projected parameters in units of cm^-1:")
            for op, num in self.term_len.items():
                if op == 'diag':
                    print("H_{}: {}".format(op, num))
                else:
                    term = op[0]
                    ops = op[1] if term == 'cf' else ", ".join(op[1])
                    print("H_{}({}): {}".format(term, ops, num))

        # extract and organise parameters
        def ranges():
            acc = 0
            for term, size in self.term_len.items():
                yield (term, (acc, acc + size))
                acc = acc + size

        return {term: dict(zip(self.term_dict[term].keys(),
                               param[range(*rng)].real))
                for term, rng in ranges()}


def project_CF(so_ener, so_spin, so_angm, basis, space=None, symbol=None,
               ion=None, k_max=6, theta=False, quax=None, ground=False,
               field=0.0, ener_thresh=1e-7, comp_thresh=0.05, verbose=False,
               so_ener_dx=None, so_spin_dx=None, so_angm_dx=None):
    """Projects crystal field parameters in a given angular momentum basis from
    energies and angular momentum operators in the SO basis.

    Parameters
    ----------
    so_ener : np.array
        Array containing SO energies.
    so_spin : np.array
        Array containing the spin operators.
    so_angm : np.array
        Array containing the orbital angular momentum operators.
    basis : str, {'j', 'l', 'zeeman'}
        Angular momentum basis.
    space : list
        Symbols of the ^(2S+1)L_[J] levels or terms present in the calculation
        in the format "[spin multiplicity][total orbital ang. mom.]
        [total ang. mom.]", e.g 6H15/2 (level), 2F (term).
    symbol : object
        Symbol of the term/level requested for CFP projection.
    ion : object, default = None
        Ion object for operator equivalent factor lookup.
    k_max : int
        Maximum rank of expansion.
    theta : bool, default = False
        If true, factor out operator equivalent factors theta.
    quax : list
        3x3 matrix containig the rotation from the initial to the reference
        quantisation axis frame.
    ground : bool
        Only include the SO states corresponding to the ground multiplet into
        the basis transformation.
    field : float
        Magnetic field in mT applied along the quantisation axis.
    ener_thresh : float
        Energy threshold to classify Kramers doublets in terms of the maximum
        energy difference.
    comp_thresh : float
        Maximum amplitude of a given angular momentum state to be printed in
        the composition section.
    verbose : bool
        Flag for printing LSQ residuals and plotting of angular momentum and
        CF Hamiltonian matrices.
    so_ener_dx : np.array, default=None
        Array containing SO energy derivatives.
    so_spin_dx : np.array, default=None
        Array containing the spin operator derivatives.
    so_angm_dx : np.array, default=None
        Array containing the orbital angular momentum operator derivatives.

    Returns
    -------
    list of np.arrays
        Vector of CFPs ordered by ascending k and q, e.g.
        idx :  0  1  2  3  4    5  6  7  8  9 10 11 12 13   ...
        k   :        2       |              4             |
        q   : -2 -1  0 +1 +2 | -4 -3 -2 -1  0 +1 +2 +3 +4 | ...
    """

    if ground:
        if basis == 'l':  # WIP
            raise NotImplementedError(
                "ground keyword not implemented for l basis.")

        else:
            symbol = ion.ground_level
            lowest = symbol.mult['J']

        space = [symbol]

    else:
        # default symbol: ground term/level
        if basis == 'l':
            symbol = symbol or ion.ground_term
        else:
            space = [level for term in space if isinstance(term, Term)
                     for level in term.levels()] + \
                    [level for level in space if isinstance(level, Level)]
            symbol = symbol or ion.ground_level

        if basis == 'zeeman':
            raise ValueError("Zeeman basis only available for ground=True.")

        lowest = None

    so_ener = [so_ener, so_ener_dx]
    so_spin = [so_spin, so_spin_dx]
    so_angm = [so_angm, so_angm_dx]

    # subset operators
    if lowest is not None:
        subset = np.argsort(so_ener[0])[:lowest]
        so_ener = apply_subset(subset, so_ener)
        so_spin = apply_subset(np.ix_(range(3), subset, subset), so_spin)
        so_angm = apply_subset(np.ix_(range(3), subset, subset), so_angm)

    # rotate operators
    if quax is not None:
        so_spin = apply_unary(rotate_angm, so_spin, quax)
        so_angm = apply_unary(rotate_angm, so_angm, quax)

    ener_diag = apply_unary(np.diag, so_ener)

    # clean up so basis
    if field is not None:
        vec_doublets, vec_doublets_dx = perturb_doublets(
            so_ener[0], so_spin[0], so_angm[0], field=field, verbose=verbose,
            thresh=ener_thresh, ener_dx=so_ener[1], spin_dx=so_spin[1],
            angm_dx=so_angm[1])

        ener_diag = unitary_transform(
            ener_diag[0], vec_doublets, ener_diag[1], vec_doublets_dx)
        so_spin = unitary_transform(
            so_spin[0], vec_doublets, so_spin[1], vec_doublets_dx)
        so_angm = unitary_transform(
            so_angm[0], vec_doublets, so_angm[1], vec_doublets_dx)

    if basis == 'zeeman':  # Hack to diagonalise mag-mom operator
        g_e = 2.002319
        so_spin = apply_unary(lambda x: g_e * x, so_spin)

    # block diagonalisation
    basis_labs, (vec, vec_dx) = find_angm_basis(
        so_spin[0], so_angm[0], space, comp_thresh=comp_thresh,
        verbose=verbose, spin_dx=so_spin[1], angm_dx=so_angm[1])

    # Transform ab initio Hamiltonian to angm basis
    H_ai = unitary_transform(ener_diag[0], vec, ener_diag[1], vec_dx)

    if verbose:
        ut.plot_op([H_ai[0]], "h_ai_full.pdf")
        if H_ai[1] is not None:
            ut.plot_op([H_ai[1]], "h_ai_full_dx.pdf")

    manifold_idc = [basis_labs.index(state) for state in symbol.states]

    model = SpinHamiltonian(symbol, k_max=k_max, theta=theta, ion=ion,
                            cf=['L'] if isinstance(symbol, Term) else ['J'])

    # Subset crystal field Hamiltonian
    H_ai_ss = apply_subset(np.ix_(manifold_idc, manifold_idc), H_ai)
    prms = apply_unary(model.project, H_ai_ss, verbose=verbose)

    return apply_subset(('cf', 'L' if isinstance(symbol, Term) else 'J'), prms)


def perturb_doublets(ener, spin, angm, field=0.0, thresh=1e-7, verbose=False,
                     ener_dx=None, spin_dx=None, angm_dx=None):
    """Split Kramers doublets along quantisation axis by either applying an
    explicit magnetic field or by rotating each doublet into eigenstates of Jz.

    Parameters
    ----------
    ener : np.array
        Array of SO energies in hartree.
    spin : np.array
        Spin operator in the SO basis.
    angm : np.array
        Orbital angular momentum operator in the SO basis.
    field : float
        Magnetic field in mT applied along the quantisation axis.
    thresh : float
        Energy threshold to classify Kramers doublets in terms of the maximum
        energy difference.
    verbose : bool
        Print information about Kramers doublet treatment.
    ener_dx : np.array
        Array of first derivative of the SO energies.
    spin : np.array
        First derivative of the spin operator in the SO basis.
    angm : np.array
        First derivative of the orbital angmom operator in the SO basis.

    Returns
    -------
    tuple of np.arrays
        Pair of transformation matrix and its first derivative.
    """

    if field == 0.0:  # perturbed J basis for each Kramers doublet

        if verbose:
            print("Rotating Kramers doublets into eigenstates of Jz at zero "
                  "field.")

        doublet_blks = next(find_blks_thresh([thresh]))(ener)
        _, (vec, vec_dx) = block_transformation(
                *zip(apply_subset(2, apply_binary(
                    lambda l, s: l + s, [angm, angm_dx], [spin, spin_dx]))),
                blks=list(zip(doublet_blks)))

    else:  # apply magnetic field

        if verbose:
            print(f"Applying magnetic field of {field} mT to split doublets.")

        muB = 0.5  # atomic units
        au2mT = 2.35051756758e5 * 1e3  # mTesla / au
        g_e = 2.002319
        pre = muB * field / au2mT

        # calculate zeeman operator and convert field in mT to T
        zeeman, zeeman_dx = apply_subset(2, apply_binary(
            lambda l, s: l + s,
            apply_unary(lambda l: pre * l, [angm, angm_dx]),
            apply_unary(lambda s: pre * g_e * s, [spin, spin_dx])
        ))

        _, vec, _, vec_dx = eigh_perturbation(*apply_binary(
            lambda e, z: e + z,
            apply_unary(np.diag, [ener, ener_dx]),
            [zeeman, zeeman_dx]
        ))

    return vec, vec_dx
