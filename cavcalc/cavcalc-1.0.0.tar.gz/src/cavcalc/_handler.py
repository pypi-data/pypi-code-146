from pint.errors import DimensionalityError, UndefinedUnitError

from . import _CONFIG, Q_
from ._arguments._container import _Arguments
from ._exiters import quit_print, bug
from .functions._maps import (
    RESONANCE_TARGETS_FUNC_MAP as _RES_TARGETS_MAP,
    SYMMETRIC_TARGETS_FUNC_MAP as _SYMM_TARGETS_MAP,
    ASYMMETRIC_TARGETS_FUNC_MAP as _ASYMM_TARGETS_MAP,
)
from .output import SingleOutput, MultiOutput
from .parameters import ArgParameter, TargetParameter, ParameterType
from .parameters.tools import get_name


def make_handler(args: _Arguments):
    if args.is_single_target:
        handler = _SingleTargetHandler(args)
    else:
        handler = _AllTargetHandler(args)

    return handler


class _Handler:
    def __init__(self, args: _Arguments):
        self.args = args

        self.is_symmetric = not any(
            (self.args.has(f"{name}1" or self.args.has(f"{name}2"))) for name in ("w", "Rc", "g")
        )

        # Make a copy to ensure we do not modify resonance's dependencies map itself!
        self.func_dep_map = _RES_TARGETS_MAP.copy()
        if self.is_symmetric:
            self.func_dep_map |= _SYMM_TARGETS_MAP
        else:
            self.func_dep_map |= _ASYMM_TARGETS_MAP

    def _get_computable_funcs(self):
        all_poss_computable_params = set(rp for _, rp in self.func_dep_map.values())

        def _update_computables(phys_arg_params: set[ParameterType]):
            computables = {}
            for target in all_poss_computable_params:
                if target in phys_arg_params or target in computables:
                    continue

                for func, (reqd_params, ret_param) in self.func_dep_map.items():
                    if ret_param == target:
                        if not set(reqd_params).difference(phys_arg_params):
                            if computables.get(ret_param):
                                quit_print(
                                    "Incompatible arguments detected! The parameter "
                                    f"'{get_name(ret_param)}' can be computed multiple different ways "
                                    "based on the arguments given."
                                )

                            computables[ret_param] = func

            return computables

        computable_funcs = {}
        available_params = set(self.args.physical_args.keys())
        # Keep updating the physical argument parameter set using
        # the functions we just determined could be computed. This
        # let's us chain together many targets from a relatively
        # sparse initial set of given arguments.
        while new_funcs := _update_computables(available_params):
            computable_funcs |= new_funcs
            available_params |= new_funcs.keys()

        return computable_funcs


class _SingleTargetHandler(_Handler):
    def __init__(self, args: _Arguments):
        super().__init__(args)
        phys_arg_params = set(self.args.physical_args.keys())
        self.target_parameter = TargetParameter(self.args.compute)

        # Get the functions which have target parameter as return
        target_functions = {
            func: (reqd_params, ret_param)
            for func, (reqd_params, ret_param) in self.func_dep_map.items()
            if ret_param == self.target_parameter.ptype
        }

        def _find_target_func():
            return next(
                (
                    func
                    for func, (reqd_params, _) in target_functions.items()
                    if not set(reqd_params).difference(phys_arg_params)
                ),
                None,
            )

        self.target_function = _find_target_func()
        if self.target_function is None:  # couldn't compute it directly, so let's do chaining
            # First step of chaining logic is to get the functions that we *can*
            # compute from both our initial arg set and the extra chained args
            # themselves as we add them
            computable_funcs = self._get_computable_funcs()
            phys_arg_params |= computable_funcs.keys()

            self.target_function = _find_target_func()
            if self.target_function:
                reqd_params, _ = self.func_dep_map[self.target_function]
                # Which chained targets do we need to compute?
                diff = set(reqd_params).difference(self.args.physical_args.keys())
                self.chained = {}
                for pd in diff:  # calculate each of these in-turn...
                    chained_func = computable_funcs[pd]
                    chained_reqd, _ = self.func_dep_map[chained_func]
                    chained_func_args = tuple(
                        self.args.physical_args.get(p) or self.chained.get(p) for p in chained_reqd
                    )
                    # ... storing them as chained ArgParameter instances, for
                    # easy use when calculating self.target_function later on
                    self.chained[pd] = ArgParameter(pd, compute(chained_func, *chained_func_args))
            else:
                msg = f"Incorrect usage. To compute {self.args.compute} I require one of: "
                all_maps = _RES_TARGETS_MAP | _SYMM_TARGETS_MAP | _ASYMM_TARGETS_MAP
                for reqd_params, ret_param in all_maps.values():
                    if ret_param == self.target_parameter.ptype:
                        msg += "\n\t"
                        msg += " AND ".join(
                            ArgParameter(param).cli_form
                            if param != ParameterType.WAVELENGTH
                            else f"[-wl = {self.args.wl.value:~}]"
                            for param in reqd_params
                        )

                msg += (
                    "\n\nOR a combination of parameters which allows one of "
                    "the above sets to be computed."
                )
                quit_print(msg)

    def run(self):
        reqd_params, _ = self.func_dep_map[self.target_function]
        func_args = tuple(
            self.args.physical_args.get(p) or self.chained.get(p) for p in reqd_params
        )

        result = compute(self.target_function, *func_args)
        if not self.target_parameter.is_unitless:
            units = self.args["units"] or _CONFIG["units"].get(self.target_parameter.name)
            try:
                result = result.to(units)
            except (DimensionalityError, UndefinedUnitError, ValueError) as ex:
                quit_print(str(ex))

        self.target_parameter = TargetParameter(self.target_parameter.name, result)
        return SingleOutput(self.target_parameter, tuple(self.args.physical_args.values()))


