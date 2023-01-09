#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""Pyxel CosmiX model to generate charge by ionization."""

import logging
import math

# noqa: F401
from pathlib import Path
from typing import Optional, Tuple, Union

import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from typing_extensions import Literal

from pyxel.detectors import Detector
from pyxel.models.charge_generation.cosmix.plotting import PlottingCosmix
from pyxel.models.charge_generation.cosmix.simulation import Simulation
from pyxel.models.charge_generation.cosmix.util import interpolate_data, read_data
from pyxel.util import set_random_seed

# from astropy import units as u
# TODO: write basic test to check inputs, private function, documentation


# @validators.validate
# @config.argument(name='', label='', units='', validate=)
def cosmix(
    detector: Detector,
    simulation_mode: Optional[
        Literal["cosmic_ray", "cosmics", "radioactive_decay", "snowflakes"]
    ] = None,
    running_mode: Optional[
        Literal["stopping", "stepsize", "geant4", "plotting"]
    ] = None,
    particle_type: Optional[Literal["proton", "alpha", "ion"]] = None,
    initial_energy: Optional[Union[int, float, Literal["random"]]] = None,
    particles_per_second: Optional[float] = None,
    incident_angles: Optional[Tuple[str, str]] = None,
    starting_position: Optional[Tuple[str, str, str]] = None,
    # step_size_file: str = None,
    # stopping_file: str = None,
    spectrum_file: Optional[str] = None,
    seed: Optional[int] = None,
    ionization_energy: float = 3.6,
    progressbar: bool = True,
) -> None:
    """Apply CosmiX model.

    Parameters
    ----------
    detector : Detector
        Pyxel Detector object.
    simulation_mode : literal
        Simulation mode: ``cosmic_rays``, ``radioactive_decay``.
    running_mode : literal
        Mode: ``stopping``, ``stepsize``, ``geant4``, ``plotting``.
    particle_type
        Type of particle: ``proton``, ``alpha``, ``ion``.
    initial_energy : int or float or literal
        Kinetic energy of particle, set `random` for random.
    particles_per_second : float
        Number of particles per second.
    incident_angles : tuple of str
        Incident angles: ``(α, β)``.
    starting_position : tuple of str
        Starting position: ``(x, y, z)``.
    spectrum_file : str
        Path to input spectrum
    seed : int, optional
        Random seed.
    ionization_energy : float
        Mean ionization energy of the semiconductor lattice.
    progressbar : bool
        Progressbar.
    """
    if simulation_mode is None:
        raise ValueError("CosmiX: Simulation mode is not defined")
    if running_mode is None:
        raise ValueError("CosmiX: Running mode is not defined")
    if particle_type is None:
        raise ValueError("CosmiX: Particle type is not defined")
    if particles_per_second is None:
        raise ValueError("CosmiX: Particles per second is not defined")
    if spectrum_file is None:
        raise ValueError("CosmiX: Spectrum is not defined")

    if initial_energy is None:
        initial_energy = "random"  # TODO

    if incident_angles is None:
        incident_angle_alpha, incident_angle_beta = ("random", "random")
    else:
        incident_angle_alpha, incident_angle_beta = incident_angles

    if starting_position is None:
        start_pos_ver, start_pos_hor, start_pos_z = ("random", "random", "random")
    else:
        start_pos_ver, start_pos_hor, start_pos_z = starting_position

    particle_number = int(particles_per_second * detector.time_step)

    with set_random_seed(seed):
        cosmix = Cosmix(
            detector=detector,
            simulation_mode=simulation_mode,
            particle_type=particle_type,
            initial_energy=initial_energy,
            particle_number=particle_number,
            incident_angle_alpha=incident_angle_alpha,
            incident_angle_beta=incident_angle_beta,
            start_pos_ver=start_pos_ver,
            start_pos_hor=start_pos_hor,
            start_pos_z=start_pos_z,
            ionization_energy=ionization_energy,
            progressbar=progressbar,
        )

        # cosmix.set_simulation_mode(simulation_mode)
        # cosmix.set_particle_type(particle_type)                # MeV
        # cosmix.set_initial_energy(initial_energy)              # MeV
        # cosmix.set_particle_number(particle_number)            # -
        # cosmix.set_incident_angles(incident_angles)            # rad
        # cosmix.set_starting_position(starting_position)        # um
        cosmix.set_particle_spectrum(Path(spectrum_file))

        if running_mode == "stopping":
            # cosmix.run_mod()          ########
            raise NotImplementedError
            # cosmix.set_stopping_power(stopping_file)
            # cosmix.run()
        elif running_mode == "stepsize":
            cosmix.set_stepsize()
            cosmix.run()
        elif running_mode == "geant4":
            cosmix.set_geant4()
            cosmix.run()
        elif running_mode == "plotting":

            plot_obj = PlottingCosmix(cosmix, save_plots=True, draw_plots=True)

            plot_obj.plot_flux_spectrum()
            plot_obj.plot_gaia_vs_gras_hist(normalize=True)

            plot_obj.show()
        else:
            raise ValueError


