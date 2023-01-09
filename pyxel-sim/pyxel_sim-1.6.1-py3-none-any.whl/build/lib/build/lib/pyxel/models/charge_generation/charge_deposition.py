#   Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#  #
#   This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#   is part of this Pyxel package. No part of the package, including
#   this file, may be copied, modified, propagated, or distributed except according to
#   the terms contained in the file ‘LICENCE.txt’.

"""Simple models to simulate charge deposition by ionizing particles (e.g. cosmic rays)."""

from pathlib import Path
from typing import Optional, Sequence, Union

import numpy as np
import pandas as pd
from typing_extensions import Literal

from pyxel.data_structure import Charge
from pyxel.detectors import Detector
from pyxel.util import materials, set_random_seed


def charge_deposition(
    detector: Detector,
    flux: float,
    step_size: float = 1.0,
    energy_mean: float = 1.0,
    energy_spread: float = 0.1,
    energy_spectrum: Union[str, Path, None] = None,
    energy_spectrum_sampling: Optional[Literal["linear", "log", None]] = "log",
    ehpair_creation: float = 3.65,
    material_density: float = 2.3290,
    particle_direction: Optional[
        Literal["isotropic", "orthogonal", None]
    ] = "isotropic",
    stopping_power_curve: Union[str, Path, None] = None,
    seed: Optional[int] = None,
) -> None:
    """Simulate charge deposition by ionizing particles using a stopping power curve.

    Parameters
    ----------
    detector : Detector
        the detector
    flux : float
        the flux of incoming particles in particle/s
    step_size : float
        the size of the considered unitary step in unit length along which energy is deposited
    energy_mean : float
        the mean energy of the incoming ionizing particles in MeV
    energy_spread : float
        the spread in energy of the incoming ionizing particles in MeV
    energy_spectrum : str
        the location of the file describing the energy spectrum of incident particles
        if no spectrum is provided energies are randomly drawn from a normal distribution
        with mean and spread defined above
        note that the energy spectrum is assumed to be a txt file with two columns [energy, flux]
        with the energy in MeV
    energy_spectrum_sampling : str
        "log" or None: the energy spectrum is sampled in log space
        "linear" : the energy spectrum is sampled in linear space
    ehpair_creation : float
        the energy required to generate a electron-hole pair in eV
        by default the Si value at room temperature is parsed i.e. 3.65 eV
    material_density : float
        the material density in g/cm3
        by default he Si value at room temperature is parsed i.e. 2.3290 g/cm3
    particle_direction : str
        "isotropic" : particles are coming from all directions (outside of the sensor)
        "orthogonal" : particles are coming from the top of the sensor (thickness = 0) and orthogonal to its surface
    stopping_power_curve : str
        the location of the file describing the total massive stopping power
        energetic loss per mass of material and per unit path length versus particle energy
        note that the the stopping power curve is assumed to be a csv file with two columns [energy, stopping power]
        energy in MeV, stopping power in MeV cm2/g
    seed : int, optional
    """
    with set_random_seed(seed):
        tracks = simulate_charge_deposition(
            flux=flux,
            exposure=detector.time_step,
            x_lim=detector.geometry.horz_dimension,
            y_lim=detector.geometry.vert_dimension,
            z_lim=detector.geometry.total_thickness,
            step_size=step_size,
            energy_mean=energy_mean,
            energy_spread=energy_spread,
            energy_spectrum=energy_spectrum,
            energy_spectrum_sampling=energy_spectrum_sampling,
            ehpair_creation=ehpair_creation,
            material_density=material_density,
            particle_direction=particle_direction,
            stopping_power_curve=stopping_power_curve,
        )

    detector.charge.add_charge_dataframe(tracks_to_charge(tracks))


