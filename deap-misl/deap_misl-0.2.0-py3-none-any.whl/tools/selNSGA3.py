# -*- coding: utf-8 -*-
# author:rosawa
import bisect
import math
import random
import numpy as np

from itertools import chain, product, permutations
from operator import attrgetter, itemgetter
from collections import defaultdict
#######################################
# Non-Dominated Sorting   (NSGA-III)  #
#######################################


def selNSGA3(individuals, k, nd='standard', pertition=12):
    """
    NSGA-IIIによる選択を行うメソッド
    リファレンスポイントの総数H = combinations_count(M + p - 1, p)
    pertition(p)の値はリファレンスポイントの数が個体数と等しくなるように設定すること
    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :param nd: Specify the non-dominated algorithm to use: 'standard' or 'log'.
    :param pertition:
    :returns: A list of selected individuals.
    """

    if nd == 'standard':
        pareto_fronts = sortNondominated(individuals, k)
    elif nd == 'log':
        pareto_fronts = sortLogNondominated(individuals, k)
    else:
        raise Exception('selNSGA2: The choice of non-dominated sorting '
                        'method "{0}" is invalid.'.format(nd))
    for front in pareto_fronts:
        assignCrowdingDist(front)
    chosen = list(chain(*pareto_fronts[:-1]))
    st = list(chain(*pareto_fronts))
    k = k - len(chosen)
    zr = createReferencePoint(individuals, pertition)
    zr = adaptiveNormalized(st, zr)
    associate(st, zr)
    tmp_ρ = [ind.fitness.ρi_s for ind in st[:len(chosen)]]
    ρ = np.array([float(tmp_ρ.count(i)) for i in range(len(zr))])
    niching(k, ρ, st[len(chosen):], chosen)
    return chosen


def niching(k, ρ, pareto_fronts, chosen):
    """
    ニッチな個体を選択するメソッド
    :param k: 個体群の数 - 非優越ソートで選択された個体数
    :param ρ: 各リファレンスラインと関連付けされた選択済み個体群の数
    :param pareto_fronts: 非優越ソートで選択されなかった次のフロント
    :param chosen: 非優越ソートで選択済みの個体群
    :return: なし
    """
    while k > 0:  # k(不足個体数)が0になるまで繰り返す
        j_array = np.where(ρ == ρ.min())[0]
        j = random.choice(j_array)
        Ij = [ind for ind in pareto_fronts if ind.fitness.ρi_s == j]
        if Ij != []:
            if ρ[j] == 0:
                Ij.sort(key=attrgetter("fitness.d_s"))
                ch_Ij = Ij[0]
            else:
                ch_Ij = random.choice(Ij)
            chosen.append(ch_Ij)

            for index, ind in enumerate(pareto_fronts):
                if ind is ch_Ij:
                    del pareto_fronts[index]
            ρ[j] += 1
            k -= 1
        else:
            ρ[j] = np.inf


def associate(individuals, zr):
    for ind in individuals:
        u = zr
        v = np.array(ind.fitness.fn)
        if len(ind.fitness.fn) == 2:
            d = np.linalg.norm(u - v, axis=1)
        else:
            d = np.linalg.norm(np.cross(u, v), axis=1) / np.linalg.norm(u, axis=1)
        ρi_s = np.argmin(d)
        d_s = d[ρi_s]

        ind.fitness.ρi_s = ρi_s
        ind.fitness.d_s = d_s


def calc_a(fit, M, k):
    """
    intercepts aを計算するメソッド
    :param fit: 個体群の適合度をndarrayで取り出した配列
    :param M: 目的関数の数
    :param k: 選択済み個体の数
    :return: 原点から極点zmaxと目的関数軸の交点までの大きさ(intercepts a)
    """
    zmin = np.array([m.min() for m in fit.T])
    e = np.zeros([M, M])
    for i in range(M):
        for j in range(M):
            if i == j:
                e[i, j] = 1
    fn = (fit - zmin)
    zmax = np.zeros([M, M])
    smin = np.array([np.inf for i in range(M)])
    for j in range(M):
        w = GetScalarizingVector(M, j)
        s = np.zeros([1, k])
        for i in range(k):
            tmp = fn[i, :].T
            tmp_s = tmp / w
            s[0, i] = tmp_s.max()
        sminj = s.min()
        index = np.argmin(s)
        if sminj < smin[j]:
            zmax[j, :] = fn[index, :]
            smin[j] = sminj
    a = FindHyperplaneIntercepts(zmax)   #　原点から極点zmaxと目的関数軸の交点までの大きさ

    return a, zmin


