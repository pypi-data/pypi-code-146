#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""PacketParser time module"""
import os
import os.path as osp
from datetime import datetime

import numpy as np
from poppy.core.configuration import Configuration
from poppy.core.generic.metaclasses import Singleton
from poppy.core.logger import logger

from roc.rpl.constants import SOLAR_ORBITER_NAIF_ID
from roc.rpl.packet_structure.data import Data
from roc.rpl.time.spice import SpiceHarvester


__all__ = ['Time']


# SEC TO NANOSEC conversion factor
SEC_TO_NANOSEC = np.timedelta64(1000000000, 'ns')

# J2000 base time
J2000_BASETIME = np.datetime64('2000-01-01T12:00', 'ns')

# Number of leap nanoseconds at J2000 origin (32 sec)
J2000_LEAP_NSEC = np.timedelta64(32000000000, 'ns')

# RPW CCSDS CUC base time
RPW_BASETIME = np.datetime64('2000-01-01T00:00', 'ns')

# Delta nanosec betwen TAI and TT time bases (TAI = TT + 32.184 sec)
DELTA_NSEC_TAI_TT = np.timedelta64(32184000000, 'ns')

# Delta nanosec between RPW and J2000 epoch (J2000 = RPW + 12h)
DELTA_NSEC_RPW_J2000 = RPW_BASETIME - J2000_BASETIME

# RPW BASETIME in TT2000 (nanoseconds since J2000)
TT2000_RPW_BASETIME = DELTA_NSEC_TAI_TT + \
    J2000_LEAP_NSEC + DELTA_NSEC_RPW_J2000

# TT2000 BASETIME in Julian days
TT2000_JD_BASETIME = 2451545.0

# CUC fine part max value
CUC_FINE_MAX = 65536

# NASA CDF leapsecond table filename
CDF_LEAPSECONDSTABLE = 'CDFLeapSeconds.txt'


class TimeError(Exception):
    """Errors for the time."""


