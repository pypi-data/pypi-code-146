"""
This module contains related classes for monitoring the pipeline progress status.

The following class is available:

    * :class:`PipelineProgressStatusMonitor`
"""

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
# pylint: disable=protected-access, bare-except
# pylint: disable=no-else-continue
# pylint: disable=broad-except
# pylint: disable=superfluous-parens
import os
import threading
import time
import uuid
import logging
import pandas as pd
try:
    from IPython.core.display import display, update_display, Javascript
except ImportError as error:
    logging.getLogger(__name__).error("%s: %s", error.__class__.__name__, str(error))
    pass
try:
    from jinja2 import Environment, PackageLoader
except ImportError as error:
    logging.getLogger(__name__).error("%s: %s", error.__class__.__name__, str(error))
    pass
from hana_ml.dataframe import ConnectionContext
from hana_ml.visualizers.model_report import TemplateUtil
from hana_ml.visualizers.ui_components import HTMLFrameUtils


def get_tempdir_path():
    template_name = 'pipeline_progress.html'
    file_path = Environment(loader=PackageLoader('hana_ml.visualizers', 'templates')).get_template(template_name).filename
    temp_dir = file_path.replace(template_name, 'temp')
    if os.path.exists(temp_dir) is False:
        os.mkdir(temp_dir)
    return temp_dir


def create_interrupt_file(frame_id):
    file = open(get_tempdir_path() + os.sep + frame_id, 'w')
    file.close()


def build_frame_html(frame_id, frame_src, frame_height):
    frame_html = """
        <iframe
            id="{iframe_id}"
            width="{width}"
            height="{height}"
            srcdoc="{src}"
            style="border:1px solid #ccc"
            allowfullscreen="false"
            webkitallowfullscreen="false"
            mozallowfullscreen="false"
            oallowfullscreen="false"
            msallowfullscreen="false"
        >
        </iframe>
    """.format(
        iframe_id=frame_id,
        width='100%',
        height=frame_height,
        src=frame_src
    )

    return frame_html


def create_connection_context(original_connection_context: ConnectionContext) -> ConnectionContext:
    if original_connection_context.userkey is None:
        conn_str = original_connection_context.connection.__str__().replace('<dbapi.Connection Connection object : ', '')[:-1]
        if conn_str.count(',') >= 4:
            for i in range(0, conn_str.count(',') - 4):
                try:
                    url, remain_str = conn_str.split(',', 1)
                    port, remain_str = remain_str.split(',', 1)
                    user, remain_str = remain_str.split(',', 1)
                    password = remain_str.rsplit(',', i + 1)[0]
                    conn = ConnectionContext(url, port, user, password)
                    return conn
                except Exception as err:
                    if i < conn_str.count(',') - 5:
                        continue
                    else:
                        raise(err)
        conn_config = conn_str.split(',')
        url = conn_config[0]
        port = conn_config[1]
        user = conn_config[2]
        password = conn_config[3]
    try:
        if original_connection_context.userkey:
            conn = ConnectionContext(userkey=original_connection_context.userkey)
        else:
            conn = ConnectionContext(url, port, user, password)
    except:
        if original_connection_context.userkey:
            conn = ConnectionContext(userkey=original_connection_context.userkey, encrypt='true', sslValidateCertificate='false')
        else:
            conn = ConnectionContext(url, port, user, password, encrypt='true', sslValidateCertificate='false')
    return conn


