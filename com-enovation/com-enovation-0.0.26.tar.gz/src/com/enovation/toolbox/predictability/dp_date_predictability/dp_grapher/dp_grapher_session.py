from datetime import datetime
from inspect import stack
from logging import Logger, getLogger
from typing import Union

from com.enovation.toolbox.predictability.bean import PredictabilityBean
from dash.html import P


class Session:

    _logger: Logger = getLogger(__name__)

    # The Predictability bean to graph, as a global class instance
    _obj_cls_predictability_bean: PredictabilityBean

    # The zoomed Predictability bean to graph, as a global class instance
    # _obj_cls_zoomed_predictability_bean: PredictabilityBean
    # _str_cls_zoomed_key: str
    # _dt_cls_zoomed_date: datetime

    # The logged message, to be printed in the debug
    _lst_cls_debug_samp_children: list[P] = []

    @staticmethod
    def debug(debug_trace: Union[str, list[str]], session_id=None):
        Session._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called with parameter "
                              f"debug_trace of type '{type(debug_trace)}', with value '{debug_trace}'.")

        lst_the_list_of_traces: list[str]
        if isinstance(debug_trace, str):
            lst_the_list_of_traces = [debug_trace]
        else:
            lst_the_list_of_traces = debug_trace

        for i_str in lst_the_list_of_traces:
            Session._lst_cls_debug_samp_children.append(
                P(
                    f">> {debug_trace}",
                    className="m-0 m-0 p-0"
                )
            )
            Session._logger.info(f"{debug_trace}")

        Session._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

    @staticmethod
    def get_predictability_bean(session_id=None) -> PredictabilityBean:
        """
        Getter method for the instance of the predictability bean which has been loaded, and kept in the session.
        :param session_id:
        :return:
        """
        return Session._obj_cls_predictability_bean

    @staticmethod
    def set_predictability_bean(obj_predictability_bean: PredictabilityBean, session_id=None):
        """
        Getter method for the instance of the predictability bean which has been loaded, and kept in the session.
        :param obj_predictability_bean:
        :param session_id:
        :return:
        """
        Session._obj_cls_predictability_bean = obj_predictability_bean

    @staticmethod
    def get_debug(session_id=None) -> list[P]:
        """
        Getter method for the debug messages that the application append into the property _lst_cls_debug_samp_children.
        :param session_id:
        :return:
        """
        return Session._lst_cls_debug_samp_children

    # @staticmethod
    # def set_zoom(obj_zoomed_predictability_bean: PredictabilityBean, str_zoomed_key: str, dt_zoomed_date: datetime):
    #     Session._obj_cls_zoomed_predictability_bean = obj_zoomed_predictability_bean
    #     Session._str_cls_zoomed_key = str_zoomed_key
    #     Session._dt_cls_zoomed_date = dt_zoomed_date
    #
    # @staticmethod
    # def get_zoom() -> tuple[PredictabilityBean, str, datetime]:
    #     return Session._obj_cls_zoomed_predictability_bean, Session._str_cls_zoomed_key, Session._dt_cls_zoomed_date
    #
    # @staticmethod
    # def reset_zoom():
    #     Session._obj_cls_zoomed_predictability_bean = None
    #     Session._str_cls_zoomed_key = None
    #     Session._dt_cls_zoomed_date = None
    #
    # @staticmethod
    # def is_zoom():
    #     if Session._obj_cls_zoomed_predictability_bean is None:
    #         return False
    #     return True