class Cosmix:
    """TBW."""

    def __init__(
        self,
        detector: Detector,
        simulation_mode: Literal[
            "cosmic_ray", "cosmics", "radioactive_decay", "snowflakes"
        ],
        particle_type: Literal[
            "proton", "ion", "alpha", "beta", "electron", "gamma", "x-ray"
        ],
        initial_energy: Union[int, float, Literal["random"]],
        particle_number: int,
        incident_angle_alpha: str,
        incident_angle_beta: str,
        start_pos_ver: str,
        start_pos_hor: str,
        start_pos_z: str,
        ionization_energy: float = 3.6,
        progressbar: bool = True,
    ):
        self.simulation_mode = simulation_mode
        self.part_type = particle_type
        self.init_energy = initial_energy
        self.particle_number = particle_number
        self.angle_alpha = incident_angle_alpha
        self.angle_beta = incident_angle_beta
        self.position_ver = start_pos_ver
        self.position_hor = start_pos_hor
        self.position_z = start_pos_z
        self.ionization_energy = ionization_energy
        self._progressbar = progressbar

        self.sim_obj = Simulation(detector)
        self.charge_obj = detector.charge
        self._log = logging.getLogger(__name__)

    # TODO: Is it still used ?
    def set_simulation_mode(
        self,
        sim_mode: Literal["cosmic_ray", "cosmics", "radioactive_decay", "snowflakes"],
    ) -> None:
        self.simulation_mode = sim_mode

    # TODO: Is it still used ?
    def set_particle_type(
        self,
        particle_type: Literal[
            "proton", "ion", "alpha", "beta", "electron", "gamma", "x-ray"
        ],
    ) -> None:
        self.part_type = particle_type

    # TODO: Is it still used ?
    def set_initial_energy(self, energy: Union[int, float, Literal["random"]]) -> None:
        self.init_energy = energy

    # TODO: Is it still used ?
    def set_particle_number(self, number: int) -> None:
        self.particle_number = number

    # TODO: Is it still used ?
    def set_incident_angles(self, angles: Tuple[str, str]) -> None:
        alpha, beta = angles
        self.angle_alpha = alpha
        self.angle_beta = beta

    # TODO: Is it still used ?
    def set_starting_position(self, start_position: Tuple[str, str, str]) -> None:
        position_vertical, position_horizontal, position_z = start_position
        self.position_ver = position_vertical
        self.position_hor = position_horizontal
        self.position_z = position_z

    def set_particle_spectrum(self, file_name: Path) -> None:
        """Set up the particle specs according to a spectrum.

        Parameters
        ----------
        file_name : Path
            Path of the file containing the spectrum.
        """
        spectrum = read_data(file_name)  # nuc/m2*s*sr*MeV
        geo = self.sim_obj.detector.geometry
        detector_area = geo.vert_dimension * geo.horz_dimension * 1.0e-8  # cm2

        spectrum[:, 1] *= 4 * math.pi * 1.0e-4 * detector_area  # nuc/s*MeV

        spectrum_function = interpolate_data(spectrum)

        lin_energy_range = np.arange(
            np.min(spectrum[:, 0]), np.max(spectrum[:, 0]), 0.01
        )
        self.sim_obj.flux_dist = spectrum_function(lin_energy_range)

        cum_sum = np.cumsum(self.sim_obj.flux_dist)
        cum_sum /= np.max(cum_sum)
        self.sim_obj.spectrum_cdf = np.stack((lin_energy_range, cum_sum), axis=1)

    def set_stopping_power(self, stopping_file: Path) -> None:
        self.sim_obj.energy_loss_data = "stopping"
        self.sim_obj.stopping_power = read_data(stopping_file)

    def set_stepsize(self) -> None:
        self.sim_obj.energy_loss_data = "stepsize"
        self.create_data_library()

    def set_geant4(self) -> None:
        self.sim_obj.energy_loss_data = "geant4"

    def create_data_library(self) -> None:
        self.sim_obj.data_library = pd.DataFrame(
            columns=["type", "energy", "thickness", "path"]
        )

        # mat_list = ['Si']

        type_list = [
            "proton"
        ]  # , 'ion', 'alpha', 'beta', 'electron', 'gamma', 'x-ray']
        energy_list = [100.0]  # MeV
        thick_list = [40.0, 50.0, 60.0, 70.0, 100.0]  # um

        # TODO: Fix this. See issue #152
        path = Path(__file__).parent.joinpath("data", "inputs")
        filename_list = [
            "stepsize_proton_100MeV_40um_Si_10k.ascii",
            "stepsize_proton_100MeV_50um_Si_10k.ascii",
            "stepsize_proton_100MeV_60um_Si_10k.ascii",
            "stepsize_proton_100MeV_70um_Si_10k.ascii",
            "stepsize_proton_100MeV_100um_Si_10k.ascii",
        ]

        i = 0
        for pt in type_list:
            for en in energy_list:
                for th in thick_list:
                    data_dict = {
                        "type": pt,
                        "energy": en,
                        "thickness": th,
                        "path": str(Path(path, filename_list[i])),
                    }
                    new_df = pd.DataFrame(data_dict, index=[0])
                    self.sim_obj.data_library = pd.concat(
                        [self.sim_obj.data_library, new_df], ignore_index=True
                    )
                    i += 1

    def run(self) -> None:
        # print("CosmiX - simulation processing...\n")

        self.sim_obj.parameters(
            sim_mode=self.simulation_mode,
            part_type=self.part_type,
            init_energy=self.init_energy,
            pos_ver=self.position_ver,
            pos_hor=self.position_hor,
            pos_z=self.position_z,
            alpha=self.angle_alpha,
            beta=self.angle_beta,
            ionization_energy=self.ionization_energy,
        )

        # Get output folder and create it (if needed)
        out_path = Path("data").resolve()
        out_path.mkdir(parents=True, exist_ok=True)

        self._log.info("Save data in folder '%s'", out_path)

        for k in tqdm(
            range(self.particle_number),
            desc="Cosmix",
            unit=" particle",
            disable=(not self._progressbar),
        ):
            # for k in range(0, self.particle_number):
            err: Optional[bool] = None
            if self.sim_obj.energy_loss_data == "stepsize":  # TODO
                err = self.sim_obj.event_generation()
            elif self.sim_obj.energy_loss_data == "geant4":
                err = self.sim_obj.event_generation_geant4()
            if k % 10 == 0:
                np.save(
                    f"{out_path}/cosmix-e_num_lst_per_event.npy",
                    self.sim_obj.e_num_lst_per_event,
                )
                np.save(
                    f"{out_path}/cosmix-sec_lst_per_event.npy",
                    self.sim_obj.sec_lst_per_event,
                )
                np.save(
                    f"{out_path}/cosmix-ter_lst_per_event.npy",
                    self.sim_obj.ter_lst_per_event,
                )
                np.save(
                    f"{out_path}/cosmix-track_length_lst_per_event.npy",
                    self.sim_obj.track_length_lst_per_event,
                )
                np.save(
                    f"{out_path}/cosmix-p_energy_lst_per_event.npy",
                    self.sim_obj.p_energy_lst_per_event,
                )
                np.save(
                    f"{out_path}/cosmix-alpha_lst_per_event.npy",
                    self.sim_obj.alpha_lst_per_event,
                )
                np.save(
                    f"{out_path}/cosmix-beta_lst_per_event.npy",
                    self.sim_obj.beta_lst_per_event,
                )

                np.save(
                    f"{out_path}/cosmix-e_num_lst_per_step.npy",
                    self.sim_obj.e_num_lst_per_step,
                )
                np.save(f"{out_path}/cosmix-e_pos0_lst.npy", self.sim_obj.e_pos0_lst)
                np.save(f"{out_path}/cosmix-e_pos1_lst.npy", self.sim_obj.e_pos1_lst)
                np.save(f"{out_path}/cosmix-e_pos2_lst.npy", self.sim_obj.e_pos2_lst)

                np.save(
                    f"{out_path}/cosmix-all_e_from_eloss.npy",
                    self.sim_obj.electron_number_from_eloss,
                )
                np.save(
                    f"{out_path}/cosmix-sec_e_from_eloss.npy",
                    self.sim_obj.secondaries_from_eloss,
                )
                np.save(
                    f"{out_path}/cosmix-ter_e_from_eloss.npy",
                    self.sim_obj.tertiaries_from_eloss,
                )
            if err:
                k -= 1

        size = len(self.sim_obj.e_num_lst_per_step)

        self.sim_obj.e_vel0_lst = np.zeros(size)
        self.sim_obj.e_vel1_lst = np.zeros(size)
        self.sim_obj.e_vel2_lst = np.zeros(size)

        self.charge_obj.add_charge(
            particle_type="e",
            particles_per_cluster=np.asarray(self.sim_obj.e_num_lst_per_step),
            init_energy=np.asarray(self.sim_obj.e_energy_lst),
            init_ver_position=np.asarray(self.sim_obj.e_pos0_lst),
            init_hor_position=np.asarray(self.sim_obj.e_pos1_lst),
            init_z_position=np.asarray(self.sim_obj.e_pos2_lst),
            init_ver_velocity=self.sim_obj.e_vel0_lst,
            init_hor_velocity=self.sim_obj.e_vel1_lst,
            init_z_velocity=self.sim_obj.e_vel2_lst,
        )

    def run_mod(self) -> None:
        # TODO: Use `logging`
        print("CosmiX - adding previous cosmic ray signals to image ...\n")

        # TODO: Use `pathlib.Path`
        out_path = "data/"
        e_num_lst_per_step = np.load(out_path + "cosmix-e_num_lst_per_step.npy")
        e_pos0_lst = np.load(out_path + "cosmix-e_pos0_lst.npy")
        e_pos1_lst = np.load(out_path + "cosmix-e_pos1_lst.npy")
        e_pos2_lst = np.load(out_path + "cosmix-e_pos2_lst.npy")

        size = len(e_num_lst_per_step)
        e_energy_lst = np.zeros(size)
        e_vel0_lst = np.zeros(size)
        e_vel1_lst = np.zeros(size)
        e_vel2_lst = np.zeros(size)

        self.charge_obj.add_charge(
            particle_type="e",
            particles_per_cluster=e_num_lst_per_step,
            init_energy=e_energy_lst,
            init_ver_position=e_pos0_lst,
            init_hor_position=e_pos1_lst,
            init_z_position=e_pos2_lst,
            init_ver_velocity=e_vel0_lst,
            init_hor_velocity=e_vel1_lst,
            init_z_velocity=e_vel2_lst,
        )