def adaptiveNormalized(st, zs):
    """
    適応型正規化メソッド
    非優越ソートで選択済みの個体群を用いて目的関数空間を正規化
    正規化されたfitness.valuesをfitness.fn属性で保存
    :param st: F1~Fl個体群
    :param zs: リファレンスポイント構造
    :return: 正規化された超平面上のリファレンスポイント
    """
    all_fit = np.array([ind.fitness.values for ind in st])
    M = len(st[0].fitness.values)
    k = len(st)

    fit = np.array([ind.fitness.values for ind in st])
    a, zmin = calc_a(fit, M, k)
    all_fn = (all_fit - zmin) / a

    for ind, i in zip(st, all_fn):
        ind.fitness.fn = i

    zr = zs

    return zr


def FindHyperplaneIntercepts(zmax):
    """
    正規化に必要なintercepts aを計算するメソッド
    :param zmax: 極点
    :return: intercepts a
    """
    wt = np.ones([1, len(zmax[0])])
    w = wt/zmax
    t = 1 / w
    a = [np.linalg.norm(i) for i in t]
    return a


def GetScalarizingVector(M, j):
    epsilon = 10 ** (-10)
    w = epsilon * np.ones([1, M])
    w[0, j] = 1

    return w


def createReferencePoint(individuals, p=4):
    """
    リファレンスポイントの構造を得るメソッド
    H = combinations_count(M + p - 1, p)の値が個体数と等しくなるようなpを自分で設定すること
    :param individuals: 全個体群
    :param p: リファレンスポイントの分割数
    :return: リファレンスポイントの構造
    """
    M = len(individuals[0].fitness.values)
    tmp = [i for i in range(p + 1)]
    tmp_RP = np.array(list(product(tmp, repeat=M)))
    RP = np.array([i for i in tmp_RP if sum(i) == p]) / p

    return RP


def combinations_count(n, r):
    return math.factorial(n) // (math.factorial(n - r) * math.factorial(r))


def sortNondominated(individuals, k, first_front_only=False):
    """Sort the first *k* *individuals* into different nondomination levels
    using the "Fast Nondominated Sorting Approach" proposed by Deb et al.,
    see [Deb2002]_. This algorithm has a time complexity of :math:`O(MN^2)`,
    where :math:`M` is the number of objectives and :math:`N` the number of
    individuals.
    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :param first_front_only: If :obj:`True` sort only the first front and
                             exit.
    :returns: A list of Pareto fronts (lists), the first list includes
              nondominated individuals.
    .. [Deb2002] Deb, Pratab, Agarwal, and Meyarivan, "A fast elitist
       non-dominated sorting genetic algorithm for multi-objective
       optimization: NSGA-II", 2002.
    """
    if k == 0:
        return []

    map_fit_ind = defaultdict(list)
    for ind in individuals:
        map_fit_ind[ind.fitness].append(ind)
    fits = list(map_fit_ind.keys())

    current_front = []
    next_front = []
    dominating_fits = defaultdict(int)
    dominated_fits = defaultdict(list)

    # Rank first Pareto front
    for i, fit_i in enumerate(fits):
        for fit_j in fits[i+1:]:
            if fit_i.dominates(fit_j):
                dominating_fits[fit_j] += 1
                dominated_fits[fit_i].append(fit_j)
            elif fit_j.dominates(fit_i):
                dominating_fits[fit_i] += 1
                dominated_fits[fit_j].append(fit_i)
        if dominating_fits[fit_i] == 0:
            current_front.append(fit_i)

    fronts = [[]]
    for fit in current_front:
        fronts[-1].extend(map_fit_ind[fit])
    pareto_sorted = len(fronts[-1])

    # Rank the next front until all individuals are sorted or
    # the given number of individual are sorted.
    if not first_front_only:
        N = min(len(individuals), k)
        while pareto_sorted < N:
            fronts.append([])
            for fit_p in current_front:
                for fit_d in dominated_fits[fit_p]:
                    dominating_fits[fit_d] -= 1
                    if dominating_fits[fit_d] == 0:
                        next_front.append(fit_d)
                        pareto_sorted += len(map_fit_ind[fit_d])
                        fronts[-1].extend(map_fit_ind[fit_d])
            current_front = next_front
            next_front = []

    return fronts

