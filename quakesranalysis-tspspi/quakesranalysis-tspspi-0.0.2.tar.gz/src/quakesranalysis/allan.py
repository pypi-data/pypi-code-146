import numpy as np

import allantools

def get_allan_deviations(scan):
    # Calculate allan deviations for all samplign points along
    # main axis ...

    sigI, sigQ = scan.get_raw_signal_iq()
    sigIZ, sigQZ = scan.get_raw_zero_iq()

    adevs = {
        'I' : [],
        'Q' : [],
        'IZero' : [],
        'QZero' : [],
        'IDiff' : [],
        'QDiff' : []
    }

    for imain, mainval in enumerate(scan.get_main_axis_data()):
        # We iterate over all frequencies / field amplitudes / etc. along main axis
        taus, ad, ade, _ = allantools.oadev(sigI[imain], rate = 1.0, data_type = 'freq', taus = "all")
        adevs['I'].append({
            f"{scan.get_main_axis_symbol()}" : mainval,
            'taus' : taus,
            'ad' : ad,
            'ade' : ade
        })

        taus, ad, ade, _ = allantools.oadev(sigQ[imain], rate = 1.0, data_type = 'freq', taus = "all")
        adevs['Q'].append({
            scan.get_main_axis_symbol() : mainval,
            'taus' : taus,
            'ad' : ad,
            'ade' : ade
        })

        if sigIZ is not None:
            taus, ad, ade, _ = allantools.oadev(sigIZ[imain], rate = 1.0, data_type = 'freq', taus = "all")
            adevs['IZero'].append({
                scan.get_main_axis_symbol() : mainval,
                'taus' : taus,
                'ad' : ad,
                'ade' : ade
            })

            taus, ad, ade, _ = allantools.oadev(sigQZ[imain], rate = 1.0, data_type = 'freq', taus = "all")
            adevs['QZero'].append({
                scan.get_main_axis_symbol() : mainval,
                'taus' : taus,
                'ad' : ad,
                'ade' : ade
            })

            taus, ad, ade, _ = allantools.oadev(sigI[imain] - sigIZ[imain], rate = 1.0, data_type = 'freq', taus = "all")
            adevs['IDiff'].append({
                scan.get_main_axis_symbol() : mainval,
                'taus' : taus,
                'ad' : ad,
                'ade' : ade
            })

            taus, ad, ade, _ = allantools.oadev(sigQ[imain] - sigQZ[imain], rate = 1.0, data_type = 'freq', taus = "all")
            adevs['QDiff'].append({
                scan.get_main_axis_symbol() : mainval,
                'taus' : taus,
                'ad' : ad,
                'ade' : ade
            })

    worstadevs = {
        'I' : {
            'taus' : adevs['I'][0]['taus'],
            'ad' : np.zeros((adevs['I'][0]['ad'].shape))
        },
        'Q' : {
            'taus' : adevs['Q'][0]['taus'],
            'ad' : np.zeros((adevs['Q'][0]['ad'].shape))
        }
    }
    if sigIZ is not None:
        worstadevs['IZero'] = {
            'taus' : adevs['IZero'][0]['taus'],
            'ad' : np.zeros((adevs['IZero'][0]['ad'].shape))
        }
        worstadevs['QZero'] = {
            'taus' : adevs['QZero'][0]['taus'],
            'ad' : np.zeros((adevs['QZero'][0]['ad'].shape))
        }
        worstadevs['IDiff'] = {
            'taus' : adevs['IDiff'][0]['taus'],
            'ad' : np.zeros((adevs['IDiff'][0]['ad'].shape))
        }
        worstadevs['QDiff'] = {
            'taus' : adevs['QDiff'][0]['taus'],
            'ad' : np.zeros((adevs['QDiff'][0]['ad'].shape))
        }

    for iMain in range(len(adevs['I'])):
        for channel in worstadevs:
            if len(adevs[channel]) > 0:
                for iPos in range(len(adevs[channel][iMain]['ad'])):
                    if adevs[channel][iMain]['ad'][iPos] > worstadevs[channel]['ad'][iPos]:
                        worstadevs[channel]['ad'][iPos] = adevs[channel][iMain]['ad'][iPos]

    return adevs, worstadevs