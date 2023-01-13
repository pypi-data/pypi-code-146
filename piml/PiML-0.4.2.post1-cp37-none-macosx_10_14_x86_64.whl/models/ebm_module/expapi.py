from logging.config import valid_ident
import os
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import gridspec
from sklearn.base import is_classifier

from piml.workflow.plots import PlotHeatmap, PlotHBar, PlotEffect
from piml.utils.result import TestDataResult


def get_1D_function(inputs, fidx, splits, values, right_inclusive=False):
    idx1 = np.digitize(inputs[:, fidx[0]], bins=splits[1:-1], right=right_inclusive)
    output = values[idx1]
    return output


def predict_1D_func(fidx, splits, values, right_inclusive=False):
    def wrapper(inputs):
        return get_1D_function(inputs, fidx, splits, values, right_inclusive=right_inclusive)

    return wrapper


def get_2D_function(inputs, fidx, splits_v1, splits_v2, values, right_inclusive=False):
    idx1 = np.digitize(inputs[:, fidx[0]], bins=splits_v1[1:-1], right=right_inclusive)
    idx2 = np.digitize(inputs[:, fidx[1]], bins=splits_v2[1:-1], right=right_inclusive)
    output = values[idx1, idx2]
    return output


def predict_2D_func(fidx, splits_v1, splits_v2, values, right_inclusive=False):
    def wrapper(inputs):
        return get_2D_function(inputs, fidx, splits_v1, splits_v2, values, right_inclusive=right_inclusive)

    return wrapper