class Time(object, metaclass=Singleton):
    """
    PacketParser Time class.
    (Singleton: only one instance can be called.)

    """

    def __init__(self,
                 kernel_date=None,
                 predictive=True,
                 flown=True,
                 spice_kernel_path='',
                 lstable_file=None,
                 no_spice=False):

        # Set SPICE attributes
        self.kernel_date = kernel_date
        self.predictive = predictive
        self.flown = flown
        self.kernel_path = spice_kernel_path
        self.no_spice = no_spice

        # Initialize cached property and unloaded kernels (if any)
        self.reset()

        # If no spice, need a CDF leap second table file
        if no_spice and lstable_file:
            self.leapsec_file = lstable_file

    def reset(self, spice=True, lstable=True):
        """
        Reset spice and lstable related attribute values of the Time object.

        :param spice: If True, reset spice attribute
        :param lstable: If True, reset lstable attribute
        :return:
        """

        if lstable:
            self._leapsec_file = ''
            self._lstable = None
        if spice:
            # Make sure to unload all kernels
            if hasattr(self, '_spice') and self._spice:
                self._spice.unload_all()

            self.kernel_path = ''
            self._spice = None

    @property
    def leapsec_file(self):
        return self._leapsec_file

    @leapsec_file.setter
    def leapsec_file(self, lstable_file):
        """
        Set input leap seconds table file (and reload table if necessary).

        :param lstable_file: Path to the leap seconds table file, as provided in the NASA CDF software
        :return:
        """

        if lstable_file and lstable_file == self._leapsec_file:
            logger.debug(f'{lstable_file} already loaded')
        else:

            from maser.tools.time import Lstable

            if not lstable_file:
                if 'pipeline.environment.CDF_LEAPSECONDSTABLE' in Configuration.manager:
                    lstable_file = Configuration.manager['pipeline'][
                        'environment.CDF_LEAPSECONDSTABLE']
                elif 'CDF_LEAPSECONDSTABLE' in os.environ:
                    lstable_file = os.environ['CDF_LEAPSECONDSTABLE']
                elif 'CDF_LIB' in os.environ:
                    lstable_file = osp.join(
                        os.environ['CDF_LIB'], '..', CDF_LEAPSECONDSTABLE)
                else:
                    lstable_file = CDF_LEAPSECONDSTABLE

            try:
                lstable = Lstable(file=lstable_file)
            except:
                logger.error(f'New leap second table "{lstable_file}" cannot be loaded!')
            else:
                self._lstable = lstable
                self._leapsec_file = lstable_file

    @property
    def lstable(self):
        if not self._lstable:
            # If not alread loaded,
            # get lstable (Set self.leapsec_file to None will trigger loading table file from config. file or
            # environment variables)
            self.leapsec_file = None

        return self._lstable

    @property
    def spice(self):
        if not self._spice and not self.no_spice:
            self.spice = self._load_spice()
        return self._spice

    @spice.setter
    def spice(self, value):
        self._spice = value

    def _load_spice(self):
        """
        Load NAIF Solar Orbiter SPICE kernels for the current session.

        :return:
        """

        if not self.kernel_path:
            self.kernel_path = SpiceHarvester.spice_kernel_path()

        # Load SPICE kernels (only meta kernels for the moment)
        return SpiceHarvester.load_spice_kernels(self.kernel_path,
                                                 only_mk=True,
                                                 by_date=self.kernel_date,
                                                 predictive=self.predictive,
                                                 flown=self.flown)

    def obt_to_utc(self, cuc_time,
                   to_datetime=False,
                   to_tt2000=False):
        """
        Convert input RPW CCSDS CUC time(s) into UTC time(s).

        :param cuc_time: RPW CCSDS CUC time(s)
        :param to_datetime: If True, return UTC time as datetime object
        :param to_tt2000: If True, return TT2000 epoch time (nanosec since J2000) instead of UTC (data type is int)
        :param: predictive: If True, then use predictive SPICE kernels instead of as-flown
        :param: kernel_date: datetime object containing the date for which SPICE kernels must be loaded (if not passed, then load the latest kernels)
        :param: reset: If True, then reset Time instance harvester
        :param: no_spice: If True, dot not use SPICE toolkit to compute UTC time
        :return: utc time(s) as numpy.datetime64 datatype (datetime object if to_datetime is True)
        """

        # Make sure that cuc_time is a numpy array
        cuc_time = np.array(cuc_time)

        # Check that input cuc_time has the good shape
        shape = cuc_time.shape
        if shape == (2,):
            cuc_time = cuc_time.reshape([1, 2])

        # If no_spice = True ...
        if self.no_spice:
            # If SPICE not available, use internal routines
            # (assuming no drift of OBT or light time travel corrections
            # . It should be used for on-ground test only)
            utc_time = self.cuc_to_utc(cuc_time, to_tt2000=to_tt2000)
        else:
            spice = self.spice

            nrec = len(cuc_time)

            if not to_tt2000:
                utc_time = np.empty(nrec, dtype='datetime64[ns]')
            else:
                utc_time = np.empty(nrec, dtype=int)

            # Then use SpiceManager to compute utc
            for i, current_time in enumerate(cuc_time):

                obt = spice.cuc2obt(current_time)
                et = spice.obt2et(SOLAR_ORBITER_NAIF_ID, obt)

                if not to_tt2000:
                    utc_time[i] = spice.et2utc(et)
                else:
                    tdt = spice.et2tdt(et)
                    utc_time[i] = tdt * SEC_TO_NANOSEC

        # Convert to datetime object if to_datetime keyword is True
        if not to_tt2000 and to_datetime:
            utc_time = Time.datetime64_to_datetime(utc_time)

        return utc_time

    @staticmethod
    def cuc_to_nanosec(cuc_time, j2000=False):
        """
        Given a CCSDS CUC coarse and fine cuc_time in the numpy array format,
        returns it in nanoseconds since the defined epoch.

        :param cuc_time: input RPW CCSDS CUC time provided as numpy array
        :return: Return time in nano seconds since RPW origin (or J2000 if j2000 keyword is True) as numpy.uint64 array
        """
        # first convert cuc time into scet
        scet = Time.cuc_to_scet(cuc_time)

        # Then convert scet in nanosec
        nanosec = scet * np.float64(SEC_TO_NANOSEC)

        if j2000:
            nanosec -= np.float64(DELTA_NSEC_RPW_J2000)

        return nanosec.astype(np.uint64)

    @staticmethod
    def cuc_to_scet(cuc_time):
        """
        Return input RPW CCSDS CUC time as spacecraft elapsed time since RPW origin

        :param cuc_time: input RPW CCSDS CUC time as numpy array
        :return: spacecraft elapsed time since RPW origin as numpy.float46 array
        """

        # Make sure that input cuc_time is a numpy array
        if not isinstance(cuc_time, np.ndarray):
            cuc_time = np.array(cuc_time, dtype=np.float64)

        # Check that input cuc_time has the good shape
        shape = cuc_time.shape
        if shape == (2,):
            cuc_time = cuc_time.reshape([1, 2])

        # convert coarse part into nanoseconds
        coarse = cuc_time[:, 0].astype('float64')

        # same for fine part
        fine = cuc_time[:, 1].astype('float64')
        fine = fine / np.float64(CUC_FINE_MAX)

        return coarse + fine

    def cuc_to_utc(self, cuc_time,
                   from_nanosec=False,
                   to_tt2000=False):
        """
        Convert RPW CCSDS CUC time(s) into in UTC time(s)

        :param cuc_time: numpy uint array of RPW CCSDS CUC time(s)
        :param from_nanosec: If True, then input RPW CCSDS CUC time array is expected in nanoseconds
        :param to_tt2000: Convert input CCSDS CUC time into TT2000 epoch instead of UTC
        :return: numpy datetime64 array of UTC time(s)
        """

        if not from_nanosec:
            # Convert cuc to nanosec since RPW_BASETIME
            cuc_nanosec = self.cuc_to_nanosec(cuc_time)
        else:
            cuc_nanosec = cuc_time.astype(np.unint64)

        # Convert to TT20000 epoch time
        tt2000_epoch = cuc_nanosec + TT2000_RPW_BASETIME

        if to_tt2000:
            return tt2000_epoch
        else:
            return self.tt2000_to_utc(tt2000_epoch)

    def tt2000_to_utc(self, tt2000_epoch,
                      leap_sec=None,
                      to_datetime=True):
        """
        Convert input TT2000 epoch time into UTC time

        :param tt2000_epoch: TT2000 epoch time to convert
        :param leap_sec: number of leap second to apply
        :param to_datetime: return utc time as a datetime object (microsecond resolution)
        :return: UTC time (datetime.datetime if to_datetime=True, format returned by spice.tdt2uct otherwise)
        """

        if self.no_spice:
            # TT2000 to TT time
            tt_time = tt2000_epoch + J2000_BASETIME

            # Get leap seconds in nanosec
            if not leap_sec:
                lstable = self.lstable

                leap_nsec = np.array([lstable.get_leapsec(Time.datetime64_to_datetime(tt)) * SEC_TO_NANOSEC
                                      for tt in tt_time], dtype='timedelta64[ns]')
            else:
                leap_nsec = leap_sec * np.uint64(SEC_TO_NANOSEC)

            utc_time = tt_time - DELTA_NSEC_TAI_TT - leap_nsec
        else:
            spice = self.spice
            # Convert input TT2000 time in seconds (float)
            tdt = float(tt2000_epoch) / float(SEC_TO_NANOSEC)
            utc_time = spice.tdt2utc(tdt)
            if to_datetime:
                utc_time = datetime.strptime(utc_time,
                                             spice.TIME_ISOC_STRFORMAT)

        return utc_time

    def utc_to_tt2000(self, utc_time,
                      leap_sec=None):
        """
        Convert an input UTC time value into a TT2000 epoch time

        :param utc_time: an input UTC time value to convert (numpy.datetime64 or datetime.datetime type)
        :param leap_sec: number of leap seconds at the utc_time (only used if no_spice=True)
        :param no_spice: If True, do not use SPICE toolkit to compute tt2000 time.
        :return: TT2000 epoch time value (integer type)
        """

        # Only works with scalar value for input utc_time
        if isinstance(utc_time, list):
            utc_time = utc_time[0]

        if isinstance(utc_time, datetime):
            utc_dt64 = Time.datetime_to_datetime64(utc_time)
            utc_dt = utc_time
        elif isinstance(utc_time, np.datetime64):
            utc_dt64 = utc_time
            utc_dt = Time.datetime64_to_datetime(utc_time)
        else:
            logger.error('Unknown type for input utc_time!')
            return None

        # Compute without SPICE
        if self.no_spice:
            # Get leap seconds in nanosec
            if not leap_sec:
                lstable = self.lstable
                leap_nsec = lstable.get_leapsec(utc_dt) * SEC_TO_NANOSEC
            else:
                leap_nsec = leap_sec * np.uint64(SEC_TO_NANOSEC)

            # Get nanoseconds since J2000
            # And add leap seconds + the delta time between TAI and TT
            tt2000_epoch = int(utc_dt64 - J2000_BASETIME) \
                + DELTA_NSEC_TAI_TT + np.timedelta64(leap_nsec, 'ns')
        else:
            # Use SPICE toolkit
            spice = self.spice

            # Convert input utc to string
            utc_string = spice.utc_datetime_to_str(utc_dt)
            # Convert utc string into ephemeris time then tdt
            et = spice.utc2et(utc_string)
            tdt = spice.et2tdt(et)

            # Get tt2000_epoch in nanoseconds
            tt2000_epoch = int(tdt * SEC_TO_NANOSEC)

        return tt2000_epoch

    @staticmethod
    def cuc_to_microsec(time):
        """
        cuc_to_microsec.

        Convert a RPW CUC format time into microsec.
        """
        # convert coarse part into microseconds
        coarse = time[:, 0].astype('uint64') * 1000000

        # same for fine part
        fine = np.rint((time[:, 1].astype('uint64') * 1000000) / 65536).astype(
            'uint64'
        )

        return coarse + fine

    @staticmethod
    def cuc_to_numpy_datetime64(time):
        """
        Given a CUC format RPW time in the numpy array format
        , returns it np datetime64 format.
        (For more details about RPW CUC format see RPW-SYS-SSS-00013-LES)

        :param time: array of input CCSDS CUC times (coarse, fine)
        :return: datetime64 object of input CUC time
        """

        ns = Time.cuc_to_nanosec(time)
        base_time = RPW_BASETIME

        dt64 = np.array([
                        base_time + np.timedelta64(int(nsec), 'ns')
                        for nsec in ns
                        ], dtype=np.datetime64)

        #dt64 = Time.datetime64_to_datetime(dt64)

        return dt64

    @staticmethod
    def cuc_to_datetime(time):
        """
        Convert input CCSDS CUC RPW time into datetime object.

        :param time: array of input CCSDS CUC times (coarse, fine)
        :return: CUC time as datetime
        """

        dt = Time.cuc_to_numpy_datetime64(time)
        return Time.datetime64_to_datetime(dt)

    @staticmethod
    def numpy_datetime64_to_cuc(time, synchro_flag=False):
        """
        Given a numpy.datetime64, returns CCSDS CUC format time in the numpy array format.
        (For more details about RPW CUC format see RPW-SYS-SSS-00013-LES)

        :param time: numpy.datetime64 to convert to CCSDS CUC
        :param synchro_flag: If True, time synchro flag bit is 1 (=not sync), 0 (=sync) otherwise
        :return:numpy.array with [CUC coarse, fine, sync_flag]
        """

        # convert time into nanoseconds since 2000-01-01T00:00:00
        base_time = RPW_BASETIME

        nanoseconds = np.timedelta64(time - base_time, 'ns').item()

        # compute coarse part
        coarse = nanoseconds // SEC_TO_NANOSEC

        # compute fine part
        fine = np.rint(((nanoseconds - coarse * SEC_TO_NANOSEC) /
                        SEC_TO_NANOSEC) * 65536).astype('uint16')

        return np.array([[coarse, fine, int(synchro_flag)]])

    @staticmethod
    def extract_cuc(cuc_bytes):
        """
        Extract RPW CCSDS CUC time 48 bytes and return
        coarse, fine and sync flag

        :param cuc_bytes: 48-bytes CUC time
        :return: coarse, fine and sync flag
        """

        if not isinstance(cuc_bytes, bytes):
            cuc_bytes = bytes(cuc_bytes)

        nbytes = len(cuc_bytes)
        if nbytes != 48:
            logger.error(f'Expect 48 bytes, but {nbytes} found for input CUC time!')
            return None, None, None

        return Data(cuc_bytes, nbytes).timep(0, 0, 48)

    @staticmethod
    def str2datetime64(string):
        """
        Convert an input string in numpy.datetime64

        :param string: string of ISO8601 format 'YYYY-MM-DDThh:mm:ss.ffffffZ'
        :return: numpy.datetime64 time
        """
        return np.datetime64(string)

    @staticmethod
    def datetime64_to_datetime(datetime64_input):
        """
        Convert numpy.datetime64 object into datetime.datetime object

        :param datetime64_input: input numpy.datetime64 object to convert
        :return: datetime.datetime object
        """
        return datetime64_input.astype('M8[us]').astype('O')

    @staticmethod
    def datetime_to_datetime64(datetime_input):
        """
        Convert datetime.datetime object into numpy.datetime64 object

        :param datetime_input: datetime.datetime object to convert
        :return: numpy.datetime64 object
        """
        return np.datetime64(datetime_input)

    @staticmethod
    def tt2000_to_jd(tt2000_time):
        """
        Convert input TT2000 format time into Julian days

        :param tt2000_time: TT2000 format time (i.e., nanoseconds since J2000)
        :return: time in julian days (double)
        """
        return (float(tt2000_time) / (1000000000.0 * 3600.0 * 24.0)) + TT2000_JD_BASETIME

    @staticmethod
    def jd_to_tt2000(jd_time):
        """
        Convert input Julian day into TT2000 time

        :param jd_time: Julian day time
        :return: time in TT2000 format time (i.e., nanoseconds since J2000)
        """
        return (float(jd_time) - TT2000_JD_BASETIME) * (1000000000.0 * 3600.0 * 24.0)

    def jd_to_datetime(self, jd_time):
        """
        Convert input Julian day into datetime.datetime object

        :param jd_time: Julian day time
        :return: datetime.datime object
        """
        # convert to UTC first
        utc_time = self.tt2000_to_utc(
            np.array([
                Time.jd_to_tt2000(jd_time)]), to_datetime=True)
        return utc_time
