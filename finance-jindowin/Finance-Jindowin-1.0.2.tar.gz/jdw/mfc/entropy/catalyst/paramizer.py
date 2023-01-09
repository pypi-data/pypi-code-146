# -*- coding: utf-8 -*-


class Paramizer(object):

    @classmethod
    def HuberRegression(cls, **kwargs):
        return {
            'max_iter': [i for i in range(80, 180, 20)],
            'epsilon': [(i / 100) for i in range(100, 180, 15)],
            'alpha': [(i / 100000) for i in range(10, 40, 5)]
        }

    @classmethod
    def SGDRegression(cls, **kwargs):
        return {
            'penalty': ['l2', 'l1'],
            'alpha': [(i / 100000) for i in range(10, 40, 5)],
            'l1_ratio': [(i / 1000) for i in range(10, 40, 5)],
            'max_iter': [i for i in range(800, 3000, 50)],
        }

    @classmethod
    def RidgeRegression(cls, **kwargs):
        return {
            'alpha': [(i / 10000000) for i in range(10, 500, 20)],
            'max_iter': [i for i in range(180, 380, 10)],
            'solver': ['auto', 'svd', 'lsqr', 'sparse_cg', 'saga']
        }

    @classmethod
    def BayesianRegression(cls, **kwargs):
        return {
            'n_iter': [i for i in range(180, 380, 10)],
            'alpha_1': [(i / 10000000) for i in range(10, 500, 20)],
            'alpha_2': [(i / 10000000) for i in range(10, 500, 20)],
            'lambda_1': [(i / 10000000) for i in range(10, 500, 20)],
            'lambda_2': [(i / 10000000) for i in range(10, 500, 20)]
        }

    @classmethod
    def LogisticRegression(cls, **kwargs):
        return {
            'penalty': ['l1', 'l2', 'elasticnet', 'none'],
            'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'],
            'max_iter': [i for i in range(80, 180, 10)]
        }

    @classmethod
    def LassoRegression(cls, **kwargs):
        return {
            'alpha': [1.0],
            'fit_intercept': [True, False],
            'normalize': [True, False],
            'selection': ['cyclic', 'random'],
            'positive': [True, False],
            'max_iter': [i for i in range(80, 180, 10)]
        }

    @classmethod
    def RandomForestRegressor(cls, **kwargs):
        return {
            'n_estimators': [i for i in range(80, 180, 10)],
            'max_depth': [i for i in range(3, 5, 2)],
            'max_features': ['auto', 'sqrt', 'log2']
        }

    @classmethod
    def ExtraTreesRegressor(cls, **kwargs):
        return {
            'n_estimators': [i for i in range(80, 180, 10)],
            'max_depth': [i for i in range(3, 5, 2)],
            'max_features': ['auto', 'sqrt', 'log2']
        }

    @classmethod
    def BaggingRegressor(cls, **kwargs):
        return {
            'n_estimators': [i for i in range(80, 180, 10)],
            'max_depth': [i for i in range(3, 5, 2)],
            'max_features': ['auto', 'sqrt', 'log2']
        }

    @classmethod
    def AdaBoostRegressor(cls, **kwargs):
        return {
            'n_estimators': [i for i in range(50, 150, 10)],
            'learning_rate': [(i / 10) for i in range(1, 10, 2)],
            'loss': ['linear', 'square', 'exponential']
        }

    @classmethod
    def DecisionTreeRegressor(cls, **kwargs):
        return {
            'criterion': ['mse', 'friedman_mse', 'mae', 'poisson'],
            'splitter': ['best', 'random']
        }

    @classmethod
    def GradientBoostingRegressor(cls, **kwargs):
        return {
            'n_estimators': [i for i in range(50, 150, 10)],
            'learning_rate': [(i / 10) for i in range(1, 10, 2)],
            'loss': ['ls', 'lad', 'huber', 'quantile'],
            'criterion': ['friedman_mse', 'mse', 'mae']
        }

    @classmethod
    def XGBRegressor(cls, **kwargs):
        return {
            'max_depth': [i for i in range(6, 15, 2)],
            'n_estimators': [i for i in range(50, 150, 10)],
            'learning_rate': [(i / 100) for i in range(1, 10, 2)]
        }

    @classmethod
    def LGBMRegressor(cls, **kwargs):
        return {
            'max_depth': [i for i in range(6, 15, 2)],
            'n_estimators': [i for i in range(50, 150, 10)],
            'learning_rate': [(i / 100) for i in range(1, 10, 2)]
        }
