"""
Functions to install and configure UI onto this machine.
"""

import ctypes, glob, os, shutil, subprocess, sys, ctypes.wintypes, json
import matplotlib as mpl, matplotlib.font_manager as mpl_fonts, matplotlib.pyplot as plt
import uintel as ui

if sys.platform == "win32":
    try:
        import winreg
    except ImportError:
        import _winreg as winreg

class _printColours:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def _create_config_file() -> None:
    """
    Create a configuration file that contains key information about the user and key Urban Intelligence information, that is commonly used throughout multiple programs. The configuration file is stored at ~/.ui/config
    """

    if os.path.exists(ui._config_path):
        return 
        
    print(f"{_printColours.UNDERLINE}{_printColours.BOLD}{_printColours.BLUE}Kia ora and welcome to Urban Intelligence.{_printColours.END}\n")
    print(f"{_printColours.BLUE}To streamline this package and reduce asking these details continuously, we wish to ask you some questions about yourself to store in a credentials file.\nThis file will be located at {ui._config_path} should you ever wish to view it or alter information.{_printColours.END}\n")

    config = {}
    config["name"] = input("To begin, what is your name? ").title()
    
    print(f"{_printColours.BLUE}It's a pleasure to have you here, {config['name']}.\nIf at any stage you do not know the answer to any of the questions or if they are not applicable, then please leave the prompt empty and hit enter.\n\nThese next set of questions deal with connecting to our main server, piwakawaka.{_printColours.END}")
    config["piwakawaka"] = {"address": "167.99.90.75"}
    config["piwakawaka"]["username"] = input("What is your username when connecting to piwakawaka? ")
    config["piwakawaka"]["ssh_key"] = "yes" in input("Do you use a SSH key to connect to piwakawaka? (yes/no) ").lower()
    if not config["piwakawaka"]["ssh_key"]:
        config["piwakawaka"]["password"] = input("Since you have indicated you do not use a SSH key, what is your password? ")

    print(f"\n{_printColours.BLUE}This next section will address the use of Slack.\n{_printColours.UNDERLINE}{_printColours.BOLD}This will require you to navigate to a pinned post in the #pyui slack channel containing the answers to the question, and paste them here. If you are not a member of that channel, then please contact Sam directly.{_printColours.END}")
    config["slack"] = {
        "UI": input("What is the token to access the Urban Intelligence slack channel? "),
        "UC": input("What is the token to access the University of Canterbury (CivilSystems) slack channel? "),
    }

    print(f"\n{_printColours.BLUE}This next section will address the use of SQL databases.{_printColours.END}")
    config["SQL"] = {
        "host": input("What is the name of the host for SQL? (This is typically 'encivmu-tml62') "), 
        "port": int(input("What port is the SQL database on? (Typically 5002) ")),
        "password": input("What is the password to connect to SQL? ")}

    if not os.path.exists(os.path.expanduser("~/.aws/credentials")):
        print(f"{_printColours.BLUE}This next section will address the use of Amazon Web Services (AWS).{_printColours.END}")
        if "yes" in input(f"{_printColours.BLUE}To send files to AWS for the UI dashboards, you will require an AWS account. I noticed you have not saved your credentials to this computer.\nDo you have an AWS account you wish to connect?{_printColours.END} ").lower():
            print(f"{_printColours.BLUE}Excellent. There are two key bits of information I require to do this - an access key id and a secret access key.\n\n{_printColours.BOLD}Instructions: To create a new secret access key for an IAM user, open the IAM console in AWS. Click Users in the Details pane, click the appropriate IAM user, and then click Create Access Key on the Security Credentials tab. The two bits of information should now be showing.{_printColours.END}")
            aws_credentials = f"[default]\naws_access_key_id = {input('What is the access key? ')}\naws_secret_access_key = {input('What is the secret access key? ')}"
            if not os.path.exists(os.path.expanduser("~/.aws")):
                os.makedirs(os.path.expanduser("~/.aws"))
            with open(os.path.expanduser("~/.aws/credentials"), "w") as file:
                _ = file.write(aws_credentials)

    # Save the config file
    if not os.path.exists(os.path.dirname(ui._config_path)):
        os.makedirs(os.path.dirname(ui._config_path))
    json.dump(config, open(ui._config_path, "w"), indent=4)
    print(f"\n{_printColours.BLUE}Awesome, thanks for answering those questions {config['name']}! I'll now continue the installation :) {_printColours.END}")


