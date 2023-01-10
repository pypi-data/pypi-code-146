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
    vrbp__pqyq = context.get_python_api(builder)
    return vrbp__pqyq.unserialize(vrbp__pqyq.serialize_object(pyval))


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
        guayi__bbuy = ', '.join('e{}'.format(ssizr__pov) for ssizr__pov in
            range(len(args)))
        if guayi__bbuy:
            guayi__bbuy += ', '
        tergy__tzlua = ', '.join("{} = ''".format(rlmmj__xip) for
            rlmmj__xip in kws.keys())
        obneq__xtulz = (
            f'def format_stub(string, {guayi__bbuy} {tergy__tzlua}):\n')
        obneq__xtulz += '    pass\n'
        sjoza__dzusq = {}
        exec(obneq__xtulz, {}, sjoza__dzusq)
        wge__ithq = sjoza__dzusq['format_stub']
        zliez__vsf = numba.core.utils.pysignature(wge__ithq)
        kqz__dgmoj = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, kqz__dgmoj).replace(pysig=zliez__vsf)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for uvph__xdr in ('logging.Logger', 'logging.RootLogger'):
        for dauy__xjbsq in func_names:
            izxu__jitn = f'@bound_function("{uvph__xdr}.{dauy__xjbsq}")\n'
            izxu__jitn += (
                f'def resolve_{dauy__xjbsq}(self, logger_typ, args, kws):\n')
            izxu__jitn += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(izxu__jitn)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for exw__vtbp in logging_logger_unsupported_attrs:
        zthqc__trx = 'logging.Logger.' + exw__vtbp
        overload_attribute(LoggingLoggerType, exw__vtbp)(
            create_unsupported_overload(zthqc__trx))
    for hfdgp__vigh in logging_logger_unsupported_methods:
        zthqc__trx = 'logging.Logger.' + hfdgp__vigh
        overload_method(LoggingLoggerType, hfdgp__vigh)(
            create_unsupported_overload(zthqc__trx))


_install_logging_logger_unsupported_objects()
