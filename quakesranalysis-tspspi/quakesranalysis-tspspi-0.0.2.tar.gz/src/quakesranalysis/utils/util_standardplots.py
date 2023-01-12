import sys
sys.path.append("../../")
sys.path.append("../")
sys.path.append("../../../")

import numpy as np
import matplotlib.pyplot as plt

import sys
import os
import textwrap
import json

from quakesranalysis import scanhandler
from quakesranalysis import gaussianmixture
from quakesranalysis import mixturefit
from quakesranalysis import allan

def printUsage():
    print(textwrap.dedent("""
        Standard plots generation tool for QUAK/ESR

        \t{} [options] FILENAME [FILENAME ...]

        This tool accepts either runfiles or NPZ files and generates a
        selectable set of standard plots for reporting purposes. The
        set of plots is selected by different options:

        \t-iqmean\t\tGenerated I/Q mean and noise plots
        \t-apmean\t\tGenerate amplitude and phase from I/Q samples
        \t-wndnoise N\tPlots noise in a sliding window of N samples
        \t-offsettime\tPlot offset change (mean of all samples) over time
        \t-allan\tPlot allan deviations for all sampled points along main axis
        \t-mixfit\tDecompose into Gaussian and Cauchy distributions for all channels
        \t-mixfitdebug\tDump all fitting steps (might require MPLBACKEND=tkagg instead of qt?agg)
        \t-decompose\tDecompose gaussian mixture for all channels (old fitter)
        \t-metrics\tCollect core metrics in metrics.json for this run
    """).format(sys.argv[0]))

def metrics_collect_core(fileprefix, scan, metrics = {}):
    #   Allan deviation -> converges or diverges? How well is it a 1/r?

    metrics['core'] = {}

    # Spans

    meanI, stdI, meanQ, stdQ = scan.get_signal_mean_iq()
    meanIZ, stdIZ, meanQZ, stdQZ = scan.get_zero_mean_iq()
    if meanIZ is not None:
        meanIDiff, stdIDiff, meanQDiff, stdQDiff = scan.get_diff_mean_iq()

    metrics['core']['vpp_signalI'] = np.max(meanI) - np.min(meanI)
    metrics['core']['vpp_signalQ'] = np.max(meanQ) - np.min(meanQ)
    metrics['core']['mean_signalI'] = np.mean(meanI)
    metrics['core']['mean_signalQ'] = np.mean(meanQ)
    metrics['core']['maxnoise_signalI'] = np.max(stdI)
    metrics['core']['maxnoise_signalQ'] = np.max(stdQ)
    metrics['core']['meannoise_signalI'] = np.mean(stdI)
    metrics['core']['meannoise_signalQ'] = np.mean(stdQ)
    if meanIZ is not None:
        metrics['core']['vpp_signalIZero'] = np.max(meanIZ) - np.min(meanIZ)
        metrics['core']['vpp_signalQZero'] = np.max(meanQZ) - np.min(meanQZ)
        metrics['core']['vpp_signalIDiff'] = np.max(meanIDiff) - np.min(meanIDiff)
        metrics['core']['vpp_signalQDiff'] = np.max(meanQDiff) - np.min(meanQDiff)
        metrics['core']['mean_signalIZero'] = np.mean(meanIZ)
        metrics['core']['mean_signalQZero'] = np.mean(meanQZ)
        metrics['core']['mean_signalIDiff'] = np.mean(meanIDiff)
        metrics['core']['mean_signalQDiff'] = np.mean(meanQDiff)
        metrics['core']['maxnoise_signalIZero'] = np.max(stdIZ)
        metrics['core']['maxnoise_signalQZero'] = np.max(stdQZ)
        metrics['core']['maxnoise_signalIDiff'] = np.max(stdIDiff)
        metrics['core']['maxnoise_signalQDiff'] = np.max(stdQDiff)
        metrics['core']['meannoise_signalIZero'] = np.mean(stdIZ)
        metrics['core']['meannoise_signalQZero'] = np.mean(stdQZ)
        metrics['core']['meannoise_signalIDiff'] = np.mean(stdIDiff)
        metrics['core']['meannoise_signalQDiff'] = np.mean(stdQDiff)

    return metrics

def metrics_write(fileprefix, scan, metrics):
    # Write metrics file with all collected metrics ...
    with open(f"{fileprefix}_metrics.json", "w") as outfile:
        outfile.write(json.dumps(metrics))

    print(f"[METRICS] Written {fileprefix}_metrics.json")

