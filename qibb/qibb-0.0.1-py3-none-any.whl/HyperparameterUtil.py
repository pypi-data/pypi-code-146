from hyperopt import fmin, tpe, hp, anneal, Trials
from sklearn.model_selection import cross_val_score

class hyperparameter_tuning():

    '''for the hyperparameter tuning we use the hyperopts, and it's return the best values for each parameters'''

    def __init__(self):
        pass

    def objective(self,params):
        ''' Here we create the one objective and this take the input as x and y train data, scoring values and model which we want to train our models.'''
        model = self.clf(**params)
        score = cross_val_score(model, self.x, self.y, cv= self.cv, scoring= self.score).mean()
        return score

    
    def tune_model(self,clf, x, y, cv, score, hyperperameter,max_evals):
        ''' here we use the hyperopts for find the best parameters using the hyperopts,
        we use this function only when user has not a objective function'''
        self.clf = clf
        self.x = x
        self.y = y
        self.cv = cv
        self.score = score
        self.hyperperameter = hyperperameter
        self.max_evals = max_evals

        search_space = {}
        for i in self.hyperperameter.keys():
            search_space[i] = hp.choice(i, self.hyperperameter[i])

        best = fmin(self.objective, search_space, algo=tpe.suggest, max_evals=self.max_evals)

        # print(best)

        return best

    def tune_objective(self , objective, hyperperameter , max_evals):
        '''If user has objective function then we use direct this function.'''
        self.objective = objective
        self.max_evals = max_evals
        self.hyperperameter = hyperperameter

        search_space = {}
        for i in self.hyperperameter.keys():
            search_space[i] = hp.choice(i, self.hyperperameter[i])

        best = fmin(self.objective, search_space, algo=tpe.suggest, max_evals=self.max_evals)

        return best
        