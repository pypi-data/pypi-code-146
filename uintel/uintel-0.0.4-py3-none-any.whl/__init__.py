import os, json, uintel.install
_config_path = os.path.expanduser("~/.ui/config")

def reset(force=False, verbose=True):
    """
    Complete all necessary installations, including matplotlib stylesheets and Rubik fonts, onto this machine. To revert stylesheets back to default (in case they were manually edited) and revert fonts, use force=True. To re-create the configuration file, please delete the configuration file and run 'import ui'.
    """
    
    # Step 1 - Create the configuration file
    if not os.path.exists(_config_path):
        uintel.install._create_config_file()

    # Step 2 - Install the matplotlib style sheets
    uintel.install._install_styles(force, verbose)

    # Step 3 - Install fonts
    uintel.install._install_fonts(force, verbose)

reset()

config = json.load(open(_config_path, "r"))

import uintel.aws, uintel.colours, uintel.db, uintel.esri, uintel.server, uintel.slack
__all__ = ["aws", "colours", "db", "esri", "server", "slack"]
