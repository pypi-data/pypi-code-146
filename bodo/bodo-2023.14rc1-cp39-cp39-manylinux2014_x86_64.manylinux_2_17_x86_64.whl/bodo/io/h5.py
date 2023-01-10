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
        nnxs__rwi = self._get_h5_type(lhs, rhs)
        if nnxs__rwi is not None:
            wlirc__mhlx = str(nnxs__rwi.dtype)
            qbge__vrh = 'def _h5_read_impl(dset, index):\n'
            qbge__vrh += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(nnxs__rwi.ndim, wlirc__mhlx))
            awsld__eao = {}
            exec(qbge__vrh, {}, awsld__eao)
            ougve__twl = awsld__eao['_h5_read_impl']
            yeqw__ofex = compile_to_numba_ir(ougve__twl, {'bodo': bodo}
                ).blocks.popitem()[1]
            elzkv__enuo = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(yeqw__ofex, [rhs.value, elzkv__enuo])
            ziqpj__wyvxa = yeqw__ofex.body[:-3]
            ziqpj__wyvxa[-1].target = assign.target
            return ziqpj__wyvxa
        return None

    def _get_h5_type(self, lhs, rhs):
        nnxs__rwi = self._get_h5_type_locals(lhs)
        if nnxs__rwi is not None:
            return nnxs__rwi
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        elzkv__enuo = rhs.index if rhs.op == 'getitem' else rhs.index_var
        unir__gwgh = guard(find_const, self.func_ir, elzkv__enuo)
        require(not isinstance(unir__gwgh, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            qlzdd__rruz = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            jbgo__eant = get_const_value_inner(self.func_ir, qlzdd__rruz,
                arg_types=self.arg_types)
            obj_name_list.append(jbgo__eant)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        sse__jdyn = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        oqp__hsxd = h5py.File(sse__jdyn, 'r')
        aee__ndku = oqp__hsxd
        for jbgo__eant in obj_name_list:
            aee__ndku = aee__ndku[jbgo__eant]
        require(isinstance(aee__ndku, h5py.Dataset))
        icgn__iyo = len(aee__ndku.shape)
        qibo__cbsy = numba.np.numpy_support.from_dtype(aee__ndku.dtype)
        oqp__hsxd.close()
        return types.Array(qibo__cbsy, icgn__iyo, 'C')

    def _get_h5_type_locals(self, varname):
        lhe__lxh = self.locals.pop(varname, None)
        if lhe__lxh is None and varname is not None:
            lhe__lxh = self.flags.h5_types.get(varname, None)
        return lhe__lxh
