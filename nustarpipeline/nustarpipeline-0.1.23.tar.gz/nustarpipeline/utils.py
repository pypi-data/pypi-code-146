import logging
from numpy import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil

# file_handler = logging.FileHandler(filename='nustar_utils_%s.log' % (strftime("%Y-%m-%dT%H:%M:%S", gmtime())))
# stdout_handler = logging.StreamHandler(sys.stdout)
# handlers = [stdout_handler, file_handler]
#
# logging.basicConfig(level=logging.DEBUG, format=' %(levelname)s - %(message)s', handlers=handlers)
#[%(asctime)s] {%(filename)s:%(lineno)d}
logger = logging.getLogger('')

from subprocess import Popen, PIPE, STDOUT

def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        logging.info(line.decode()[0:-1])

#shell_cmd = os.environ['HOME'] + '/Soft/timingsuite/dist/Debug/GNU-MacOSX/timingsuite <timing_cmd.txt'
shell_cmd = 'timingsuite <timing_cmd.txt'


def run(cmd=shell_cmd):
    logger.info("------------------------------------------------------------------------------------------------\n")
    logger.info("**** running %s ****\n" % cmd)
    #out=subprocess.call(cmd, stdout=logger, stderr=logger, shell=True)
    process = Popen('export DYLD_LIBRARY_PATH=$HEADAS/lib;'+cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    with process.stdout:
        log_subprocess_output(process.stdout)
    out = process.wait()  # 0 means success

    logger.info("------------------------------------------------------------------------------------------------\n")

    logger.info("Command '%s' finished with exit value %d" % (cmd, out))

    return out

def get_obsids(src):
    from astroquery.heasarc import Heasarc
    from astropy.io import ascii
    heasarc = Heasarc()
    payload = heasarc._args_to_payload(mission='numaster', entry=src, radius='10 arcmin')
    table = heasarc.query_async(payload)

    table_body = table.content.decode().split('END')[-1].strip().split('\n')
    table_body_clean = [cc for cc in table_body if 'SCIENCE' in cc and 'archived' in cc]
    logger.info("************************************")
    logger.info(src)
    logger.info("************************************")
    logger.info(table_body_clean)
    logger.info("************************************")

    try:
        data = ascii.read(table_body_clean, format='fixed_width_no_header', delimiter=' ')
        logger.info(data['col5'])
        output = [str(x) for x in data['col5'].data]
    except:
        logger.warning('No OBSIDS')
        output =[]

    return output

def make_basic_fit():
    ff = open('files-auto.xcm', 'w')
    ff.write('stati cstat\n')
    ff.write('data 1:1 FPMA_sr_rbn.pi\n')
    ff.write('data 2:2 FPMB_sr_rbn.pi\n')
    ff.write('ignore bad\n')
    ff.write('ignore *:**-3.0,70.0-**\n')
    ff.write('abun wilm\nmodel tbabs*high*peg')
    ff.write('\n\n\n\n\n3\n70\n1\n\n\n\n\n3\n70\n1,.1\n\n')
    ff.write('query yes\n')
    ff.write('freeze 2,3\nfit\n\n')
    ff.write('tha 2,3\nfit\n\n')
    ff.write('rm -f mod_base.xcm\nsave mod mod_base.xcm\n')
    ff.write('setpl ene\ncpd basic-plot.gif/GIF\nplot ld del\n')
    ff.write('quit\n\n')
    ff.close()

    ff = open('files-iterative.xcm', 'w')
    ff.write('stati cstat\n')
    ff.write('data 1:1 FPMA_sr_rbn.pi\n')
    ff.write('data 2:2 FPMB_sr_rbn.pi\n')
    ff.write('ignore bad\n')
    ff.write('ignore *:**-3.0,70.0-**\n')
    ff.write('@mod_base.xcm\n')
    ff.write('query yes\n')
    ff.write('setpl ene\ncpd /XW\npl ld del\n')
    ff.close()

    #logger.debug(xspec_commands)
    status = run('xspec - files-auto.xcm')
    from IPython.display import Image
    from IPython.display import display
    _ = display(Image(filename='basic-plot.gif_2', format="gif"))
    return status

def plot_periodogram():
    with open('ef_pipe_periodogram_f.qdp') as ff:
        qdp_lines = ff.readlines()
    with open('tmp.qdp', 'w') as ff:
        ff.write(qdp_lines[0])
        ff.write('cpd tmp.gif/GIF\n')
        ff.write('scr white\n')
        ff.write('ma 17 on\n')
        ff.write('time off\n')
        ff.write('lab f\n')
        for ll in qdp_lines[2:]:

            ff.write(ll)
        ff.write('\n')


    run("qdp tmp.qdp")
    from IPython.display import Image
    from IPython.display import display
    _ = display(Image(filename='tmp.gif', format="gif"))


efold_cmd='''14
1
list_evt.txt
%f
%f
ef_pipe
n
%d

%f
%f
1
0
'''

efold_orbit_cmd='''14
1
list_evt.txt
%f
%f
ef_pipe
y
%s
%d

%f
%f
1
0
'''

def get_efold_frequency(nu_min, nu_max, min_en=3., max_en=20., n_bins=32, unit='A',orbitfile=None,
                        actual_search=True):

    if actual_search:
        with open('list_evt.txt', 'w') as ff:
            ff.write('source%s.evt' % unit)

        with open('timing_cmd.txt', 'w') as ff:
            if orbitfile is None:
                ff.write(efold_cmd % (min_en, max_en, n_bins, nu_min, nu_max))
            else:
                if not os.path.isfile(orbitfile):
                    raise FileExistsError('File %s does not exist' % orbitfile)

                ff.write(efold_orbit_cmd % (min_en, max_en, orbitfile, n_bins, nu_min, nu_max))

        run()

    plot_periodogram()

    x = np.loadtxt('ef_pipe_res.dat', dtype=np.double)

    return x[2]

def get_nu_search_limits(filename, freq_search_interval=0.2, plot_filename=None, nyquist_factor=1, min_frequency=1e-4, max_frequency=10.):
    """It uses the Lomb-Scargle periodogram to find a range of spin frequencies to explore
        to find a reliable periodicity

    Args:
        filename (_type_): name of the light curve in fits format to load
        freq_search_interval (float, optional): it will provide a search interval from (1-/+freq_search_interval) of the peak. Defaults to 0.2.
        plot_filename (str, optional): the name of output plot file. Defaults to None to avoid plotting.
        nyquist_factor (int, optional): Lomb Scargle nymquist factor, see https://docs.astropy.org/en/stable/timeseries/lombscargle.html. Defaults to 1.
        min_frequency (float, optional): it will search peaks only above this frequency (to avoid red-noise). Defaults to 1e-4
        max_frequency (float, optional): it will search peaks only below this frequency (to avoid red-noise). Defaults to 10

    Returns:
        nu_start, nu_stop: minimum and maximum frequencies to search
    """    

    import hratio
    lc_unbinned = hratio.light_curve()
    lc_unbinned.read_from_fits(filename=filename)
    from astropy.timeseries import LombScargle
    max_freq = 0.5/lc_unbinned._timedel_
    min_freq = max(1e-4,1./(lc_unbinned._tstop_ - lc_unbinned._tstart_ ))
    #frequencies = np.arange(min_freq, max_freq, min_freq)
    #power = LombScargle(lc_unbinned._times_, lc_unbinned._rates_).power(frequencies)
    frequencies, power = LombScargle(lc_unbinned._times_, lc_unbinned._rates_).autopower(nyquist_factor=nyquist_factor)
    
    mask = (frequencies >= min_frequency) & (frequencies <= max_frequency)
    max_freq = frequencies[mask][np.argmax(power[mask])]
    nu_start = max_freq * (1.-freq_search_interval)
    nu_stop = max_freq * (1.+freq_search_interval)
    logger.info("We suggest to explore from %f to %f Hz" %(nu_start, nu_stop))
    
    if plot_filename is not None:
        plt.figure()
        plt.loglog(frequencies, power) 
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Power (Lomb-Scargle)')
        plt.axvspan(nu_start, nu_stop, alpha=0.5, color='cyan')
        plt.savefig(plot_filename)

    return nu_start, nu_stop
    

    
    




enphase_cmd='''17
list_evt.txt
none
%s
n
%d
%19.12e
%19.12e
%19.12e
0
n
%f
%f
%f
0
0
0
1000000000
'''

enphase_cmd_binfile='''17
list_evt.txt
none
%s
n
%d
%19.12e
%19.12e
%19.12e
0
y
%s
0
0
0
0
1000000000
'''

enphase_cmd_orbit='''17
list_evt.txt
none
%s
y
%s
%d
%19.12e
%19.12e
%19.12e
0
n
%f
%f
%f
0
0
0
1000000000
'''

enphase_cmd_orbit_binfile='''17
list_evt.txt
none
%s
y
%s
%d
%19.12e
%19.12e
%19.12e
0
y
%s
0
0
0
0
1000000000
'''




def make_enphase(freq,  min_en=3., max_en=70., en_step=0.5, n_bins=32, orbitfile=None, nudot=0, t_ref=0):
    
    '''
    Wrapper on timingsuite to produce Energy - Phase matrixes for source and background for both FPM units.
    :param freq: spin frequency
    :param min_en: minimum energy (=3 keV
    :param max_en: mximum energy (=70 keV)
    :param en_step: energy step (=0.5 keV)
    :param n_bins: number of phase bins (=32)
    :param orbitfile: orbitfile for orbital correction (timingsuite) if None
    :param nudot: spinn requency derivative (=0)
    :param t_ref: reference time for folding (if <= 0, it takes the first time)
    :return: it writes the fits files sourceA_ENPHASE.fits sourceB_ENPHASE.fits
                        backgroundA_ENPHASE.fits backgroundB_ENPHASE.fits
    '''

    for tt in ['source', 'background']:
        for unit in ['A', 'B']:
            with open('list_evt.txt', 'w') as ff:
                ff.write('%s%s.evt' % (tt, unit))

            if orbitfile is None:
                with open('timing_cmd.txt', 'w') as ff:
                    if type(en_step) == float:
                        ff.write(enphase_cmd % ('%s%s_ENPHASE.fits' % (tt, unit),
                                         n_bins, t_ref, freq, nudot, en_step, min_en, max_en) )
                    else:
                        if not os.path.isfile(en_step):
                            raise FileExistsError('File %s does not exist' % en_step)
                        ff.write(enphase_cmd_binfile % ('%s%s_ENPHASE.fits' % (tt, unit),
                                                n_bins, t_ref, freq, nudot, en_step))
            else:
                if not os.path.isfile(orbitfile):
                    raise FileExistsError('File %s does not exist' % orbitfile)

                with open('timing_cmd.txt', 'w') as ff:
                    if type(en_step) == float:
                        ff.write(enphase_cmd_orbit % ('%s%s_ENPHASE.fits' % (tt, unit), orbitfile,
                                     n_bins, t_ref, freq, nudot, en_step, min_en, max_en) )
                    else:
                        if not os.path.isfile(en_step):
                            raise FileExistsError('File %s does not exist' % en_step)
                        ff.write(enphase_cmd_orbit_binfile % ('%s%s_ENPHASE.fits' % (tt, unit), 
                        orbitfile, n_bins, t_ref, freq, nudot, en_step))
            
            run()
            shutil.copy('%s%s_ENPHASE.fits' % (tt, unit), '%s%s_ENPHASE_%03d.fits' % (tt, unit, n_bins))

            

def pad_matrices_with_zeros(x1_min, x1_max, pp1, dpp1, x2_min, x2_max, pp2, dpp2, tolerance=1e-2):
    '''
    :param x1_min:
    :param x1_max:
    :param pp1:
    :param dpp1:
    :param x2_min:
    :param x2_max:
    :param pp2:
    :param dpp2:
    :param tolerance:
    :return:
    '''
    if len(x1_min) == len(x2_min):
        diff = np.sum(x1_min - x2_min)
        if np.abs(diff) > tolerance:
            logger.warning("vector lower edges have same size but likely different values")
        return x1_min, x1_max, pp1, dpp1, x2_min, x2_max, pp2, dpp2

    if len(x1_min) < len(x2_min):
        new_x1_min, new_x1_max, new_pp1, new_dpp1 = pad_matrix_with_zeros(x1_min, x1_max, pp1, dpp1, x2_min, x2_max)
        return new_x1_min, new_x1_max, new_pp1, new_dpp1, x2_min, x2_max, pp2, dpp2

    if len(x1_min) > len(x2_min):
        new_x2_min, new_x2_max, new_pp2, new_dpp2 = pad_matrix_with_zeros(x2_min, x2_max, pp2, dpp2, x1_min, x1_max)
        return x1_min, x1_max, pp1, dpp1, new_x2_min, new_x2_max, new_pp2, new_dpp2



def pad_matrix_with_zeros(x1_min, x1_max, pp1, dpp1, x2_min, x2_max):
    '''
    returns matrix padded with zeros to fill the gaps
    :param x1_min:
    :param x1_max:
    :param pp1:
    :param dpp1:
    :param x2_min:
    :param x2_max:
    :return:
    '''

    new_x1_min = []
    new_x1_max = []
    new_pp1 = []
    new_dpp1 = []
    n_bins = pp1.shape[1]
    for y, z in zip(x2_min, x2_max):
        found = False
        for i in range(len(x1_min)):
            if x1_min[i] == y:
                new_x1_min.append(x1_min[i])
                new_x1_max.append(x1_max[i])
                new_pp1.append(pp1[i, :])
                new_dpp1.append(dpp1[i, :])
                found = True

        if not found:
            new_x1_min.append(y)
            new_x1_max.append(z)
            new_pp1.append(np.zeros(n_bins))
            new_dpp1.append(np.zeros(n_bins))

    if len(x2_min) != len(new_x1_min):
        raise RuntimeError('Padding matrix with zeros gave wrong sizes !!')

    return np.array(new_x1_min), np.array(new_x1_max), np.array(new_pp1), np.array(new_dpp1)


def read_one_matrix(kind, unit, background_difference_limit=5):
    '''

    :param kind: 'E' for Energy-Phase, 'T' for Time-Phase
    :param unit: 'A' or 'B' for FPM unit
    :param background_difference_limit:
            =0 does not subtract the background
            <0 subtracts the background after padding background matrix with zeros
            >0  if sizes of source and background matrices differs by more than this value, it will skip subtraction
    :return: x_min lower edge of time or energy bins
             x_min upper edge of time or energy bins,
             pp matrix
             dpp matrix of uncertainties
    '''
    import astropy.io.fits as pf

    if not (unit == 'A' or unit == 'B'):
        raise UserWarning('The unit must be A or B, you have %s ' % unit)

    if kind == 'E':
        fname_src = 'source%s_ENPHASE.fits' % unit
        fname_bck = 'background%s_ENPHASE.fits' % unit
        key1 = 'E_MIN'
        key2 = 'E_MAX'
    elif kind == 'T':
        key1 = 'T_START'
        key2 = 'T_STOP'
        fname_src = 'source%s_TPHASE.fits' % unit
        fname_bck = 'background%s_TPHASE.fits' % unit
    else:
        raise UserWarning('The kind of matrix can be E or T, you gave %s' % kind)

    ff = pf.open(fname_src, 'readonly')
    t_minA = ff[1].data[key1]
    t_maxA = ff[1].data[key2]
    ptA = ff[1].data['MATRIX']
    dptA = ff[1].data['ERROR']
    ff.close()

    ff = pf.open(fname_bck, 'readonly')
    t_minAb = ff[1].data[key1]
    t_maxAb = ff[1].data[key2]
    ptbA = ff[1].data['MATRIX']
    dptbA = ff[1].data['ERROR']
    ff.close()

    if background_difference_limit < 0:
        t_minA, t_maxA, ptA, dptA, t_minAb, t_maxAb, ptbA, dptbA = \
            pad_matrices_with_zeros(t_minA, t_maxA, ptA, dptA, t_minAb, t_maxAb, ptbA, dptbA)
        ptA -= ptbA
        dptA = np.sqrt(dptbA ** 2 + dptA ** 2)
        logger.info('Subtracted the background, possibly padded with zeros')
    elif background_difference_limit > 0:
        if np.abs(len(t_minA) - len(t_minAb)) < background_difference_limit:
            indA, indAb = get_ind_combine(t_minA, t_minAb)
            t_minA = t_minA[indA]
            t_maxA = t_maxA[indA]

            ptA = ptA[indA, :] - ptbA[indAb, :]
            dptA = np.sqrt(dptA[indA, :] ** 2 + dptbA[indAb, :] ** 2)
            logger.info('Subtracted the background')
        else:
            logger.info('We do not subtract the background because the difference in matrix dimension is %d' %
                        np.abs(len(t_minA) - len(t_minAb)))
    else:
        logger.info("Not subtracting the background")

    return t_minA, t_maxA, ptA, dptA

def read_and_sum_matrixes(kind, background_difference_limit=5):
    '''

    :param kind: 'E' for ENERGY-Phase, 'T'  for 'TIME-Phase
    :param background_difference_limit:
    :return:
    '''
    t_minA, t_maxA, ptA, dptA = read_one_matrix(kind, 'A', background_difference_limit=background_difference_limit)
    t_minB, t_maxB, ptB, dptB = read_one_matrix(kind, 'B', background_difference_limit=background_difference_limit)

    if background_difference_limit > 0 :
        indA, indB = get_ind_combine(t_minA, t_minB)
        t_min = t_minA[indA]
        t_max = t_maxA[indA]
        pp = ptA[indA, :] + ptB[indB, :]
        dpp = np.sqrt(dptA[indA, :] ** 2 + dptB[indB, :] ** 2)
    else:
        t_min, t_max, ptA, dptA, t_minB, t_maxB, ptB, dptB = \
            pad_matrices_with_zeros(t_minA, t_maxA, ptA, dptA, t_minB, t_maxB, ptB, dptB)

        pp = ptA + ptB
        dpp = np.sqrt(dptA ** 2 + dptB ** 2)

    logger.info('Matrix for unit A has size %d x %d ' % (ptA.shape[0], ptA.shape[1]))
    logger.info('Matrix for unit B has size %d x %d ' % (ptB.shape[0], ptB.shape[1]))
    logger.info('The combined matrix has size %d x %d' % (pp.shape[0], pp.shape[1]))

    return t_min, t_max, pp, dpp

def get_ind_combine_engine(x1, x2):
    '''
    Util function to find index of common values in x1 and x2
    :param x1:
    :param x2:
    :return:
    '''
    ind1 = []
    ind2 = []
    n_removed = 0
    for i in range(len(x1)):
        not_found = True
        for j in range(max((i - n_removed), 0), len(x2)):
            if x1[i] == x2[j]:
                ind1.append(i)
                ind2.append(j)
                not_found = False
                logger.debug("Found %d %d" % (i, j))
                break
        if not_found:
            logger.debug("Remove %d" % i)
            n_removed += 1
    return ind1, ind2


def get_ind_combine(t_minA, t_minB):
    '''
    it calls get_ind_combine_engine after sorting for length
    :param t_minA:
    :param t_minB:
    :return:
    '''
    if len(t_minA) == len(t_minB):
        return np.arange(len(t_minA)), np.arange(len(t_minB))
    elif len(t_minA) < len(t_minB):
        return get_ind_combine_engine(t_minA, t_minB)
    else:
        indA, indB =get_ind_combine_engine(t_minB, t_minA)
        return indB, indA


tphase_cmd='''12
list_evt.txt
none
%s
n
%d
%19.12e
%19.12e
%19.12e
0
n
%f
0
0
%f
%f
'''

tphase_cmd_orbit='''12
list_evt.txt
none
%s
y
%s
%d
%19.12e
%19.12e
%19.12e
0
n
%f
0
0
%f
%f
'''

def make_tphase(freq,  min_en=3., max_en=70., t_step=1000, n_bins=32, orbitfile=None, nudot=0, t_ref=0):
    """It builds the time-phase matrix

    Args:
        freq (float): folding frequency in Hertz
        min_en (float, optional): minimum energy to accumulate the matrix. Defaults to 3..
        max_en (float, optional): maximum energy to accumulate the matrix. Defaults to 70..
        t_step (int, optional): time step. Defaults to 1000.
        n_bins (int, optional): number of bins of the pulse profile. Defaults to 32.
        orbitfile (string, optional): name of the orbit correction file. Defaults to None.
        nudot (int, optional): frequency derivative. Defaults to 0.
        t_ref (int, optional): folding reference time (<=0 it takes the first time). Defaults to 0 to take the first time.

    Raises:
        It writes the time phase matrixes in fits format
    """    
    for tt in ['source', 'background']:
        for unit in ['A', 'B']:
            with open('list_evt.txt', 'w') as ff:
                ff.write('%s%s.evt' % (tt, unit))

            with open('timing_cmd.txt', 'w') as ff:
                if orbitfile is None:
                    ff.write(tphase_cmd % ('%s%s_TPHASE.fits' % (tt, unit),
                                     n_bins, t_ref, freq, nudot, t_step, min_en, max_en) )
                else:
                    if not os.path.isfile(orbitfile):
                        raise FileExistsError('File %s does not exist' % orbitfile)
                    ff.write(tphase_cmd_orbit % ('%s%s_TPHASE.fits' % (tt, unit), orbitfile,
                                           n_bins, t_ref, freq, nudot, t_step, min_en, max_en))

            run()
            shutil.copy('%s%s_TPHASE.fits' % (tt, unit), '%s%s_TPHASE_%03d.fits' % (tt, unit, n_bins))

def rebin_matrix(e_min, e_max, pp_input, dpp_input, min_s_n = 50, only_pulsed=False):
    '''

    :param e_min: array with minimum energy of each bin
    :param e_max: array with maximum energy of each bin
    :param pp: 2-d array with pulse profiles
    :param dpp: 2-d array with pulse profile uncertainties
    :param min_s_n: minimum S/N for rebin
    :param only_pulsed:  it subtracts the average value before rebinning
    :return:
    new_e_mins rebinned array with minimum energy of each bin
    new_e_maxs rebinned array with maximum energy of each bin
    new_pulses rebinned 2-d array with pulse profiles
    dnew_pulses rebinned 2-d array with pulse profile uncertainties
    '''

    new_pulses = []
    dnew_pulses = []
    new_e_mins = []
    new_e_maxs = []
    i1 = 0
    rebinned_index = 0

    pp = copy.deepcopy(pp_input)
    dpp = copy.deepcopy(dpp_input)
    while i1 < len(e_min) - 1:
        p1 = copy.copy(pp[i1, :])
        dp1 = copy.copy(dpp[i1, :])
        logger.debug('%d' % i1)
        for i2 in range(i1 + 1, len(e_min)):

            ind = dp1 > 0
            if only_pulsed:
                s_n = np.sum(np.abs(p1[ind] - np.mean(p1[ind]))) / np.sqrt(np.sum(dp1[ind] ** 2))
            else:
                s_n = np.sum(np.abs(p1[ind])) / np.sqrt(np.sum(dp1[ind] ** 2))

            logger.debug(s_n)
            #print(np.sum(np.abs(p1)), np.sqrt(np.sum(dp1 ** 2)), s_n)
            if s_n >= min_s_n or i2 == len(e_min) - 1:
                new_pulses.append(p1/float(i2-i1))
                dnew_pulses.append(dp1/float(i2-i1))
                new_e_mins.append(e_min[i1])
                new_e_maxs.append(e_max[i2 - 1])
                logger.debug("Boom %f %d %d " % (s_n, i1, i2))
                # print("Boom", s_n, i1, i2)
                # print(np.mean(p1)/float(i2-i1), np.mean(dp1)/float(i2-i1))
                i1 = i2
                logger.debug('Rebinned index : %d' % rebinned_index)
                # print('Rebinned index : %d' % rebinned_index)
                rebinned_index += 1
                break
            else:
                logger.debug("i2 %d" % i2)

                p1 += pp[i2, :]
                dp1 = np.sqrt(dp1 ** 2 + dpp[i2, :] ** 2)
                # print("i2", i2)
                # print(np.count_nonzero(p1), np.count_nonzero(pp[i2, :]))
                #It may happen that 1 background photon (negative rate) makes a bin to zero
                # if np.count_nonzero(p1) < old_nonzero:
                #     print(p1)
                #     print(pp[i2, :])
                old_nonzero = np.count_nonzero(p1)


    logger.info('We rebinned from %d to %d bins at a minimum S/N of %.1f' % (len(e_min), len(new_e_mins), min_s_n))
    return np.array(new_e_mins), np.array(new_e_maxs), np.array(new_pulses), np.array(dnew_pulses)

def pulse_fraction_from_data_rms(counts, counts_err, n_harm=3):
    a0 = np.mean(counts)
    K = n_harm
    N = np.size(counts)

    A = np.zeros(K)
    B = np.zeros(K)

    a = np.zeros(K)
    b = np.zeros(K)
    sigma_a = np.zeros(K)
    sigma_b = np.zeros(K)

    k = 0
    while k < K:
        L = np.zeros(N)
        M = np.zeros(N)
        P = np.zeros(N)
        O = np.zeros(N)
        # print('K=',k+1)
        for i in range(0, N):
            # print('aaaah: ',k,i)
            argsinus = (2 * np.pi * (k + 1) * (i + 1)) / N
            # print('argsin di '+str(k+1),' '+str(i+1)+' :',argsinus)
            L[i] = counts[i] * np.cos(argsinus)
            # print(L)
            # print('L: ',L[i])
            M[i] = counts[i] * np.sin(argsinus)
            # print('M: ',M[i])
            P[i] = counts_err[i] ** 2 * np.cos(argsinus) ** 2
            O[i] = counts_err[i] ** 2 * np.sin(argsinus) ** 2
            #
        A[k] = np.sum(L)
        # print('A:',A[k])
        B[k] = np.sum(M)
        # print('B: ',B)
        SIGMA_A = np.sum(P)
        SIGMA_B = np.sum(O)
        #
        a[k] = (1. / N) * A[k]
        # print(a[k])
        b[k] = (1. / N) * B[k]
        sigma_a[k] = (1. / (N ** 2)) * SIGMA_A
        sigma_b[k] = (1. / (N ** 2)) * SIGMA_B
        k = k + 1

    somma = a ** 2 + b ** 2
    # print(somma)
    differenza = sigma_a ** 2 + sigma_b ** 2
    bla = somma - differenza
    # print('diff: ',differenza)
    PF_rms = np.sqrt(2 * sum(bla)) / a0
    return (PF_rms)

def get_pulsed_fraction(e_min, e_max, pp, dpp, method_calc_rms='adaptive', output_file=None, force_recompute=False):
    """ this function fits an input energy range of the pulse profile.
        the fitting function will be a simple polynomial + gaussian
        the aim is to retrieve basic gaussian parameters to be compared
        to those obtained in spectral analysis around Ecycl.

    Args:
        e_min (_type_): _description_
        e_max (_type_): _description_
        pp (_type_): _description_
        dpp (_type_): _description_
        method_calc_rms (str, optional): _description_. Defaults to 'adaptive'.
        output_file (_type_, optional): _description_. Defaults to None.
        force_recompute (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
        output files: 
               1. the fit result
               2. the fit results to be plotted in a file
               3. Figure in pdf

    """
    if output_file is not None:
        filename = output_file
        if os.path.isfile(filename) and (force_recompute is False):
            ee_pulsed, dee_pulsed, pulsed_frac, dpulsed_frac = np.loadtxt(filename, unpack=True, skiprows=1)
            return ee_pulsed, dee_pulsed, pulsed_frac, dpulsed_frac

    ee_pulsed=(e_max+e_min)/2.
    dee_pulsed=(e_max-e_min)/2.
    pulsed_frac=np.zeros(len(e_min))
    dpulsed_frac=np.zeros(len(e_min))

    old_n_harm = pp.shape[1]

    for i in range(0, len(e_min)):
        x = pp[i,:]
        dx = dpp[i,:]
        if method_calc_rms=='minmax':
        #Min/MAX 
            pulsed_frac[i], dpulsed_frac[i] = pulse_fraction_from_data_min_max(x,dx)
        elif method_calc_rms=='fixednharm':
        #RMS with fixed n_harm
            pulsed_frac[i] = pulse_fraction_from_data_rms(x,dx, n_harm=3)
            dpulsed_frac[i] = get_error_from_simul(x,dx, pulse_fraction_from_data_rms, n_harm=3)
        else:
        #RMS with adaptive n_harm
            print(e_min[i], e_max[i])
            pulsed_frac[i] = fft_pulsed_fraction(x, dx, level=0.1, n_harm_min=2, n_harm_max=8, plot=False)
            dpulsed_frac[i] = get_error_from_simul(x,dx, fft_pulsed_fraction, level=0.1, n_harm_min=2, 
                                                         n_harm_max=8, verbose=False,  n_simul=300)
        
    if output_file is not None:
        with open(output_file, 'w') as ff:
            ff.write("Energy Energy_error Pullsed_fraction Pulsed_fraction_Error\n")
            for i in range(0, len(e_min)):
                ff.write("%.2f %.2f %.4f %.4f\n" % (ee_pulsed[i], dee_pulsed[i], 
                            pulsed_frac[i], dpulsed_frac[i]))
    return ee_pulsed, dee_pulsed, pulsed_frac, dpulsed_frac

def elaborate_pulsed_fraction(ee_pulsed, dee_pulsed, pulsed_frac, dpulsed_frac, debug_plots=True, e1=10, e2=20, 
                              stem='', poly_deg=[3, 3], title='', save_plot=True, e_threshold=0.3, 
                              division_derivative_order=2, max_n_high_lines = 2, forced_gaussian_centroids = [],
                              forced_gaussian_amplitudes = [],
                              forced_gaussian_sigmas = [],
                              y_lim=[0,1]):
    """This function implements the logics to perform a fit of the pulsed fraction.
    It first interpolates the pulsed fraction with a spline to find extremes of the function.
    Then it performs a fit with a polynomial plus gaussians.
    The general idea is to split the pulsed fraction into two regions, based on the flex of the function.
    Then to fit the lower energy checking for a gaussian feature in correspondence of the iron line complex.
    Then we look for minima of the PF in the highe part and inet gussians. 
    If there are too may minima, we reduce them.
    Logic is included to comply with few points.

    Args:
        ee_pulsed (numpy array): energy
        dee_pulsed (numpy array): energy error
        pulsed_frac (numpy array): pulsed fraction
        dpulsed_frac (numpy array): pulsed fraction uncertainty
        debug_plots (bool, optional): plot the derivative and the fits. Defaults to True.
        e1 (int, optional): lower energy to search the flex in this interval. Defaults to 10.
        e2 (int, optional): lower energy to search the flex in this interval. Defaults to 20.
        Note that if you put e1>=e2, we will use only one interval.
        stem (str, optional): a string in fron of output plot names. Defaults to ''.
        poly_deg (int or list of int, optional): degree of the polynomial. Defaults to 3.
        title (str, optional): title of the plots. Defaults to ''.
        save_plot (bool, optional): if plots should be saved Defaults to True.
        e_threshold (float, optional): if energies of PF minima differ in relative terms less than this values, they are reduced.
                                       ex.: if the algorithm finds minima at 32 and 35 keV, it retains only 32.
                                       This is used also as a range for the centroid search from (1-e_treshold)*e_centroid to 
                                       (1+e_treshold)*e_centroid Defaults to 0.3.
        division_derivative_order (int, optional): order of the derivative to search for the division, if 2 it searches a flex. Defaults to 2.
        max_n_high_lines (int, optional): do not use more gaussians thn this. Defaults to 2.
        forced_gaussian_centroids (list, optional): you can force the initial centroid energies with this parameter. Defaults to [].
        forced_gaussian_amplitudes (list, optional): you can force the initial amplitudes with this parameter, if the length of the list 
                                                    is different from the one of forced_gaussian_centroids, it is unused. Defaults to [].
        forced_gaussian_sigmas (list, optional): you can force the initial sigmas with this parameter, if the length of the list 
                                                 is different from the one of forced_gaussian_centroids, it is unused. Defaults to [].
        y_lim : limits for the plotting. DEfaults to [0,1]
    Returns:
        two fitting objects for the two ranges (the output of utils.fit_pulsed_frac). if only one is used, the second is None.
     """    
    from scipy import interpolate

    if type(poly_deg) is not list:
        poly_deg = [poly_deg]
    else:
        poly_deg = poly_deg

    smoothing = interpolate.UnivariateSpline(ee_pulsed, pulsed_frac, w=1./dpulsed_frac, k=3)
    fake_en = np.linspace(ee_pulsed[0], ee_pulsed[-1], 1000)
    smoothed_pulsed_frac_deriv=smoothing.derivative(1)(fake_en)
    smoothed_pulsed_frac_deriv_2=smoothing.derivative(2)(fake_en)

    def get_zeros(energy,deriv,deriv_2,selection):
        positive = deriv[selection] > 0
        ind_extreme = np.where(np.bitwise_xor(positive[1:], positive[:-1]))
        #print(energy[selection][ind_extreme])
        if deriv_2 is not None:
            ind_zeros = deriv_2[selection][ind_extreme] > 0
            return energy[selection][ind_extreme][ind_zeros]
        else:
            ind_zeros = ind_extreme
            return energy[selection][ind_zeros]

    def get_minimum(energy, deriv, selection):
        ind_min = np.argmin(deriv[selection])
        return energy[selection][ind_min]

    if debug_plots:
        fig,axes = plt.subplots(1,2,sharex=True)
        axes[0].errorbar(ee_pulsed,pulsed_frac, xerr=dee_pulsed, yerr=dpulsed_frac, linestyle='')
        axes[0].set_xlabel('Energy [keV]')
        axes[0].set_ylabel('Pulsed Fraction')
        axes[0].plot(fake_en, smoothing(fake_en))

        pulsed_frac_deriv=np.gradient(pulsed_frac, ee_pulsed)
        axes[1].plot(ee_pulsed, (pulsed_frac_deriv))
        axes[1].plot(fake_en, smoothed_pulsed_frac_deriv)
        axes[1].set_xlabel('Energy [keV]')
        axes[1].set_ylabel('Pulsed Fraction Derivative')

    ind_range1 = (fake_en >= e1) & (fake_en <=e2)
    make_double_fit = True
    if np.sum(ind_range1) <= 0:
        make_double_fit = False


    center=[[6.5, 5.5, 7.5]]
    sigma=[[0.2,0,1.0]]
    amplitude=[[0,-1,1]]
    if make_double_fit:
        if division_derivative_order == 2:
            e_turn = get_zeros(fake_en, smoothed_pulsed_frac_deriv_2, None, ind_range1)
        else:
            e_turn = get_zeros(fake_en, smoothed_pulsed_frac_deriv, smoothed_pulsed_frac_deriv_2, ind_range1)
        
        if len(e_turn) == 0:
            logger.info('Using the minimum derivative instead of zero in dividing regimes')
            e_turn = get_minimum(fake_en, smoothed_pulsed_frac_deriv, ind_range1)
        else:
            logger.info('Getting a zero of derivative to divide regimes')
            e_turn = e_turn[0]

        logger.info("We separate PF fit at %f keV" % e_turn)

        if debug_plots:
            axes[0].axvline(e_turn, 0, 1, color='cyan')
            axes[1].axvline(e_turn, 0, 1, color='cyan')

        ind_low = ee_pulsed <= e_turn
        ind_high = ee_pulsed > e_turn
        logger.info('We use %d points in the low-energy' % np.sum(ind_low))
        n_gauss = 1
    else:
        #all values
        ind_low = ee_pulsed > 0
        #no value
        ind_high = ee_pulsed > 0
        n_gauss = 1

        if len(forced_gaussian_centroids) > 0:
            center += [ [ee, (1-e_threshold)*ee, (1+e_threshold)*ee] for ee in forced_gaussian_centroids]
            if len(forced_gaussian_sigmas) == len(forced_gaussian_centroids):
                sigma += [[ee,0,2*ee] for ee in forced_gaussian_sigmas ]
            else:
                sigma = [[1+0*ee,0,3] for ee in forced_gaussian_centroids]
            
            if len(forced_gaussian_amplitudes) == len(forced_gaussian_centroids):
                amplitude += [[ee,-2*ee,4*ee] for ee in forced_gaussian_amplitudes ]
            else:
                amplitude = [[0*ee,-2,2] for ee in forced_gaussian_centroids ]
            n_gauss = len(center)



    pulsed_fit_low = fit_pulsed_frac(ee_pulsed[ind_low],dee_pulsed[ind_low], 
                                        pulsed_frac[ind_low], dpulsed_frac[ind_low], n_gauss=n_gauss, 
                                       center=center,
                                        sigma=sigma,
                                        amplitude=amplitude,
                                       degree_pol=poly_deg[0], plot_final=True, stem=stem+'low', y_lim=y_lim)

    if make_double_fit:

        e_cyc = get_zeros(fake_en, smoothed_pulsed_frac_deriv, smoothed_pulsed_frac_deriv_2, fake_en>e_turn)
        
        if len(e_cyc)>1:
            logger.info("Checking for too close Gaussians in %d elements" % len(e_cyc))
            diff_e_cyc= ( 1- e_cyc[0:-1]/e_cyc[1:] )
            ind_stay = diff_e_cyc > e_threshold
    #         print(e_cyc)
    #         print(diff_e_cyc)
    #         print(ind_stay)
            e_cyc = [e_cyc[0]] + [ee for ee in e_cyc[1:][ind_stay]]
            logger.info("Kept %d gaussians" % len(e_cyc))
        
        n_gauss = len(e_cyc)
        if n_gauss > 0 and max_n_high_lines > 0 and len(forced_gaussian_centroids) == 0:
            center = [ [ee, (1-e_threshold)*ee, (1+e_threshold)*ee] for ee in e_cyc[0:max_n_high_lines]]
            sigma=[[1+0*ee,0,3] for ee in e_cyc]
            amplitude=[[0*ee,-2,2] for ee in e_cyc ]
        elif len(forced_gaussian_centroids) > 0:
            center = [ [ee, (1-e_threshold)*ee, (1+e_threshold)*ee] for ee in forced_gaussian_centroids]

            if len(forced_gaussian_sigmas) == len(forced_gaussian_centroids):
                sigma = [[ee,0,2*ee] for ee in forced_gaussian_sigmas ]
            else:
                sigma = [[1+0*ee,0,3] for ee in forced_gaussian_centroids]
            
            if len(forced_gaussian_amplitudes) == len(forced_gaussian_centroids):
                amplitude = [[ee,-2*ee,4*ee] for ee in forced_gaussian_amplitudes ]
            else:
                amplitude = [[0*ee,-2,2] for ee in forced_gaussian_centroids ]
            n_gauss = len(forced_gaussian_centroids)
        else:
            center = []
            sigma = []
            amplitude = []
            n_gauss = 0
            
        #print(center,sigma,amplitude)
        logger.info('We use %d points in the high-energy' % np.sum(ind_high))
        high_poly_deg = poly_deg[-1]
        
        if np.sum(ind_high) <= high_poly_deg + n_gauss * 3:
            logger.info("Reducing polynomial order")
            while (np.sum(ind_high) <= high_poly_deg + n_gauss * 3) and high_poly_deg >0:
                
                high_poly_deg -= 1
            
            if (np.sum(ind_high) <= high_poly_deg + n_gauss * 3):
                n_gauss = 0
                center = []
                sigma = []
                amplitude = []
                high_poly_deg=1
        
        logger.info('We fit an order %d polynomial in the high-energy section' % high_poly_deg)
        logger.info('We fit %d gaussians in the high-energy section' % n_gauss)
        
        pulsed_fit_high = fit_pulsed_frac(ee_pulsed[ind_high],dee_pulsed[ind_high], 
                                            pulsed_frac[ind_high], dpulsed_frac[ind_high], n_gauss=n_gauss, 
                                        center=center,
                                            sigma=sigma,
                                            amplitude=amplitude,
                                        degree_pol=high_poly_deg, plot_final=True, stem=stem+'high',
                                        y_lim=y_lim)
    else:
        pulsed_fit_high = None

    
    from matplotlib.pyplot import cm
    comps_low = pulsed_fit_low.eval_components(x=ee_pulsed[ind_low])
    bb_low = (pulsed_frac[ind_low] - pulsed_fit_low.best_fit) / dpulsed_frac[ind_low]
    if make_double_fit:
        comps_high = pulsed_fit_high.eval_components(x=ee_pulsed[ind_high])
        bb_high = (pulsed_frac[ind_high] - pulsed_fit_high.best_fit) / dpulsed_frac[ind_high]

    col = cm.viridis(np.linspace(0, 1, 6))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 6.0), sharex=True, gridspec_kw={'height_ratios': [3, 1],
                                                                        'hspace': 0.0}
                                )
    ax1.errorbar(ee_pulsed,pulsed_frac, xerr=dee_pulsed, yerr=dpulsed_frac, linestyle=''
                , fmt='.', color=col[4], label='data')
    ax1.plot(ee_pulsed[ind_low], pulsed_fit_low.best_fit, '-', label='best fit (low)', color=col[0])
    ax1.plot(ee_pulsed[ind_low], comps_low['poly_'], '--', label='Polynomial (low)', color=col[1])
    if make_double_fit:
        ax1.plot(ee_pulsed[ind_high], pulsed_fit_high.best_fit, '-', label='best fit (high)', color=col[2])
        ax1.plot(ee_pulsed[ind_high], comps_high['poly_'], '--', label='Polynomial (high)', color=col[3])

    ax1.legend(loc='upper left')
    ax1.set_xscale('log')
    ax2.set_xlabel('E (keV)')
    ax1.set_ylabel('PF')
    ax1.set_ylim(y_lim)
    #ax1.set_xlim(x_lim)
    ax1.set_title(title)

    ax2.set_ylabel('Residuals')
    ax1.set_ylim(-0.1, 1)
    if make_double_fit:
        ax2.errorbar(ee_pulsed, np.concatenate([bb_low,bb_high]), xerr=dee_pulsed, yerr=1., fmt='.', color=col[2])
    else:
        ax2.errorbar(ee_pulsed, bb_low, xerr=dee_pulsed, yerr=1., fmt='.', color=col[2])
    ax2.axhline(y=0, color='k', linestyle='--')
    if save_plot:
        plt.savefig(stem + 'global_pulsed_fitted.pdf')

    return pulsed_fit_low, pulsed_fit_high

