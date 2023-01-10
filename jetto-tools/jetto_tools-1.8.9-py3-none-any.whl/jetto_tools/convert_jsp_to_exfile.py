# Pkg imports
try:
    from jetto_tools.binary import read_binary_file, write_binary_exfile
except:
    # this might cause issues if directly calling from python
    import sys
    sys.exit('JETTO python tools needs to be loaded for this program to work')

# Std imports
import copy
from datetime import datetime
import os
import json
import argparse
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

def plot_profiles(exfile_orig,jsp,key):

    plt.figure(1)
    plt.plot(exfile_orig, '-r', label='jsp')
    plt.ylabel(key)
    plt.plot(jsp, '-k', label='exfile')
    plt.legend()
    plt.title('Please close figure when finished to contine with plotting')
    plt.show()
def parse_opt(parents=[]):
    parser = argparse.ArgumentParser(parents=parents, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # labels for plots


    # REQUIRED ARGS
    # Name of exfile to be used.
    parser.add_argument("-n", "--name_exfile", dest="new_exfile_name",
                         action="store", default=None,
                         help="Name of EXFILE to be written out to", required=True)


    ####################################################################################################################
    # OPTIONAL ARGS

    # Time to be used. Optional else uses the end time
    parser.add_argument("-t", "--time", dest="time",
                        action="store_true", default=None,
                        help="Choose time from JSP to use profiles to make EXFILE")

    # Path to exfile to file written out OPTIONAL
    user = os.environ.get('USER')
    exfile_output_path = '/home/'+user+'/cmg/jams/data/exfile/'
    parser.add_argument("-ex_new", "--ex_path_new", dest="exfile_path",
                        action="store", default=exfile_output_path,
                        help="Optional path to ouptput the EXFILE")

    # Path to template exfile to be used optional
    default_exfile_temp_path = None
    parser.add_argument("-ex", "--ex_path", dest="orig_exfile_path",
                         action="store", default=default_exfile_temp_path,
                         help="Provide FULL path to EXFILE to be used a template for new exfile. Default"
                              "is using the EXFILE template from JETTO binary tools. Advise to use EXFILE "
                              "from JETTO run which the JSP has been made from")

    # JSP path to be used. Defaults to looking in the current directory
    parser.add_argument("-jsp", "--jsp", dest="jsp_path",
                        action="store", default=None,
                        help="Path to the jsp to make EXFILE from")

    # JSP path to be used. Defaults to looking in the current directory
    parser.add_argument("-p", "--plot", dest="plot_debug",
                        action="store_true", default=False,
                        help="Plot the JSP profiles versus the template EXFILE to check the profiles are as expected")

    opts = parser.parse_args()

    return opts


def format_jsp_profiles(jsp):
    temp = (jsp).tolist()
    temp1 = [temp]
    return  np.array(temp1)

def check_xaxis(jsp,jsp_key,key):
    """
    check that the x vector for the profile is XVEC1 and nothing else. Returns  boolean for checking
    :param jsp: jsp dictionary
    :param jsp_key: signal for the jsp
    :param key: signal for the exfile
    :return: Boolean
    """
    if key == 'XVEC1':
        # this doesn't need to be checked. Special case.
        return True

    if jsp['INFO'][jsp_key]['XBASE'] != 'XVEC1':
        print('The JSP signal {key} is on the wrong X axis - {xbasis} cannot be used the signal'
              '{ex_signal} is being removed the EXFILE. The EXFILE can only contain profiles on XVEC1 axis'
              .format(key=jsp_key, xbasis=jsp['INFO'][jsp_key]['XBASE'], ex_signal=key))

        return False
    else:
        return True

def jsp2exp_write(jsp_path,exfile_orig_path,time,exfile_path, new_exfile_name,
                  plot_debug,verbosity=2):
    """
        Desc - reads a template EXFILE, over writes the physics signals from the JSP with it and keep the INFO sections
           then writes that new EXFILE structure out


    Note some of these params are filled by argparse and have default values set in parse_opt

    :param jsp_path: path to JSP file to be used
    :param orig_exfile_path: path to template JSP
    :param time: time which the profiles should be read from the JSP
    :param exfile_path: path to output the new exfile to
    :param new_exfile_name: name of the new exfile to be written
    :param plot_debug: debug output which allows plotting of the matched JSP signal on top the template EXFILE signals

    :return: status - return from write_binary_exfile 0 - written other - failed
    """

    # Check if new EXFILE already exists
    output_exfile_name = exfile_path + '/' + new_exfile_name
    if os.path.isfile(output_exfile_name):
        import sys
        sys.exit('EXFILE to be written to already exist - {path}'.format(path=output_exfile_name))

    exfile_data = jsp2exp(jsp_path, exfile_orig_path, time, plot_debug, verbosity=verbosity)

    status = write_binary_exfile(exfile_data,output_file=output_exfile_name)
    return status

def jsp2exp(jsp_dir, exfile_orig_path, time, plot_debug, verbosity=2):
    """
    Desc - reads a template EXFILE, over writes the physics signals from the JSP with it and keep the INFO sections

    :param jsp_path: path to JSP file to be used assume the file name is jetto,jsp
    :param orig_exfile_path: path to template JSP assume the file name is jetto.ex
    :param time: time which the profiles should be read from the JSP
    :param plot_debug: debug output which allows plotting of the matched JSP signal on top the template EXFILE signals
    :return: exfile_data - dictionary which contains the EXFILE data
    """



    # the JSP file read should throw an error is it doesn't exist
    jsp_path = Path(jsp_dir) / 'jetto.jsp'
    jsp = read_binary_file(jsp_path)


    # Read the exfile
    exfile_orig_path = Path(exfile_orig_path) / 'jetto.ex'
    exfile_orig = read_binary_file(exfile_orig_path)
    exfile_data = copy.deepcopy(exfile_orig)


    # Provides the mapping between EXFILE and JSP signals
    json_config_file = Path(__file__).resolve().parent / "convert_jsp_to_exfile_config.json"
    with open(json_config_file, 'r') as read_file:
        config = json.load(read_file)


    # establish first the database information section of the exfile, and keep those.
    # only the signals profiles need to be kept from the JSP
    exfile_config = config["exfile_data"]
    databsae_info_keys = exfile_config["DB_data"]

    if time is not None:
        user_time = time
        # TODO possibly change this to use built xarray nearest
        idx_time = np.abs(jsp['TIME']-user_time)
    else:
        # use end time
        idx_time = -1

    exfile_data['TVEC1'] = jsp['TIME'][idx_time]



    # Print out what has been added to the new EXFILE and units
    no_columns=5
    columns = ["EXFILE VAR", "JSP VAR", "Description from EXFILE","Description from JSP", "Units for EXFILE", "Units from JSP"]
    row_format = '{:<15}{:<10}{:<40}{:<40}{:<20}{:<20}'
    if verbosity >= 1:
        print("PROFILE WRITTEN TO NEW EXFILE FROM SPECIFIED JSP")
        print(row_format.format(*['='*15,'='*10,'='*40,'='*40,'='*20,'='*20]))
        print(row_format.format(*columns))
        print(row_format.format(*['='*15,'='*10,'='*40,'='*40,'='*20,'='*20]))

    for key in exfile_orig.keys():

        if key in databsae_info_keys:
            # the data is already in the datastrcutre and doesn't replacing (see the end for some exceptions)
            # this only relates the info section and not any physics signals
            continue
        # the names in the physics variables don't always match between exfile and JSP
        elif key == 'TVEC1':
            # this was sorted above
            continue

        # USE MAPPING IN JSON FILE
        elif key in exfile_config['exfile_keys'].keys():
            # JSON format doesn't allow keyword None, hence:
            if exfile_config['exfile_keys'][key]['jsp_key'] == "None":
                if verbosity >= 2:
                    print("Key = {key} is not available in the JSP. It will be removed".format(key=key))
                del exfile_data[key]
                continue



            try:
                # Set mapping
                jsp_key = exfile_config['exfile_keys'][key]['jsp_key']
                jsp_data = jsp[jsp_key][idx_time]
                exfile_data[key] = format_jsp_profiles(jsp_data)
                # checks wheter the profile in question from the JSP uses XVEC1 as the xaxis is not skip profile as not
                # compabile with the EXFILE
                if check_xaxis(jsp, jsp_key, key) == False:
                    del exfile_data[key]
                    continue
                if verbosity >= 1:
                    print(row_format.format(key, jsp_key, str(exfile_orig['INFO'][key]['DESC']),
                                            str(jsp['INFO'][jsp_key]['DESC']), str(exfile_orig['INFO'][key]['UNITS']),
                                            str(jsp['INFO'][jsp_key]['UNITS'])))

                if plot_debug == True:
                    plot_profiles(exfile_orig[key][-1], jsp[jsp_key][idx_time], key)

            except KeyError:
                # The JSON file contained a signal which is not in the JSP
                print('\n Signal from EXFILE = {exfile} is not present '
                      'in the JSP (signal from JSP {jsp}).'
                      'Note this signal was in the orginal EXFILE!!!! and will now be removed'
                      '\n'.format(exfile=key,jsp=jsp_key))
                # remove entry from dictionary
                del exfile_data[key]
                continue


        else:
            # JSP KEY annd EXFILE key are the same
            try:
                jsp_key = key

                # checks wheter the profile in question from the JSP uses XVEC1 as the xaxis is not skip profile as not
                # compabile with the EXFILE
                if check_xaxis(jsp, jsp_key, key) == False:
                    del exfile_data[key]
                    continue

                exfile_data[key] = format_jsp_profiles(jsp[jsp_key][idx_time])
                if verbosity >= 1:
                    print(row_format.format(key, jsp_key, str(exfile_data['INFO'][key]['DESC']),
                                            str(jsp['INFO'][jsp_key]['DESC']), str(exfile_data['INFO'][key]['UNITS']),
                                            str(jsp['INFO'][jsp_key]['UNITS'])))
                # TODO add copy the same profile into the EXFILE from new EXFILE if the user wants it
                if plot_debug == True:
                    plot_profiles(exfile_orig[key][-1],jsp[jsp_key][idx_time],key)

            except KeyError:
                print('****** Variable - {key} NOT FOUND in the JSP. '
                      'PLEASE set up JSON FILE to map correctly between this key. '
                      'Note this signal was in the orginal EXFILE!!!! and will now be removed ******'.format(key=key))

                # remove entry from dictionary
                del exfile_data[key]

    # Update the creation date and time
    today = datetime.today()
    exfile_data['CREATION_DATE'] = today.strftime("%d/%m/%Y")
    exfile_data['CREATION_TIME'] = today.strftime("%H:%M:%S")
    DB_name_string = 'JSP2EX'
    exfile_data['DATABASE NAME'] = DB_name_string

    return exfile_data


def main():


    # Get command line options
    opts = parse_opt()
    if opts.jsp_path == None:
        opts.jsp_path = './' # jetto.jsp appended later on

    # Build JSP path depending on command line
    if opts.orig_exfile_path is None:
        exfile_orig_path = opts.jsp_path
    else:
        exfile_orig_path = opts.orig_exfile_path

    exfile_write_status = jsp2exp_write(opts.jsp_path,exfile_orig_path,opts.time,opts.exfile_path,
                                        opts.new_exfile_name,opts.plot_debug)


if __name__ == '__main__':
    main()

