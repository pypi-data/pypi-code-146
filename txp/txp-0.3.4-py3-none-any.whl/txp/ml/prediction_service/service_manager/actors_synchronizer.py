import ray


@ray.remote
class ActorsStack:
    """ This class is used to keep track of running actors in the service.
    In order to shut down prediction service correctly we need to shut it down when no processes
    are running.
    This class provides 2 decorators.

    stateful_method: use this decorator whenever the method of an actor is called and you want it
    method to be stateful.

    stateful_function: use this decorator when you want to make a ray remote function stateful
    """
    def __init__(self):
        self.running_actors = 0

    def push(self):
        self.running_actors += 1

    def get_running_actors_count(self):
        return self.running_actors

    def pop(self):
        if self.running_actors:
            self.running_actors -= 1
        else:
            raise Exception("Trying to remove an actor from stack but stack is empty")


def stateful_method(func):
    def inner(self, *args, **kwargs):
        if 'actors_stack' in kwargs:
            stack = kwargs['actors_stack']
            stack.push.remote()
            kwargs.pop('actors_stack')
            try:
                ret = func(self, *args, **kwargs)
                stack.pop.remote()
            except Exception as e:
                stack.pop.remote()
                raise e
        else:
            ret = func(self, *args, **kwargs)
        return ret
    return inner


def stateful_function(func):
    def inner(*args, **kwargs):
        if 'actors_stack' in kwargs:
            stack = kwargs['actors_stack']
            stack.push.remote()
            try:
                ret = func(*args, **kwargs)
                stack.pop.remote()
            except Exception as e:
                stack.pop.remote()
                raise e
        else:
            ret = func(*args, **kwargs)
        return ret
    return inner