def fit_pulsed_frac(en, den, pf, dpf, stem=None, degree_pol=4, n_gauss=0, center=[],
                    sigma=[], amplitude=[],
                    plot_final=True, print_results=True, y_lim=[0,1], x_lim=[3,70]):
    '''
    this function will fit an input energy range of the pulse profile.
    the fitting function will be a simple polynomial + gaussian
    the aim is to retrieve basic gaussian parameters to be compared
    to those obtained in spectral analysis around Ecycl.
     output files: 1. the fit result
                   2. the fit results to be plotted in a file
                   3. Figure in pdf
    :param en: input energy
    :param den: input energy uncertainty
    :param pf: pulsed fraction
    :param dpf: pulsed fractio uncertainty
    :param stem: output prefix
    :param degree_pol: degree of the polynomial to fit
    :param n_gauss: number of gaussian lines
    :param center: array of centers of gaussians [[initial_value, min, max]]
    :param sigma: array of sigmas of gaussians [[initial_value, min, max]]
    :param amplitude: array of amplitude of gaussians [[initial_value, min, max]],
                        use negative values for absorption-like
    :param plot_final: if make a final plot
    :param print_results: if results should be printed out in file
    :return:
    '''
    from matplotlib.pyplot import cm
    from lmfit.models import PolynomialModel, GaussianModel

    if len(center) != n_gauss or len(sigma) != n_gauss or len (amplitude) != n_gauss:
        logger.error("You provided %d centers, %d sigmas, and %d amplitudes for %d gaussians" % (len(center), 
                            len(sigma), len(amplitude), n_gauss))
        return

    col = cm.viridis(np.linspace(0, 1, 6))

    if stem is not None:
        outputfile = open(stem + '_fit_pf.out', 'w')
    else:
        stem = ''
        outputfile = open('fit_pf.out', 'w')

    poly_mod = PolynomialModel(prefix='poly_', degree=degree_pol)
    pars = poly_mod.guess(pf, x=en, degree=degree_pol)
    mod = poly_mod

    for N in range(1, n_gauss+1):
        logger.debug("%d" % N)
        logger.debug("%g" % center[N - 1][0])
        gauss = GaussianModel(prefix='g' + str(N) + '_')
        pars.update(gauss.make_params())
        pars['g' + str(N) + '_center'].set(value=center[N - 1][0], min=center[N - 1][1], max=center[N - 1][2])
        pars['g' + str(N) + '_sigma'].set(sigma[N - 1][0], min=sigma[N - 1][1], max=sigma[N - 1][2])
        pars['g' + str(N) + '_amplitude'].set(amplitude[N - 1][0], min=amplitude[N - 1][1],
                                               max=amplitude[N - 1][2])
        mod = mod + gauss

    #initialfit = mod.eval(pars, x=en)

    out = mod.fit(pf, pars, x=en, weights = 1./dpf)

    bb = (pf - out.best_fit) / dpf

    comps = out.eval_components(x=en)
    logger.info(comps)

    if not plot_final:
        fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.8))
        axes[0].errorbar(en, pf, xerr=den, yerr=dpf, fmt='.', color=col[0])
        axes[0].plot(en, out.best_fit, '-', label='best fit', color=col[2])
        axes[0].legend(loc='upper left')
        axes[0].set_xlabel('E [keV]')
        axes[0].set_ylabel('PF')
        axes[0].set_ylim(y_lim)
        axes[0].set_xlim(x_lim)
        

        axes[1].errorbar(en, pf, xerr=den, yerr=dpf, fmt='.', color=col[0])
        for N in range(1, n_gauss+1):
            axes[1].plot(en, comps['g%d_' % N], '--', label='Gaussian %d' % N, color=col[3])
        axes[1].plot(en, comps['poly_'], '--', label='Polynomial component', color=col[4])
        axes[1].legend(loc='upper left')
        axes[1].set_xlabel('E [keV]')
        axes[1].set_ylabel('PF')
        axes[1].set_ylim(y_lim)
        axes[1].set_xlim(x_lim)
        
        plt.savefig(stem + 'fit_results.pdf')

    if print_results:
        datafile = open(stem + 'model_components_fit.dat', 'w')
        datafile.write('# fit results \n')
        datafile.write('# E[0]       dE[1]       pf_bestfit[2]          poly[3]            gauss1...N [4]...[N+4] \n')
        for j in range(len(pf)):
            datafile.write(str(round(en[j], 5)).ljust(10) + str(round(den[j], 2)).ljust(10) +
                           str(round(out.best_fit[j], 5)).ljust(15) + str(round(comps['poly_'][j], 5)).ljust(15) + '\t')
            for S in range(1, n_gauss+1):
                datafile.write(str(round(comps['g' + str(S) + '_'][j], 8)).ljust(25) + '\t')
            datafile.write('\n')

        datafile.close()

    if plot_final:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 6.0), sharex=True, gridspec_kw={'height_ratios': [3, 1],
                                                                              'hspace': 0.0}
                                       )
        ax1.errorbar(en, pf, xerr=den, yerr=dpf, fmt='.', color=col[4], label='data')
        ax1.plot(en, out.best_fit, '-', label='best fit', color=col[0])
        ax1.plot(en, comps['poly_'], '--', label='Polynomial', color=col[1])
        ax1.legend(loc='upper left')
        ax1.set_xscale('log')
        ax2.set_xlabel('E (keV)')
        ax1.set_ylabel('PF')
        ax1.set_ylim(y_lim)
        ax1.set_xlim(x_lim)
        
        ax2.set_ylabel('Residuals')
        ax1.set_ylim(-0.1, 1)
        ax2.errorbar(en, bb, xerr=den, yerr=1., fmt='.', color=col[2])
        ax2.axhline(y=0, color='k', linestyle='--')
        plt.savefig(stem + 'pulsed_fitted.pdf')

    logger.info(str(out.fit_report()))
    outputfile.write(out.fit_report())
    outputfile.close()

    return out