class ProgressStatus(object):
    def __init__(self):
        self.progress_current_2_message = {}
        self.progress_current_2_status = {}
        self.base_progress_status = None

        self.data_columns_tuples = []
        self.data_columns_tuples_count = 0
        self.parse_data_columns_tuple_index = 0

        self.available_max_progress_current = -1
        self.read_progress_current = -1

        self.fetch_end = False

    def fetch_done(self):
        return self.fetch_end

    def get_next_progress_status(self):
        current_data_columns_tuples_count = self.data_columns_tuples_count
        for data_columns_tuple_index in range(self.parse_data_columns_tuple_index, current_data_columns_tuples_count):
            self.parse_data_columns_tuple(self.data_columns_tuples[data_columns_tuple_index])
        self.parse_data_columns_tuple_index = current_data_columns_tuples_count

        progress_current_status = None
        if self.available_max_progress_current > -1:
            if self.read_progress_current + 1 <= self.available_max_progress_current:
                next_progress_current = self.read_progress_current + 1
                progress_message = ''.join(self.progress_current_2_message.get(next_progress_current))
                if progress_message.strip() == '':
                    progress_message = 'None'
                progress_current_status = self.progress_current_2_status.get(next_progress_current)
                progress_current_status['PROGRESS_MESSAGE'] = progress_message
                self.read_progress_current = next_progress_current
                progress_current_status.update(self.base_progress_status)
                return progress_current_status

        return progress_current_status

    def parse_data_columns_tuple(self, data_columns_tuple):
        pandas_df = pd.DataFrame(data_columns_tuple[0], columns=data_columns_tuple[1])
        if self.base_progress_status is None:
            head_row = pandas_df.head(1)
            self.base_progress_status = {
                'PROGRESS_MAX': list(head_row['PROGRESS_MAX'])[0],
                'EXECUTION_ID': str(list(head_row['EXECUTION_ID'])[0]),
                'FUNCTION_NAME': str(list(head_row['FUNCTION_NAME'])[0]),
                'HOST': str(list(head_row['HOST'])[0]),
                'PORT': list(head_row['PORT'])[0],
                'CONNECTION_ID': str(list(head_row['CONNECTION_ID'])[0]),
                'PROGRESS_TIMESTAMP': str(list(head_row['PROGRESS_TIMESTAMP'])[0]),
            }

        row_count = pandas_df.shape[0]
        progress_current_list = list(pandas_df['PROGRESS_CURRENT'])
        progress_msg_list = list(pandas_df['PROGRESS_MESSAGE'])
        progress_elapsedtime_list = list(pandas_df['PROGRESS_ELAPSEDTIME'])
        for row_index in range(0, row_count):
            progress_current = progress_current_list[row_index]
            if progress_current >= 1:
                self.available_max_progress_current = progress_current - 1
            progress_msg = progress_msg_list[row_index]
            progress_elapsedtime = progress_elapsedtime_list[row_index]
            if self.progress_current_2_message.get(progress_current) is None:
                if progress_msg.strip() == '' or progress_msg is None:
                    progress_msg = 'None'
                self.progress_current_2_message[progress_current] = [progress_msg]
                self.progress_current_2_status[progress_current] = {
                    'PROGRESS_CURRENT': progress_current,
                    'PROGRESS_ELAPSEDTIME': progress_elapsedtime
                }
            else:
                self.progress_current_2_message[progress_current].append(progress_msg)

    def push_data_columns_tuple(self, data_columns_tuple):
        self.data_columns_tuples.append(data_columns_tuple)
        self.data_columns_tuples_count += 1


class ProgressStatusMonitorThread(threading.Thread):
    def __init__(self, connection_context, automatic_obj, interval):
        threading.Thread.__init__(self)
        self.done = False
        self.interrupted = False
        self.automatic_obj = automatic_obj
        self.progress_status = ProgressStatus()
        self.display_progress_status_timer = DisplayProgressStatusTimer(self, interval)
        self.fetch_progress_status_thread = FetchProgressStatusThread(self, connection_context)
        self.frame_file_path = self.display_progress_status_timer.frame_file_path
        self.connection_context_to_close_session = create_connection_context(connection_context)

    def is_interrupted(self):
        return self.interrupted

    def is_done(self):
        return self.done

    def run(self):
        self.automatic_obj._status = 0
        self.fetch_progress_status_thread.start()
        self.display_progress_status_timer.start()

        while True:
            time.sleep(1)
            if self.is_interrupted():
                break
            if self.is_done():
                break
            if os.path.exists(self.frame_file_path):
                # sql = "ALTER SYSTEM DISCONNECT SESSION '{}'"
                # sql = "ALTER SYSTEM CANCEL WORK IN SESSION '{}'"
                self.connection_context_to_close_session.execute_sql("ALTER SYSTEM CANCEL WORK IN SESSION '{}'".format(self.automatic_obj.fit_data.connection_context.connection_id))
                self.automatic_obj._status = -2
                self.connection_context_to_close_session.close()
                self.automatic_obj.progress_indicator_id = "cancelled_{}".format(self.automatic_obj.progress_indicator_id)

    def do_interrupt(self):
        self.interrupted = True

    def do_end(self):
        self.done = True