def charge_deposition_in_mct(
    detector: Detector,
    flux: float,
    step_size: float = 1.0,
    energy_mean: float = 1.0,
    energy_spread: float = 0.1,
    energy_spectrum: Union[str, Path, None] = None,
    energy_spectrum_sampling: Optional[Literal["linear", "log", None]] = "log",
    cutoff_wavelength: float = 2.5,
    particle_direction: Optional[
        Literal["isotropic", "orthogonal", None]
    ] = "isotropic",
    stopping_power_curve: Union[str, Path, None] = None,
    seed: Optional[int] = None,
) -> None:
    """Simulate charge deposition by ionizing particles using a stopping power curve.

    Parameters
    ----------
    detector : Detector
        the detector
    flux : float
        the flux of incoming particles in particle/s
    step_size : float
        the size of the considered unitary step in unit length along which energy is deposited
    energy_mean : float
        the mean energy of the incoming ionizing particles in MeV
    energy_spread : float
        the spread in energy of the incoming ionizing particles in MeV
    energy_spectrum : str
        the location of the file describing the energy spectrum of incident particles
        if no spectrum is provided energies are randomly drawn from a normal distribution
        with mean and spread defined above
        note that the energy spectrum is assumed to be a txt file with two columns [energy, flux]
        with the energy in MeV
    energy_spectrum_sampling : str
        "log" or None: the energy spectrum is sampled in log space
        "linear" : the energy spectrum is sampled in linear space
    cutoff_wavelength : float
        the longest wavelength in micrometer at which the QE reaches 50% of its maximum,
        used to compute the bandgap energy, and the corresponding fraction of cadmium
    particle_direction : str
        "isotropic" : particles are coming from all directions (outside of the sensor)
        "orthogonal" : particles are coming from the top of the sensor (thickness = 0) and orthogonal to its surface
    stopping_power_curve : str
        the location of the file describing the total massive stopping power
        energetic loss per mass of material and per unit path length versus particle energy
        note that the the stopping power curve is assumed to be a csv file with two columns [energy, stopping power]
        energy in MeV, stopping power in MeV cm2/g
    seed : int, optional
    """
    lambdae = materials.lambda_e(cutoff_wavelength)
    eg = 1.24 / lambdae
    ehpair_creation = 3 * eg
    x = materials.eg_hansen_inverse(eg, detector.environment.temperature)
    material_density = materials.density(x)

    with set_random_seed(seed):
        tracks = simulate_charge_deposition(
            flux=flux,
            exposure=detector.time_step,
            x_lim=detector.geometry.horz_dimension,
            y_lim=detector.geometry.vert_dimension,
            z_lim=detector.geometry.total_thickness,
            step_size=step_size,
            energy_mean=energy_mean,
            energy_spread=energy_spread,
            energy_spectrum=energy_spectrum,
            energy_spectrum_sampling=energy_spectrum_sampling,
            ehpair_creation=ehpair_creation,
            material_density=material_density,
            particle_direction=particle_direction,
            stopping_power_curve=stopping_power_curve,
        )

    detector.charge.add_charge_dataframe(tracks_to_charge(tracks))


def tracks_to_charge(tracks: Sequence[float]) -> pd.DataFrame:
    """Convert tracks into a panda dataframe compatible with a detector charge object.

    Parameters
    ----------
    tracks : list
        with the following structure for each track :
        tracks[track_id], track_id = (vc, vx, vy, vz), vc[cluster_id] etc.
    """
    # tracks = np.array(tracks, dtype="object")

    tracks_arr = np.array(tracks, dtype="object")
    vc_arr = np.concatenate(tracks_arr[:, 0])
    vx_arr = np.concatenate(tracks_arr[:, 1])
    vy_arr = np.concatenate(tracks_arr[:, 2])
    vz_arr = np.concatenate(tracks_arr[:, 3])
    zeros = np.zeros(np.shape(vc_arr))

    return Charge.create_charges(
        particle_type="e",
        particles_per_cluster=vc_arr,
        init_energy=zeros,
        init_ver_position=vy_arr,
        init_hor_position=vx_arr,
        init_z_position=vz_arr,
        init_ver_velocity=zeros,
        init_hor_velocity=zeros,
        init_z_velocity=zeros,
    )


