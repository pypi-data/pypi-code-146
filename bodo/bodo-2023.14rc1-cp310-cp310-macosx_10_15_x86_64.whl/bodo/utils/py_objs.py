from numba.core import cgutils, types
from numba.extending import NativeValue, box, make_attribute_wrapper, models, register_model, typeof_impl, unbox


def install_py_obj_class(types_name, module, python_type=None, class_name=
    None, model_name=None):
    class_name = ''.join(map(str.title, types_name.split('_'))
        ) if class_name is None else class_name
    model_name = f'{class_name}Model' if model_name is None else model_name
    tseso__vqq = f'class {class_name}(types.Opaque):\n'
    tseso__vqq += f'    def __init__(self):\n'
    tseso__vqq += f"       types.Opaque.__init__(self, name='{class_name}')\n"
    tseso__vqq += f'    def __reduce__(self):\n'
    tseso__vqq += (
        f"        return (types.Opaque, ('{class_name}',), self.__dict__)\n")
    bfl__bmn = {}
    exec(tseso__vqq, {'types': types, 'models': models}, bfl__bmn)
    heouf__hdue = bfl__bmn[class_name]
    setattr(module, class_name, heouf__hdue)
    class_instance = heouf__hdue()
    setattr(types, types_name, class_instance)
    tseso__vqq = f'class {model_name}(models.StructModel):\n'
    tseso__vqq += f'    def __init__(self, dmm, fe_type):\n'
    tseso__vqq += f'        members = [\n'
    tseso__vqq += (
        f"            ('meminfo', types.MemInfoPointer({types_name})),\n")
    tseso__vqq += f"            ('pyobj', types.voidptr),\n"
    tseso__vqq += f'        ]\n'
    tseso__vqq += (
        f'        models.StructModel.__init__(self, dmm, fe_type, members)\n')
    exec(tseso__vqq, {'types': types, 'models': models, types_name:
        class_instance}, bfl__bmn)
    ngs__hai = bfl__bmn[model_name]
    setattr(module, model_name, ngs__hai)
    register_model(heouf__hdue)(ngs__hai)
    make_attribute_wrapper(heouf__hdue, 'pyobj', '_pyobj')
    if python_type is not None:
        typeof_impl.register(python_type)(lambda val, c: class_instance)
    unbox(heouf__hdue)(unbox_py_obj)
    box(heouf__hdue)(box_py_obj)
    return heouf__hdue


def box_py_obj(typ, val, c):
    vgya__xwe = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    obj = vgya__xwe.pyobj
    c.pyapi.incref(obj)
    c.context.nrt.decref(c.builder, typ, val)
    return obj


def unbox_py_obj(typ, obj, c):
    vgya__xwe = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vgya__xwe.meminfo = c.pyapi.nrt_meminfo_new_from_pyobject(c.context.
        get_constant_null(types.voidptr), obj)
    vgya__xwe.pyobj = obj
    return NativeValue(vgya__xwe._getvalue())
