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
        deg__ljjlk = self._get_h5_type(lhs, rhs)
        if deg__ljjlk is not None:
            fxr__woznd = str(deg__ljjlk.dtype)
            rcarv__rgrwy = 'def _h5_read_impl(dset, index):\n'
            rcarv__rgrwy += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(deg__ljjlk.ndim, fxr__woznd))
            iho__xwbu = {}
            exec(rcarv__rgrwy, {}, iho__xwbu)
            zlsma__mdq = iho__xwbu['_h5_read_impl']
            xsp__gldng = compile_to_numba_ir(zlsma__mdq, {'bodo': bodo}
                ).blocks.popitem()[1]
            oqw__tipzi = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(xsp__gldng, [rhs.value, oqw__tipzi])
            ewh__gqbk = xsp__gldng.body[:-3]
            ewh__gqbk[-1].target = assign.target
            return ewh__gqbk
        return None

    def _get_h5_type(self, lhs, rhs):
        deg__ljjlk = self._get_h5_type_locals(lhs)
        if deg__ljjlk is not None:
            return deg__ljjlk
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        oqw__tipzi = rhs.index if rhs.op == 'getitem' else rhs.index_var
        wcrxq__quw = guard(find_const, self.func_ir, oqw__tipzi)
        require(not isinstance(wcrxq__quw, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            pnr__caha = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            tbiu__llmgo = get_const_value_inner(self.func_ir, pnr__caha,
                arg_types=self.arg_types)
            obj_name_list.append(tbiu__llmgo)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        fyhsk__njwce = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        xqeol__vab = h5py.File(fyhsk__njwce, 'r')
        jpj__dturo = xqeol__vab
        for tbiu__llmgo in obj_name_list:
            jpj__dturo = jpj__dturo[tbiu__llmgo]
        require(isinstance(jpj__dturo, h5py.Dataset))
        mdx__aty = len(jpj__dturo.shape)
        tfgzk__zpeda = numba.np.numpy_support.from_dtype(jpj__dturo.dtype)
        xqeol__vab.close()
        return types.Array(tfgzk__zpeda, mdx__aty, 'C')

    def _get_h5_type_locals(self, varname):
        htgvn__atkge = self.locals.pop(varname, None)
        if htgvn__atkge is None and varname is not None:
            htgvn__atkge = self.flags.h5_types.get(varname, None)
        return htgvn__atkge
