from typing import Sequence
import re

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from experiments.population_growth.ivp import ivp
from experiments.population_growth.operators import fine_fdm, coarse_fdm, \
    coarse_ar, coarse_pidon


experiment = 'population_growth'

TEST_LOSS_PATTERN = r'rank (\d) (.*) test loss: (.*)'
EXECUTION_TIME_PATTERN = \
    r'rank (\d) (.*) execution time - mean: (.*)s; sd: (.*)'
RSS_DIFFERENCES_PATTERN = \
    r'Parareal iterations (\d) - rank (\d) - RSS differences'

t_lower, t_upper = ivp.t_interval
matching_time_points = \
    np.linspace(t_lower + (t_upper - t_lower) / 4., t_upper, 4)

marker_types = ['o', 'v', 's']
line_styles = ['-', '--', ':']


def plot_solution():
    sol = fine_fdm.solve(ivp)

    fig, ax = plt.subplots()

    ax.plot(sol.t_coordinates, sol.discrete_y()[..., 0])
    ax.set_xlabel('t')
    ax.set_ylabel('y')
    ax.set_ylim(bottom=0)

    fig.tight_layout()
    fig.savefig(f'{experiment}_solution.png')
    plt.close(fig)


def plot_execution_times(
        mean_execution_times: Sequence[float],
        sd_execution_times: Sequence[float],
        labels: Sequence[str],
        x_label: str,
        name: str):
    positions = np.arange(len(mean_execution_times))

    fig, ax = plt.subplots()
    ax.bar(positions, mean_execution_times, yerr=sd_execution_times)

    ax.set_xticks(positions, labels, rotation=60)
    ax.set_xlabel(x_label)
    ax.set_ylabel('execution time (s)')

    fig.tight_layout()
    fig.savefig(f'{experiment}_{name}.png')
    plt.close(fig)


def plot_coarse_solution_diffs(
        best_ar_model_ind: int,
        best_pidon_model_ind: int):
    coarse_ar.model.model.load_weights(f'weights/ar_{best_ar_model_ind}')
    coarse_pidon.model.load_weights(f'weights/pidon_{best_pidon_model_ind}')
    fine_fdm_sol = fine_fdm.solve(ivp)
    coarse_fdm_sol = coarse_fdm.solve(ivp)
    coarse_ar_sol = coarse_ar.solve(ivp)
    coarse_pidon_sol = coarse_pidon.solve(ivp)
    diff = fine_fdm_sol.diff(
        [coarse_fdm_sol, coarse_ar_sol, coarse_pidon_sol])
    labels = ['coarse FDM', 'coarse AR', 'coarse PIDON']

    fig, ax = plt.subplots()

    for i in range(len(labels)):
        color = cm.tab20(float(i) / len(labels))
        ax.plot(
            matching_time_points,
            diff.differences[i][..., 0],
            color=color,
            label=labels[i],
            marker=marker_types[i],
            linestyle=line_styles[i])

    ax.set_xlabel('t')
    ax.set_ylabel('error')
    ax.legend(loc='upper right')

    fig.tight_layout()
    fig.savefig(f'{experiment}_diff.png')
    plt.close(fig)


def plot_rss_solution_diffs(
        rss_diffs: Sequence[Sequence[float]],
        labels: Sequence[str],
        name: str):
    fig, ax = plt.subplots()

    for i in range(len(labels)):
        color = cm.tab20(float(i) / len(labels))
        ax.plot(
            matching_time_points,
            rss_diffs[i],
            color=color,
            label=labels[i],
            marker=marker_types[i],
            linestyle=line_styles[i])

    ax.set_xlabel('t')
    ax.set_ylabel('absolute error')
    ax.set_ylim(bottom=0)
    ax.legend(loc='upper left')

    fig.tight_layout()
    fig.savefig(f'{experiment}_{name}.png')
    plt.close(fig)


