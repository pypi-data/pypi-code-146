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
    hvk__hnp = context.get_python_api(builder)
    return hvk__hnp.unserialize(hvk__hnp.serialize_object(pyval))


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
        pje__ttq = ', '.join('e{}'.format(uwigj__tlcw) for uwigj__tlcw in
            range(len(args)))
        if pje__ttq:
            pje__ttq += ', '
        kjbj__kjpwv = ', '.join("{} = ''".format(lqx__adh) for lqx__adh in
            kws.keys())
        bvvt__gcets = f'def format_stub(string, {pje__ttq} {kjbj__kjpwv}):\n'
        bvvt__gcets += '    pass\n'
        wxp__mskk = {}
        exec(bvvt__gcets, {}, wxp__mskk)
        nsyej__hno = wxp__mskk['format_stub']
        vmby__euo = numba.core.utils.pysignature(nsyej__hno)
        dhjv__cwx = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, dhjv__cwx).replace(pysig=vmby__euo)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for jbt__gej in ('logging.Logger', 'logging.RootLogger'):
        for xdc__tmzpf in func_names:
            tvr__kfcy = f'@bound_function("{jbt__gej}.{xdc__tmzpf}")\n'
            tvr__kfcy += (
                f'def resolve_{xdc__tmzpf}(self, logger_typ, args, kws):\n')
            tvr__kfcy += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(tvr__kfcy)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for caw__edjl in logging_logger_unsupported_attrs:
        mhv__uskq = 'logging.Logger.' + caw__edjl
        overload_attribute(LoggingLoggerType, caw__edjl)(
            create_unsupported_overload(mhv__uskq))
    for cppzz__uiu in logging_logger_unsupported_methods:
        mhv__uskq = 'logging.Logger.' + cppzz__uiu
        overload_method(LoggingLoggerType, cppzz__uiu)(
            create_unsupported_overload(mhv__uskq))


_install_logging_logger_unsupported_objects()
