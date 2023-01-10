"""
This module contains Python wrapper for SAP HANA PAL unified-clustering.

The following classes are available:
    * :class:`UnifiedClustering`
"""
#pylint: disable=too-many-lines, too-many-branches, unused-argument, super-with-arguments
#pylint: disable=line-too-long, too-many-statements, c-extension-no-member
#pylint: disable=too-many-locals, consider-using-dict-items
#pylint: disable=too-many-arguments, use-a-generator
#pylint: disable=ungrouped-imports
#pylint: disable=consider-using-f-string
import logging
import uuid
import warnings
#import pandas as pd
try:
    import pyodbc
except ImportError as error:
    pass
from hdbcli import dbapi

from hana_ml.ml_base import try_drop
from hana_ml.ml_exceptions import FitIncompleteError
from hana_ml.algorithms.pal.sqlgen import trace_sql
from hana_ml.algorithms.pal.utility import check_pal_function_exist
from hana_ml.algorithms.pal.tsa.arima import _col_index_check
from hana_ml.algorithms.pal.pal_base import (
    arg,
    PALBase,
    ParameterTable,
    require_pal_usable,
    pal_param_register,
    ListOfStrings)

logger = logging.getLogger(__name__) #pylint: disable=invalid-name

def _params_check(input_dict, param_map, func):
    update_params = {}

    if func == 'GMM':
        if input_dict.get('init_param') is None:
            err_msg = "init_param is a madantory parameter in Gaussianmixture!"
            logger.error(err_msg)
            raise KeyError(err_msg)
        # init_param is not None
        method = input_dict['init_param']
        if method == 'manual' and input_dict.get('init_centers') is None:
            err_msg = "init_centers is a madantory parameter when init_param is 'manual' in Gaussianmixture!"
            logger.error(err_msg)
            raise KeyError(err_msg)
        if method != 'manual' and input_dict.get('n_components') is None:
            err_msg = "n_components is a madantory parameter when init_param is not 'manual' in Gaussianmixture!"
            logger.error(err_msg)
            raise KeyError(err_msg)


    if func == 'DBSCAN':
        minpts_val = input_dict.get('minpts')
        eps_val = input_dict.get('eps')
        if minpts_val is None and eps_val is None:
            update_params['AUTO_PARAM'] = ('true', str)
        else:
            update_params['AUTO_PARAM'] = ('false', str)

        if (minpts_val is not None and eps_val is None) or (minpts_val is None and eps_val is not None):
            msg = 'minpts and eps need to be provided together in DBSCAN!'
            logger.error(msg)
            raise KeyError(msg)

        if ((input_dict.get('metric') is not None) and (input_dict.get('distance_level') is not None) and (input_dict['metric'] != input_dict['distance_level'])):
            input_dict['metric'] = None
            warn_msg = "when metric and distance_level are both entered in DBSCAN, distance_level takes precedence over metric!"
            warnings.warn(message=warn_msg)

    if func == 'AHC':
        if ((input_dict.get('affinity') is not None) and (input_dict.get('distance_level') is not None) and (input_dict['affinity'] != input_dict['distance_level'])):
            input_dict['affinity'] = None
            warn_msg = "when affinity and distance_level are both entered in AgglomerateHierarchicalClustering, distance_level takes precedence over affinity!"
            warnings.warn(message=warn_msg)

    for parm in input_dict:
        if parm in param_map.keys():
            if parm in ['categorical_variable']:
                pass
            elif parm == 'n_components':
                val = arg('n_components', input_dict['n_components'], int)
                update_params['INITIALIZE_PARAMETER'] = (str(val), str)
            elif parm == 'init_centers':
                val = arg('init_centers', input_dict['init_centers'], list)
                update_params['INITIALIZE_PARAMETER'] = (val, list)
            else:
                parm_val = input_dict[parm]
                if parm_val is not None:
                    arg_map = param_map[parm]
                    if arg_map[1] == ListOfStrings and isinstance(parm_val, str):
                        parm_val = [parm_val]
                    if len(arg_map) == 2:
                        update_params[arg_map[0]] = (arg(parm, parm_val, arg_map[1]), arg_map[1])
                    else:
                        update_params[arg_map[0]] = (arg(parm, parm_val, arg_map[2]), arg_map[1])
        else:
            err_msg = f"{parm} is not a valid parameter name for initializing a {func} model!"
            logger.error(err_msg)
            raise KeyError(err_msg)

    return update_params

def _listofstring_check(var, name):
    var_update = None
    if var is not None:
        if isinstance(var, str):
            var = [var]
        var_update = arg(name, var, ListOfStrings)
    return var_update

def _variable_weight_check(var):
    if var is not None:
        var = arg('variable_weight', var, dict)
        for k, value in var.items():
            if not isinstance(k, str):
                msg = ("The key of variable_weight must be a string!")
                logger.error(msg)
                raise TypeError(msg)
            if not isinstance(value, (float, int)):
                msg = ("The value of variable_weight must be a float!")
                logger.error(msg)
                raise TypeError(msg)
    return var

