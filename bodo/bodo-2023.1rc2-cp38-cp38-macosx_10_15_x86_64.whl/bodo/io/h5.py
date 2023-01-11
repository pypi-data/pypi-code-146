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
        ozo__fpdet = self._get_h5_type(lhs, rhs)
        if ozo__fpdet is not None:
            twjyg__ivtdn = str(ozo__fpdet.dtype)
            yaalw__cwqzk = 'def _h5_read_impl(dset, index):\n'
            yaalw__cwqzk += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(ozo__fpdet.ndim, twjyg__ivtdn))
            rzrbl__nmw = {}
            exec(yaalw__cwqzk, {}, rzrbl__nmw)
            uexwc__lrjm = rzrbl__nmw['_h5_read_impl']
            ljp__nxyxz = compile_to_numba_ir(uexwc__lrjm, {'bodo': bodo}
                ).blocks.popitem()[1]
            zjk__exb = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(ljp__nxyxz, [rhs.value, zjk__exb])
            ixe__kmkjf = ljp__nxyxz.body[:-3]
            ixe__kmkjf[-1].target = assign.target
            return ixe__kmkjf
        return None

    def _get_h5_type(self, lhs, rhs):
        ozo__fpdet = self._get_h5_type_locals(lhs)
        if ozo__fpdet is not None:
            return ozo__fpdet
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        zjk__exb = rhs.index if rhs.op == 'getitem' else rhs.index_var
        xnzp__ndyc = guard(find_const, self.func_ir, zjk__exb)
        require(not isinstance(xnzp__ndyc, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            jtodk__svzhv = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            mfnjy__zps = get_const_value_inner(self.func_ir, jtodk__svzhv,
                arg_types=self.arg_types)
            obj_name_list.append(mfnjy__zps)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        nsgk__zjui = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        anhsc__jwr = h5py.File(nsgk__zjui, 'r')
        licu__tpeu = anhsc__jwr
        for mfnjy__zps in obj_name_list:
            licu__tpeu = licu__tpeu[mfnjy__zps]
        require(isinstance(licu__tpeu, h5py.Dataset))
        gaaw__rrsv = len(licu__tpeu.shape)
        akuw__phfq = numba.np.numpy_support.from_dtype(licu__tpeu.dtype)
        anhsc__jwr.close()
        return types.Array(akuw__phfq, gaaw__rrsv, 'C')

    def _get_h5_type_locals(self, varname):
        pzujq__ysc = self.locals.pop(varname, None)
        if pzujq__ysc is None and varname is not None:
            pzujq__ysc = self.flags.h5_types.get(varname, None)
        return pzujq__ysc
