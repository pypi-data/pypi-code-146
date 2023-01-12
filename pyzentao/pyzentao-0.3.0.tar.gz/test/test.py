# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2021-07-15
#


import time
from pyzentao import Zentao


if "__main__" == __name__:
    zentao = Zentao({
        # zentao root url
        "url": "http://0.0.0.0:21761/zentao",
        "version": "17.6",

        # "url": "http://0.0.0.0:21650/zentao",
        # "version": "16.5",

        # "url": "http://0.0.0.0:21250/zentao",
        # "version": "12",

        # authentication
        "username": "admin",
        "password": "Lton2008@",
    })

    # - use task -
    # response = zentao.user_task(
    #     userID=1,
    #     type="assignedTo",
    #     # raw=True
    # )

    # - project create -
    # response = zentao.project_create(
    #     productID="1",
    #     projectID="0",
    #     copyProjectID="2",
    # )

    # - task create -
    response = zentao.task_create(
        executionID=2,
        storyID=0,
        moduleID=0,
        data={
            "execution": 2,
            "type": "test",
            "name": "task-锦囊喵叽-%s" % time.strftime("%Y-%m-%d-%H-%M-%S"),
            "assignedTo[]": "admin",
            "pri": 3,
            "desc": "指派任务暴打小柯基-%s" % time.strftime("%Y-%m-%d-%H-%M-%S")
        },
    )

    # response = zentao.task_create(
    #     projectID=3,
    #     storyID=0,
    #     moduleID=0,
    #     data={
    #         "project": 3,
    #         "type": "design",
    #         "name": "task-锦囊喵叽-%s" % time.strftime("%Y-%m-%d-%H-%M-%S"),
    #         "assignedTo[]": "admin",
    #         "pri": 3,
    #         "desc": "指派任务暴打小柯基-%s" % time.strftime("%Y-%m-%d-%H-%M-%S")
    #     },
    # )

    # - task create -
    # response = zentao.task_edit(
    #     taskID=1,
    #     data={
    #         "project": 3,
    #         "type": "design",
    #         "name": "task-锦囊喵叽",
    #         "assignedTo": "admin",
    #         "pri": 3,
    #         "desc": "desc-指派任务暴打小柯基"
    #     },
    # )

    print(">" * 30)
    print(response)
    print("<" * 30)


# end
