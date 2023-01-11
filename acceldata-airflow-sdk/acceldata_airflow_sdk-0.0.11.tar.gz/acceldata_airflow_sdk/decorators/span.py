import functools
import logging
from datetime import datetime
from acceldata_airflow_sdk.utils.torch_client import TorchDAGClient
from acceldata_sdk.events.generic_event import GenericEvent
from acceldata_airflow_sdk.utils.constants import PIPELINE_UID_XCOM, get_dag_run_pipeline_run_id, CONNECTION_ID

LOGGER = logging.getLogger("airflow.task")


def span(span_uid=None, associated_job_uids=None, xcom_to_event_mapper_ids=None):
    """
    Description:
        Used to decorate function for which you need span in side your pipeline. Just decorate your function with `span`
    :param xcom_to_event_mapper_ids: xcom pull ids that you want to send with span event
    :param associated_job_uids: list of string
    :param span_uid: uid of the span

    Example:

    @span(span_uid='customer.orders.datagen.span')
    def function(**context)

    """

    def decorator_span(func):
        @functools.wraps(func)
        def wrapper_span(*args, **kwargs):
            global xcom_context_data
            span_context = None
            try:
                LOGGER.info("Sending Span Start Event")
                if kwargs is None or kwargs.get('ti', None) is None:
                    raise Exception(f'Please pass context to function: {str(func.__name__)}')
                task_instance = kwargs['ti']
                pipeline_uid_ = task_instance.xcom_pull(key=PIPELINE_UID_XCOM)
                conn_id = task_instance.xcom_pull(key=CONNECTION_ID)
                xcoms = xcom_to_event_mapper_ids
                parent_span_context = task_instance.xcom_pull(key='parent_span_context')
                if parent_span_context is None:
                    LOGGER.debug('Sending new request to catalog to get parent span context')
                    client = TorchDAGClient(conn_id)
                    pipeline_run_id = get_dag_run_pipeline_run_id(task_instance)
                    parent_span_context = client.get_root_span(pipeline_uid=pipeline_uid_, pipeline_run_id=pipeline_run_id)
                    # task_instance.xcom_push(key="parent_span_context", value=parent_span_context)
                else:
                    LOGGER.debug('using xcom to get parent span context to send span event')
                associatedJobUids = associated_job_uids
                if span_uid is None:
                    fname_six = '{:.6}'.format(func.__name__)
                    temp_span_uid = f'{task_instance.task_id}_{fname_six}.span'
                else:
                    temp_span_uid = span_uid
                span_context = parent_span_context.create_child_span(uid=temp_span_uid,
                                                                     context_data={'time': str(datetime.now()),
                                                                                   'xcom_to_event_mapper_ids': xcoms},
                                                                     associatedJobUids=associatedJobUids)
                xcom_context_data = {}
                if xcoms is None:
                    xcoms = []
                else:
                    for key in xcoms:
                        value = task_instance.xcom_pull(key=key)
                        if value is not None:
                            xcom_context_data[key] = value
                kwargs['span_context_parent'] = span_context
                LOGGER.info('Xcom context data ', xcom_context_data)
                func(*args, **kwargs)
            except Exception as e:
                LOGGER.error("Sending Span End Event with status Failure")
                exception = e.__dict__
                LOGGER.error(exception)
                span_context.send_event(
                    GenericEvent(context_data={'status': 'error', 'error_data': str(e), 'time': str(datetime.now()),
                                               'exception_type': str(type(e).__name__)},
                                 event_uid=f'{temp_span_uid}.error.event'))
                span_context.failed(context_data=xcom_context_data)
                raise e
            else:
                LOGGER.info("Sending Span End event with status Success")
                span_context.end(context_data=xcom_context_data)

        return wrapper_span

    return decorator_span
