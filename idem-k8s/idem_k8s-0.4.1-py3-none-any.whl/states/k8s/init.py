def __init__(hub):
    # Provides the ctx argument to all state modules
    # which will have profile info from the account module
    hub.states.k8s.ACCT = ["k8s"]
