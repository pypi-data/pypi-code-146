# TODO: module for creating simple GUI components and applications
import pyautogui
import klsframe.utilities.utils as klsutils


def confirm_yes_no(selection, default=True):
    if not isinstance(default, bool):
        raise ValueError("Unknown value for parameter 'default'")
    elif default:
        hint = f'[Y/n]'
        butt1 = 'Yes'
        butt2 = 'No'
    else:
        hint = f'[N/y]'
        butt1 = 'No'
        butt2 = 'Yes'
    opt = user_confirmation(title='Confirm selection',
                            text=f"You selected:\n\n{selection}\n\nConfirm selection? {hint}\t",
                            button1=butt1, button2=butt2)
    if opt == 'Yes':
        return True
    elif opt == 'No':
        return False
    else:
        print(f"Option '{opt}' not recognized")


def confirm_continue_or_exit(title="Continue or exit", text="Do you want to continue?",
                             button_continue="continue", button_cancel="exit", timeout=None):
    def say_bye():
        print("You decided to continue...death awaits you...")

    def _user_exit():
        print('[INFO] Execution cancelled by the user. Exiting...')
        pyautogui.alert(title='Exiting', text='Execution cancelled by the user.\nExiting...')
        exit(0)

    user_confirmation(title=title, text=text, button1=button_continue, button2=button_cancel,
                      action1=say_bye, action2=_user_exit, timeout=timeout)


def user_confirmation(title="", text="", button1='continue', button2='cancel',
                      action1=None, action2=None, timeout=None, action_timeout=None):
    """
    Prompts a window to arise a question with two possible answers.
    Useful for example for Continue/cancel prompts

    :param title: Window title
    :param text: Window text content
    :param button1: text to be displayed in button 1
    :param button2: text to be displayed in button 2
    :param action1: callback  executed if button1 is pressed
    :param action2: callback  executed if button1 is pressed
    :param timeout: prompt timeout in seconds
    :param action_timeout: callback (function) executed if timeout is reached
    :return: the pressed button's text
    """
    if timeout is not None:
        ret = pyautogui.confirm(title=title, text=text, buttons=(button1, button2), timeout=timeout * 1000)
    else:
        ret = pyautogui.confirm(title=title, text=text, buttons=(button1, button2))
    if klsutils.equals_ignore_case(ret, button1):
        if action1 is not None:
            action1()
    elif klsutils.equals_ignore_case(ret, button2):
        if action2 is not None:
            action2()
    elif timeout is not None and ret == 'Timeout':
        if action_timeout is not None:
            action_timeout()
    else:
        raise ValueError("Unexpected input value")
    return ret


def prompt(title="", text="", default="", timeout=None, validations=None, error_msg=None,
           confirm=False, allow_empty=True):
    # TODO: implement it like safe input
    """
    Prompts a window for the user to input a text value

    :param title: Prompt title
    :param text: prompt description text
    :param default: Default value for the input
    :param timeout: prompt timeout in seconds
    :param validations: Set of RegExp indicating the possible values of the input, like a whitelist
    :param error_msg: Message to be displayed when the input is not valid
    :param confirm: Enable/disable input confirmation
    :param allow_empty: Enable/disable empty inputs
    :return: The user input as a string or None if the input was cancelled
    """
    if validations is None:
        validations = []
    elif type(validations) is not list:
        validations = [validations]
    if error_msg is None:
        error_msg = "Error. Invalid input"
    while True:
        if timeout is None:
            inval = pyautogui.prompt(title=title, text=text, default=default)
        else:
            inval = pyautogui.prompt(title=title, text=text, default=default, timeout=timeout * 1000)
        if not allow_empty and inval == "":
            pyautogui.alert(title='Input error', text=error_msg)
        elif len(validations) > 0:
            if klsutils.validate(inval, validations):  # Validation passed
                if bool(confirm) and inval is not None:  # Confirmation prompt enabled
                    if confirm_yes_no(inval):
                        return inval  # Confirmation: accepted
                    else:
                        continue  # Confirmation: rejected. Continue the questioning loop
                else:  # Confirmation prompt disabled
                    return inval
            else:  # Validation failed
                pyautogui.alert(title='Input error', text=error_msg)
        else:  # No validations to be passed
            if bool(confirm):  # Confirmation prompt enabled
                if confirm_yes_no(inval):
                    return inval  # Confirmation: accepted
                else:
                    continue  # Confirmation: rejected. Continue the questioning loop
            else:  # Confirmation prompt disabled
                return inval


if __name__ == '__main__':
    # confirm_continue_or_exit()
    print(prompt(title="Testing testing", text="poninedo a prueba tu subwoffer", confirm=True))
    # print(confirm_yes_no('Morir'))
