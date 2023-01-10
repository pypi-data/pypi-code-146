# """
#
#     This code reads in a given Flow360 BET input JSON file and plots the 2D Cl and CD polars along with the twist and chord
#     distribution in that file.
#
#     The goal is to make sure that the polars and geometry information being given to the Flow360 solver is as expected.
#
#     Returns
#     -------
#     None: saves plots of the 2D polars
# """
#
#
# import json
# import matplotlib.pyplot as plt
# import argparse
# import os
#
# figSize = [16, 8]
# ticks = ['x-', '+--', 'p:', '^-', '>--', '<-', '*:', '-', '1-', '2--','3--','4:']
#
# ################################################################################################################
# def plotClCd(jsonDict,saveBool):
#     """
#     Take a valid Flow360 BET disk JSON dictionary and plot the 2D polar values for the various stations.
#
#     Returns
#     -------
#     saves plots of the 2D polars in png
#     """
#     nDisks = len(jsonDict['BETDisks'])
#     for diskNum in range((nDisks)):
#         nStations = len(jsonDict['BETDisks'][diskNum]['sectionalRadiuses'])
#         alphas = jsonDict['BETDisks'][diskNum]['alphas']
#         nMachs = len(jsonDict['BETDisks'][diskNum]['MachNumbers'])
#         #plt.figure(figsize=(32, 16))
#           # needed to differentiate the various sections in the final plot.
#         for stationIdx in range(nStations):
#             plt.figure(figsize=(figSize[0], figSize[1]))
#             for machIdx in range(nMachs):
#                 plt.subplot(1, 2, 1)
#                 plt.plot(jsonDict['BETDisks'][diskNum]['sectionalPolars'][stationIdx]['dragCoeffs'][machIdx][0],
#                          jsonDict['BETDisks'][diskNum]['sectionalPolars'][stationIdx]['liftCoeffs'][machIdx][0], ticks[stationIdx],
#                          label='Mach#:%.2f' % (jsonDict['BETDisks'][diskNum]['MachNumbers'][machIdx]))
#                 plt.subplot(1, 2, 2)
#                 plt.plot(alphas, jsonDict['BETDisks'][diskNum]['sectionalPolars'][stationIdx]['liftCoeffs'][machIdx][0],
#                          ticks[stationIdx], label=' Mach#:%.2f' % (jsonDict['BETDisks'][diskNum]['MachNumbers'][machIdx]))
#
#             plt.subplot(1, 2, 1)
#             plt.xlim(0, 0.07)
#             plt.ylim(-1, 3)
#             plt.xlabel('Cd')
#             plt.ylabel('Cl')
#             plt.grid('on')
#             plt.legend()
#             plt.title('CL vs Cd')
#             plt.subplot(1, 2, 2)
#             plt.xlim(-10, 20)
#             plt.ylim(-1, 3)
#             plt.xlabel('Alpha')
#             plt.ylabel('Cl')
#             plt.grid('on')
#             plt.legend()
#             plt.title('Cl vs Alpha')
#             if saveBool:
#                 plt.savefig('disk%i_CL_CD_comparetoXrotor_station%i.png' % (diskNum, stationIdx))
#             plt.close()
#
#         # Now we plot the CL v alpha and CD vs alpha at larger alphas
#         for stationIdx in range(nStations):
#             plt.figure(figsize=(figSize[0], figSize[1]))
#             for machIdx in range(nMachs):
#                 plt.subplot(1, 2, 1)
#                 plt.plot(alphas, jsonDict['BETDisks'][diskNum]['sectionalPolars'][stationIdx]['liftCoeffs'][machIdx][0], ticks[stationIdx],
#                          label='CL Mach#:%.2f' % (jsonDict['BETDisks'][diskNum]['MachNumbers'][machIdx]))
#                 plt.subplot(1, 2, 2)
#                 plt.plot(alphas, jsonDict['BETDisks'][diskNum]['sectionalPolars'][stationIdx]['dragCoeffs'][machIdx][0], ticks[stationIdx],
#                          label='Cd Mach#:%.2f' % (jsonDict['BETDisks'][diskNum]['MachNumbers'][machIdx]))
#
#
#             plt.subplot(1, 2, 1)
#             plt.xlabel('alpha')
#             plt.ylabel('Cl')
#             plt.grid('on')
#             plt.legend()
#             plt.title('CL vs Alpha')
#             plt.subplot(1, 2, 2)
#             plt.xlabel('Alpha')
#             plt.ylabel('Cd')
#             plt.grid('on')
#             plt.legend()
#             plt.title('Cd vs Alpha')
#             if saveBool:
#                 plt.savefig('disk%i_CL_CDvAlpha_station%i.png' % (diskNum, stationIdx))
#             plt.subplot(1, 2, 1)
#             plt.xlim(-45, 45)
#             plt.subplot(1, 2, 2)
#             plt.xlim(-45, 45)
#             if saveBool:
#                 plt.savefig('disk%i_CL_CDvAlphaZoomed_station%i.png' % (diskNum, stationIdx))
#             plt.subplot(1, 2, 1)
#             plt.xlim(-20, 20)
#             plt.subplot(1, 2, 2)
#             plt.xlim(-20, 20)
#             if saveBool:
#                 plt.savefig('disk%i_CL_CDvAlphaZoomed2_station%i.png' % (diskNum, stationIdx))
#             plt.close()
#
#
# ################################################################################################################
# def plotTwistChord(jsonDict,saveBool):
#     """
#     Take a valid Flow360 BET disk JSON dictionary and plot the twist and chord of the propeller vs radius for the
#     various stations.
#
#     Returns
#     -------
#     saves png plots of the blade geometry (twist and chord)
#
#     """
#     nDisks = len(jsonDict['BETDisks'])
#     plt.figure(figsize=(32, 16))
#     for diskNum in range((nDisks)):
#         twists=[]
#         radius=[]
#         twistList=jsonDict['BETDisks'][diskNum]['twists']
#         for i in range(len(twistList)):
#             twists.append(twistList[i]['twist'])
#             radius.append(twistList[i]['radius'])
#         plt.plot(radius,twists,label='Disk %i'%diskNum)
#     plt.xlabel('radius')
#     plt.ylabel('Twist')
#     plt.grid('on')
#     plt.legend()
#     plt.title('Twist vs Propeller Radius')
#     if saveBool:
#         plt.savefig('TwistVRadius.png')
#     plt.close()
#
#     # now we plot the chords vs radius
#     plt.figure(figsize=(32, 16))
#     for diskNum in range((nDisks)):
#         chords=[]
#         radius=[]
#         chordList=jsonDict['BETDisks'][diskNum]['chords']
#         for i in range(len(chordList)):
#             chords.append(chordList[i]['chord'])
#             radius.append(chordList[i]['radius'])
#         plt.plot(radius,chords,label='Disk %i'%diskNum)
#     plt.xlabel('radius')
#     plt.ylabel('chords')
#     plt.grid('on')
#     plt.legend()
#     plt.title('Chord vs Propeller Radius')
#     if saveBool:
#         plt.savefig('ChordVRadius.png')
#     plt.close()
# ################################################################################################################
# def main():
#     """
#
#     Returns
#     -------
#     saves plots of the 2D polars along with the twist and chord distributions of the blades being simulated with the flow360-BETDisk
#     """
#     parser = argparse.ArgumentParser(description="PLotting script for the BET 2D polar information contained within a Flow360.json File.")
#     parser.add_argument('-i', '--input',
#                         type     = str,
#                         required = False,
#                         help     = 'input Flow360.json file with a BETdisk field we want to validate')
#     parser.add_argument('-s','--savePNG',
#                         type = bool,
#                         required = False,
#                         default = True,
#                         help='Boolean whether to save the PNG plots of the 2D polars or not')
#     args = parser.parse_args()
#
#     # load in the files
#     if args.input is not None:  # assume we passed it the json file names
#         JsonFile = args.input
#     else:  # assume we need to enter the Flow360 file name
#         JsonFile = input('Please enter the path of the Flow360 json input file you would like to use:')
#         saveBool = True
#
#     if not os.path.isfile(JsonFile):
#         print('flow360 json input file %s does not exist.' % JsonFile)
#         print('EXITING')
#         raise NameError('flow360 json input file %s does not exist.' % JsonFile)
#
#     with open(JsonFile) as fh:
#         jsonDict = json.load(fh)
#
#
#     plotClCd(jsonDict, saveBool)
#     plotTwistChord(jsonDict, saveBool)
#
#
# ################################################################################################################
# if __name__ == '__main__':
#     main()