def plot_parareal_rss_solution_diff_evolution(
        all_aggregate_rss_diffs: Sequence[Sequence[float]],
        aggregation_type: str,
        labels: Sequence[str],
        name: str):
    numbers_of_iterations = range(len(all_aggregate_rss_diffs[0]))

    fig, ax = plt.subplots()

    for i in range(len(labels)):
        aggregate_rss_diffs = all_aggregate_rss_diffs[i]
        color = cm.tab20(float(i) / len(labels))
        ax.plot(
            numbers_of_iterations,
            aggregate_rss_diffs,
            color=color,
            label=labels[i].split(' ')[-1],
            marker=marker_types[i],
            linestyle=line_styles[i])

    ax.set_yscale('log')
    ax.set_xticks(numbers_of_iterations)
    ax.set_xlabel('number of Parareal iterations')
    ax.set_ylabel(f'{aggregation_type} absolute error')
    ax.legend(loc='lower left')

    fig.tight_layout()
    fig.savefig(f'{experiment}_{name}.png')
    plt.close(fig)


plot_solution()

best_ar_model_ind = None
best_pidon_model_ind = None

with open('training.out') as file:
    lowest_ar_test_loss = np.inf
    lowest_pidon_test_loss = np.inf
    for line in file:
        match = re.match(TEST_LOSS_PATTERN, line)
        if match:
            rank = int(match.group(1))
            model_type = match.group(2)

            if model_type == 'ar':
                test_loss = float(match.group(3))
                if test_loss < lowest_ar_test_loss:
                    lowest_ar_test_loss = test_loss
                    best_ar_model_ind = rank

            elif model_type == 'pidon':
                test_loss = sum([
                    float(loss) for loss in match.group(3)[1:-1].split(' ')
                ])
                if test_loss < lowest_pidon_test_loss:
                    lowest_pidon_test_loss = test_loss
                    best_pidon_model_ind = rank

print(f'best {experiment} ar model ind:', best_ar_model_ind)
print(f'best {experiment} pidon model ind:', best_pidon_model_ind)

plot_coarse_solution_diffs(best_ar_model_ind, best_pidon_model_ind)

aggregate_exec_times = [{} for _ in range(4)]

with open('inference.out') as file:
    for line in file:
        match = re.match(EXECUTION_TIME_PATTERN, line)
        if match:
            rank = int(match.group(1))
            label = match.group(2)
            label = label.replace('pidon', 'PIDON')
            label = label.replace('ar', 'AR')
            label = label.replace('fdm', 'FDM')
            label = label.replace('parareal', 'Parareal')
            mean_exec_time = float(match.group(3))
            sd_exec_time = float(match.group(4))
            aggregate_exec_times[rank][label] = \
                (mean_exec_time, sd_exec_time)

for rank, times_by_label in enumerate(aggregate_exec_times):
    labels = list(times_by_label.keys())
    mean, sd = zip(*times_by_label.values())
    plot_execution_times(
        mean,
        sd,
        labels,
        'operator',
        f'execution_times_{rank}'
    )

first_rank_mean, first_rank_sd = zip(*aggregate_exec_times[0].values())
best_ar_mean, best_ar_sd = zip(
    *aggregate_exec_times[best_ar_model_ind].values()
)
best_pidon_mean, best_pidon_sd = zip(
    *aggregate_exec_times[best_pidon_model_ind].values()
)
best_mean = list(first_rank_mean)
best_sd = list(first_rank_sd)
best_mean[2] = best_ar_mean[2]
best_sd[2] = best_ar_sd[2]
best_mean[3] = best_pidon_mean[3]
best_sd[3] = best_pidon_sd[3]
best_mean[5] = best_ar_mean[5]
best_sd[5] = best_ar_sd[5]
best_mean[6] = best_pidon_mean[6]
best_sd[6] = best_pidon_sd[6]

print(best_mean)
print(best_sd)
plot_execution_times(
    best_mean,
    best_sd,
    list(aggregate_exec_times[0].keys()),
    'operator',
    'execution_times_best'
)

