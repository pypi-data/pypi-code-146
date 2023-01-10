from numba.core import cgutils, types
from numba.extending import NativeValue, box, make_attribute_wrapper, models, register_model, typeof_impl, unbox


def install_py_obj_class(types_name, module, python_type=None, class_name=
    None, model_name=None):
    class_name = ''.join(map(str.title, types_name.split('_'))
        ) if class_name is None else class_name
    model_name = f'{class_name}Model' if model_name is None else model_name
    gyz__txtkn = f'class {class_name}(types.Opaque):\n'
    gyz__txtkn += f'    def __init__(self):\n'
    gyz__txtkn += f"       types.Opaque.__init__(self, name='{class_name}')\n"
    gyz__txtkn += f'    def __reduce__(self):\n'
    gyz__txtkn += (
        f"        return (types.Opaque, ('{class_name}',), self.__dict__)\n")
    itre__mqgjf = {}
    exec(gyz__txtkn, {'types': types, 'models': models}, itre__mqgjf)
    lcebh__mkqf = itre__mqgjf[class_name]
    setattr(module, class_name, lcebh__mkqf)
    class_instance = lcebh__mkqf()
    setattr(types, types_name, class_instance)
    gyz__txtkn = f'class {model_name}(models.StructModel):\n'
    gyz__txtkn += f'    def __init__(self, dmm, fe_type):\n'
    gyz__txtkn += f'        members = [\n'
    gyz__txtkn += (
        f"            ('meminfo', types.MemInfoPointer({types_name})),\n")
    gyz__txtkn += f"            ('pyobj', types.voidptr),\n"
    gyz__txtkn += f'        ]\n'
    gyz__txtkn += (
        f'        models.StructModel.__init__(self, dmm, fe_type, members)\n')
    exec(gyz__txtkn, {'types': types, 'models': models, types_name:
        class_instance}, itre__mqgjf)
    wsgmr__pew = itre__mqgjf[model_name]
    setattr(module, model_name, wsgmr__pew)
    register_model(lcebh__mkqf)(wsgmr__pew)
    make_attribute_wrapper(lcebh__mkqf, 'pyobj', '_pyobj')
    if python_type is not None:
        typeof_impl.register(python_type)(lambda val, c: class_instance)
    unbox(lcebh__mkqf)(unbox_py_obj)
    box(lcebh__mkqf)(box_py_obj)
    return lcebh__mkqf


def box_py_obj(typ, val, c):
    xtjky__vnmoz = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    obj = xtjky__vnmoz.pyobj
    c.pyapi.incref(obj)
    c.context.nrt.decref(c.builder, typ, val)
    return obj


def unbox_py_obj(typ, obj, c):
    xtjky__vnmoz = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    xtjky__vnmoz.meminfo = c.pyapi.nrt_meminfo_new_from_pyobject(c.context.
        get_constant_null(types.voidptr), obj)
    xtjky__vnmoz.pyobj = obj
    return NativeValue(xtjky__vnmoz._getvalue())