def _install_styles(force: bool, verbose: bool) -> None:
    """
    Copy all unregistered UI style sheets (saved in 'styles' folder) to the matplotlib configuration folder. To revert stylesheets back to default (in case they were manually edited), use force=True.
    """
    try:
        style_dir = os.path.dirname(ui.__file__) + '/styles'
        mpl_style_dir = os.path.join(mpl.get_configdir(), "stylelib")
        stylesheets = glob.glob(style_dir + "/*.mplstyle")     
        if len(stylesheets) == 0:
            print(f"{_printColours.YELLOW}No matplotlib stylesheets detected in this version. If you were expecting some to install, please contact the maintainer of this package, Sam.{_printColours.END}")
            return
        else:
            altered_files = 0
            for stylefile in stylesheets:
                if os.path.basename(stylefile).split(".")[0] not in plt.style.library or force:
                    # Move each style sheet to the right place, which replaces any manual changes to UI stylelibs
                    _ = shutil.copy(stylefile, os.path.join(mpl_style_dir, os.path.basename(stylefile)))
                    altered_files += 1

        # Update the current instance of matplotlib with the stylesheets
        stylesheets = plt.style.core.read_style_directory(style_dir)
        _ = plt.style.core.update_nested_dict(plt.style.library, stylesheets)
        plt.style.core.available[:] = sorted(plt.style.library.keys())
        
        if altered_files > 0 and verbose:
            print(f"{_printColours.GREEN}Successfully updated {altered_files} matplotlib stylesheets!{_printColours.END}")
        elif verbose:
            print(f"{_printColours.GREEN}All matplotlib stylesheets were already up to date!{_printColours.END}")
    except Exception as error:
        print(f"{_printColours.RED}The Urban Intelligence matplotlib stylesheets have not been successfully installed. Please contact the maintainer of this package, Sam, with the following error message:\n{error}{_printColours.END}")


def _install_fonts(force: bool, verbose=True) -> None:
    """
    Copy and install all unregistered fonts (saved in 'fonts' folder) to this machine. To revert fonts back to default (in case they were manually edited), use force=True.
    """

    fonts = {os.path.basename(filepath): filepath for filepath in glob.glob(os.path.dirname(__file__) + "/fonts/*.ttf")}
    if len(fonts) == 0:
        print(f"{_printColours.YELLOW}No fonts detected in this version. If you were expecting some to install, please contact the maintainer of this package, Sam.{_printColours.END}")
        return
    
    if force:
        # Delete all installed fonts so they can be reinstalled
        _delete_installed_fonts(fonts)
    else:   
        # Otherwise, we should skip fonts that are already installed 
        fonts = _get_uninstalled_fonts(fonts)

    if len(fonts) > 0:
        if sys.platform == "win32":
            _install_windows_fonts(fonts, verbose)
            _refresh_matplotlib_fonts()
        elif sys.platform == "linux":
            _install_linux_fonts(fonts, verbose)
            _refresh_matplotlib_fonts()
        else:
            print(f"{_printColours.RED}Unfortunately, the automatic downloading and installing Urban Intelligence's fonts has only been set up to be used for Windows or Linux distributions (because Sam doesn't have a Mac to test this code on). If the Rubik font is not installed on your device, please do so manually. Apolgies for the inconvience.{_printColours.END}")
    else:
        print(f"{_printColours.GREEN}All fonts were already up to date!{_printColours.END}")


def _get_uninstalled_fonts(fonts: dict) -> None:
    """
    Takes a dictionary of font_name:font_path (e.g. 'Rubik.ttf':'/fonts/rubik.ttf') and returns only the keys of fonts that are not installed on this machine.
    """
    uninstalled_fonts = {}

    if sys.platform == "win32":
        for font_name, font_path in fonts.items():
            font_in_regedit = False
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows NT\CurrentVersion\Fonts', 0, winreg.KEY_READ) as key:
                # Loop over each Value (font names) in the Key (registry path to the fonts) and see if it our wanted fonts are contained
                for i in range(winreg.QueryInfoKey(key)[1]):
                    font_name_installed, _, _ = winreg.EnumValue(key, i)
                    if font_name.split(".")[0] == font_name_installed:
                        font_in_regedit = True
                        break
           
            if not font_in_regedit:
                # The font is not properly installed for at least one reason.
                uninstalled_fonts[font_name] = font_path

    elif sys.platform == "linux":
        
        installed_fonts = os.listdir(os.path.expanduser("~/.local/share/fonts/"))
        for font_name, font_path in fonts.items():
            if font_name not in installed_fonts:
                uninstalled_fonts[font_name] = font_path

    else:
        print(f"{_printColours.RED}Unfortunately, the automatic downloading and installing Urban Intelligence's fonts has only been set up to be used for Windows or Linux distributions (because Sam doesn't have a Mac to test this code on). If the Rubik font is not installed on your device, please do so manually. Apolgies for the inconvience.{_printColours.END}")

    return uninstalled_fonts


