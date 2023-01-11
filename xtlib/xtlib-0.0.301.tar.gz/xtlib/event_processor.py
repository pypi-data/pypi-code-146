#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# event_processor.py: support for processing job/node/run events and associated notification

import ast
import time

from xtlib import utils
from xtlib import cs_utils
from xtlib import console
from xtlib import run_helper

def get_ids_from_python_expression(expression):
    '''
    parse python expression, but return dotted id's joined together
    '''
    tree = ast.parse(expression)
    id_list = []

    for node in ast.walk(tree):
        if type(node) is ast.Attribute:
            attribute = node.attr

        elif type(node) is ast.Name:
            if attribute:
                col = node.id + "." + attribute
                attribute = None
            else:
                col = node.id
            id_list.append(col)

    return id_list

class EventProcessor():
    
    def __init__(self, ws_name, job_id, node_index) -> None:
        self.ws_name = ws_name
        self.job_id = job_id
        self.node_index = node_index

        # "time started" columns for job, node, run
        self.started_dict = {"job": None, "node": "app_start_time", "run": "started"}

        # "time created" columns for job, node, run
        self.created_dict = {"job": None, "node": "create_time", "run": "created"}

        week_secs = 7*24*3600
        self.time_factors = {"ms": .001, "secs": 1, "mins": 60, "hours": 3600, "days": 24*3600, "weeks": week_secs, "months": 52/12*week_secs, "years": 52*365}

    def add_needed_col(self, cols_needed, col, ev_type):
        # support for dynamic columns
        if col == "queued":
            col = self.created_dict[ev_type]

        elif col == "duration":
            col = self.started_dict[ev_type]
        
        if col and (not col in self.time_factors):
            cols_needed[col] = 1

    def get_cols_from_condition(self, cols_needed, condition, ev_type):
        if condition:
            
            # allow any python expression, so we need python to parse exp
            id_list = get_ids_from_python_expression(condition)
            for id in id_list:
                self.add_needed_col(cols_needed, id, ev_type)                    

    def eval_expression(self, expression, col_vals, ev_type):
        value = None

        if expression:
            # support for dynamic columns
            if "queued" in expression:
                new_exp = "(now-{})".format(self.created_dict[ev_type])
                expression = expression.replace("queued", new_exp)

            if "duration" in expression:
                new_exp = "(now-{})".format(self.started_dict[ev_type])
                expression = expression.replace("duration", new_exp)

            expression = expression.replace("metrics.", "").replace("hparams.", "")

            # convert units to seconds
            val_dict = {**self.time_factors, **col_vals}

            # add "now" for time
            val_dict["now"] = time.time()

            # convert time fields to seconds
            started_col = self.started_dict[ev_type]
            created_col = self.created_dict[ev_type]

            for col in [started_col, created_col]:
                if col and col in val_dict:
                    value = val_dict[col]
                    new_value = utils.get_time_from_arrow_str(value)
                    val_dict[col] = new_value

            # evaluate
            try:
                value = eval(expression, val_dict)
            except BaseException as ex:
                console.print("exception during eval of '{}': {}".format(expression, ex))

        return value

    def test_condition(self, condition, col_vals, ev_type):
        # how to deal with time units ("5.3 hours", etc.)
        match = True

        if condition:
            value = self.eval_expression(condition, col_vals, ev_type)
            match = bool(value)

        return match

    def build_notify_report(self, report, col_vals, ev_type):
        text = ""

        for col in report:

            value = self.eval_expression(col, col_vals, ev_type)
            if value is None:
                value = "<unknown>"

            elif col in ["duration", "queued"]:
                value = utils.friendly_duration_format(value, True)
                
            else:
                value = str(value)

            text += "<b>{}</b>: {}<br>".format(col, value)
        
        return text

    def gather_columns_for_event(self, all_cols_needed, event_dict):
        ev_type = event_dict["type"]
        cols_needed = all_cols_needed[ev_type]

        ev_if = utils.safe_value(event_dict, "if")
        self.get_cols_from_condition(cols_needed, ev_if, ev_type)

        ev_report = utils.safe_value(event_dict, "report")
        for col in ev_report:
            self.add_needed_col(cols_needed, col, ev_type)                    

    def get_values_from_rows(self, all_col_values, all_key, rows, needed_cols):
        if rows:
            value_dict = rows[0] 

            run_helper.flatten_prop(value_dict, "metrics")
            run_helper.flatten_prop(value_dict, "hparams")

            # flatten names in needed_cols
            flat_needed_cols = [col.split(".")[-1] for col in needed_cols]

            all_col_values[all_key] = {col:value for col, value in value_dict.items() if col in flat_needed_cols}

    def get_column_values(self, store, all_cols_values, all_cols_needed, run_name):

        for ev_type in ["job", "node", "run"]:

            if all_cols_needed[ev_type]:
                type_cols = all_cols_needed[ev_type]
                #console.print("  get_column_values(): ev_type: {}, needed: {}".format(ev_type, type_cols))
                
                using_run_name_arg = False
                if run_name and "run_name" in type_cols:
                    del type_cols["run_name"]
                    using_run_name_arg = True

                if ev_type == "job":
                    filter_dict = {"job_id": self.job_id}
                    type_rows = store.database.get_info_for_jobs(self.ws_name, filter_dict, type_cols)

                elif ev_type == "node":
                    filter_dict = {"job_id": self.job_id, "node_index": self.node_index}
                    type_rows = store.database.get_info_for_nodes(self.ws_name, filter_dict, type_cols)

                else:   # ev_type == "run"
                    filter_dict = {"job_id": self.job_id, "run_name": run_name}
                    type_rows = store.database.get_info_for_runs(self.ws_name, filter_dict, type_cols)

                self.get_values_from_rows(all_cols_values, ev_type, type_rows, type_cols)

                if using_run_name_arg:
                    all_cols_values[ev_type]["run_name"] = run_name


    def process_notifications(self, store, context, current_event_when, run_name=None):
        #console.print("processing notifications for current_event_when: {}, run_name: {}".format(current_event_when, run_name))

        config_events = context.config_events
        job_events = context.job_events
        username = context.username
        notify_list = context.notify_list 

        all_cols_needed = {"job": {}, "node": {}, "run": {}}

        # on first pass, we just gather columns used in job_events
        for event_name in job_events:
            event_dict = config_events[event_name]
            if event_dict["when"] != current_event_when:
                continue

            if event_dict["notify_count"] >= event_dict["max_notify_count"]:
                continue

            self.gather_columns_for_event(all_cols_needed, event_dict)

        # now, get the values for needed columns
        all_cols_values = {"job": {}, "node": {}, "run": {}}
        self.get_column_values(store, all_cols_values, all_cols_needed, run_name)

        # finally, apply column values to event processing
        for event_name in job_events:
            if event_dict["when"] != current_event_when:
                continue

            if event_dict["notify_count"] >= event_dict["max_notify_count"]:
                continue

            event_dict = config_events[event_name]

            ev_type = event_dict["type"]
            col_vals = all_cols_values[ev_type]
            condition = utils.safe_value(event_dict, "if")
            match = self.test_condition(condition, col_vals, ev_type)
            #console.print("  event: {}, match: {}".format(event_name, match))
            if not match:
                continue

            self.send_event_notification(context, event_dict, notify_list, username, event_name, all_cols_values)

            # count this notification
            event_dict["notify_count"] += 1

    def send_event_notification(self, context, event_dict, notify_list, username, event_name, col_values):
        #console.print("  sending event notification for: {}".format(event_name))

        subject = utils.safe_value(event_dict, "title")
        report = utils.safe_value(event_dict, "report")

        if not notify_list:
            notify_list = [username]

        if not subject:
            subject = event_name + " notification"

        ev_type = event_dict["type"]
        col_vals = col_values[ev_type]

        msg = self.build_notify_report(report, col_vals, ev_type)

        email_cs = context.email_cs
        email_from = context.email_from
        sms_cs = context.sms_cs
        sms_from = context.sms_from

        to_contacts = []
        for nl in notify_list:
            contacts = cs_utils.get_contacts(context.team_dict, nl)
            to_contacts += contacts

        cs_utils.send_to_contacts(email_cs, email_from, sms_cs, sms_from, to_contacts, None, subject, msg)

def test():
    # testing is crucial here since its slow and painful to debug the controller (running on remote compute node)
    from xtlib.helpers import xt_config
    from xtlib.storage.store import Store

    class Bag(): pass

    config = xt_config.get_merged_config()
    store = Store(config=config)  
    username = config.get("general", "username")

    context = Bag()
    context.config_events = config.get("events")
    context.team_dict = config.get("team")
    context.job_events = ["perfect-train-acc"]    # ["start-of-odd-node"]
    context.notify_list = [username]
    context.username = username

    # expand config_event to include a "notify_count" property
    for event in context.config_events.values():
        event["notify_count"] = 0
        event["max_notify_count"] = 1

    context.email_cs = config.get("external-services", "xt-email", "connection-string")
    context.email_from = config.get("external-services", "xt-email", "from")
    context.sms_cs = config.get("external-services", "xt-sms", "connection-string")
    context.sms_from = config.get("external-services", "xt-sms", "from")

    ep = EventProcessor("ws4", "job1159", node_index=0)

    ep.process_notifications(store, context, "log_run", "run1159.1")

if __name__ == "__main__":
    test()