def simulate_charge_deposition(
    flux: float,
    exposure: float,
    x_lim: float,
    y_lim: float,
    z_lim: float,
    step_size: float = 1.0,
    energy_mean: float = 1.0,
    energy_spread: float = 0.1,
    energy_spectrum: Union[str, Path, None] = None,
    energy_spectrum_sampling: Optional[Literal["linear", "log"]] = "log",
    ehpair_creation: float = 3.65,
    material_density: float = 2.3290,
    particle_direction: Optional[Literal["isotropic", "orthogonal"]] = "isotropic",
    stopping_power_curve: Union[str, Path, None] = None,
) -> list:
    """Simulate charge deposition of incident ionizing particles inside a detector.

    Parameters
    ----------
    flux : float
        the flux of incoming particles in particle/s
    exposure : float
        the detector exposure duration in s (how long it takes to take one readout)
    x_lim : float
        the maximum dimension of the sensor in the x direction
    y_lim : float
        the maximum dimension of the sensor in the y direction
    z_lim : float
        the maximum dimension of the sensor in the z direction (thickness)
    step_size : float
        the size of the considered unitary step in unit length along which energy is deposited
    energy_mean : float
        the mean energy of the incoming ionizing particles
    energy_spread : float
        the spread in energy of the incoming ionizing particles
    energy_spectrum : str
        the location of the file describing the energy spectrum of incident particles
        if no spectrum is provided energies are randomly drawn from a normal distribution
        with mean and spread defined above
        note that the energy spectrum is assumed to be a txt file with two columns [energy, flux]
        with the energy in MeV
    energy_spectrum_sampling : str
        "log" or None: the energy spectrum is sampled in log space
        "linear" : the energy spectrum is sampled in linear space
    ehpair_creation : float
        the energy required to generate a electron-hole pair in eV
        by default the Si value at room temperature is parsed i.e. 3.65 eV
    material_density : float
        the material density in g/cm3
        by default he Si value at room temperature is parsed i.e. 2.3290 g/cm3
    particle_direction : str
        "isotropic" : particles are coming from all directions (outside of the sensor)
        "orthogonal" : particles are coming from the top of the sensor (thickness = 0) and orthogonal to its surface
    stopping_power_curve : str
        the location of the file describing the total massive stopping power
        energetic loss per mass of material and per unit path length versus particle energy
        note that the the stopping power curve is assumed to be a csv file with two columns [energy, stopping power]
        energy in MeV, stopping power in MeV cm2/g
    """

    # determine the total number of ionizing particles to simulate based on flux and exposure duration
    n_p = np.int64(flux * exposure)

    if n_p <= 0:
        raise ValueError("The number of particles generated has to be greater than 0.")

    if x_lim <= 0 or y_lim <= 0 or z_lim <= 0:
        raise ValueError("Detector dimension is negative or 0.")

    # generate random energies for each particle
    if energy_spectrum is None:
        # from normal distribution
        p_energies = np.random.normal(energy_mean, energy_spread, n_p)
    else:
        # from parsed spectrum using either logarithmic or linear sampling
        energy_spectrum_data = np.loadtxt(energy_spectrum, dtype="float", comments="#")
        n_samples = 100000
        if energy_spectrum_sampling == "log":
            log_energy_range = np.logspace(
                np.log10(np.min(energy_spectrum_data[:, 0])),
                np.log10(np.max(energy_spectrum_data[:, 0])),
                n_samples,
            )
            log_energy_pdf = np.interp(
                log_energy_range, energy_spectrum_data[:, 0], energy_spectrum_data[:, 1]
            )
            log_energy_pdf /= np.sum(log_energy_pdf)
            p_energies = np.random.choice(log_energy_range, size=n_p, p=log_energy_pdf)
        else:
            lin_energy_range = np.linspace(
                np.min(energy_spectrum_data[:, 0]),
                np.max(energy_spectrum_data[:, 0]),
                n_samples,
            )
            energy_pdf = np.interp(
                lin_energy_range, energy_spectrum_data[:, 0], energy_spectrum_data[:, 1]
            )
            energy_pdf /= np.sum(energy_pdf)
            p_energies = np.random.choice(lin_energy_range, n_p, p=energy_pdf)
    p_energies *= 1.0e6  # from MeV to eV

    # extract stopping power data convert to correct units and compute initial deposited energy
    if stopping_power_curve is None:
        raise ValueError("No stopping power curve has been parsed.")

    stopping_power_data = np.genfromtxt(
        stopping_power_curve, skip_header=1, delimiter=","
    )
    stopping_power_data[:, 0] *= 1.0e6  # from MeV to eV
    stopping_power_data[:, 1] *= (
        material_density * 1.0e2 * step_size
    )  # from MeV cm2/g to eV
    deposited_energies = np.interp(
        p_energies, stopping_power_data[:, 0], stopping_power_data[:, 1]
    )

    tracks = []
    # for each particle generate and store the energy deposition track
    for e, de in zip(p_energies, deposited_energies):

        # generate random particle coordinates
        x = np.random.random() * x_lim
        y = np.random.random() * y_lim

        # generate direction
        if particle_direction == "isotropic":
            alpha = 2.0 * np.pi * np.random.random()
            beta = 2.0 * np.pi * np.random.random()
        else:
            alpha = np.pi / 2.0
            beta = np.pi / 2.0
            # alpha = np.pi/2. + (np.random.randint(0,2))*np.pi
            # beta = np.pi/2. + (np.random.randint(0,2))*np.pi

        # compute equivalent step_size along each dimension
        dx = np.cos(alpha) * np.cos(beta) * step_size
        dy = np.cos(alpha) * np.sin(beta) * step_size
        dz = np.sin(alpha) * step_size

        # the particle is coming from outside the sensor: top or bottom, depending on travel direction (i.e. dz sign)
        if dz >= 0:
            z: float = 0.0
        else:
            z = z_lim

        # compute distances to the closest edge of the sensor along each dimension
        if dx > 0:
            distance_x = x_lim - x
        else:
            distance_x = x
        if dy > 0:
            distance_y = y_lim - y
        else:
            distance_y = y
        if dz > 0:
            distance_z = z_lim - z
        else:
            distance_z = z

        # compute the minimum number of steps required to reach one of the sensor edge
        distances = np.array([distance_x, distance_y, distance_z])
        deltas = np.abs(np.array([dx, dy, dz]))
        n_steps = int(np.min(np.divide(distances, deltas)))

        # check if incoming particle has enough energy to deposit all along the track or stops in the sensor
        if (e - n_steps * de) < 0:
            n_steps = int(e / de)
            # normally de should always be smaller than e
            # but it may happen that the particles would have stopped within a step_size
            # we assume that in that case the particle deposits its entire energy in one step
            if n_steps < 1:
                n_steps = 1
            vde = np.zeros(n_steps)
            for step in range(n_steps):
                vde[step] = np.interp(
                    e, stopping_power_data[:, 0], stopping_power_data[:, 1]
                )
                e -= de
        else:  # otherwise assumes the deposited energy is not a significant fraction of input energy,
            # the input energy remains the same all along track as os the deposited energy
            vde = np.ones(n_steps) * de

            # convert vde in amount of charge created
        vc = vde / ehpair_creation

        # generate vectors
        vx = x + np.arange(n_steps) * dx
        vy = y + np.arange(n_steps) * dy
        vz = z + np.arange(n_steps) * dz

        # gather results in a track
        track = (vc, vx, vy, vz)
        tracks.append(track)

    return tracks
