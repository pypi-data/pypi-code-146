"""
This module represents the whole time series report.
A report can contain many pages, and each page can contain many items.
You can use the class 'DatasetAnalysis' to generate all the items and combine them into different pages at will.

The following classes are available:
    * :class:`TimeSeriesReport`
    * :class:`DatasetAnalysis`
"""

# pylint: disable=invalid-name
# pylint: disable=bad-continuation
# pylint: disable=invalid-name
# pylint: disable=no-else-continue
import uuid
import numpy as np
from hana_ml.algorithms.pal.tsa import correlation_function, seasonal_decompose, stationarity_test
from hana_ml.algorithms.pal.tsa.outlier_detection import OutlierDetectionTS
from hana_ml.visualizers.report_builder import ChartItem, ReportBuilder, TableItem
from hana_ml.algorithms.pal.tsa.changepoint import BCPD


class TimeSeriesReport(ReportBuilder):
    """
    This class is the builder of time series report.

    Parameters
    ----------
    title : str
        The name of time series report.

    Examples
    --------
    0. Importing classes

    >>> from hana_ml.visualizers.time_series_report import TimeSeriesReport, DatasetAnalysis
    >>> from hana_ml.visualizers.report_builder import Page

    1. Creating a report instance:

    >>> report = TimeSeriesReport('Time Series Data Report')

    2. Create a data analysis instance and a page array:

    >>> dataset_analysis = DatasetAnalysis(data=df_acf, endog="Y", key="ID")
    >>> pages = []

    3. Construct the contents of each page of the report:

    >>> page0 = Page('Stationarity')
    >>> page0.addItem(dataset_analysis.stationarity_item())
    >>> pages.append(page0)

    >>> page1 = Page('Partial Autocorrelation')
    >>> page1.addItem(dataset_analysis.pacf_item())
    >>> pages.append(page1)

    >>> page2 = Page('Rolling Mean and Standard Deviation')
    >>> page2.addItems([dataset_analysis.moving_average_item(-3), dataset_analysis.rolling_stddev_item(10)])
    >>> pages.append(page2)

    >>> page3 = Page('Real and Seasonal')
    >>> page3.addItem(dataset_analysis.real_item())
    >>> page3.addItem(dataset_analysis.seasonal_item())
    >>> page3.addItems(dataset_analysis.seasonal_decompose_items())
    >>> pages.append(page3)

    >>> page4 = Page('Box')
    >>> page4.addItem(dataset_analysis.timeseries_box_item('YEAR'))
    >>> page4.addItem(dataset_analysis.timeseries_box_item('MONTH'))
    >>> page4.addItem(dataset_analysis.timeseries_box_item('QUARTER'))
    >>> pages.append(page4)

    >>> page5 = Page('Quarter')
    >>> page5.addItem(dataset_analysis.quarter_item())
    >>> pages.append(page5)

    >>> page6 = Page('Outlier')
    >>> page6.addItem(dataset_analysis.outlier_item())
    >>> pages.append(page6)

    >>> page7 = Page('Change Points')
    >>> bcpd = BCPD(max_tcp=2, max_scp=1, max_harmonic_order =10, random_seed=1, max_iter=10000)
    >>> page7.addItem(dataset_analysis.change_points_item(bcpd))
    >>> pages.append(page7)

    4. Add all pages to report instance:

    >>> report.addPages(pages)

    5. Generating notebook iframe:

    >>> report.build()
    >>> report.generate_notebook_iframe()

    6. Generating a local HTML file:

    >>> report.generate_html("TimeSeriesReport")

    An example of time series data report is below:

    .. image:: image/ts_data_report.png

    """
    # def __init__(self, title):
    #     super(TimeSeriesReport, self).__init__(title)


