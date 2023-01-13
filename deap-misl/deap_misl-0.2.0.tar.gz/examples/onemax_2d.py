import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from deap_misl import tools as misl_tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("attr_row", tools.initRepeat, list, toolbox.attr_bool, 10)

# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_row, 10)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    return sum([sum(row) for row in individual]),

N = 300
CXPB = 0.5
MUTPB = 0.2
NGEN = 40
AREA_MAX = 50

def adaptive_area_max(count):
    # Crossover is called half the number of individuals.
    # So, we can estimate "current generation" using crossover rate.
    gen = int(count / ((N / 2) * CXPB))
    # Decrement area_max by generation.
    return AREA_MAX - gen

adaptive_cx2d = misl_tools.AdaptiveParameterWrapper(misl_tools.cx2d, "area_max", adaptive_area_max)

toolbox.register("evaluate", evalOneMax)
#toolbox.register("mate", misl_tools.cxTwoPoint2d)
#toolbox.register("mate", misl_tools.cx2d, area_max=AREA_MAX, rounding=round)
toolbox.register("mate", adaptive_cx2d, rounding=round)
toolbox.register("mutate1d", tools.mutFlipBit, indpb=0.05)
toolbox.register("mutate", misl_tools.mutSimple2dExtend, mut1d=toolbox.mutate1d)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    pop = toolbox.population(n=N)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN, 
                                   stats=stats, halloffame=hof, verbose=True)
    
    return pop, log, hof

if __name__ == "__main__":
    random.seed(64)
    main()
