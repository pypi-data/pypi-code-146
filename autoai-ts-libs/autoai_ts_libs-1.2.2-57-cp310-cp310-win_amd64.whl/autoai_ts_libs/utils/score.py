# ************* Begin Copyright - Do not add comments here **************
#   Licensed Materials - Property of IBM
#
#   (C) Copyright IBM Corp. 2021, 2022, All Rights Reserved
#
# The source code for this program is not published or other-
# wise divested of its trade secrets, irrespective of what has
# been deposited with the U.S. Copyright Office.
# **************************** End Copyright ***************************

import logging
import pickle
import os
import gzip
import sys

from autoai_ts_libs.utils.messages.messages import Messages
from sklearn.pipeline import Pipeline as sklearnPipeline
logger = logging.getLogger(__name__)
logger.setLevel('WARNING')
from autoai_ts_libs.sklearn.autoai_ts_pipeline import AutoaiTSPipeline
from autoai_ts_libs.utils.model_utils import Model_utils

class Score:

    PREDICT_SLIDING_WINDOW = 'sliding_window'
    PREDICT_FORECAST = 'forecast'

    @classmethod
    def get_estimator(cls, pipeline_obj):
        # in case of autoai pipeline return the pipeline
        #print('INPT PIPELINE=========================',pipeline_obj)
        #if isinstance(pipeline_obj, sklearnPipeline) and isinstance(pipeline_obj[-1], AutoaiTSPipeline)\
        #        and not isinstance(pipeline_obj, AutoaiTSPipeline):
        #    print("INTO WEIRED CONIDTION============", type(pipeline_obj))
        #    return pipeline_obj[-1]
        if isinstance(pipeline_obj,sklearnPipeline) and not isinstance(pipeline_obj, AutoaiTSPipeline):
            return cls.get_estimator(pipeline_obj[-1])
        elif isinstance(pipeline_obj, AutoaiTSPipeline) and isinstance(pipeline_obj[-1], AutoaiTSPipeline):
            # fix for backward compatibility issue #1672
            return cls.get_estimator(pipeline_obj[-1])
        else:
            return pipeline_obj

    @classmethod
    def get_lookback_win(cls, pipeline_obj):
        """
        Return lookback window
        
        """
        # obj = pipeline_obj
        # if isinstance(pipeline_obj, sklearnPipeline) and not isinstance(pipeline_obj, AutoaiTSPipeline):
        #     obj = pipeline_obj[-1]




        obj = cls.get_estimator(pipeline_obj)

        if isinstance(obj, AutoaiTSPipeline):
            return obj.steps[-1][-1].lookback_window

        if hasattr(obj, "lookback_win"):
            return obj.lookback_win
        else:
            return obj.lookback_window

    @classmethod
    def get_target_columns(cls, pipeline_obj):
        """
        Return a list of target columns in X_train/X_test
        Currently apply to SROM and Watfore only
        """
        # obj = pipeline_obj
        # if isinstance(pipeline_obj, sklearnPipeline) and not isinstance(pipeline_obj, AutoaiTSPipeline):
        #     obj = pipeline_obj[-1]

        obj = cls.get_estimator(pipeline_obj)

        if isinstance(obj, AutoaiTSPipeline):
            return obj.steps[-1][-1].target_columns
        # Valid with Watfore and SROM (TODO: check with AutoAI ppln):
        if hasattr(obj, "target_column_indices"): # Watfore
            return obj.target_column_indices
        else: # SROM
            return obj.target_columns

    @classmethod
    def get_feature_columns(cls, pipeline_obj):
        """
        Return a list of feature columns in X_train/X_test
        Currently apply to SROM and Watfore only
        """
        # obj = pipeline_obj
        # if isinstance(pipeline_obj, sklearnPipeline) and not isinstance(pipeline_obj, AutoaiTSPipeline):
        #     obj = pipeline_obj[-1]

        obj = cls.get_estimator(pipeline_obj)

        # Handle AutoaiTSPipeline
        if isinstance(obj, AutoaiTSPipeline):
            return obj.steps[-1][-1].feature_columns

        # Valid with Watfore and SROM (TODO: check with AutoAI ppln):
        if hasattr(obj, "feature_column_indices"): # Watfore
            return obj.feature_column_indices
        else: # SROM
            # SROM's MT2RForecaster has NO feature_columns
            # return obj.feature_columns if hasattr(obj, "feature_columns") else []
            if hasattr(obj, "feature_columns") and hasattr(obj, "look_ahead_fcolumns"):
                if obj.look_ahead_fcolumns is not None:
                    return obj.feature_columns + obj.look_ahead_fcolumns
                else:
                    return obj.feature_columns
            elif hasattr(obj, "feature_columns"):
                return obj.feature_columns
            else:
                return []
        

    @classmethod
    def get_prediction_win(cls, pipeline_obj):



        obj = cls.get_estimator(pipeline_obj)

        if isinstance(obj, AutoaiTSPipeline):
            return obj.steps[-1][-1].prediction_horizon
        if hasattr(obj, "prediction_win"):
            return obj.prediction_win
        elif hasattr(obj, "pred_win"):
            return obj.pred_win
        elif hasattr(obj, "prediction_horizon"):
            return obj.prediction_horizon
        else:
            return 1
    @classmethod
    def save(cls, pipeline_obj, file_path, verbose=False):
        save_status = False
        try:
            # WatFore piplines
            # if isinstance(pipeline_obj, ai4ml_ts.estimators.watfore_forecasters.WatForeForecaster) \
            #         or isinstance(pipeline_obj, ai4ml_ts.joint_optimizers.watfore_joint_optimizer.WatForeTimeSeriesJointOptimizer):
            #     pipeline_obj.export(file_path, verbose)  # save m model and close TSContext to java
            # else:  # Autoai or SROM
            # Watfore now supports pickle.dump and pickle.load
            file_path = file_path #+ '.pkl'
            # pickle.dump(pipeline_obj, open(file_path, 'wb'))
            pickle.dump(pipeline_obj, gzip.open(file_path, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

            if verbose:
                print('Saved model ', str(pipeline_obj),' to file ',file_path)
            save_status = True
        except Exception as e:
            logger.warning('Could not save pipeline',exc_info=False)

        del pipeline_obj

        return save_status

    @classmethod
    def load(cls,file_path,verbose = False):
        # from ai4ml_ts.estimators.watfore_forecasters import WatForeForecaster

        pipeline = None
        # wf_pkl_filename = wf.Accessors.make_watfore_save_filename(file_path) #+ '.pkl'
        #
        # if os.path.exists(wf_pkl_filename) and os.path.isfile(wf_pkl_filename):
        #     #load Watfore Models
        #     if verbose:
        #         print('Loading STATS Models from location ',file_path)
        #     pipeline = WatForeForecaster.load(file_path,verbose)
        # else:
            # srom,autoai
            # file_path = file_path #+ '.pkl'
        if verbose:
            print('Loading Model(s) from location ',file_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                # pipeline = pickle.load(open(file_path, 'rb'))
                pipeline = pickle.load(gzip.open(file_path, 'rb'))
            except Exception as e:
                error_msg = Messages.get_message(file_path, message_id='AUTOAITSLIBS0001E')
                logger.error(error_msg)
                raise Exception(error_msg)
            if pipeline is None:
                error_msg = Messages.get_message(file_path, message_id='AUTOAITSLIBS0002E')
                logger.error(error_msg)
                raise Exception(error_msg)

        else:
            error_msg = Messages.get_message(file_path, message_id='AUTOAITSLIBS0003E')
            logger.error(error_msg)
            raise Exception(error_msg)

        return pipeline

    @classmethod
    def get_model_type(cls, pipeline_obj):
        """
        Get pipeline type which is exogenous or non-exogenous
        Input:
            pipeline_obj: a pipeline object
        Output:
            pipeline type: 'exogenous'/'non-exogenous' (String)
        """
        is_exogenous_pipeline_ = False
        est = cls.get_estimator(pipeline_obj)

        if hasattr(est, "is_exogenous_pipeline_"):  # scrom and Wotefor has is_exogenous_pipeline property
            is_exogenous_pipeline_ = est.is_exogenous_pipeline_
        elif type(est) in [sklearnPipeline, AutoaiTSPipeline]:
            if hasattr(est, "steps"):  # Pipeline
                mvpttr = est.steps[-1][1]
            else:
                mvpttr = est
            pipeline_name, _ = Model_utils.get_names_from_autoai_estimator(mvpttr)
            if "Exogenous" in pipeline_name:
                is_exogenous_pipeline_ = True
                
        if is_exogenous_pipeline_:
            return "exogenous"
        else:
            return "non-exogenous"