class FetchProgressStatusThread(threading.Thread):
    def __init__(self, manager: ProgressStatusMonitorThread, connection_context):
        threading.Thread.__init__(self)
        self.already_init = False
        self.manager = manager
        self.connection_context = connection_context
        self.cur = self.connection_context.connection.cursor()
        self.cur.setfetchsize(32000)
        self.target_columns1 = ['PROGRESS_CURRENT', 'PROGRESS_MESSAGE', 'PROGRESS_ELAPSEDTIME']
        self.target_columns2 = ['EXECUTION_ID', 'FUNCTION_NAME', 'HOST', 'PORT', 'CONNECTION_ID', 'PROGRESS_TIMESTAMP', 'PROGRESS_ELAPSEDTIME', 'PROGRESS_CURRENT', 'PROGRESS_MAX', 'PROGRESS_LEVEL', 'PROGRESS_MESSAGE']
        self.sql3 = "SELECT PROGRESS_CURRENT from _SYS_AFL.FUNCTION_PROGRESS_IN_AFLPAL WHERE EXECUTION_ID='{}'".format(self.manager.automatic_obj.progress_indicator_id)

    def get_data_columns_tuple(self, sql, target_columns):
        self.cur.execute(sql)
        return (self.cur.fetchall(), target_columns)

    def run(self):
        offset = 0
        limit = 1000
        while True:
            if self.manager.is_interrupted():
                break
            current_data_columns_tuple = None
            if self.already_init is True:
                current_data_columns_tuple = self.get_data_columns_tuple("SELECT PROGRESS_CURRENT, PROGRESS_MESSAGE, PROGRESS_ELAPSEDTIME from _SYS_AFL.FUNCTION_PROGRESS_IN_AFLPAL WHERE EXECUTION_ID='{}' limit {} offset {}".format(self.manager.automatic_obj.progress_indicator_id, limit, offset), self.target_columns1)
            else:
                current_data_columns_tuple = self.get_data_columns_tuple("SELECT * from _SYS_AFL.FUNCTION_PROGRESS_IN_AFLPAL WHERE EXECUTION_ID='{}' limit {} offset {}".format(self.manager.automatic_obj.progress_indicator_id, limit, offset), self.target_columns2)
            current_count = len(current_data_columns_tuple[0])
            if current_count == 0:
                if self.manager.is_done():
                    if len(self.get_data_columns_tuple(self.sql3, ['PROGRESS_CURRENT'])[0]) == 0:
                        break
            else:
                self.already_init = True
                self.manager.progress_status.push_data_columns_tuple(current_data_columns_tuple)
                offset = offset + current_count
        self.manager.progress_status.fetch_end = True
        self.connection_context.close()


