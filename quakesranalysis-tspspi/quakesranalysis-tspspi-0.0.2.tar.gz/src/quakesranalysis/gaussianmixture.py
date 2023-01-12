from lmfit import Parameters, fit_report, minimize
import numpy as np
import matplotlib.pyplot as plt

FUNTYPE_DIFFGAUSSIAN=0
FUNTYPE_GAUSSIAN=1

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def diffgaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.))) * -1.0 * (x - mu)/(sig)

def sumofgaussian(pars, x, data = None):
    vals = pars.valuesdict()

    n = vals["gaussiancount"]
    model = 0.0

    for ngauss in range(n):
        amp = vals[f"gaussian{ngauss}_amp"]
        mu = vals[f"gaussian{ngauss}_mu"]
        sig = vals[f"gaussian{ngauss}_sigma"]
        model = model + amp * gaussian(x, mu, sig)

    if data is None:
        return model
    return model - data

def sumofdiffgaussian(pars, x, data = None):
    vals = pars.valuesdict()

    n = vals["gaussiancount"]
    model = 0.0

    for ngauss in range(n):
        amp = vals[f"gaussian{ngauss}_amp"]
        mu = vals[f"gaussian{ngauss}_mu"]
        sig = vals[f"gaussian{ngauss}_sigma"]
        offs = 0
        if f"gaussian{ngauss}_off" in vals:
            off = vals[f"gaussian{ngauss}_off"]

        model = model + amp * diffgaussian(x, mu, sig) + offs

    if data is None:
        return model
    return model - data

def sumoffunctions(pars, x, data = None):
    vals = pars.valuesdict()
    n = vals["gaussiancount"]
    model = 0.0
    for nfunct in range(n):
        if vals[f"gaussian{nfunct}_type"] == FUNTYPE_DIFFGAUSSIAN:
            amp = vals[f"gaussian{nfunct}_amp"]
            mu = vals[f"gaussian{nfunct}_mu"]
            sig = vals[f"gaussian{nfunct}_sigma"]
            offs = 0
            if f"gaussian{nfunct}_off" in vals:
                off = vals[f"gaussian{nfunct}_off"]

            model = model + amp * diffgaussian(x, mu, sig) + offs
        elif vals[f"gaussian{nfunct}_type"] == FUNTYPE_GAUSSIAN:
            amp = vals[f"gaussian{nfunct}_amp"]
            mu = vals[f"gaussian{nfunct}_mu"]
            sig = vals[f"gaussian{nfunct}_sigma"]
            offs = 0
            if f"gaussian{nfunct}_off" in vals:
                off = vals[f"gaussian{nfunct}_off"]

            model = model + amp * gaussian(x, mu, sig) + offs

    if data is None:
        return model
    return model - data

def get_center_largest_minmax(x):
    maxvpos = np.argmax(x)
    minvpos = np.argmin(x)
    maxv = np.max(x)
    minv = np.min(x)
    offv = (maxv + minv) / 2
    if np.abs(minv) > np.abs(maxv):
        a = np.abs(minv)
    else:
        a = np.abs(maxv)

    if minvpos < maxvpos:
        a = -1.0 * a

    center = int((maxvpos + minvpos)/ 2)
    return a, center, offv


def decompose_gaussian_mixtures__catstrconditional(s1, s2):
    if s1 is None:
        return None
    else:
        return f"{s1}{s2}"

