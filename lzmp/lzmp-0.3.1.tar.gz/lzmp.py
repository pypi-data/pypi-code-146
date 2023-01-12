"""
    Copyright 2022 Stéphane De Mita

    lzmp is a simple wrapper around the multiprocessing module,
    allowing the lazy programmer to run batches of processes.

    lzmp contains the class Pool which lets the user specify one or more
    callable objects (such as functions) along with lists of arguments
    to process. lzmp collects the return value of each call and return
    the whole lot as a list, keeping the original submission order. For
    a single type of callable, the standalone function run wraps the
    wrapper and allows one-line parallelization.

    lzmp is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    lzmp is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with lzmp.  If not, see <http://www.gnu.org/licenses/>.
"""

__version__ = '0.3.1'

import multiprocessing, random, queue

class Pool:
    """
    Class to run tasks in parallel. Can be used to run different
    functions at once.

    *max_threads* can be passed as an argument at object creation to
    limit the number of processes created simultaneously. Values below
    1 and ``None`` are ignored.
    """

    def __init__(self, max_threads=None):
        self._tasks = [] # the list of  functions to process
        self._queue = multiprocessing.Queue() # the queue used to collect return values
        self._idx = 0 # counter used to order results
        self.max_threads = max_threads

    @property
    def max_threads(self):
        """ maximum number of simultaneous processes """
        return self._max_threads

    @max_threads.setter
    def max_threads(self, max_threads):
        if max_threads is not None:
            if not isinstance(max_threads, int): raise TypeError
            if max_threads < 1: raise ValueError('max_threads must be None or positive')
        self._max_threads = max_threads

    def _wrapper(self, f, idx): # generates the function which will be actually sent to a subprocess
        def task(*args):
            self._queue.put((f(*args), idx)) # the task index is bound to its outcome
        return task

    def add(self, f, args):
        """
        Add a type of tasks.

        :param f: callable.
        :param args: iterable of arguments values (each as a list of tuples).
        """
        for arg in args:
            self._tasks.append((self._wrapper(f, self._idx), arg))
            self._idx += 1

    def _start(self):
        if len(self._waiting):
            p = self._waiting.pop(0)
            p.start()
            self._started.append(p)
            return True
        else:
            return False

    def run(self, final=None, final_args=None, shuffle=False, echo=False):
        """
        Run the requested tasks. If *shuffle* is true, the order of
        tasks is randomized. Return a list of return values of the
        called function (order is not altered by shuffling). If *final*
        is not ``None``, call this function on this list and return the
        result. The callable passed as *final* will receive the combined
        return values of the callable passed to :meth:`.Pool.add` as
        first argument and, if specified, *final_args* as second
        argument. If *echo* is set, the arguments (but not the callable)
        are returned along with the corresponding results, wrapped in
        two-item tuples ``(args, res)``. If arguments are all one-item
        tuples, they are unwrapped automatically. It is not possible to
        set both *final* and *echo*.

        .. versionchanged:: 0.2
            *echo* argument
        
        .. versionchanged:: 0.3
            close automatically terminated processes upon completion
        """
        if final and echo: raise ValueError("cannot set both final and echo arguments")
        if not len(self._tasks): return []
        self._waiting = [multiprocessing.Process(target=f, args=args) for (f, args) in self._tasks]
        if shuffle: random.shuffle(self._waiting)
        n = len(self._waiting)
        results = [None] * self._idx
        self._started = []
        if self._max_threads is None: nt = multiprocessing.cpu_count()
        else: nt = min(multiprocessing.cpu_count(), self._max_threads)
        for _ in range(nt):
            if not self._start():
                break
        c = 0
        err = 0
        returncodes = set()
        while c < n:
            try:
                res, idx = self._queue.get(timeout=1)
                c += 1
            except queue.Empty as e:
                if not returncodes <= {0}:
                    for p in self._started:
                        if p.exitcode is None: p.terminate()
                    err = 1
                    break
                continue
            results[idx] = res
            i = 0
            while i < len(self._started):
                if self._started[i].exitcode is not None:
                    returncodes.add(self._started[i].exitcode)
                    self._started[i].close()
                    del self._started[i]
                else:
                    i += 1
            self._start()
        if err:
            raise RuntimeError('at least one error occurred in parallelized processes: see details above')
        if final is not None:
            if final_args is not None: return final(results, final_args)
            else: return final(results)
        elif echo:
            args = [args for f, args in self._tasks]
            if set(map(len, args)) == {1}: return [(arg[0], res) for arg, res in zip(args, results)]
            else: return list(zip(args, results))
        else:
            return results

def run(f, args, final=None, final_args=None, max_threads=None, shuffle=False, echo=False):
    """
    Convenience function to parallelise a single type of tasks.

    :param f: callable (typically a function) to execute
    :param args: iterable of arguments (each one must be a sequence).
        :func:`.wrap` can generate a proper iterable out of a
        single-item iterable.
    :param final: optional callable (function) to apply to the list of
        results. See :meth:`.Pool.run` for details.
    :param final_args: arguments to pass to *final* if specified.
    :param max_threads: maximum number of process to run
        simultaneously.
    :param shuffle: randomly shuffle tasks. Will not affect the order
        or returned items.
    :param echo: return the arguments (but not the callable) along with
        the corresponding results, wrapped in two-item tuples
        ``(args, res)``. If arguments are all one-item tuples, they are
        unwrapped automatically. It is not possible to set both *final*
        and *echo*.
    :return: The list of return values of the passed iterable, or the
        return value of *final*, if specified.

    .. versionchanged:: 0.2
        *echo* argument
    """
    p = Pool(max_threads)
    p.add(f, args)
    return p.run(final, final_args, shuffle, echo)

def wrap(iterable, *extra):
    """
    Return a generator wherein each item yields by *iterable* is
    included as a single-item tuple. Constant *extra* arguments are
    appended to the tuple at each iteration round.

    .. versionchanged:: 0.3
        *extra* arguments
    """
    return ((i,) + extra for i in iterable)
