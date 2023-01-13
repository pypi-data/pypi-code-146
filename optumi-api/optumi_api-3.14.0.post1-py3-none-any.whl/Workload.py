##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi

from .CloudStorage import CloudStorage
from .CloudFileVersion import CloudFileVersion
from .Log import Log
from .Summary import Summary
from .Program import Program
from .Machine import Machine
from .utils import *

import json, time, os, re
from sys import exit

from enum import Enum


class Status(Enum):
    QUEUED = "queued"
    LAUNCHING = "launching"
    RUNNING = "running"
    COMPLETED = "completed"


class Progress(Enum):
    SILENT = "silent"
    # STATUS = "status"
    SUMMARY = "summary"
    DETAIL = "detail"


class Workload:
    def __init__(
        self,
        path: str,
        program: str,
        workload_uuid: str,
        module_uuid: str,
        nb_config: dict,
        run_num: str,
        initializing_lines: list = [],
        preparing_lines: list = [],
        running_lines: list = [],
        input_files: list = [],
        update_lines: list = [],
        output: list = [],
        num_patches: int = 0,
        output_files: list = [],
        machine: Machine = None,
        token: str = None,
    ):
        self._path = path
        self._program = program

        self._workload_uuid = workload_uuid
        self._module_uuid = module_uuid

        self._nb_config = nb_config

        self._run_num = run_num

        self._initializing_lines = initializing_lines.copy()
        self._preparing_lines = preparing_lines.copy()
        self._running_lines = running_lines.copy()
        self._input_files = []

        self._update_lines = update_lines.copy()
        self._output = output.copy()
        self._last_patches = num_patches

        self._output_files = output_files.copy()

        self._machine = machine
        self._token = token

        self._last_refresh = time.time()

    @classmethod
    def reconstruct(cls, app_map):
        # Reconstruct the app
        initializing = []
        for i in range(len(app_map["initializing"])):
            initializing.append(
                (app_map["initializing"][i], app_map["initializingmod"][i])
            )

        preparing = []
        for i in range(len(app_map["preparing"])):
            preparing.append((app_map["preparing"][i], app_map["preparingmod"][i]))

        running = []
        for i in range(len(app_map["running"])):
            running.append((app_map["running"][i], app_map["runningmod"][i]))

        input_files = []
        if "files" in app_map:
            for i in range(len(app_map["files"])):
                if app_map["files"][i] != "":
                    input_files.append(
                        CloudFileVersion(
                            app_map["files"][i],
                            app_map["hashes"][i],
                            int(app_map["filessize"][i]),
                            app_map["filescrt"][i],
                            app_map["filesmod"][i],
                        )
                    )

        module_uuid = None
        output = []
        updates = []
        output_files = []
        num_patches = 0
        program = None
        machine = None
        token = None

        # Add modules
        for module in app_map["modules"]:
            module_uuid = module["uuid"]

            if "output" in module:
                for i in range(len(module["output"])):
                    output.append((module["output"][i], module["outputmod"][i]))

            if "updates" in module:
                for i in range(len(module["updates"])):
                    updates.append((module["updates"][i], module["updatesmod"][i]))

            if "files" in module:
                for i in range(len(module["files"])):
                    if module["files"][i] != "":
                        output_files.append(
                            CloudFileVersion(
                                module["files"][i],
                                module["hashes"][i],
                                int(module["filessize"][i]),
                                module["filescrt"][i],
                                module["filesmod"][i],
                            )
                        )

            # monitoring = []
            # if 'monitoring' in module:
            #     for i in range(len(module['monitoring'])):
            #         monitoring.append((module['monitoring'][i], module['monitoringmod'][i]))

            if "patches" in module:
                num_patches = len(module["patches"])

            if "notebook" in module:
                program = module["notebook"]

            if "machine" in module:
                machine = Machine(*Machine.reconstruct(module["machine"]))

            if "token" in module:
                token = module["token"]

        return (
            app_map["name"],
            program,
            app_map["uuid"],
            module_uuid,
            json.loads(app_map["nbConfig"]),
            app_map["runNum"],
            initializing,
            preparing,
            running,
            input_files,
            updates,
            output,
            num_patches,
            output_files,
            machine,
            token,
        )

    def _refresh(self):
        now = time.time()
        if now - self._last_refresh > 5:
            self._last_refresh = now
            user_information = json.loads(optumi.core.get_user_information(True).text)
            # Add apps from user information if they don't already exist
            if "jobs" in user_information:
                for app_map in user_information["jobs"]:
                    if app_map["uuid"] == self._workload_uuid:
                        (
                            _,
                            _,
                            _,
                            _,
                            _,
                            _,
                            self._initializing_lines,
                            self._preparing_lines,
                            self._running_lines,
                            self._input_files,
                            self._update_lines,
                            self._output,
                            self._last_patches,
                            self._output_files,
                            self._machine,
                            self._token,
                        ) = Workload.reconstruct(app_map)

    # def __print_status(self):
    #     collapsed = collapseUpdates(
    #         self._initializing_lines + self._preparing_lines + self._running_lines
    #     ).split("\n")
    #     line = collapsed[-1] if collapsed[-1] != "" else collapsed[-2]
    #     print("\b" * self._last_line_length, end="")
    #     print(" " * self._last_line_length, end="")
    #     print("\b" * self._last_line_length, end="")
    #     self._last_line_length = len(line)
    #     print(line, end="", flush=True)
    #     time.sleep(0.3)

    def __print_output(self, progress, output_to_print):
        if progress == Progress.DETAIL:
            for output in output_to_print:
                print(output[0], end="")

    def __print_updates(self, progress, updates_to_print):
        for update in updates_to_print:
            if (
                re.sub("[^a-zA-Z]", "", update[0]) != ""
                and update[0] != "\n"
                and update[0] != "stop"
                and update[0] != "error"
            ):
                if progress == Progress.SUMMARY:
                    print(
                        update[0]
                        if update[0].endswith("\n")
                        else self.__adjust_message(update[0]) + "\n",
                        end="",
                        flush=True,
                    )
                # elif progress == Progress.STATUS:
                #     self.__print_status()

    def wait(self, progress=Progress.SUMMARY):
        self._last_line_length = 0

        self.__print_output(progress, self._output)
        self.__print_updates(
            progress,
            self._initializing_lines + self._preparing_lines + self._running_lines,
        )

        while True:
            updates = json.loads(
                optumi.pull_workload_status_updates(
                    [self._workload_uuid],
                    [len(self._initializing_lines)],
                    [len(self._preparing_lines)],
                    [len(self._running_lines)],
                ).text
            )[self._workload_uuid]

            updates_to_print = []

            new_preparing = updates["preparing"]
            new_preparing_mod = updates["preparingmod"]
            for i in range(len(new_preparing)):
                update = new_preparing[i]
                update_mod = new_preparing_mod[i]
                self._preparing_lines.append((update, update_mod))
                updates_to_print.append(self._preparing_lines[-1])

            new_running = updates["running"]
            new_running_mod = updates["runningmod"]
            for i in range(len(new_running)):
                update = new_running[i]
                update_mod = new_running_mod[i]
                self._running_lines.append((update, update_mod))
                updates_to_print.append(self._running_lines[-1])

            self.__print_updates(progress, updates_to_print)

            if self._module_uuid:
                updates = json.loads(
                    optumi.pull_module_status_updates(
                        [self._workload_uuid],
                        [self._module_uuid],
                        [len(self._update_lines)],
                        [len(self._output)],
                        [0],
                        [self._last_patches],
                    ).content
                )[self._module_uuid]

                new_updates = updates["updates"]
                new_updates_mod = updates["updatesmod"]
                for i in range(len(new_updates)):
                    self._update_lines.append((new_updates[i], new_updates_mod[i]))

                output_to_print = []

                new_output = updates["output"]
                new_output_mod = updates["outputmod"]
                for i in range(len(new_output)):
                    update = new_output[i]
                    self._output.append((update, new_output_mod[i]))
                    output_to_print.append(self._output[-1])

                self.__print_output(progress, output_to_print)

                if "patches" in updates:
                    new_patches = updates["patches"]
                    self._last_patches += len(new_patches)

                self._output_files = CloudStorage(
                    [
                        CloudFileVersion(
                            updates["files"][i],
                            updates["hashes"][i],
                            int(updates["filessize"][i]),
                            updates["filescrt"][i],
                            updates["filesmod"][i],
                        )
                        for i in range(len(updates["files"]))
                    ]
                )

                if "machine" in updates:
                    self._machine = Machine(*Machine.reconstruct(updates["machine"]))

                if self._token == None and "token" in updates:
                    self._token = updates["token"]
                    print(
                        "Session available at: https://"
                        + self._machine.dns_name
                        + ":54321/?token="
                        + self._token
                    )
                    return

            if self.__get_status() == Status.COMPLETED:
                break

            time.sleep(5)

        # if progress == Progress.STATUS:
        #     print()

    def stop(self, wait=True):
        from .Workloads import Workloads

        if (
            optumi.login.is_dynamic()
            and Workloads.current()._workload_uuid == self._workload_uuid
        ):
            print("Stopping current workload")
            # This is for sessions
            code = os.system("jupyter lab stop 54321")
            if code > 15:  # 15 is SIGTERM
                # This is for jobs
                exit(0)
        else:
            print("Stopping workload " + self.name + "...")
            if self.status != Status.COMPLETED:
                optumi.core.stop_notebook(
                    self._workload_uuid, None
                )  # Remove the second argument when we move to 3.14
                if wait and self.status == Status.RUNNING:
                    self.wait(progress=Progress.SILENT)
            print("...completed")

    def remove(self, wait=True):
        # TODO: Add an override flag to stop workload before removing
        if self.status != Status.COMPLETED:
            self.stop()
        print("Removing workload " + self.name + "...")
        optumi.core.teardown_notebook(
            self._workload_uuid, None
        )  # Remove the second argument when we move to 3.14
        print("...completed")

    @property
    def status(self):
        self._refresh()
        return self.__get_status()

    def __get_status(self):
        if len(self._preparing_lines) == 0:
            for update in self._initializing_lines:
                if Workload.__is_error(update):
                    return Status.COMPLETED

        if len(self._running_lines) == 0:
            for update in self._preparing_lines:
                if Workload.__is_error(update) or Workload.__is_terminated(update):
                    return Status.COMPLETED

        if len(self._update_lines) > 0:
            running = True
            for update in self._update_lines:
                if update[1] == "stop":
                    running = False
            if running:
                return Status.RUNNING

        for update in self._running_lines:
            if Workload.__is_stop(update):
                return Status.COMPLETED

        for update in self._preparing_lines:
            if Workload.__is_stop(update):
                return Status.RUNNING

        return Status.LAUNCHING

    def __adjust_message(self, message):
        # We will say a session is starting until we can connect to it
        if (
            self._nb_config["interactive"]
            and message == "Running"
            and self._token == None
        ):
            return "Connecting"
        # We call a running app 'Connected'
        if self._nb_config["interactive"] and message == "Running":
            return "Connected"
        # We call a terminated or completed app 'closed',
        if self._nb_config["interactive"] and message == "Terminating":
            return "Closing"
        if self._nb_config["interactive"] and message == "Terminated":
            return "Closed"
        if self._nb_config["interactive"] and message == "Completed":
            return "Closed"
        return message

    @property
    def detailed_status(self):
        self._refresh()

        message = ""
        if Workload.__message(self._initializing_lines) != "":
            message = Workload.__message(self._initializing_lines)
        if Workload.__message(self._preparing_lines) != "":
            message = Workload.__message(self._preparing_lines)
        if Workload.__message(self._running_lines) != "":
            message = Workload.__message(self._running_lines)

        failed_message = "Failed"

        for update in self._initializing_lines:
            if Workload.__is_error(update):
                message = failed_message
            break

        for update in self._preparing_lines:
            if Workload.__is_error(update):
                message = failed_message
            break

        for update in self._running_lines:
            if Workload.__is_error(update):
                message = failed_message
            break

        for update in self._update_lines:
            if update[1] == "error":
                message = failed_message
                break

        return message

    @classmethod
    def __is_error(cls, update):
        line = update[0]
        modifier = update[1]
        if line == "error":
            return True
        if line != "error" and line != "stop" and line != "":
            if modifier.startswith("{"):
                jsonPayload = json.loads(modifier)
                if jsonPayload["level"] == "error":
                    return True
        return False

    @classmethod
    def __is_stop(cls, update):
        return update[0] == "stop"

    @classmethod
    def __is_terminated(cls, update):
        return update[0] == "Terminated"

    @classmethod
    def __message(cls, updates):
        for update in reversed(updates):
            line = update[0]
            modifier = update[1]
            if (
                line != "error"
                and line != "stop"
                and line != ""
                and not modifier.startswith("{")
            ):
                return line
        return ""

    @property
    def log(self):
        self._refresh()
        return Log(self._path, self._output)

    @property
    def summary(self):
        self._refresh()
        return Summary(
            self._path,
            self._initializing_lines,
            self._preparing_lines,
            self._running_lines,
        )

    @property
    def program(self):
        self._refresh()
        return Program(self._path, self._run_num, self._program)

    @property
    def input_files(self):
        self._refresh()
        return self._input_files

    @property
    def output_files(self):
        self._refresh()
        return self._output_files

    @property
    def name(self):
        return self._path.split("/")[-1] + " (Run #" + str(self._run_num) + ")"

    @property
    def path(self):
        return optumi.utils.normalize_path(self._path, strict=False)

    @property
    def machine(self):
        return self._machine

    def __str__(self):
        return str(self.name)
