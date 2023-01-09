import numpy as np
import os
import matplotlib.pyplot as plt
import csv
import pylab
import matplotlib.ticker
import sys
import pandas as pd
import sys
import scipy.stats as sc
import matplotlib
import glob

from pudb import set_trace as bp  # noqa: F401

def PLOT2(
    DATA_ID,
    i_Profile,
    DATA_PRO,
    CODE_DIR,
    Bande,
    DATA_DIR,
    Threshold_Cor,
    Threshold_Surf,
    DATA_FINAL_DIR,
    PLOT_DIR,
    Threshold_int,
):

    ############################## NEW PART #########################
    ############################## PATZOLD FINDER ###################

    DATA = DATA_ID[i_Profile]

    ###Loading Python output#################################################################################

    Python_OUT_IONO = []
    N_data_IONO = []

    # output filename
    Python_OUT_IONO.append(
        DATA_FINAL_DIR + "/" + Bande + "-IONO-" + str(i_Profile + 1) + ".txt"
    )

    output_data_IONO = np.genfromtxt(Python_OUT_IONO[-1], dtype=None)
    N_data_IONO = len(output_data_IONO)
    ET = []
    Doppler = []
    Doppler_debias = []
    Doppler_biasfit = []
    distance = []
    refractivity1 = []
    Ne = []
    error = []
    error_refrac1 = []
    error_elec = []
    TEC = []

    for i in range(N_data_IONO):
        ET.append(output_data_IONO[i][0])
        Doppler.append(output_data_IONO[i][1])
        Doppler_debias.append(output_data_IONO[i][2])
        Doppler_biasfit.append(output_data_IONO[i][3])
        distance.append(output_data_IONO[i][4])
        refractivity1.append(output_data_IONO[i][5])
        Ne.append(output_data_IONO[i][6])
        error.append(output_data_IONO[i][7])
        error_refrac1.append(output_data_IONO[i][8])
        error_elec.append(output_data_IONO[i][9])
        TEC.append(output_data_IONO[i][10])

    Python_OUT_ATMO = []
    N_data_ATMO = []

    # output filename
    Python_OUT_ATMO.append(
        DATA_FINAL_DIR + "/" + Bande + "-ATMO-" + str(i_Profile + 1) + ".txt"
    )

    # print('*** ' + Python_OUT[-1] + '\n')
    output_data_ATMO = np.genfromtxt(Python_OUT_ATMO[-1], dtype=None)
    N_data_ATMO = len(output_data_ATMO)
    ET = []
    Doppler = []
    Doppler_debias = []
    Doppler_biasfit = []
    distance = []
    refractivity2 = []
    Nn = []
    error = []
    error_refrac2 = []
    error_neut = []
    P_low = []
    P_med = []
    P_upp = [] 
    T_low = []
    T_med = [] 
    T_upp = []

    for i in range(N_data_ATMO):
        ET.append(output_data_IONO[i][0])
        Doppler.append(output_data_ATMO[i][1])
        Doppler_debias.append(output_data_ATMO[i][2])
        Doppler_biasfit.append(output_data_ATMO[i][3])
        distance.append(output_data_ATMO[i][4])
        refractivity2.append(output_data_ATMO[i][5])
        Nn.append(output_data_ATMO[i][6])
        error.append(output_data_ATMO[i][7])
        error_refrac2.append(output_data_ATMO[i][8])
        error_neut.append(output_data_ATMO[i][9])
        P_low.append(output_data_ATMO[i][10])
        P_med.append(output_data_ATMO[i][11])
        P_upp.append(output_data_ATMO[i][12])
        T_low.append(output_data_ATMO[i][13])
        T_med.append(output_data_ATMO[i][14])
        T_upp.append(output_data_ATMO[i][15])

    # #########print L2_data#################################################################################
    # os.chdir(DATA_PRO)
    # PATH = os.path.normpath(DATA_PRO + os.sep + os.pardir)

    # if Bande == 'X':
    #     if os.path.getsize(PATH+'/INFORMATION/PATH_X.txt') == 0 :
    #         print('No data available in X')
    #         sys.exit('No data to plot')
    #     else:
    #         file = open(PATH+'/INFORMATION/PATH_X.txt', 'r')
    #         PATH_X = file.read()
    #         L2_data = np.genfromtxt(PATH_X,dtype=None)
    # else :
    #     if os.path.getsize(PATH+'/INFORMATION/PATH_S.txt') == 0 :
    #         print('No data available in S')
    #         sys.exit('No data to plot')
    #     else:
    #         file = open(PATH+'/INFORMATION/PATH_S.txt', 'r')
    #         PATH_S = file.read()
    #         L2_data = np.genfromtxt(PATH_S,dtype=None)

    ########Plot files##########################################################################
    # retval = os.getcwd()
    # print("Current working directory %s" % retval)

    distance = (np.array(distance) - Threshold_Surf) / 1e3
    # min_y = Threshold_Surf
    # max_y = Threshold_Cor

    # min_y = Threshold_Surf
    # max_y = Threshold_Cor
    Doppler = np.array(Doppler)
    Doppler_debias = np.array(Doppler_debias)
    cond_dop = np.logical_and(
        Doppler < 1, distance <= ((Threshold_int - Threshold_Surf) / 1e3)
    )
    cond_deb = np.logical_and(
        Doppler_debias < 1, distance <= ((Threshold_int - Threshold_Surf) / 1e3)
    )

    fig6 = plt.figure(6)
    plt.errorbar(
        Doppler,
        distance,
        xerr=np.array(error),
        fmt="o",
        color="black",
        ecolor="lightgray",
        elinewidth=1,
        capsize=1,
        ms=1,
        label="Raw L2 Data " + DATA,
    )  # (1+880./749.)
    plt.errorbar(
        Doppler_debias,
        distance,
        xerr=np.array(error),
        fmt="o",
        color="red",
        ecolor="lightgray",
        elinewidth=1,
        capsize=1,
        ms=1,
        label="Debias Raw L2 Data " + DATA,
    )  # (1+880./749.)

    Doppler1 = Doppler[cond_dop]
    Doppler_debias1 = Doppler_debias[cond_deb]

    min_x1 = (
        np.nanmedian(Doppler_debias1)
        - sc.median_absolute_deviation(Doppler_debias1, nan_policy="omit") * 5
    )
    min_x2 = (
        np.nanmedian(Doppler1)
        - sc.median_absolute_deviation(Doppler1, nan_policy="omit") * 5
    )
    max_x1 = (
        np.nanmedian(Doppler_debias1)
        + sc.median_absolute_deviation(Doppler_debias1, nan_policy="omit") * 5
    )
    max_x2 = (
        np.nanmedian(Doppler1)
        + sc.median_absolute_deviation(Doppler1, nan_policy="omit") * 5
    )
    min_x = min([min_x1, min_x2])
    max_x = max([max_x1, max_x2])
    max_y = (Threshold_int - Threshold_Surf) / 1e3
    plt.xlabel("Doppler Frequency Residuals (Hz)", fontsize=13)
    plt.ylabel("Altitude (km)", fontsize=13)
    plt.xlim(min_x, max_x)
    plt.ylim(ymin=0, ymax=max_y)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.grid(True)
    plt.legend()
    fig6.set_size_inches(8, 6)  # Inch

    if Bande == "X":
        plt.savefig(PLOT_DIR + "/" + "Doppler_X1.png", dpi=600)
    else:
        plt.savefig(PLOT_DIR + "/" + "Doppler_S1.png", dpi=600)
    plt.close(fig6)

    """
    fig7 = plt.figure(7)
    plt.errorbar(Doppler,distance,xerr=np.array(error), fmt='o', color='black',
                 ecolor='lightgray', elinewidth=1, capsize=1, ms = 1, label = 'Raw L2 Data '+DATA)#(1+880./749.)

    plt.xlabel('Doppler Frequency Residuals (Hz)',fontsize=13)
    plt.ylabel('Altitude (km)',fontsize=13)
    plt.xlim(min_x, max_x)
    plt.ylim(ymin=0,ymax=max_y)
    plt.legend()
    fig7.set_size_inches(8, 6) #Inch
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.grid(True)
    if Bande == 'X':
        plt.savefig(PLOT_DIR + '/' + 'Doppler_X2.png',dpi=600)
    else :
        plt.savefig(PLOT_DIR + '/' + 'Doppler_S2.png',dpi=600)
    plt.close(fig7)
    """
    ############################ REFRACTIVITY ATMO

    fig20 = plt.figure(20)
    cond_ref2 = np.where(np.array(refractivity2) > -1)

    if Bande == "X":
        plt.errorbar(
            np.array(refractivity2)[cond_ref2],
            np.array(distance)[cond_ref2],
            xerr=np.array(error_refrac2)[cond_ref2],
            fmt="o",
            color="black",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="X-Band Data " + DATA,
        )

    if Bande == "S":

        plt.errorbar(
            np.array(refractivity2)[cond_ref2],
            distance[cond_ref2],
            xerr=np.array(error_refrac2)[cond_ref2],
            fmt="o",
            color="black",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="S-Band Data " + DATA,
        )

    if Bande == "Diff":

        plt.errorbar(
            np.array(refractivity2)[cond_ref2],
            distance[cond_ref2],
            xerr=np.array(error_refrac2)[cond_ref2],
            fmt="o",
            color="black",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="Differential Doppler Data " + DATA,
        )

    plt.xlabel("Refractivity", fontsize=13)
    plt.ylabel("Altitude (km)", fontsize=13)
    pylab.legend(loc="upper right")

    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)

    min_x = np.nanmin(np.array(refractivity2)[cond_ref2])
    max_x = (
        np.nanmedian(np.array(refractivity2)[cond_ref2])
        + sc.median_absolute_deviation(
            np.array(refractivity2)[cond_ref2], nan_policy="omit"
        )
        * 3
    )

    plt.xlim(min_x, max_x)
    plt.grid(True)
    plt.legend()
    fig20.set_size_inches(8, 6)  # Inch

    if Bande == "X":
        plt.savefig(PLOT_DIR + "/" + "refractivity_ATMO_X.png", dpi=600)
    if Bande == "S":
        plt.savefig(PLOT_DIR + "/" + "refractivity_ATMO_S.png", dpi=600)
    if Bande == "Diff":
        plt.savefig(PLOT_DIR + "/" + "refractivity_ATMO_Diff.png", dpi=600)

    plt.close(fig20)

    ########################## REFRACTIVITY IONO

    fig10 = plt.figure(10)
    cond_ref1 = np.where(np.array(refractivity1) > -1)
    if Bande == "X":
        plt.errorbar(
            np.array(refractivity1)[cond_ref1],
            np.array(distance)[cond_ref1],
            xerr=np.array(error_refrac1)[cond_ref1],
            fmt="o",
            color="black",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="X-Band Data " + DATA,
        )

    if Bande == "S":
        plt.errorbar(
            np.array(refractivity1)[cond_ref1],
            np.array(distance)[cond_ref1],
            xerr=np.array(error_refrac1)[cond_ref1],
            fmt="o",
            color="blue",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="S-Band Data " + DATA,
        )

    if Bande == "Diff":
        plt.errorbar(
            np.array(refractivity1)[cond_ref1],
            np.array(distance)[cond_ref1],
            xerr=np.array(error_refrac1)[cond_ref1],
            fmt="o",
            color="blue",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="Differential Doppler Data " + DATA,
        )

    plt.xlabel("Refractivity", fontsize=13)
    plt.ylabel("Altitude (km)", fontsize=13)
    pylab.legend(loc="upper right")

    min_x = np.nanmin(np.array(refractivity1)[cond_ref1])
    max_x = (
        np.nanmedian(np.array(refractivity1)[cond_ref1])
        + sc.median_absolute_deviation(
            np.array(refractivity1)[cond_ref1], nan_policy="omit"
        )
        * 3
    )

    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)

    # plt.xlim(min_x, max_x)
    #    plt.ylim(min_y,max_y)
    #    mf = matplotlib.ticker.ScalarFormatter(useOffset=False, useMathText=True)
    #    mf.set_powerlimits((-3,3))
    #    plt.gca().xaxis.set_major_formatter(mf)
    plt.grid(True)
    fig10.set_size_inches(8, 6)  # Inch
    plt.legend()

    if Bande == "X":
        plt.savefig(PLOT_DIR + "/" + "refractivity_IONO_X.png", dpi=600)
    if Bande == "S":
        plt.savefig(PLOT_DIR + "/" + "refractivity_IONO_S.png", dpi=600)
    if Bande == "Diff":
        plt.savefig(PLOT_DIR + "/" + "refractivity_IONO_Diff.png", dpi=600)

    plt.close(fig10)

    ########################Electron Density
    fig8 = plt.figure(8)

    if Bande == "X":
        plt.errorbar(
            np.array(Ne),
            distance,
            xerr=error_elec,
            fmt="o",
            color="black",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="X-Band Data " + DATA,
        )

    if Bande == "S":
        plt.errorbar(
            np.array(Ne),
            distance,
            xerr=error_elec,
            fmt="o",
            color="blue",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="S-Band Data " + DATA,
        )

    if Bande == "Diff":
        plt.errorbar(
            np.array(Ne),
            distance,
            xerr=error_elec,
            fmt="o",
            color="blue",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="Differential Data " + DATA,
        )

    plt.xlabel("Electron density (el/m$^{3}$)", fontsize=13)

    #    plt.ylim(min_y,max_y)    plt.ylabel('Altitude (km)',fontsize=13)
    pylab.legend(loc="upper right")
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)

    min_x = np.nanmedian(Ne) - sc.median_absolute_deviation(Ne, nan_policy="omit") * 3
    max_x = (
        np.nanmax(np.array(Ne)[np.array(Ne) < 1e13])
        + sc.median_absolute_deviation(
            np.array(Ne)[np.array(Ne) < 1e13], nan_policy="omit"
        )
        * 3
    )
    # plt.xlim(min_x, max_x)
    #    mf = matplotlib.ticker.ScalarFormatter(useOffset=False, useMathText=True)
    #    mf.set_powerlimits((-3,3))
    #    plt.gca().xaxis.set_major_formatter(mf)
    plt.grid(True)
    fig8.set_size_inches(8, 6)  # Inch
    plt.legend()

    if Bande == "X":
        plt.savefig(PLOT_DIR + "/" + "Ne_X.png", dpi=600)
    if Bande == "S":
        plt.savefig(PLOT_DIR + "/" + "Ne_S.png", dpi=600)
    if Bande == "Diff":
        plt.savefig(PLOT_DIR + "/" + "Ne_Diff.png", dpi=600)
    plt.close(fig8)

    fig11 = plt.figure(11)
    xmini = 10 ** 8
    xmax = max_x
    index = np.where(np.array(Ne) > xmini)

    if Bande == "X":
        plt.errorbar(
            np.array(Ne[index[0][0] : index[0][-1]]),
            distance[index[0][0] : index[0][-1]],
            xerr=error_elec[index[0][0] : index[0][-1]],
            fmt="o",
            color="black",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="X-Band Data " + DATA,
        )

    if Bande == "S":
        plt.errorbar(
            np.array(Ne[index[0][0] : index[0][-1]]),
            distance[index[0][0] : index[0][-1]],
            xerr=error_elec[index[0][0] : index[0][-1]],
            fmt="o",
            color="blue",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="S-Band Data " + DATA,
        )

    if Bande == "Diff":
        plt.errorbar(
            np.array(Ne),
            distance,
            xerr=error_elec,
            fmt="o",
            color="blue",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="Differential Doppler Data" + DATA,
        )

    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)

    plt.xlabel("Electron density (el/m$^{3}$)", fontsize=13)
    plt.ylabel("Altitude (km)", fontsize=13)
    pylab.legend(loc="upper right")

    # plt.xlim(min_x, 1.5E11)
    #    plt.ylim(min_y,max_y)
    #    mf = matplotlib.ticker.ScalarFormatter(useOffset=False, useMathText=True)
    #    mf.set_powerlimits((-3,3))
    #    plt.gca().xaxis.set_major_formatter(mf)
    plt.grid(True)
    plt.legend()
    fig11.set_size_inches(8, 6)  # Inch
    plt.xscale("log")
    plt.xlim(xmini, xmax)
    plt.legend()

    if Bande == "X":
        plt.savefig(PLOT_DIR + "/" + "Ne_X_log.png", dpi=600)
    if Bande == "S":
        plt.savefig(PLOT_DIR + "/" + "Ne_S_log.png", dpi=600)
    if Bande == "Diff":
        plt.savefig(PLOT_DIR + "/" + "Ne_Diff_log.png", dpi=600)
    plt.close(fig11)

    ########################Neutral Density
    fig9 = plt.figure(9)
    if Bande == "X":
        plt.errorbar(
            np.array(Nn),
            distance,
            xerr=error_neut,
            fmt="o",
            color="black",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="X-Band Data " + DATA,
        )  # (1+880./749.)

    if Bande == "S":
        plt.errorbar(
            np.array(Nn),
            distance,
            xerr=error_neut,
            fmt="o",
            color="blue",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="S-Band Data " + DATA,
        )  # (1+880./749.)

    if Bande == "Diff":
        plt.errorbar(
            np.array(Nn),
            distance,
            xerr=error_neut,
            fmt="o",
            color="blue",
            ecolor="lightgray",
            elinewidth=1,
            capsize=1,
            ms=1,
            label="Differential Doppler Data" + DATA,
        )  # (1+880./749.)

    plt.xlabel("Neutral number density (m$^{-3}$)", fontsize=13)
    plt.ylabel("Altitude (km)", fontsize=13)
    pylab.legend(loc="upper right")
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)

    min_x = np.nanmedian(Nn) - sc.median_absolute_deviation(Nn, nan_policy="omit") * 3
    max_x = np.nanmedian(Nn) + sc.median_absolute_deviation(Nn, nan_policy="omit") * 9

    plt.grid(True)
    plt.xlim(xmin=-1e22, xmax=3e23)
    #    plt.ylim(min_y,max_y)
    fig9.set_size_inches(8, 6)  # Inch
    plt.legend()

    if Bande == "X":
        plt.savefig(PLOT_DIR + "/" + "Neutral_X.png", dpi=600)
    if Bande == "S":
        plt.savefig(PLOT_DIR + "/" + "Neutral_S.png", dpi=600)
    if Bande == "Diff":
        plt.savefig(PLOT_DIR + "/" + "Neutral_Diff.png", dpi=600)
    plt.close(fig9)

    ########################T_low
    fig10 = plt.figure(10)
    if Bande == "X":
        plt.plot(
            np.array(T_low),
            distance,
            color="black",
            linewidth=1,
            label="X-Band Data " + DATA,
        )  
    if Bande == "S":
        plt.plot(
            np.array(T_low),
            distance,
            color="blue",
            linewidth=1,
            label="S-Band Data " + DATA,
        )  

    if Bande == "Diff":
        plt.plot(
            np.array(T_low),
            distance,
            color="blue",
            linewidth=1,
            label="Differential Doppler Data" + DATA,
        )  # (1+880./749.)

    plt.xlabel("Temperature Low (K)", fontsize=13)
    plt.ylabel("Altitude (km)", fontsize=13)
    pylab.legend(loc="upper right")
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)

    min_x = np.nanmedian(T_low) - sc.median_absolute_deviation(T_low, nan_policy="omit") * 3
    max_x = np.nanmedian(T_low) + sc.median_absolute_deviation(T_low, nan_policy="omit") * 9

    plt.grid(True)
    plt.xlim(min_x, max_x)
    #    plt.ylim(min_y,max_y)
    fig10.set_size_inches(8, 6)  # Inch
    plt.legend()

    if Bande == "X":
        plt.savefig(PLOT_DIR + "/" + "T_low_X.png", dpi=600)
    if Bande == "S":
        plt.savefig(PLOT_DIR + "/" + "T_low_S.png", dpi=600)
    if Bande == "Diff":
        plt.savefig(PLOT_DIR + "/" + "T_low_Diff.png", dpi=600)
    plt.close(fig10)

    ########################T_med
    fig11 = plt.figure(11)
    if Bande == "X":
        plt.plot(
            np.array(T_med),
            distance,
            color="black",
            linewidth=1,
            label="X-Band Data " + DATA,
        )  
    if Bande == "S":
        plt.plot(
            np.array(T_med),
            distance,
            color="blue",
            linewidth=1,
            label="S-Band Data " + DATA,
        )  

    if Bande == "Diff":
        plt.plot(
            np.array(T_med),
            distance,
            color="blue",
            linewidth=1,
            label="Differential Doppler Data" + DATA,
        )  # (1+880./749.)

    plt.xlabel("Temperature med (K)", fontsize=13)
    plt.ylabel("Altitude (km)", fontsize=13)
    pylab.legend(loc="upper right")
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)

    min_x = np.nanmedian(T_med) - sc.median_absolute_deviation(T_med, nan_policy="omit") * 3
    max_x = np.nanmedian(T_med) + sc.median_absolute_deviation(T_med, nan_policy="omit") * 9

    plt.grid(True)
    plt.xlim(min_x, max_x)
    #    plt.ylim(min_y,max_y)
    fig11.set_size_inches(8, 6)  # Inch
    plt.legend()

    if Bande == "X":
        plt.savefig(PLOT_DIR + "/" + "T_med_X.png", dpi=600)
    if Bande == "S":
        plt.savefig(PLOT_DIR + "/" + "T_med_S.png", dpi=600)
    if Bande == "Diff":
        plt.savefig(PLOT_DIR + "/" + "T_med_Diff.png", dpi=600)
    plt.close(fig11)

    ########################T_upp
    fig12 = plt.figure(12)
    if Bande == "X":
        plt.plot(
            np.array(T_upp),
            distance,
            color="black",
            linewidth=1,
            label="X-Band Data " + DATA,
        )  
    if Bande == "S":
        plt.plot(
            np.array(T_upp),
            distance,
            color="blue",
            linewidth=1,
            label="S-Band Data " + DATA,
        )  

    if Bande == "Diff":
        plt.plot(
            np.array(T_upp),
            distance,
            color="blue",
            linewidth=1,
            label="Differential Doppler Data" + DATA,
        )  # (1+880./749.)

    plt.xlabel("Temperature upper (K)", fontsize=13)
    plt.ylabel("Altitude (km)", fontsize=13)
    pylab.legend(loc="upper right")
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)

    min_x = np.nanmedian(T_upp) - sc.median_absolute_deviation(T_upp, nan_policy="omit") * 3
    max_x = np.nanmedian(T_upp) + sc.median_absolute_deviation(T_upp, nan_policy="omit") * 9

    plt.grid(True)
    plt.xlim(min_x, max_x)
    #    plt.ylim(min_y,max_y)
    fig12.set_size_inches(8, 6)  # Inch
    plt.legend()

    if Bande == "X":
        plt.savefig(PLOT_DIR + "/" + "T_upp_X.png", dpi=600)
    if Bande == "S":
        plt.savefig(PLOT_DIR + "/" + "T_upp_S.png", dpi=600)
    if Bande == "Diff":
        plt.savefig(PLOT_DIR + "/" + "T_upp_Diff.png", dpi=600)
    plt.close(fig12)

    ########################P_low
    fig13 = plt.figure(13)
    if Bande == "X":
        plt.plot(
            np.array(P_low),
            distance,
            color="black",
            linewidth=1,
            label="X-Band Data " + DATA,
        )  
    if Bande == "S":
        plt.plot(
            np.array(P_low),
            distance,
            color="blue",
            linewidth=1,
            label="S-Band Data " + DATA,
        )  

    if Bande == "Diff":
        plt.plot(
            np.array(P_low),
            distance,
            color="blue",
            linewidth=1,
            label="Differential Doppler Data" + DATA,
        )  # (1+880./749.)

    plt.xlabel("Pressure low ", fontsize=13)
    plt.ylabel("Altitude (km)", fontsize=13)
    pylab.legend(loc="upper right")
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)

    min_x = np.nanmedian(P_low) - sc.median_absolute_deviation(P_low, nan_policy="omit") * 3
    max_x = np.nanmedian(P_low) + sc.median_absolute_deviation(P_low, nan_policy="omit") * 9

    plt.grid(True)
    plt.xlim(min_x, max_x)
    #    plt.ylim(min_y,max_y)
    fig13.set_size_inches(8, 6)  # Inch
    plt.legend()

    if Bande == "X":
        plt.savefig(PLOT_DIR + "/" + "P_low_X.png", dpi=600)
    if Bande == "S":
        plt.savefig(PLOT_DIR + "/" + "P_low_S.png", dpi=600)
    if Bande == "Diff":
        plt.savefig(PLOT_DIR + "/" + "P_low_Diff.png", dpi=600)
    plt.close(fig13)

    ########################P_med
    fig14 = plt.figure(14)
    if Bande == "X":
        plt.plot(
            np.array(P_med),
            distance,
            color="black",
            linewidth=1,
            label="X-Band Data " + DATA,
        )  
    if Bande == "S":
        plt.plot(
            np.array(P_med),
            distance,
            color="blue",
            linewidth=1,
            label="S-Band Data " + DATA,
        )  

    if Bande == "Diff":
        plt.plot(
            np.array(P_med),
            distance,
            color="blue",
            linewidth=1,
            label="Differential Doppler Data" + DATA,
        )  # (1+880./749.)

    plt.xlabel("Pressure med ", fontsize=13)
    plt.ylabel("Altitude (km)", fontsize=13)
    pylab.legend(loc="upper right")
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)

    min_x = np.nanmedian(P_med) - sc.median_absolute_deviation(P_med, nan_policy="omit") * 3
    max_x = np.nanmedian(P_med) + sc.median_absolute_deviation(P_med, nan_policy="omit") * 9

    plt.grid(True)
    plt.xlim(min_x, max_x)
    #    plt.ylim(min_y,max_y)
    fig14.set_size_inches(8, 6)  # Inch
    plt.legend()

    if Bande == "X":
        plt.savefig(PLOT_DIR + "/" + "P_med_X.png", dpi=600)
    if Bande == "S":
        plt.savefig(PLOT_DIR + "/" + "P_med_S.png", dpi=600)
    if Bande == "Diff":
        plt.savefig(PLOT_DIR + "/" + "P_med_Diff.png", dpi=600)
    plt.close(fig14)

    ########################P_upp
    fig15 = plt.figure(15)
    if Bande == "X":
        plt.plot(
            np.array(P_upp),
            distance,
            color="black",
            linewidth=1,
            label="X-Band Data " + DATA,
        )  
    if Bande == "S":
        plt.plot(
            np.array(P_upp),
            distance,
            color="blue",
            linewidth=1,
            label="S-Band Data " + DATA,
        )  

    if Bande == "Diff":
        plt.plot(
            np.array(P_upp),
            distance,
            color="blue",
            linewidth=1,
            label="Differential Doppler Data" + DATA,
        )  # (1+880./749.)

    plt.xlabel("Pressure upp ", fontsize=13)
    plt.ylabel("Altitude (km)", fontsize=13)
    pylab.legend(loc="upper right")
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)

    min_x = np.nanmedian(P_upp) - sc.median_absolute_deviation(P_upp, nan_policy="omit") * 3
    max_x = np.nanmedian(P_upp) + sc.median_absolute_deviation(P_upp, nan_policy="omit") * 9

    plt.grid(True)
    plt.xlim(min_x, max_x)
    #    plt.ylim(min_y,max_y)
    fig15.set_size_inches(8, 6)  # Inch
    plt.legend()

    if Bande == "X":
        plt.savefig(PLOT_DIR + "/" + "P_upp_X.png", dpi=600)
    if Bande == "S":
        plt.savefig(PLOT_DIR + "/" + "P_upp_S.png", dpi=600)
    if Bande == "Diff":
        plt.savefig(PLOT_DIR + "/" + "P_upp_Diff.png", dpi=600)
    plt.close(fig15)

    print("\t PLOTS DONE")
    return
