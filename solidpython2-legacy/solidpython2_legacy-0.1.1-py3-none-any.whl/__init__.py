from .bill_of_materials import *
from .part_hole import *
from .repr_png import __nothing__
from .types import *
from .utils import *
from . import splines
from . import screw_thread

from solid2.core.object_base import ObjectBase
from solid2.core.utils import escape_openscad_identifier
from solid2.extensions.operators import _union_op
from solid2.core.builtins import debug, background, root, disable

def set_modifier(self, m):
        """
        Used to add one of the 4 single-character modifiers:
        #(debug) !(root) %(background) or *(disable)
        """
        print("WARNING: OpenSCADObject.set_modifier is deprecated in ExpSolid! " +\
                        "Use debug()(obj) resp. background, root, disable.")
        string_vals = {'disable': '*',
                       'debug': '#',
                       'background': '%',
                       'root': '!',
                       '*': '*',
                       '#': '#',
                       '%': '%',
                       '!': '!'}

        self.modifier = string_vals.get(m.lower(), '')
        return self

def _render(self):
    render_func = _openscadobject_render if isinstance(self, OpenSCADObject) else _objectbase_render
    if not "modifier" in self.__dict__.keys():
        self.modifier = ""
    return self.modifier + render_func(self)

def add_param(self, k, v):
    def legacy_patch(key):
        # this function patches the kwargs to be backward compatible
        import keyword
        if key == "segments":
            return "_fn"

        if key.endswith("_") and keyword.iskeyword(key[:-1]):
            return "_" + key[:-1]

        if key.startswith("__") and key[2].isdigit():
            return "_" + key[2:]

        return key

    print("WARNING: OpenSCADObject.add_param is deprecated in ExpSolid! " +\
          "You should not need it ;)")
    self.params[escape_openscad_identifier(legacy_patch(k))] = v
    return self

def add_trait(self, trait_name:str, trait_data:Dict[str, float]):
    print("WARNING: OpenSCADObject.add_trait is deprecated in ExpSolid! " +\
          "Use solid2_legacy.bill_of_materials")
    if not "traits" in self.__dict__.keys():
        self.traits = {}
    self.traits[trait_name] = trait_data

def get_trait(self, trait_name:str) -> Optional[Dict[str, float]]:
    print("WARNING: OpenSCADObject.get_trait is deprecated in ExpSolid! " +\
          "Use solid2_legacy.bill_of_materials ;)")
    if not "traits" in self.__dict__.keys():
        return None
    return self.traits.get(trait_name)

ObjectBase.set_parent = lambda self, *args, **kwargs: \
    print("WARNING: ExpSolid does not support OpenSCADObject.set_parent! " +\
          "This call will be ignored! Use solid2_legacy.bill_of_materials")

ObjectBase.set_hole = lambda self, *args, **kwargs: \
    print("WARNING: ExpSolid does not support OpenSCADObject.set_hole! " +\
          "This call will be ignored! Use solid2_legacy.part_hole")

ObjectBase.set_part_root = lambda self, *args, **kwargs: \
    print("WARNING: ExpSolid does not support OpenSCADObject.set_part_root! " +\
          "This call will be ignored! Use solid2_legacy.part_hole")

ObjectBase.find_hole_children = lambda self, *args, **kwargs: \
    print("WARNING: ExpSolid does not support OpenSCADObject.find_hole_children! " +\
          "This call will be ignored! Use solid2_legacy.part_hole")

def legacy_add(self, x):
    if isinstance(x, int) and x == 0:
        return self
    else:
        _objectbase_add(self, x)

_openscadobject_render = OpenSCADObject._render
_objectbase_render = ObjectBase._render
_objectbase_add = ObjectBase.add

ObjectBase.set_modifier = set_modifier
ObjectBase._render = _render
OpenSCADObject._render = _render
ObjectBase.add_param = add_param
ObjectBase.add_trait = add_trait
ObjectBase.get_trait = get_trait
ObjectBase.add = legacy_add

