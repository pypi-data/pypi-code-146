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
    pofl__tfz = context.get_python_api(builder)
    return pofl__tfz.unserialize(pofl__tfz.serialize_object(pyval))


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
        yept__jqd = ', '.join('e{}'.format(mjr__sva) for mjr__sva in range(
            len(args)))
        if yept__jqd:
            yept__jqd += ', '
        hsum__ayktl = ', '.join("{} = ''".format(nrmsa__qggpv) for
            nrmsa__qggpv in kws.keys())
        syvh__bee = f'def format_stub(string, {yept__jqd} {hsum__ayktl}):\n'
        syvh__bee += '    pass\n'
        gzlja__dywk = {}
        exec(syvh__bee, {}, gzlja__dywk)
        rjdsn__ikwc = gzlja__dywk['format_stub']
        gkh__abz = numba.core.utils.pysignature(rjdsn__ikwc)
        zue__poe = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, zue__poe).replace(pysig=gkh__abz)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for myxx__ytk in ('logging.Logger', 'logging.RootLogger'):
        for khxke__jox in func_names:
            opq__mdd = f'@bound_function("{myxx__ytk}.{khxke__jox}")\n'
            opq__mdd += (
                f'def resolve_{khxke__jox}(self, logger_typ, args, kws):\n')
            opq__mdd += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(opq__mdd)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for pmctu__johqv in logging_logger_unsupported_attrs:
        ykmlf__rna = 'logging.Logger.' + pmctu__johqv
        overload_attribute(LoggingLoggerType, pmctu__johqv)(
            create_unsupported_overload(ykmlf__rna))
    for xhd__hip in logging_logger_unsupported_methods:
        ykmlf__rna = 'logging.Logger.' + xhd__hip
        overload_method(LoggingLoggerType, xhd__hip)(
            create_unsupported_overload(ykmlf__rna))


_install_logging_logger_unsupported_objects()
