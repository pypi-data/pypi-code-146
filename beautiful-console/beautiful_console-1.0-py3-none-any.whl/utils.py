def end_point(beautiful_console):
    def wrapper(*args, **kwargs):
        if "get_input" in kwargs.keys():
            if kwargs["get_input"] is True:
                try:
                    text = input(beautiful_console(*args, **kwargs))
                except KeyboardInterrupt:
                    exit()
                else:
                    return text
                finally:
                    print("\u001b[0m")
        return beautiful_console(*args, **kwargs)
    return wrapper
