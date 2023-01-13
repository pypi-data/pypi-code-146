"""
===============================
Metrics calculation
===============================
Includes a few metric as well as functions composing metrics on results files.

"""



import numpy as np
import torch
from sklearn.metrics import roc_auc_score, accuracy_score, balanced_accuracy_score, average_precision_score, mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import rankdata
import pandas as pd

def root_mean_squared_error_metric(target, pred):
    target = torch.tensor(target) if not torch.is_tensor(target) else target
    pred = torch.tensor(pred) if not torch.is_tensor(pred) else pred
    return torch.sqrt(torch.nn.functional.mse_loss(target, pred))

def mean_squared_error_metric(target, pred):
    target = torch.tensor(target) if not torch.is_tensor(target) else target
    pred = torch.tensor(pred) if not torch.is_tensor(pred) else pred
    return torch.nn.functional.mse_loss(target, pred)

def mean_absolute_error_metric(target, pred):
    target = torch.tensor(target) if not torch.is_tensor(target) else target
    pred = torch.tensor(pred) if not torch.is_tensor(pred) else pred
    return torch.tensor(mean_absolute_error(target, pred))

"""
===============================
Metrics calculation
===============================
"""
def auc_metric(target, pred, multi_class='ovo', numpy=False):
    lib = np if numpy else torch
    try:
        if not numpy:
            target = torch.tensor(target) if not torch.is_tensor(target) else target
            pred = torch.tensor(pred) if not torch.is_tensor(pred) else pred
        if len(lib.unique(target)) > 2:
            if not numpy:
                return torch.tensor(roc_auc_score(target, pred, multi_class=multi_class))
            return roc_auc_score(target, pred, multi_class=multi_class)
        else:
            if len(pred.shape) == 2:
                pred = pred[:, 1]
            if not numpy:
                return torch.tensor(roc_auc_score(target, pred))
            return roc_auc_score(target, pred)
    except ValueError as e:
        print(e)
        return np.nan if numpy else torch.tensor(np.nan)

def accuracy_metric(target, pred):
    target = torch.tensor(target) if not torch.is_tensor(target) else target
    pred = torch.tensor(pred) if not torch.is_tensor(pred) else pred
    if len(torch.unique(target)) > 2:
        return torch.tensor(accuracy_score(target, torch.argmax(pred, -1)))
    else:
        return torch.tensor(accuracy_score(target, pred[:, 1] > 0.5))

def brier_score_metric(target, pred):
    target = torch.tensor(target) if not torch.is_tensor(target) else target
    target = torch.nn.functional.one_hot(target, num_classes=len(torch.unique(target)))
    pred = torch.tensor(pred) if not torch.is_tensor(pred) else pred
    diffs = (pred - target)**2
    return torch.mean(torch.sum(diffs, axis=1))

def ece_metric(target, pred):
  import torchmetrics
  target = torch.tensor(target) if not torch.is_tensor(target) else target
  pred = torch.tensor(pred) if not torch.is_tensor(pred) else pred
  return torchmetrics.functional.calibration_error(pred, target)


def average_precision_metric(target, pred):
    target = torch.tensor(target) if not torch.is_tensor(target) else target
    pred = torch.tensor(pred) if not torch.is_tensor(pred) else pred
    if len(torch.unique(target)) > 2:
        return torch.tensor(average_precision_score(target, torch.argmax(pred, -1)))
    else:
        return torch.tensor(average_precision_score(target, pred[:, 1] > 0.5))

def balanced_accuracy_metric(target, pred):
    target = torch.tensor(target) if not torch.is_tensor(target) else target
    pred = torch.tensor(pred) if not torch.is_tensor(pred) else pred
    if len(torch.unique(target)) > 2:
        return torch.tensor(balanced_accuracy_score(target, torch.argmax(pred, -1)))
    else:
        return torch.tensor(balanced_accuracy_score(target, pred[:, 1] > 0.5))

def cross_entropy(target, pred):
    target = torch.tensor(target) if not torch.is_tensor(target) else target
    pred = torch.tensor(pred) if not torch.is_tensor(pred) else pred
    if len(torch.unique(target)) > 2:
        ce = torch.nn.CrossEntropyLoss()
        return ce(pred.float(), target.long())
    else:
        bce = torch.nn.BCELoss()
        return bce(pred[:, 1].float(), target.float())

def r2_metric(target, pred):
    target = torch.tensor(target) if not torch.is_tensor(target) else target
    pred = torch.tensor(pred) if not torch.is_tensor(pred) else pred
    return torch.tensor(neg_r2(target, pred))

def neg_r2(target, pred):
    return -r2_score(pred.float(), target.float())

def is_classification(metric_used):
    if metric_used == auc_metric or metric_used == cross_entropy:
        return True
    return False

def time_metric():
    """
    Dummy function, will just be used as a handler.
    """
    pass

def count_metric(x, y):
    """
    Dummy function, returns one count per dataset.
    """
    return 1