def explore_fit_mcmc(model_fitted, pars=[], hm_steps=7000, hm_walkers=2000, hm_jump=500, plot_corner=True, print_file=True,
                     stem='posterior'):
    '''
    this function explore the posterior parameter space obtained with a previous fit
    using mcmc
    outputs: - corner plot
             - Maximum Likelihood Estimation
             - Error @ 1,2,3 sigma  


    Parameters
    ----------
    model_fitted :  lmfit.model.ModelResult
        output of the fit procedure obtained with
        the function 'fit_pulsed_frac'
    pars :  lmfit.parameter.Parameters
        parameters of the fit (if not specified, we derive them from the results)
    hm_steps : INTEGER
        how many steps: number of steps for the MCMC, default = 7000
    hm_walkers : INTEGER
        how many walkers: number of walkers for MCMC, default = 2000
    hm_jump : INTEGER
        how many first step not to consider, default = 500
    plot_corner : BOOLEAN
        if the corner_plot has to be plotted

    Returns
    -------
    explore: lmfit.minimizer.MinimizerResult (result of the minimization using emcee)
    emcee_plot: corner plot of the posterior distribution


    '''
    import corner
    if hm_steps <= hm_jump :
        logger.error(" You almost did it!. However, the number of steps must be higher than the jumped ones:"
                     "hm_steps >>> hm_jump")

    if pars ==[]:
        pars = model_fitted.params.copy()

    explore = model_fitted.emcee(params=pars, steps=hm_steps, nwalkers=hm_walkers,
                                is_weighted=True, burn=hm_jump)
    if plot_corner:
        emcee_plot = corner.corner(explore.flatchain, labels=explore.var_names, show_titles=True,
                                   plot_datapoints=True)

    highest_prob = np.argmax(explore.lnprob)
    hp_loc = np.unravel_index(highest_prob, explore.lnprob.shape)
    mle_soln = explore.chain[hp_loc]

    pars2 = {}
    for el in pars.keys():
        if (pars[str(el)]).expr is None:
            pars2[str(el)] = pars[str(el)]

    for i, par in enumerate(pars2):
        pars2[par].value = mle_soln[i]

    fmt = '{:5s} {:11.5f} {:11.5f} {:11.5f}'.format

    logger.info('\nMaximum Likelihood Estimation from emcee ')
    logger.info('-------------------------------------------------')
    logger.info('Parameter MLE Value Median Value Uncertainty')

    for name, param in pars2.items():
        logger.info(fmt(name, param.value, explore.params[name].value, explore.params[name].stderr))

    logger.info('\Error estimates from emcee:')
    logger.info('------------------------------------------------------')
    logger.info('Parameter -3sigma -2sigma -1sigma median +1sigma +2sigma +3sigma')

    if print_file:
        o_f_emcee = open(stem + '.out', 'w')
        o_f_emcee.write('# Maximum Likelihood Estimation from emcee \n#Parameter MLE Value Median Value Uncertainty \n')
        for name, param in pars2.items():
            o_f_emcee.write(fmt(name, param.value, explore.params[name].value, explore.params[name].stderr) + '\n')
        o_f_emcee.write(
            '#\Error estimates from emcee: \n#Parameter -3sigma -2sigma -1sigma median +1sigma +2sigma +3sigma \n')

    for name in pars2.keys():
        quantiles = np.percentile(explore.flatchain[name], [0.135, 2.275, 15.865, 50, 84.135, 97.725, 99.865])
        median = quantiles[3]
        err_m3 = quantiles[0] - median
        err_m2 = quantiles[1] - median
        err_m1 = quantiles[2] - median
        err_p1 = quantiles[4] - median
        err_p2 = quantiles[5] - median
        err_p3 = quantiles[6] - median
        fmt = '{:5s} {:8.4f} {:8.4f} {:8.4f} {:8.4f} {:8.4f} {:8.4f} {:8.4f}'.format
        logger.info(fmt(name, err_m3, err_m2, err_m1, median, err_p1, err_p2, err_p3))
        o_f_emcee.write(fmt(name, err_m3, err_m2, err_m1, median, err_p1, err_p2, err_p3) + '\n')

    o_f_emcee.close()

    return explore, emcee_plot


