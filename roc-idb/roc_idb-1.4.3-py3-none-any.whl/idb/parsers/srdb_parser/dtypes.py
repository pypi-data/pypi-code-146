# -*- coding: utf-8 -*-
import numpy

# Note: we use object instead of int type where columns can contain empty values

__all__ = ['vdf_dtype', 'sw_para_dtype', 'cpc_dtype', 'pcf_dtype', 'cdf_dtype']

vdf_dtype = numpy.dtype(
    [
        ('NAME', 'U8'),  # short version name (8 char)
        ('COMMENT', 'U32'),
        ('DOMAINID', int),
        ('RELEASE', int),
        ('ISSUE', int),
    ]
)

sw_para_dtype = numpy.dtype(
    [('SCOS_NAME', 'U8'), ('SW_NAME', 'U32'), ('SW_DESCR', 'U255')]
)

cpc_dtype = numpy.dtype(
    [
        ('PNAME', 'U8'),  # Complet SRDB ID (tm/tc + kind + srdbid)
        ('DESCR', 'U24'),  # PALISADE ID
        ('PTC', int),
        ('PFC', int),
        ('DISPFMT', 'U1'),
        ('RADIX', 'U1'),
        ('UNIT', 'U4'),
        ('CATEG', 'U1'),
        ('PRFREF', 'U10'),
        ('CCAREF', 'U10'),
        ('PAFREF', 'U10'),
        ('INTER', 'U1'),
        ('DEFVAL', 'U17'),
        # ('OBTID', int),
    ]
)

pcf_dtype = numpy.dtype(
    [
        ('NAME', 'U8'),  # Complet SRDB ID (tm/tc + kind + srdbid)
        ('DESCR', 'U24'),  # PALISADE ID
        ('PID', object),  # On-board  ID  of  the  telemetry  parameter
        ('UNIT', 'U4'),
        ('PTC', int),  # Parameter Type Code.
        ('PFC', int),  # Parameter Format Code
        ('WIDTH', object),
        ('VALID', 'U8'),
        ('RELATED', 'U8'),
        ('CATEG', 'U1'),
        ('NATUR', 'U1'),
        ('CURTX', 'U10'),  # Parameter calibration identification name
        ('INTER', 'U1'),
        ('USCON', 'U1'),
        ('DECIM', object),
        ('PARVAL', 'U14'),
        ('SUBSYS', 'U8'),
        ('VALPAR', object),
        ('SPTYPE', 'U1'),
        # ('CORR', str), # Optional
        # ('OBTID', int),  # Optional
        # ('DARC', str),   # Optional
        # ('ENDIAN', str), # Optional
    ]
)

cdf_dtype = numpy.dtype(
    [
        ('CNAME', 'U8'),  # Complete SRDB ID (tm/tc + kind + srdbid)
        ('ELTYPE', 'U1'),
        ('DESCR', 'U24'),  # PALISADE ID
        ('ELLEN', int),
        ('BIT', int),
        ('GRPSIZE', int),
        ('PNAME', 'U8'),
        ('INTER', 'U1'),
        ('VALUE', 'U17'),
        ('TMID', 'U8'),
    ]
)

plf_dtype = numpy.dtype(
    [
        ('NAME', 'U8'),  # Complet SRDB ID (tm/tc + kind + srdbid)
        ('SPID', object),
        ('OFFBY', int),
        ('OFFBI', int),
        ('NBOCC', int),
        ('LGOCC', int),
        ('TIME', int),
        ('TDOCC', int),
    ]
)

cap_dtype = numpy.dtype(
    [
        ('NAME', 'U10'),  # Complet SRDB ID
        ('RAW', object),  # Raw value
        ('ENG', 'U30'),  # Eng Value
    ]
)

ccs_dtype = numpy.dtype(
    [
        ('NAME', 'U10'),  # Complet SRDB ID
        ('ENG', 'U30'),  # Eng Value
        ('RAW', int),  # Raw value
    ]
)

pas_dtype = numpy.dtype(
    [
        ('NAME', 'U10'),  # Complet SRDB ID
        ('ENG', 'U30'),  # Eng Value
        ('RAW', int),  # Raw value
    ]
)