"""
===============================
Metrics composition
===============================
"""
def calculate_score_per_method(metric, name:str, global_results:dict, ds:list, eval_positions:list, aggregator:str='mean'):
    """
    Calculates the metric given by 'metric' and saves it under 'name' in the 'global_results'

    :param metric: Metric function
    :param name: Name of metric in 'global_results'
    :param global_results: Dicrtonary containing the results for current method for a collection of datasets
    :param ds: Dataset to calculate metrics on, a list of dataset properties
    :param eval_positions: List of positions to calculate metrics on
    :param aggregator: Specifies way to aggregate results across evaluation positions
    :return:
    """
    aggregator_f = np.nanmean if aggregator == 'mean' else np.nansum
    for pos in eval_positions:
        valid_positions = 0
        for d in ds:
            if f'{d[0]}_outputs_at_{pos}' in global_results:
                preds = global_results[f'{d[0]}_outputs_at_{pos}']
                y = global_results[f'{d[0]}_ys_at_{pos}']

                preds, y = preds.detach().cpu().numpy() if torch.is_tensor(
                    preds) else preds, y.detach().cpu().numpy() if torch.is_tensor(y) else y

                try:
                    if metric == time_metric:
                        global_results[f'{d[0]}_{name}_at_{pos}'] = global_results[f'{d[0]}_time_at_{pos}']
                        valid_positions = valid_positions + 1
                    else:
                        global_results[f'{d[0]}_{name}_at_{pos}'] = aggregator_f(
                            [metric(y[split], preds[split]) for split in range(y.shape[0])])
                        valid_positions = valid_positions + 1
                except Exception as err:
                    print(f'Error calculating metric with {err}, {type(err)} at {d[0]} {pos} {name}')
                    global_results[f'{d[0]}_{name}_at_{pos}'] = np.nan
            else:
                global_results[f'{d[0]}_{name}_at_{pos}'] = np.nan

        if valid_positions > 0:
            global_results[f'{aggregator}_{name}_at_{pos}'] = aggregator_f([global_results[f'{d[0]}_{name}_at_{pos}'] for d in ds])
        else:
            global_results[f'{aggregator}_{name}_at_{pos}'] = np.nan

    for d in ds:
        metrics = [global_results[f'{d[0]}_{name}_at_{pos}'] for pos in eval_positions]
        metrics = [m for m in metrics if not np.isnan(m)]
        global_results[f'{d[0]}_{aggregator}_{name}'] = aggregator_f(metrics) if len(metrics) > 0 else np.nan

    metrics = [global_results[f'{aggregator}_{name}_at_{pos}'] for pos in eval_positions]
    metrics = [m for m in metrics if not np.isnan(m)]
    global_results[f'{aggregator}_{name}'] = aggregator_f(metrics) if len(metrics) > 0 else np.nan


def calculate_score(metric, name, global_results, ds, eval_positions, aggregator='mean', limit_to=''):
    """
    Calls calculate_metrics_by_method with a range of methods. See arguments of that method.
    :param limit_to: This method will not get metric calculations.
    """
    for m in global_results:
        if limit_to not in m:
            continue
        calculate_score_per_method(metric, name, global_results[m], ds, eval_positions, aggregator=aggregator)


def make_metric_matrix(global_results, methods, pos, name, ds):
    # print(f"ds {len(ds[0])}") # ds is a list of length 30 (30 lists where each one has 6 elements)
    # print(f"ds[0] {ds[0][0]}")
    # print(f"global_results {len(global_results)}")
    # print(f"list(global_results.keys()) {list(global_results.keys())}")
    result = []
    # print(f"pos {str(pos)}")
    for m in global_results:
        #print(f"m {m}")
        #print(f"[global_results[m] {global_results[m]}")
        # print(f"m {m} + {ds[0][0]}_{name}_at_{str(pos)}")
        try:
            result += [[global_results[m][d[0] + '_' + name + '_at_' + str(pos)] for d in ds]]
            # print(f"from global_results {[global_results[m][d[0] + '_' + name + '_at_' + str(pos)] for d in ds]}")
            # print(f"m {m} + {ds[0][0]}_{name}_at_{str(pos)}")
        except Exception as e:
            #raise(e)
            result += [[np.nan]]
    result = np.array(result)
    # print(f"result {result}")
    # print(f"result len {len(result)}")
    # print(f"result[0] len {len(result[0])}")
    # print(f"result.T len {len(result.T)}")
    # print(f"ds[0] len {len(ds)}")
    result = pd.DataFrame(result.T, index=[d[0] for d in ds], columns=[k for k in list(global_results.keys())])
    print(f"result.shape {result.shape}")
    # print(f"result {result}")

    # print(f"list(global_results.keys()) {list(global_results.keys())}") # ['transformer_time_0.5roc_auc_split_1', 'logistic_time_0.5roc_auc_split_1']
    # print(f"result.shape in make_metric_matrix() {result.shape} ") # result.shape in make_metric_matrix() (30, 10)
    # print(f"result in make_metric_matrix() {result} ")
    matrix_means, matrix_stds, matrix_per_split = [], [], []

    for method in methods:
        matrix_means += [result.iloc[:, [c.startswith(method+'_time') for c in result.columns]].mean(axis=1)]
        matrix_stds += [result.iloc[:, [c.startswith(method+'_time') for c in result.columns]].std(axis=1)]
        matrix_per_split += [result.iloc[:, [c.startswith(method+'_time') for c in result.columns]]]
    
    # print(f"matrix_means {len(matrix_means)}") 
    # print(f"matrix_means {matrix_means}")
    matrix_means = pd.DataFrame(matrix_means, index=methods).T
    matrix_stds = pd.DataFrame(matrix_stds, index=methods).T

    # print(f"matrix_means (2) {matrix_means.shape}") # matrix_means (2) (30, 2)
    # print(f"matrix_stds (2) {matrix_stds.shape}") # matrix_stds (2) (30, 2)
    return matrix_means, matrix_stds, matrix_per_split


def make_ranks_and_wins_table(matrix):
    for dss in matrix.T:
        matrix.loc[dss] = rankdata(-matrix.round(3).loc[dss])
    ranks_acc = matrix.mean()
    wins_acc = (matrix == 1).sum()

    return ranks_acc, wins_acc