class UnifiedClustering(PALBase):#pylint: disable=too-many-instance-attributes
    """
    The Python wrapper for SAP HANA PAL Unified Clustering function.

    The clustering algorithms include:

    - 'AgglomerateHierarchicalClustering'
    - 'DBSCAN'
    - 'GaussianMixture'
    - 'AcceleratedKMeans'
    - 'KMeans'
    - 'KMedians'
    - 'KMedoids'
    - 'SOM'
    - 'AffinityPropagation'

    For GaussianMixture, you must configure ``init_mode`` and ``n_components`` or ``init_centers`` parameters to define INITIALIZE_PARAMETER in SAP HANA PAL.

    Compared to the original KMedians and KMedoids, UnifiedClustering creates models after a training and then performs cluster assignment through the model.


    Parameters
    ----------

    func : str

        The name of a specified clustering algorithm.

        The following algorithms are supported:

        - 'AgglomerateHierarchicalClustering'
        - 'DBSCAN'
        - 'GaussianMixture'
        - 'AcceleratedKMeans'
        - 'KMeans'
        - 'KMedians'
        - 'KMedoids'
        - 'SOM'
        - 'AffinityPropagation'

    massive : bool, optional
        Specifies whether or not to use massive mode of unified clustering.

        For parameter setting in massive mode, you could use both
        group_params (please see the example below) or the original parameters.
        Using original parameters will apply for all groups. However, if you define some parameters of a group,
        the value of all original parameter setting will be not applicable to such group.

        An example is as follows:

        .. raw:: html

            <iframe allowtransparency="true" style="border:1px solid #ccc; background: #eeffcb;"
                 src="../_static/uni_clustering_example.html" width="100%" height="100%">
            </iframe>

        In this example, as 'thread_ratio' is set in group_params for Group_1,
        parameter setting of 'metric' is not applicable to Group_1.

        Defaults to False.

    group_params : dict, optional
        If massive mode is activated (``massive`` is True), input data for clustering shall be divided into different
        groups with different clustering parameters applied. This parameter specifies the parameter
        values of the chosen clustering algorithm ``func`` w.r.t. different groups in a dict format,
        where keys corresponding to group_key while values should be a dict for clustering algorithm
        parameter value assignments.

        An example is as follows:

        .. only:: latex

            >>> uc = UnifiedClustering(func='dbscan',
                                       massive=True,
                                       metric='manhattan',
                                       group_params={'Group_1': {'thread_ratio':0.6}})

        .. raw:: html

            <iframe allowtransparency="true" style="border:1px solid #ccc; background: #eeffcb;"
                 src="../_static/uni_clustering_example.html" width="100%" height="100%">
            </iframe>

        Valid only when ``massive`` is True and defaults to None.

    **kwargs : keyword arguments

        Arbitrary keyword arguments and please referred to the responding algorithm for the parameters' key-value pair.

        .. Note::  **Some parameters are disabled in the clustering algorithm!**

          - **'AgglomerateHierarchicalClustering'** : :class:`~hana_ml.algorithms.pal.clustering.AgglomerateHierarchicalClustering`
            Note that ``distance_level`` is supported which has the same options as ``affinity``. If both parameters are entered, ``distance_level`` takes precedence over ``affinity``.

          - **'DBSCAN'** : :class:`~hana_ml.algorithms.pal.clustering.DBSCAN`
            Note that ``distance_level`` is supported which has the same options as ``metric``. If both parameters are entered, ``distance_level`` takes precedence over ``metric``.

          - **'GMM'** : :class:`~hana_ml.algorithms.pal.mixture.GaussianMixture`

          - **'AcceleratedKMeans'** : :class:`~hana_ml.algorithms.pal.clustering.KMeans`  Note that parameter ``accelerated`` is not valid in this function.

          - **'KMeans'** : :class:`~hana_ml.algorithms.pal.clustering.KMeans`

          - **'KMedians'** : :class:`~hana_ml.algorithms.pal.clustering.KMedians`

          - **'KMedoids'** : :class:`~hana_ml.algorithms.pal.clustering.KMedoids`

          - **'SOM'** : :class:`~hana_ml.algorithms.pal.som.SOM`

          - **'AffinityPropagation'** : :class:`~hana_ml.algorithms.pal.clustering.AffinityPropagation`

        For more parameter mappings of hana_ml and HANA PAL, please refer to the doc page: :ref:`param_mapping`

    Attributes
    ----------

    labels_ : DataFrame

        Label assigned to each sample. Also includes Distance between a given point and
        the cluster center (k-means), nearest core object (DBSCAN), weight vector (SOM)
        Or probability of a given point belonging to the corresponding cluster (GMM).

    centers_ : DataFrame

        Coordinates of cluster centers.

    model_ : DataFrame

        Model content.

    statistics_ : DataFrame

        Names and values of statistics.

    optimal_param_ : DataFrame

        Provides optimal parameters selected.

        Available only when parameter selection is triggered.


    Examples
    --------
    Training data for clustering:

    >>> data_tbl.collect()
        ID  V000 V001  V002
    0    0   0.5    A   0.5
    1    1   1.5    A   0.5
    2    2   1.5    A   1.5
    3    3   0.5    A   1.5
    4    4   1.1    B   1.2
    5    5   0.5    B  15.5
    6    6   1.5    B  15.5
    7    7   1.5    B  16.5
    8    8   0.5    B  16.5
    9    9   1.2    C  16.1
    10  10  15.5    C  15.5
    11  11  16.5    C  15.5
    12  12  16.5    C  16.5
    13  13  15.5    C  16.5
    14  14  15.6    D  16.2
    15  15  15.5    D   0.5
    16  16  16.5    D   0.5
    17  17  16.5    D   1.5
    18  18  15.5    D   1.5
    19  19  15.7    A   1.6

    Create a UnifiedClustering instance:

    >>> kmeans_params = dict(n_clusters=4, init='first_k', max_iter=100,
                             tol=1.0E-6, thread_ratio=1.0, distance_level='Euclidean',
                             category_weights=0.5)

    >>> ukmeans = UnifiedClustering(func = 'Kmeans', **kmeans_params)

    Fit the UnifiedClustering instance with the aforementioned training data:

    >>> ukmeans.fit(self.data_kmeans, key='ID')

    Check the resulting statistics on testing data:

    >>> ukmeans.label_.collect()
        ID  CLUSTER_ID  DISTANCE  SLIGHT_SILHOUETE
    0    0           0  0.891088          0.944370
    1    1           0  0.863917          0.942478
    2    2           0  0.806252          0.946288
    3    3           0  0.835684          0.944942
    ......
    16  16           1  0.976885          0.939386
    17  17           1  0.818178          0.945878
    18  18           1  0.722799          0.952170
    19  19           1  1.102342          0.925679

    Data for prediction(cluster assignment):

    >>> data_pred.collect()
       ID  CLUSTER_ID  DISTANCE
    0  88           3  0.981659
    1  89           3  0.826454
    2  90           2  1.990205
    3  91           2  0.325812

    Perform prediction:

    >>> result = ukmeans.predict(self.data_kmeans_predict, key='ID')
    >>> result.collect()
       ID  CLUSTER_ID  DISTANCE
    0  88           3  0.981659
    1  89           3  0.826454
    2  90           2  1.990205
    3  91           2  0.325812

    """

    func_dict = {
        'agglomeratehierarchicalclustering' : 'AHC',
        'dbscan' : 'DBSCAN',
        'gaussianmixture' : 'GMM',
        'acceleratedkmeans' : 'AKMEANS',
        'kmeans' : 'KMEANS',
        'kmedians' : 'KMEDIANS',
        'kmedoids' : 'KMEDOIDS',
        'som' : 'SOM',
        'affinitypropagation' : 'AP'}

    map_dict = {
        'AHC' : {
            'n_clusters' : ('N_CLUSTERS', int),
            'affinity' : ('AFFINITY', int, {'manhattan' : 1, 'euclidean' : 2, 'minkowski' : 3, 'chebyshev' : 4,
                                            'cosine' : 6, 'pearson correlation' : 7, 'squared euclidean' : 8,
                                            'jaccard' : 9, 'gower' : 10, 'precomputed' : 11}),
            'distance_level' : ('DISTANCE_LEVEL', int, {'manhattan' : 1, 'euclidean' : 2, 'minkowski' : 3, 'chebyshev' : 4,
                                                        'cosine' : 6, 'pearson correlation' : 7, 'squared euclidean' : 8,
                                                        'jaccard' : 9, 'gower' : 10, 'precomputed' : 11}),
            'linkage' : ('LINKAGE', int, {'nearest neighbor' : 1, 'furthest neighbor' : 2, 'group average' : 3, 'weighted average' : 4,
                                          'centroid clustering' : 5, 'median clustering' : 6, 'ward' : 7}),
            'thread_ratio' : ('THREAD_RATIO', float),
            'distance_dimension' : ('DISTANCE_DIMENSION', float),
            'normalization' : ('NORMALIZATION', int, {'no' : 0, 'z-score' : 1, 'zero-centred-min-max' : 2, 'min-max' : 3}),
            'category_weights' : ('CATEGORY_WEIGHTS', float)},
        'DBSCAN' : {
            'minpts' : ('MINPTS', int),
            'eps' : ('EPS', float),
            'thread_ratio' : ('THREAD_RATIO', float),
            'metric' : ('METRIC', int, {'manhattan' : 1, 'euclidean' : 2, 'minkowski' : 3, 'chebyshev' : 4,
                                        'standardized_euclidean' : 5, 'cosine' : 6}),
            'distance_level' : ('DISTANCE_LEVEL', int, {'manhattan' : 1, 'euclidean' : 2, 'minkowski' : 3, 'chebyshev' : 4,
                                                        'standardized_euclidean' : 5, 'cosine' : 6}),
            'minkowski_power' : ('MINKOWSKI_POWER', int),
            'category_weights' : ('CATEGORY_WEIGHTS', float),
            'algorithm' : ('ALGORITHM', int, {'brute-force' : 0, 'kd-tree' : 1}),
            'save_model' : ('SAVE_MODEL', bool)},
        'GMM' : {
            'init_param' : ('INIT_MODE', int, {'farthest_first_traversal' : 0, 'manual' : 1,
                                               'random_means' : 2, 'k_means++' : 3}),
            'n_components' : ('INITIALIZE_PARAMETER', int),
            'init_centers' : ('INITIALIZE_PARAMETER', ListOfStrings),
            'covariance_type' : ('COVARIANCE_TYPE', int, {'full' : 0, 'diag' : 1, 'tied_diag' : 2}),
            'shared_covariance' : ('SHARED_COVARIANCE', bool),
            'category_weight' : ('CATEGORY_WEIGHT', float),
            'max_iter' : ('MAX_ITER', int),
            'thread_ratio' : ('THREAD_RATIO', float),
            'error_tol' : ('ERROR_TOL', float),
            'regularization' : ('REGULARIZATION', float),
            'random_seed' : ('SEED', int)},
        'AKMEANS' : {
            'n_clusters' : ('N_CLUSTERS', int),
            'n_clusters_min' : ('N_CLUSTERS_MIN', int),
            'n_clusters_max' : ('N_CLUSTERS_MAX', int),
            'distance_level' : ('DISTANCE_LEVEL', int, {'manhattan' : 1, 'euclidean' : 2,
                                                        'minkowski' : 3, 'chebyshev' : 4}),
            'minkowski_power' : ('MINKOWSKI_POWER', float),
            'category_weights' : ('CATEGORY_WEIGHTS', float),
            'max_iter' : ('MAX_ITER', int),
            'init' : ('INIT', int, {'first_k' : 1, 'no_replace' : 2, 'replace' : 3, 'patent' : 4}),
            'normalization' : ('NORMALIZATION', int, {'no' : 0, 'l1_norm' : 1, 'min_max' : 2}),
            'thread_ratio' : ('THREAD_RATIO', float),
            'memory_mode' : ('MEMORY_MODE', int, {'auto' : 0, 'optimize-speed' : 1, 'optimize-space' : 2}),
            'use_fast_library': ('USE_FAST_LIBRARY', bool),
            'use_float': ('USE_FLOAT', bool)},
        'KMEANS' : {
            'n_clusters' : ('N_CLUSTERS', int),
            'n_clusters_min' : ('N_CLUSTERS_MIN', int),
            'n_clusters_max' : ('N_CLUSTERS_MAX', int),
            'distance_level' : ('DISTANCE_LEVEL', int, {'manhattan' : 1, 'euclidean' : 2,
                                                        'minkowski' : 3, 'chebyshev' : 4,
                                                        'cosine' : 6}),
            'minkowski_power' : ('MINKOWSKI_POWER', float),
            'category_weights' : ('CATEGORY_WEIGHTS', float),
            'max_iter' : ('MAX_ITER', int),
            'init' : ('INIT', int, {'first_k' : 1, 'replace' : 2, 'no_replace' : 3, 'patent' : 4}),
            'normalization' : ('NORMALIZATION', int, {'no' : 0, 'l1_norm' : 1, 'min_max' : 2}),
            'thread_ratio' : ('THREAD_RATIO', float),
            'tol' : ('TOL', float),
            'use_fast_library': ('USE_FAST_LIBRARY', bool),
            'use_float': ('USE_FLOAT', bool)},
        'KMEDIANS' : {
            'n_clusters' : ('N_CLUSTERS', int),
            'init' : ('INIT', int, {'first_k' : 1, 'replace' : 2, 'no_replace' : 3, 'patent' : 4}),
            'max_iter' : ('MAX_ITER', int),
            'tol' : ('TOL', float),
            'thread_ratio' : ('THREAD_RATIO', float),
            'distance_level' : ('DISTANCE_LEVEL', int, {'manhattan' : 1, 'euclidean' : 2,
                                                        'minkowski' : 3, 'chebyshev' : 4,
                                                        'cosine' : 6}),
            'minkowski_power' : ('MINKOWSKI_POWER', float),
            'category_weights' : ('CATEGORY_WEIGHTS', float),
            'normalization' : ('NORMALIZATION', int, {'no' : 0, 'l1_norm' : 1, 'min_max' : 2})},
        'KMEDOIDS' : {
            'n_clusters' : ('N_CLUSTERS', int),
            'init' : ('INIT', int, {'first_k' : 1, 'replace' : 2, 'no_replace' : 3, 'patent' : 4}),
            'max_iter' : ('MAX_ITER', int),
            'tol' : ('TOL', float),
            'thread_ratio' : ('THREAD_RATIO', float),
            'distance_level' : ('DISTANCE_LEVEL', int, {'manhattan' : 1, 'euclidean' : 2,
                                                        'minkowski' : 3, 'chebyshev' : 4,
                                                        'jaccard' : 5, 'cosine' : 6}),
            'minkowski_power' : ('MINKOWSKI_POWER', float),
            'category_weights' : ('CATEGORY_WEIGHTS', float),
            'normalization' : ('NORMALIZATION', int, {'no' : 0, 'l1_norm' : 1, 'min_max' : 2})},
        'SOM' : {
            'covergence_criterion' : ('COVERGENCE_CRITERION', float),
            'normalization' : ('NORMALIZATION', int, {'no' : 0, 'min-max' : 1, 'z-score' : 2}),
            'random_seed' : ('RANDOM_SEED', int),
            'height_of_map' : ('HEIGHT_OF_MAP', int),
            'width_of_map' : ('WIDTH_OF_MAP', int),
            'kernel_function' : ('KERNEL_FUNCTION', int, {'gaussian' : 1, 'flat' : 2}),
            'alpha' : ('ALPHA', float),
            'learning_rate' : ('LEARNING_RATE', int, {'exponential' : 1, 'linear' : 2}),
            'shape_of_grid' : ('SHAPE_OF_GRID', int, {'rectangle' : 1, 'hexagon' : 2}),
            'radius' : ('RADIUS', float),
            'batch_som' : ('BATCH_SOM', int, {'classical' : 0, 'batch' : 1}),
            'max_iter' : ('MAX_ITER', int)},
        'AP' : {
            'affinity' : ('DISTANCE_LEVEL', int, {'manhattan' : 1, 'euclidean' : 2, 'minkowski' : 3,
                                                  'chebyshev' : 4, 'standardized_euclidean' : 5, 'cosine' : 6}),
            'n_clusters' : ('CLUSTER_NUMBER', int),
            'max_iter' : ('MAX_ITER', int),
            'convergence_iter' : ('CON_ITERATION', int),
            'damping' : ('DAMP', float),
            'preference' : ('PREFERENCE', float),
            'seed_ratio' : ('SEED_RATIO', float),
            'times' : ('TIMES', int),
            'minkowski_power' : ('MINKOW_P', int),
            'thread_ratio' : ('THREAD_RATIO', float)
        }
    }

    def __init__(self,
                 func,
                 massive=False,
                 group_params=None,
                 **kwargs):
        setattr(self, 'hanaml_parameters', pal_param_register())
        super(UnifiedClustering, self).__init__()

        func = func.lower()
        self.func = self._arg('Function name', func, self.func_dict)

        self.params = dict(**kwargs)
        self.__pal_params = {}
        func_map = self.map_dict[self.func]

        # for massive mode
        self.massive = self._arg('massive', massive, bool)
        group_params = self._arg('group_params', group_params, dict)
        group_params = {} if group_params is None else group_params
        if group_params:
            for group in group_params:
                self._arg(f"{self.func} group_params of group '{str(group)}'",
                          group_params[group], dict)

        if self.massive is not True: # single mode
            self.__pal_params = _params_check(input_dict=self.params, param_map=func_map, func=self.func)

        else: # massive mode
            self.group_params = group_params
            if self.group_params:
                for group in self.group_params:
                    self.__pal_params[group] = {}
                    self.__pal_params[group] = _params_check(input_dict=self.group_params[group],
                                                             param_map=func_map,
                                                             func=self.func)

            special_group_name = 'PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID'
            self.__pal_params[special_group_name] = _params_check(input_dict=self.params,
                                                                  param_map=func_map,
                                                                  func=self.func)

        self.labels_ = None
        self.centers_ = None
        self.model_ = None
        self.statistics_ = None
        self.optimal_param_ = None
        self.error_msg_ = None

    def __map_param(self, name, value, typ):#pylint:disable=no-self-use
        tpl = ()
        if typ in [int, bool]:
            tpl = (name, value, None, None)
        elif typ == float:
            tpl = (name, None, value, None)
        elif typ in [str, ListOfStrings]:
            tpl = (name, None, None, value)
        elif isinstance(typ, dict):
            val = value
            if isinstance(val, (int, float)):
                tpl = (name, val, None, None)
            else:
                tpl = (name, None, None, val)
        return tpl

    @trace_sql
    def fit(self,
            data,
            key=None,
            features=None,
            group_key=None,
            group_params=None,
            categorical_variable=None,
            string_variable=None,
            variable_weight=None):
        """
        Fit function for unified clustering.

        Parameters
        ----------

        data : DataFrame
            Training data.

        key : str, optional

            Name of ID column.
            Defaults to the index column of data (i.e. data.index) if it is set.
            If the index of column of data is not provided, please enter the value of key.

        features : list of str, optional
            Names of the feature columns.

            If ``features`` is not provided, it defaults to all non-ID columns.

        group_key : str, optional
            The column of group_key. Data type can be INT or NVARCHAR/VARCHAR.
            If data type is INT, only parameters set in the group_params are valid.

            This parameter is only valid when massive mode is activated in class instance
            initialization(i.e. parameter ``massive`` is set as True).

            Defaults to the first column of data if the index columns of data is not provided.
            Otherwise, defaults to the first column of index columns.

        categorical_variable : str or list of str, optional
            Specifies INTEGER column(s) that should be treated as categorical.

            Other INTEGER columns will be treated as continuous.

            No default value.

        string_variable : str or list of str, optional
            Indicates a string column storing not categorical data.

            Levenshtein distance is used to calculate similarity between two strings.

            Ignored if it is not a string column. Only valid for DBSCAN.

            Defaults to None.

        variable_weight : dict, optional
            Specifies the weight of a variable participating in distance calculation.
            The value must be greater or equal to 0.

            Defaults to 1 for variables not specified. Only valid for DBSCAN.

            Defaults to None.

        group_params : dict, optional
            If massive mode is activated (``massive`` is set as True in class instance initialization),
            input data for clustering shall be divided into different
            groups with different clustering parameters applied. This parameter specifies the parameter
            values of the chosen clustering algorithm ``func`` w.r.t. different groups in a dict format,
            where keys corresponding to ``group_key`` while values should be a dict for clustering algorithm
            parameter value assignments.

            An example is as follows:

            .. only:: latex

                >>> uc = UnifiedClustering(func='dbscan',
                                           massive=True,
                                           metric='manhattan',
                                           group_params={'Group_1': {'thread_ratio':0.6}})
                >>> uc.fit(data=df,
                           key='ID',
                           features=['V1' ,'V2', 'V3'],
                           group_key="GROUP_ID",
                           group_params={'Group_1': {'categorical_variable':'V3'})

            .. raw:: html

                <iframe allowtransparency="true" style="border:1px solid #ccc; background: #eeffcb;"
                     src="../_static/uni_clustering_fit_example.html" width="100%" height="100%">
                 </iframe>

            Valid only when ``massive`` is set as True in class instance initialization.

            Defaults to None.

        Returns
        -------

        A fitted object.

        """
        setattr(self, 'hanaml_fit_params', pal_param_register())
        conn = data.connection_context
        require_pal_usable(conn)

        cols = data.columns
        index = data.index

        # if use precomputed in AHC, use the input data directly
        flag1 = all(x not in self.params for x in ['affinity', 'distance_level'])
        distance_func = None
        if not flag1:
            if 'affinity' in self.params:
                distance_func = self.params['affinity']
            else:
                distance_func = self.params['distance_level']
        if self.func != 'AHC' or flag1 or distance_func != 'precomputed':
            if self.massive is not True: # single mode
                key = self._arg('key', key, str)
                if index is not None:
                    key = _col_index_check(key, 'key', index, cols)
                else:
                    if key is None:
                        key = cols[0]
            elif not self._disable_hana_execution: # massive mode
                group_key = self._arg('group_key', group_key, str)
                if index is not None:
                    group_key = _col_index_check(group_key, 'group_key', index[0], cols)
                else:
                    if group_key is None:
                        group_key = cols[0]
                if group_key is not None and group_key not in cols:
                    msg = f"Please select group_key from {cols}!"
                    logger.error(msg)
                    raise ValueError(msg)
                data_groups = list(data[[group_key]].collect()[group_key].drop_duplicates())
                param_keys = list(self.group_params.keys())
                gid_type = data[[group_key]].dtypes()[0]
                if not all([(int(ky) if 'INT' in gid_type[1] else ky) in data_groups for ky in param_keys]):
                    msg = 'Invalid group key identified in group parameters!'
                    logger.error(msg)
                    raise ValueError(msg)
                if 'INT' in gid_type[1]:
                    group_key_type = gid_type[1]
                elif 'VARCHAR' in gid_type[1]:
                    group_key_type = gid_type[1] + '({})'.format(gid_type[2])
                cols.remove(group_key)

                key = self._arg('key', key, str)
                if index is not None:
                    key = _col_index_check(key, 'key', index[1], cols)
                else:
                    if key is None:
                        key = cols[0]
            else:
                gid_type = {x[0]:(x[1], x[2]) for x in data._dtypes}[group_key]#pylint:disable=protected-access
                group_key_type = gid_type[0] if 'INT' in gid_type[0] else gid_type[1] + '({})'.format(gid_type[2])
                data_groups = list(group_params.keys()) if group_params else []
            # for both modes
            if key is not None and key not in cols:
                msg = f"Please select key from {cols}!"
                logger.error(msg)
                raise ValueError(msg)
            cols.remove(key)

            features = _listofstring_check(features, 'features')
            if features is None:
                features = cols

            if self.massive is not True: # single mode
                data_ = data[[key] + features]
            else: # massive mode
                data_ = data[[group_key] + [key] + features]
        else:
            data_ = data # use the input data directly in precomputed in AHC

        if self.massive is not True: # single mode
            param_rows = [('FUNCTION', None, None, self.func)]
            for name in self.__pal_params:
                value, typ = self.__pal_params[name]
                if self.func == 'GMM' and name == 'INITIALIZE_PARAMETER' and isinstance(value, list):
                    param_rows.extend([('INITIALIZE_PARAMETER', None, None, str(var)) for var in value])
                else:
                    tpl = [self.__map_param(name, value, typ)]
                    param_rows.extend(tpl)

            categorical_variable = _listofstring_check(categorical_variable, 'categorical_variable')
            if categorical_variable is not None:
                param_rows.extend([('CATEGORICAL_VARIABLE', None, None, var) for var in categorical_variable])

            string_variable = _listofstring_check(string_variable, 'string_variable')
            if string_variable is not None:
                param_rows.extend(('STRING_VARIABLE', None, None, var) for var in string_variable)

            variable_weight = _variable_weight_check(variable_weight)
            if variable_weight is not None:
                param_rows.extend(('VARIABLE_WEIGHT', None, value, k) for k, value in variable_weight.items())

            unique_id = str(uuid.uuid1()).replace('-', '_').upper()
            outputs = ['RESULT', 'CENTERS', 'MODEL', 'STATS', 'OPT_PARAM', 'PLACE_HOLDER1', 'PLACE_HOLDER2']
            outputs = ['#PAL_UNIFIED_CLUSTERING_{}_{}_{}'.format(tbl, self.id, unique_id)
                       for tbl in outputs]
            labels_tbl, centers_tbl, model_tbl, stats_tbl, opt_param_tbl, _, _ = outputs
            try:
                self._call_pal_auto(conn,
                                    'PAL_UNIFIED_CLUSTERING',
                                    data_,
                                    ParameterTable().with_data(param_rows),
                                    *outputs)
            except dbapi.Error as db_err:
                logger.error(str(db_err))
                try_drop(conn, outputs)
                raise
            except pyodbc.Error as db_err:
                logger.error(str(db_err.args[1]))
                try_drop(conn, outputs)
                raise
        else: # massive mode
            special_group_name = 'PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID'
            if 'INT' in group_key_type and self.params:
                warn_msg = "If the type of group_key is INTEGER, only parameters in group_params are valid!"
                warnings.warn(message=warn_msg)
            param_rows = [(None, 'FUNCTION', None, None, self.func)] # only need assign once

            # Temp code
            if 'INT' in group_key_type:
                for each in data_groups:
                    each_val = int(each)
                    param_rows.extend([(each_val, 'FUNCTION', None, None, self.func)])
            else:
                param_rows.extend([('PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID', 'FUNCTION', None, None, self.func)])

            # special key categorical_variable/string_variable/variable_weight
            if 'INT' not in group_key_type:
                categorical_variable = _listofstring_check(categorical_variable, 'categorical_variable')
                if categorical_variable is not None:
                    param_rows.extend([(special_group_name, 'CATEGORICAL_VARIABLE', None, None, var)
                                       for var in categorical_variable])

                string_variable = _listofstring_check(string_variable, 'string_variable')
                if string_variable is not None:
                    param_rows.extend((special_group_name, 'STRING_VARIABLE', None, None, var)
                                      for var in string_variable)

                variable_weight = _variable_weight_check(variable_weight)
                if variable_weight is not None:
                    param_rows.extend((special_group_name, 'VARIABLE_WEIGHT', None, value, k)
                                      for k, value in variable_weight.items())

            for group in self.__pal_params:
                is_special_group = False
                if group in ['PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID']:
                    group_val = 'PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID'
                    is_special_group = True
                else:
                    group_val = int(group) if 'INT' in group_key_type else group
                if 'INT' in group_key_type and is_special_group is True:
                    continue
                for name in self.__pal_params[group]:
                    value, typ = self.__pal_params[group][name]
                    if self.func == 'GMM' and name == 'INITIALIZE_PARAMETER' and isinstance(value, list):
                        param_rows.extend([(group_val, 'INITIALIZE_PARAMETER', None, None, str(var)) for var in value])
                    else:
                        tpl = [tuple([group_val] + list(self.__map_param(name, value, typ)))]
                        param_rows.extend(tpl)

            # for each group
            if group_params:
                for group in group_params:
                    if group in ['PAL_MASSIVE_PROCESSING_SPECIAL_GROUP_ID']:
                        continue
                    group_val = int(group) if 'INT' in group_key_type else group

                    # group categorical_variable/string_variable/variable_weight when group_key_type is not INT
                    group_categorical_variable = None
                    if group_params[group].get('categorical_variable') is not None:
                        group_categorical_variable = group_params[group]['categorical_variable']
                    group_categorical_variable = _listofstring_check(group_categorical_variable, f'categorical_variable in group {group}')
                    if group_categorical_variable:
                        param_rows.extend([(group_val, 'CATEGORICAL_VARIABLE', None, None, var) for var in group_categorical_variable])

                    group_string_variable = None
                    if group_params[group].get('string_variable') is not None:
                        group_string_variable = group_params[group]['string_variable']
                    group_string_variable = _listofstring_check(group_string_variable, f'string_variable in in group {group}')
                    if group_string_variable is not None:
                        param_rows.extend((group_val, 'STRING_VARIABLE', None, None, var)
                                          for var in group_string_variable)

                    group_variable_weight = None
                    if group_params[group].get('variable_weight') is not None:
                        group_variable_weight = group_params[group]['variable_weight']
                    group_variable_weight = _variable_weight_check(group_variable_weight)
                    if group_variable_weight is not None:
                        param_rows.extend((group_val, 'VARIABLE_WEIGHT', None, value, k)
                                          for k, value in group_variable_weight.items())

            unique_id = str(uuid.uuid1()).replace('-', '_').upper()
            outputs = ['RESULT', 'CENTERS', 'MODEL', 'STATS', 'OPT_PARAM', 'ERRORMSG', 'PLACE_HOLDER1', 'PLACE_HOLDER2']
            outputs = ['#PAL_UNIFIED_CLUSTERING_{}_{}_{}'.format(tbl, self.id, unique_id)
                       for tbl in outputs]
            labels_tbl, centers_tbl, model_tbl, stats_tbl, opt_param_tbl, errormsg_tbl, _, _ = outputs
            pal_func_exist = True
            if not self._disable_hana_execution:
                pal_func_exist = check_pal_function_exist(conn, '%UNIFIED_MASSIVE%', like=True)
            if pal_func_exist:
                try:
                    self._call_pal_auto(conn,
                                        'PAL_UNIFIED_MASSIVE_CLUSTERING',
                                        data_,
                                        ParameterTable(itype=group_key_type).with_data(param_rows),
                                        *outputs)

                except dbapi.Error as db_err:
                    logger.error(str(db_err))
                    try_drop(conn, outputs)
                    raise
                except pyodbc.Error as db_err:
                    logger.error(str(db_err.args[1]))
                    try_drop(conn, outputs)
                    raise
            else:
                msg = 'The version of your SAP HANA does not support unified massive clustering!'
                logger.error(msg)
                raise ValueError(msg)
        #pylint: disable=attribute-defined-outside-init
        if not self._disable_hana_execution:
            self.labels_ = conn.table(labels_tbl)
            self.centers_ = conn.table(centers_tbl)
            self.model_ = conn.table(model_tbl)
            self.statistics_ = conn.table(stats_tbl)
            self.optimal_param_ = conn.table(opt_param_tbl)
            if self.massive is True:
                self.error_msg_ = conn.table(errormsg_tbl)
                if not self._disable_hana_execution:
                    if not self.error_msg_.collect().empty:
                        row = self.error_msg_.count()
                        for i in range(1, row+1):
                            warn_msg = "For group_key '{}',".format(self.error_msg_.collect()[group_key][i-1]) +\
                                       " the error message is '{}'.".format(self.error_msg_.collect()['MESSAGE'][i-1]) +\
                                       "More information could be seen in the attribute error_msg_!"
                            warnings.warn(message=warn_msg)
        return self

    @trace_sql
    def predict(self, data, key=None, group_key=None, features=None, model=None):
        r"""
        Predict with the clustering model.

        Cluster assignment is a unified interface to call a cluster assignment algorithm
        to assign data to clusters that are previously generated by some clustering methods,
        including K-Means, Accelerated K-Means, K-Medians, K- Medoids, DBSCAN, SOM, and GMM.

        AgglomerateHierarchicalClustering does not provide predict function!

        Parameters
        ----------
        data :  DataFrame
            Data to be predicted.

        key : str, optional

            Name of ID column.
            Defaults to the index column of data (i.e. data.index) if it is set.
            If the index of column of data is not provided, please enter the value of key.

        group_key : str, optional
            The column of group_key. Data type can be INT or NVARCHAR/VARCHAR.
            If data type is INT, only parameters specified in the ``group_params``
            in class instance initialization are valid.

            This parameter is only valid when massive mode is activated(i.e. ``massive``
            is set as True in class instance initialization).

            Defaults to the first column of data if the index columns of data is not provided.
            Otherwise, defaults to the first column of index columns.

        features : ListOfStrings, optional
            Names of feature columns in data for prediction.

            Defaults all non-ID columns in ``data`` if not provided.

        model : DataFrame
            Fitted clustering model.

            Defaults to self.model\_.

        Returns
        -------
        DataFrame
            Cluster assignment result, structured as follows:

            1st column : Data ID

            2nd column : Assigned cluster ID

            3rd column : Distance metric between a given point and the assigned cluster.
            For different functions, this could be:

                - Distance between a given point and the cluster center(k-means, k-medians, k-medoids)
                - Distance between a given point and the nearest core object(DBSCAN)
                - Distance between a given point and the weight vector(SOM)
                - Probability of a given point belonging to the corresponding cluster(GMM)

        """

        if self.func == 'AHC':
            err_msg = "AgglomerateHierarchicalClustering does not provide predict function!"
            logger.error(err_msg)
            raise ValueError(err_msg)
        if model is None and getattr(self, 'model_') is None:
            msg = "Model not initialized. Perform a fit first."
            logger.error(msg)
            raise FitIncompleteError(msg)
        conn = data.connection_context

        if model is None:
            model = self.model_

        cols = data.columns
        index = data.index
        if not self._disable_hana_execution:
            if self.massive is not True: # single mode
                key = self._arg('key', key, str)
                if index is not None:
                    key = _col_index_check(key, 'key', index, cols)
                else:
                    if key is None:
                        key = cols[0]
            else: # massive mode
                group_key = self._arg('group_key', group_key, str)
                if index is not None:
                    group_key = _col_index_check(group_key, 'group_key', index[0], cols)
                else:
                    if group_key is None:
                        group_key = cols[0]
                gid_type = data[[group_key]].dtypes()[0]
                if 'INT' in gid_type[1]:
                    group_key_type = gid_type[1]
                elif 'VARCHAR' in gid_type[1]:
                    group_key_type = gid_type[1] + '({})'.format(gid_type[2])

                if group_key is not None and group_key not in cols:
                    msg = f"Please select group_key from {cols}!"
                    logger.error(msg)
                    raise ValueError(msg)
                cols.remove(group_key)

                key = self._arg('key', key, str)
                if index is not None:
                    key = _col_index_check(key, 'key', index[1], cols)
                else:
                    if key is None:
                        key = cols[0]
            # for both modes
            if key is not None and key not in cols:
                msg = f"Please select key from {cols}!"
                logger.error(msg)
                raise ValueError(msg)
            cols.remove(key)

            features = _listofstring_check(features, 'features')
            if features is None:
                features = cols
            data_ = data[[group_key] + [key] + features] if self.massive else data[[key] + features]
        else:
            data_ = data
            gid_type = {x[0]:(x[1], x[2]) for x in data._dtypes}[group_key]#pylint:disable=protected-access
            group_key_type = gid_type[0] if 'INT' in gid_type[0] else gid_type[1] + '({})'.format(gid_type[2])
        if self.massive is not True: # single mode
            unique_id = str(uuid.uuid1()).replace('-', '_').upper()
            outputs = ['ASSIGNMENT', 'PLACE_HOLDER1']
            outputs = ['#PAL_UNIFIED_CLUSTERING_PREDICT_{}_{}_{}'.format(tbl, self.id, unique_id)
                       for tbl in outputs]
            assignment_tbl, _ = outputs

            try:
                self._call_pal_auto(conn,
                                    'PAL_UNIFIED_CLUSTERING_ASSIGNMENT',
                                    data_,
                                    model,
                                    ParameterTable(),
                                    *outputs)
            except dbapi.Error as db_err:
                logger.exception(str(db_err))
                try_drop(conn, outputs)
                raise
            except pyodbc.Error as db_err:
                logger.exception(str(db_err.args[1]))
                try_drop(conn, outputs)
                raise
            return conn.table(assignment_tbl)

        # massive mode
        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        outputs = ['ASSIGNMENT', 'ERRORMSG', 'PLACE_HOLDER1']
        outputs = [f'#PAL_UNIFIED_CLUSTERING_PREDICT_{tbl}_TBL_{self.id}_{unique_id}'
                  for tbl in outputs]
        assignment_tbl, errormsg_tbl, _ = outputs
        if "INT" in group_key_type:
            param_rows = [(555, 'THREAD_RATIO', None, 1, None)]
        else:
            param_rows = [('GROUP', 'THREAD_RATIO', None, 1, None)]
        pal_func_exist = True
        if not self._disable_hana_execution:
            pal_func_exist = check_pal_function_exist(conn, '%UNIFIED_MASSIVE%', like=True)
        if pal_func_exist:
            try:
                self._call_pal_auto(conn,
                                    'PAL_UNIFIED_MASSIVE_CLUSTERING_ASSIGNMENT',
                                    data_,
                                    model,
                                    ParameterTable(itype=group_key_type).with_data(param_rows),
                                    *outputs)
            except dbapi.Error as db_err:
                logger.exception(str(db_err))
                try_drop(conn, outputs)
                raise
            except pyodbc.Error as db_err:
                logger.exception(str(db_err.args[1]))
                try_drop(conn, outputs)
                raise
        else:
            msg = 'The version of your SAP HANA does not support unified massive clustering!'
            logger.error(msg)
            raise ValueError(msg)

        error_msg = conn.table(errormsg_tbl)
        if not self._disable_hana_execution:
            if not error_msg.collect().empty:
                row = error_msg.count()
                for i in range(1, row+1):
                    warn_msg = f"For group_key '{self.error_msg_.collect()[group_key][i-1]}'," +\
                               " the error message is '{self.error_msg_.collect()['MESSAGE'][i-1]}'." +\
                               "More information could be seen in the attribute error_msg_!"
                    warnings.warn(message=warn_msg)

        return conn.table(assignment_tbl), error_msg
