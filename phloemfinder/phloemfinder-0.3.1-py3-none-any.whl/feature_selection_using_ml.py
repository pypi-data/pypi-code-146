#!/usr/bin/env python3 

import os
from warnings import WarningMessage
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.inspection import permutation_importance

from autosklearn.classification import AutoSklearnClassifier
from autosklearn.metrics import balanced_accuracy, precision, recall, f1

from tpot import TPOTClassifier
from tpot.export_utils import set_param_recursive

from phloemfinder.utils import compute_metrics_classification 

class MetabolitePhenotypeFeatureSelection:
    '''
    A class to perform metabolite feature selection using phenotyping and metabolic data. 

    - Perform sanity checks on input dataframes (values above 0, etc.).
    - Get a baseline performance of a simple Machine Learning Random Forest ("baseline").
    - Perform automated Machine Learning model selection using autosklearn.
        Using metabolite data, train a model to predict phenotypes.
        Yields performance metrics (balanced accuracy, precision, recall) on the selected model.
    - Extracts performance metrics from the best ML model. 
    - Extracts the best metabolite features based on their feature importance and make plots per sample group. 

    Parameters
    ----------
    metabolome_csv: string
        A path to a .csv file with the cleaned up metabolome data (unreliable features filtered out etc.)
        Use the MetabolomeAnalysis class methods. 
        Shape of the dataframe is usually (n_samples, n_features) with n_features >> n_samples
    phenotype_csv: string
        A path to a .csv file with the phenotyping data. 
        Should be two columns at least with: 
          - column 1 containing the sample identifiers
          - column 2 containing the phenotypic class e.g. 'resistant' or 'sensitive'
    metabolome_feature_id_col: string, default='feature_id'
        The name of the column that contains the feature identifiers.
        Feature identifiers should be unique (=not duplicated).
    phenotype_sample_id: string, default='sample_id'
        The name of the column that contains the sample identifiers.
        Sample identifiers should be unique (=not duplicated).


    Attributes
    ----------
    metabolome_validated: bool
      Is the metabolome file valid for Machine Learning? (default is False)   

    phenotype_validated: bool
      Is the phenotype file valid for Machine Learning? (default is False)

    baseline_performance: float 
      The baseline performance computed with get_baseline_performance() i.e. using a simple Random Forest model. 
      Search for the best ML model using search_best_model() should perform better than this baseline performance. 

    best_ensemble_models_searched: bool
      Is the search for best ensemble model using auto-sklearn already performed? (default is False)

    metabolome: pandas.core.frame.DataFrame
      The validated metabolome dataframe of shape (n_features, n_samples).
    
    phenotype: pandas.core.frame.DataFrame
      A validated phenotype dataframe of shape (n_samples, 1)
      Sample names in the index and one column named 'phenotype' with the sample classes.
    
    baseline_performance: str
      Average balanced accuracy score (-/+ standard deviation) of the basic Random Forest model. 
    
    best_model: sklearn.pipeline.Pipeline
      A scikit-learn pipeline that contains one or more steps.
      It is the best performing pipeline found by TPOT automated ML search.

    feature_importances: pandas.core.frame.DataFrame
       A Pandas dataframe that contains feature importance information using scikit-learn permutation_importance()
        Mean of feature importance over n_repeats.
        Standard deviation over n_repeats.
        Raw permutation importance scores.
    
    
    Methods
    --------
    validate_input_metabolome_df()
      Validates the dataframe read from the 'metabolome_csv' input file.
    
    validate_input_phenotype_df()
      Validates the phenotype dataframe read from the 'phenotype_csv' input file.
    
    get_baseline_performance()
      Fits a basic Random Forest model to get default performance metrics. 
    
    search_best_model_with_tpot_and_get_feature_importances()
      Search for the best ML pipeline using TPOT genetic programming method.
      Computes and output performance metrics from the best pipeline.
      Extracts feature importances using scikit-learn permutation_importance() method. 

    

    Notes
    --------

    Example of an input metabolome .csv file

        | feature_id  | genotypeA_rep1 | genotypeA_rep2 | genotypeA_rep3 | genotypeA_rep4 |
        |-------------|----------------|----------------|----------------|----------------|
        | metabolite1 |   1246         | 1245           | 12345          | 12458          |
        | metabolite2 |   0            | 0              | 0              | 0              |
        | metabolite3 |   10           | 0              | 0              | 154            |

    Example of an input phenotype .csv file

        | sample_id      | phenotype | 
        |----------------|-----------|
        | genotypeA_rep1 | sensitive | 
        | genotypeA_rep2 | sensitive |   
        | genotypeA_rep3 | sensitive |
        | genotypeA_rep4 | sensitive | 
        | genotypeB_rep1 | resistant |   
        | genotypeB_rep2 | resistant |
    
    '''
    # Class attribute shared among all instances of the class
    # By default the metabolome and phenotype data imported from .csv files will have to be validated
    # By default all filters have not been executed (blank filtering, etc.)
    # Baseline performance of a simple ML model as well as search of best model are also None/False by default. 
    metabolome_validated=False
    phenotype_validated=False
    baseline_performance=None
    best_ensemble_models_searched=False

    # Class constructor method
    def __init__(
        self, 
        metabolome_csv, 
        phenotype_csv,
        metabolome_feature_id_col='feature_id', 
        phenotype_sample_id='sample_id'):
        
        # Import metabolome dataframe and verify presence of feature id column
        self.metabolome = pd.read_csv(metabolome_csv)
        if metabolome_feature_id_col not in self.metabolome.columns:
            raise ValueError("The specified column with feature identifiers '{0}' is not present in your '{1}' file.".format(metabolome_feature_id_col,os.path.basename(metabolome_csv)))
        else:
            self.metabolome.set_index(metabolome_feature_id_col, inplace=True)

        # Import phenotype dataframe and verify presence of sample id column
        self.phenotype = pd.read_csv(phenotype_csv)
        if phenotype_sample_id not in self.phenotype.columns:
            raise ValueError("The specified column with sample identifiers '{0}' is not present in your '{1}' file.".format(phenotype_sample_id, os.path.basename(phenotype_csv)))
        else:
            try: 
                self.phenotype.set_index(phenotype_sample_id, inplace=True)
            except:
                raise IndexError("Values for sample identifiers have to be unique. Check your ", phenotype_sample_id, " column.")

    ################
    ## Verify inputs
    ################
    def validate_input_metabolome_df(self):
        '''
        Validates the dataframe containing the feature identifiers, metabolite values and sample names.
        Will place the 'feature_id_col' column as the index of the validated dataframe. 
        The validated metabolome dataframe is stored as the 'validated_metabolome' attribute 
        
        
        Returns
        --------
        self: object
          Object with metabolome_validated set to True

        Example of a validated output metabolome dataframe

                      | genotypeA_rep1 | genotypeA_rep2 | genotypeA_rep3 | genotypeA_rep4 |
                      |----------------|----------------|----------------|----------------|
          feature_id
        | metabolite1 |   1246         | 1245           | 12345          | 12458          |
        | metabolite2 |   0            | 0              | 0              | 0              |
        | metabolite3 |   10           | 0              | 0              | 154            |
        '''
        
        if np.any(self.metabolome.values < 0):
            raise ValueError("Sorry, metabolite values have to be zero or positive integers (>=0)")
        else:
            self.metabolome_validated = True
            print("Metabolome data validated.")
    
    def validate_input_phenotype_df(self, phenotype_class_col="phenotype"):
        '''
        Validates the dataframe containing the phenotype classes and the sample identifiers

        Params
        ------
        phenotype_class_col: string, default="phenotype"
            The name of the column to be used 

        Returns
        --------
        self: object
          Object with phenotype_validated set to True

        Notes
        --------
        Example of an input phenotype dataframe
        

        | sample_id      | phenotype | 
        |----------------|-----------|
        | genotypeA_rep1 | sensitive | 
        | genotypeA_rep2 | sensitive |   
        | genotypeA_rep3 | sensitive |
        | genotypeA_rep4 | sensitive | 
        | genotypeB_rep1 | resistant |   
        | genotypeB_rep2 | resistant |

        Example of a validated output phenotype dataframe. 

                         | phenotype | 
                         |-----------|
          sample_id      
        | genotypeA_rep1 | sensitive | 
        | genotypeA_rep2 | sensitive |   
        | genotypeA_rep3 | sensitive |
        | genotypeA_rep4 | sensitive | 
        | genotypeB_rep1 | resistant |   
        | genotypeB_rep2 | resistant |

        Example
        -------
        >> fs = MetabolitePhenotypeFeatureSelection(
        >>        metabolome_csv="clean_metabolome.csv", 
        >>        phenotype_csv="phenotypes_test_data.csv", 
        >>        phenotype_sample_id='sample')
        >> fs.validate_input_phenotype_df()

        '''
        n_distinct_classes = self.phenotype[phenotype_class_col].nunique()
        try:
            n_distinct_classes == 2
            self.phenotype_validated = True    
            print("Phenotype data validated.")
        except:
            raise ValueError("The number of distinct phenotypic classes in the {0} column should be exactly 2.".format(phenotype_class_col))
    
    #################
    ## Baseline model
    #################
    def get_baseline_performance(
      self, 
      class_of_interest,
      kfold=5, 
      train_size=0.8,
      random_state=123,
      scoring_metric='balanced_accuracy'):
        '''
        Takes the phenotype and metabolome dataset and compute a simple Random Forest analysis with default hyperparameters. 
        This will give a base performance for a Machine Learning model that has then to be optimised using autosklearn

        k-fold cross-validation is performed to mitigate split effects on small datasets. 

        Parameters
        ----------
        class_of_interest: str
          The name of the class of interest also called "positive class".
          This class will be used to calculate recall_score and precision_score. 
          Recall score = TP / (TP + FN) with TP: true positives and FN: false negatives.
          Precision score = TP / (TP + FP) with TP: true positives and FP: false positives. 

        kfold: int, optional
          Cross-validation strategy. Default is to use a 5-fold cross-validation. 
        
        train_size: float or int, optional
          If float, should be between 0.5 and 1.0 and represent the proportion of the dataset to include in the train split.
          If int, represents the absolute number of train samples. If None, the value is automatically set to the complement of the test size.
          Default is 0.8 (80% of the data used for training).

        random_state: int, optional
          Controls both the randomness of the train/test split  samples used when building trees (if bootstrap=True) and the sampling of the features to consider when looking for the best split at each node (if max_features < n_features). See Glossary for details.
          You can change this value several times to see how it affects the best ensemble model performance.
          Default is 123.


        scoring_metric: str, optional
          A valid scoring value (default="balanced_accuracy")
          To get a complete list, type:
          >> from sklearn.metrics import SCORERS 
          >> sorted(SCORERS.keys()) 
          balanced accuracy is the average of recall obtained on each class. 

        Returns
        -------
        self: object
          Object with baseline_performance attribute.
        
        Example
        -------
        >>> fs = MetabolitePhenotypeFeatureSelection(
                   metabolome_csv="../tests/clean_metabolome.csv", 
                   phenotype_csv="../tests/phenotypes_test_data.csv", 
                   phenotype_sample_id='sample')
            fs.get_baseline_performance()

        '''
        try:
            self.metabolome_validated == True
        except:
            raise ValueError("Please validate metabolome data first using the validate_input_metabolome_df() method.")

        try:
            self.phenotype_validated == True
        except:
            raise ValueError("Please validate phenotype data first using the validate_input_phenotype_df() method.")

        X = self.metabolome.transpose()
        y = self.phenotype.values.ravel() # ravel makes the array contiguous
        X_train, X_test, y_train, y_test = train_test_split(
          X, y, 
          train_size=train_size, 
          random_state=random_state, 
          stratify=y)

        # Train model and assess performance
        clf = RandomForestClassifier(n_estimators=1000, random_state=random_state)
        scores = cross_val_score(clf, X_train, y_train, scoring=scoring_metric, cv=kfold)
        average_scores = np.average(scores).round(3) * 100
        stddev_scores = np.std(scores).round(3) * 100
        print("====== Training a basic Random Forest model =======")
        baseline_performance = "Average {0} score on training data is: {1:.3f} % -/+ {2:.2f}".format(scoring_metric, average_scores, stddev_scores)
        print(baseline_performance)
        print("\n")
        print("====== Performance on test data of the basic Random Forest model =======")
        clf.fit(X_train, y_train)
        predictions = clf.predict(X_test)
        model_balanced_accuracy_score = balanced_accuracy(y_true=y_test, y_pred=predictions).round(3) * 100 
        print("Average {0} score on test data is: {1:.3f} %".format(scoring_metric, model_balanced_accuracy_score))
        self.baseline_performance = baseline_performance

    # TODO: make decorator function to check arguments     
    # See -> https://www.pythonforthelab.com/blog/how-to-use-decorators-to-validate-input/
    def search_best_model_with_tpot_and_get_feature_importances(
        self,
        class_of_interest,
        scoring_metric='balanced_accuracy',
        kfolds=3,
        train_size=0.8,
        max_time_mins=5,
        max_eval_time_mins=1,
        random_state=123,
        tpot_config_dict=None,
        n_permutations=10):
      '''
      Search for the best ML model with TPOT genetic programming methodology and extracts feature importances. 

      A resampling strategy called "cross-validation" will be performed on a subset of the data (training data) to increase 
      the model generalisation performance. Finally, the model performance is tested on the unseen test data subset.  
      
      By default, TPOT will make use of a set of preprocessors (e.g. Normalizer, PCA) and algorithms (e.g. RandomForestClassifier)
      defined in the default config (classifier.py).
      See: https://github.com/EpistasisLab/tpot/blob/master/tpot/config/classifier.py

      Parameters
      ----------
      class_of_interest: str
          The name of the class of interest also called "positive class".
          This class will be used to calculate recall_score and precision_score. 
          Recall score = TP / (TP + FN) with TP: true positives and FN: false negatives.
          Precision score = TP / (TP + FP) with TP: true positives and FP: false positives. 

      scoring_metric: str, optional
        Function used to evaluate the quality of a given pipeline for the classification problem. 
        Default is 'balanced accuracy'. 
        The following built-in scoring functions can be used:
          'accuracy', 'adjusted_rand_score', 'average_precision', 'balanced_accuracy', 
          'f1', 'f1_macro', 'f1_micro', 'f1_samples', 'f1_weighted', 'neg_log_loss', 
          'precision' etc. (suffixes apply as with ‘f1’), 'recall' etc. (suffixes apply as with ‘f1’), 
          ‘jaccard’ etc. (suffixes apply as with ‘f1’), 'roc_auc', ‘roc_auc_ovr’, ‘roc_auc_ovo’, ‘roc_auc_ovr_weighted’, ‘roc_auc_ovo_weighted’ 

      kfolds: int, optional
        kfolds: int, optional
        Number of folds for the stratified K-Folds cross-validation strategy. Default is 3-fold cross-validation. 
        Has to be comprised between 3 and 10 i.e. 3 <= kfolds =< 10
        See https://scikit-learn.org/stable/modules/cross_validation.html
      
      train_size: float or int, optional
        If float, should be between 0.5 and 1.0 and represent the proportion of the dataset to include in the train split.
        If int, represents the absolute number of train samples. If None, the value is automatically set to the complement of the test size.
        Default is 0.8 (80% of the data used for training).

      max_time_mins: int, optional
        How many minutes TPOT has to optimize the pipeline (in total). Default is 5 minutes.
        This setting will allow TPOT to run until max_time_mins minutes elapsed and then stop.
        Try short time intervals (5, 10, 15min) and then see if the model score on the test data improves. 
      
      max_eval_time_mins: float, optional 
        How many minutes TPOT has to evaluate a single pipeline. Default is 1min. 
        This time has to be smaller than the 'max_time_mins' setting.

      random_state: int, optional
          Controls both the randomness of the train/test split  samples used when building trees (if bootstrap=True) and the sampling of the features to consider when looking for the best split at each node (if max_features < n_features). See Glossary for details.
          You can change this value several times to see how it affects the best ensemble model performance.
          Default is 123.

      n_permutations: int, optional
        Number of permutations used to compute feature importances from the best model using scikit-learn permutation_importance() method.
        Default is 10 permutations.
      
      tpot_config_dict: Python dictionary, str or None, optional.
        A configuration dictionary for customizing the operators and parameters that TPOT searches. 
        Default is None meaning that TPOT will buse the default configuration. See https://epistasislab.github.io/tpot/using/#customizing-tpots-operators-and-parameters 
        A customized Python dictionary can be made and passed to TPOTClassifier. See https://epistasislab.github.io/tpot/using/#customizing-tpots-operators-and-parameters
       

       Returns
        ------
        self: object
          The object with best model searched and feature importances computed. 

       See also
       --------

       Notes
       -----
       Permutation importances are calculated on the training set
       Permutation importances can be computed either on the training set or on a held-out testing or validation set.
       Using a held-out set makes it possible to highlight which features contribute the most to the generalization power of the inspected model. 
       Features that are important on the training set but not on the held-out set might cause the model to overfit.
       https://scikit-learn.org/stable/modules/permutation_importance.html#permutation-importance 
          
      '''
      X = self.metabolome.transpose().to_numpy(dtype='float64')
      y = self.phenotype.values.ravel()
        
      # Verify input arguments
      try:
        3 <= kfolds <= 10
      except:
        raise ValueError('kfolds argument has to be comprised between 3 and 10')
        
      try:
        0.5 < train_size < 0.9
      except:
        raise ValueError('train_size has to be comprised between 0.5 and 0.9')

      try:
        class_of_interest in set(y)
      except:
        raise ValueError('The class_of_interest value "{0}" has to be in the phenotype labels {1}'.format(class_of_interest, set(y)))
      
      ### Automated search for best model/pipeline
      X_train, X_test, y_train, y_test = train_test_split(
          X, y, 
          train_size=train_size, 
          random_state=random_state, 
          stratify=y)
      tpot = TPOTClassifier(
        generations=None, # If None, the parameter max_time_mins must be defined as the runtime limit. 
        max_time_mins=max_time_mins,
        max_eval_time_mins=max_eval_time_mins,
        cv=kfolds,        # Number of folds in an unshuffled StratifiedKFold.
        config_dict=tpot_config_dict,
        random_state=random_state, 
        verbosity=0)
      tpot.fit(X_train, y_train)
      best_pipeline = make_pipeline(tpot.fitted_pipeline_)
      
      ### Fit best model/pipeline
      if len(best_pipeline) == 1:
        # one step pipeline thus one model  
        one_step_pipeline = best_pipeline["pipeline"][-1]
        one_step_pipeline.fit(X_train, y_train)
        print(one_step_pipeline.score(X_test, y_test))
        predictions = one_step_pipeline.predict(X_test)
        print("============ Performance of ML model on train data =============")
        print("Train {0} score {1:.3f}".format(scoring_metric, one_step_pipeline.score(X_train, y_train).round(3)*100))
        print("\n")
        print("============ Performance of ML model on test data =============")
        print(compute_metrics_classification(y_predictions=predictions, y_trues=y_test, positive_class=class_of_interest))
        self.best_model = one_step_pipeline
      else:
        # multiple steps pipeline
        n_steps_pipeline = make_pipeline(tpot.fitted_pipeline_)
        set_param_recursive(best_pipeline, 'random_state', random_state)
        n_steps_pipeline.fit(X_train, y_train)
        predictions = n_steps_pipeline.predict(X_test)
        training_score = n_steps_pipeline.score(X_train, y_train).round(3) * 100
        print("============ Performance of ML model on train data =============")
        print("Train {0} score {1:.3f}".format(scoring_metric, training_score))
        print("\n")
        print("============ Performance of ML model on test data =============")
        print(compute_metrics_classification(y_predictions=predictions, y_trues=y_test, positive_class=class_of_interest))
        self.best_model = n_steps_pipeline

      ### Compute feature importances
      # Has to be done on the same train/test split. 
      print("\n")
      print("======== Computing feature importances on the training set =======")
      feature_importances_training_set = permutation_importance(
        self.best_model, 
        X=X_train, 
        y=y_train, 
        scoring=scoring_metric, 
        n_repeats=n_permutations, 
        random_state=random_state)
      mean_imp = pd.DataFrame(feature_importances_training_set.importances_mean, columns=["mean_var_imp"])
      std_imp = pd.DataFrame(feature_importances_training_set.importances_std, columns=["std_var_imp"])
      raw_imp = pd.DataFrame(feature_importances_training_set.importances, columns=["perm" + str(i) for i in range(n_permutations)])

      feature_importances = pd.concat([mean_imp, std_imp], axis=1).set_index(self.metabolome.index.values).sort_values('mean_var_imp', ascending=False)

      self.feature_importances = feature_importances
      self.feature_importances_permutations = raw_imp