"""
This module is to build report for PAL/APL models.

The following class is available:

    * :class:`UnifiedReport`
"""
#pylint: disable=line-too-long
#pylint: disable=consider-using-f-string
import logging
from deprecated import deprecated
import matplotlib
from hana_ml.algorithms.pal.auto_ml import _AutoMLBase
from hana_ml.dataframe import DataFrame
from hana_ml.ml_exceptions import FitIncompleteError
from hana_ml.visualizers.automl_report import BestPipelineReport
from hana_ml.visualizers.dataset_report import DatasetReportBuilder
from hana_ml.visualizers.model_debriefing import TreeModelDebriefing
from hana_ml.visualizers.model_report import _UnifiedClassificationReportBuilder, _UnifiedRegressionReportBuilder
from hana_ml.algorithms.pal.preprocessing import Sampling
from hana_ml.algorithms.pal.utility import version_compare

logger = logging.getLogger(__name__) #pylint: disable=invalid-name

class UnifiedReport(object):
    """
    The report generator for PAL/APL models. Currently, it only supports UnifiedClassification and UnifiedRegression.

    Examples
    --------
    Data used is called diabetes_train.

    Case 1: UnifiedReport for UnifiedClassification is shown as follows, please set build_report=True in the fit() function:

    >>> from hana_ml.algorithms.pal.model_selection import GridSearchCV
    >>> from hana_ml.algorithms.pal.model_selection import RandomSearchCV
    >>> hgc = UnifiedClassification('HybridGradientBoostingTree')
    >>> gscv = GridSearchCV(estimator=hgc,
                            param_grid={'learning_rate': [0.1, 0.4, 0.7, 1],
                                        'n_estimators': [4, 6, 8, 10],
                                        'split_threshold': [0.1, 0.4, 0.7, 1]},
                            train_control=dict(fold_num=5,
                                               resampling_method='cv',
                                               random_state=1,
                                               ref_metric=['auc']),
                            scoring='error_rate')
    >>> gscv.fit(data=diabetes_train, key= 'ID',
                 label='CLASS',
                 partition_method='stratified',
                 partition_random_state=1,
                 stratified_column='CLASS',
                 build_report=True)

    To look at the dataset report:

    >>> UnifiedReport(diabetes_train).build().display()

     .. image:: image/unified_report_dataset_report.png

    To see the model report:

    >>> UnifiedReport(gscv.estimator).display()

     .. image:: image/unified_report_model_report_classification.png

    We could also see the Optimal Parameter page:

     .. image:: image/unified_report_model_report_classification2.png

    Case 2: UnifiedReport for UnifiedRegression is shown as follows, please set build_report=True in the fit() function:

    >>> hgr = UnifiedRegression(func = 'HybridGradientBoostingTree')
    >>> gscv = GridSearchCV(estimator=hgr,
                            param_grid={'learning_rate': [0.1, 0.4, 0.7, 1],
                                        'n_estimators': [4, 6, 8, 10],
                                        'split_threshold': [0.1, 0.4, 0.7, 1]},
                            train_control=dict(fold_num=5,
                                               resampling_method='cv',
                                               random_state=1),
                            scoring='rmse')
    >>> gscv.fit(data=diabetes_train, key= 'ID',
                 label='CLASS',
                 partition_method='random',
                 partition_random_state=1,
                 build_report=True)

    To see the model report:

    >>> UnifiedReport(gscv.estimator).display()

     .. image:: image/unified_report_model_report_regression.png

    """
    def __init__(self, obj):
        self.obj = obj
        self.dataset_report = None

    def build(self, key=None, scatter_matrix_sampling: Sampling = None,
              ignore_scatter_matrix: bool = False, ignore_correlation: bool = False, subset_bins = None):
        """
        Build the report.

        Parameters
        ----------
        key : str, valid only for DataFrame
            Name of ID column.

            Defaults to the first column.
        scatter_matrix_sampling : :class:`~hana_ml.algorithms.pal.preprocessing.Sampling`, valid only for DataFrame
            Scatter matrix sampling.
        ignore_scatter_matrix : bool, optional
            Ignore the plotting of scatter matrix if True.

            Defaults to False.
        ignore_correlation : bool, optional
            Ignore the correlation computation if True.

            Defaults to False.
        subset_bins : dict, optional
            Define the bin number in distribution chart for each column, e.g. {"col_A": 20}.

            Defaults to 20 for all.
        """
        if not version_compare(matplotlib.__version__, "3.4.0"):
            logger.warning("The version of matplotlib is lower than 3.4.0. The report build may run in error.")
        if isinstance(self.obj, _UnifiedClassificationReportBuilder):
            self._unified_classification_build()
        elif isinstance(self.obj, _UnifiedRegressionReportBuilder):
            self._unified_regression_build()
        elif isinstance(self.obj, DataFrame):
            if key is None:
                key = self.obj.columns[0]
                logger.warning("key has not been set. The first column has been treaded as the index column.")
            self._dataset_report_build(key, scatter_matrix_sampling, ignore_scatter_matrix, ignore_correlation, subset_bins)
        elif isinstance(self.obj, _AutoMLBase):
            pass
        else:
            raise NotImplementedError
        return self

    @deprecated("This method is deprecated. AUC points can be controled by the parameter `ntiles`.")
    def set_metric_samplings(self, roc_sampling: Sampling = None, other_samplings: dict = None):
        """
        Set metric samplings to report builder.

        Parameters
        ----------
        roc_sampling : :class:`~hana_ml.algorithms.pal.preprocessing.Sampling`, optional
            ROC sampling.

        other_samplings : dict, optional
            Key is column name of metric table.

                - CUMGAINS
                - RANDOM_CUMGAINS
                - PERF_CUMGAINS
                - LIFT
                - RANDOM_LIFT
                - PERF_LIFT
                - CUMLIFT
                - RANDOM_CUMLIFT
                - PERF_CUMLIFT

            Value is sampling.

        Examples
        --------
        Creating the metric samplings:

        >>> roc_sampling = Sampling(method='every_nth', interval=2)

        >>> other_samplings = dict(CUMGAINS=Sampling(method='every_nth', interval=2),
                              LIFT=Sampling(method='every_nth', interval=2),
                              CUMLIFT=Sampling(method='every_nth', interval=2))
        >>> unified_report.set_metric_samplings(roc_sampling, other_samplings)
        """
        self.obj.roc_sampling = roc_sampling
        self.obj.other_samplings = other_samplings

        return self

    def tree_debrief(self, save_html=None, digraph=True, **kwargs):
        """
        Visualize tree model.

        Parameters
        ----------
        save_html : str, optional
            If it is not None, the function will generate a html report and stored in the given name.

            Defaults to None.

        digraph : bool, optional
            If True, it will output the digraph tree structure.

            Defaults to False.
        """
        model = self.obj.model_[0] if isinstance(self.obj.model_, (list, tuple)) else self.obj.model_
        if not digraph:
            if save_html:
                TreeModelDebriefing.tree_export(model, filename=save_html, **kwargs)
            else:
                TreeModelDebriefing.tree_debrief(model, **kwargs)
        else:
            if save_html:
                TreeModelDebriefing.tree_export_with_dot(model, filename=save_html, **kwargs)
            else:
                TreeModelDebriefing.tree_debrief_with_dot(model, **kwargs)

    def display(self, save_html=None, metric_sampling=False):
        """
        Display the report.

        Parameters
        ----------
        save_html : str, optional
            If it is not None, the function will generate a html report and stored in the given name.

            Defaults to None.
        metric_sampling : bool, optional (deprecated)
            Whether the metric table needs to be sampled. It is only valid for UnifiedClassification and used together with set_metric_samplings.
            Since version 2.14, the metric_sampling is no need to specify.

            Defaults to False.
        """
        if isinstance(self.obj, _UnifiedClassificationReportBuilder):
            if hasattr(self.obj, 'auto_metric_sampling'):
                if self.obj.auto_metric_sampling:
                    metric_sampling = True
            self._unified_classification_display(save_html=save_html, metric_sampling=metric_sampling)
        elif isinstance(self.obj, _UnifiedRegressionReportBuilder):
            self._unified_regression_display(save_html)
        elif isinstance(self.obj, DataFrame):
            self._dataset_report_display(save_html)
        elif isinstance(self.obj, _AutoMLBase):
            self._pipeline_report_display(save_html)
        else:
            raise NotImplementedError

    def _dataset_report_build(self, key, scatter_matrix_sampling, ignore_scatter_matrix, ignore_correlation, subset_bins):
        self.dataset_report = DatasetReportBuilder()
        self.dataset_report.build(self.obj, key, scatter_matrix_sampling, ignore_scatter_matrix, ignore_correlation, subset_bins)

    def _unified_classification_build(self):
        self.obj.build_report()

    def _unified_regression_build(self):
        self.obj.build_report()

    def _dataset_report_display(self, save_html):
        if save_html is None:
            self.dataset_report.generate_notebook_iframe_report()
        else:
            self.dataset_report.generate_html_report(save_html)

    def _unified_classification_display(self, save_html, metric_sampling):
        if save_html is None:
            self.obj.generate_notebook_iframe_report(metric_sampling=metric_sampling)
        else:
            self.obj.generate_html_report(filename=save_html, metric_sampling=metric_sampling)

    def _unified_regression_display(self, save_html):
        if save_html is None:
            self.obj.generate_notebook_iframe_report()
        else:
            self.obj.generate_html_report(save_html)

    def _pipeline_report_display(self, save_html):
        if save_html is None:
            BestPipelineReport(self.obj).generate_notebook_iframe()
        else:
            BestPipelineReport(self.obj).generate_html(filename=save_html)

    def get_iframe_report(self):
        """
        Return iframe report without display.
        """
        if isinstance(self.obj, DataFrame):
            if self.dataset_report is None:
                raise FitIncompleteError("Unified report has not been built.")
            return self.dataset_report.get_iframe_report_html()
        else:
            return self.obj.report
