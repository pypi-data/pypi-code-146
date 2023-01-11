from numba.core import cgutils, types
from numba.extending import NativeValue, box, make_attribute_wrapper, models, register_model, typeof_impl, unbox


def install_py_obj_class(types_name, module, python_type=None, class_name=
    None, model_name=None):
    class_name = ''.join(map(str.title, types_name.split('_'))
        ) if class_name is None else class_name
    model_name = f'{class_name}Model' if model_name is None else model_name
    fbp__amv = f'class {class_name}(types.Opaque):\n'
    fbp__amv += f'    def __init__(self):\n'
    fbp__amv += f"       types.Opaque.__init__(self, name='{class_name}')\n"
    fbp__amv += f'    def __reduce__(self):\n'
    fbp__amv += (
        f"        return (types.Opaque, ('{class_name}',), self.__dict__)\n")
    zjml__tfriw = {}
    exec(fbp__amv, {'types': types, 'models': models}, zjml__tfriw)
    gus__mqca = zjml__tfriw[class_name]
    setattr(module, class_name, gus__mqca)
    class_instance = gus__mqca()
    setattr(types, types_name, class_instance)
    fbp__amv = f'class {model_name}(models.StructModel):\n'
    fbp__amv += f'    def __init__(self, dmm, fe_type):\n'
    fbp__amv += f'        members = [\n'
    fbp__amv += (
        f"            ('meminfo', types.MemInfoPointer({types_name})),\n")
    fbp__amv += f"            ('pyobj', types.voidptr),\n"
    fbp__amv += f'        ]\n'
    fbp__amv += (
        f'        models.StructModel.__init__(self, dmm, fe_type, members)\n')
    exec(fbp__amv, {'types': types, 'models': models, types_name:
        class_instance}, zjml__tfriw)
    hulj__lgk = zjml__tfriw[model_name]
    setattr(module, model_name, hulj__lgk)
    register_model(gus__mqca)(hulj__lgk)
    make_attribute_wrapper(gus__mqca, 'pyobj', '_pyobj')
    if python_type is not None:
        typeof_impl.register(python_type)(lambda val, c: class_instance)
    unbox(gus__mqca)(unbox_py_obj)
    box(gus__mqca)(box_py_obj)
    return gus__mqca


def box_py_obj(typ, val, c):
    oxya__axf = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    obj = oxya__axf.pyobj
    c.pyapi.incref(obj)
    c.context.nrt.decref(c.builder, typ, val)
    return obj


def unbox_py_obj(typ, obj, c):
    oxya__axf = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    oxya__axf.meminfo = c.pyapi.nrt_meminfo_new_from_pyobject(c.context.
        get_constant_null(types.voidptr), obj)
    oxya__axf.pyobj = obj
    return NativeValue(oxya__axf._getvalue())
