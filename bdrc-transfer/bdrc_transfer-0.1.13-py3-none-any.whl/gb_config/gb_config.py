#!/usr/bin/env python3
"""
Google Books GRIN initial setup script
- Copy grin config from install directory to user's ~/.config/gb directory
- Backs up any existing grin.config into a backup with random suffix
"""
import shutil
from inspect import getsourcefile
import os
from pathlib import Path

cfg_file_name = 'grin.config'

def config_main():
    """
    Configure google books process. Mostly load the Google Books non-confidential config file
    variables
    :return:
    """
    where_am_i = getsourcefile(config_main)
    config_src: Path = Path(where_am_i).parent / cfg_file_name
    config_dest: Path = Path(Path.home(), '.config', 'gb')
    os.makedirs(name = config_dest, exist_ok = True, mode = 0o700 )
    new_dest_path: Path = config_dest / cfg_file_name
    print(f'Copying config to user path {str(config_dest)}')
    if Path.exists(config_dest / cfg_file_name):
        import random, string
        backup_cfg: str = cfg_file_name + '.' + ''.join(random.choice(string.ascii_letters) for _ in range(6))
        backup_dest: Path = config_dest / backup_cfg

        print(f"Backing up {new_dest_path} to {backup_dest}")
        shutil.move(new_dest_path, backup_dest)

    shutil.copyfile(config_src, config_dest / cfg_file_name)

# Uncomment for testing
# config_main()