def decompose_gaussian_mixtures(scan, progressPrint = False, debugplots = False, debugplotPrefix = None):
    scanx = scan.get_main_axis_data()

    meanI, _, meanQ, _ = scan.get_signal_mean_iq()
    amp, _ = scan.get_signal_ampphase()

    meanIZero, _, meanQZero, _ = scan.get_zero_mean_iq()
    ampZero, _ = scan.get_zero_ampphase()
    meanIDiff, _, meanQDiff, _ = scan.get_diff_mean_iq()
    ampDiff, _ = scan.get_diff_ampphase()

    if debugplotPrefix is not None:
        print(f"[GMIX]: Debug plot prefix for all plots: {debugplotPrefix}")

    res = {
        'I' : _decompose_gaussian_mixture(scanx, meanI, progressPrint = progressPrint, debugplotPrefix=decompose_gaussian_mixtures__catstrconditional(debugplotPrefix, 'I'), debugplots = debugplots),
        'Q' : _decompose_gaussian_mixture(scanx, meanQ, progressPrint = progressPrint, debugplotPrefix=decompose_gaussian_mixtures__catstrconditional(debugplotPrefix, 'Q'), debugplots = debugplots),
        'A' : _decompose_gaussian_mixture(scanx, amp, progressPrint = progressPrint, debugplotPrefix=decompose_gaussian_mixtures__catstrconditional(debugplotPrefix, 'A'), debugplots = debugplots),
        'IZero' : _decompose_gaussian_mixture(scanx, meanIZero, progressPrint = progressPrint, debugplotPrefix=decompose_gaussian_mixtures__catstrconditional(debugplotPrefix, 'IZero'), debugplots = debugplots),
        'QZero' : _decompose_gaussian_mixture(scanx, meanQZero, progressPrint = progressPrint, debugplotPrefix=decompose_gaussian_mixtures__catstrconditional(debugplotPrefix, 'QZero'), debugplots = debugplots),
        'AZero' : _decompose_gaussian_mixture(scanx, ampZero, progressPrint = progressPrint, debugplotPrefix=decompose_gaussian_mixtures__catstrconditional(debugplotPrefix, 'AZero'), debugplots = debugplots),
        'IDiff' : _decompose_gaussian_mixture(scanx, meanIDiff, progressPrint = progressPrint, debugplotPrefix=decompose_gaussian_mixtures__catstrconditional(debugplotPrefix, 'IDiff'), debugplots = debugplots),
        'QDiff' : _decompose_gaussian_mixture(scanx, meanQDiff, progressPrint = progressPrint, debugplotPrefix=decompose_gaussian_mixtures__catstrconditional(debugplotPrefix, 'QDiff'), debugplots = debugplots),
        'ADiff' : _decompose_gaussian_mixture(scanx, ampDiff, progressPrint = progressPrint, debugplotPrefix=decompose_gaussian_mixtures__catstrconditional(debugplotPrefix, 'ADiff'), debugplots = debugplots)
    }

    return res

def decompose_gaussian_mixtures_plotcomponents(scan, component):
    fig, ax = plt.subplots(len(component), 2, figsize=(6.4 * 2, 4.8 * len(component)))

    for icomp, comp in enumerate(component):
        fit_params = Parameters()
        fit_params.add('gaussiancount', value = 1, vary = False)
        fit_params.add(f"gaussian0_type", comp['type'], vary = False)
        fit_params.add(f"gaussian0_amp", comp['amp'])
        fit_params.add(f"gaussian0_mu", comp['mu'])
        fit_params.add(f"gaussian0_sigma", comp['sigma'])
        fit_params.add(f"gaussian0_off", comp['off'])

        if comp['type'] == FUNTYPE_DIFFGAUSSIAN:
            ax[icomp][0].set_xlabel(f"{scan.get_main_axis_title()} {scan.get_main_axis_symbol()}")
            # ax[icomp][0].set_ylabel(ylabel)
            ax[icomp][0].set_title(f"Diff. Gaussian; $\mu$ = {comp['mu']:.2f}, FWHM = {2.83*comp['sigma']:.2f}")
            ax[icomp][0].plot(scan.get_main_axis_data(), sumofdiffgaussian(fit_params, scan.get_main_axis_data()), 'r--', label = "Fit")
            ax[icomp][0].legend()
            ax[icomp][0].grid()
        elif comp['type'] == FUNTYPE_GAUSSIAN:
            ax[icomp][0].set_xlabel(f"{scan.get_main_axis_title()} {scan.get_main_axis_symbol()}")
            # ax[icomp][0].set_ylabel(ylabel)
            ax[icomp][0].set_title(f"Gaussian; $\mu$ = {comp['mu']:.2f}, FWHM = {2.83*comp['sigma']:.2f}")
            ax[icomp][0].plot(scan.get_main_axis_data(), sumofgaussian(fit_params, scan.get_main_axis_data()), 'r--', label = "Fit")
            ax[icomp][0].legend()
            ax[icomp][0].grid()

        if comp['type'] == FUNTYPE_DIFFGAUSSIAN:
            ax[icomp][1].set_xlabel(f"{scan.get_main_axis_title()} {scan.get_main_axis_symbol()}")
            # ax[icomp][1].set_ylabel(ylabel)
            ax[icomp][1].plot(scan.get_main_axis_data(), sumofgaussian(fit_params, scan.get_main_axis_data()), 'g--', label = "Fit reconstruction")
            ax[icomp][1].legend()
            ax[icomp][1].grid()

    return fig, ax

