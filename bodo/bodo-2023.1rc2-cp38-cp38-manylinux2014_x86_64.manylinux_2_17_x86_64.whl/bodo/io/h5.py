"""
Analysis and transformation for HDF5 support.
"""
import types as pytypes
import numba
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, find_callname, find_const, get_definition, guard, replace_arg_nodes, require
import bodo
import bodo.io
from bodo.utils.transform import get_const_value_inner


class H5_IO:

    def __init__(self, func_ir, _locals, flags, arg_types):
        self.func_ir = func_ir
        self.locals = _locals
        self.flags = flags
        self.arg_types = arg_types

    def handle_possible_h5_read(self, assign, lhs, rhs):
        rha__zgt = self._get_h5_type(lhs, rhs)
        if rha__zgt is not None:
            yjhq__uwk = str(rha__zgt.dtype)
            hli__kgkoc = 'def _h5_read_impl(dset, index):\n'
            hli__kgkoc += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(rha__zgt.ndim, yjhq__uwk))
            tnf__doe = {}
            exec(hli__kgkoc, {}, tnf__doe)
            any__doag = tnf__doe['_h5_read_impl']
            jokp__gsoyp = compile_to_numba_ir(any__doag, {'bodo': bodo}
                ).blocks.popitem()[1]
            yxefj__onl = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(jokp__gsoyp, [rhs.value, yxefj__onl])
            uluc__btnsd = jokp__gsoyp.body[:-3]
            uluc__btnsd[-1].target = assign.target
            return uluc__btnsd
        return None

    def _get_h5_type(self, lhs, rhs):
        rha__zgt = self._get_h5_type_locals(lhs)
        if rha__zgt is not None:
            return rha__zgt
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        yxefj__onl = rhs.index if rhs.op == 'getitem' else rhs.index_var
        cyxa__prd = guard(find_const, self.func_ir, yxefj__onl)
        require(not isinstance(cyxa__prd, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            hki__fhwv = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            miym__ysxwi = get_const_value_inner(self.func_ir, hki__fhwv,
                arg_types=self.arg_types)
            obj_name_list.append(miym__ysxwi)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        vli__bujwu = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        ojy__zhvuz = h5py.File(vli__bujwu, 'r')
        qnvt__zkayb = ojy__zhvuz
        for miym__ysxwi in obj_name_list:
            qnvt__zkayb = qnvt__zkayb[miym__ysxwi]
        require(isinstance(qnvt__zkayb, h5py.Dataset))
        vnqnx__ogl = len(qnvt__zkayb.shape)
        qrgsm__jkju = numba.np.numpy_support.from_dtype(qnvt__zkayb.dtype)
        ojy__zhvuz.close()
        return types.Array(qrgsm__jkju, vnqnx__ogl, 'C')

    def _get_h5_type_locals(self, varname):
        zdnaj__lta = self.locals.pop(varname, None)
        if zdnaj__lta is None and varname is not None:
            zdnaj__lta = self.flags.h5_types.get(varname, None)
        return zdnaj__lta