class _AllTargetHandler(_Handler):
    def __init__(self, args):
        super().__init__(args)

        # Get all the targets that we can compute from both the initial
        # argument set and the extra chained targets
        self.target_functions = tuple(self._get_computable_funcs().values())

    def run(self):
        computed_targets: dict[TargetParameter, tuple[ParameterType]] = {}
        for func in self.target_functions:
            reqd_params, ret_param = self.func_dep_map[func]
            func_args = tuple(
                (
                    self.args.physical_args.get(p)
                    or next((arg for arg in computed_targets.keys() if arg.ptype == p))
                )
                for p in reqd_params
            )

            target_param = TargetParameter(ret_param)

            result = compute(func, *func_args)
            if not target_param.is_unitless:
                units = self.args["units"] or _CONFIG["units"].get(target_param.name)
                try:
                    result = result.to(units)
                except (DimensionalityError, UndefinedUnitError, ValueError) as ex:
                    quit_print(str(ex))

            target_param = TargetParameter(ret_param, result)
            computed_targets[target_param] = reqd_params

        to_update = {}
        for tgt_p, reqd_params in computed_targets.items():
            for rp in reqd_params:
                # A required parameter was not specified, so it must be a chained target...
                if rp not in self.args.physical_args:
                    # ... find this target and get *its* required params
                    chained_target = next((tp for tp in computed_targets if tp.ptype == rp), None)
                    if not chained_target:
                        bug(f"Could not find chained target parameter corresponding to {rp}")

                    chained_tgt_reqd_params = computed_targets[chained_target]
                    # Now get the chained target required params which *were* specified...
                    extra_params = tuple(
                        filter(lambda p: p in self.args.physical_args, chained_tgt_reqd_params)
                    )
                    # ... and add them as chained extra required params
                    if extra_params:
                        if tgt_p in to_update:
                            to_update[tgt_p] += extra_params
                        else:
                            to_update[tgt_p] = extra_params

        # These chained target parameter types are then added to the relevant
        # target mappings as extra "required" params, so that we can correctly
        # construct SingleOutput instances from within the MultiOutput
        for tgt_p, extras in to_update.items():
            computed_targets[tgt_p] = tuple(set(computed_targets[tgt_p] + extras))

        return MultiOutput(computed_targets, tuple(self.args.physical_args.values()))


def compute(func, *args) -> Q_:
    try:
        return func(*(arg_p.value for arg_p in args))
    except Exception as ex:
        if isinstance(ex, ValueError) and "operands could not be broadcast" in str(ex):
            shapes = (str(getattr(arg_p.value.m, "shape", 1)) for arg_p in args)
            quit_print(
                f"Encountered inconsistent parameter shapes when calling {func.__name__}. "
                f"Parameters: {{{', '.join(arg_p.name for arg_p in args)}}}, with shapes: "
                f"{{{', '.join(shapes)}}}, could not be broadcast together."
            )
        else:
            bug(
                "The following error occurred:\n\n"
                f"\t{ex}\n\n"
                f"when calling {func.__name__} with arguments:\n\n"
                + "\n\t".join(arg_p.compact_str for arg_p in args)
            )
