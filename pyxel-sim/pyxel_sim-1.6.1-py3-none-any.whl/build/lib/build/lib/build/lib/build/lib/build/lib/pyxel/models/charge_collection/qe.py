#   Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#  #
#   This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#   is part of this Pyxel package. No part of the package, including
#   this file, may be copied, modified, propagated, or distributed except according to
#   the terms contained in the file ‘LICENCE.txt’.


def prnu_simple_conversion(detector: Detector, qe_2d: np.ndarray) -> None:
    """Convert photons to charge with simple conversion using a QE map.

    Parameters
    ----------
    detector: Detector
    qe_2d: ndarray
        2D QE map.

    Returns
    -------
    None
    """
    logging.info("")

    geo = detector.geometry
    ch = detector.characteristics
    ph = detector.photon

    detector_charge = np.zeros(
        (geo.row, geo.col)
    )  # all pixels has zero charge by default
    photon_rows, photon_cols = ph.array.shape
    qe_2d = qe_2d[slice(0, photon_rows), slice(0, photon_cols)]
    detector_charge[slice(0, photon_rows), slice(0, photon_cols)] = (
        ph.array * qe_2d * ch.eta
    )

    charge_number = detector_charge.flatten()  # the average charge numbers per pixel
    where_non_zero = np.where(charge_number > 0.0)
    charge_number = charge_number[where_non_zero]
    size = charge_number.size

    init_ver_pix_position = geo.vertical_pixel_center_pos_list()[where_non_zero]
    init_hor_pix_position = geo.horizontal_pixel_center_pos_list()[where_non_zero]

    detector.charge.add_charge(
        particle_type="e",
        particles_per_cluster=charge_number,
        init_energy=[0.0] * size,
        init_ver_position=init_ver_pix_position,
        init_hor_position=init_hor_pix_position,
        init_z_position=[0.0] * size,
        init_ver_velocity=[0.0] * size,
        init_hor_velocity=[0.0] * size,
        init_z_velocity=[0.0] * size,
    )


def prnu_simple_conversion_random(detector: Detector, sigma: float):
    ph = detector.photon
    ch = detector.characteristics

    prnu_simple_conversion(detector, qe_2d)

    photon_mean_array = ch.qe * ph.array.astype("float")
    sigma_array = sigma * np.ones(photon_mean_array.shape)

    photon_random_array = np.random.normal(loc=signal_mean_array, scale=sigma_array)
    qe_2d = photon_random_array / ph.array

    prnu_simple_conversion(detector, qe_2d)


def prnu_simple_conversion_upload(
    detector: Detector,
    single_qe_map_file: t.Union[Path, str],
) -> None:
    """Convert photons to charge with simple conversion using a QE map from a file upload.

    Parameters
    ----------
    detector: Detector
    single_qe_map_file: str or Path or None

    Returns
    -------
    None
    """
    qe_2d = load_image(single_qe_map_file)

    prnu_simple_conversion(detector, qe_2d)


def prnu_wavelength_dependant(
    detector: Detector,
    single_qe_map_file: t.Union[Path, str],
    wavelength: float,
    filter_filename: t.Union[Path, str],
) -> None:
    """Convert photons to charge with simple conversion using a wavelength dependant QE map.

    Parameters
    ----------
    detector: Detector
    single_qe_map_file: str or Path
    wavelength: float
    filter_filename: str or Path

    Returns
    -------
    None
    """
    qe_2d = load_image(single_qe_map_file)

    qe_2d = qe_2d * wavelength_filter_factor(filter_filename, wavelength)

    prnu_simple_conversion(detector, qe_2d)