class DisplayProgressStatusTimer(object):
    __TEMPLATE = TemplateUtil.get_template('pipeline_progress.html')

    def __init__(self, manager: ProgressStatusMonitorThread, interval):
        self.manager = manager
        self.interval = interval
        self.self_timer = None
        self.frame_id = '{}'.format(uuid.uuid4()).replace('-', '_').upper()
        self.temp_dir = get_tempdir_path()
        self.frame_file_path = self.temp_dir + os.sep + self.frame_id
        html_str = DisplayProgressStatusTimer.__TEMPLATE.render(
            executionId=self.manager.automatic_obj.progress_indicator_id,
            frameId=self.frame_id,
            highlighted_metric_name=self.manager.automatic_obj._get_highlight_metric())
        frame_src_str = HTMLFrameUtils.build_frame_src(html_str)
        self.frame_html = build_frame_html(self.frame_id, frame_src_str, '1000px')

    def display(self, js_str):
        display(Javascript("{}".format(js_str)), display_id=self.frame_id)

    def update_display(self, js_str):
        update_display(Javascript("{}".format(js_str)), display_id=self.frame_id)

    def generate_js_str(self, progress_status_str):
        js_str = "targetWindow['{}']={}".format(self.manager.automatic_obj.progress_indicator_id, progress_status_str)
        js_str = "for (let i = 0; i < window.length; i++) {const targetWindow = window[i];if(targetWindow['frameId']){if(targetWindow['frameId'] === '" + self.frame_id + "'){" + js_str + "}}}"
        return js_str

    def update_progress_status(self, progress_status):
        progress_status['pending'] = '__js_true'
        progress_status_str = str(progress_status).replace("'__js_true'", 'true')
        self.update_display(self.generate_js_str(progress_status_str))

    def delete_progress_status(self, progress_status):
        progress_status['pending'] = '__js_false'
        progress_status_str = str(progress_status).replace("'__js_false'", 'false')
        self.update_display(self.generate_js_str(progress_status_str))

    def __task(self):
        if self.manager.automatic_obj._status == -2:
            self.manager.do_interrupt()
            return
        if self.manager.automatic_obj._status == -1:
            self.manager.do_interrupt()
            self.update_display("document.getElementById('{}').style.display = 'none';".format(self.frame_id))
            return
        elif self.manager.automatic_obj._status == 1:
            self.manager.do_end()
        next_progress_status = self.manager.progress_status.get_next_progress_status()
        if next_progress_status is None:
            if self.manager.progress_status.fetch_done():
                self.delete_progress_status({})
            else:
                self.__run()
        else:
            self.update_progress_status(next_progress_status)
            self.__run()

    def __run(self):
        self.self_timer = threading.Timer(self.interval, self.__task)
        self.self_timer.start()

    def start(self):
        self.display("")
        HTMLFrameUtils.display(self.frame_html)
        self.self_timer = threading.Timer(self.interval, self.__task)
        self.self_timer.start()


class PipelineProgressStatusMonitor(object):
    """
    The instance of this class can monitor the progress of AutoML execution.

    Parameters
    ----------
    connection_context : :class:`~hana_ml.dataframe.ConnectionContext`
        The connection to the SAP HANA system.

        Please use a new connection to SAP HANA when you create a
        new PipelineProgressStatusMonitor object.

        For example:

        .. only:: latex

            >>> from hana_ml.dataframe import ConnectionContext as CC
            >>> progress_status_monitor = PipelineProgressStatusMonitor(connection_context=CC(url, port, user, pwd),
                                                                        automatic_obj=auto_c)

        .. raw:: html

            <iframe allowtransparency="true" style="border:1px solid #ccc; background: #eeffcb;"
                src="_static/automl_progress_example.html" width="100%" height="100%">
            </iframe>

    automatic_obj : :class:`~hana_ml.algorithms.pal.auto_ml.AutomaticClassification` or :class:`~hana_ml.algorithms.pal.auto_ml.AutomaticRegression`
        An instance object of the AutomaticClassification type or AutomaticRegression type
        that contains the progress_indicator_id attribute.

    interval : float, optional
        Specifies the time interval of updating the UI of pipeline progress.

        Defaults to 0.01s.

    Examples
    --------
    Create an AutomaticClassification instance:

    >>> progress_id = "automl_{}".format(uuid.uuid1())
    >>> auto_c = AutomaticClassification(generations=2,
                                         population_size=5,
                                         offspring_size=5,
                                         progress_indicator_id=progress_id)
    >>> auto_c.enable_workload_class("MY_WORKLOAD")

    Invoke a PipelineProgressStatusMonitor:

    >>> progress_status_monitor = PipelineProgressStatusMonitor(connection_context=dataframe.ConnectionContext(url, port, user, pwd),
                                                                automatic_obj=auto_c)
    >>> progress_status_monitor.start()
    >>> auto_c.fit(data=df_train)

    Output:

    .. image:: image/progress_classification.png

    """
    def __init__(self, connection_context: ConnectionContext, automatic_obj, interval=0.01):
        self.connection_context = create_connection_context(connection_context)
        self.automatic_obj = automatic_obj
        if self.automatic_obj.progress_indicator_id is None:
            self.automatic_obj.progress_indicator_id = "AutoML-{}".format(self.automatic_obj.gen_id)
        self.interval = interval

    def start(self):
        """
        Call the method before executing the fit method of AutomaticClassification or AutomaticRegression.
        """
        ProgressStatusMonitorThread(self.connection_context, self.automatic_obj, self.interval).start()