def get_error_from_simul_rms(counts, counts_err, n_simul=100, n_harm=3):

    return get_error_from_simul(counts, counts_err, pulse_fraction_from_data_rms,
                                n_simul=n_simul, n_harms=n_harm)

def get_error_from_simul(counts, counts_err, method, n_simul=100, use_poisson=False, **kwargs):
    '''
    :param counts: input data
    :param counts_err: input data error
    :param method: a fnction with the method to compute the quantity
    :param n_simul: number of simulations
    :param kwargs: additional arguments to the function to be computed
    :return:
    '''
    simul_rms = []
    for i in range(n_simul):
        if use_poisson:
            fp = random.poisson(counts)
        else:
            fp = random.normal(counts, counts_err)
        simul_rms.append(method(fp, counts_err, **kwargs))

    return np.std(simul_rms)

def fft_pulsed_fraction(x, dx, level=0.1, n_harm_min=2, n_harm_max=-1, plot=False, verbose=True, label=''):
    '''
    Computes the pulsed fraction using an FFT. It stops as soon as the pulse is described at better than level
    :param x: pulse profile
    :param dx: pulse profile uncertainty
    :param level: confidenvce level for chi^2 test to stop number of harmonics (default 0.1)
    :param n_harm_min: minimum number of harmonics to use (default 2)
    :param n_harm_max: minimum number of harmonics to use (default -1 takes the size of pulse profile)
    :param plot: plot the pulse profile
    :param lavel: to save the plot with name "rms_`label`.pdf", if label=='' it does not save the plot
    :return: pulsed fraction (float)
    '''
    # import scipy.stats.chisquare as chi2
    from scipy.stats import chi2
    n = len(x)

    if n_harm_max < n_harm_min or n_harm_max > n/2:
        n_harm_max = n / 2

    fft = np.fft.fft(x)
    old_chi2_sf = -1.0
    for n_harm in range(int(n_harm_min), int(n_harm_max)):
        mask = np.ones(n, dtype=np.cdouble)
        mask[n_harm:-(n_harm - 1)] = 0 + 0j
        ifft = np.fft.ifft(fft * mask)
        y = np.real(ifft)
        #Necessary to avoid infinite for zero uncertaity
        ind = dx > 0
        chi2_val = np.sum(((x[ind] - y[ind]) / dx[ind]) ** 2)
        dof = max(1, n - (1 + 2 * (n_harm - 1)))
        chi2_sf = chi2.sf(chi2_val, dof)
        # print(chi2_val, dof)
        # print(chi2_sf, old_chi2_sf)
        #Sometimes, we do ot reach the required level, but we cannot describe the pulse significantly better,
        # so we stop in any case (condition chi2_sf < old_chi2_sf)
        if chi2_sf > level or chi2_sf < old_chi2_sf:
            break
        old_chi2_sf = chi2_sf

    if verbose:
        logger.info("Used %d harmonics for pulse description" % n_harm)
    a = np.absolute(fft) / n
    pulsed_frac = np.sqrt(np.sum(a[1:n_harm] ** 2) + np.sum(a[-n_harm + 1:] ** 2)) / a[0]

    if plot:
        import matplotlib.pyplot as plt
        plt.figure()
        f = np.linspace(0, 1, n)
        plt.errorbar(f, x, yerr=dx, marker='.', label='data %s' % label)
        plt.plot(f, y, label='%d harmonics' % n_harm)
        plt.xlabel('Phase')
        plt.legend()
        if label != '':
            plt.savefig('rms_%s.pdf' % label)

    return pulsed_frac

