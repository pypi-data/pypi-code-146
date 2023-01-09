class BaseEstimator:
  pass

class ClassifierMixin:
  pass

from mlpack.adaboost_train import adaboost_train
from mlpack.adaboost_classify import adaboost_classify
from mlpack.adaboost_probabilities import adaboost_probabilities
try: 
  from sklearn.base import BaseEstimator, ClassifierMixin
except:
  pass

class Adaboost(BaseEstimator, ClassifierMixin):
  def __init__(self,
               check_input_matrices = False,
               copy_all_inputs = False,
               iterations = None,
               tolerance = None,
               verbose = False,
               weak_learner = None,
              ):

    # serializable attributes.
    self._AdaBoostModel = None

    # hyper-parameters.
    self.check_input_matrices = check_input_matrices
    self.copy_all_inputs = copy_all_inputs
    self.iterations = iterations
    self.tolerance = tolerance
    self.verbose = verbose
    self.weak_learner = weak_learner

  def fit(self, 
          X = None,
          y = None,
          training = None,
          labels = None,
         ):

    if X is not None and training is None:
      training = X
    elif X is not None and training is not None:
      raise ValueError("training and X both cannot be not None!")

    if y is not None and labels is None:
      labels = y
    elif y is not None and labels is not None:
      raise ValueError("labels and y both cannot be not None!")

    out = adaboost_train(training = training,
                         check_input_matrices = self.check_input_matrices,
                         copy_all_inputs = self.copy_all_inputs,
                         iterations = self.iterations,
                         labels = labels,
                         tolerance = self.tolerance,
                         verbose = self.verbose,
                         weak_learner = self.weak_learner,
                        )

    self._AdaBoostModel = out["output_model"]

    return self

  def predict(self, 
              X = None,
              test = None,
             ):

    if X is not None and test is None:
      test = X
    elif X is not None and test is not None:
      raise ValueError("test and X both cannot be not None!")

    out = adaboost_classify(input_model = self._AdaBoostModel,
                            test = test,
                            check_input_matrices = self.check_input_matrices,
                            copy_all_inputs = self.copy_all_inputs,
                            verbose = self.verbose,
                           )


    return out["predictions"]

  def predict_proba(self, 
                    X = None,
                    test = None,
                   ):

    if X is not None and test is None:
      test = X
    elif X is not None and test is not None:
      raise ValueError("test and X both cannot be not None!")

    out = adaboost_probabilities(input_model = self._AdaBoostModel,
                                 test = test,
                                 check_input_matrices = self.check_input_matrices,
                                 copy_all_inputs = self.copy_all_inputs,
                                 verbose = self.verbose,
                                )


    return out["probabilities"]