def assignCrowdingDist(individuals):
    """Assign a crowding distance to each individual's fitness. The
    crowding distance can be retrieve via the :attr:`crowding_dist`
    attribute of each individual's fitness.
    """
    if len(individuals) == 0:
        return

    distances = [0.0] * len(individuals)
    crowd = [(ind.fitness.values, i) for i, ind in enumerate(individuals)]

    nobj = len(individuals[0].fitness.values)

    for i in range(nobj):
        crowd.sort(key=lambda element: element[0][i])
        distances[crowd[0][1]] = float("inf")
        distances[crowd[-1][1]] = float("inf")
        if crowd[-1][0][i] == crowd[0][0][i]:
            continue
        norm = nobj * float(crowd[-1][0][i] - crowd[0][0][i])
        for prev, cur, next in zip(crowd[:-2], crowd[1:-1], crowd[2:]):
            distances[cur[1]] += (next[0][i] - prev[0][i]) / norm

    for i, dist in enumerate(distances):
        individuals[i].fitness.crowding_dist = dist


def selTournamentDCD(individuals, k):
    """Tournament selection based on dominance (D) between two individuals, if
    the two individuals do not interdominate the selection is made
    based on crowding distance (CD). The *individuals* sequence length has to
    be a multiple of 4. Starting from the beginning of the selected
    individuals, two consecutive individuals will be different (assuming all
    individuals in the input list are unique). Each individual from the input
    list won't be selected more than twice.

    This selection requires the individuals to have a :attr:`crowding_dist`
    attribute, which can be set by the :func:`assignCrowdingDist` function.

    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :returns: A list of selected individuals.
    """

    def tourn(ind1, ind2):
        if ind1.fitness.dominates(ind2.fitness):
            return ind1
        elif ind2.fitness.dominates(ind1.fitness):
            return ind2

        if ind1.fitness.crowding_dist < ind2.fitness.crowding_dist:
            return ind2
        elif ind1.fitness.crowding_dist > ind2.fitness.crowding_dist:
            return ind1

        if random.random() <= 0.5:
            return ind1
        return ind2

    individuals_1 = random.sample(individuals, len(individuals))
    individuals_2 = random.sample(individuals, len(individuals))

    chosen = []
    for i in range(0, k, 4):
        chosen.append(tourn(individuals_1[i], individuals_1[i + 1]))
        chosen.append(tourn(individuals_1[i + 2], individuals_1[i + 3]))
        chosen.append(tourn(individuals_2[i], individuals_2[i + 1]))
        chosen.append(tourn(individuals_2[i + 2], individuals_2[i + 3]))

    return chosen


#######################################
# Generalized Reduced runtime ND sort #
#######################################

def identity(obj):
    """Returns directly the argument *obj*.
    """
    return obj


def isDominated(wvalues1, wvalues2):
    """Returns whether or not *wvalues1* dominates *wvalues2*.

    :param wvalues1: The weighted fitness values that would be dominated.
    :param wvalues2: The weighted fitness values of the dominant.
    :returns: :obj:`True` if wvalues2 dominates wvalues1, :obj:`False`
              otherwise.
    """
    not_equal = False
    for self_wvalue, other_wvalue in zip(wvalues1, wvalues2):
        if self_wvalue > other_wvalue:
            return False
        elif self_wvalue < other_wvalue:
            not_equal = True
    return not_equal


