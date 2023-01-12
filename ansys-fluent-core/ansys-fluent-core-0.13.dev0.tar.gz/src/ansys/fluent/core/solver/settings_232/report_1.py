#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .simulation_reports import simulation_reports
from .discrete_phase_1 import discrete_phase
from .fluxes import fluxes
from .flow import flow
from .modified_setting_options import modified_setting_options
from .population_balance import population_balance
from .heat_exchange import heat_exchange
from .system import system
from .print_write_histogram import print_write_histogram
from .aero_optical_distortions import aero_optical_distortions
from .forces import forces
from .mphase_summary import mphase_summary
from .particle_summary import particle_summary
from .path_line_summary import path_line_summary
from .projected_surface_area import projected_surface_area
from .summary_1 import summary
from .surface_integrals import surface_integrals
from .volume_integrals import volume_integrals
class report(Group):
    """
    'report' child.
    """

    fluent_name = "report"

    child_names = \
        ['simulation_reports', 'discrete_phase', 'fluxes', 'flow',
         'modified_setting_options', 'population_balance', 'heat_exchange',
         'system', 'print_write_histogram']

    simulation_reports: simulation_reports = simulation_reports
    """
    simulation_reports child of report.
    """
    discrete_phase: discrete_phase = discrete_phase
    """
    discrete_phase child of report.
    """
    fluxes: fluxes = fluxes
    """
    fluxes child of report.
    """
    flow: flow = flow
    """
    flow child of report.
    """
    modified_setting_options: modified_setting_options = modified_setting_options
    """
    modified_setting_options child of report.
    """
    population_balance: population_balance = population_balance
    """
    population_balance child of report.
    """
    heat_exchange: heat_exchange = heat_exchange
    """
    heat_exchange child of report.
    """
    system: system = system
    """
    system child of report.
    """
    print_write_histogram: print_write_histogram = print_write_histogram
    """
    print_write_histogram child of report.
    """
    command_names = \
        ['aero_optical_distortions', 'forces', 'mphase_summary',
         'particle_summary', 'path_line_summary', 'projected_surface_area',
         'summary', 'surface_integrals', 'volume_integrals']

    aero_optical_distortions: aero_optical_distortions = aero_optical_distortions
    """
    aero_optical_distortions command of report.
    """
    forces: forces = forces
    """
    forces command of report.
    """
    mphase_summary: mphase_summary = mphase_summary
    """
    mphase_summary command of report.
    """
    particle_summary: particle_summary = particle_summary
    """
    particle_summary command of report.
    """
    path_line_summary: path_line_summary = path_line_summary
    """
    path_line_summary command of report.
    """
    projected_surface_area: projected_surface_area = projected_surface_area
    """
    projected_surface_area command of report.
    """
    summary: summary = summary
    """
    summary command of report.
    """
    surface_integrals: surface_integrals = surface_integrals
    """
    surface_integrals command of report.
    """
    volume_integrals: volume_integrals = volume_integrals
    """
    volume_integrals command of report.
    """
