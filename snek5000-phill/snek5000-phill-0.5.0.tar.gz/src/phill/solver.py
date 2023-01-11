from snek5000.info import InfoSolverMake
from snek5000.solvers.kth import SimulKTH


class InfoSolverPhill(InfoSolverMake):
    """Contain the information on a :class:`eturb.solvers.abl.Simul`
    instance.

    .. todo::

        Move Output info to :class:`InfoSolverNek` and only override it in
        :class:`InfoSolverABL`.

    """

    def _init_root(self):
        from . import short_name

        super()._init_root()
        self.module_name = "phill.solver"
        self.class_name = "Simul"
        self.short_name = short_name

        self.classes.Output.module_name = "phill.output"
        self.classes.Output.class_name = "OutputPhill"


class SimulPhill(SimulKTH):
    """A solver which compiles and runs using a Snakefile."""

    InfoSolver = InfoSolverPhill

    @classmethod
    def create_default_params(cls):
        """Set default values of parameters as given in reference
        implementation.

        """
        params = super().create_default_params()

        params.nek.velocity._set_attrib("advection", True)

        # Set par file parameters
        # ------------------------
        # Alternative can be to add phill.par to the current directory and
        # Synchronize baseline parameters as follows:
        # -----------------------------------------------------------------
        #  primary_par_file = get_root() / "phill.par"
        #  if mpi.rank == 0:
        #      logger.info(f"Reading baseline parameters from {primary_par_file}")
        #
        #  params.nek._read_par(primary_par_file)

        # https://github.com/KTH-Nek5000/KTH_Examples/blob/master/phill_STAT/phill.par
        general = params.nek.general
        general.stop_at = "num_steps"
        general.num_steps = 20
        general.dt = -2e-4
        general.time_stepper = "bdf3"
        general.variable_dt = False
        general.target_cfl = 0.3
        general.write_control = "timestep"
        general.write_interval = 100
        general.dealiasing = True
        general.filtering = "explicit"
        general.filter_weight = 0.02
        general.filter_cutoff_ratio = 0.67

        params.nek.problemtype.stress_formulation = False
        params.nek.problemtype.variable_properties = False

        params.nek.pressure.residual_tol = params.nek.velocity.residual_tol = 1e-8
        params.nek.pressure.residual_proj = params.nek.velocity.residual_proj = 1e-8
        params.nek.velocity.density = 1.0
        params.nek.velocity.viscosity = -700

        # User parameters for KTH framework
        params.nek.stat.av_step = 10
        params.nek.stat.io_step = 50

        # Set box file parameters
        # -----------------------
        # https://github.com/KTH-Nek5000/KTH_Examples/blob/master/phill_STAT/phill.box
        oper = params.oper
        # logger.info(oper._doc)

        oper.dim = 3
        oper.scalars = 1
        oper.nx = 22
        oper.ny = 16
        oper.nz = 19

        oper.Lx = oper.Ly = oper.Lz = 1.0
        oper.boundary = ["P", "P", "W", "W", "P", "P"]

        # Set SIZE file parameters
        # ------------------------
        # https://github.com/KTH-Nek5000/KTH_Examples/blob/master/phill_STAT/SIZE
        # Basic
        #  logger.info(oper.elem._doc)
        #  logger.info(oper.max._doc)
        #  logger.info(oper.misc._doc)

        oper.elem.order = 6  # lx1
        oper.elem.coef_dealiasing = 2 / 3  # lxd
        oper.elem.staggered = True  # Pn Pn-2

        # lelg calculated automatically
        oper.nproc_min = 8  # lpmin
        oper.nproc_max = 32  # lpmax

        oper.misc.fast_diag = False
        return params


Simul = SimulPhill