def pulse_fraction_from_data_min_max(x,dx):

    i_min = np.argmin(x)
    i_max = np.argmax(x)
    tmp1 = (x[i_min]+x[i_max])
    pulsed_frac = (x[i_max] - x[i_min]) / tmp1
    dpulsed_frac = 2*np.sqrt((x[i_max]/tmp1**2)**2 * dx[i_max]**2 + (x[i_min]/tmp1**2)**2 * dx[i_min]**2)

    return pulsed_frac, dpulsed_frac
import matplotlib.cm
def plot_matrix_as_image(ee, pp, kind='E', normalize=True,outfile=None, cmap=matplotlib.cm.gist_earth,
                         sliders=False, n_levels=30, min_level=None, max_level=None, source_name=None):
    '''

    :param ee: y-scale (time or energy)
    :param pp: Energy-Phase or Time-Phase matrix (# of rows must equal len(ee))
    :param kind: * 'E' energy phase
                 * 'T' Time-phase
                 * 'NE' energy phase with energy normalized to the cyclotron energy
    :param normalize: normalize each pulse at its average and divide by the standard deviation
    :param outfile: the file to save the figure as image (optional)
    ;param cmap the colormap of matplotlib, defaults to matplotlib.cm.gist_earth
    ;param sliders if True uses sliders
    ;param n_levels the number of linearly spaced contour levels
    ;param min_level the minimum level for contours
    ;param max_level the maximum level for contours
    ;param source_name if not None, it is used as plot title
    :return:
    '''

    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider
    # from matplotlib.widgets import Button

    if pp.shape[0] != len(ee):
        raise ImportError('len(ee) [%d] != # rows pp [%d]' % (len(ee), pp.shape[0]))
    pp1 = pp.copy()
    if normalize:
        for i in range(pp.shape[0]):
            x = pp[i, :]
            m = np.mean(x)
            s = np.std(x)
            pp1[i, :] = (x - m) / s

    phi = np.linspace(0, 1, pp.shape[1])
    plt.figure(figsize=(8.8, 7))
    # if sliders:
    #     plt.subplots_adjust(top=0.82)
    if min_level is None:
        min_level = np.min(pp1)
    if max_level is None:
        max_level = np.max(pp1)
    levels = np.linspace(min_level, max_level, n_levels)
    cs = plt.contourf(phi, ee, pp1, cmap=cmap, levels=levels,
                           extend="both", zorder=0)
    cs.cmap.set_under('k')
    cs.set_clim(np.min(levels), np.max(levels))
    cb = plt.colorbar(cs)

    plt.xlabel('Phase')
    if kind == 'E':
        plt.yscale('log')
        plt.ylabel('Energy [keV]')
    elif kind == 'T':
        plt.ylabel('Time [s]')
    elif kind == 'NE':
        plt.yscale('log')
        plt.ylabel('$E/E_\\mathrm{Cyc}$')

    if source_name is not None:
        plt.title(source_name)
    if outfile is not None:
        plt.savefig(outfile)

    if sliders:
        # Nice to have : slider
        cmin = plt.axes([0.05, 0.95, 0.3, 0.02])
        cmax = plt.axes([0.65, 0.95, 0.3, 0.02])

        smin = Slider(cmin, 'Min', min_level, max_level, valinit=np.min(levels), orientation='horizontal')
        smax = Slider(cmax, 'Max', min_level, max_level, valinit=np.max(levels), orientation='horizontal')
        # areplot = plt.axes([0.4, 0.88, 0.1, 0.05])
        # bnext = Button(areplot, 'Reset', color='0.55', hovercolor='0.9')
        n_levels = 10

        # def reset(x):
        #     smin.reset()
        #     smax.reset()
        # cid = bnext.on_clicked(reset)

        def update(x):
            if smin.val < smax.val:
                cs.set_clim(smin.val, smax.val)

        smin.on_changed(update)
        smax.on_changed(update)

        return cs




