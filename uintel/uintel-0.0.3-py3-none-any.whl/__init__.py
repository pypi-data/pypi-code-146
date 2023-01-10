import os, glob, sys, json, uintel.install as install
_config_path = os.path.expanduser("~/.ui/config")

def reset(force=False):
    """
    Complete all necessary installations, including matplotlib stylesheets and Rubik fonts, onto this machine. To revert stylesheets back to default (in case they were manually edited) and revert fonts, use force=True. To re-create the configuration file, please delete the configuration file and run 'import ui'.
    """
    
    if not os.path.exists(_config_path):
        install._create_config_file()

    install._install_styles(force)

    fonts = {os.path.basename(filepath): filepath for filepath in glob.glob(os.path.dirname(__file__) + "/fonts/*.ttf")}
    if len(fonts) == 0:
        print(f"{install._printColours.YELLOW}No fonts detected in this version. If you were expecting some to install, please contact the maintainer of this package, Sam.{install._printColours.END}")
        return
    
    if not force:
        fonts = install._get_uninstalled_fonts(fonts)

    if sys.platform == "win32":
        install._install_windows_fonts(fonts)
    elif sys.platform == "linux":
        install._install_linux_fonts(fonts)
    else:
        print(f"{install._printColours.RED}Unfortunately, the automatic downloading and installing Urban Intelligence's fonts has only been set up to be used for Windows or Linux distributions (because Sam doesn't have a Mac to test this code on). If the Rubik font is not installed on your device, please do so manually. Apolgies for the inconvience.{install._printColours.END}")

reset()

config = json.load(open(_config_path, "r"))

import uintel.aws, uintel.colours, uintel.db, uintel.esri, uintel.server, uintel.slack
__all__ = ["aws", "colours", "db", "esri", "server", "slack"]
