from tendo.singleton import SingleInstance, SingleInstanceException

from sleepytime.gui import run

if __name__ == "__main__":
    # you must give a var for SingleInstance to live in... otherwise
    # __del__ is likely to get called in it and delete the instance file.
    try:
        t = SingleInstance()
    except SingleInstanceException:
        raise RuntimeError(
            "Another instance of sleepytime is already running, quitting."
        )

    run()
