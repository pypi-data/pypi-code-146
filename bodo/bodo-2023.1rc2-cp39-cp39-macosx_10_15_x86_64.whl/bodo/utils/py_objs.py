from numba.core import cgutils, types
from numba.extending import NativeValue, box, make_attribute_wrapper, models, register_model, typeof_impl, unbox


def install_py_obj_class(types_name, module, python_type=None, class_name=
    None, model_name=None):
    class_name = ''.join(map(str.title, types_name.split('_'))
        ) if class_name is None else class_name
    model_name = f'{class_name}Model' if model_name is None else model_name
    pfa__szrr = f'class {class_name}(types.Opaque):\n'
    pfa__szrr += f'    def __init__(self):\n'
    pfa__szrr += f"       types.Opaque.__init__(self, name='{class_name}')\n"
    pfa__szrr += f'    def __reduce__(self):\n'
    pfa__szrr += (
        f"        return (types.Opaque, ('{class_name}',), self.__dict__)\n")
    zpi__fve = {}
    exec(pfa__szrr, {'types': types, 'models': models}, zpi__fve)
    qycb__mak = zpi__fve[class_name]
    setattr(module, class_name, qycb__mak)
    class_instance = qycb__mak()
    setattr(types, types_name, class_instance)
    pfa__szrr = f'class {model_name}(models.StructModel):\n'
    pfa__szrr += f'    def __init__(self, dmm, fe_type):\n'
    pfa__szrr += f'        members = [\n'
    pfa__szrr += (
        f"            ('meminfo', types.MemInfoPointer({types_name})),\n")
    pfa__szrr += f"            ('pyobj', types.voidptr),\n"
    pfa__szrr += f'        ]\n'
    pfa__szrr += (
        f'        models.StructModel.__init__(self, dmm, fe_type, members)\n')
    exec(pfa__szrr, {'types': types, 'models': models, types_name:
        class_instance}, zpi__fve)
    tws__dqdp = zpi__fve[model_name]
    setattr(module, model_name, tws__dqdp)
    register_model(qycb__mak)(tws__dqdp)
    make_attribute_wrapper(qycb__mak, 'pyobj', '_pyobj')
    if python_type is not None:
        typeof_impl.register(python_type)(lambda val, c: class_instance)
    unbox(qycb__mak)(unbox_py_obj)
    box(qycb__mak)(box_py_obj)
    return qycb__mak


def box_py_obj(typ, val, c):
    dwsc__yhd = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    obj = dwsc__yhd.pyobj
    c.pyapi.incref(obj)
    c.context.nrt.decref(c.builder, typ, val)
    return obj


def unbox_py_obj(typ, obj, c):
    dwsc__yhd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    dwsc__yhd.meminfo = c.pyapi.nrt_meminfo_new_from_pyobject(c.context.
        get_constant_null(types.voidptr), obj)
    dwsc__yhd.pyobj = obj
    return NativeValue(dwsc__yhd._getvalue())
