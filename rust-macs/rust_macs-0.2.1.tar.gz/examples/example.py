import rust_macs
import numpy as np

M = np.inf
graph = np.array([[0, 1, 3, np.inf],
                   [1, 0, 1, 3],
                   [3, 1, 0, 1],
                   [np.inf, 3, 1, 0]])
source = 0
dest = 3
t_max = 20
cl_len = 5

n_ants = 5
n_types = 2
init_pheromones = 0.05
beta = 2
rho = 0.1

q0 = 0
gamma = 0

sum = 0
sum1 = 0
sum2 = 0
sum_nonopti = 0
for i in range(100):
    print(f"Iteration {i}")
    result = rust_macs.optimize_macs(graph, n_ants, n_types, init_pheromones, beta, q0, gamma, rho, source, dest, t_max, cl_len)
    result = [i[0] for i in result]
    if [0, 1, 3] in result and [0, 2, 3] in result:
        sum += 1
    elif [0, 1, 3] in result:
        sum1 += 1
    elif [0, 2, 3] in result:
        sum2 += 1
    else:
        sum_nonopti += 1
        print(result)
print(sum, sum1, sum2, sum_nonopti)
