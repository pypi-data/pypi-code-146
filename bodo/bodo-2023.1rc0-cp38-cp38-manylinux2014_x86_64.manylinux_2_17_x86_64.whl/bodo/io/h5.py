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
        wzq__zzrfw = self._get_h5_type(lhs, rhs)
        if wzq__zzrfw is not None:
            mei__ifp = str(wzq__zzrfw.dtype)
            oayp__wzbn = 'def _h5_read_impl(dset, index):\n'
            oayp__wzbn += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(wzq__zzrfw.ndim, mei__ifp))
            iwz__nwkfo = {}
            exec(oayp__wzbn, {}, iwz__nwkfo)
            gtcfd__rbqr = iwz__nwkfo['_h5_read_impl']
            bmuqd__lvfyv = compile_to_numba_ir(gtcfd__rbqr, {'bodo': bodo}
                ).blocks.popitem()[1]
            gjv__zxlqb = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(bmuqd__lvfyv, [rhs.value, gjv__zxlqb])
            rtu__aao = bmuqd__lvfyv.body[:-3]
            rtu__aao[-1].target = assign.target
            return rtu__aao
        return None

    def _get_h5_type(self, lhs, rhs):
        wzq__zzrfw = self._get_h5_type_locals(lhs)
        if wzq__zzrfw is not None:
            return wzq__zzrfw
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        gjv__zxlqb = rhs.index if rhs.op == 'getitem' else rhs.index_var
        hcgo__auf = guard(find_const, self.func_ir, gjv__zxlqb)
        require(not isinstance(hcgo__auf, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            xmwd__mnqei = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            bmxms__usdea = get_const_value_inner(self.func_ir, xmwd__mnqei,
                arg_types=self.arg_types)
            obj_name_list.append(bmxms__usdea)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        eknbj__yze = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        sve__mbos = h5py.File(eknbj__yze, 'r')
        uncdd__imsie = sve__mbos
        for bmxms__usdea in obj_name_list:
            uncdd__imsie = uncdd__imsie[bmxms__usdea]
        require(isinstance(uncdd__imsie, h5py.Dataset))
        uqc__rbmh = len(uncdd__imsie.shape)
        qbl__saikp = numba.np.numpy_support.from_dtype(uncdd__imsie.dtype)
        sve__mbos.close()
        return types.Array(qbl__saikp, uqc__rbmh, 'C')

    def _get_h5_type_locals(self, varname):
        rak__izem = self.locals.pop(varname, None)
        if rak__izem is None and varname is not None:
            rak__izem = self.flags.h5_types.get(varname, None)
        return rak__izem
