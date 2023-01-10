#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exceptions definition for FILM plugin.
"""

from poppy.core.logger import logger

__all__ = ['FilmException',
           'MetadataException',
           'UnknownPipeline',
           'AncReportProdError',
           'LoadDataSetError',
           'NoData',
           'NoEpochFoundError',
           'L0ProdFailure',
           'L1BiaProdError',
           'L1SurvProdFailure',
           'L1PostProError',
           'HkProdFailure',
           'L1SbmProdError',
           'AncBiaProdError',
           'HandlingFileError',
           'InvalidDataVersion',
           'EmptyInput']


class FilmException(Exception):
    """FILM plugin generic exception."""

    pass


class EmptyInput(Exception):
    """Exception raise if an input is empty."""

    def __init__(self, message, *args, **kwargs):
        super(EmptyInput, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message


class HandlingFileError(Exception):
    """Exception raise if issue happens when handling a file (e.g., copy, move, delete)."""

    def __init__(self, message, *args, **kwargs):
        super(HandlingFileError, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message


class MetadataException(Exception):
    """Exception raise if issue with metadata."""

    def __init__(self, message, *args, **kwargs):
        super(MetadataException, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message


class AncReportProdError(Exception):
    """Exception for summary Report production."""

    pass


class UnknownPipeline(Exception):
    """Exception for unknown pipeline ID."""

    pass


class NoEpochFoundError(Exception):
    """
    Exception raised when the no Epoch variable found
    """

    def __init__(self, message, *args, **kwargs):
        super(NoEpochFoundError, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message


class L1SurvProdFailure(Exception):
    """
    Exception raised when the L1 survey CDF production has failed
    """

    def __init__(self, message, *args, **kwargs):
        super(L1SurvProdFailure, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message


class L1PostProError(Exception):
    """
    Exception raised when the L1 survey CDF production has failed
    """

    def __init__(self, message, *args, **kwargs):
        super(L1PostProError, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message


class L0ProdFailure(Exception):
    """
    Exception raised when the L0 HDF5 production has failed
    """

    def __init__(self, message=None, *args, **kwargs):
        super(L0ProdFailure, self).__init__(*args, **kwargs)
        if message:
            logger.error(message)
            self.message = message


class HkProdFailure(Exception):
    """
    Exception raised when the HK CDF production has failed
    """

    def __init__(self, message, *args, **kwargs):
        super(HkProdFailure, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message


class LoadDataSetError(Exception):
    """
    Exception raised when dataset cannot be loaded correctly
    """

    def __init__(self, message, *args, **kwargs):
        super(LoadDataSetError, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message

    pass


class NoData(Exception):
    """
    Exception raised when no output data processed
    """

    def __init__(self, message=None, ll=logger.error,
                 *args, **kwargs):
        super(NoData, self).__init__(*args, **kwargs)
        if message is not None:
            ll(message)
            self.message = message

    pass


class L1SbmProdError(Exception):
    """Exception for L1 SBM production."""

    """
    For exceptions related to the L1 SBM data file production
    """

    def __init__(self, message, *args, **kwargs):
        super(L1SbmProdError, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message

#    logger_level = 'warning'
#    use_traceback = True

    pass


class L1BiaProdError(Exception):
    """Exception raised if L1 Bias data production has failed."""

    def __init__(self, message, *args, **kwargs):
        super(L1BiaProdError, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message

#    logger_level = 'warning'
#    use_traceback = True

    pass


class AncBiaProdError(Exception):
    """Exception raised if ANC Bias data production has failed."""

    def __init__(self, message, *args, **kwargs):
        super(AncBiaProdError, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message

#    logger_level = 'warning'
#    use_traceback = True

    pass


class InvalidDataVersion(Exception):
    """Exception raised if Data version is invalid."""

    def __init__(self, message, *args, **kwargs):
        super(InvalidDataVersion, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message

#    logger_level = 'warning'
#    use_traceback = True

    pass
