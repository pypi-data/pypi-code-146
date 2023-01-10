from robertcommonbasic.basic.exector.utils import Code


def run():
    src = """
    def fib(n):
        print(f"fib({n})")
        if n == 1 or n == 2:
            return 1
        print(f"fib1({n})")
        return fib(n-1) + fib(n-2)
    return fib(3)
    """
    module = Code(src)
    print(module.run_code())


def run2():
    src = """
    import time
    def fib(n):
        print(f"fib({n})")
        time.sleep(1)
        if n == 1 or n == 2:
            return 1
        print(f"fib1({n})")
        return fib(n-1) + fib(n-2)
    return fib(3)
    """
    module = Code(src, True)
    print(module.run_code())


def run21():
    src = """
    import time
    def fib(n):
        print(f"fib({n})")
        time.sleep(1)
        if n == 1 or n == 2:
            return 1
        print(f"fib1({n})")
        return fib(n-1) + fib(n-2)
    return fib(3)
    """
    module = Code(src, True)
    print(module.run_code())


def run1():
    src = """
def fib(n):
    print(f"fib({n})")
    if n == 1 or n == 2:
        return 1
    print(f"fib1({n})")
    return fib(n-1) + fib(n-2)
    """
    module = Code(src, False)
    print(module.run_code('fib', 2))


run2()