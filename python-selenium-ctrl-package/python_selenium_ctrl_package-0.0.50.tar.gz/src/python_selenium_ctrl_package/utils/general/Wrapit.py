"""
Class to hold miscellaneous but useful decorators for our framework
"""

from inspect import getfullargspec


class Wrapit():
    "Wrapit class to hold decorator functions"

    def _exceptionHandler(f):
        "Decorator to handle exceptions"

        def inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                args[0].write('You have this exception')
                args[0].write('Exception in method: %s' % str(f.__name__))
                args[0].write('PYTHON SAYS: %s' % str(e))
                # we denote None as failure case
                return None

        return inner

    def _screenshot(func):
        "Decorator for taking screenshots"

        # Usage: Make this the first decorator to a method (right above the 'def function_name' line)
        # Otherwise, we cannot name the screenshot with the name of the function that called it
        def wrapper(*args, **kwargs):
            """Original code"""
            # result = func(*args, **kwargs)
            # screenshot_name = '%003d' % args[0].screenshot_counter + '_' + func.__name__
            # args[0].screenshot_counter += 1
            # args[0].save_screenshot(screenshot_name)
            #
            # return result

            # Run function with _screenshot decorator, get the return result (Expect boolean)
            result = func(*args, **kwargs)
            # If return True, only take screenshot if option -screenshot all
            # If return False, take screenshot for both -screenshot all/failonly
            # If not return boolean, skip screenshot
            if args[0].screenshot == 'all':
                screenshot_name = '%003d' % args[0].screenshot_counter + '_' + func.__name__
                args[0].screenshot_counter += 1
                args[0].save_screenshot(screenshot_name)
            elif args[0].screenshot == 'failonly' and result is False:
                screenshot_name = '%003d' % args[0].screenshot_counter + '_' + func.__name__
                args[0].screenshot_counter += 1
                args[0].save_screenshot(screenshot_name)
            return result

        return wrapper

    def _check_browser_console_log(func):
        "Decorator to check the browser's console log for errors"

        def wrapper(*args, **kwargs):
            # As IE driver does not support retrieval of any logs,
            # we are bypassing the read_browser_console_log() method
            result = func(*args, **kwargs)
            if "ie" not in str(args[0].driver):
                result = func(*args, **kwargs)
                log_errors = []
                new_errors = []
                log = args[0].read_browser_console_log()
                if log is not None:
                    for entry in log:
                        if entry['level'] == 'SEVERE':
                            log_errors.append(entry['message'])

                    if args[0].current_console_log_errors != log_errors:
                        # Find the difference
                        new_errors = list(set(log_errors) - set(args[0].current_console_log_errors))
                        # Set current_console_log_errors = log_errors
                        args[0].current_console_log_errors = log_errors

                    if len(new_errors) > 0:
                        args[0].failure("\nBrowser console error on url: %s\nMethod: %s\nConsole error(s):%s" % (
                            args[0].get_current_url(), func.__name__, '\n----'.join(new_errors)))

            return result

        return wrapper

        # def _screencap(func):
        #     "Decorator for taking screencap for test"
        #
        #     # Usage: Make this the first decorator to a method (right above the 'def function_name' line)
        #     # Otherwise, we cannot name the screenshot with the name of the function that called it
        #     def wrapper(*args, **kwargs):
        #         result = "this is _screencap"
        #         print("%s is running" % func.__name__)

        return wrapper

    _exceptionHandler = staticmethod(_exceptionHandler)
    _screenshot = staticmethod(_screenshot)
    _check_browser_console_log = staticmethod(_check_browser_console_log)
