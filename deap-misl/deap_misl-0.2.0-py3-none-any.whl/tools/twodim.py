import random
import math

def cxTwoPoint2d(ind1, ind2):
    """Executes a 2D two-point crossover on the input individuals.
    The two individuals are modified in place and both keep their
    original length.

    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :returns: A tuple of two individuals.

    This function uses the :func:`~random.randint` function from the
    Python base :mod:`random` module.
    """
    row_size = len(ind1)
    col_size = len(ind1[0])
    
    cx_row1 = random.randint(0, row_size - 1)
    cx_row2 = random.randint(0, row_size - 1)
    if cx_row2 >= cx_row1:
        cx_row2 += 1
    else:
        cx_row1, cx_row2 = cx_row2, cx_row1
    
    cx_col1 = random.randint(0, col_size)
    cx_col2 = random.randint(0, col_size - 1)
    if cx_col2 >= cx_col1:
        cx_col2 += 1
    else:
        cx_col1, cx_col2 = cx_col2, cx_col1
    
    for i in range(cx_row1, cx_row2):
        ind1[i][cx_col1:cx_col2], ind2[i][cx_col1:cx_col2] \
            = ind2[i][cx_col1:cx_col2], ind1[i][cx_col1:cx_col2]
    
    return ind1, ind2

def cx2d(ind1, ind2, area_max, rounding=round):
    """Executes a 2D(area) crossover on the input individuals.
    The two individuals are modified in place and both keep their
    original length.

    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :param area_max: maximum value for area.
    :param rounding: Rounding method after the decimal point.
    :returns: A tuple of two individuals.

    This function uses the :func:`~random.randint` function from the
    Python base :mod:`random` module.
    """
    row_size = len(ind1)
    col_size = len(ind1[0])

    area = random.randint(1, area_max)

    # calcurate min value to ensure col_len <= col_size
    row_min = math.ceil(area / col_size)
    row_max = min(area, row_size)
    row_len = random.randint(row_min, row_max)
    row_start = random.randint(0, row_size - row_len)
    cx_row1 = row_start
    cx_row2 = row_start + row_len

    col_len = rounding(area / (cx_row2 - cx_row1))
    col_start = random.randint(0, col_size - col_len)
    cx_col1 = col_start
    cx_col2 = col_start + col_len

    for i in range(cx_row1, cx_row2):
        ind1[i][cx_col1:cx_col2], ind2[i][cx_col1:cx_col2] \
            = ind2[i][cx_col1:cx_col2], ind1[i][cx_col1:cx_col2]
    
    return ind1, ind2

def cxSimple2dExtend(ind1, ind2, cx1d):
    """Executes a simple 2D extended crossover on the input individuals.

    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :param cx1d: Crossover function for each row.
    :returns: A tuple of two individuals.
    """
    row_size = len(ind1)
    for i in range(row_size):
        cx1d(ind1[i], ind2[i])
    return ind1, ind2

def mutSimple2dExtend(individual, mut1d):
    """Executes a simple 2D extended mutation on the input individual
    and return the mutant.

    :param individual: Individual to be mutated.
    :param mutate1d: Mutation function for each row.
    :returns: A tuple of one individual.
    """
    for row in individual:
        mut1d(row)
    return individual,
