"""Attenuation correction module."""

# WRaINfo, Is a software to process FURUNO weather radar data.
#
# Copyright (c) 2023, FernLab (GFZ Potsdam, fernlab@gfz-potsdam.de)
#
# This software was developed within the context of the RaINfo ("Potential use of
# high resolution weather data in agriculture") project of FernLab funded by
# the Impulse and Networking Fund of the Helmholtz Association.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# imports
# -------

import xarray as xr
import numpy as np
import wradlib as wrl
from scipy import integrate


# phase processing
# ----------------

def phase_zphi(phi, rng=1000., start_range=0.):
    """Preprocess of PHIDP.

    Parameters
    ----------
    phi : xarray.DataArray
    rng : int
        range to calculate the window to search precipitation bins
    start_range : int
        distance from radar where the processing is starting

    Returns
    -------
    : xarray.Dataset
        xarray.Dataset of preprocessed PHIDP.
    """
    # select measurements after startrange
    phi = phi.where(phi.range >= start_range)

    # get first rangestep
    range_step = np.diff(phi.range)[0]

    # calculate window (need uneven number)
    nprec = int(rng / range_step)
    if (nprec % 2) == 0:
        nprec += 1

    # create binary array
    phib = xr.where(np.isnan(phi), 0, 1)

    # take nprec range bins and calculate sum of valid values
    phib_sum = phib.rolling(range=nprec, center=True).sum(skipna=True)

    # offset in m
    offset = nprec // 2 * range_step
    # offset in idx
    offset_idx = nprec // 2

    # start_range in m (centered)
    start_range = phib_sum.idxmax(dim="range") - offset
    # start_range in idx (centered)
    start_range_idx = phib_sum.argmax(dim="range") - offset_idx

    # stop_range in m (centered)
    stop_range = phib_sum[..., ::-1].idxmax(dim="range") + offset
    # stop_range in idx (centered)
    stop_range_idx = len(phib_sum.range) - (phib_sum[..., ::-1].argmax(dim="range") - offset_idx) - 2

    first0 = phi.where((phi.range >= start_range) & (phi.range <= start_range + rng),
                       drop=True)

    first_min = first0.min(dim='range', skipna=True)
    first_max = first0.max(dim='range', skipna=True)
    first_mean = first0.mean(dim='range', skipna=True)
    first_median = first0.median(dim='range', skipna=True)

    last0 = phi.where((phi.range >= stop_range - rng) & (phi.range <= stop_range),
                      drop=True)

    last_min = last0.min(dim='range', skipna=True)
    last_max = last0.max(dim='range', skipna=True)
    last_mean = last0.mean(dim='range', skipna=True)
    last_median = last0.median(dim='range', skipna=True)

    #     # get min phase values in specified range
    #     first = phi.where((phi.range >= start_range) & (phi.range <= start_range + rng),
    #                        drop=True).min(dim='range', skipna=True)
    #     # get max phase values in specified range
    #     last = phi.where((phi.range >= stop_range - rng) & (phi.range <= stop_range),
    #                        drop=True).max(dim='range', skipna=True)

    return xr.Dataset(dict(phib=phib_sum,
                           offset=offset,
                           offset_idx=offset_idx,
                           start_range=start_range,
                           stop_range=stop_range,
                           first_min=first_min,
                           first_max=first_max,
                           first_mean=first_mean,
                           first_median=first_median,
                           first_idx=start_range_idx,
                           last_min=last_min,
                           last_max=last_max,
                           last_mean=last_mean,
                           last_median=last_median,
                           last_idx=stop_range_idx,
                           ))


def cumulative_trapezoid(da, coord, **kwargs):
    """Cumulative trapezoid integration.

    Parameters
    ---------
    da : xarray.DataArray
        array with data to integrate
    coord : str
        name of coordinate to integrate over

    Returns
    -------
    : xarray.DataArray
        DataArray with integrated values.
    """
    x = da[coord]
    dim = x.dims[0]
    input_core_dim = [dim]
    output_core_dim = [dim]

    # calculate dx
    dx = da[coord].diff(dim).median()
    if coord == "range":
        dx /= 1000.

    kwargs['dx'] = kwargs.get("dx", dx.values)
    kwargs['axis'] = kwargs.get("axis", -1)
    kwargs["initial"] = kwargs.get("initial", 0)

    return xr.apply_ufunc(integrate.cumulative_trapezoid,
                          da,
                          input_core_dims=[input_core_dim],
                          output_core_dims=[output_core_dim],
                          output_dtypes=['float'],
                          dask='parallelized',
                          kwargs=kwargs,
                          dask_gufunc_kwargs=dict(allow_rechunk=True),)


# zphi-method (Testud et al. 2001)
# -------------------------------

