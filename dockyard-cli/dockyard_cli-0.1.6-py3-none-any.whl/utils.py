
 
def catch_os_exec(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except FileNotFoundError as e:
            print(f"Please install {func.__name__} and try again.") 
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper