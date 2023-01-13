import random
import numpy

from deap import base
from deap import creator
from deap import tools

from deap_misl import tools as misl_tools

import utils

NUM_ITEMS = 100
weights, profits, capacities, pareto = utils.knapsack.knapsack_100_2()

creator.create("Fitness", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, NUM_ITEMS)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", utils.knapsack.evaluate, weights=weights, profits=profits, capacities=capacities)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", misl_tools.selNSGA2m)

def main():
    MU = 300
    NGEN = 1000
    CXPB = 0.9
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    
    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"
    
    pop = toolbox.population(n=MU)
    
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)

    # assign crowding distance
    pop = toolbox.select(pop, len(pop))

    logbook.record(gen=0, evals=len(pop), **stats.compile(pop))
    print(logbook.stream)
    
    gen = 1
    while gen <= NGEN:
        #chosen_by_variable = False
        #chosen_by_variable = True
        chosen_by_variable = (gen % 2 == 0)

        offspring = misl_tools.selTournamentDCDm(pop, len(pop), chosen_by_variable)
        offspring = [toolbox.clone(ind) for ind in offspring]

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)
            
            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        for ind in invalid_ind:
            ind.fitness.values = toolbox.evaluate(ind)

        pop = toolbox.select(pop + offspring, MU, chosen_by_variable=chosen_by_variable)
            
        logbook.record(gen=gen, evals=len(invalid_ind), **stats.compile(pop))
        print(logbook.stream)
        
        gen += 1
    
    return pop, logbook

if __name__ == "__main__":
    random.seed(64)

    pop, logbook = main()
    pop.sort(key=lambda x: x.fitness.values)

    import matplotlib.pyplot as plt

    front = numpy.array([ind.fitness.values for ind in pop])
    plt.scatter(front[:,0], front[:,1], c="b")

    optimal = numpy.array(pareto)
    plt.scatter(optimal[:,0], optimal[:,1], c="r")

    plt.axis("tight")
    plt.show()
