import numpy as np
np.random.seed(0)
import pandas as pd
# import time
# import re
# from datetime import date
# from dateutil.relativedelta import relativedelta
# from statsmodels.tsa.exponential_smoothing.ets import ETSModel
from zeno_etl_libs.utils.warehouse.forecast.errors import ape_calc, ae_calc
from prophet import Prophet
from statsmodels.tsa.holtwinters import ExponentialSmoothing
# from statsmodels.tsa.api import ExponentialSmoothing

# import sktime
from sktime.forecasting.ets import AutoETS
from zeno_etl_libs.utils.ipc2.helpers.helper_functions import sum_std,\
    applyParallel, applyParallel_croston
# from boruta import BorutaPy

from zeno_etl_libs.utils.goodaid_forecast.engine.config_goodaid import (
    date_col,
    target_col,
    models,
    ets_params
)

import logging
logger = logging.getLogger("_logger")
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


class Goodaid_tS_forecast:

    def train_test_split(self, df, train_max_date, forecast_start):
        df.rename(columns={date_col: 'ds', target_col: 'y'}, inplace=True)
        df.sort_values(by=['ds'], inplace=True)
        train = df[df['ds'] <= train_max_date]
        test = df[df['ds'] >= forecast_start]

        return train, test

    def Croston_TSB(self, ts, extra_periods=4, alpha=0.4, beta=0.4):
        d = np.array(ts)  # Transform the input into a numpy array
        cols = len(d)  # Historical period length
        d = np.append(d, [
            np.nan] * extra_periods)  # Append np.nan into the demand array to cover future periods

        # level (a), probability(p) and forecast (f)
        a, p, f = np.full((3, cols + extra_periods), np.nan)
        # Initialization
        first_occurence = np.argmax(d[:cols] > 0)
        a[0] = d[first_occurence]
        p[0] = 1 / (1 + first_occurence)
        f[0] = p[0] * a[0]

        # Create all the t+1 forecasts
        for t in range(0, cols):
            if d[t] > 0:
                a[t + 1] = alpha * d[t] + (1 - alpha) * a[t]
                p[t + 1] = beta * (1) + (1 - beta) * p[t]
            else:
                a[t + 1] = a[t]
                p[t + 1] = (1 - beta) * p[t]
            f[t + 1] = p[t + 1] * a[t + 1]

        # Future Forecast
        a[cols + 1:cols + extra_periods] = a[cols]
        p[cols + 1:cols + extra_periods] = p[cols]
        f[cols + 1:cols + extra_periods] = f[cols]

        df = pd.DataFrame.from_dict(
            {"Demand": d, "Forecast": f, "Period": p, "Level": a,
             "Error": d - f})
        return np.round(df[-extra_periods:])

    def ETS_forecast(self, train, test,ets_params):
        try:
            train = train.copy(deep=True)
            test = test.copy(deep=True)
            train.set_index(['ds'], inplace=True)
            test.set_index(['ds'], inplace=True)
            train.index.freq = train.index.inferred_freq
            test.index.freq = test.index.inferred_freq

            train_final = train.copy(deep=True)

            out_of_sample = len(test)
            horizon = len(test)

            # Train for grid search
            train.drop(train.tail(out_of_sample).index, inplace=True)

            # dividing the series into train and validation set
            drug_id = train['drug_id'].values[0]
            input_series = train['y'].values
            validation = train['y'].tail(out_of_sample).values

            # creating dummy best fit param and fit values
            best_fit_params = [None, None, False, None, False]
            best_accuracy = np.inf

            # running a loop for grid search
            for params in ets_params:
                trend, seasonal, damped, seasonal_periods, use_boxcox = params
                try:
                    ape = []
                    ae = []

                    # model fitting
                    model = ExponentialSmoothing(
                        input_series, trend=trend, seasonal=seasonal, damped=damped,
                        seasonal_periods=seasonal_periods, use_boxcox=use_boxcox)
                    fit = model.fit(optimized=True)

                    # accuracy parameter can be  - aic, bic, sse or mape
                    forecast = np.round(fit.forecast(horizon))
                    # print(forecast)
                    ape = [
                        ape_calc(actual, forecast)
                        for actual, forecast in zip(validation, forecast)]
                    ae = [
                        ae_calc(actual, forecast)
                        for actual, forecast in zip(validation, forecast)]

                    fit_mape = np.mean(ape)
                    # identifying the best fit params
                    if (fit_mape <= best_accuracy) & (fit_mape != -np.inf):
                        best_fit_params = params
                        best_accuracy = fit_mape
                except Exception as error:
                    error_str = '''Drug {} Params {} Error: {}'''.format(
                        drug_id, str(params), error)
                    # logger.info(error_str)
                    pass

            # creating out of output dataset

            trend, seasonal, damped, seasonal_periods, use_boxcox = best_fit_params

            model = ExponentialSmoothing(
                train_final['y'], trend=trend, seasonal=seasonal, damped=damped,
                seasonal_periods=seasonal_periods, use_boxcox=use_boxcox)
            fit = model.fit(optimized=True)
            forecast = np.round(fit.forecast(horizon+1))
            forecast = forecast[-horizon:]

        except Exception as e:
            logger.info("error in ETS fcst")
            logger.info(str(e))
            forecast = 0

        return forecast

    def SES_forecast(self, train, test):
        try:
            train = train.copy(deep=True)
            test = test.copy(deep=True)
            train.set_index(['ds'], inplace=True)
            test.set_index(['ds'], inplace=True)
            train.index.freq = train.index.inferred_freq
            test.index.freq = test.index.inferred_freq

            fit = ExponentialSmoothing(train['y']).fit(optimized=True)
            # preds_ses = fit.forecast(len(test) + 1)
            preds_ses = np.round(fit.forecast(len(test)+1))
            preds_ses = preds_ses[-len(test):]
        except Exception as e:
            logger.info("error in SES fcst")
            logger.info(str(e))
            preds_ses = 0

        return preds_ses

    def ma_forecast(self, data):
        """
        Purpose: Compute MA forecast for the for the forecast horizon specified
        Inputs: time series to create forecast
        Output: series with forecasted values
        """

        sma_df = data.copy(deep=True)
        yhat = []
        if len(data) >= 8:
            for i in range(5):
                sma_val = sma_df.rolling(7).mean().iloc[-1]
                sma_df.loc[sma_df.index.max() + 1] = sma_val
                yhat.append(sma_val)
        else:
            for i in range(5):
                sma_val = sma_df.rolling(len(data)).mean().iloc[-1]
                sma_df.loc[sma_df.index.max() + 1] = sma_val
                yhat.append(sma_val)
                yhat.append(sma_val)
        logger.info(yhat)
        return np.round(yhat[-4:])

    def ewm_forecast(self, data):
        sma_df = data.copy(deep=True)
        yhat = []
        if len(data) >= 8:
            for i in range(5):
                sma_val = sma_df.ewm(span=7,adjust=False).mean().iloc[-1]
                sma_df.loc[sma_df.index.max() + 1] = sma_val
                yhat.append(sma_val)
        else:
            for i in range(5):
                sma_val = sma_df.ewm(span=len(data),adjust=False).mean().iloc[-1]
                sma_df.loc[sma_df.index.max() + 1] = sma_val
                yhat.append(sma_val)
                yhat.append(sma_val)
        logger.info(yhat)
        return np.round(yhat[-4:])

    def prophet_fcst(self, train, test, params=None):
        # reg_list = []
        try:
            if params is None:
                pro = Prophet()
            else:
                pro = Prophet(n_changepoints=params)
            # for j in train.columns:
            #     if j not in col_list:
            #         pro.add_regressor(j)
            #         reg_list.append(j)
            pro.fit(train[['ds', 'y']])
            pred_f = pro.predict(test)
            test = test[["ds", "y"]]
            test = pd.merge(test, pred_f, on="ds", how="left")
        except Exception as e:
            logger.info("error in prophet fcst")
            logger.info(str(e))
            test['yhat'] = 0
        return np.round(test)

    def ts_forecast(self, df, train_max_date, forecast_start):
        train, test = self.train_test_split(df, train_max_date=train_max_date,
                                            forecast_start=forecast_start)
        test = test.sort_values(by=['ds'])
        if 'croston' in models:
            preds_croston = self.Croston_TSB(train['y'])
            test['preds_croston'] = preds_croston['Forecast'].values
        if 'ETS' in models:
            preds_ETS = self.ETS_forecast(train.copy(), test.copy(),ets_params)
            try:
                test['preds_ETS'] = preds_ETS.values
            except:
                test['preds_ETS'] = np.nan
        if 'SES' in models:
            preds_SES = self.SES_forecast(train.copy(), test.copy())
            try:
                test['preds_SES'] = preds_SES.values
            except:
                test['preds_SES'] = np.nan
        if 'EWM' in models:
            preds_ewm = self.ewm_forecast(train['y'])
            test['preds_ewm'] = preds_ewm
        if 'MA' in models:
            preds_ma = self.ma_forecast(train['y'])
            test['preds_ma'] = preds_ma
        if 'prophet' in models:
            preds_prophet = self.prophet_fcst(train.copy(), test.copy())
            test['preds_prophet'] = preds_prophet['yhat'].values

        return test

    def apply_ts_forecast(self, df, train_max_date, forecast_start):
        # global train_date
        # train_date = train_max_date
        # global forecast_start_date
        # forecast_start_date  = forecast_start
        preds = applyParallel_croston(
            df.groupby('ts_id'),
            func=self.ts_forecast, train_max_date=train_max_date,
            forecast_start=forecast_start
        )

        preds.rename(columns={'ds': date_col, 'y': target_col}, inplace=True)
        ts_fcst_cols = [i for i in preds.columns if i.startswith('preds_')]
        for col in ts_fcst_cols:
            preds[col].fillna(0, inplace=True)
            preds[col] = np.where(preds[col] < 0, 0, preds[col])
            preds[col] = preds[col].replace(0, np.NaN)

        preds['preds_AE_ts'] = preds[ts_fcst_cols].mean(axis=1,skipna=True)
        preds['preds_ME_ts'] = preds[ts_fcst_cols].max(axis=1)

        ts_fcst_cols = [i for i in preds.columns if i.startswith('preds_')]
        for col in ts_fcst_cols:
            preds[col].fillna(0, inplace=True)
            preds[col] = np.where(preds[col] < 0, 0, preds[col])

        return preds, ts_fcst_cols