def plot_matrix_as_lines(t, pp, dpp, kind='T', normalize=False, offset=0):
    '''

    :param t: time or energy array
    :param pp: time-phase or energy-phase matrix
    :param dpp: uncertainty on time-phase or energy-phase matrix
    :param kind: 'E' or 'T'
    :param normalize: normalize the pulses to mean and standard deviation
    :param offset: Offset between on profile and the following one
    :return:
    '''

    pt = pp.copy()
    dpt = dpp.copy()
    if normalize:
        for i in range(pp.shape[0]):
            x = pp[i, :]
            dx = dpp[i, :]
            m = np.mean(x)
            s = np.std(x)
            pt[i, :] = (x - m) / s
            dpt[i, :] = dx / s

    import matplotlib.pyplot as plt
    plt.figure()
    phi = np.linspace(0, 2, 2*pt.shape[1])

    plot_pt = np.tile(pt, 2)
    plot_dpt = np.tile(dpt, 2)

    total_offset = 0
    from matplotlib.colors import hsv_to_rgb
    from cycler import cycler
    colors = [hsv_to_rgb([(i * 0.618033988749895) % 1.0, 1, 1])
              for i in range(pt.shape[0])]
    plt.rc('axes', prop_cycle=(cycler('color', colors)))
    for i in range(pt.shape[0]):

        y = plot_pt[i, :]
        dy = plot_dpt[i, :]
        if np.sum(dy) > 0:
            # if np.sum(y) / np.sqrt(np.sum(dy ** 2)) > 10:
            label = "%.0f s" % ( t[i] - t[0])
            if kind == 'E':
                label = "%.1f keV" % t[i]
            ebar = plt.errorbar(phi, y+total_offset, xerr=0.5 / pt.shape[1], yerr=dy, linestyle='-',
                                marker='.', label=label)
            plt.text(phi[int(plot_pt.shape[1]*0.75)], y[int(plot_pt.shape[1]*0.75)]+total_offset, label,
                     color=ebar[0].get_color())
            #print(int(pt.shape[1]/2), phi[int(pt.shape[1]/2)], y[int(pt.shape[1]/2)]+total_offset,)
            total_offset += offset
    plt.ylabel('Rate per bin')
    plt.xlabel('Phase')
    #plt.legend()

