from numba.core import cgutils, types
from numba.extending import NativeValue, box, make_attribute_wrapper, models, register_model, typeof_impl, unbox


def install_py_obj_class(types_name, module, python_type=None, class_name=
    None, model_name=None):
    class_name = ''.join(map(str.title, types_name.split('_'))
        ) if class_name is None else class_name
    model_name = f'{class_name}Model' if model_name is None else model_name
    fxa__pcsgh = f'class {class_name}(types.Opaque):\n'
    fxa__pcsgh += f'    def __init__(self):\n'
    fxa__pcsgh += f"       types.Opaque.__init__(self, name='{class_name}')\n"
    fxa__pcsgh += f'    def __reduce__(self):\n'
    fxa__pcsgh += (
        f"        return (types.Opaque, ('{class_name}',), self.__dict__)\n")
    egm__nrde = {}
    exec(fxa__pcsgh, {'types': types, 'models': models}, egm__nrde)
    wwi__bgsfe = egm__nrde[class_name]
    setattr(module, class_name, wwi__bgsfe)
    class_instance = wwi__bgsfe()
    setattr(types, types_name, class_instance)
    fxa__pcsgh = f'class {model_name}(models.StructModel):\n'
    fxa__pcsgh += f'    def __init__(self, dmm, fe_type):\n'
    fxa__pcsgh += f'        members = [\n'
    fxa__pcsgh += (
        f"            ('meminfo', types.MemInfoPointer({types_name})),\n")
    fxa__pcsgh += f"            ('pyobj', types.voidptr),\n"
    fxa__pcsgh += f'        ]\n'
    fxa__pcsgh += (
        f'        models.StructModel.__init__(self, dmm, fe_type, members)\n')
    exec(fxa__pcsgh, {'types': types, 'models': models, types_name:
        class_instance}, egm__nrde)
    wtwi__cqo = egm__nrde[model_name]
    setattr(module, model_name, wtwi__cqo)
    register_model(wwi__bgsfe)(wtwi__cqo)
    make_attribute_wrapper(wwi__bgsfe, 'pyobj', '_pyobj')
    if python_type is not None:
        typeof_impl.register(python_type)(lambda val, c: class_instance)
    unbox(wwi__bgsfe)(unbox_py_obj)
    box(wwi__bgsfe)(box_py_obj)
    return wwi__bgsfe


def box_py_obj(typ, val, c):
    rjgur__qdhtk = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    obj = rjgur__qdhtk.pyobj
    c.pyapi.incref(obj)
    c.context.nrt.decref(c.builder, typ, val)
    return obj


def unbox_py_obj(typ, obj, c):
    rjgur__qdhtk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    rjgur__qdhtk.meminfo = c.pyapi.nrt_meminfo_new_from_pyobject(c.context.
        get_constant_null(types.voidptr), obj)
    rjgur__qdhtk.pyobj = obj
    return NativeValue(rjgur__qdhtk._getvalue())
