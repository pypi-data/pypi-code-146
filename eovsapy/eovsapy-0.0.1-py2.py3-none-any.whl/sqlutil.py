from .util import Time
import numpy as np
from . import cal_header as ch
from .util import extract

def sql2refcalX(trange, *args, **kwargs):
    ''' Returns SQL refcal calibration records for the given timerange. trange can be either a timestamp or a timerange.'''

    caltype = 8
    xml, bufs = ch.read_calX(caltype, t=trange, *args, **kwargs)
    if isinstance(bufs, np.ndarray):
        refcals = []
        for i, buf in enumerate(bufs):
            try:
                ref = extract(buf, xml['Refcal_Real']) + extract(buf, xml['Refcal_Imag']) * 1j
                flag = extract(buf, xml['Refcal_Flag'])
                fghz = extract(buf, xml['Fghz'])
                sigma = extract(buf, xml['Refcal_Sigma'])
                timestamp = Time(extract(buf, xml['Timestamp']), format='lv')
                tbg = Time(extract(buf, xml['T_beg']), format='lv')
                ted = Time(extract(buf, xml['T_end']), format='lv')
                pha = np.angle(ref)
                amp = np.absolute(ref)
                refcals.append({'pha': pha, 'amp': amp, 'flag': flag, 'fghz': fghz, 'sigma': sigma, 'timestamp': timestamp, 't_bg': tbg, 't_ed': ted})
            except:
                print('failed to load record {} ---> {}'.format(i + 1, Time(extract(buf, xml['Timestamp']), format='lv').iso))
        return refcals
    elif isinstance(bufs, bytes):
        refcal = extract(bufs, xml['Refcal_Real']) + extract(bufs, xml['Refcal_Imag']) * 1j
        flag = extract(bufs, xml['Refcal_Flag'])
        fghz = extract(bufs, xml['Fghz'])
        sigma = extract(bufs, xml['Refcal_Sigma'])
        timestamp = Time(extract(bufs, xml['Timestamp']), format='lv')
        tbg = Time(extract(bufs, xml['T_beg']), format='lv')
        ted = Time(extract(bufs, xml['T_end']), format='lv')
        pha = np.angle(refcal)
        amp = np.absolute(refcal)
        return {'pha': pha, 'amp': amp, 'flag': flag, 'fghz': fghz, 'sigma': sigma, 'timestamp': timestamp, 't_bg': tbg, 't_ed': ted}


def sql2phacalX(trange, *args, **kwargs):
    '''Supply a timestamp in Time format, return the closest phacal data.
        If a time range is provided, return records within the time range.'''
    from . import cal_header as ch
    from .util import extract
    xml, bufs = ch.read_calX(9, t=trange, *args, **kwargs)
    if isinstance(bufs, np.ndarray):
        phacals = []
        for i, buf in enumerate(bufs):
            try:
                phacal_flag = extract(buf, xml['Phacal_Flag'])
                fghz = extract(buf, xml['Fghz'])
                sigma = extract(buf, xml['Phacal_Sigma'])
                timestamp = Time(extract(buf, xml['Timestamp']), format='lv')
                tbg = Time(extract(buf, xml['T_beg']), format='lv')
                ted = Time(extract(buf, xml['T_end']), format='lv')
                pha = extract(buf, xml['Phacal_Pha'])
                amp = extract(buf, xml['Phacal_Amp'])
                tmp = extract(buf, xml['MBD'])
                poff, pslope = tmp[:, :, 0], tmp[:, :, 1]
                flag = extract(buf, xml['Flag'])[:, :, 0]
                t_ref = Time(extract(buf, xml['T_refcal']), format='lv')
                phacals.append({'pslope': pslope, 't_pha': timestamp, 'flag': flag, 'poff': poff, 't_ref': t_ref,
                                'phacal': {'pha': pha, 'amp': amp, 'flag': phacal_flag, 'fghz': fghz, 'sigma': sigma, 'timestamp': timestamp,
                                           't_bg': tbg, 't_ed': ted}})
            except:
                print('failed to load record {} ---> {}'.format(i + 1, Time(extract(buf, xml['Timestamp']), format='lv').iso))
        return phacals
    elif isinstance(bufs, bytes):
        phacal_flag = extract(bufs, xml['Phacal_Flag'])
        fghz = extract(bufs, xml['Fghz'])
        sigma = extract(bufs, xml['Phacal_Sigma'])
        timestamp = Time(extract(bufs, xml['Timestamp']), format='lv')
        tbg = Time(extract(bufs, xml['T_beg']), format='lv')
        ted = Time(extract(bufs, xml['T_end']), format='lv')
        pha = extract(bufs, xml['Phacal_Pha'])
        amp = extract(bufs, xml['Phacal_Amp'])
        tmp = extract(bufs, xml['MBD'])
        poff, pslope = tmp[:, :, 0], tmp[:, :, 1]
        flag = extract(bufs, xml['Flag'])[:, :, 0]
        t_ref = Time(extract(bufs, xml['T_refcal']), format='lv')
        return {'pslope': pslope, 't_pha': timestamp, 'flag': flag, 'poff': poff, 't_ref': t_ref,
                'phacal': {'pha': pha, 'amp': amp, 'flag': phacal_flag, 'fghz': fghz, 'sigma': sigma, 'timestamp': timestamp, 't_bg': tbg,
                           't_ed': ted}}