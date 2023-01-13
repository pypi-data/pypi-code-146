# https://sop.tik.ee.ethz.ch/download/supplementary/testProblemSuite/
# にあるテストデータを解析して返すパーサ

import os
import operator

def parse(filename):
    knapsacks = []
    knapsack = None
    item = None
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith('knapsack problem'):
                pass
            elif line.startswith('knapsack'):
                knapsack = {}
                knapsack['items'] = []
                knapsacks.append(knapsack)
            elif line.startswith('capacity'):
                knapsack['capacity'] = float(line.split(':')[1])
            elif line.startswith('item'):
                item = {}
                knapsack['items'].append(item)
            elif line.startswith('weight'):
                item['weight'] = int(line.split(':')[1])
            elif line.startswith('profit'):
                item['profit'] = int(line.split(':')[1])
    return knapsacks

def parse_pareto(filename):
    with open(filename) as f:
        return [list(map(int, line.split(' '))) for line in f]

def _fullpath(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def extract(knapsacks):
    w = [[i['weight'] for i in k['items']] for k in knapsacks]
    p = [[i['profit'] for i in k['items']] for k in knapsacks]
    c = [k['capacity'] for k in knapsacks]
    return w, p, c

def _knapsack_common(basename):
    knapsacks = parse(_fullpath(basename + '.txt'))
    weights, profits, capacities = extract(knapsacks)
    pareto = parse_pareto(_fullpath(basename + '.pareto.txt'))
    return weights, profits, capacities, pareto

def knapsack_100_2():
    return _knapsack_common('knapsack.100.2')

def knapsack_250_2():
    return _knapsack_common('knapsack.250.2')

def knapsack_500_2():
    return _knapsack_common('knapsack.500.2')

def evaluate(individual, weights, profits, capacities):
    f = [0] * len(capacities)
    for i in range(len(capacities)):
        if sum(map(operator.mul, weights[i], individual)) <= capacities[i]:
            f[i] = sum(map(operator.mul, profits[i], individual))
    return f

if __name__ == '__main__':
    knapsacks = parse('knapsack.100.2.txt')
    assert len(knapsacks) == 2
    knapsack = knapsacks[0]
    assert knapsack['capacity'] == 2732
    assert len(knapsack['items']) == 100
    items = knapsack['items']
    assert items[0]['weight'] == 94
    assert items[0]['profit'] == 57
    print('assertion ok')
