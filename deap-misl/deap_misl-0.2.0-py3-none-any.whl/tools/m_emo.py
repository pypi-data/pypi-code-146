from __future__ import division
import random

from itertools import chain
from operator import attrgetter

from deap.tools import emo

import functools

######################################
# Non-Dominated Sorting   (NSGA-II)  #
######################################

def selNSGA2m(individuals, k, nd='standard', chosen_by_variable=False):
    """Apply NSGA-II selection operator on the *individuals*. Usually, the
    size of *individuals* will be larger than *k* because any individual
    present in *individuals* will appear in the returned list at most once.
    Having the size of *individuals* equals to *k* will have no effect other
    than sorting the population according to their front rank. The
    list returned contains references to the input *individuals*. For more
    details on the NSGA-II operator see [Deb2002]_.
    
    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :param nd: Specify the non-dominated algorithm to use: 'standard' or 'log'.
    :param chosen_by_variable: Use variable space crowding distance.
    :returns: A list of selected individuals.
    
    .. [Deb2002] Deb, Pratab, Agarwal, and Meyarivan, "A fast elitist
       non-dominated sorting genetic algorithm for multi-objective
       optimization: NSGA-II", 2002.
    """
    if nd == 'standard':
        pareto_fronts = emo.sortNondominated(individuals, k)
    elif nd == 'log':
        pareto_fronts = emo.sortLogNondominated(individuals, k)
    else:
        raise Exception('selNSGA2m: The choice of non-dominated sorting '
                        'method "{0}" is invalid.'.format(nd))

    for front in pareto_fronts:
        emo.assignCrowdingDist(front)
        assignCrowdingDistForVariable(front)
    
    chosen = list(chain(*pareto_fronts[:-1]))
    k = k - len(chosen)
    if k > 0:
        if chosen_by_variable:
            sorted_front = sorted(pareto_fronts[-1], key=attrgetter("crowding_dist"), reverse=True)
        else:
            sorted_front = sorted(pareto_fronts[-1], key=attrgetter("fitness.crowding_dist"), reverse=True)
        chosen.extend(sorted_front[:k])
        
    return chosen

def assignCrowdingDistForVariable(individuals):
    """Assign a crowding distance to each individual's variables. The 
    crowding distance can be retrieve via the :attr:`crowding_dist` 
    attribute of each individual.
    """
    if len(individuals) == 0:
        return
    
    distances = [0.0] * len(individuals)
    crowd = [(ind, i) for i, ind in enumerate(individuals)]
       
    def variable_diff(x, y):
        sum = 0
        for a, b in zip(x, y):
            sum += (a - b)
        return sum

    def mycmp(x, y):
        return variable_diff(x[0], y[0])
    crowd.sort(key=functools.cmp_to_key(mycmp))

    distances[crowd[0][1]] = float("inf")
    distances[crowd[-1][1]] = float("inf")
    if crowd[-1][0] != crowd[0][0]:
        norm = float(abs(variable_diff(crowd[-1][0], crowd[0][0])))
        for prev, cur, next in zip(crowd[:-2], crowd[1:-1], crowd[2:]):
            distances[cur[1]] += abs(variable_diff(next[0], prev[0])) / norm

    for i, dist in enumerate(distances):
        individuals[i].crowding_dist = dist

def selTournamentDCDm(individuals, k, chosen_by_variable=False):
    """Tournament selection based on dominance (D) between two individuals, if
    the two individuals do not interdominate the selection is made
    based on crowding distance (CD). The *individuals* sequence length has to
    be a multiple of 4 only if k is equal to the length of individuals. 
    Starting from the beginning of the selected, individuals, two consecutive
    individuals will be different (assuming all individuals in the input list
    are unique). Each individual from the input list won't be selected more
    than twice.
    
    This selection requires the individuals to have a :attr:`crowding_dist`
    attribute, which can be set by the :func:`assignCrowdingDist` function.
    
    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select. Must be less than or equal 
              to len(individuals).
    :param chosen_by_variable: Use variable space crowding distance.
    :returns: A list of selected individuals.
    """

    if k > len(individuals): 
        raise ValueError("selTournamentDCDm: k must be less than or equal to individuals length")

    if k == len(individuals) and k % 4 != 0:
        raise ValueError("selTournamentDCDm: k must be divisible by four if k == len(individuals)")

    def tourn(ind1, ind2):
        if ind1.fitness.dominates(ind2.fitness):
            return ind1
        elif ind2.fitness.dominates(ind1.fitness):
            return ind2

        if chosen_by_variable:
            if ind1.crowding_dist < ind2.crowding_dist:
                return ind2
            elif ind1.crowding_dist > ind2.crowding_dist:
                return ind1
        else:
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
        chosen.append(tourn(individuals_1[i],   individuals_1[i+1]))
        chosen.append(tourn(individuals_1[i+2], individuals_1[i+3]))
        chosen.append(tourn(individuals_2[i],   individuals_2[i+1]))
        chosen.append(tourn(individuals_2[i+2], individuals_2[i+3]))

    return chosen