def plot_allan(fileprefix, scan):
    print(f"[ALLAN] Starting for {fileprefix}")

    res, worstres = allan.get_allan_deviations(scan)

    maindata = scan.get_main_axis_data()

    fig, ax = plt.subplots(len(maindata), 1, squeeze = False, figsize=(6.4, 4.8 * len(maindata)))

    for i in range(len(maindata)):
        ax[i][0].set_title("Allan deviation for {} = {}".format(scan.get_main_axis_symbol(), res['I'][i][f"{scan.get_main_axis_symbol()}"]))
        ax[i][0].set_ylabel("Allan deviation")
        ax[i][0].set_xlabel("Time (samples)")
        for channel in res:
            # Check if channel is present or empty ...
            if len(res[channel]) == len(maindata):
                ax[i][0].plot(res[channel][i]['taus'], res[channel][i]['ad'], label = f"{channel}")
        ax[i][0].legend()
        ax[i][0].grid()

    plt.tight_layout()
    ##plt.savefig(f"{fileprefix}_allanall.svg")
    plt.savefig(f"{fileprefix}_allanall.png")
    plt.close(fig)
    print(f"[ALLAN] Written {fileprefix}_allanall")

    fig, ax = plt.subplots()
    ax.set_title(f"Worst Allan deviation (from all {scan.get_main_axis_symbol()})")
    ax.set_ylabel("Allan deviation")
    ax.set_xlabel("Time (samples)")
    for channel in worstres:
        ax.plot(worstres[channel]['taus'], worstres[channel]['ad'], label = f"{channel}")
    ax.legend()
    ax.grid()

    plt.tight_layout()
    ##plt.savefig(f"{fileprefix}_allan.svg")
    plt.savefig(f"{fileprefix}_allan.png")
    plt.close(fig)
    print(f"[ALLAN] Written {fileprefix}_allan")

    fig, ax = plt.subplots()
    ax.set_title(f"Worst Allan deviation (from all {scan.get_main_axis_symbol()})")
    ax.set_ylabel("Allan deviation")
    ax.set_xlabel("Time (samples)")
    ax.set_yscale('log')
    ax.set_xscale('log')
    for channel in worstres:
        ax.plot(worstres[channel]['taus'], worstres[channel]['ad'], label = f"{channel}")
    ax.legend()
    ax.grid()

    plt.tight_layout()
    #plt.savefig(f"{fileprefix}_allan_log.svg")
    plt.savefig(f"{fileprefix}_allan_log.png")
    plt.close(fig)
    print(f"[ALLAN] Written {fileprefix}_allan_log")