txp_dtype = numpy.dtype(
    [
        ('NAME', 'U10'),  # Complet SRDB ID
        ('RAW', 'U14'),  # Raw value
        ('dum', 'U14'),  # dummy value (identical to raw)
        ('ENG', 'U14'),  # Eng Value
    ]
)

pcf_glob_det_dtype = numpy.dtype(
    [('GLOBALID', 'U8'), ('DETAILEDID', 'U8'), ('UNDEF', int)]
)

ccf_dtype = numpy.dtype(
    [
        ('CNAME', 'U8'),  # Complet SRDB ID (tm/tc + kind + srdbid)
        ('DESCR', 'U24'),  # PALISADE ID
        ('DESCR2', 'U64'),  # Description
        ('CTYPE', 'U8'),  # Command type
        ('CRITICAL', 'U1'),  # Y/N
        ('PKTID', 'U8'),  # Name  of  the  packet  header  (TCP_ID)
        ('TYPE', object),  # Service Type
        ('STYPE', object),  # Service Sub-Type
        (
            'APID',
            object,
        ),  # Integer value in the range (0....65535). PACKET_CATEGORY + PID.
        (
            'NPARS',
            object,
        ),  # Number of elements  (i.e. parameters or fixed areas)
        ('PLAN', 'U1'),
        ('EXEC', 'U1'),
        ('ILSCOPE', 'U1'),
        ('ILSTAGE', 'U1'),
        ('SUBSYS', object),
        ('HIPRI', 'U1'),
        ('MAPID', object),
        ('DEFSET', 'U8'),
        ('RAPID', object),
        ('ACK', object),
        ('SUBSCHED', object),
    ]
)

pid_dtype = numpy.dtype(
    [
        ('TYPE', object),
        ('STYPE', object),
        ('APID', int),
        ('PI1_VAL', object),  # SID
        ('PI2_VAL', object),
        ('SPID', object),
        ('DESCR', 'U64'),
        ('UNIT', 'U8'),
        ('TPSD', int),
        ('DFHSIZE', object),
        ('TIME', 'U1'),
        ('INTER', object),
        ('VALID', 'U1'),
        ('CHECK', object),
        ('EVENT', 'U1'),
        ('EVID', 'U17'),
    ]
)

vpd_dtype = numpy.dtype(
    [
        ('TPSD', int),
        ('POS', int),
        ('NAME', 'U8'),
        ('GRPSIZE', int),
        ('FIXREP', int),
        ('CHOICE', 'U1'),
        ('PIDREF', 'U1'),
        ('DISDESC', 'U16'),
        ('WIDTH', int),
        ('JUSTIFY', 'U1'),
        ('NEWLINE', 'U1'),
        ('DCHAR', int),
        ('FORM', 'U1'),
        ('OFFSET', int),
    ]
)

caf_dtype = numpy.dtype(
    [
        ('NUMBR', 'U10'),  # calibration identification name.
        ('DESCR', 'U32'),  # palisade id
        ('ENGFMT', 'U1'),
        ('RAWFMT', 'U1'),
        ('RADIX', 'U1'),
        ('UNIT', 'U4'),
        ('NCURVE', int),
        (
            'INTER',
            'U1',
        ),  # Controls the extrapolation behaviour for raw values outside the range
    ]
)


# numerical (de-)calibration curves
cca_dtype = numpy.dtype(
    [
        ('NUMBR', 'U10'),  # calibration identification name.
        ('DESCR', 'U24'),  # palisade id
        ('ENGFMT', 'U1'),
        ('RAWFMT', 'U1'),
        ('RADIX', 'U1'),
        ('UNIT', 'U4'),
        ('NCURVE', int),
    ]
)


txf_dtype = numpy.dtype(
    [
        ('NUMBR', 'U10'),  # calibration identification name.
        ('DESCR', 'U32'),  # palisade id
        ('RAWFMT', 'U1'),
        ('NALIAS', int),  # number of records
    ]
)


paf_dtype = numpy.dtype(
    [
        ('NUMBR', 'U10'),  # calibration identification name.
        ('DESCR', 'U24'),
        ('RAWFMT', 'U1'),
        ('NALIAS', int),  # number of records
    ]
)