def decompose_gaussian_mixtures_plotfit(scan, result):
    # Summary plot
    fig, ax = plt.subplots(len(result), 2, figsize=(6.4 * 2, 4.8 * len(result)))

    for iaxis, axis in enumerate(result):
        if axis == 'I':
            data, _, _, _ = scan.get_signal_mean_iq()
            ylabel = "I signal $\mu V$"
        elif axis == 'Q':
            _, _, data, _ = scan.get_signal_mean_iq()
            ylabel = "Q signal $\mu V$"
        elif axis == 'A':
            data, _ = scan.get_signal_ampphase()
            ylabel = "Amplitude signal $\mu V$"
        elif axis == 'IZero':
            data, _, _, _ = scan.get_zero_mean_iq()
            ylabel = 'I zero $\mu V$'
        elif axis == 'QZero':
            _, _, data, _ = scan.get_zero_mean_iq()
            ylabel = 'Q zero $\mu V$'
        elif axis == 'AZero':
            data, _ = scan.get_zero_ampphase()
            ylabel = 'Amplitude zero $\mu V$'
        elif axis == 'IDiff':
            data, _, _, _ = scan.get_diff_mean_iq()
            ylabel = 'I difference $\mu V$'
        elif axis == 'QDiff':
            _, _, data, _ = scan.get_diff_mean_iq()
            ylabel = 'Q difference $\mu V$'
        elif axis == 'ADiff':
            data, _ = scan.get_diff_ampphase()
            ylabel = 'Amplitude difference $\mu V$'

        mainaxis = scan.get_main_axis_data()

        fit_params = Parameters()
        fit_params.add('gaussiancount', value = len(result[axis]), vary = False)
        for ig, g in enumerate(result[axis]):
            fit_params.add(f"gaussian{ig}_type", g['type'])
            fit_params.add(f"gaussian{ig}_amp", g['amp'])
            fit_params.add(f"gaussian{ig}_mu", g['mu'])
            fit_params.add(f"gaussian{ig}_sigma", g['sigma'])
            fit_params.add(f"gaussian{ig}_off", g['off'])

        ax[iaxis][0].set_xlabel(f"{scan.get_main_axis_title()} {scan.get_main_axis_symbol()}")
        ax[iaxis][0].set_ylabel(ylabel)
        ax[iaxis][0].plot(mainaxis, data, label = ylabel)
        ax[iaxis][0].plot(mainaxis, sumoffunctions(fit_params, mainaxis), 'r--', label = "Fit")
        ax[iaxis][0].legend()
        ax[iaxis][0].grid()

        #ax[iaxis][1].set_xlabel(f"{scan.get_main_axis_title()} {scan.get_main_axis_symbol()}")
        #ax[iaxis][1].set_ylabel(ylabel)
        #ax[iaxis][1].plot(mainaxis, sumofgaussian(fit_params, mainaxis), 'g--', label = "Reconstruction from fit")
        #ax[iaxis][1].legend()
        #ax[iaxis][1].grid()

    plt.tight_layout()
    return fig, ax