def zphi(refl, cphase, alphax=0.28, bx=0.78):
    """Process of PHIDP, KDP and specific attenuation AH_ZPHI.

    Parameter
    ---------
    refl : xarray.DataArray
        array with reflectivity
    cphase : xarray.DataArray
        array of function phase_zphi
    alphax : float
        threshold, default for x-band: 0.28
    bx : float
        threshold

    Returns
    -------
    : xarray.Dataset
        xarray.Dataset with processed variables.
    """
    # calculate delta-phi
    dphi = cphase.last_median - cphase.first_median

    # if negative set dphi zero
    dphi = dphi.where(dphi >= 0).fillna(0)

    # calculate function of dphi
    fdphi = 10 ** (0.1 * bx * dphi * alphax) - 1

    # extract reflectivity
    zhraw = refl.where((refl.range < cphase.stop_range))

    # transform to linear space and fill NaN with zero
    zax = zhraw.pipe(wrl.trafo.idecibel).fillna(0)

    # transform to decibel again
    # zh_cal = zax.pipe(wrl.trafo.decibel)

    # caclulate power
    # equ. 9
    za = zax ** bx

    # fill NaN with zero
    za_zero = za.fillna(0)

    # calculate cumulative integral over range
    iza_x = 0.46 * bx * cumulative_trapezoid(za_zero, coord='range')

    # get maximum over last axis (range) and subtract cumulative integral
    # equ. 10 (r->r2)
    iza = np.max(iza_x, axis=-1) - iza_x

    # divide by function of delta-phi
    iza_fdphi = iza / fdphi

    # TODO: check if this calculates the correct/wanted iza_first
    # equ. 10 (r1->r2)
    # iza_first = iza_fdphi.isel(range=0)
    iza_first = iza_fdphi.isel(range=cphase.first_idx.load())

    # calculate specific attenuation
    # equ. 8
    att = za / (iza_first + iza)
    phi = 2 * cumulative_trapezoid(att / alphax, coord='range')

    # KDP
    kdp = att / alphax

    # encoding properties for output
    enc = dict(zlib=True, complevel=4, chunksizes=(1,) + phi.shape[1:])
    phi.encoding = enc
    phi.name = "PHIDP_RECALC"
    phi_attrs = wrl.io.xarray.moments_mapping["PHIDP"].copy()
    phi_attrs.pop("gamic")
    phi.attrs = phi_attrs

    att.encoding = enc
    pol = refl.long_name[-1:]
    att_name = f"A{pol.upper()}"
    att.name = att_name + "_ZPHI"
    spec_att = dict(units='dB/km',
                    standard_name=f'specific_attenuation_{pol.lower()}',
                    long_name=f'Specific attenuation {pol.upper()}',
                    short_name=att_name
                    )
    att.attrs = spec_att

    kdp.encoding = enc
    kdp.name = "KDP_RECALC"
    kdp_attrs = wrl.io.xarray.moments_mapping["KDP"].copy()
    kdp_attrs.pop("gamic")
    kdp.attrs = kdp_attrs

    return xr.merge([phi.to_dataset(), att.to_dataset(), kdp.to_dataset()])


# process chain for attenuation correction
# ----------------------------------------

def attenuation_correction(ds, moment, dims=["azimuth", "range"]):
    """Attenuation correction with zphi method.

    Parameters
    ----------
    ds : xarray.DataArray
    moment : xarray.DataArray
        DBZH (clutter corrected)
    dims : list
        dimension of the dataset

    Returns
    -------
    : xarray.Dataset
        xarray.Dataset with attenuation corrected refelctivity and recalculated variables.
    """
    # phase processing
    # ----------------

    cphase = phase_zphi(ds.PHIDP.where((ds.RHOHV > 0.8) & (ds[moment] > 10)), rng=1000., start_range=0)

    ds_out = zphi(ds[moment], cphase)

    # attenuation correction
    # ----------------------

    zhcorr = ds[moment] + 0.28 * ds_out.PHIDP_RECALC

    # concat datasets
    # ---------------

    ds["DBZH_CORR"] = xr.DataArray(zhcorr,
                                   dims=dims,
                                   attrs=ds.DBZH.attrs)

    phidp_recalc = ds_out.PHIDP_RECALC
    ds["PHIDP_RECALC"] = xr.DataArray(phidp_recalc,
                                      dims=dims,
                                      attrs=ds_out.PHIDP_RECALC.attrs)

    ah_zphi = ds_out.AH_ZPHI
    ds["AH_ZPHI"] = xr.DataArray(ah_zphi,
                                 dims=dims,
                                 attrs=ds_out.AH_ZPHI.attrs)

    kdp = ds_out.KDP_RECALC
    ds["KDP_RECALC"] = xr.DataArray(kdp,
                                    dims=dims,
                                    attrs=ds_out.KDP_RECALC.attrs)

    return ds
