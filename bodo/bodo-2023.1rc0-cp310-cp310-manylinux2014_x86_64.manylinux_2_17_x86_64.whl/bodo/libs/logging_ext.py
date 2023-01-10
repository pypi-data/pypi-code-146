"""
JIT support for Python's logging module
"""
import logging
import numba
from numba.core import types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import bound_function
from numba.core.typing.templates import AttributeTemplate, infer_getattr, signature
from numba.extending import NativeValue, box, models, overload_attribute, overload_method, register_model, typeof_impl, unbox
from bodo.utils.typing import create_unsupported_overload, gen_objmode_attr_overload


class LoggingLoggerType(types.Type):

    def __init__(self, is_root=False):
        self.is_root = is_root
        super(LoggingLoggerType, self).__init__(name=
            f'LoggingLoggerType(is_root={is_root})')


@typeof_impl.register(logging.RootLogger)
@typeof_impl.register(logging.Logger)
def typeof_logging(val, c):
    if isinstance(val, logging.RootLogger):
        return LoggingLoggerType(is_root=True)
    else:
        return LoggingLoggerType(is_root=False)


register_model(LoggingLoggerType)(models.OpaqueModel)


@box(LoggingLoggerType)
def box_logging_logger(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(LoggingLoggerType)
def unbox_logging_logger(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@lower_constant(LoggingLoggerType)
def lower_constant_logger(context, builder, ty, pyval):
    bbixp__aueq = context.get_python_api(builder)
    return bbixp__aueq.unserialize(bbixp__aueq.serialize_object(pyval))


gen_objmode_attr_overload(LoggingLoggerType, 'level', None, types.int64)
gen_objmode_attr_overload(LoggingLoggerType, 'name', None, 'unicode_type')
gen_objmode_attr_overload(LoggingLoggerType, 'propagate', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'disabled', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'parent', None,
    LoggingLoggerType())
gen_objmode_attr_overload(LoggingLoggerType, 'root', None,
    LoggingLoggerType(is_root=True))


@infer_getattr
class LoggingLoggerAttribute(AttributeTemplate):
    key = LoggingLoggerType

    def _resolve_helper(self, logger_typ, args, kws):
        kws = dict(kws)
        btj__gvc = ', '.join('e{}'.format(ptzuw__unjv) for ptzuw__unjv in
            range(len(args)))
        if btj__gvc:
            btj__gvc += ', '
        pilw__vgkhh = ', '.join("{} = ''".format(vyyl__qcfz) for vyyl__qcfz in
            kws.keys())
        lqx__rjlgd = f'def format_stub(string, {btj__gvc} {pilw__vgkhh}):\n'
        lqx__rjlgd += '    pass\n'
        dcwr__crwg = {}
        exec(lqx__rjlgd, {}, dcwr__crwg)
        cbxy__hfgra = dcwr__crwg['format_stub']
        xznqc__jyavk = numba.core.utils.pysignature(cbxy__hfgra)
        jnzwd__navt = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, jnzwd__navt).replace(pysig=xznqc__jyavk)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for lon__fhjc in ('logging.Logger', 'logging.RootLogger'):
        for lcz__fhtj in func_names:
            zumz__qkecg = f'@bound_function("{lon__fhjc}.{lcz__fhtj}")\n'
            zumz__qkecg += (
                f'def resolve_{lcz__fhtj}(self, logger_typ, args, kws):\n')
            zumz__qkecg += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(zumz__qkecg)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for jjex__mrp in logging_logger_unsupported_attrs:
        xrje__osudz = 'logging.Logger.' + jjex__mrp
        overload_attribute(LoggingLoggerType, jjex__mrp)(
            create_unsupported_overload(xrje__osudz))
    for qrr__mehr in logging_logger_unsupported_methods:
        xrje__osudz = 'logging.Logger.' + qrr__mehr
        overload_method(LoggingLoggerType, qrr__mehr)(
            create_unsupported_overload(xrje__osudz))


_install_logging_logger_unsupported_objects()
