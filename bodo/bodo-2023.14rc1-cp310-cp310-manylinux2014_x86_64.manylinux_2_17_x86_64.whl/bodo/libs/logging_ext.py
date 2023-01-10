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
    eoktp__omyrz = context.get_python_api(builder)
    return eoktp__omyrz.unserialize(eoktp__omyrz.serialize_object(pyval))


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
        jkpf__ric = ', '.join('e{}'.format(xqzh__ujiz) for xqzh__ujiz in
            range(len(args)))
        if jkpf__ric:
            jkpf__ric += ', '
        wsa__blv = ', '.join("{} = ''".format(awg__zoi) for awg__zoi in kws
            .keys())
        jak__xor = f'def format_stub(string, {jkpf__ric} {wsa__blv}):\n'
        jak__xor += '    pass\n'
        beafk__zbixn = {}
        exec(jak__xor, {}, beafk__zbixn)
        irr__vktmv = beafk__zbixn['format_stub']
        cccri__bmp = numba.core.utils.pysignature(irr__vktmv)
        bxzyj__tqlqm = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, bxzyj__tqlqm).replace(pysig=cccri__bmp)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for cplzz__led in ('logging.Logger', 'logging.RootLogger'):
        for deg__uqcg in func_names:
            lhnv__ryoyb = f'@bound_function("{cplzz__led}.{deg__uqcg}")\n'
            lhnv__ryoyb += (
                f'def resolve_{deg__uqcg}(self, logger_typ, args, kws):\n')
            lhnv__ryoyb += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(lhnv__ryoyb)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for uccw__ixzbq in logging_logger_unsupported_attrs:
        ylq__xkh = 'logging.Logger.' + uccw__ixzbq
        overload_attribute(LoggingLoggerType, uccw__ixzbq)(
            create_unsupported_overload(ylq__xkh))
    for gva__nzxkq in logging_logger_unsupported_methods:
        ylq__xkh = 'logging.Logger.' + gva__nzxkq
        overload_method(LoggingLoggerType, gva__nzxkq)(
            create_unsupported_overload(ylq__xkh))


_install_logging_logger_unsupported_objects()
