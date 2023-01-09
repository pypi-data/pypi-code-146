from typing import List, Union, Optional, Dict
import os
import glob
import json
import shutil

import quickstats

def compile_macros(macros:Optional[Union[str, List[str]]]=None):
    """
    Compile ROOT macros
    
    Arguments:
        macros: (Optional) str or list of str
            If str, it is a string containing comma delimited list of macro names to be compiled.
            If list of str, it is the list of macro names to be compiled.
    """
    custom_list = True
    if macros is None:
        macros = get_all_macros()
        custom_list = False
    elif isinstance(macros, str):
        macros = macros.split(',')
    from quickstats.utils.root_utils import compile_macro
    for macro in macros:
        if ((macro == "FlexibleInterpVarMkII") and (quickstats.root_version >= (6, 26, 0))) and (not custom_list):
            quickstats._PRINT_.info("INFO: Skip compiling macro \"FlexibleInterpVarMkII\" which is "
                                    "deprecated since ROOT 6.26/00")
            continue
        compile_macro(macro)
        
def get_all_macros():
    """
    Get the list of macros names
    
    Note: Only macros ending in .cxx will be considered
    """
    macro_dir = quickstats.macro_path
    macro_subdirs = [path for path in glob.glob(os.path.join(macro_dir, "*")) if os.path.isdir(path)]
    macro_names = []
    for macro_subdir in macro_subdirs:
        macro_name = os.path.basename(macro_subdir)
        macro_path = os.path.join(macro_subdir, f"{macro_name}.cxx")
        if os.path.exists(macro_path):
            macro_names.append(macro_name)
    return macro_names

def set_verbosity(verbosity:Union[str, int]="INFO"):
    quickstats._PRINT_.verbosity = verbosity
    
def get_root_version():
    from quickstats.root_checker import ROOTChecker, ROOTVersion
    try:
        root_config_cmd = ROOTChecker.get_root_config_cmd()
        root_version = ROOTChecker.get_installed_root_version(root_config_cmd)
    except:
        root_version = ROOTVersion((0, 0, 0))
    return root_version

def get_workspace_extensions():
    extension_config = get_workspace_extension_config()
    extensions = extension_config['required']
    if not extension_config['strict']:
        # deprecated extension
        if (quickstats.root_version >= (6, 26, 0)) and 'FlexibleInterpVarMkII' in extensions:
            extensions.remove('FlexibleInterpVarMkII')
    return extensions

def get_workspace_extension_config():
    resource_path = quickstats.resource_path
    extension_config_file = os.path.join(resource_path, "workspace_extensions.json")
    if not os.path.exists(extension_config_file):
        extension_config_file = os.path.join(resource_path, "default_workspace_extensions.json")
    with open(extension_config_file, "r") as file:
        extension_config = json.load(file)
    return extension_config

def add_macro(path:str, name:Optional[str]=None, copy_files:bool=True,
              workspace_extension:bool=True, force:bool=False):
    if not os.path.isdir(path):
        raise ValueError("macro path must be a directory")
    if name is None:
        name = os.path.basename(os.path.abspath(path))
    source_path = os.path.join(path, f"{name}.cxx")
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"macro path must contain a source file named {name}.cxx")
    macro_path = quickstats.macro_path
    if copy_files:
        dest_path = os.path.join(macro_path, name)
        if os.path.exists(dest_path):
            if force or input(f'WARNING: The macro already exists in {dest_path}, overwrite? [Y/N]') == "Y":
                shutil.rmtree(dest_path)
                shutil.copytree(path, dest_path)
                quickstats._PRINT_.info(f'INFO: Overwritten contents for the macro "{name}" from {path} to {dest_path}.')
            else:
                quickstats._PRINT_.info(f'INFO: Overwrite cancelled.')
        else:
            shutil.copytree(path, dest_path)
            quickstats._PRINT_.info(f'INFO: Copied contents for the macro "{name}" from {path} to {dest_path}.')
    if workspace_extension:
        resource_path = quickstats.resource_path
        extension_config_file = os.path.join(resource_path, "workspace_extensions.json")
        extension_config = get_workspace_extension_config()
        if name not in extension_config['required']:
            extension_config['required'].append(name)
            with open(extension_config_file, "w") as file:
                json.dump(extension_config, file, indent=2)
        quickstats._PRINT_.info(f'INFO: The macro "{name}" has been added to the workspace extension list.')
        
def remove_macro(name:str, remove_files:bool=True, force:bool=False):
    resource_path = quickstats.resource_path
    extension_config_file = os.path.join(resource_path, "workspace_extensions.json")
    extension_config = get_workspace_extension_config()
    if (name not in extension_config):
        quickstats._PRINT_.info(f'WARNING: Extension "{name}" not found in the workspace extension list. Skipped.')
    else:
        extension_config.remove(name)
        with open(extension_config_file, "w") as file:
            json.dump(extension_config, file, indent=2)
        quickstats._PRINT_.info(f'INFO: The extension "{name}" has been removed from the workspace extension list.')
    if remove_files:
        macro_path = quickstats.macro_path
        extension_path = os.path.abspath(os.path.join(macro_path, name))
        if force or input(f'WARNING: Attempting to remove files from {extension_path}, confirm? [Y/N]') == "Y":
            quickstats._PRINT_.info(f'INFO: Files for the macro "{name}" has been removed from {extension_path}.')
            shutil.rmtree(extension_path)
        else:
            quickstats._PRINT_.info(f'INFO: Macro files removal cancelled.')

def load_corelib():
    if not quickstats.corelib_loaded:
        from quickstats.utils.root_utils import load_macro
        load_macro("QuickStatsCore")
        quickstats.corelib_loaded = True
        
def load_extensions():
    extensions = get_workspace_extensions()
    extensions.extend(["QuickStatsCore", "AsymptoticCLsTool"])
    from quickstats.utils.root_utils import load_macro
    for extension in extensions:
        load_macro(extension)
        
def load_processor_methods():
    from quickstats.components.processors.builtin_methods import BUILTIN_METHODS
    from quickstats.utils.root_utils import declare_expression
    for name, definition in BUILTIN_METHODS.items():
        declare_expression(definition, name)    