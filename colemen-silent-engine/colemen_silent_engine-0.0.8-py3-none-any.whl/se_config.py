# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

import os
from typing import TypeVar as _TypeVar
from typing import Union as _Union
from typing import Iterable as _Iterable
from typing import TYPE_CHECKING
import colemen_utils as _c



schemas = ["idealech_Equari_Management_Database","idealech_Equari_Content_Database","idealech_Equari_Business_Database","idealech_Equari_Meta"]
crud_types = ["create","read","read_single","update","delete"]


output_path = "Z:/Structure/Ra9/2023/23-0001 - ApricityGod/_OUTPUT"
documentation_output_path = "Z:/Structure/Ra9/2023/23-0001 - ApricityGod/_DOCUMENTATION"
database_cache_path = "Z:/Structure/Ra9/2023/23-0001 - ApricityGod/_DB_CACHE"

generate_master_summary = False
generate_database_documentation = True


objects_path = f"{output_path}/apricity/objects"
objects_stratum_path = f"{output_path}/apricity/objects/stratum"
settings_path = f"{output_path}/apricity/settings"
susurrus_path = f"{output_path}/apricity/susurrus"
susurrus_stratum_path = f"{output_path}/apricity/susurrus/stratum"



# ---------------------------------------------------------------------------- #
#                                   TEMPLATES                                  #
# ---------------------------------------------------------------------------- #











# ---------------------------------------------------------------------------- #
#                               TYPE DECLARATIONS                              #
# ---------------------------------------------------------------------------- #

_main_type = None
_package_type = None
_py_class_type = None
_py_property_type = None
_py_module_type = None
_py_import_type = None
_method_type = None
_method_argument_type = None


# _master_type = None
# _table_type = None
# _table_doc_type = None
# _column_type = None
# _column_doc_type = None
# _relationship_type = None



# _entity_type = None
# _entity_attribute_type = None
# _entity_column_attribute_type = None
# _form_type = None
# _attribute_declaration_type = None
# _type_declaration_type = None
# _attribute_getter_type = None
# _susurrus_type = None




# ControlPanel = _control_panel.ControlPanel()

if TYPE_CHECKING:

    import silent_engine as _m
    _main_type = _TypeVar('_main_type', bound=_m.Main)
    
    import silent.Package as _p
    _package_type = _TypeVar('_package_type', bound=_p.Package)
    # import silent.Master as _master
    # _master_type = _TypeVar('_master_type', bound=_master.Master)


    import silent.Class as _class
    _py_class_type = _TypeVar('_py_class_type', bound=_class.Class)
    
    import silent.Class.Property as _prop
    _py_property_type = _TypeVar('_py_property_type', bound=_prop.Property)
   
    import silent.Module as _mod
    _py_module_type = _TypeVar('_py_module_type', bound=_mod.Module)
   
    import silent.Import.ImportStatement as _imps
    _py_import_type = _TypeVar('_py_import_type', bound=_imps.ImportStatement)


    import silent.Method.Method as _classM
    _method_type = _TypeVar('_method_type', bound=_classM.Method)

    import silent.Method.MethodArgument as _methArg
    _method_argument_type = _TypeVar('_method_argument_type', bound=_methArg.MethodArgument)




_templates = {}

def get_template(name):
    if len(_templates.keys()) == 0:
        files = _c.file.get_files(f"{os.getcwd()}/silent",extension=['md','py'])
        for file in files:
            if "template" in file['file_name']:
                file['contents'] = _c.file.readr(file['file_path'])
                _templates[file['name_no_ext']] = file
    if name in _templates:
        return _templates[name]['contents']
    _c.con.log(f"Failed to locate template: {name}","warning")
    return ""




def type_to_python_real(value):
    if value == "boolean":
        value = "bool"
    if value == "string":
        value = "str"
    if value == "integer":
        value = "int"
    return value