class DatasetAnalysis(object):
    """
    This class will generate all items of dataset analysis result.

    Parameters
    ----------

    data : DataFrame
        Input data.

    endog : str
        Name of the dependent variable.

    key : str, optional
        Name of the ID column.

        Defaults to the index column of ``data`` (i.e. data.index) if it is set.
    """
    def __init__(self, data, endog, key=None):
        if data is None or data.empty():
            raise ValueError("Dataset is empty.")
        if key is None:
            if data.index:
                key = data.index
            else:
                raise ValueError("Index should be set by key or use set_index function!")
        else:
            data.set_index(key)
        if endog is None:
            raise ValueError("Endog should be set by endog!")

        self.dataset = data
        self.columns = data.columns
        self.key = key
        self.endog = endog
        self.features = data.columns
        self.features.remove(key)
        self.features.remove(endog)
        # default: auto render chart
        self.lazy_load = False
        # 10W
        if self.dataset.count() >= 100000:
            # manual load
            self.lazy_load = True

    def pacf_item(self, thread_ratio=None, method=None, max_lag=None, calculate_confint=True, alpha=None, bartlett=None):
        """
        It will plot PACF for two time series data.

        Parameters
        ----------

        col : str
            Name of the time series data column.

        thread_ratio : float, optional

            The ratio of available threads.

            - 0: single thread
            - 0~1: percentage
            - Others: heuristically determined

            Valid only when ``method`` is set as 'brute_force'.

            Defaults to -1.

        method : {'auto', 'brute_force', 'fft'}, optional
            Indicates the method to be used to calculate the correlation function.

            Defaults to 'auto'.

        max_lag : int, optional
            Maximum lag for the correlation function.

        calculate_confint : bool, optional
            Controls whether to calculate confidence intervals or not.

            If it is True, two additional columns of confidence intervals are shown in the result.

            Defaults to True.

        alpha : float, optional
            Confidence bound for the given level are returned. For instance if alpha=0.05, 95 % confidence bound is returned.

            Valid only when only ``calculate_confint`` is True.

            Defaults to 0.05.

        bartlett : bool, optional

            - False: using standard error to calculate the confidence bound.
            - True: using Bartlett's formula to calculate confidence bound.

            Valid only when only ``calculate_confint`` is True.

            Defaults to True.

        Returns
        -------
        item : ChartItem
            The item for the plot.
        """
        col = self.endog
        res = correlation_function.correlation(data=self.dataset, key=self.key, x=col, thread_ratio=thread_ratio, method=method, max_lag=max_lag, calculate_pacf=True, calculate_confint=calculate_confint, alpha=alpha, bartlett=bartlett)
        fetch_xy = res.select(["LAG", "PACF"]).sort_values("LAG").collect()

        confidence_x = []
        confidence_l = []
        confidence_u = []
        if calculate_confint is True:
            fetch_confint = res.select(["LAG", "PACF_CONFIDENCE_BOUND"]).sort_values("LAG").collect()
            lower_bound = np.negative(fetch_confint["PACF_CONFIDENCE_BOUND"].to_numpy())
            upper_bound = fetch_confint["PACF_CONFIDENCE_BOUND"].to_numpy()

            x = list(fetch_confint["LAG"].to_numpy())
            lower_bound_y = list(lower_bound)
            upper_bound_y = list(upper_bound)
            for i in range(0, len(lower_bound_y)):
                if bool(np.isnan(lower_bound_y[i])) is False:
                    confidence_x.append(x[i])
                    confidence_l.append(lower_bound_y[i])
                    confidence_u.append(upper_bound_y[i])
            confidence_x.insert(0, 'ConfidenceX')
            confidence_l.insert(0, 'ConfidenceL')
            confidence_u.insert(0, 'ConfidenceU')

        X = list(fetch_xy["LAG"])
        X.insert(0, 'LAG')
        Y = list(fetch_xy["PACF"])
        Y.insert(0, 'PACF')

        option = {
            'customFalseFlag': ['xAxis.axisTick.show'],
            'dataset': [
                {
                    'source': [
                        X,
                        Y,
                        Y
                    ]
                },
                {
                    'source': [
                        confidence_x,
                        confidence_l,
                        confidence_u
                    ]
                }
            ],
            'grid': {
                'show': 'true',
                'containLabel': 'true'
            },
            'xAxis': {
                'type': 'category',
                'name': 'LAG',
                'axisTick': {
                    'alignWithLabel': 'true',
                    'show': 'false'
                }
            },
            'yAxis': {
                'type': 'value',
                'name': 'PACF',
                'axisLine': {
                    'show': 'true',
                },
                'axisTick': {
                    'show': 'true'
                }
            },
            'tooltip': {},
            'series': [
                {
                    'type': 'scatter',
                    'seriesLayoutBy': 'row',
                    'color': '#5698C6',
                    'symbolSize': 5
                },
                {
                    'type': 'bar',
                    'seriesLayoutBy': 'row',
                    'color': '#5698C6',
                    'barWidth': 1
                },
                {
                    'type': 'line',
                    'datasetIndex': 1,
                    'seriesLayoutBy': 'row',
                    'symbol': 'none',
                    'smooth': 'true',
                    'color': '#C00000',
                    'lineStyle': {
                        'opacity': 0
                    },
                    'areaStyle': {
                        'color': '#C00000',
                        'opacity': 0.3
                    }
                },
                {
                    'type': 'line',
                    'datasetIndex': 1,
                    'seriesLayoutBy': 'row',
                    'symbol': 'none',
                    'smooth': 'true',
                    'color': '#C00000',
                    'lineStyle': {
                        'opacity': 0
                    },
                    'areaStyle': {
                        'color': '#C00000',
                        'opacity': 0.3
                    }
                }
            ]
        }
        if self.lazy_load:
            option['lazyLoad'] = 'true'
        return ChartItem('PACF[{}]'.format(col), option)

    def moving_average_item(self, rolling_window):
        """
        It will plot rolling mean by given rolling window size.

        Parameters
        ----------

        rolling_window : int, optional
                Window size for rolling function. If negative, it will use the points before CURRENT ROW.

        Returns
        -------
        item : ChartItem
            The item for the plot.
        """
        col = self.endog
        data_ = self.dataset.select([self.key, col]).generate_feature(targets=[col], order_by=self.key, trans_func="AVG", rolling_window=rolling_window).collect()

        X = list(data_.iloc[:, 0].astype(str))
        X.insert(0, self.key)
        Y1 = list(data_.iloc[:, 1])
        Y1.insert(0, data_.columns[1])
        Y2 = list(data_.iloc[:, 2])
        Y2.insert(0, data_.columns[2])

        option = {
            'dataset': {
                'source': [
                    X,
                    Y1,
                    Y2
                ]
            },
            'grid': {
                'show': 'true',
                'containLabel': 'true'
            },
            'legend': {},
            'xAxis': {
                'type': 'category',
                'axisTick': {
                    'alignWithLabel': 'true'
                },
                'axisLabel': {
                    'showMinLabel': 'true',
                    'showMaxLabel': 'true',
                    'hideOverlap': 'true',
                    'rotate': 45,
                    'fontSize': 9,
                }
            },
            'yAxis': {
                'type': 'value',
                'axisLine': {
                    'show': 'true',
                },
                'axisTick': {
                    'show': 'true'
                },
                'axisLabel': {
                    'showMinLabel': 'true',
                    'showMaxLabel': 'true',
                    'hideOverlap': 'true',
                    'rotate': 15,
                    'fontSize': 9,
                    'interval': 0
                }
            },
            'tooltip': {
                'trigger': 'axis'
            },
            'series': [
                {
                    'type': 'line',
                    'seriesLayoutBy': 'row',
                    'color': '#5698C6',
                    'name': data_.columns[1],
                    'emphasis': {
                        'focus': 'self'
                    }
                },
                {
                    'type': 'line',
                    'seriesLayoutBy': 'row',
                    'color': '#FFA65C',
                    'name': data_.columns[2],
                    'emphasis': {
                        'focus': 'self'
                    }
                }
            ]
        }
        if self.lazy_load:
            option['lazyLoad'] = 'true'
        return ChartItem('Rolling Mean[{}]'.format(col), option)

    def rolling_stddev_item(self, rolling_window):
        """
        It will plot rolling standard deviation by given rolling window size.

        Parameters
        ----------

        rolling_window : int, optional
                Window size for rolling function. If negative, it will use the points before CURRENT ROW.

        Returns
        -------
        item : ChartItem
            The item for the plot.
        """
        col = self.endog
        data_ = self.dataset.select([self.key, col]).generate_feature(targets=[col], order_by=self.key, trans_func="STDDEV", rolling_window=rolling_window).collect()

        X = list(data_.iloc[:, 0].astype(str))
        X.insert(0, self.key)
        Y = list(data_.iloc[:, 2])
        Y.insert(0, data_.columns[2])

        option = {
            'dataset': {
                'source': [
                    X,
                    Y
                ]
            },
            'grid': {
                'show': 'true',
                'containLabel': 'true'
            },
            'legend': {},
            'xAxis': {
                'type': 'category',
                'axisTick': {
                    'alignWithLabel': 'true'
                },
                'axisLabel': {
                    'showMinLabel': 'true',
                    'showMaxLabel': 'true',
                    'hideOverlap': 'true',
                    'rotate': 45,
                    'fontSize': 9,
                }
            },
            'yAxis': {
                'type': 'value',
                'axisLine': {
                    'show': 'true',
                },
                'axisTick': {
                    'show': 'true'
                },
                'axisLabel': {
                    'showMinLabel': 'true',
                    'showMaxLabel': 'true',
                    'hideOverlap': 'true',
                    'rotate': 15,
                    'fontSize': 9,
                    'interval': 0
                }
            },
            'tooltip': {
                'trigger': 'axis'
            },
            'series': [
                {
                    'type': 'line',
                    'seriesLayoutBy': 'row',
                    'color': '#5698C6',
                    'name': data_.columns[2]
                }
            ]
        }
        if self.lazy_load:
            option['lazyLoad'] = 'true'
        return ChartItem('Rolling Standard Deviation[{}]'.format(col), option)

    def seasonal_item(self):
        """
        It will plot time series data by year.

        Returns
        -------
        item : ChartItem
            The item for the plot.
        """
        col = self.endog
        data_ = self.dataset.select([self.key, col]).generate_feature(targets=[self.key], trans_func="YEAR")
        temp_tab_name = "#timeseries_box_plot_{}".format(str(uuid.uuid1()).replace('-', '_'))
        data_.save(temp_tab_name)
        data_ = data_.connection_context.table(temp_tab_name)
        lines_to_plot = data_.distinct(data_.columns[2]).collect()[data_.columns[2]].to_list()

        datasets = []
        series = []
        datasetIndex = -1

        for line_to_plot in lines_to_plot:
            datasetIndex = datasetIndex + 1
            temp_df = data_.filter('"{}"={}'.format(data_.columns[2], line_to_plot))
            temp_df = temp_df.generate_feature(targets=[self.key], trans_func="MONTH")
            temp_df = temp_df.agg([('avg', col, 'MONTH_AVG')], group_by=temp_df.columns[3])
            temp_pf = temp_df.collect().sort_values(temp_df.columns[0])


            X = list(temp_pf.iloc[:, 0])
            X.insert(0, 'MONTH')
            Y = list(temp_pf.iloc[:, 1])
            Y.insert(0, 'AVG({})'.format(col))
            datasets.append({
                'source': [X, Y]
            })
            series.append({
                'datasetIndex': datasetIndex,
                'type': 'line',
                'seriesLayoutBy': 'row',
                'name': line_to_plot,
                'emphasis': {
                    'focus': 'self'
                }
            })
        data_.connection_context.drop_table(temp_tab_name)

        option = {
            'dataset': datasets,
            'grid': {
                'show': 'true',
                'containLabel': 'true'
            },
            'legend': {},
            'xAxis': {
                'name': 'MONTH',
                'type': 'category',
                'axisTick': {
                    'alignWithLabel': 'true'
                },
                'axisLabel': {
                    'showMinLabel': 'true',
                    'showMaxLabel': 'true',
                    'hideOverlap': 'true',
                    'fontSize': 9,
                }
            },
            'yAxis': {
                'name': 'AVG({})'.format(col),
                'type': 'value',
                'axisLine': {
                    'show': 'true',
                },
                'axisTick': {
                    'show': 'true'
                },
                'axisLabel': {
                    'showMinLabel': 'true',
                    'showMaxLabel': 'true',
                    'hideOverlap': 'true',
                    'rotate': 15,
                    'fontSize': 9,
                    'interval': 0
                }
            },
            'tooltip': {
                'trigger': 'axis'
            },
            'series': series
        }
        if self.lazy_load:
            option['lazyLoad'] = 'true'
        return ChartItem('Monthly[{}]'.format(col), option)

    def timeseries_box_item(self, cycle=None):
        """
        It will plot year-wise/month-wise box plot.

        Parameters
        ----------

        cycle : {"YEAR", "QUARTER", "MONTH", "WEEK"}, optional
            It defines the x-axis for the box plot.

        Returns
        -------
        item : ChartItem
            The item for the plot.
        """
        col = self.endog
        data_ = self.dataset.select([self.key, col]).generate_feature(targets=[self.key], trans_func=cycle)
        if cycle != "QUARTER":
            data_ = data_.cast({data_.columns[2]: "INT"})
        temp_tab_name = "#timeseries_box_plot_{}".format(str(uuid.uuid1()).replace('-', '_'))
        data_.save(temp_tab_name)
        data_ = data_.connection_context.table(temp_tab_name)
        temp_data_ = data_.collect().sort_values(data_.columns[2], ascending=True)

        Y = list(temp_data_.iloc[:, 1])
        X = list(temp_data_.iloc[:, 2].astype(str))
        temp_dataset = {}
        for i in set(X):
            temp_dataset[i] = []
        for i in range(0, len(X)):
            temp_dataset[X[i]].append(Y[i])
        dataset = []
        sorted_x = list(set(X))
        sorted_x.sort(key=X.index)
        for i in sorted_x:
            dataset.append(temp_dataset[i])
        data_.connection_context.drop_table(temp_tab_name)

        option = {
            'customFn': ['xAxis.axisLabel.formatter'],
            'dataset': [
                {
                    'source': dataset
                },
                {
                    'transform': {
                        'type': 'boxplot'
                    }
                },
                {
                    'fromDatasetIndex': 1,
                    'fromTransformResult': 1
                }
            ],
            'grid': {
                'show': 'true',
                'containLabel': 'true'
            },
            'legend': {},
            'xAxis': {
                'type': 'category',
                'axisTick': {
                    'alignWithLabel': 'true'
                },
                'axisLabel': {
                    'showMinLabel': 'true',
                    'showMaxLabel': 'true',
                    'hideOverlap': 'true',
                    'fontSize': 9,
                    'formatter': {
                        'params': ['value'],
                        'body': "".join(['return {}[value]'.format(str(sorted_x))])
                    }
                }
            },
            'yAxis': {
                'type': 'value',
                'axisLine': {
                    'show': 'true',
                },
                'axisTick': {
                    'show': 'true'
                },
                'axisLabel': {
                    'showMinLabel': 'true',
                    'showMaxLabel': 'true',
                    'hideOverlap': 'true',
                    'rotate': 15,
                    'fontSize': 9,
                    'interval': 0
                }
            },
            'tooltip': {
                'trigger': 'item',
                'axisPointer': {
                    'type': 'shadow'
                }
            },
            'series': [
                {
                    'name': 'Boxplot',
                    'type': 'boxplot',
                    'datasetIndex': 1
                },
                {
                    'name': 'Outlier',
                    'type': 'scatter',
                    'datasetIndex': 2,
                    'color': '#C00000'
                }
            ]
        }
        if self.lazy_load:
            option['lazyLoad'] = 'true'
        return ChartItem('Box[{}-{}]'.format(col, cycle), option)

    def seasonal_decompose_items(self, alpha=None, thread_ratio=None, decompose_type=None, extrapolation=None, smooth_width=None):
        """
        It will to decompose a time series into three components: trend, seasonality and random noise, then to plot.

        Parameters
        ----------

        alpha : float, optional
            The criterion for the autocorrelation coefficient.
            The value range is (0, 1). A larger value indicates stricter requirement for seasonality.

            Defaults to 0.2.

        thread_ratio : float, optional
            Controls the proportion of available threads to use.
            The ratio of available threads.

                - 0: single thread.
                - 0~1: percentage.
                - Others: heuristically determined.

            Defaults to -1.

        decompose_type : {'additive', 'multiplicative', 'auto'}, optional
            Specifies decompose type.

              - 'additive': additive decomposition model
              - 'multiplicative': multiplicative decomposition model
              - 'auto': decomposition model automatically determined from input data

            Defaults to 'auto'.

        extrapolation : bool, optional
            Specifies whether to extrapolate the endpoints.
            Set to True when there is an end-point issue.

            Defaults to False.

        smooth_width : int, optional
            Specifies the width of the moving average applied to non-seasonal data.
            0 indicates linear fitting to extract trends.
            Can not be larger than half of the data length.

            Defaults to 0.

        Returns
        -------
        item : ChartItem
            The item for the plot.
        """
        col = self.endog
        _, res = seasonal_decompose.seasonal_decompose(data=self.dataset, endog=col, key=self.key, alpha=alpha, thread_ratio=thread_ratio, decompose_type=decompose_type, extrapolation=extrapolation, smooth_width=smooth_width)
        res = res.collect()

        X = list(res.iloc[:, 0].astype(str))
        X.insert(0, self.key)
        items = []
        for i in range(0, 3):
            datasets = []
            series = []
            Y = list(res.iloc[:, i + 1])
            Y.insert(0, res.columns[i + 1])
            datasets.append({
                'source': [X, Y]
            })
            series.append({
                'type': 'line',
                'seriesLayoutBy': 'row',
                'name': res.columns[i + 1],
                'emphasis': {
                    'focus': 'self'
                }
            })
            option = {
                'dataset': datasets,
                'grid': {
                    'show': 'true',
                    'containLabel': 'true'
                },
                'legend': {},
                'xAxis': {
                    'type': 'category',
                    'axisTick': {
                        'alignWithLabel': 'true'
                    },
                    'axisLabel': {
                        'showMinLabel': 'true',
                        'showMaxLabel': 'true',
                        'hideOverlap': 'true',
                        'rotate': 45,
                        'fontSize': 9,
                    }
                },
                'yAxis': {
                    'type': 'value',
                    'axisLine': {
                        'show': 'true',
                    },
                    'axisTick': {
                        'show': 'true'
                    },
                    'axisLabel': {
                        'showMinLabel': 'true',
                        'showMaxLabel': 'true',
                        'hideOverlap': 'true',
                        'rotate': 15,
                        'fontSize': 9,
                        'interval': 0
                    }
                },
                'tooltip': {
                    'trigger': 'axis'
                },
                'series': series
            }
            if self.lazy_load:
                option['lazyLoad'] = 'true'
            items.append(ChartItem("Seasonal Decompose[{}-{}]".format(col, res.columns[i + 1]), option))
        return items

    def quarter_item(self):
        """
        It performs quarter plot to view the seasonality.

        Returns
        -------
        item : ChartItem
            The item for the plot.
        """
        col = self.endog
        new_id = "NEWID_{}".format(str(uuid.uuid1()).replace("-", "_"))
        temp_tab = "#temp_tab_{}".format(str(uuid.uuid1()).replace("-", "_"))
        temp_df = self.dataset.select([self.key, col]).generate_feature(targets=[self.key], trans_func="QUARTER")
        temp_df = temp_df.split_column(temp_df.columns[2], '-', ["YEAR", "Q"]).add_id(new_id, ref_col=["Q", "YEAR", self.key])
        years = temp_df.select("YEAR").distinct().collect().iloc[:, 0]
        temp_df.save(temp_tab)
        temp_df = self.dataset.connection_context.table(temp_tab)

        datasets = []
        series = []
        mark_exist = False
        datasetIndex = -1
        my_pos = None
        for quarter in ["Q1", "Q2", "Q3", "Q4"]:
            my_pos = temp_df.filter("Q='{}'".format(quarter)).select([new_id]).median()
            min_x = temp_df.filter("Q='{}'".format(quarter)).select([new_id]).min()
            max_x = temp_df.filter("Q='{}'".format(quarter)).select([new_id]).max()
            avg_q = temp_df.filter("Q='{}'".format(quarter)).select([col]).mean()
            mark_exist = False

            for year in years:
                # ID Y
                xx_filter = temp_df.filter("Q='{}' AND YEAR='{}'".format(quarter, year)).select([new_id, col])
                xx_filter_collect = xx_filter.collect()
                X = list(xx_filter_collect.iloc[:, 0])
                if len(X) == 0:
                    continue
                X.insert(0, "{}-{}".format(year, quarter))
                Y = list(xx_filter_collect.iloc[:, 1])
                Y.insert(0, col)
                datasets.append({
                    'source': [X, Y]
                })
                datasetIndex = datasetIndex + 1

                sery = {
                    'datasetIndex': datasetIndex,
                    'type': 'line',
                    'seriesLayoutBy': 'row',
                    'name': "{}-{}".format(year, quarter),
                    'color': '#5698C6'
                }
                if mark_exist is False and my_pos:
                    # sery['markPoint'] = {
                    #     'data': [
                    #         {
                    #             'name': '',
                    #             'xAxis': my_pos - 1,
                    #             'yAxis': 0,
                    #             'value': quarter
                    #         }
                    #     ],
                    #     'itemStyle': {
                    #         'color': '#FFC957',
                    #         'opacity': 0.8
                    #     },
                    # }
                    sery['markLine'] = {
                        'symbol': ['none', 'none'],
                        'symbolSize': 4,
                        'data': [
                            [
                                {
                                    # 'name': quarter,
                                    'symbol': 'circle',
                                    'lineStyle': {
                                        'color': '#C00000'
                                    },
                                    'label': {
                                        'position': 'middle',
                                        'color': '#C00000'
                                    },
                                    'coord': [min_x - 1, avg_q]
                                },
                                {
                                    'symbol': 'circle',
                                    'coord': [max_x - 1, avg_q]
                                }
                            ],
                            {
                                'name': quarter,
                                'xAxis': my_pos - 1,
                                'label': {
                                    'position': 'start',
                                    'formatter': quarter
                                },
                                'lineStyle': {
                                    'color': '#B7BEC9'
                                }
                            }
                        ]
                    }
                    mark_exist = True
                series.append(sery)
        self.dataset.connection_context.drop_table(temp_tab)
        option = {
            'dataset': datasets,
            'grid': {
                'show': 'true',
                'containLabel': 'true'
            },
            'xAxis': {
                'type': 'category',
                'axisTick': {
                    'alignWithLabel': 'true'
                },
                'axisLabel': {
                    'showMinLabel': 'true',
                    'showMaxLabel': 'true',
                    'hideOverlap': 'true',
                    'rotate': 45,
                    'fontSize': 9,
                    'formatter': ''
                }
            },
            'yAxis': {
                'type': 'value',
                'axisLine': {
                    'show': 'true',
                },
                'axisTick': {
                    'show': 'true'
                },
                'axisLabel': {
                    'showMinLabel': 'true',
                    'showMaxLabel': 'true',
                    'hideOverlap': 'true',
                    'rotate': 15,
                    'fontSize': 9,
                    'interval': 0
                }
            },
            'tooltip': {
                'trigger': 'axis'
            },
            'series': series
        }
        if self.lazy_load:
            option['lazyLoad'] = 'true'
        return ChartItem('Quarter[{}]'.format(col), option)

    def outlier_item(self, window_size=None, detect_seasonality=None, alpha=None, periods=None, outlier_method=None, threshold=None):
        """
        Perform PAL time series outlier detection and plot time series with the highlighted outliers.

        Parameters
        ----------
        window_size : int, optional
            Odd number, the window size for median filter, not less than 3.

            Defaults to 3.

        outlier_method : str, optional

            The method for calculate the outlier score from residual.

              - 'z1' : Z1 score.
              - 'z2' : Z2 score.
              - 'iqr' : IQR score.
              - 'mad' : MAD score.

            Defaults to 'z1'.

        threshold : float, optional
            The threshold for outlier score. If the absolute value of outlier score is beyond the
            threshold, we consider the corresponding data point as an outlier.

            Defaults to 3.

        detect_seasonality : bool, optional
            When calculating the residual,

            - False: Does not consider the seasonal decomposition.
            - True: Considers the seasonal decomposition.

            Defaults to False.

        alpha : float, optional
            The criterion for the autocorrelation coefficient. The value range is (0, 1).
            A larger value indicates a stricter requirement for seasonality.

            Only valid when ``detect_seasonality`` is True.

            Defaults to 0.2.

        periods : int, optional
            When this parameter is not specified, the algorithm will search the seasonal period.
            When this parameter is specified between 2 and half of the series length, autocorrelation value
            is calculated for this number of periods and the result is compared to ``alpha`` parameter.
            If correlation value is equal to or higher than ``alpha``, decomposition is executed with the value of ``periods``.
            Otherwise, the residual is calculated without decomposition. For other value of parameter ``periods``,
            the residual is also calculated without decomposition.

            No Default value.

        thread_ratio : float, optional
            The ratio of available threads.

            - 0: single thread.
            - 0~1: percentage.
            - Others: heuristically determined.

            Only valid when ``detect_seasonality`` is True.

            Defaults to -1.

        Returns
        -------
        item : ChartItem
            The item for the plot.
        """
        odts = OutlierDetectionTS(window_size=window_size,
                                detect_seasonality=detect_seasonality,
                                alpha=alpha,
                                periods=periods,
                                outlier_method=outlier_method,
                                threshold=threshold)
        result = odts.fit_predict(data=self.dataset, key=self.key, endog=self.endog)
        res_col = result.columns
        result = result.select([res_col[0], res_col[1], res_col[4]]).collect()
        result.set_index(res_col[0])
        outliers = result.loc[result["IS_OUTLIER"] == 1, [res_col[0], "RAW_DATA"]]

        datasets = []
        series = []
        datasetIndex = -1

        datasetIndex = datasetIndex + 1
        # TIMESTAMP
        X = list(result.iloc[:, 0].astype(str))
        X.insert(0, 'TIMESTAMP')
        # RAW_DATA
        Y = list(result.iloc[:, 1])
        Y.insert(0, 'RAWDATA')
        datasets.append({
            'source': [X, Y]
        })
        series.append({
            'datasetIndex': datasetIndex,
            'type': 'line',
            'seriesLayoutBy': 'row',
            'name': '',
            'emphasis': {
                'focus': 'self'
            }
        })

        datasetIndex = datasetIndex + 1
        # TIMESTAMP
        X = list(outliers.iloc[:, 0].astype(str))
        X.insert(0, 'TIMESTAMP')
        # RAW_DATA
        Y = list(outliers.iloc[:, 1])
        Y.insert(0, 'RAWDATA')
        datasets.append({
            'source': [X, Y]
        })
        series.append({
            'datasetIndex': datasetIndex,
            'type': 'scatter',
            'seriesLayoutBy': 'row',
            'name': 'Outlier',
            'color': '#C00000',
            'emphasis': {
                'focus': 'self'
            }
        })

        option = {
            'dataset': datasets,
            'grid': {
                'show': 'true',
                'containLabel': 'true'
            },
            'legend': {},
            'xAxis': {
                'name': 'TIMESTAMP',
                'type': 'category',
                'axisTick': {
                    'alignWithLabel': 'true'
                },
                'axisLabel': {
                    'showMinLabel': 'true',
                    'showMaxLabel': 'true',
                    'hideOverlap': 'true',
                    'rotate': 45,
                    'fontSize': 9,
                }
            },
            'yAxis': {
                'name': 'RAWDATA',
                'type': 'value',
                'axisLine': {
                    'show': 'true',
                },
                'axisTick': {
                    'show': 'true'
                },
                'axisLabel': {
                    'showMinLabel': 'true',
                    'showMaxLabel': 'true',
                    'hideOverlap': 'true',
                    'rotate': 15,
                    'fontSize': 9,
                    'interval': 0
                }
            },
            'tooltip': {
                'trigger': 'axis'
            },
            'series': series
        }
        if self.lazy_load:
            option['lazyLoad'] = 'true'
        return ChartItem('Outlier', option)

    def stationarity_item(self, method=None, mode=None, lag=None, probability=None):
        """
        Stationarity means that a time series has a constant mean and constant variance over time.
        For many time series models, the input data has to be stationary for reasonable analysis.

        Parameters
        ----------
        method : str, optional
            Statistic test that used to determine stationarity. The options are "kpss" and "adf".

            Defaults "kpss".

        mode : str, optional
            Type of stationarity to determine. The options are "level", "trend" and "no".
            Note that option "no" is not applicable to "kpss".

            Defaults to "level".

        lag : int, optional
            The lag order to calculate the test statistic.

            Default value is "kpss": int(12*(data_length / 100)^0.25" ) and "adf": int(4*(data_length / 100)^(2/9)).

        probability : float, optional
            The confidence level for confirming stationarity.

            Defaults to 0.9.

        Returns
        -------
        item : TableItem
            The item for the statistical data.
        """
        stats = stationarity_test.stationarity_test(self.dataset, key=self.key, endog=self.endog, method=method, mode=mode, lag=lag, probability=probability)
        columns = list(stats.columns)
        stats = stats.collect()

        table_item = TableItem('Stationarity')
        table_item.addColumn(columns[0], list(stats.iloc[:, 0].astype(str)))
        table_item.addColumn(columns[1], list(stats.iloc[:, 1].astype(str)))
        return table_item

    def real_item(self):
        """
        It will plot a chart based on the original data.

        Parameters
        ----------
        None

        Returns
        -------
        item : ChartItem
            The item for the plot.
        """
        data_ = self.dataset.collect().sort_values(self.key, ascending=True)

        X = list(data_[self.key].astype(str))
        X.insert(0, self.key)
        Y = list(data_[self.endog])
        Y.insert(0, self.endog)

        option = {
            'dataset': {
                'source': [
                    X,
                    Y
                ]
            },
            'grid': {
                'show': 'true',
                'containLabel': 'true'
            },
            'legend': {},
            'xAxis': {
                'type': 'category',
                'axisTick': {
                    'alignWithLabel': 'true'
                },
                'axisLabel': {
                    'showMinLabel': 'true',
                    'showMaxLabel': 'true',
                    'hideOverlap': 'true',
                    'rotate': 45,
                    'fontSize': 9,
                }
            },
            'yAxis': {
                'type': 'value',
                'axisLine': {
                    'show': 'true',
                },
                'axisTick': {
                    'show': 'true'
                },
                'axisLabel': {
                    'showMinLabel': 'true',
                    'showMaxLabel': 'true',
                    'hideOverlap': 'true',
                    'rotate': 15,
                    'fontSize': 9,
                    'interval': 0
                }
            },
            'tooltip': {
                'trigger': 'axis'
            },
            'series': [
                {
                    'type': 'line',
                    'seriesLayoutBy': 'row',
                    'color': '#5698C6',
                    'name': 'Real[{}]'.format(self.endog)
                }
            ]
        }
        if self.lazy_load:
            option['lazyLoad'] = 'true'
        return ChartItem('Real[{}]'.format(self.endog), option)

    def change_points_item(self, cp_object, display_trend=True, cp_style="axvline", title=None):
        """
        Plot time series with the highlighted change points and BCPD is used for change point detection.

        Parameters
        ----------
        cp_object : BCPD object

            An object of BCPD for change points detection. Please initialize a BCPD object first.
            An exmaple is shown below:

            .. raw:: html

                <iframe allowtransparency="true" style="border:1px solid #ccc; background: #eeffcb;"
                    src="_static/eda_example.html" width="100%" height="100%">
                </iframe>
        cp_style : {"axvline", "scatter"}, optional

            The style of change points in the plot.

            Defaults to "axvline".

        display_trend : bool, optional

            If True, draw the trend component based on decomposed component of trend of BCPD fit_predict().

            Default to True.

        title : str, optional

            The title of plot.

            Defaults to "Change Points".

        Returns
        -------
        item : ChartItem
            The item for the plot.
        """
        if isinstance(cp_object, BCPD):
            datasets = []
            series = []
            datasetIndex = -1

            tcp, scp, period, components = cp_object.fit_predict(data=self.dataset, key=self.key, endog=self.endog)
            if display_trend is True:
                x_loc = -1
                for j in range(0, len(components.columns)):
                    if components.columns[j] == self.key:
                        x_loc = j
                        break
                # build data
                temp_components = components.collect()
                X = list(temp_components.iloc[:, x_loc].astype(str))
                X.insert(0, self.key)
                Y = list(temp_components["TREND"])
                Y.insert(0, 'TREND')
                datasetIndex = datasetIndex + 1
                datasets.append({
                    'source': [X, Y]
                })
                series.append({
                    'datasetIndex': datasetIndex,
                    'type': 'line',
                    'seriesLayoutBy': 'row',
                    'name': 'Trend Component',
                    'emphasis': {
                        'focus': 'self'
                    }
                })
            # build data
            temp_dataset = self.dataset.collect()
            x_loc = -1
            for j in range(0, len(self.dataset.columns)):
                if self.dataset.columns[j] == self.key:
                    x_loc = j
                    break
            X = list(temp_dataset.iloc[:, x_loc].astype(str))
            X.insert(0, self.key)
            Y = list(temp_dataset[self.endog])
            Y.insert(0, self.endog)
            datasetIndex = datasetIndex + 1
            datasets.append({
                'source': [X, Y]
            })
            series.append({
                'datasetIndex': datasetIndex,
                'type': 'line',
                'seriesLayoutBy': 'row',
                'name': 'Original Time Series',
                'emphasis': {
                    'focus': 'self'
                }
            })

            if tcp.shape[0] > 0:
                if cp_style == "scatter":
                    tcp.set_index('TREND_CP')
                    result = tcp.join(self.dataset, how='left')
                    x_loc = -1
                    for j in range(0, len(result.columns)):
                        if result.columns[j] == 'TREND_CP':
                            x_loc = j
                            break
                    # build data
                    temp_result = result.collect()
                    X = list(temp_result.iloc[:, x_loc].astype(str))
                    X.insert(0, 'TREND_CP')
                    Y = list(temp_result[self.endog])
                    Y.insert(0, self.endog)
                    datasetIndex = datasetIndex + 1
                    datasets.append({
                        'source': [X, Y]
                    })
                    series.append({
                        'datasetIndex': datasetIndex,
                        'type': 'scatter',
                        'color': 'red',
                        'seriesLayoutBy': 'row',
                        'name': 'Trend Change Points',
                        'emphasis': {
                            'focus': 'self'
                        }
                    })

                if cp_style == "axvline":
                    temp_tcp = tcp.collect()
                    x_loc = -1
                    for j in range(0, len(tcp.columns)):
                        if tcp.columns[j] == 'TREND_CP':
                            x_loc = j
                            break
                    tcp_list = list(temp_tcp.iloc[:, x_loc].astype(str))
                    axvlines = []
                    for i in range(len(tcp_list)):
                        axvlines.append({
                            'xAxis': tcp_list[i],
                            'lineStyle': {
                                'color': 'red'
                            }
                        })
                    X = [tcp_list[0]]
                    X.insert(0, 'TREND_CP')
                    Y = [0]
                    Y.insert(0, 'fake data')
                    datasetIndex = datasetIndex + 1
                    datasets.append({
                        'source': [X, Y]
                    })
                    series.append({
                        'datasetIndex': datasetIndex,
                        'type': 'line',
                        'color': 'red',
                        'seriesLayoutBy': 'row',
                        'name': 'Trend Change Points',
                        'showSymbol': 'false',
                        'tooltip': {
                            'show': 'false'
                        },
                        'label': {
                            'borderType': 'dashed'
                        },
                        'markLine' : {
                            'symbol': ['none', 'none'],
                            'symbolSize': 4,
                            'label': {
                                'show': 'false'
                            },
                            'data': axvlines
                        }
                    })
            if scp.shape[0] > 0:
                if cp_style == "scatter":
                    scp.set_index('SEASON_CP')
                    result = scp.join(self.dataset, how='left')
                    x_loc = -1
                    for j in range(0, len(result.columns)):
                        if result.columns[j] == 'SEASON_CP':
                            x_loc = j
                            break
                    # build data
                    temp_result = result.collect()
                    X = list(temp_result.iloc[:, x_loc].astype(str))
                    X.insert(0, 'SEASON_CP')
                    Y = list(temp_result[self.endog])
                    Y.insert(0, self.endog)
                    datasetIndex = datasetIndex + 1
                    datasets.append({
                        'source': [X, Y]
                    })
                    series.append({
                        'datasetIndex': datasetIndex,
                        'type': 'scatter',
                        'seriesLayoutBy': 'row',
                        'color': 'green',
                        'name': 'Seasonal Change Points',
                        'emphasis': {
                            'focus': 'self'
                        }
                    })
                if cp_style == "axvline":
                    temp_scp = scp.collect()
                    x_loc = -1
                    for j in range(0, len(scp.columns)):
                        if scp.columns[j] == 'SEASON_CP':
                            x_loc = j
                            break
                    scp_list = list(temp_scp.iloc[:, x_loc].astype(str))
                    axvlines = []
                    for i in range(len(scp_list)):
                        axvlines.append({
                            'xAxis': scp_list[i],
                            'lineStyle': {
                                'color': 'green'
                            }
                        })
                    X = [scp_list[0]]
                    X.insert(0, 'SEASON_CP')
                    Y = [0]
                    Y.insert(0, 'fake data')
                    datasetIndex = datasetIndex + 1
                    datasets.append({
                        'source': [X, Y]
                    })
                    series.append({
                        'datasetIndex': datasetIndex,
                        'type': 'line',
                        'color': 'green',
                        'seriesLayoutBy': 'row',
                        'name': 'Seasonal Change Points',
                        'showSymbol': 'false',
                        'tooltip': {
                            'show': 'false'
                        },
                        'label': {
                            'borderType': 'dashed'
                        },
                        'markLine' : {
                            'symbol': ['none', 'none'],
                            'symbolSize': 4,
                            'label': {
                                'show': 'false'
                            },
                            'data': axvlines
                        }
                    })

            # self.dataset.select(self.key).dtypes()[0][1] != "INT
            if title is None:
                title = "Change Points"
            option = {
                'dataset': datasets,
                'grid': {
                    'show': 'true',
                    'containLabel': 'true'
                },
                'legend': {},
                'xAxis': {
                    'name': self.key,
                    'type': 'category',
                    'axisTick': {
                        'alignWithLabel': 'true'
                    },
                    'axisLabel': {
                        'showMinLabel': 'true',
                        'showMaxLabel': 'true',
                        'hideOverlap': 'true',
                        'rotate': 45,
                        'fontSize': 9,
                    }
                },
                'yAxis': {
                    'name': self.endog,
                    'type': 'value',
                    'axisLine': {
                        'show': 'true',
                    },
                    'axisTick': {
                        'show': 'true'
                    },
                    'axisLabel': {
                        'showMinLabel': 'true',
                        'showMaxLabel': 'true',
                        'hideOverlap': 'true',
                        'rotate': 15,
                        'fontSize': 9,
                        'interval': 0
                    }
                },
                'tooltip': {
                    'trigger': 'axis'
                },
                'series': series
            }
            if self.lazy_load:
                option['lazyLoad'] = 'true'
            return ChartItem(title, option)
