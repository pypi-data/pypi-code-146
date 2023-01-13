import numpy as np
import warnings

from .. import Q_
from .._exiters import quit_print
from ..parameters import ArgParameter, ParameterType


# TODO (sjr) Should probably add a decorator to enable freezing of instances of
#            this, and set it to frozen in _CavCalcSession.parse_args after
#            parsing the arguments into it.
class _Arguments:
    def __init__(self):
        self.__physical_args = {}

    @property
    def physical_args(self) -> dict[ParameterType, ArgParameter]:
        return self.__physical_args

    @property
    def is_all_target(self) -> bool:
        return self["compute"] == "all"

    @property
    def is_single_target(self) -> bool:
        return not self.is_all_target

    def __getitem__(self, argname: str):
        return getattr(self, argname)

    def has(self, argname: str) -> bool:
        """Checks that `argname` was specified as one of the arguments, and so
        is held by this namespace-like object."""
        return getattr(self, argname, None) is not None

    def process(self, arg_orders: dict[str, int]):
        filter_phys_args = lambda: {name: v for name, v in vars(self).items() if isinstance(v, Q_)}
        phys_args = filter_phys_args()

        # Construct mesh-grids from these parameters in the order specified
        axis_orders = {}
        if self.mesh:
            if isinstance(self.mesh, bool):
                auto_mesh = tuple(
                    name for name in arg_orders.keys() if isinstance(phys_args[name].m, np.ndarray)
                )
                if not auto_mesh:
                    warnings.warn("Ignoring mesh argument, as no parameters are array-like.")

                self.mesh = (auto_mesh,)

            for param_combo in self.mesh:
                if len(param_combo) == 1:
                    pname = param_combo[0]
                    axis_orders[pname] = 0
                    warnings.warn(f"Ignoring single parameter '{pname}' in mesh.")
                    continue

                try:
                    arg_ps = tuple(phys_args[pname] for pname in param_combo)
                except KeyError as ex:
                    quit_print(f"Mesh parameter {str(ex)} was not specified!")

                if any(not isinstance(p.m, np.ndarray) for p in arg_ps):
                    quit_print(
                        "One or more of the specified mesh parameters is not array-like! Cannot "
                        "construct a mesh-grid from scalar arguments."
                    )
                meshes = np.meshgrid(*(arg_p.m for arg_p in arg_ps), indexing="ij")
                for i, (pname, mesh) in enumerate(zip(param_combo, meshes)):
                    setattr(self, pname, Q_(mesh, phys_args[pname].units))
                    axis_orders[pname] = i

            # For the remaining array-like args, which were not in any mesh combination, just
            # set the axis number to the *current* number of entries in axis_orders
            n_axes = len(axis_orders)
            for pname, v in phys_args.items():
                if pname not in axis_orders and isinstance(v.m, np.ndarray):
                    axis_orders[pname] = n_axes

            # Re-construct physical args dict, as we've now modified attributes
            phys_args = filter_phys_args()
        else:
            for pname, v in phys_args.items():
                if isinstance(v.m, np.ndarray):
                    axis_orders[pname] = 0

        # Make Parameter instances for each physical argument given
        for name, q in phys_args.items():
            param_obj = ArgParameter(
                name, q, index=arg_orders.get(name), axis=axis_orders.get(name)
            )
            setattr(self, name, param_obj)
            self.__physical_args[param_obj.ptype] = param_obj

        for m in (1, 2):
            # Set the loss arguments to zero if either of R<m>, T<m> given but L<m> not
            if (self.has(f"R{m}") or self.has(f"T{m}")) and not self.has(f"L{m}"):
                Lm = ArgParameter(f"L{m}", Q_(0))
                setattr(self, f"L{m}", Lm)
                self.__physical_args[Lm.ptype] = Lm

    def verify(self):
        """Checks that the arguments held by this namespace-like object make sense
        and are consistent with one another."""
        if self.has("units"):
            if self.is_all_target:
                quit_print(
                    "Specifying output units is only supported in single target mode. Use "
                    "a 'cavcalc.ini' config file to override units in multi target mode, or "
                    "interact with cavcalc via the Python API for tasks requiring more "
                    "customisation."
                )

        if self.has("loadfile") and self.physical_args:
            # We will always have wavelength in the physical_args as this takes on a default value
            if tuple(self.physical_args.keys()) != (ParameterType.WAVELENGTH,):
                quit_print(
                    "You cannot give physical parameter arguments when loading a "
                    "serialized cavcalc output object."
                )

        self.verify_physical_parameters()

    def verify_physical_parameters(self):
        if self.has("T1") and self.has("R1"):
            quit_print(
                "Incorrect usage! Cannot specify both reflectivity and transmission of first mirror."
            )
        if self.has("T2") and self.has("R2"):
            quit_print(
                "Incorrect usage! Cannot specify both reflectivity and transmission of second mirror."
            )

        # Check {R, T, L} are within [0, 1] for both mirrors
        for p in "R", "T", "L":
            for m in (1, 2):
                if self.has(f"{p}{m}"):
                    v = self[f"{p}{m}"].value.m
                    if np.any((v < 0) | (v > 1)):
                        quit_print(f"{p}{m} is invalid. Value(s) must satisfy 0 <= {p} <= 1.")

        # And, if necessary, check {(R + L) | (T + L)} < 1 for both mirrors too
        for p in "R", "T":
            for m in (1, 2):
                if (Pm := self[f"{p}{m}"]) and (Lm := self[f"L{m}"]):
                    Pv = Pm.value.m
                    Lv = Lm.value.m
                    try:
                        if np.any((Pv + Lv) > 1):
                            quit_print(
                                f"Invalid combination of {p}{m} and L{m} given. Value(s) "
                                f"must satisfy {p} + L <= 1."
                            )
                    except ValueError:
                        quit_print(
                            f"Encountered inconsistent array shapes for {p}{m} and L{m}, with "
                            f"shapes: {Pv.shape}, {Lv.shape}, respectively. Could not broadcast "
                            "these arrays together."
                        )

        if L := self["L"]:
            if np.any(L.value.m < 0):
                quit_print("L is invalid. Cavity lengths must be non-negative.")

        if wl := self["wl"]:
            if np.any(wl.value.m <= 0):
                quit_print("wl is invalid. Wavelengths must be positive.")

        # Make sure no illogical combinations of stability were given...
        has_g = self.has("g")
        has_g1 = self.has("g1")
        has_g2 = self.has("g2")
        has_gs = self.has("gs")
        if has_g and (has_g1 or has_g2 or has_gs):
            instruct = (
                "To specify a non-symmetric cavity please use both 'g1' and 'g2', do not give a "
                "value for 'g'. Or, to specify a symmetric cavity please use either 'g' or 'gs'; "
                "g is then gs * gs where gs = g1 = g2."
            )

            if has_g1 or has_g2:
                msg = (
                    "Incorrect usage! Cavity g-factor and individual mirror g-factors "
                    "cannot be specified simulataneously."
                )
            elif has_gs:
                msg = (
                    "Incorrect usage! Cavity g-factor and symmetric mirror g-factors "
                    "cannot be specified simulataneously."
                )

            quit_print(msg + "\n\n" + instruct)

        # ... and same goes for combinations of RoCs...
        if self.has("Rc") and (self.has("Rc1") or self.has("Rc2")):
            quit_print(
                "Incorrect usage! Symmetric curvature, 'Rc', and individual (non-symmetric), 'Rc1' and 'Rc2', "
                "curvatures cannot be specified simulataneously.\n\nTo specify a non-symmetric cavity "
                "please use both 'Rc1' and 'Rc2', do not give a value for 'Rc'. To specify a symmetric "
                "cavity please use just 'Rc'."
            )

        # ... and beam-sizes
        if self.has("w") and (self.has("w1") or self.has("w2")):
            quit_print(
                "Incorrect usage! Symmetric beam-size, 'w', and individual (non-symmetric), 'w1' and 'w2', "
                "beam-sizes cannot be specified simulataneously.\n\nTo specify a non-symmetric cavity "
                "please use both 'w1' and 'w2', do not give a value for 'w'. To specify a symmetric "
                "cavity please use just 'w'."
            )
        for p in "w", "w1", "w2", "w0":
            if P := self[p]:
                if np.any(P.value.m < 0):
                    quit_print(f"{p} is invalid. Beam sizes must be non-negative.")
