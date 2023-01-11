from snek5000.info import InfoSolverMake

from snek5000.solvers.kth import SimulKTH


class InfoSolverCbox(InfoSolverMake):
    """Contain the information on a :class:`snek5000_cbox.solver.Simul`
    instance.

    """

    def _init_root(self):
        super()._init_root()
        self.module_name = "snek5000_cbox.solver"
        self.class_name = "Simul"
        self.short_name = "cbox"

        self.classes.Output.module_name = "snek5000_cbox.output"
        self.classes.Output.class_name = "OutputCbox"

        self.par_sections_disabled = ("mesh", "scalar01", "cvode")


class SimulCbox(SimulKTH):
    """A solver which compiles and runs using a Snakefile."""

    InfoSolver = InfoSolverCbox

    @classmethod
    def create_default_params(cls):
        """Set default values of parameters as given in reference
        implementation.

        """
        params = super().create_default_params()

        params._set_attribs({"prandtl": 0.71, "Ra_side": 0.0, "Ra_vert": 0.0})
        params._record_nek_user_params({"prandtl": 1, "Ra_side": 2, "Ra_vert": 3})

        params.oper.nproc_min = 2

        params.oper.Ly = 1.0

        params.nek.problemtype._set_attribs(
            {"solveBaseFlow": "no", "numberOfPerturbations": 1}
        )

        params.nek.velocity.density = 1.0
        params.nek.temperature.rho_cp = 1.0

        params.nek.temperature.residual_tol = 1e-8
        params.nek.temperature.absolute_tol = 1e-8
        params.nek.velocity.residual_tol = 1e-8
        params.nek.pressure.residual_tol = 1e-8

        params.oper._set_attribs({"mesh_stretch_factor": 0.0})
        params.oper._record_nek_user_params({"mesh_stretch_factor": 4})
        params.oper._set_doc(
            params.oper._doc
            + """
User parameter for mesh stretching in .usr file (subroutine usrdat2):

- ``mesh_stretch_factor``: float

  Mesh stretch factor (default = 0.0, meaning no stretching).
  The locations of the grid points are changed in the 3 directions (x, y, z)
  as follow: ``x_i  = x_i - stretch_factor_x*(sin(2pi*x_i/L_x))``.
  The stretching factors in different directions are computed such that
  elements at the corners are of aspect ratio 1. Typical reasonable values
  could be between 0.05 and 0.1. 0.15 corresponds to a very strongly stretched
  mesh.
"""
        )

        params.oper._set_attribs({"delta_T_side": 0.0})
        params.oper._record_nek_user_params({"delta_T_side": 5})
        params.oper._set_doc(
            params.oper._doc
            + """
User parameter for sidewall temperature difference in .usr file (subroutine userbc):

- ``delta_T_side``: float

  Lateral temperature difference (default = 0.0, meaning no temperature difference).

"""
        )

        params.oper._set_attribs({"delta_T_vert": 0.0})
        params.oper._record_nek_user_params({"delta_T_vert": 6})
        params.oper._set_doc(
            params.oper._doc
            + """
User parameter for vertical temperature difference in .usr file (subroutine userbc):

- ``delta_T_vert``: float

  Vertical temperature difference (default = 0.0, meaning no temperature difference).

"""
        )

        params.oper._set_attribs({"x_periodicity": False})
        params.oper._set_doc(
            params.oper._doc
            + """

- ``x_periodicity``: boolean

  Periodic boundary condition in x direction (default = False, meaning
  we have wall).

"""
        )

        params.oper._set_attribs({"y_periodicity": False})
        params.oper._set_doc(
            params.oper._doc
            + """

- ``y_periodicity``: boolean

  Periodic boundary condition in y direction (default = False, meaning
  we have wall).

"""
        )

        params.oper._set_attribs({"z_periodicity": False})
        params.oper._set_doc(
            params.oper._doc
            + """

- ``z_periodicity``: boolean

  Periodic boundary condition in z direction (default = False, meaning
  we have wall).

"""
        )

        params.oper._set_attribs({"enable_sfd": float(False)})
        params.oper._record_nek_user_params({"enable_sfd": 7})
        params.oper._set_doc(
            params.oper._doc
            + """
User parameter for activation of Selective Frequency Damping method in .usr file

- ``enable_sfd``: float

  Selective Frequency Damping (SFD) activation parameter(default = float(False) , meaning
  we don't use KTH framewok's SFD method to compute base flow).
  ``params.oper.enable_sfd = float(True)``, activates SFD.

"""
        )

        params.output.phys_fields._set_attribs(
            {"write_interval_pert_field": 1000},
        )
        params.output.phys_fields._record_nek_user_params(
            {"write_interval_pert_field": 9}
        )

        params.nek._set_child("sfd")
        attribs = {
            "filterwdth": 1.05,
            "controlcff": 0.5,
            "residualtol": 1e-8,
            "loginterval": 50,
            "sfdreadchpnt": False,
        }
        params.nek.sfd._set_attribs(attribs)
        params.nek.sfd._set_doc(
            """
Runtime parameter section for Selective Frequency Damping module (`KTH toolbox <https://github.com/KTH-Nek5000/KTH_Toolbox>`__)

- ``filterwdth``: Filter width
- ``controlcff``: Control coefficient
- ``residualtol``: Tolerance for residual
- ``loginterval``: Frequency for logging convegence data
- ``sfdreadchpnt``: Restart from checkpoint in SFD
"""
        )

        return params

    def __init__(self, params):

        if params.oper.Ly != 1.0:
            raise ValueError("One have to assign `params.oper.Ly = 1.0`")

        if params.Ra_side > 0 and params.Ra_vert == 0:
            params.oper.delta_T_side = 1.0
            rayleigh = params.Ra_side

            if params.oper.dim == 2:
                if params.oper.y_periodicity:
                    params.oper.boundary = list("WWPP")
                    params.oper.boundary_scalars = list("ttPP")
                else:
                    params.oper.boundary = list("WWWW")
                    params.oper.boundary_scalars = list("ttII")
            else:
                if params.oper.y_periodicity and params.oper.z_periodicity:
                    params.oper.boundary = list("WWPPPP")
                    params.oper.boundary_scalars = list("ttPPPP")
                elif params.oper.z_periodicity:
                    params.oper.boundary = list("WWWWPP")
                    params.oper.boundary_scalars = list("ttIIPP")
                else:
                    params.oper.boundary = list("WWWWWW")
                    params.oper.boundary_scalars = list("ttIIII")

        elif params.Ra_side == 0 and params.Ra_vert > 0:
            params.oper.delta_T_vert = 1.0
            rayleigh = params.Ra_vert

            if params.oper.dim == 2:
                if params.oper.x_periodicity:
                    params.oper.boundary = list("PPWW")
                    params.oper.boundary_scalars = list("PPtt")
                else:
                    params.oper.boundary = list("WWWW")
                    params.oper.boundary_scalars = list("IItt")
            else:
                if params.oper.x_periodicity and params.oper.z_periodicity:
                    params.oper.boundary = list("PPWWPP")
                    params.oper.boundary_scalars = list("PPttPP")
                elif params.oper.z_periodicity:
                    params.oper.boundary = list("WWWWPP")
                    params.oper.boundary_scalars = list("IIttPP")
                else:
                    params.oper.boundary = list("WWWWWW")
                    params.oper.boundary_scalars = list("IIttII")

        elif params.Ra_side > 0 and params.Ra_vert > 0:

            params.oper.delta_T_vert = 1.0
            params.oper.delta_T_side = (
                params.Ra_side / params.Ra_vert * params.oper.delta_T_vert
            )

            rayleigh = params.Ra_vert

            if params.oper.dim == 2:
                params.oper.boundary = list("WWWW")
                params.oper.boundary_scalars = list("tttt")
            else:
                if params.oper.z_periodicity:
                    params.oper.boundary = list("WWWWPP")
                    params.oper.boundary_scalars = list("ttttPP")
                else:
                    params.oper.boundary = list("WWWWWW")
                    params.oper.boundary_scalars = list("ttttII")

        else:
            raise ValueError("params.Ra_side or params.Ra_vert should be > 0")

        params.nek.velocity.viscosity = params.prandtl / rayleigh ** (1 / 2)
        params.nek.temperature.conductivity = 1.0 / rayleigh ** (1 / 2)

        super().__init__(params)


Simul = SimulCbox