rss_solution_diffs = [[[] for _ in range(4)] for _ in range(4)]

with open('parareal_accuracy.out') as file:
    n_parareal_iterations = None
    rank = None

    for line in file:
        match = re.match(RSS_DIFFERENCES_PATTERN, line)
        if match:
            n_parareal_iterations = int(match.group(1))
            rank = int(match.group(2))

        if n_parareal_iterations is not None and rank is not None:
            diffs_string = line[line.rindex('[') + 1:line.index(']')]
            diffs = [float(s) for s in diffs_string.split(',')]
            rss_solution_diffs[n_parareal_iterations - 1][rank].append(
                diffs
            )

all_max_rss_diffs = np.empty((4, 3, 4), dtype=object)
all_mean_rss_diffs = np.empty((4, 3, 4), dtype=object)
for n_iterations_minus_one, rss_solution_diffs_for_iterations \
        in enumerate(rss_solution_diffs[:-1]):
    for rank, rss_solution_diffs_for_rank_and_iterations \
            in enumerate(rss_solution_diffs_for_iterations):
        max_rss_diff = np.max(
            rss_solution_diffs_for_rank_and_iterations, axis=1
        )
        mean_rss_diff = np.mean(
            rss_solution_diffs_for_rank_and_iterations, axis=1
        )
        all_max_rss_diffs[rank, :, 0] = max_rss_diff[:3]
        all_mean_rss_diffs[rank, :, 0] = mean_rss_diff[:3]
        all_max_rss_diffs[rank, :, n_iterations_minus_one + 1] = \
            max_rss_diff[3:]
        all_mean_rss_diffs[rank, :, n_iterations_minus_one + 1] = \
            mean_rss_diff[3:]

for rank in range(4):
    plot_rss_solution_diffs(
        rss_solution_diffs[0][rank][:3],
        list(aggregate_exec_times[rank].keys())[1:4],
        f'serial_rss_diffs_{rank}'
    )

    plot_parareal_rss_solution_diff_evolution(
        all_max_rss_diffs[rank],
        'max',
        list(aggregate_exec_times[rank].keys())[4:],
        f'parareal_max_rss_diff_{rank}'
    )

    plot_parareal_rss_solution_diff_evolution(
        all_mean_rss_diffs[rank],
        'mean',
        list(aggregate_exec_times[rank].keys())[4:],
        f'parareal_mean_rss_diff_{rank}'
    )

best_rss_solution_diffs = rss_solution_diffs[0][0][:3]
best_rss_solution_diffs[1] = rss_solution_diffs[0][best_ar_model_ind][1]
best_rss_solution_diffs[2] = rss_solution_diffs[0][best_pidon_model_ind][2]
plot_rss_solution_diffs(
    best_rss_solution_diffs,
    list(aggregate_exec_times[rank].keys())[1:4],
    'serial_rss_diffs_best'
)

best_max_rss_diffs = all_max_rss_diffs[0]
best_max_rss_diffs[1] = all_max_rss_diffs[best_ar_model_ind][1]
best_max_rss_diffs[2] = all_max_rss_diffs[best_pidon_model_ind][2]
plot_parareal_rss_solution_diff_evolution(
    best_max_rss_diffs,
    'max',
    list(aggregate_exec_times[rank].keys())[4:],
    'parareal_max_rss_diff_best'
)

best_mean_rss_diffs = all_mean_rss_diffs[0]
best_mean_rss_diffs[1] = all_mean_rss_diffs[best_ar_model_ind][1]
best_mean_rss_diffs[2] = all_mean_rss_diffs[best_pidon_model_ind][2]
plot_parareal_rss_solution_diff_evolution(
    best_mean_rss_diffs,
    'mean',
    list(aggregate_exec_times[rank].keys())[4:],
    'parareal_mean_rss_diff_best'
)
