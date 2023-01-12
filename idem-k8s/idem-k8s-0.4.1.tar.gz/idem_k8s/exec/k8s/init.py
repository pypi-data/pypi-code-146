"""
This plugin provides an interface for interacting with the k8s python API using idem's acct system and CLI paradigm.

All underlying calls are done asynchronously in a Threadpool Executor
"""


def __init__(hub):
    # Provides the ctx argument to all execution modules
    # which will have profile info from the account module
    hub.exec.k8s.ACCT = ["k8s"]

    # Load dynamic subs for accessing k8s python clients
    hub.pop.sub.dynamic(
        sub=hub.exec.k8s,
        subname="client",
        resolver=hub.tool.k8s.resolve.client,
        context=None,
    )