def _delete_installed_fonts(fonts: dict) -> None:
    """
    Delete all installed fonts
    """
    
    if sys.platform == "win32":
        # Delete registry keys
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows NT\CurrentVersion\Fonts', 0, winreg.KEY_ALL_ACCESS) as key:
            for font_name in fonts:
                try:
                    _ = winreg.DeleteValue(key, font_name.split(".")[0])
                except:
                    pass
        
        # Delete the actual files
        font_save_path = os.path.expandvars('%LOCALAPPDATA%/Microsoft/Windows/Fonts')
        for font_name in fonts:
            if os.path.exists(os.path.join(font_save_path, font_name)):
                _ = os.remove(os.path.join(font_save_path, font_name))

    
    elif sys.platform == "linux":
        # Delete the actual files
        font_save_path = os.path.expanduser("~/.local/share/fonts/")
        for font_name in fonts:
            if os.path.exists(os.path.join(font_save_path, font_name)):
                _ = os.remove(os.path.join(font_save_path, font_name))

    else:
        print(f"{_printColours.RED}Unfortunately, the automatic downloading and installing Urban Intelligence's fonts has only been set up to be used for Windows or Linux distributions (because Sam doesn't have a Mac to test this code on). If the Rubik font is not installed on your device, please do so manually. Apolgies for the inconvience.{_printColours.END}")

    return


def _install_windows_fonts(fonts: dict, verbose=True) -> None:
    """
    Install the fonts into the computers fonts folder (or users local fonts folder if permissions are denied) and register them on RegistryEditor.
    Based on code by https://stackoverflow.com/a/68714427    
    """

    user32 = ctypes.WinDLL('user32', use_last_error=True)
    gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)

    if not hasattr(ctypes.wintypes, 'LPDWORD'):
        ctypes.wintypes.LPDWORD = ctypes.POINTER(ctypes.wintypes.DWORD)

    user32.SendMessageTimeoutW.restype = ctypes.wintypes.LPVOID
    user32.SendMessageTimeoutW.argtypes = (ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.LPVOID, ctypes.wintypes.LPVOID, ctypes.wintypes.UINT, ctypes.wintypes.UINT, ctypes.wintypes.LPVOID)
    gdi32.AddFontResourceW.argtypes = (ctypes.wintypes.LPCWSTR,)
    gdi32.GetFontResourceInfoW.argtypes = (ctypes.wintypes.LPCWSTR, ctypes.wintypes.LPDWORD, ctypes.wintypes.LPVOID, ctypes.wintypes.DWORD)
    
    for font_name, font_path in fonts.items():
        try:
            # Copy the font to the user's Font folder
            dst_path = os.path.join(os.path.expandvars('%LOCALAPPDATA%/Microsoft/Windows/Fonts'), font_name)
            _ = shutil.copy(font_path, dst_path)
                            
            # Notify running programs that there is a new font
            _ = user32.SendMessageTimeoutW(0xFFFF, 0x001D, 0, 0, 0x0002, 1000, None)
            
            # Store the fontname/filename in the registry so it can be found 
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows NT\CurrentVersion\Fonts', 0, winreg.KEY_SET_VALUE) as key:
                _ = winreg.SetValueEx(key, font_name.split(".")[0], 0, winreg.REG_SZ, dst_path)

            if verbose:
                print(f"{_printColours.GREEN}Successfully installed {font_name}!{_printColours.END}")
        except Exception as error:
            print(f"{_printColours.RED}The font {font_name} could not be installed. Please download and install the font manually, or contact the maintainer of this package, Sam, about the following error message:\n{error}{_printColours.END}")
    

def _install_linux_fonts(fonts: dict, verbose=True) -> None:
    """
    Install the fonts into the computers fonts folder (or users local fonts folder if permissions are denied) and then refresh the font cache.
    """

    for font_name, font_path in fonts.items():
        try:
            # Copy the font to the user's Font folder
            dst_path = os.path.join(os.path.expanduser("~/.local/share/fonts/"), font_name)
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            _ = shutil.copy(font_path, dst_path)
                            
        except Exception as error:
            print(f"{_printColours.RED}The font '{font_name}' could not be installed. Please log the following error message as an issue on the GiHub repository https://github.com/uintel/pyui/issues\n{error}{_printColours.END}")
    
    # Rebuild the font cache with fc-cache -f -v
    process = subprocess.run(["fc-cache", "-f"])    
    if process.returncode == 0 and verbose:
        print(f"{_printColours.GREEN}Successfuly installed {len(fonts)} fonts!{_printColours.END}")
    elif process.returncode != 0:
        print(f"{_printColours.RED}One or more of the fonts '{list(fonts.keys())}' could not be installed. Please download and install the font manually, or contact the maintainer of this package, Sam, about the following error message:\nError {process.returncode}: {process.stderr.decode()}{_printColours.END}")
    

def _refresh_matplotlib_fonts():
    """
    Refresh the cache of available fonts to use in matplotlib
    """
    mpl_fonts.json_dump(mpl_fonts.FontManager(), os.path.join(mpl.get_cachedir(), f"fontlist-v{mpl_fonts.FontManager.__version__}.json"))