def get_fourier_coeff(pulse):
    '''
    returns the first two harmonic coefficients
    :param pulse:
    :return:
    phi0 phase of first harmonic
    phi0_2 phase of second harmonic
    a relative amplitude of first harmonic
    a2 relative amplitude of second harmonic
    '''

    phi = np.linspace(0, 2 * np.pi, len(pulse))
    i_c = np.sum(np.cos(phi) * pulse) / np.pi
    i_s = np.sum(np.sin(phi) * pulse) / np.pi
    i_c2 = np.sum(np.cos(2 * phi) * pulse) / np.pi
    i_s2 = np.sum(np.sin(2 * phi) * pulse) / np.pi

    phi0 = np.arctan2(i_s, i_c) / 2 / np.pi
    phi0_2 = np.arctan2(i_s2, i_c2) / 2 / np.pi
    a = np.sqrt(i_c * i_c + i_s * i_s) / len(pulse) / np.mean(pulse)
    a2 = np.sqrt(i_c2 * i_c2 + i_s2 * i_s2) / len(pulse) / np.mean(pulse)

    return phi0, phi0_2, a, a2

def get_fourier_coeff_error( counts, counts_err, n_simul=100, use_poisson=False):

    sim_phi0 = []
    sim_phi0_2 = []
    sim_A = []
    sim_A2 = []

    for i in range(n_simul):
        if use_poisson:
            fp = random.poisson(counts)
        else:
            fp = random.normal(counts, counts_err)
        phi0, phi0_2, A, A2 = get_fourier_coeff(fp)
        sim_phi0.append(phi0)
        sim_phi0_2.append(phi0_2)
        sim_A.append(A)
        sim_A2.append(A)

    return np.std(sim_phi0), np.std(sim_phi0_2,), np.std(sim_A), np.std(sim_A2)

