from profilehooks import timecall


@timecall(immediate=True)
def func_to_profile():
    pass
