import numpy as np
import math
import random
import operator

from deap import tools

def distance(w1, w2):
    sum = 0.0
    for i in range(len(w1)):
        sum += (w1[i] - w2[i]) ** 2
    return math.sqrt(sum)

def sorting(tobesorted):
    index = [i for i in range(len(tobesorted))]
    for i in range(1, len(tobesorted)):
        for j in range(i):
            if tobesorted[index[i]] < tobesorted[index[j]]:
                temp = index[i]
                for k in range(i-1, j-1, -1):
                    index[k+1] = index[k]
                index[j] = temp
                break
    return index

class MOEAD:
    def initWeight(self, m):
        self.weights = []
        for i in range(m+1):
            if self.numObjectives == 2:
                self.weights.append([i / float(m), (m - i) / float(m)])
            elif self.numObjectives == 3:
                for j in range(m+1):
                    if i + j <= m:
                        k = m - i - j
                        self.weights.append([i / float(m), j / float(m),k / float(m)])
        self.popsize = len(self.weights)

    def initNeighbour(self):
        self.neighbourTable = []
        distancematrix = np.zeros((self.popsize, self.popsize))
        for i in range(self.popsize):
            for j in range(i+1, self.popsize):
                distancematrix[i][j] = distance(self.weights[i], self.weights[j])
                distancematrix[j][i] = distancematrix[i][j]

        for i in range(self.popsize):
            index = sorting(distancematrix[i])
            self.neighbourTable.append(index[:self.neighboursize])

    def createPopulation(self, popsize):
        return self.toolbox.population(n=popsize)

    def evaluateIndividual(self, ind):
        ind.fitness.values = self.toolbox.evaluate(ind)

    def evaluatePopluation(self, mainpop):
        for i in range(len(mainpop)):
            self.evaluateIndividual(mainpop[i])

    def updateReference(self, ind):
        for j in range(len(ind.fitness.values)):
            if ind.fitness.weights[j] > 0:
                if ind.fitness.values[j] > self.idealpoint[j]:
                    self.idealpoint[j] = ind.fitness.values[j] * self.idealalpha[j]
            else:
                if ind.fitness.values[j] < self.idealpoint[j]:
                    self.idealpoint[j] = ind.fitness.values[j] * self.idealalpha[j]

    def initialize(self):
        self.EP = []
        self.idealpoint = []
        ind = self.toolbox.individual()
        for w in ind.fitness.weights:
            if w > 0:
                self.idealpoint.append(-1.0e+30)
            else:
                self.idealpoint.append(1.0e+30)

        self.initWeight(self.popsize)
        self.initNeighbour()
        self.mainpop = self.createPopulation(self.popsize)
        self.evaluatePopluation(self.mainpop)
        for j in range(self.popsize):
            self.updateReference(self.mainpop[j])

    def GeneticOPDE(self, i):
        CR = 1
        F = 0.5

        while True:
            k = self.neighbourTable[i][random.randint(0, self.neighboursize-1)]
            if k != i:
                break
        while True:
            l = self.neighbourTable[i][random.randint(0, self.neighboursize-1)]
            if l != k and l != i:
                break
        c1 = self.mainpop[k]
        c2 = self.mainpop[l]

        choice = random.random()
        if choice < self.cxpb:
            c1 = self.toolbox.clone(c1)
            c2 = self.toolbox.clone(c2)
            c1, c2 = self.toolbox.mate(c1, c2)
            del c1.fitness.values
        choice = random.random()
        if choice < self.mutpb:
            c1 = self.toolbox.clone(c1)
            c1, = self.toolbox.mutate(c1)
            del c1.fitness.values
        offSpring = c1

        return offSpring

    def improve(self, i, offSpring):
        # do nothing
        pass

    def tcheScalarObj(self, namda, var):
        max_fun = -1.0e+30
        for n in range(self.numObjectives):
            diff = abs(var.fitness.values[n] - self.idealpoint[n])
            if namda[n] == 0:
                feval = 0.00001 * diff
            else:
                feval = diff * namda[n]
            if feval > max_fun:
                max_fun = feval
        return max_fun

    def wsScalarObj(self, namda, var):
        sum = 0.0
        for n in range(self.numObjectives):
            sum += namda[n] * var.fitness.values[n]
        return sum

    def updateCretia(self, problemIndex, ind):
        ds = self.weights[problemIndex]
        return self.scalarObj(ds, ind)

    def updateNeighbours(self, i, offSpring):
        for j in range(self.neighboursize):
            weightindex = self.neighbourTable[i][j]
            sol = self.mainpop[weightindex]
            d = self.updateCretia(weightindex, offSpring)
            e = self.updateCretia(weightindex, sol)

            if self.scalarMethod == 'wsScalar':
                if offSpring.fitness.weights[0] > 0:
                    if d > e:
                        self.mainpop[weightindex] = self.toolbox.clone(offSpring)
                else:
                    if d < e:
                        self.mainpop[weightindex] = self.toolbox.clone(offSpring)
            elif self.scalarMethod == 'tcheScalar':
                if d < e:
                    self.mainpop[weightindex] = self.toolbox.clone(offSpring)

    def updateEP(self, offSpring):
        cond = [operator.gt if w > 0 else operator.lt
                for w in offSpring.fitness.weights]

        def dominated(a, b):
            return sum([c(a, b) for a, b, c in zip(a.fitness.values, b.fitness.values, cond)]) == self.numObjectives

        self.EP = [ind for ind in self.EP if not dominated(offSpring, ind)]

        for ind in self.EP:
            if dominated(ind, offSpring):
                return
        self.EP.append(offSpring)

    def evolveNewInd(self, i):
        offSpring = self.GeneticOPDE(i)
        self.improve(i, offSpring)
        self.evaluateIndividual(offSpring)
        self.updateNeighbours(i, offSpring)
        self.updateEP(offSpring)
        self.updateReference(offSpring)

    def run(self):
        self.logbook = tools.Logbook()
        self.logbook.header = ['gen', 'nevals'] + (self.stats.fields if self.stats else [])

        if self.scalarMethod == 'wsScalar':
            self.scalarObj = self.wsScalarObj
        elif self.scalarMethod == 'tcheScalar':
            self.scalarObj = self.tcheScalarObj
        else:
            raise ValueError('unknown scalar method')

        self.initialize()

        record = self.stats.compile(self.mainpop) if self.stats is not None else {}
        self.logbook.record(gen=0, nevals=self.popsize, **record)
        if self.verbose:
            print(self.logbook.stream)

        for i in range(self.generation):
            for j in range(self.popsize):
                self.evolveNewInd(j)

            record = self.stats.compile(self.mainpop) if self.stats is not None else {}
            self.logbook.record(gen=i+1, nevals=self.popsize, **record)
            if self.verbose:
                print(self.logbook.stream)

def execute(toolbox, numObjectives, idealalpha, popSize, neighbourSize, scalarMethod, cxpb, mutpb, generation, stats, verbose=False):
    moead = MOEAD()
    moead.toolbox = toolbox
    moead.numObjectives = numObjectives
    moead.idealalpha = idealalpha
    moead.popsize = popSize
    moead.neighboursize = neighbourSize
    moead.scalarMethod = scalarMethod
    moead.cxpb = cxpb
    moead.mutpb = mutpb
    moead.generation = generation
    moead.stats = stats
    moead.verbose = verbose
    moead.run()
    return moead.EP, moead.logbook