def rate_filter(time, rate, drate, level_down=0, level_up = 1e10, quantile=0.8, make_plot=True, 
                far=1e-4, rate_label='rate', histo_bins=300):
    '''
rate_filter(self, typical_level=0.5, quantile=0.7,  make_plot=True, far=1e-3,
                    tmin=0,tmax=1e12):
This function prepares cleaned events by apllying a standard filter eliminating bins with FAR < far
This is useful if one want to eliminate a peculiar part of an observation.
The filter is controlled in the following way:
- a Gaussian is fitted on LC data within the innner quantile (default=0.8) of the light curve
- a limit is set on FAR, but it can be overrided by using the level_up and level_down parameters, which are the lowest/highest possible limit.
        '''
        
    print(rate_filter.__doc__)

    if make_plot:
        f, axes = plt.subplots(1, 2)
        axes[0].errorbar(time, rate, yerr=drate, linestyle='none')
        axes[0].set_ylabel(rate_label)
        #axes[0].set_title(self.target + ' ' + self.obs_id)
        axes[0].set_xlabel('Time [s]')
        n_hist, edges, patches = axes[1].hist(rate, bins=histo_bins, density=True, facecolor='green',
                                              alpha=0.75)
        axes[1].set_xlabel(rate_label)

    # x=(edges[0:-2]+edges[1:])/2
    from scipy.stats import norm
    ind = (rate <= np.quantile(rate, quantile)) & (rate >= np.quantile(rate, 1.-quantile))
    (mu, sigma) = norm.fit(rate[ind])

    y = norm.pdf(edges, mu, sigma)

    fap = np.min([1. / len(rate), far])
    tmp = norm.isf(fap, loc=mu, scale=sigma)
    limit_up = np.min([level_up, tmp ])
    limit_down = np.max([level_down, 2*mu-tmp])

    if make_plot:
        _ = axes[1].plot(edges, y, 'r--', linewidth=2)
        _ = axes[1].axvline(limit_up, 0, 1, color='cyan')
        _ = axes[0].axhline(limit_up, 0, 1, color='cyan')
        _ = axes[1].axvline(limit_down, 0, 1, color='blue')
        _ = axes[0].axhline(limit_down, 0, 1, color='blue')
        
        plt.savefig('rate_select.pdf')
    return limit_down, limit_up

def write_orbit_file_from_gbm_page(url, file_name='orbit.dat',
                                   orbital_parameters = ['axsin', 'Eccentricity', 'periastron',
                                                         'T<sub>', 'Orbital Period', 'Period Deriv.']):
    '''
    It writes a file to be used in timingsuite for the orbit starting from the GBM page
    This is tested just for Cen X-3 at the moment and it is very fragile

    :param url: The url of the GBM page of the source
        (e.g. 'https://gammaray.nsstc.nasa.gov/gbm/science/pulsars/lightcurves/cenx3.html')
    :param file_name: the name of output file default 'orbit.dat'
    :param orbital_parameters the orbital parameters to be extracted from the table
        default: ['axsin', 'Eccentricity', 'periastron',
                 'T<sub>', 'Orbital Period', 'Period Deriv.']
    :return: file_name or None
    '''
    import requests
    from bs4 import BeautifulSoup
    import re
    from astropy.time import Time

    #Parses the table with a particular argument (fragile)
    html = requests.get(url).content
    soup = BeautifulSoup(html)
    orbit_table = soup.find('table', attrs={'border': 2})
    trs = orbit_table.find_all('tr')

    #removes the first row as it contains the table title
    trs[0].extract()

    #Find numbers (https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string)
    numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    rx = re.compile(numeric_const_pattern, re.VERBOSE)

    #for each parmeter it extracts the value as string
    orbit = {}
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) < 2:
            continue
        for k in orbital_parameters:
            if k.lower() in str(tds[0]).lower():
                orbit.update({k: rx.findall(str(tds[1]))[0]})

    if orbital_parameters[0] not in orbit:
        logger.warning('Not able to retrieve the orbital parameters as %s could not be read' % orbital_parameters[0])
        return None
    # it writes the orbit file
    logger.info('Writing the following orbit parameters')
    with open(file_name, 'w') as ff:
        for kk in orbital_parameters:
            if 'T' in kk:
                t_90 = Time(orbit[kk], format='jd')
                # The orbit file contains the longitude of periastron or the lower conjunction
                if float(orbit['Eccentricity']) >= 0.:
                    logger.debug('Special eccentricity')
                    ff.write('%f\n' % (t_90.mjd + (float(orbit['periastron']) - 90.)/360. *\
                                       float(orbit['Orbital Period'])))
                else:
                    logger.debug('Non Special eccentricity')
                    ff.write('%f\n' % (t_90.mjd - 0.25 * float(orbit['Orbital Period'])))
            else:
                ff.write(orbit[kk] + '\n')
            logger.info('%s %s' % (kk , orbit[kk]))
    return file_name

def get_cross_correlation(pp, plot=False):

    correlation = []
    lag = []
    for i in range(pp.shape[0]):

        x = (pp[i, :] - np.mean(pp[i, :])) / np.std(pp[i, :])
        y = np.sum(pp[0:i, :], 0) + np.sum(pp[i + 1:, :], 0)
        y = (y - np.mean(y)) / np.std(y)
        corr = np.correlate(np.tile(x, 2), y) / len(x)
        correlation.append(np.max(corr))
        lag.append(np.argmax(corr))

    if plot:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.subplot(1, 2, 1)
        plt.plot(corr)
        plt.subplot(1, 2, 2)
        plt.plot(x)
        plt.plot(y, linestyle='--')

    lag = np.array(lag)
    lag[lag > (pp.shape[1]/2)] -= pp.shape[1]
    return lag, np.array(correlation)

def get_cross_correlation_error(pp, dpp, n_simul=100, use_poisson=False):

    fake_lags = np.empty([n_simul, pp.shape[0]], dtype=float)
    fake_corrs = np.empty([n_simul, pp.shape[0]], dtype=float)

    for i in range(n_simul):
        if use_poisson:
            fake_pp = random.poisson(pp)
        else:
            fake_pp = random.normal(pp, dpp)

        fake_lags[i, :], fake_corrs[i, :] = get_cross_correlation(fake_pp)

    return np.std(fake_lags, 0), np.std(fake_corrs, 0)

def get_target_coords_extern(input_name):
    from astroquery.simbad import Simbad
    from astropy import units as u
    from astropy.coordinates import SkyCoord

    name = input_name
    simbad = Simbad.query_object(name)
    c = SkyCoord(simbad['RA'], simbad['DEC'], unit=[u.hour, u.deg])
    c.fk5
    logger.info("Coordinates for %s are RA=%.4f, Dec=%.4f" % (name, c.ra.deg[0], c.dec.deg[0]))

    return c.ra.deg[0], c.dec.deg[0]