def median(seq, key=identity):
    """Returns the median of *seq* - the numeric value separating the higher
    half of a sample from the lower half. If there is an even number of
    elements in *seq*, it returns the mean of the two middle values.
    """
    sseq = sorted(seq, key=key)
    length = len(seq)
    if length % 2 == 1:
        return key(sseq[(length - 1) // 2])
    else:
        return (key(sseq[(length - 1) // 2]) + key(sseq[length // 2])) / 2.0


def sortLogNondominated(individuals, k, first_front_only=False):
    """Sort *individuals* in pareto non-dominated fronts using the Generalized
    Reduced Run-Time Complexity Non-Dominated Sorting Algorithm presented by
    Fortin et al. (2013).

    :param individuals: A list of individuals to select from.
    :returns: A list of Pareto fronts (lists), with the first list being the
              true Pareto front.
    """
    if k == 0:
        return []

    # Separate individuals according to unique fitnesses
    unique_fits = defaultdict(list)
    for i, ind in enumerate(individuals):
        unique_fits[ind.fitness.wvalues].append(ind)

    # Launch the sorting algorithm
    obj = len(individuals[0].fitness.wvalues) - 1
    fitnesses = list(unique_fits.keys())
    front = dict.fromkeys(fitnesses, 0)

    # Sort the fitnesses lexicographically.
    fitnesses.sort(reverse=True)
    sortNDHelperA(fitnesses, obj, front)

    # Extract individuals from front list here
    nbfronts = max(front.values()) + 1
    pareto_fronts = [[] for i in range(nbfronts)]
    for fit in fitnesses:
        index = front[fit]
        pareto_fronts[index].extend(unique_fits[fit])

    # Keep only the fronts required to have k individuals.
    if not first_front_only:
        count = 0
        for i, front in enumerate(pareto_fronts):
            count += len(front)
            if count >= k:
                return pareto_fronts[:i + 1]
        return pareto_fronts
    else:
        return pareto_fronts[0]


def sortNDHelperA(fitnesses, obj, front):
    """Create a non-dominated sorting of S on the first M objectives"""
    if len(fitnesses) < 2:
        return
    elif len(fitnesses) == 2:
        # Only two individuals, compare them and adjust front number
        s1, s2 = fitnesses[0], fitnesses[1]
        if isDominated(s2[:obj + 1], s1[:obj + 1]):
            front[s2] = max(front[s2], front[s1] + 1)
    elif obj == 1:
        sweepA(fitnesses, front)
    elif len(frozenset(list(map(itemgetter(obj), fitnesses)))) == 1:
        # All individuals for objective M are equal: go to objective M-1
        sortNDHelperA(fitnesses, obj - 1, front)
    else:
        # More than two individuals, split list and then apply recursion
        best, worst = splitA(fitnesses, obj)
        sortNDHelperA(best, obj, front)
        sortNDHelperB(best, worst, obj - 1, front)
        sortNDHelperA(worst, obj, front)


def splitA(fitnesses, obj):
    """Partition the set of fitnesses in two according to the median of
    the objective index *obj*. The values equal to the median are put in
    the set containing the least elements.
    """
    median_ = median(fitnesses, itemgetter(obj))
    best_a, worst_a = [], []
    best_b, worst_b = [], []

    for fit in fitnesses:
        if fit[obj] > median_:
            best_a.append(fit)
            best_b.append(fit)
        elif fit[obj] < median_:
            worst_a.append(fit)
            worst_b.append(fit)
        else:
            best_a.append(fit)
            worst_b.append(fit)

    balance_a = abs(len(best_a) - len(worst_a))
    balance_b = abs(len(best_b) - len(worst_b))

    if balance_a <= balance_b:
        return best_a, worst_a
    else:
        return best_b, worst_b


def sweepA(fitnesses, front):
    """Update rank number associated to the fitnesses according
    to the first two objectives using a geometric sweep procedure.
    """
    stairs = [-fitnesses[0][1]]
    fstairs = [fitnesses[0]]
    for fit in fitnesses[1:]:
        idx = bisect.bisect_right(stairs, -fit[1])
        if 0 < idx <= len(stairs):
            fstair = max(fstairs[:idx], key=front.__getitem__)
            front[fit] = max(front[fit], front[fstair] + 1)
        for i, fstair in enumerate(fstairs[idx:], idx):
            if front[fstair] == front[fit]:
                del stairs[i]
                del fstairs[i]
                break
        stairs.insert(idx, -fit[1])
        fstairs.insert(idx, fit)


def sortNDHelperB(best, worst, obj, front):
    """Assign front numbers to the solutions in H according to the solutions
    in L. The solutions in L are assumed to have correct front numbers and the
    solutions in H are not compared with each other, as this is supposed to
    happen after sortNDHelperB is called."""
    key = itemgetter(obj)
    if len(worst) == 0 or len(best) == 0:
        # One of the lists is empty: nothing to do
        return
    elif len(best) == 1 or len(worst) == 1:
        # One of the lists has one individual: compare directly
        for hi in worst:
            for li in best:
                if isDominated(hi[:obj + 1], li[:obj + 1]) or hi[:obj + 1] == li[:obj + 1]:
                    front[hi] = max(front[hi], front[li] + 1)
    elif obj == 1:
        sweepB(best, worst, front)
    elif key(min(best, key=key)) >= key(max(worst, key=key)):
        # All individuals from L dominate H for objective M:
        # Also supports the case where every individuals in L and H
        # has the same value for the current objective
        # Skip to objective M-1
        sortNDHelperB(best, worst, obj - 1, front)
    elif key(max(best, key=key)) >= key(min(worst, key=key)):
        best1, best2, worst1, worst2 = splitB(best, worst, obj)
        sortNDHelperB(best1, worst1, obj, front)
        sortNDHelperB(best1, worst2, obj - 1, front)
        sortNDHelperB(best2, worst2, obj, front)


def splitB(best, worst, obj):
    """Split both best individual and worst sets of fitnesses according
    to the median of objective *obj* computed on the set containing the
    most elements. The values equal to the median are attributed so as
    to balance the four resulting sets as much as possible.
    """
    median_ = median(best if len(best) > len(worst) else worst, itemgetter(obj))
    best1_a, best2_a, best1_b, best2_b = [], [], [], []
    for fit in best:
        if fit[obj] > median_:
            best1_a.append(fit)
            best1_b.append(fit)
        elif fit[obj] < median_:
            best2_a.append(fit)
            best2_b.append(fit)
        else:
            best1_a.append(fit)
            best2_b.append(fit)

    worst1_a, worst2_a, worst1_b, worst2_b = [], [], [], []
    for fit in worst:
        if fit[obj] > median_:
            worst1_a.append(fit)
            worst1_b.append(fit)
        elif fit[obj] < median_:
            worst2_a.append(fit)
            worst2_b.append(fit)
        else:
            worst1_a.append(fit)
            worst2_b.append(fit)

    balance_a = abs(len(best1_a) - len(best2_a) + len(worst1_a) - len(worst2_a))
    balance_b = abs(len(best1_b) - len(best2_b) + len(worst1_b) - len(worst2_b))

    if balance_a <= balance_b:
        return best1_a, best2_a, worst1_a, worst2_a
    else:
        return best1_b, best2_b, worst1_b, worst2_b


def sweepB(best, worst, front):
    """Adjust the rank number of the worst fitnesses according to
    the best fitnesses on the first two objectives using a sweep
    procedure.
    """
    stairs, fstairs = [], []
    iter_best = iter(best)
    next_best = next(iter_best, False)
    for h in worst:
        while next_best and h[:2] <= next_best[:2]:
            insert = True
            for i, fstair in enumerate(fstairs):
                if front[fstair] == front[next_best]:
                    if fstair[1] > next_best[1]:
                        insert = False
                    else:
                        del stairs[i], fstairs[i]
                    break
            if insert:
                idx = bisect.bisect_right(stairs, -next_best[1])
                stairs.insert(idx, -next_best[1])
                fstairs.insert(idx, next_best)
            next_best = next(iter_best, False)

        idx = bisect.bisect_right(stairs, -h[1])
        if 0 < idx <= len(stairs):
            fstair = max(fstairs[:idx], key=front.__getitem__)
            front[h] = max(front[h], front[fstair] + 1)

