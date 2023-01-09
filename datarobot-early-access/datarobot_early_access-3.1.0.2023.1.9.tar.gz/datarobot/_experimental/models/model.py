#
# Copyright 2021-2022 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.

from datarobot.models import DatetimeModel as datarobot_datetime_model
from datarobot.models import FeatureEffects
from datarobot.models import Model as datarobot_model


class Model(datarobot_model):  # pylint: disable=missing-class-docstring
    def get_feature_effect(self, source, include_ice_plots=False):
        """
        Retrieve Feature Effects for the model.

        Feature Effects provides partial dependence and predicted vs actual values for top-500
        features ordered by feature impact score.

        The partial dependence shows marginal effect of a feature on the target variable after
        accounting for the average effects of all other predictive features. It indicates how,
        holding all other variables except the feature of interest as they were,
        the value of this feature affects your prediction.

        Requires that Feature Effects has already been computed with
        :meth:`request_feature_effect <datarobot.models.Model.request_feature_effect>`.

        See :meth:`get_feature_effect_metadata <datarobot.models.Model.get_feature_effect_metadata>`
        for retrieving information the available sources.

        Parameters
        ----------
        source : string
            The source Feature Effects are retrieved for.
        include_ice_plots: bool, optional
            Indicates whether Individual Conditional Expectation (ICE) plots should be returned.

        Returns
        -------
        feature_effects : FeatureEffects
           The feature effects data.

        Raises
        ------
        ClientError (404)
            If the feature effects have not been computed or source is not valid value.
        """
        params = {"source": source, "includeIcePlots": include_ice_plots}
        fe_url = self._get_feature_effect_url()
        server_data = self._client.get(fe_url, params=params).json()
        return FeatureEffects.from_server_data(server_data)


class DatetimeModel(datarobot_datetime_model):  # pylint: disable=missing-class-docstring
    def get_feature_effect(self, source, backtest_index, include_ice_plots=False):
        """
        Retrieve Feature Effects for the model.

        Feature Effects provides partial dependence and predicted vs actual values for top-500
        features ordered by feature impact score.

        The partial dependence shows marginal effect of a feature on the target variable after
        accounting for the average effects of all other predictive features. It indicates how,
        holding all other variables except the feature of interest as they were,
        the value of this feature affects your prediction.

        Requires that Feature Effects has already been computed with
        :meth:`request_feature_effect <datarobot.models.Model.request_feature_effect>`.

        See :meth:`get_feature_effect_metadata \
        <datarobot.models.DatetimeModel.get_feature_effect_metadata>`
        for retrieving information of source, backtest_index.

        Parameters
        ----------
        source: string
            The source Feature Effects are retrieved for.
            One value of [FeatureEffectMetadataDatetime.sources]. To retrieve the available
            sources for feature effect.

        backtest_index: string, FeatureEffectMetadataDatetime.backtest_index.
            The backtest index to retrieve Feature Effects for.

        include_ice_plots: bool, optional
            Indicates whether Individual Conditional Expectation (ICE) plots should be returned.

        Returns
        -------
        feature_effects: FeatureEffects
           The feature effects data.

        Raises
        ------
        ClientError (404)
            If the feature effects have not been computed or source is not valid value.
        """
        params = {
            "source": source,
            "backtestIndex": backtest_index,
            "includeIcePlots": include_ice_plots,
        }
        fe_url = self._get_feature_effect_url()
        server_data = self._client.get(fe_url, params=params).json()
        return FeatureEffects.from_server_data(server_data)