class EBMExplainer():

    def __init__(self, estimator):

        self.estimator = estimator

    def fit(self, x):
        """
        Extract the fitted effects and calcualte the importance based on Shapley value.
        """
        self.main_effect_ = {}
        self.interaction_ = {}
        self.intercept_ = self.estimator.intercept_
        self.n_features_in_ = len(self.estimator.preprocessor_.col_names_)

        self.min_value_ = np.zeros((self.n_features_in_))
        self.max_value_ = np.zeros((self.n_features_in_))
        for i in range(self.n_features_in_):
            fidx = self.estimator.feature_groups_[i]
            if self.estimator.feature_types[fidx[0]] == "categorical":
                self.min_value_[i] = min(list(map(float, self.estimator.preprocessor_.col_mapping_[i].keys())))
                self.max_value_[i] = max(list(map(float, self.estimator.preprocessor_.col_mapping_[i].keys())))
            else:
                self.min_value_[i] = self.estimator.preprocessor_.col_min_[i]
                self.max_value_[i] = self.estimator.preprocessor_.col_max_[i]

        self.feature_names_ = self.estimator.feature_names[:self.n_features_in_]
        self.effect_importances_ = self.estimator.feature_importances_ / np.sum(self.estimator.feature_importances_)
        for i in range(len(self.estimator.feature_names)):
            key = self.estimator.feature_names[i]
            fidx = self.estimator.feature_groups_[i]
            key_type = self.estimator.feature_types[i]
            if key_type == "interaction":

                values = self.estimator.additive_terms_[i][1:][:, 1:]
                importance = self.effect_importances_[i]
                if self.estimator.feature_types[fidx[0]] == "categorical":
                    categories = np.array(
                        [float(k) for k in self.estimator.pair_preprocessor_.col_mapping_[fidx[0]].keys()])
                    sorted_idx = np.argsort(categories)
                    categories = np.sort(categories)
                    splits_v1 = np.hstack([-np.inf, (categories[1:] + categories[:-1]) / 2, np.inf])
                    values = values[sorted_idx]
                else:
                    splits_v1 = np.hstack([-np.inf, self.estimator.pair_preprocessor_.col_bin_edges_[fidx[0]], np.inf])

                if self.estimator.feature_types[fidx[1]] == "categorical":
                    categories = np.array(
                        [float(k) for k in self.estimator.pair_preprocessor_.col_mapping_[fidx[1]].keys()])
                    sorted_idx = np.argsort(categories)
                    categories = np.sort(categories)
                    splits_v2 = np.hstack([-np.inf, (categories[1:] + categories[:-1]) / 2, np.inf])
                    values = values[:, sorted_idx]
                else:
                    splits_v2 = np.hstack([-np.inf, self.estimator.pair_preprocessor_.col_bin_edges_[fidx[1]], np.inf])

                predict_func = predict_2D_func(fidx, splits_v1, splits_v2, values, False)
                self.interaction_[key] = {"fidx": fidx,
                                          "type": "pairwise",
                                          "splits_v1": splits_v1,
                                          "splits_v2": splits_v2,
                                          "importance": importance,
                                          "predict_func": predict_func}
            elif key_type == "numerical":
                splits = np.hstack([-np.inf, self.estimator.preprocessor_.col_bin_edges_[fidx[0]], np.inf])
                values = self.estimator.additive_terms_[i][1:]
                importance = self.effect_importances_[i]
                density = {"names": self.estimator.preprocessor_._get_hist_edges(fidx[0]),
                           "scores": self.estimator.preprocessor_._get_hist_counts(fidx[0])}
                predict_func = predict_1D_func(fidx, splits, values, False)
                self.main_effect_[key] = {"fidx": fidx,
                                          "type": "numerical",
                                          "splits": splits,
                                          "values": values,
                                          "importance": importance,
                                          "density": density,
                                          "predict_func": predict_func}
            elif key_type == "categorical":
                categories = np.array(
                    [float(k) for k in self.estimator.pair_preprocessor_.col_mapping_[fidx[0]].keys()])
                sorted_idx = np.argsort(categories)
                categories = np.sort(categories)
                splits = np.unique(np.hstack([-np.inf, (categories[1:] + categories[:-1]) / 2, np.inf]))
                values = self.estimator.additive_terms_[i][1:][sorted_idx]
                importance = self.effect_importances_[i]
                density = {"names": np.array(self.estimator.preprocessor_._get_hist_edges(fidx[0]))[sorted_idx],
                           "scores": np.array(self.estimator.preprocessor_._get_hist_counts(fidx[0]))[sorted_idx]}
                predict_func = predict_1D_func(fidx, splits, values, False)
                self.main_effect_[key] = {"fidx": fidx,
                                          "type": "categorical",
                                          "splits": splits,
                                          "values": values,
                                          "importance": importance,
                                          "density": density,
                                          "predict_func": predict_func}

        mout = self.get_main_effect_raw_output(x)
        iout = self.get_interaction_raw_output(x)
        interaction_list = self.estimator.feature_groups_[self.n_features_in_:]
        if len(interaction_list) > 0:
            shapley_value = np.vstack([mout[:, fidx] +
                                       0.5 * iout[:, np.where(np.vstack(interaction_list) == fidx)[0]].sum(1)
                                       for fidx in range(self.n_features_in_)]).T
        else:
            shapley_value = mout
        feature_importance_raw = shapley_value.var(0)
        if np.sum(feature_importance_raw) == 0:
            self.feature_importance_ = np.zeros((self.n_features_in_))
        else:
            self.feature_importance_ = feature_importance_raw / feature_importance_raw.sum()

    def get_main_effect_raw_output(self, x):
        """
        Returns numpy array of main effects' raw prediction.

        Parameters
        ----------
        x : np.ndarray of shape (n_samples, n_features)
            Data features.

        Returns
        -------
        pred : np.ndarray of shape (n_samples, n_features)
            numpy array of main effects' raw prediction.
        """
        if len(self.main_effect_) > 0:
            pred = np.vstack([item["predict_func"](x) for key, item in self.main_effect_.items()]).T
        else:
            pred = np.empty(shape=(x.shape[0], 0))
        return pred

    def get_interaction_raw_output(self, x):
        """
        Returns numpy array of interactions' raw prediction.

        Parameters
        ----------
        x : np.ndarray of shape (n_samples, n_features)
            Data features.

        Returns
        -------
        pred : np.ndarray of shape (n_samples, n_interactions)
            numpy array of interactions' raw prediction.
        """
        if len(self.interaction_) > 0:
            pred = np.vstack([item["predict_func"](x) for key, item in self.interaction_.items()]).T
        else:
            pred = np.empty(shape=(x.shape[0], 0))
        return pred

    def local_effect_explain(self, x, y=None):
        """
        Extract the main effects and interactions values of a given sample.

        Parameters
        ----------
        x : np.ndarray of shape (n_samples, n_features)
            Data features.
        y : np.ndarray of shape (n_samples, )
            Target response.
        """
        if is_classifier(self.estimator):
            predicted = self.estimator.predict_proba(x)[:, 1]
        else:
            predicted = self.estimator.predict(x)

        intercept = self.intercept_
        main_effect_output = self.get_main_effect_raw_output(x)
        interaction_output = self.get_interaction_raw_output(x)
        scores = np.hstack([np.repeat(intercept, x.shape[0]).reshape(-1, 1),
                            np.hstack([main_effect_output, interaction_output])])
        effect_names = np.array(["Intercept"] + list(self.main_effect_.keys())
                                + list(self.interaction_.keys()))
        active_indices = np.arange(1 + main_effect_output.shape[1] + interaction_output.shape[1])
        if y is not None:
            data_dict_local = [{"active_indices": active_indices,
                                "scores": scores[i],
                                "effect_names": effect_names,
                                "predicted": predicted[i],
                                "actual": y[i] if y is not None else None} for i in range(x.shape[0])]
        else:
            data_dict_local = [{"active_indices": active_indices,
                                "scores": scores[i],
                                "effect_names": effect_names,
                                "predicted": predicted[i]} for i in range(x.shape[0])]
        return data_dict_local

    def local_feature_explain(self, x, y=None):
        """
        Extract the main effects and interactions values of a given sample.

        Parameters
        ----------
        x : np.ndarray of shape (n_samples, n_features)
            Data features.
        y : np.ndarray of shape (n_samples, )
            Target response.
        """
        if is_classifier(self.estimator):
            predicted = self.estimator.predict_proba(x)[:, 1]
        else:
            predicted = self.estimator.predict(x)

        mout = self.get_main_effect_raw_output(x)
        iout = self.get_interaction_raw_output(x)
        interaction_list = self.estimator.feature_groups_[self.n_features_in_:]
        if len(interaction_list) > 0:
            shapley_value = np.vstack([mout[:, fidx] +
                                       0.5 * iout[:, np.where(np.vstack(interaction_list) == fidx)[0]].sum(1)
                                       for fidx in range(self.n_features_in_)]).T
        else:
            shapley_value = mout

        scores = shapley_value
        effect_names = np.array(list(self.main_effect_.keys()))
        if y is not None:
            data_dict_local = [{"active_indices": np.where(np.abs(scores[i]) > 0)[0],
                                "scores": scores[i],
                                "effect_names": effect_names,
                                "predicted": predicted[i],
                                "actual": y[i] if y is not None else None} for i in range(x.shape[0])]
        else:
            data_dict_local = [{"active_indices": np.where(np.abs(scores[i]) > 0)[0],
                                "scores": scores[i],
                                "effect_names": effect_names,
                                "predicted": predicted[i]} for i in range(x.shape[0])]
        return data_dict_local

    def global_explain(self, main_grid_size=100, interact_grid_size=20):
        """
        Extract the fitted main effects and interactions.

        Parameters
        ----------
        main_grid_size : int
            The grid size of main effects, by default 100.
        interact_grid_size : int
            The grid size of interactions, by default 20.
        """
        if hasattr(self, "data_dict_global_"):
            return self.data_dict_global_

        data_dict_global = {}
        for key, item in self.main_effect_.items():
            fidx = item["fidx"]
            if item["type"] == "numerical":
                predict_func = item["predict_func"]
                inputs = np.linspace(self.min_value_[fidx[0]], self.max_value_[fidx[0]], main_grid_size)
                xgrid_input = np.zeros((inputs.shape[0], self.n_features_in_))
                xgrid_input[:, fidx[0]] = inputs
                outputs = predict_func(xgrid_input)
            else:
                inputs = np.array([float(k) for k in self.estimator.preprocessor_.col_mapping_[fidx[0]].keys()])
                outputs = item["values"]
            data_dict_global[key] = {"type": item["type"],
                                     "fidx": item["fidx"],
                                     "inputs": inputs,
                                     "outputs": outputs,
                                     "importance": item["importance"],
                                     "density": item["density"]}
        for key, item in self.interaction_.items():
            fidx = item["fidx"]
            predict_func = item["predict_func"]
            key_type1 = self.estimator.feature_types[fidx[0]]
            key_type2 = self.estimator.feature_types[fidx[1]]
            if key_type1 == "numerical":
                x1grid = np.linspace(self.min_value_[fidx[0]], self.max_value_[fidx[0]], interact_grid_size)
            else:
                x1grid = np.array([float(k) for k in self.estimator.preprocessor_.col_mapping_[fidx[0]].keys()])
            if key_type2 == "numerical":
                x2grid = np.linspace(self.min_value_[fidx[1]], self.max_value_[fidx[1]], interact_grid_size)
            else:
                x2grid = np.array([float(k) for k in self.estimator.preprocessor_.col_mapping_[fidx[1]].keys()])
            x1, x2 = np.meshgrid(x1grid, x2grid[::-1])
            inputs = np.hstack([np.reshape(x1, [-1, 1]), np.reshape(x2, [-1, 1])])
            xgrid_input = np.zeros((x1.shape[0] * x1.shape[1], self.n_features_in_))
            xgrid_input[:, fidx] = inputs
            outputs = predict_func(xgrid_input).reshape(x1.shape)
            data_dict_global[key] = {"type": item["type"],
                                     "fidx": item["fidx"],
                                     "inputs": inputs,
                                     "outputs": outputs,
                                     "importance": item["importance"]}

        self.data_dict_global_ = data_dict_global
        return data_dict_global

    def global_interpret(self, x=None, feature_names=None, truncate_dict=None):
        act_fea_lis = list(self.main_effect_.keys())[:len(self.main_effect_)]
        act_inter_lis = list(self.interaction_.keys())[:len(self.interaction_)]
        act_fea_ei = [self.main_effect_[i]['importance'] for i in act_fea_lis]
        act_inter_ei = [self.interaction_[i]['importance'] for i in act_inter_lis]

        act_inter_lis_new = []
        for i in act_inter_lis:
            tmp_0 = truncate_dict[self.feature_names_[self.interaction_[i]['fidx'][0]]]
            tmp_1 = truncate_dict[self.feature_names_[self.interaction_[i]['fidx'][1]]]
            act_inter_lis_new.append(tmp_0 + ' x ' + tmp_1)

        self.truncate_dict = truncate_dict
        self.act_fea_lis = np.array(act_fea_lis)[np.argsort(act_fea_ei)[::-1]].tolist()
        self.act_inter_lis = np.array(act_inter_lis_new)[np.argsort(act_inter_ei)[::-1]].tolist()
        self.inter_effect_trunc_dict = {act_inter_lis[i]: act_inter_lis_new[i] for i in
                                                range(len(act_inter_lis))}

    def interpret_ei(self):
        f_lis = list(self.main_effect_.keys()) + list(self.interaction_.keys())
        vi = self.effect_importances_.tolist()

        vi = pd.DataFrame(np.array([f_lis, vi]).T, columns=['feature', 'importance'])
        vi.importance = vi.importance.astype(float)
        vi = vi.sort_values('importance', ascending=True)
        vi = vi[vi.importance > 0]
        effect = vi.loc[:, 'feature'].values.ravel().tolist()
        effect = [self.inter_effect_trunc_dict[effect_i] if effect_i in self.inter_effect_trunc_dict.keys() else effect_i for effect_i in effect]
        effect = [self.truncate_dict[effect_i] if effect_i in self.truncate_dict.keys() else effect_i for
                  effect_i in effect]
        importance = vi.loc[:, 'importance'].values.astype(float).ravel().tolist()
        result = {'type': 'effect', 'value': (effect, importance), 'title': 'Effect Importance'}
        return TestDataResult(key='ei', value=result)

    def interpret_fi(self):
        f_lis = self.feature_names_
        vi = self.feature_importance_.tolist()
        vi = pd.DataFrame(np.array([f_lis, vi]).T, columns=['feature', 'importance'])
        vi.importance = vi.importance.astype(float)
        vi = vi.sort_values('importance', ascending=True)
        vi = vi[vi.importance > 0]
        feature = vi.loc[:, 'feature'].values.ravel().tolist()
        feature = [self.truncate_dict[feature_i] for feature_i in feature]
        importance = vi.loc[:, 'importance'].values.astype(float).ravel().tolist()
        result = {'feature_names': feature, 'importance': importance, 'title': 'Feature Importance'}
        return TestDataResult(key='fi', value=result)

    def get_main_effect(self, feature, scaler=None):
        item = deepcopy(self.main_effect_[feature])
        feature_type = self.estimator.feature_types[item["fidx"][0]]

        if feature_type == "categorical":
            categories = np.array(
                [float(k) for k in self.estimator.preprocessor_.col_mapping_[item["fidx"][0]].keys()])

            result = {'feature': feature, 'feature_type': feature_type,
                      'categories': categories, 'output': item}
        else:
            mesh_grid = 100
            xgrid_input = np.zeros((mesh_grid, self.n_features_in_))
            xgrid = np.linspace(self.min_value_[item["fidx"][0]], self.max_value_[item["fidx"][0]], mesh_grid)
            xgrid_input[:, item["fidx"][0]] = xgrid
            ygrid = item["predict_func"](xgrid_input)

            result ={'feature': feature, 'feature_type': feature_type,
                     'xgrid': xgrid, 'ygrid': ygrid, 'output': item}

        return TestDataResult(key='main_effect', model='ebm', input_={'feature': feature},
                              value=result, scaler=scaler)

    def get_interaction_effect(self, feature0, feature1=None, scaler=None):
        if feature1 is None:
            feature0, feature1 = feature0.split(' x ')[0], feature0.split(' x ')[1]
        feature_combine_01 = feature0 + ' x ' + feature1
        feature_combine_10 = feature1 + ' x ' + feature0
        if feature_combine_01 in self.act_inter_lis:
            feature_combine = feature_combine_01
        elif feature_combine_10 in self.act_inter_lis:
            feature_combine = feature_combine_10
        else:
            print('No this interaction effect')
            return TestDataResult(key='interaction_effect', model='ebm',
                                  value=None, scaler=scaler)
        inverse_dict = {v: i for i, v in self.inter_effect_trunc_dict.items()}
        feature_combine = inverse_dict[feature_combine]

        item = deepcopy(self.interaction_[feature_combine])
        mesh_grid = 100
        x0, x1 = np.meshgrid(
            np.linspace(self.min_value_[item["fidx"][0]], self.max_value_[item["fidx"][0]], mesh_grid),
            np.linspace(self.min_value_[item["fidx"][1]], self.max_value_[item["fidx"][1]], mesh_grid)[::-1])
        xgrid_input = np.zeros((mesh_grid * mesh_grid, self.n_features_in_))
        xgrid_input[:, [item["fidx"][0], item["fidx"][1]]] = np.hstack(
            [np.reshape(x0, [-1, 1]), np.reshape(x1, [-1, 1])])
        ygrid = item["predict_func"](xgrid_input).reshape(mesh_grid, mesh_grid)

        extent = [self.min_value_[item["fidx"][0]],
                self.max_value_[item["fidx"][0]],
                self.min_value_[item["fidx"][1]],
                self.max_value_[item["fidx"][1]]]
        result = {'extent': extent, 'ygrid': ygrid, 'importance': item["importance"]}

        return TestDataResult(key='interaction_effect', model='ebm', input_={'feature_combine': feature_combine},
                              value=result, scaler=scaler)

    def interpret_local_effect(self, x_, y_, columns, centered=True):
        local_explain_dict = self.local_effect_explain(x_, y_)
        if self.estimator.__class__.__name__ == "ExplainableBoostingClassifier":
            predicted = self.estimator.predict_proba(x_)[0][-1]
        elif self.estimator.__class__.__name__ == "ExplainableBoostingRegressor":
            predicted = self.estimator.predict(x_)[0]
        title = "Predicted: %0.4f | Actual: %0.4f" % (predicted, y_.ravel()[0])
        x = local_explain_dict[0]['effect_names']
        y = local_explain_dict[0]['scores']

        vi = pd.DataFrame(np.array([x, y]).T, columns=['feature', 'importance'])
        vi.importance = vi.importance.astype(float)
        order = np.argsort(abs(vi.importance).values)
        vi = vi.iloc[order]
        vi = vi[vi.importance != 0].reset_index(drop=True)
        try:
            target_row = vi[vi.feature == 'Intercept'].index[0]
            idx = [i for i in range(len(vi)) if i != target_row] + [target_row]
        except ValueError:
            idx = [i for i in range(len(vi))]
        vi = vi.iloc[idx].reset_index(drop=True)
        x = vi.loc[:, 'feature'].values.ravel().tolist()
        y = vi.loc[:, 'importance'].values.astype(float).ravel().tolist()

        val = []
        value = pd.DataFrame(x_, columns=columns)

        for i in x:
            if i == 'Intercept':
                val.append('')
            else:
                if i not in self.feature_names_:
                    tmp_0 = self.feature_names_[
                        self.interaction_[i]['fidx'][0]]
                    tmp_1 = self.feature_names_[
                        self.interaction_[i]['fidx'][1]]
                    _length = 2
                else:
                    _length = 1

                if _length == 1:
                    x_val = value.loc[:, i].values[0]
                    val.append([x_val])

                elif _length == 2:
                    x_val1 = value.loc[:, tmp_0].values[0]
                    x_val2 = value.loc[:, tmp_1].values[0]
                    val.append([x_val1, x_val2])

        result = {'x': x,
                  'y': y,
                  'value': val,
                  'title': title}

        return TestDataResult(key='local_ei', model='ebm', value=result)

    def interpret_local_fi(self, x_, y_, columns, centered=True):

        local_explain_dict = self.local_feature_explain(x_, y_)

        if self.estimator.__class__.__name__ == "ExplainableBoostingClassifier":
            predicted = self.estimator.predict_proba(x_)[0][-1]
        elif self.estimator.__class__.__name__ == "ExplainableBoostingRegressor":
            predicted = self.estimator.predict(x_)[0]

        title = "Predicted: %0.4f | Actual: %0.4f" % (predicted, y_.ravel()[0])
        feature = local_explain_dict[0]['effect_names']
        importance = local_explain_dict[0]['scores']

        vi = pd.DataFrame(np.array([feature, importance]).T, columns=['feature', 'importance'])
        vi.importance = vi.importance.astype(float)
        order = np.argsort(abs(vi.importance).values)
        vi = vi.iloc[order]
        vi = vi[vi.importance != 0].reset_index(drop=True)

        idx = [i for i in range(len(vi))]
        vi = vi.iloc[idx].reset_index(drop=True)
        feature = vi.loc[:, 'feature'].values.ravel().tolist()
        importance = vi.loc[:, 'importance'].values.astype(float).ravel().tolist()

        val = []
        value = pd.DataFrame(x_, columns=columns)

        for single_fea in feature:
            feature_val = value.loc[:, single_fea].values[0]
            val.append(feature_val)
            # if type(feature_val) != str:
            #     feature_val = np.round(feature_val, 4)
            # val.append(str(feature_val))

        result = {'x': feature,
                  'y': importance,
                  'value': val,
                  'title': title}

        return TestDataResult(key='local_fi', model='ebm', value=result)

    def plot_fi(self, interpret_result, max_show=10, return_fig=False, figsize=(8, 6)):

        interpret_result = interpret_result.get_result()
        hbar = PlotHBar()
        max_show = min(len(interpret_result['value']['feature_names']), max_show)
        fig = hbar.plot(X=interpret_result['value']['feature_names'][-max_show:],
                        height=interpret_result['value']['importance'][-max_show:],
                        title=interpret_result['value']['title'], figsize=figsize)
        if return_fig:
            return fig
    
    def plot_ei(self, interpret_result, max_show=10, figsize=(8, 6)):

        interpret_result = interpret_result.get_result()
        if (interpret_result['value'] is None) or (interpret_result['value']['type'] == 'coefficient'):
            print('Not supported')

        else:
            if interpret_result['value']['type'] == 'effect':
                hbar = PlotHBar()
                max_show = min(len(interpret_result['value']['value'][0]), max_show)
                hbar.plot(X=interpret_result['value']['value'][0][-max_show:],
                          height=interpret_result['value']['value'][1][-max_show:],
                          title='Effect Importance', figsize=figsize)
    
    def plot_main_effect(self, interpret_result, figsize=(8, 6)):
        interpret_result = interpret_result.get_result()
        scaler = interpret_result['scaler']
        if interpret_result['value'] is None:  # Tree, GLM
            print('Not supported')

        else:
            effplot = PlotEffect(feature=interpret_result['value']['feature'])
            if interpret_result['value']['feature_type'] == "categorical":
                effplot.plot(interpret_result['value']['feature_type'],
                            importance=interpret_result['value']['output']["importance"],
                            categories=interpret_result['value']['categories'],
                            height=interpret_result['value']['output']["values"],
                            density_names=interpret_result['value']['output']["density"]["names"],
                            scores=interpret_result['value']['output']["density"]["scores"],
                            figsize=figsize,
                            scaler=scaler)
            else:
                effplot.plot(interpret_result['value']['feature_type'],
                            importance=interpret_result['value']['output']["importance"],
                            density_names=interpret_result['value']['output']["density"]["names"],
                            scores=interpret_result['value']['output']["density"]["scores"],
                            xgrid=interpret_result['value']['xgrid'], ygrid=interpret_result['value']['ygrid'],
                            figsize=figsize,
                            scaler=scaler)
    
    def plot_interaction_effect(self, interpret_result, figsize=(8, 6)):
        interpret_result = interpret_result.get_result()
        scaler = interpret_result['scaler']
        if interpret_result['value'] is None:
            print('Not supported')

        else:
            try:
                if interpret_result['input']['feature_combine'] == 'None':
                    print('No interaction effect')
                    return
            except:
                pass

            if interpret_result['model'] == 'ebm':
                heat_plot = PlotHeatmap(mesh_grid=100, feature_combine=interpret_result['input']['feature_combine'])
                heat_plot.plot_interpret(mat_value=interpret_result['value']['ygrid'],
                                         extent=interpret_result['value']['extent'],
                                         importance=interpret_result['value']["importance"], figsize=figsize,
                                         scaler=scaler)

    def plot_fi_local(self, interpret_result, max_show=10, figsize=(8, 6)):

        interpret_result = interpret_result.get_result()
        if interpret_result['value'] is None:
            print('Not supported')
            return
        elif len(interpret_result['value'].keys()) != 4:
            hbar2 = PlotHBar()
            max_show = min(len(interpret_result['value']['value']), max_show)
            hbar2.plot_stem(X=interpret_result['value']['x'][-max_show:],
                            height=interpret_result['value']['y'][-max_show:],
                            value=interpret_result['value']['value'][-max_show:],
                            stem_value0=interpret_result['value']['stem0'][-max_show:],
                            stem_value1=interpret_result['value']['stem1'][-max_show:],
                            title=interpret_result['value']['title'],
                            mid_center=True, pos_color='#e74c3c', neg_color='#27ae60', figsize=figsize)
        else:
            hbar2 = PlotHBar()
            max_show = min(len(interpret_result['value']['value']), max_show)
            hbar2.plot(X=interpret_result['value']['x'][-max_show:], height=interpret_result['value']['y'][-max_show:],
                       value=interpret_result['value']['value'][-max_show:],
                       title=interpret_result['value']['title'], mid_center=True, pos_color='#e74c3c',
                       neg_color='#27ae60', figsize=figsize)


    def plot_ei_local(self, interpret_result, max_show=10, figsize=(8, 6)):

        interpret_result = interpret_result.get_result()
        if interpret_result['value'] is None:
            print('Not supported')
            return
        hbar1 = PlotHBar()
        max_show = min(len(interpret_result['value']['value']), max_show)
        hbar1.plot(X=interpret_result['value']['x'][-max_show:], height=interpret_result['value']['y'][-max_show:],
                   value=interpret_result['value']['value'][-max_show:],
                   title=interpret_result['value']['title'], mid_center=True, pos_color='#e74c3c', neg_color='#27ae60',
                   figsize=figsize)

    def show_local_effect_explain(self, x, y=None, xlabel_rotation=0, folder="./", name="demo", save_png=False,
                                  save_eps=False):
        """
        Show local explanation of given samples.

        Parameters
        ----------
        x : np.ndarray of shape (n_samples, n_features)
            Data features.
        y : np.ndarray of shape (n_samples, )
            Target response.
        xlabel_rotation : int
            Rotation angle of x-axis labels, by default 0.
        folder : str
            The path of folder to save figure, by default "./".
        name : str
            Name of the file, by default "local_explain".
        save_png : boolean
            Whether to save the plot in PNG format, by default False.
        save_eps : boolean
            Whether to save the plot in EPS format, by default False.
        """

        def local_visualize(data_dict_local):

            max_ids = data_dict_local["scores"].shape[0]
            idx = 1 + np.argsort(np.abs(data_dict_local["scores"][1:]))[::-1]
            idx = np.array([0] + idx.tolist())
            fig = plt.figure(figsize=(round((max_ids + 1) * 0.6), 4))
            plt.bar(np.arange(max_ids), data_dict_local["scores"][idx])
            plt.xticks(np.arange(max_ids), data_dict_local["effect_names"][idx], rotation=xlabel_rotation)

            if "actual" in data_dict_local.keys():
                title = "Predicted: %0.4f | Actual: %0.4f" % (data_dict_local["predicted"].ravel()[0],
                                                              data_dict_local["actual"].ravel()[0])
            else:
                title = "Predicted: %0.4f" % (data_dict_local["predicted"].ravel()[0])
            plt.title(title, fontsize=15)

            if max_ids > 0:
                save_path = folder + name
                if save_eps:
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                    fig.savefig("%s.eps" % save_path, bbox_inches="tight", dpi=100)
                if save_png:
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                    fig.savefig("%s.png" % save_path, bbox_inches="tight", dpi=100)

        data_dict_local = self.local_effect_explain(x, y)
        for item in data_dict_local:
            local_visualize(item)

    def show_local_feature_explain(self, x, y=None, xlabel_rotation=0, folder="./", name="demo", save_png=False,
                                   save_eps=False):
        """
        Show local explanation of given samples.

        Parameters
        ----------
        x : np.ndarray of shape (n_samples, n_features)
            Data features.
        y : np.ndarray of shape (n_samples, )
            Target response.
        xlabel_rotation : int
            Rotation angle of x-axis labels, by default 0.
        folder : str
            The path of folder to save figure, by default "./".
        name : str
            Name of the file, by default "local_explain".
        save_png : boolean
            Whether to save the plot in PNG format, by default False.
        save_eps : boolean
            Whether to save the plot in EPS format, by default False.
        """

        def local_visualize(data_dict_local):

            max_ids = data_dict_local["scores"].shape[0]
            idx = np.argsort(np.abs(data_dict_local["scores"]))[::-1]
            fig = plt.figure(figsize=(round((max_ids + 1) * 0.6), 4))
            plt.bar(np.arange(max_ids), data_dict_local["scores"][idx])
            plt.xticks(np.arange(max_ids), data_dict_local["effect_names"][idx], rotation=xlabel_rotation)

            if "actual" in data_dict_local.keys():
                title = "Predicted: %0.4f | Actual: %0.4f" % (data_dict_local["predicted"].ravel()[0],
                                                              data_dict_local["actual"].ravel()[0])
            else:
                title = "Predicted: %0.4f" % (data_dict_local["predicted"].ravel()[0])
            plt.title(title, fontsize=15)

            if max_ids > 0:
                save_path = folder + name
                if save_eps:
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                    fig.savefig("%s.eps" % save_path, bbox_inches="tight", dpi=100)
                if save_png:
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                    fig.savefig("%s.png" % save_path, bbox_inches="tight", dpi=100)

        data_dict_local = self.local_feature_explain(x, y)
        for item in data_dict_local:
            local_visualize(item)

    def show_global_explain(self, main_effect_num=None, interaction_num=None,
                            cols_per_row=4, folder="./", name="demo", save_png=False, save_eps=False):
        """
        Show the fitted main effects and interactions.

        Parameters
        ----------
        main_effect_num : int or None
            The number of top main effects to show, by default None,
            As main_effect_num=None, all main effects would be shown.
        interaction_num : int or None
            The number of top interactions to show, by default None,
            As interaction_num=None, all main effects would be shown.
        cols_per_row : int
            The number of subfigures each row, by default 4.
        folder : str
            The path of folder to save figure, by default "./".
        name : str
            Name of the file, by default "global_explain".
        save_png : boolean
            Whether to save the plot in PNG format, by default False.
        save_eps : boolean
            Whether to save the plot in EPS format, by default False.
        """
        data_dict_global = self.global_explain()
        maineffect_count = 0
        componment_scales = []
        for key, item in data_dict_global.items():
            componment_scales.append(item["importance"])
            if item["type"] != "pairwise":
                maineffect_count += 1

        componment_scales = np.array(componment_scales)
        sorted_index = np.argsort(componment_scales)
        active_index = sorted_index[componment_scales[sorted_index].cumsum() > 0][::-1]
        active_univariate_index = active_index[active_index < maineffect_count][:main_effect_num]
        active_interaction_index = active_index[active_index >= maineffect_count][:interaction_num]
        max_ids = len(active_univariate_index) + len(active_interaction_index)

        if max_ids == 0:
            return

        idx = 0
        fig = plt.figure(figsize=(5.2 * cols_per_row, 4 * int(np.ceil(max_ids / cols_per_row))))
        outer = gridspec.GridSpec(int(np.ceil(max_ids / cols_per_row)), cols_per_row, wspace=0.25, hspace=0.35)
        for indice in active_univariate_index:
            feature_name = list(data_dict_global.keys())[indice]
            item = data_dict_global[feature_name]
            if self.estimator.feature_types[item["fidx"][0]] == "categorical":
                inner = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=outer[idx],
                                                         wspace=0.1, hspace=0.1, height_ratios=[6, 1])
                ax1 = plt.Subplot(fig, inner[0])
                ax1.bar(item["inputs"], item["outputs"])
                ax1.set_xticklabels([])
                fig.add_subplot(ax1)

                ax2 = plt.Subplot(fig, inner[1])
                ax2.bar(item["density"]["names"], item["density"]["scores"])
                ax2.get_shared_x_axes().join(ax1, ax2)
                ax2.autoscale()
                ax2.set_yticklabels([])
                fig.add_subplot(ax2)
            else:
                inner = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=outer[idx], wspace=0.1, hspace=0.1,
                                                         height_ratios=[6, 1])
                ax1 = plt.Subplot(fig, inner[0])
                ax1.plot(item["inputs"], item["outputs"])
                ax1.set_xticklabels([])
                fig.add_subplot(ax1)

                ax2 = plt.Subplot(fig, inner[1])
                xint = ((np.array(item["density"]["names"][1:]) + np.array(item["density"]["names"][:-1])) / 2).reshape(
                    [-1, 1]).reshape([-1])
                ax2.bar(xint, item["density"]["scores"], width=xint[1] - xint[0])
                ax2.get_shared_x_axes().join(ax1, ax2)
                ax2.set_yticklabels([])
                ax2.autoscale()
                fig.add_subplot(ax2)

            ax1.set_title(feature_name + " (" + str(np.round(100 * item["importance"], 1)) + "%)", fontsize=15)
            idx += 1

        for indice in active_interaction_index:
            feature_name = list(data_dict_global.keys())[indice]
            item = data_dict_global[feature_name]
            ax = plt.Subplot(fig, outer[idx])
            interact_plot = ax.imshow(item["outputs"], interpolation="nearest",
                                      aspect="auto",
                                      extent=[self.min_value_[item["fidx"][0]], self.max_value_[item["fidx"][0]],
                                              self.min_value_[item["fidx"][1]], self.max_value_[item["fidx"][1]]])
            response_precision = max(int(- np.log10(np.max(item["outputs"]) - np.min(item["outputs"]))) + 2, 0)
            fig.colorbar(interact_plot, ax=ax, orientation="vertical", format="%0." + str(response_precision) + "f",
                         use_gridspec=True)
            ax.set_title(feature_name + " (" + str(np.round(100 * item["importance"], 1)) + "%)", fontsize=15)
            fig.add_subplot(ax)
            idx += 1

            if len(str(ax.get_xticks())) > 60:
                ax.xaxis.set_tick_params(rotation=20)

    def show_feature_importance(self, xlabel_rotation=0, folder="./", name="feature_importance", save_eps=False,
                                save_png=False):
        """
        Visualize the feature importance.

        Parameters
        ----------
        xlabel_rotation : int
            Rotation angle of x-axis labels, by default 0.
        folder : str
            The path of folder to save figure, by default "./".
        name : str
            Name of the file, by default "feature_importance".
        save_png : boolean
            Whether to save the plot in PNG format, by default False.
        save_eps : boolean
            Whether to save the plot in EPS format, by default False.
        """
        all_ir = []
        all_names = []
        feature_names = self.feature_names_
        feature_importance = self.feature_importance_
        for name, importance in zip(feature_names, feature_importance):
            if importance > 0:
                all_ir.append(importance)
                all_names.append(name)

        max_ids = len(all_names)
        if max_ids > 0:
            fig = plt.figure(figsize=(0.4 + 0.65 * max_ids, 4))
            ax = plt.axes()
            ax.bar(np.arange(len(all_ir)), [ir for ir, _ in sorted(zip(all_ir, all_names))][::-1])
            ax.set_xticks(np.arange(len(all_ir)))
            ax.set_xticklabels([name for _, name in sorted(zip(all_ir, all_names))][::-1], rotation=xlabel_rotation)
            plt.ylim(0, np.max(all_ir) + 0.05)
            plt.xlim(-1, len(all_names))
            plt.title("Feature Importance")

            save_path = folder + name
            if save_eps:
                if not os.path.exists(folder):
                    os.makedirs(folder)
                fig.savefig("%s.eps" % save_path, bbox_inches="tight", dpi=100)
            if save_png:
                if not os.path.exists(folder):
                    os.makedirs(folder)
                fig.savefig("%s.png" % save_path, bbox_inches="tight", dpi=100)

    def show_effect_importance(self, xlabel_rotation=0, folder="./", name="effect_importance", save_eps=False,
                               save_png=False):
        """
        Visualize the effect importance.

        Parameters
        ----------
        xlabel_rotation : int
            Rotation angle of x-axis labels, by default 0.
        folder : str
            The path of folder to save figure, by default "./".
        name : str
            Name of the file, by default "effect_importance".
        save_png : boolean
            Whether to save the plot in PNG format, by default False.
        save_eps : boolean
            Whether to save the plot in EPS format, by default False.
        """
        data_dict_global = self.global_explain()
        all_ir = []
        all_names = []
        for key, item in data_dict_global.items():
            if item["importance"] > 0:
                all_ir.append(item["importance"])
                all_names.append(key)

        max_ids = len(all_names)
        if max_ids > 0:
            fig = plt.figure(figsize=(0.4 + 0.65 * max_ids, 4))
            ax = plt.axes()
            ax.bar(np.arange(len(all_ir)), [ir for ir, _ in sorted(zip(all_ir, all_names))][::-1])
            ax.set_xticks(np.arange(len(all_ir)))
            ax.set_xticklabels([name for _, name in sorted(zip(all_ir, all_names))][::-1], rotation=xlabel_rotation)
            plt.ylim(0, np.max(all_ir) + 0.05)
            plt.xlim(-1, len(all_names))
            plt.title("Effect Importance")

            save_path = folder + name
            if save_eps:
                if not os.path.exists(folder):
                    os.makedirs(folder)
                fig.savefig("%s.eps" % save_path, bbox_inches="tight", dpi=100)
            if save_png:
                if not os.path.exists(folder):
                    os.makedirs(folder)
                fig.savefig("%s.png" % save_path, bbox_inches="tight", dpi=100)
