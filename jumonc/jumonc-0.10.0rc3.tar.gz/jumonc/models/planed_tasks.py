import logging
from threading import Lock
from time import time
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from flask import jsonify
from flask import Response


logger = logging.getLogger(__name__)

__scheduled_tasks: List[Dict[str, Union[int, str]]] = []
__task_list_lock = Lock()

__task_max_id = 0
_new_task_callback: Optional[Callable] = None

def time_in_ms() -> int:
    return int(round(time()*1000))


def set_new_task_callback(callback: Callable) -> None:
    global _new_task_callback
    _new_task_callback = callback


def get_tasks_as_flask_json() -> Response:
    
    with __task_list_lock:
        if len(__scheduled_tasks) == 0:
            return jsonify("no tasks scheduled right now")
        return jsonify(__scheduled_tasks)


def get_next_task_and_time() -> Tuple[int, int, str]:
    waiting_time = 86400000 # one day in ms
    ID = 0
    task_str = ""
    with __task_list_lock:
        for task in __scheduled_tasks:
            this_waiting_time = int(task["exec_time_next"]) - time_in_ms()
            if this_waiting_time < waiting_time:
                waiting_time = this_waiting_time
                ID = int(task["id"])
                task_str = str(task["task"])
    return (waiting_time, ID, task_str)


def task_executed(ID: int, http_status: int, resultID: int) -> None:
    with __task_list_lock:
        for task in __scheduled_tasks:
            if task["id"] == ID:
                task["exec_time_last"] = time_in_ms()
                task["exec_time_next"] = int(task["exec_time_last"]) + int(task["interval_ms"])
                task["http_status"] = http_status
                task["result_last_id"] = resultID
                break


def task_last_result_id(ID: int) -> int:
    
    # do not search for invalid IDs
    if ID <= 0 or ID > __task_max_id:
        logger.debug("scheduling ID is not in a valid range")
        raise ValueError("wrong scheduling id supplied")
    with __task_list_lock:
        for task in __scheduled_tasks:
            if task["id"] == ID:
                return int(task["result_last_id"])
    raise ValueError("invalid scheduling id supplied")


def cancel(ID: int) -> bool:
    with __task_list_lock:
        removeTask: Optional[Dict[str, Union[int, str]]] = None
        for task in __scheduled_tasks:
            if task["id"] == ID:
                removeTask = task
                break
        if removeTask is not None:
            logger.debug("Removing a scheduled task")
            __scheduled_tasks.remove(removeTask)
            return True
        logger.debug("Not able to find scheduling task with this ID")
        return False


def addScheduledTask(task:str, interval:int) -> int:
    global __task_max_id
    
    with __task_list_lock:
        __task_max_id = __task_max_id + 1
        __scheduled_tasks.append({
            "id":                     __task_max_id,
            "task":                   task,
            "interval_ms":            interval,
            "result_last_id":         -1,
            "exec_time_last":         0,
            "exec_time_next":         0,
            "http_status":            100
            })
        if _new_task_callback is not None:
            _new_task_callback()
        else:
            logger.error("Needed Callback function for scheduling was not initialized")
        return __task_max_id