def plot_decompose_mixturefit(fileprefix, scan, metrics = {}, debugplots = False):
    print(f"[MIXFIT] Starting for {fileprefix}")

    mf = mixturefit.MixtureFitter()

    # Decompose for each channel in the scan ...
    scanx = scan.get_main_axis_data()
    scanxsymbol = scan.get_main_axis_symbol()

    meanI, _, meanQ, _ = scan.get_signal_mean_iq()
    amp, _ = scan.get_signal_ampphase()

    meanIZero, _, meanQZero, _ = scan.get_zero_mean_iq()
    ampZero, _ = scan.get_zero_ampphase()
    meanIDiff, _, meanQDiff, _ = scan.get_diff_mean_iq()
    ampDiff, _ = scan.get_diff_ampphase()

    metrics['decompose'] = {}

    resmixture = {
        'I' : mf.fitMixture(scanx, meanI, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_I", printprogress = True),
        'Q' : mf.fitMixture(scanx, meanQ, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_Q", printprogress = True),
        'A' : mf.fitMixture(scanx, amp, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_A", printprogress = True)
    }

    if meanIZero is not None:
        resmixture = resmixture | {
            'IZero' : mf.fitMixture(scanx, meanIZero, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_IZero", printprogress = True),
            'QZero' : mf.fitMixture(scanx, meanQZero, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_QZero", printprogress = True),
            'AZero' : mf.fitMixture(scanx, ampZero, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_AZero", printprogress = True),

            'IDiff' : mf.fitMixture(scanx, meanIDiff, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_IDiff", printprogress = True),
            'QDiff' : mf.fitMixture(scanx, meanQDiff, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_QDiff", printprogress = True),
            'ADiff' : mf.fitMixture(scanx, ampDiff, debugplots = debugplots, debugplotsshow = False, debugplotsprefix = f"{fileprefix}_mixfit_ADiff", printprogress = True)
        }

    chanlist = [ 'I', 'Q', 'A' ]
    if meanIZero is not None:
        chanlist = chanlist + [ 'IZero' , 'QZero' , 'AZero', 'IDiff', 'QDiff', 'ADiff' ]

    for chan in chanlist:
        fig, ax = mf.mixtures2barplot(resmixture[chan], yunitlabel = scanxsymbol, chanlabel = chan)
        plt.savefig(f"{fileprefix}_mixfit_{chan}.png")
        plt.close()
        print(f"[MIXFIT] Written {fileprefix}_mixfit_{chan}")

        metrics['decompose'][chan] = mf.mixtures2dictlist(resmixture[chan])

    print("[MIXFIT] Done")
    return metrics


def plot_decompose(fileprefix, scan, metrics = {}, debugplots = False):
    print(f"[DECOMPOSE] Starting for {fileprefix}")

    res = gaussianmixture.decompose_gaussian_mixtures(scan, progressPrint = True, debugplots = debugplots, debugplotPrefix=f"{fileprefix}_fitdebug_")
    fig, ax = gaussianmixture.decompose_gaussian_mixtures_plotfit(scan, res)

    #plt.savefig(f"{fileprefix}_gaussianmixture_fit.svg")
    plt.savefig(f"{fileprefix}_gaussianmixture_fit.png")
    print(f"[DECOMPOSE] Written {fileprefix}_gaussianmixture_fit")
    plt.close(fig)

    # Show fit results
    print("[DECOMPOSE]")
    print("[DECOMPOSE] \tCenter\tFWHM\tOffset\tAmplitude")

    metrics['decompose'] = {}

    for channel in res:
        metrics['decompose'][channel] = []

        res[channel] = sorted(res[channel], key=lambda x : x['mu'])
        print(f"[DECOMPOSE] Channel {channel}")
        for params in res[channel]:
            fwhm = 2.0 * np.sqrt(2.0 * np.log(2)) * params['sigma']
            print(f"[DECOMPOSE] \t{params['mu']}\t{fwhm}\t{params['off']}\t{params['amp']}")
            metrics['decompose'][channel].append({
                'type' : params['type'],
                'mu' : params['mu'],
                'fwhm' : fwhm,
                'off' : params['off'],
                'amp' : params['amp']
            })
    print("[DECOMPOSE]")

    # Generate component plots if debugplots is enabled
    if debugplots:
        for channel in res:
            fig, ax = gaussianmixture.decompose_gaussian_mixtures_plotcomponents(scan, res[channel])
            # plt.savefig(f"{fileprefix}_gaussianmixture_fitcomponents_{channel}.svg")
            plt.savefig(f"{fileprefix}_gaussianmixture_fitcomponents_{channel}.png")
            print(f"[DECOMPOSE] Written {fileprefix}_gaussianmixture_fitcomponents_{channel}.png")
            plt.close(fig)

    for channel in res:
        with open(f"{fileprefix}_gaussianmixture_peaks_{channel}.dat", 'w') as outfile:
            outfile.write("#Center\tFWHM\tOffset\tAmplitude\n")
            for params in res[channel]:
                fwhm = 2.0 * np.sqrt(2.0 * np.log(2)) * params['sigma']
                typestring = "Unknown"
                if params['type'] == gaussianmixture.FUNTYPE_DIFFGAUSSIAN:
                    typestring = "Diff. Gaussian"
                elif params['type'] == gaussianmixture.FUNTYPE_GAUSSIAN:
                    typestring = "Gaussian"

                outfile.write(f"{typestring}\t{params['mu']}\t{fwhm}\t{params['off']}\t{params['amp']}\n")
        print(f"[DECOMPOSE] Written {fileprefix}_gaussianmixture_peaks_{channel}.dat")

    print("[DECOMPOSE] Finished")

    return metrics


def plot_offsettime(fileprefix, scan):
    # Calculate offset drift over time

    print(f"[OFFSETTIME] Starting for {fileprefix}")

    sigI, sigQ = scan.get_raw_signal_iq()
    sigIZero, sigQZero = scan.get_raw_zero_iq()

    # Calculate means for each time ...
    times = len(sigI[0])

    offtimes = {
        'I' : np.zeros((times,)),
        'Q' : np.zeros((times,)),
        'Amp' : np.zeros((times,)),
        'Phase' : np.zeros((times,)),
        'IZero' : np.zeros((times,)),
        'QZero' : np.zeros((times,)),
        'ZeroAmp' : np.zeros((times,)),
        'ZeroPhase' : np.zeros((times,)),
        'IDiff' : np.zeros((times,)),
        'QDiff' : np.zeros((times,)),
        'DiffAmp' : np.zeros((times,)),
        'DiffPhase' : np.zeros((times,))
    }

    for tm in range(times):
        offtimes['I'][tm] = np.mean(sigI[:,tm])
        offtimes['Q'][tm] = np.mean(sigQ[:,tm])
        offtimes['Amp'][tm] = np.mean(np.sqrt(sigI[:,tm]*sigI[:,tm] + sigQ[:,tm]*sigQ[:,tm]))
        offtimes['Phase'][tm] = np.mean(np.arctan(sigQ[:,tm] / sigI[:,tm]))

        if sigIZero is not None:
            offtimes['IZero'][tm] = np.mean(sigIZero[:,tm])
            offtimes['QZero'][tm] = np.mean(sigQZero[:,tm])
            offtimes['ZeroAmp'][tm] = np.mean(np.sqrt(sigIZero[:,tm]*sigIZero[:,tm] + sigQZero[:,tm]*sigQZero[:,tm]))
            offtimes['ZeroPhase'][tm] = np.mean(np.arctan(sigQZero[:,tm] / sigIZero[:,tm]))

            sigIDiff = sigI[:,tm] - sigIZero[:,tm]
            sigQDiff = sigQ[:,tm] - sigQZero[:,tm]

            offtimes['IDiff'][tm] = np.mean(sigIDiff)
            offtimes['QDiff'][tm] = np.mean(sigQDiff)
            offtimes['DiffAmp'][tm] = np.mean(np.sqrt(sigIDiff * sigIDiff + sigQDiff * sigQDiff))
            offtimes['DiffPhase'][tm] = np.mean(np.arctan(sigQDiff / sigIDiff))

    # Plot ...
    if sigIZero is None:
        fig, ax = plt.subplots(1, 3, squeeze=False, figsize=(6.4 * 3, 4.8 * 1))
    else:
        fig, ax = plt.subplots(3, 3, squeeze=False, figsize=(6.4 * 3, 4.8 * 3))


    fig.suptitle("Offset drift over time")

    ax[0][0].set_title("Signal offset (I/Q)")
    ax[0][0].set_xlabel("Sample number")
    ax[0][0].set_ylabel("Offset signal $\mu V$")
    ax[0][0].plot(offtimes['I'], label = 'I Offset signal')
    ax[0][0].plot(offtimes['Q'], label = 'Q Offset signal')
    ax[0][0].legend()
    ax[0][0].grid()

    ax[0][1].set_title("Signal offset (Amplitude)")
    ax[0][1].set_xlabel("Sample number")
    ax[0][1].set_ylabel("Offset signal amplitude $\mu V$")
    ax[0][1].plot(offtimes['Amp'], label = 'Amplitude signal')
    ax[0][1].legend()
    ax[0][1].grid()

    ax[0][2].set_title("Signal offset (Phase)")
    ax[0][2].set_xlabel("Sample number")
    ax[0][2].set_ylabel("Offset signal phase $rad$")
    ax[0][2].plot(offtimes['Phase'], label = "Phase signal")
    ax[0][2].legend()
    ax[0][2].grid()

    if sigIZero is not None:
        ax[1][0].set_title("Zero offset (I/Q)")
        ax[1][0].set_xlabel("Sample number")
        ax[1][0].set_ylabel("Offset zero $\mu V$")
        ax[1][0].plot(offtimes['IZero'], label = 'I Offset zero signal')
        ax[1][0].plot(offtimes['QZero'], label = 'Q Offset zero signal')
        ax[1][0].legend()
        ax[1][0].grid()

        ax[1][1].set_title("Zero offset (Amplitude)")
        ax[1][1].set_xlabel("Sample number")
        ax[1][1].set_ylabel("Offset zero amplitude $\mu V$")
        ax[1][1].plot(offtimes['ZeroAmp'], label = 'Amplitude zero')
        ax[1][1].legend()
        ax[1][1].grid()

        ax[1][2].set_title("Zero offset (Phase)")
        ax[1][2].set_xlabel("Sample number")
        ax[1][2].set_ylabel("Offset zero phase $rad$")
        ax[1][2].plot(offtimes['ZeroPhase'], label = "Phase zero")
        ax[1][2].legend()
        ax[1][2].grid()

        ax[2][0].set_title("Difference offset (I/Q)")
        ax[2][0].set_xlabel("Sample number")
        ax[2][0].set_ylabel("Offset difference $\mu V$")
        ax[2][0].plot(offtimes['IDiff'], label = 'I Offset difference signal')
        ax[2][0].plot(offtimes['QDiff'], label = 'Q Offset difference signal')
        ax[2][0].legend()
        ax[2][0].grid()

        ax[2][1].set_title("Difference offset (Amplitude)")
        ax[2][1].set_xlabel("Sample number")
        ax[2][1].set_ylabel("Offset difference amplitude $\mu V$")
        ax[2][1].plot(offtimes['DiffAmp'], label = 'Amplitude difference')
        ax[2][1].legend()
        ax[2][1].grid()

        ax[2][2].set_title("Difference offset (Phase)")
        ax[2][2].set_xlabel("Sample number")
        ax[2][2].set_ylabel("Offset difference phase $rad$")
        ax[2][2].plot(offtimes['DiffPhase'], label = "Phase difference")
        ax[2][2].legend()
        ax[2][2].grid()

    plt.tight_layout()
    #plt.savefig(f"{fileprefix}_offsettime.svg")
    plt.savefig(f"{fileprefix}_offsettime.png")
    plt.close(fig)
    print(f"[OFFSETTIME] Written {fileprefix}_offsettime")
    print("[OFFSETTIME] Finished")


def plot_wndnoise(fileprefix, scan, job):
    wndSize = job['n']

    print(f"[WNDNOISE] Starting for {fileprefix}, window size {wndSize}")

    sigI, sigQ = scan.get_raw_signal_iq()
    sigIZero, sigQZero = scan.get_raw_zero_iq()

    windowCount = len(sigI[0]) - wndSize + 1
    mainlen = len(sigI)

    noiseData = {
        'I' : np.zeros((windowCount,)),
        'Q' : np.zeros((windowCount,)),
        'IMax' : np.zeros((windowCount,)),
        'QMax' : np.zeros((windowCount,)),

        'IZero' : np.zeros((windowCount,)),
        'QZero' : np.zeros((windowCount,)),
        'IMaxZero' : np.zeros((windowCount,)),
        'QMaxZero' : np.zeros((windowCount,)),

        'IDiff' : np.zeros((windowCount,)),
        'QDiff' : np.zeros((windowCount,)),
        'IMaxDiff' : np.zeros((windowCount,)),
        'QMaxDiff' : np.zeros((windowCount,))
    }

    pctfinishedLast = None
    for xstart in range(windowCount):
        # We have to recalculate std and mean ourself ...
        pctfinished = int((xstart / windowCount) * 100)
        if pctfinishedLast != pctfinished:
            pctfinishedLast = pctfinished
            if pctfinished % 10 == 0:
                print(f"[WNDNOISE] Start index {xstart}, {pctfinished}% done")

        stdI = np.zeros((mainlen,))
        stdQ = np.zeros((mainlen,))

        if sigIZero is not None:
            stdIZero = np.zeros((mainlen,))
            stdQZero = np.zeros((mainlen,))
            stdIDiff = np.zeros((mainlen,))
            stdQDiff = np.zeros((mainlen,))

        for imain in range(mainlen):
            stdI[imain] = np.std(sigI[imain][xstart:xstart+wndSize-1])
            stdQ[imain] = np.std(sigQ[imain][xstart:xstart+wndSize-1])
            if sigIZero is not None:
                stdIZero[imain] = np.std(sigIZero[imain][xstart:xstart+wndSize-1])
                stdQZero[imain] = np.std(sigQZero[imain][xstart:xstart+wndSize-1])
                stdIDiff[imain] = np.std(sigI[imain][xstart:xstart+wndSize-1] - sigIZero[imain][xstart:xstart+wndSize-1])
                stdQDiff[imain] = np.std(sigQ[imain][xstart:xstart+wndSize-1] - sigQZero[imain][xstart:xstart+wndSize-1])

        noiseData['I'][xstart] = np.max(stdI)
        noiseData['Q'][xstart] = np.max(stdQ)
        noiseData['IMax'][xstart] = np.argmax(stdI)
        noiseData['QMax'][xstart] = np.argmax(stdQ)

        if sigIZero is not None:
            noiseData['IZero'][xstart] = np.max(stdIZero)
            noiseData['QZero'][xstart] = np.max(stdQZero)
            noiseData['IMaxZero'][xstart] = np.argmax(stdIZero)
            noiseData['QMaxZero'][xstart] = np.argmax(stdQZero)

            noiseData['IDiff'][xstart] = np.max(stdIDiff)
            noiseData['QDiff'][xstart] = np.max(stdQDiff)
            noiseData['IMaxDiff'][xstart] = np.argmax(stdIDiff)
            noiseData['QMaxDiff'][xstart] = np.argmax(stdQDiff)

    if sigIZero is None:
        fig, ax = plt.subplots(1, 2, squeeze=False, figsize=(6.4 * 1, 4.8 * 2))
    else:
        fig, ax = plt.subplots(3, 2, figsize=(6.4 * 3, 4.8 * 2))

    fig.suptitle(f"Noise in window (width: {wndSize} samples")
    ax[0][0].set_title("Signal noise")
    ax[0][0].set_xlabel("Window start sample")
    ax[0][0].set_ylabel("Noise maximum $\mu V$")
    ax[0][0].plot(noiseData['I'], label = 'I')
    ax[0][0].plot(noiseData['Q'], label = 'Q')
    ax[0][0].grid()
    ax[0][0].legend()

    ax[0][1].set_title("Signal noise maximum position")
    ax[0][1].set_xlabel("Window start sample")
    ax[0][1].set_ylabel(f"Maximum position {scan.get_main_axis_symbol()}")
    ax[0][1].plot(noiseData['IMax'], label = 'I')
    ax[0][1].plot(noiseData['QMax'], label = 'Q')
    ax[0][1].grid()
    ax[0][1].legend()

    if sigIZero is not None:
        ax[1][0].set_title("Zero noise")
        ax[1][0].set_xlabel("Window start sample")
        ax[1][0].set_ylabel("Noise maximum $\mu V$")
        ax[1][0].plot(noiseData['IZero'], label = 'IZero')
        ax[1][0].plot(noiseData['QZero'], label = 'QZero')
        ax[1][0].grid()
        ax[1][0].legend()

        ax[1][1].set_title("Zero noise maximum position")
        ax[1][1].set_xlabel("Window start sample")
        ax[1][1].set_ylabel(f"Maximum position {scan.get_main_axis_symbol()}")
        ax[1][1].plot(noiseData['IMaxZero'], label = 'IZero')
        ax[1][1].plot(noiseData['QMaxZero'], label = 'QZero')
        ax[1][1].grid()
        ax[1][1].legend()

        ax[2][0].set_title("Difference noise")
        ax[2][0].set_xlabel("Window start sample")
        ax[2][0].set_ylabel("Noise maximum $\mu V$")
        ax[2][0].plot(noiseData['IDiff'], label = 'IDiff')
        ax[2][0].plot(noiseData['QDiff'], label = 'QDiff')
        ax[2][0].grid()
        ax[2][0].legend()

        ax[2][1].set_title("Difference noise maximum position")
        ax[2][1].set_xlabel("Window start sample")
        ax[2][1].set_ylabel(f"Maximum position {scan.get_main_axis_symbol()}")
        ax[2][1].plot(noiseData['IMaxDiff'], label = 'IDiff')
        ax[2][1].plot(noiseData['QMaxDiff'], label = 'QDiff')
        ax[2][1].grid()
        ax[2][1].legend()

    plt.tight_layout()
    #plt.savefig(f"{fileprefix}_wndnoise_{wndSize}.svg")
    plt.savefig(f"{fileprefix}_wndnoise_{wndSize}.png")
    plt.close(fig)
    print(f"[WNDNOISE] Written {fileprefix}_wndnoise_{wndSize}")
    print("[WNDNOISE] Finished")

def plot_ampphase(fileprefix, scan):
    print(f"[AMPHASE] Starting for {fileprefix}")

    x = scan.get_main_axis_data()
    xlabel = f"{scan.get_main_axis_title()} {scan.get_main_axis_symbol()}"

    fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))
    amp, phase = scan.get_signal_ampphase()

    ax[0].set_xlabel(xlabel)
    ax[0].set_ylabel("Amplitude $\mu V$")
    ax[0].plot(x, amp, label = "Amplitude")
    ax[0].legend()
    ax[0].grid()

    ax[1].set_xlabel(xlabel)
    ax[1].set_ylabel("Phase $rad$")
    ax[1].plot(x, phase, label = "Istd")
    ax[1].legend()
    ax[1].grid()

    plt.tight_layout()
    #plt.savefig(f"{fileprefix}_signal_ap.svg")
    plt.savefig(f"{fileprefix}_signal_ap.png")
    print(f"[AMPHASE] Written {fileprefix}_signal")
    plt.close(fig)

    amp, phase = scan.get_zero_ampphase()
    if amp is not None:
        fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

        ax[0].set_xlabel(xlabel)
        ax[0].set_ylabel("Zero amplitude $\mu V$")
        ax[0].plot(x, amp, label = "Zero amplitude")
        ax[0].legend()
        ax[0].grid()

        ax[1].set_xlabel(xlabel)
        ax[1].set_ylabel("Zero phase $rad$")
        ax[1].plot(x, phase, label = "Zero phase")
        ax[1].legend()
        ax[1].grid()

        plt.tight_layout()
        #plt.savefig(f"{fileprefix}_zero_ap.svg")
        plt.savefig(f"{fileprefix}_zero_ap.png")
        print(f"[AMPHASE] Written {fileprefix}_zero_ap")
        plt.close(fig)

        amp, phase = scan.get_diff_ampphase()
        fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

        ax[0].set_xlabel(xlabel)
        ax[0].set_ylabel("Difference amplitude $\mu V$")
        ax[0].plot(x, amp, label = "Difference amplitude")
        ax[0].legend()
        ax[0].grid()

        ax[1].set_xlabel(xlabel)
        ax[1].set_ylabel("Difference phase $rad$")
        ax[1].plot(x, phase, label = "Difference phase")
        ax[1].legend()
        ax[1].grid()

        plt.tight_layout()
        #plt.savefig(f"{fileprefix}_diff_ap.svg")
        plt.savefig(f"{fileprefix}_diff_ap.png")
        print(f"[AMPHASE] Written {fileprefix}_diff_ap")
        plt.close(fig)
    print("[AMPHASE] Finished")


def plot_iqmean(fileprefix, scan):
    print(f"[IQMEAN] Starting for {fileprefix}")
    x = scan.get_main_axis_data()
    xlabel = f"{scan.get_main_axis_title()} {scan.get_main_axis_symbol()}"

    fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))
    meanI, stdI, meanQ, stdQ = scan.get_signal_mean_iq()

    ax[0].set_xlabel(xlabel)
    ax[0].set_ylabel("Signal $\mu V$")
    ax[0].plot(x, meanI, label = "I")
    ax[0].plot(x, meanQ, label = "Q")
    ax[0].legend()
    ax[0].grid()

    ax[1].set_xlabel(xlabel)
    ax[1].set_ylabel("Noise $\mu V$")
    ax[1].plot(x, stdI, label = "Istd")
    ax[1].plot(x, stdQ, label = "Qstd")
    ax[1].legend()
    ax[1].grid()

    plt.tight_layout()
    #plt.savefig(f"{fileprefix}_signal.svg")
    plt.savefig(f"{fileprefix}_signal.png")
    print(f"[IQMEAN] Written {fileprefix}_signal")
    plt.close(fig)

    meanI, stdI, meanQ, stdQ = scan.get_zero_mean_iq()
    if meanI is not None:
        fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

        ax[0].set_xlabel(xlabel)
        ax[0].set_ylabel("Zero signal $\mu V$")
        ax[0].plot(x, meanI, label = "IZero")
        ax[0].plot(x, meanQ, label = "QZero")
        ax[0].legend()
        ax[0].grid()

        ax[1].set_xlabel(xlabel)
        ax[1].set_ylabel("Zero noise $\mu V$")
        ax[1].plot(x, stdI, label = "IZero std")
        ax[1].plot(x, stdQ, label = "QZero std")
        ax[1].legend()
        ax[1].grid()

        plt.tight_layout()
        #plt.savefig(f"{fileprefix}_zero.svg")
        plt.savefig(f"{fileprefix}_zero.png")
        print(f"[IQMEAN] Written {fileprefix}_zero")
        plt.close(fig)

        meanI, stdI, meanQ, stdQ = scan.get_diff_mean_iq()
        fig, ax = plt.subplots(1, 2, figsize=(6.4*2, 4.8))

        ax[0].set_xlabel(xlabel)
        ax[0].set_ylabel("Difference signal $\mu V$")
        ax[0].plot(x, meanI, label = "IDiff")
        ax[0].plot(x, meanQ, label = "QDiff")
        ax[0].legend()
        ax[0].grid()

        ax[1].set_xlabel(xlabel)
        ax[1].set_ylabel("Difference noise $\mu V$")
        ax[1].plot(x, stdI, label = "IDiff std")
        ax[1].plot(x, stdQ, label = "QDiff std")
        ax[1].legend()
        ax[1].grid()

        plt.tight_layout()
        #plt.savefig(f"{fileprefix}_diff.svg")
        plt.savefig(f"{fileprefix}_diff.png")
        print(f"[IQMEAN] Written {fileprefix}_diff")
        plt.close(fig)

    print("[IQMEAN] Finished")


def main():
    jobs = []
    jobfiles = []

    if len(sys.argv) < 2:
        printUsage()
        sys.exit(0)

    # We get called with one or more runfiles or NPZs as argument ...
    i = 1
    while i < len(sys.argv):
        if sys.argv[i].strip() == "-iqmean":
            jobs.append({ 'task' : 'iqmean' })
        elif sys.argv[i].strip() == "-apmean":
            jobs.append({ 'task' : 'apmean' })
        elif sys.argv[i].strip() == "-offsettime":
            jobs.append({ 'task' : 'offsettime' })
        elif sys.argv[i].strip() == "-decompose":
            jobs.append({ 'task' : 'decompose', 'debug' : False })
        elif sys.argv[i].strip() == "-decomposedebug":
            jobs.append({ 'task' : 'decompose', 'debug' : True })
        elif sys.argv[i].strip() == "-mixfit":
            jobs.append({ 'task' : 'mixfit', 'debug' : False })
        elif sys.argv[i].strip() == "-mixfitdebug":
            jobs.append({ 'task' : 'mixfit', 'debug' : True })
        elif sys.argv[i].strip() == "-allan":
            jobs.append({ 'task' : 'allan' })
        elif sys.argv[i].strip() == "-metrics":
            jobs.append({ 'task' : 'metrics' })
        elif sys.argv[i].strip() == "-wndnoise":
            n = 0
            if i == (len(sys.argv)-1):
                print("Missing length argument for wndnoise, require window size")
                sys.exit(1)
            try:
                n = int(sys.argv[i+1])
            except:
                print(f"Failed to interpret {sys.argv[i+1]} as window size (integer sample count)")
                sys.exit(1)
            if n < 1:
                print(f"Failed to interpret {sys.argv[i+1]} as window size (has to be a positive integer sample count)")
                sys.exit(1)
            jobs.append({'task' : 'wndnoise', 'n' : n })
            # Skip N
            i = i + 1
        else:
            if sys.argv[i].strip().startswith("-"):
                print(f"Unrecognized option {sys.argv[i]}")
                sys.exit(1)

            # Check if file exists
            if os.path.isfile(sys.argv[i].strip()):
                if (not sys.argv[i].strip().endswith(".npz")) and (not sys.argv[i].strip().endswith("_run.txt")):
                    print(f"Unrecognized file type for file {sys.argv[i]} (by name)")
                    sys.exit(1)
                jobfiles.append(sys.argv[i].strip())
            else:
                print(f"File {sys.argv[i]} not found")
        i = i + 1

    for jobfile in jobfiles:
        sc = None
        if jobfile.endswith(".npz"):
            # Try to load as single scan or as 1D scan
            try:
                sc = scanhandler.load_npz(jobfile)
            except Exception as e:
                print(f"Failed to load {jobfile} due to NPZ error:")
                print(e)

        # Execute jobs ...
        scans = sc.get_scans()
        for iscan, scan in enumerate(scans):
            metrics = {}
            if len(scans) > 2:
                fnprefix = f"{jobfile}"
            else:
                fnprefix = f"{jobfile}_scan{iscan}"
            for job in jobs:
                if job['task'] == "iqmean":
                    plot_iqmean(fnprefix, scan)
                if job['task'] == "apmean":
                    plot_ampphase(fnprefix, scan)
                if job['task'] == "wndnoise":
                    plot_wndnoise(fnprefix, scan, job)
                if job['task'] == "offsettime":
                    plot_offsettime(fnprefix, scan)
                if job['task'] == "decompose":
                    metrics = plot_decompose(fnprefix, scan, metrics = metrics, debugplots = job['debug'])
                if job['task'] == "allan":
                    plot_allan(fnprefix, scan)
                if job['task'] == "metrics":
                    metrics = metrics_collect_core(fnprefix, scan, metrics)
                    metrics_write(fnprefix, scan, metrics)
                if job['task'] == "mixfit":
                    metrics = plot_decompose_mixturefit(fnprefix, scan, metrics = metrics, debugplots = job['debug'])

if __name__ == "__main__":
    main()