def _decompose_gaussian_mixture(scanx, scandata, debugplots = False, debugplotPrefix = None, progressPrint = False):
    if scandata is None:
        return None

    if progressPrint:
        print("[GMIX] Starting decomposition")
        if debugplotPrefix is not None:
            print(f"[GMIX] Debug plot prefix: {debugplotPrefix}")


    startparams = []
    residuumremain = []

    lastresiduum = None
    exdata = scandata
    exdata_x = scanx

    while True:
        if len(residuumremain) > 1:
            if residuumremain[len(residuumremain)-1] > residuumremain[len(residuumremain)-2]:
                # Remove last element
                startparams = startparams[:-1]
                break

        if progressPrint:
            print(f"[GMIX] Iteration {len(residuumremain)+1}")

        # Add another gaussian to our list ... use last iteration as new start for our fit ...
        # We do this by subtracting the last "best fit", fitting a single Gaussian, then using this as a start value for the next one ...

        # Generate a temporary curve where we subtract all previous fitted ones ... or use raw data if non have been fitted before

        indata = exdata
        fit_params = Parameters()
        if len(startparams) > 0:
            fit_params.add('gaussiancount', value=len(startparams), vary = False)
            for ig, g in enumerate(startparams):
                fit_params.add(f"gaussian{ig}_type", value=g['type'], vary=False)
                fit_params.add(f"gaussian{ig}_amp", value=g['amp'])
                fit_params.add(f"gaussian{ig}_mu", value=g['mu'])
                fit_params.add(f"gaussian{ig}_sigma", value=g['sigma'])
                fit_params.add(f"gaussian{ig}_off", value=g['off'])
            indata = indata - sumoffunctions(fit_params, exdata_x)

        if debugplots:
            fig, ax = plt.subplots(1, 5, figsize=(6.4*5, 4.8))
            ax[0].plot(exdata_x, exdata, label = "Global data")
            ax[0].plot(exdata_x, indata, 'g--', label = "Next seed input")
            ax[0].grid()
            ax[0].legend()

        # Start with a first candidate and select the best one ...
        candidates = [
            FUNTYPE_DIFFGAUSSIAN,
            FUNTYPE_GAUSSIAN
        ]
        minchisq = None
        minchisqType = None
        minchisqOut = None
        minchisqParams = None

        for candidate in candidates:
            fit_params = Parameters()
            extremum_v, extremum_pos, extremum_off = get_center_largest_minmax(indata)
            fit_params.add('gaussiancount', value=1, vary = False)
            fit_params.add('gaussian0_type', value=candidate, vary=False)
            fit_params.add('gaussian0_amp', value=extremum_v)
            fit_params.add('gaussian0_mu', value=exdata_x[extremum_pos])
            fit_params.add('gaussian0_sigma', value=1)
            fit_params.add('gaussian0_off', value=extremum_off, min = 3*np.min(indata), max = 3*np.max(indata))
            out = minimize(sumoffunctions, fit_params, args=(exdata_x,), kws = {'data' : indata })
            if minchisq is None:
                minchisq = out.chisqr
                minchisqType = candidate
                minchisqOut = out
                minchisqParams = fit_params
            else:
                if out.chisqr < minchisq:
                    minchisq = out.chisqr
                    minchisqType = candidate
                    minchisqOut = out
                    minchisqParams = fit_params

        out = minchisqOut
        fit_params = minchisqParams

        if debugplots:
            ax[1].plot(exdata_x, indata, label = "Stage input")
            ax[1].plot(exdata_x, sumoffunctions(out.params, exdata_x), 'r--', label = "New seed candidate")
            ax[1].grid()
            ax[1].legend()

        startparams.append(
            {
                "type" : int(out.params['gaussian0_type']),
                "amp" : float(out.params['gaussian0_amp']),
                "mu" : float(out.params['gaussian0_mu']),
                "sigma" : float(out.params['gaussian0_sigma']),
                "off" : float(out.params['gaussian0_off'])
            }
        )

        # Now do fit with ALL parameters in a single model and refine all at once like adjusting a bundle
        fit_params = Parameters()
        fit_params.add('gaussiancount', value = len(startparams), vary = False)
        for ig, g in enumerate(startparams):
            fit_params.add(f"gaussian{ig}_type", g['type'])
            fit_params.add(f"gaussian{ig}_amp", g['amp'])
            fit_params.add(f"gaussian{ig}_mu", g['mu'])
            fit_params.add(f"gaussian{ig}_sigma", g['sigma'])
            fit_params.add(f"gaussian{ig}_off", g['off'], min = 10.0*np.min(exdata), max = 10*np.max(exdata))

        # Adjust the whole bundle ..
        try:
            out = minimize(sumoffunctions, fit_params, args=(exdata_x,), kws = {'data' : exdata })
        except Exception as e:
            startparams = startparams[:-1]
            break

        # Refine bundle using "out" data ...
        for i in range(len(startparams)):
            startparams[i]["type"] = float(out.params[f"gaussian{i}_type"])
            startparams[i]["amp"] = float(out.params[f"gaussian{i}_amp"])
            startparams[i]["mu"] = float(out.params[f"gaussian{i}_mu"])
            startparams[i]["sigma"] = float(out.params[f"gaussian{i}_sigma"])
            startparams[i]["off"] = float(out.params[f"gaussian{i}_off"])

        if debugplots:
            ax[2].plot(exdata_x, exdata, label = "Global data")
            ax[2].plot(exdata_x, sumoffunctions(out.params, exdata_x), 'r--', label = f"Fitting iteration {len(startparams)}")
            ax[2].grid()
            ax[2].legend()
        
        residuum = sumoffunctions(out.params, exdata_x) - exdata
        if debugplots:
            ax[3].plot(exdata_x, residuum, label = "Residuum")
            ax[3].grid()
            ax[3].legend()

        residuumremain.append(out.chisqr)

        if debugplots:
            ax[4].plot(residuumremain)
            ax[4].set_xlabel("Iteration")
            ax[4].set_ylabel("Chi2")

            if debugplotPrefix is not None:
                plt.savefig(f"{debugplotPrefix}_iter{len(residuumremain)-1}.png")
                # plt.savefig(f"{debugplotPrefix}_iter{len(residuumremain)-1}.svg")
                plt.close(fig)
            else:
                plt.show()

    if progressPrint:
        print("[GMIX] Done")
    return startparams