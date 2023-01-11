#!/usr/bin/env python3

import sys, re, argparse, math, os, datetime, logging, copy
from abc import ABC, abstractmethod
import numpy as np
import scipy.optimize, scipy.stats
import matplotlib.pyplot as plt

__version__ = '1.0.1'

LOG_CLASSES_BASE = math.e ** 0.02

def parse_args():
    p = argparse.ArgumentParser(
        description = 'Estimates the depth-complexity ratio and noisiness of '
            ' the amplification of a sequencing experiment given a PCR clone '
            'size histogram. Report issues at '
            'https://bitbucket.org/rochette/decoratio/issues. Please cite: (TBD).',
        usage='decoratio [--model MODEL] [...] CLONE_SIZE_HISTOGRAM.tsv',
        add_help=False)
    p.add_argument('--version', action='version', help=argparse.SUPPRESS,
        version='{} {}'.format(__package__, __version__))
    p.add_argument('-h', '--help', action='help', help=argparse.SUPPRESS)
    p.add_argument('input_path', metavar='CLONE_SIZE_HISTOGRAM.tsv',
        help='path to a TSV file whose header line starts with '
        '"clone_size \\t n_clones" or "clone_size \\t n_reads". (Alternatively, '
        'a GSTACKS output file ending with "gstacks.log.distribs".)')
    p.add_argument('--model', type=str, default='logskewnormal',
        help='An amplification model specifier such as "logskewnormal" (default), '
        '"lognormal", or "inheff:12". See MODEL SPECIFICATION section.')
    p.add_argument('--output-prefix', type=str, metavar='PREFIX',
        help='defaults to CLONE_SIZE_HISTOGRAM.tsv.decoratio.*')
    p.add_argument('--ratio-min', type=float, default=0.02, help=argparse.SUPPRESS)
    p.add_argument('--ratio-max', type=float, help=argparse.SUPPRESS)
    p.add_argument('--inheff-n-efficiency-bins', type=int, help=argparse.SUPPRESS)
    p.add_argument('--inheff-n-sims-per-bin', type=int, help=argparse.SUPPRESS)
    p.add_argument('--inheff-legacy-sims', action='store_true', help=argparse.SUPPRESS)
    p.add_argument('--inheff-uncouple-beta-parameters', action='store_true', help=argparse.SUPPRESS)
    p.add_argument('--tsv-out', action='store_true', help=argparse.SUPPRESS)
    p.add_argument('--no-plots', dest='png_out', action='store_false', help=argparse.SUPPRESS)
    p.add_argument('--log-level', type=str, default='WARN', help=argparse.SUPPRESS)

    args = p.parse_args()
    logging.basicConfig(level=args.log_level)
    logging.getLogger('matplotlib').setLevel(logging.ERROR)
    if args.output_prefix is None:
        args.output_prefix = '{}.decoratio.{}'.format(
            args.input_path, args.model.replace(':', '_'))
    try:
        args.model = AmplModel.factory(args.model)
    except ValueError:
        sys.exit('ERROR: failed to parse model \'{}\''.format(args.model))
    if isinstance(args.model, InheffAmplModel):
        assert hasattr(args.model, 'n_efficiency_bins')
        assert hasattr(args.model, 'n_sims_per_bin')
        assert hasattr(args.model, 'legacy_sims')
        if args.inheff_n_efficiency_bins:
            args.model.n_efficiency_bins = args.inheff_n_efficiency_bins
        if args.inheff_n_sims_per_bin:
            args.model.n_sims_per_bin = args.inheff_n_sims_per_bin
        if args.inheff_legacy_sims:
            args.model.legacy_sims = True
        if args.inheff_uncouple_beta_parameters:
            args.model.uncouple_beta_parameters = True
    return args

def main():
    args = parse_args()
    print(datetime.datetime.now().strftime('%Y-%m-%d-%H%M'), os.getcwd())
    print('decoratio-{} (python-{}.{}, scipy-{})'.format(
        __version__, *sys.version_info[:2], scipy.__version__))
    print('Called as:', *sys.argv)
    print('Outputing to: {}.*'.format(args.output_prefix))
    # Read the input distribution.
    print('Reading input file...', flush=True)
    with open(args.input_path) as f:
        obs_cz_d, n_clones = (load_cz_d_from_tsv(f)
            if not args.input_path.endswith('gstacks.log.distribs')
            else load_cz_d_from_gstacks_distribs_log(f))
    obs_duprate = calc_duprate(obs_cz_d)
    print('Input data shows {:.1%} PCR duplicates.'.format(obs_duprate))
    # Optimize the ratio and/or the amplification distribution.
    if args.ratio_max is None:
        args.ratio_max = 1 / (1 - obs_duprate)
    if not args.model.needs_optimization():
        model = args.model
        print('Generating the amplification factor distribution...', flush=True)
        ampl_cz_d = model.get_ampl_cz_d(LOG_CLASSES_BASE)
        print('The provided model had a noisiness of {:.3f}; a skewness of {:.2f}'.format(
            AmplModel.calc_noisiness(ampl_cz_d, LOG_CLASSES_BASE),
            AmplModel.calc_skewness(ampl_cz_d, LOG_CLASSES_BASE)))
        print('Optimizing the depth-complexity ratio...', flush=True)
        ratio = optimize_ratio(obs_cz_d, ampl_cz_d, args)
    else:
        print('Optimizing the depth-complexity ratio & amplification noise...', flush=True)
        ratio, model = optimize_ratio_noise(obs_cz_d, args)
        ampl_cz_d = model.get_ampl_cz_d(LOG_CLASSES_BASE)
    # Print the optimization results.
    pred_cz_d = generate_cz_distrib(ratio, ampl_cz_d, LOG_CLASSES_BASE)
    overlap = cz_d_overlap(pred_cz_d, obs_cz_d)
    print('Optimized:\n'
        '\n'
        '    depth_complexity_ratio = {:.3g}\n'
        '    model = {}'.format(ratio, model))
    print(
        '\n'
        'Model fit was {:.1%}; the predicted duplicate was rate {:.1%} and the saturation {:.1%}; '
        'the amplification model\'s noisiness was {:.3f} and its skewness {:.2f}.'
        .format(
            overlap,
            calc_duprate(pred_cz_d),
            ratio * (1.0 - calc_duprate(pred_cz_d)),
            AmplModel.calc_noisiness(ampl_cz_d, LOG_CLASSES_BASE),
            AmplModel.calc_skewness(ampl_cz_d, LOG_CLASSES_BASE)))
    if ratio * (1.0 - calc_duprate(obs_cz_d)) > 1 + 1e-6:
        print('WARNING: The complexity estimate was lower than physically '
            'possible given the observed rate of unique reads',
            file=sys.stderr)
    # Print the distribution.
    print('Writing output files...', flush=True)
    if args.tsv_out:
        write_tsv_output(
            open('{}.tsv'.format(args.output_prefix), 'w'),
            obs_cz_d, pred_cz_d, n_clones)
    # Draw a plot.
    if args.png_out:
        draw_png_output(
            open('{}.png'.format(args.output_prefix), 'wb'),
            obs_cz_d, pred_cz_d, n_clones)
        draw_ampl_factors_hist(
            open('{}.ampl_factors.png'.format(args.output_prefix), 'wb'),
            ampl_cz_d, LOG_CLASSES_BASE)
    print('Done.')

class AmplModel(ABC):
    @abstractmethod
    def __str__(self):
        pass
    @abstractmethod
    def get_ampl_cz_d(self, log_base):
        pass
    @abstractmethod
    def needs_optimization(self):
        pass
    @abstractmethod
    def get_optimizable_parameters_bounds(self):
        pass
    @abstractmethod
    def set_optimizable_parameters(self, p):
        pass

    @staticmethod
    def factory(model_str):
        x = model_str.strip().split(':')
        if len(x) == 0:
            raise ValueError()
        if x[0] == 'lognormal':
            return LognormalAmplModel(model_str)
        elif x[0] == 'logskewnormal':
            return LogskewnormalAmplModel(model_str)
        elif x[0] in ['inheff', 'inheffbeta']:
            return InheffAmplModel(model_str)
        else:
            raise ValueError()

    @staticmethod
    def calc_noisiness(ampl_cz_d, base):
        assert abs(sum([p for p in ampl_cz_d if p is not None]) - 1.0) < 1e-3
        m = 0.0
        for log_a, prob in enumerate(ampl_cz_d):
            a = radinitio_get_clone_class_representative_value(log_a, base)
            if a is None:
                assert prob is None or prob == 0.0
                continue
            m += prob * log_a * math.log(base)
        v = 0.0
        for log_a, prob in enumerate(ampl_cz_d):
            a = radinitio_get_clone_class_representative_value(log_a, base)
            if a is None:
                assert prob is None or prob == 0.0
                continue
            v += prob * ((log_a * math.log(base) - m) ** 2)
        return math.sqrt(v)

    @staticmethod
    def calc_skewness(ampl_cz_d, base):
        assert abs(sum([p for p in ampl_cz_d if p is not None]) - 1.0) < 1e-3
        m = 0.0
        for log_a, prob in enumerate(ampl_cz_d):
            a = radinitio_get_clone_class_representative_value(log_a, base)
            if a is None:
                assert prob is None or prob == 0.0
                continue
            m += prob * log_a * math.log(base)
        v = 0.0
        g = 0.0
        for log_a, prob in enumerate(ampl_cz_d):
            a = radinitio_get_clone_class_representative_value(log_a, base)
            if a is None:
                assert prob is None or prob == 0.0
                continue
            r = log_a * math.log(base) - m
            v += prob * (r ** 2)
            g += prob * (r ** 3)
        return g / v ** (3/2)

class LognormalAmplModel(AmplModel):
    MODEL_NAME = 'lognormal'

    def __init__(self, model_str):
        x = model_str.strip().split(':')
        if x[0] != self.MODEL_NAME:
            raise ValueError()
        if len(x) > 2:
            raise ValueError()
        self.stdev = None
        if len(x) == 2:
            self.stdev = float(x[1])
            if not self.stdev > 0.0:
                raise ValueError()

    def __str__(self):
        if self.stdev is None:
            return self.MODEL_NAME
        else:
            return '{}:{:.3f}'.format(self.MODEL_NAME, self.stdev)

    def get_ampl_cz_d(self, log_base):
        # The base matters for comparability of stdevs, so (other than for binning)
        # we're using the base of the natural logarithm.
        stdev_base = self.stdev / math.log(log_base)
        m = math.log(1_000_000, log_base)
        # Get the CDF values.
        cdf = []
        while len(cdf) == 0 or cdf[-1] < 1 - 1e-6:
            x = range(len(cdf), len(cdf)+round(100))
            cdf = np.append(cdf, scipy.stats.norm.cdf(x, loc=m, scale=stdev_base))
        # Tally the frequencies over log classes.
        ampl_d = [cdf[0]]
        prev = 0
        for i in range(1, len(cdf)):
            if radinitio_get_sizes_in_clone_class(i, log_base) is None:
                ampl_d.append(None)
            else:
                ampl_d.append(cdf[i] - cdf[prev])
                prev = i
        return ampl_d

    def needs_optimization(self):
        return self.stdev is None

    def get_optimizable_parameters_bounds(self):
        stdev_min = 0.01
        stdev_max = 2.0
        return [(math.log(stdev_min), math.log(stdev_max))]

    def set_optimizable_parameters(self, params):
        assert len(params) == 1
        logstdev = params[0]
        self.stdev = math.exp(logstdev)

class LogskewnormalAmplModel(AmplModel):
    MODEL_NAME = 'logskewnormal'

    def __init__(self, model_str):
        x = model_str.strip().split(':')
        if x[0] != self.MODEL_NAME:
            raise ValueError()
        if len(x) not in [1, 3]:
            raise ValueError()
        self.stdev = None
        self.a = None
        if len(x) == 3:
            self.stdev = float(x[1])
            self.a = float(x[2])
            if not self.stdev > 0.0:
                raise ValueError()

    def __str__(self):
        if self.stdev is None:
            return self.MODEL_NAME
        else:
            return '{}:{:.3f}:{:.3g}'.format(self.MODEL_NAME, self.stdev, self.a)

    def get_ampl_cz_d(self, log_base):
        # The base matters for comparability of stdevs, so (other than for binning)
        # we're using the base of the natural logarithm.
        stdev_base = self.stdev / math.log(log_base)
        m = math.log(1_000_000, log_base)
        a = self.a
        aa = 2.0 / math.pi * a * a / (1 + a * a)
        scale = stdev_base / math.sqrt(1 - aa)
        loc = m + np.sign(a) * scale * math.sqrt(aa)
        # Get the CDF values.
        cdf = []
        while len(cdf) == 0 or cdf[-1] < 1 - 1e-6:
            x = range(len(cdf), len(cdf) + round(100))
            cdf = np.append(cdf, scipy.stats.skewnorm.cdf(x, loc=loc, scale=scale, a=a))
        # Tally the frequencies over log classes.
        ampl_d = [cdf[0]]
        prev = 0
        for i in range(1, len(cdf)):
            if radinitio_get_sizes_in_clone_class(i, log_base) is None:
                ampl_d.append(None)
            else:
                ampl_d.append(cdf[i] - cdf[prev])
                prev = i
        assert abs(sum([p for p in ampl_d if p is not None]) - 1.0) < 1e-3
        return ampl_d

    def needs_optimization(self):
        return self.stdev is None

    def get_optimizable_parameters_bounds(self):
        log_stdev_min = math.log(0.01)
        log_stdev_max = math.log(2.0)
        a_min = -10.0
        a_max = +10.0
        return [(log_stdev_min, log_stdev_max), (a_min, a_max)]

    def set_optimizable_parameters(self, params):
        logstdev, self.a = params
        self.stdev = math.exp(logstdev)

class InheffAmplModel(AmplModel):
    DEFAULT_N_EFFICIENCY_BINS = 1000
    DEFAULT_N_SIMULATIONS_PER_BIN = 1000

    def __init__(self, model_str):
        self.n_efficiency_bins = self.DEFAULT_N_EFFICIENCY_BINS
        self.n_sims_per_bin = self.DEFAULT_N_SIMULATIONS_PER_BIN
        self.legacy_sims = False
        self.uncouple_beta_parameters = False
        x = model_str.split(':')
        if x[0] not in ['inheff', 'inheffbeta']:
            raise ValueError()
        self.type = x[0]
        if not len(x) >= 2:
            print('ERROR: "{}": a number of cycles is required.'.format(model_str))
            raise ValueError()
        self.n_cycles = int(x[1])
        if len(x) not in [2, 4]:
            raise ValueError
        self.mean = None
        self.stdev = None
        if len(x) == 4:
            self.mean = float(x[2])
            self.stdev = float(x[3])
            if not self.stdev > 0.0:
                raise ValueError()
            if self.type == 'inheff':
                if self.mean + 2 * self.stdev < 0.0 or self.mean - 2 * self.stdev > 1.0:
                    print('ERROR: "{}": distribution must overlap [0,1].'
                        .format(model_str))
                    raise ValueError()
            elif self.type == 'inheffbeta':
                if not 0.0 < self.mean < 1.0:
                    raise ValueError()
                try:
                    a, b = beta_d_mean_sdtev_to_alpha_beta(self.mean, self.stdev)
                except ValueError as e:
                    print('ERROR: "{}": impossible mean/stdev combination'
                        .format(model_str))
                    raise e
                if a < 1 or b < 1:
                    print('WARNING: "{}": distribution is bimodal (a={:.3f}, b={:.3f})'
                        .format(model_str, a, b), file=sys.stderr)

    def __str__(self):
        if self.mean is None:
            return '{}:{:d}'.format(self.type, self.n_cycles)
        else:
            return '{}:{:d}:{:.2f}:{:.2f}'.format(self.type, self.n_cycles, self.mean, self.stdev)

    def get_ampl_cz_d(self, log_base):
        if self.legacy_sims:
            return self.get_ampl_cz_d_one_by_one(log_base)
        effs = self.get_representative_bin_efficiencies()
        assert len(effs) == self.n_efficiency_bins
        assert all(np.isfinite(effs))
        ampl_d = []
        for eff in effs:
            # Simulate for this efficiency.
            clone_sizes = np.full(self.n_sims_per_bin, 1, dtype=np.int64)
            for _ in range(self.n_cycles):
                clone_sizes += np.random.binomial(clone_sizes, eff)
            # Record the observed clone sizes.
            clone_sizes_logbins = np.int64(np.floor(np.log(clone_sizes) / math.log(log_base)))
            log_cz_max = max(clone_sizes_logbins)
            for log_cz in range(len(ampl_d), log_cz_max + 1):
                ampl_d.append(
                    0.0
                    if radinitio_get_sizes_in_clone_class(log_cz, log_base) is not None
                    else None)
            for log_cz in clone_sizes_logbins:
                assert ampl_d[log_cz] is not None
                ampl_d[log_cz] += 1.0
        s = sum([n for n in ampl_d if n is not None])
        assert s == self.n_efficiency_bins * self.n_sims_per_bin
        ampl_d = [ n/s if n is not None else None for n in ampl_d ]
        return ampl_d

    def needs_optimization(self):
        return self.mean is None

    def get_optimizable_parameters_bounds(self):
        if not self.uncouple_beta_parameters:
            noisiness_min = 0.0 + 1e-6
            noisiness_max = 1.0 - 1e-6
            return [(noisiness_min, noisiness_max)]
        else:
            mean_min = 0.01 + 1e-3
            mean_max = 0.99 - 1e-6
            log_k_min = math.log(2)
            log_k_max = math.log(100)
            return [(mean_min, mean_max), (math.log(2), log_k_max)]

    def set_optimizable_parameters(self, params):
        if not self.uncouple_beta_parameters:
            # We construct the noisiness of the inherited efficiency model so that it is:
            # -- between 0 and 1;
            # -- minimal when the mean is 1.0 and the stdev is 0.0;
            # -- maximal (for a non-bimodal beta distribution) for the constant
            #    distribution, i.e. for alpha=1, beta=1, so that the mean is 0.5 and the
            #    stdev is sqrt(1/12) = 0.2886751345948129.
            # N.B. This works for both the normal and beta versions.
            assert len(params) == 1
            noisiness = params[0]
            assert 0.0 < noisiness < 1.0
            self.mean = 1.0 - 0.5 * noisiness
            self.stdev = 0.288675 * noisiness
        else:
            if self.type != 'inheffbeta':
                raise NotImplementedError()
            self.mean, log_k = params
            self._k = math.exp(log_k)
            self.stdev = math.sqrt(self.mean * (1 - self.mean) / (1+self._k))

    def get_representative_bin_efficiencies(self):
        quantiles = np.arange(0.0+1e-6, 1.0-0.9e-6, (1.0-2e-6) / self.n_efficiency_bins)
        assert len(quantiles) == self.n_efficiency_bins + 1
        if self.type == 'inheff':
            q0, q1 = scipy.stats.norm.cdf([0.0, 1.0], self.mean, self.stdev)
            quantiles = q0 + (q1-q0) * quantiles
            eff_breaks = scipy.stats.norm.ppf(quantiles, self.mean, self.stdev)
            eff_break_pdfs = scipy.stats.norm.pdf(eff_breaks, self.mean, self.stdev)
        elif self.type == 'inheffbeta':
            a, b = beta_d_mean_sdtev_to_alpha_beta(self.mean, self.stdev)
            eff_breaks = scipy.stats.beta.ppf(quantiles, a, b)
            eff_break_pdfs = scipy.stats.beta.pdf(eff_breaks, a, b)
        # effs = (eff_breaks[1:] + eff_breaks[:-1]) / 2
        effs = (
            eff_breaks[1:] * eff_break_pdfs[1:]
            + eff_breaks[:-1] * eff_break_pdfs[:-1]
            ) / (eff_break_pdfs[1:] + eff_break_pdfs[:-1])
        return effs

    def get_ampl_cz_d_one_by_one(self, log_base):
        # Legacy simulation approach.
        clone_histogram = {}
        n_sims = self.n_efficiency_bins * self.n_sims_per_bin
        for i in range(n_sims):
            eff = self.draw_one_efficiency()
            clone_size = 1
            for _ in range(self.n_cycles):
                clone_size += np.random.binomial(clone_size, eff)
            clone_histogram.setdefault(clone_size, 0)
            clone_histogram[clone_size] += 1
        max_size = max(clone_histogram.keys())
        for i in range(max_size+1):
            clone_histogram.setdefault(i, 0)
        clone_histogram = [ clone_histogram[i] / n_sims for i in range(max_size+1) ]
        return radinitio_log_convert_clone_dist(clone_histogram, log_base)

    def draw_one_efficiency(self):
        if self.type == 'inheff':
            while True:
                p = np.random.normal(self.mean, self.stdev)
                if 0 < p < 1:
                    break
        elif self.type == 'inheffbeta':
            p = np.random.beta(*beta_d_mean_sdtev_to_alpha_beta(self.mean, self.stdev))
        return p

def beta_d_mean_sdtev_to_alpha_beta(m, s):
    nu = m * (1 -m) / s**2 - 1
    if nu < 0:
        raise ValueError()
    a = nu * m
    b = nu * (1 - m)
    return a, b

def load_cz_d_from_tsv(tsv_f):
    cz_d = {}
    hist_type = None
    warned_multiple = False
    for line_i, line in enumerate(tsv_f):
        if line[0] in '#\n':
            continue
        if hist_type is None:
            m = re.search(r'^clone_size\t(n|num)_(reads|clones)\b', line)
            if not m:
                sys.exit('ERROR: The TSV header should start with '
                    '"clone_size\\tnum_reads" or "clone_size\\tnum_clones".')
            assert len(m.groups()) == 2
            hist_type = m.group(2)
            logging.info('hist_type is \'{}\''.format(hist_type))
            assert hist_type in ['reads', 'clones']
            continue
        if line.startswith('END'):
            # This happens when called from load_cz_d_from_gstacks_distribs_log().
            break
        fields = line.strip('\n').split('\t')
        z = int(fields[0])
        n = float(fields[1])
        if hist_type == 'clones':
            cz_d[z] = n
        else:
            cz_d[z] = n/z
            if n > 1 and n % z != 0.0 and not warned_multiple:
                print('WARNING: in clone size histogram file, at line {}: the '
                    'number of reads {} ought to be a multiple of the clone '
                    'size {}.'.format(line_i + 1, n, z), file=sys.stderr)
                warned_multiple = True
    if not cz_d:
        sys.exit('ERROR: input TSV file is empty.')
    n_clones = sum(cz_d.values())
    cz_d = [
        cz_d[z] if z in cz_d.keys() else 0
        for z in range(max(cz_d.keys())+1) ]
    cz_d = [ n / sum(cz_d) for n in cz_d ]
    return cz_d, n_clones

def load_cz_d_from_gstacks_distribs_log(gstacks_distlog_f):
    logging.info('Loading cz_d from gstacks log')
    for line in gstacks_distlog_f:
        if line.startswith('BEGIN pcr_clone_size_distrib'):
            break
    if not line.startswith('BEGIN pcr_clone_size_distrib'):
        # section wasn't found.
        sys.exit('ERROR: Couldn\'t find the clone size distribution in the input file;'
            ' gstacks was not run with --rm-pcr-duplicates or Stacks version is not >=2.3')
    return load_cz_d_from_tsv(gstacks_distlog_f)

def calc_duprate(cz_d):
    assert abs(sum(cz_d) - 1.0) < 1e-3
    return 1.0 - 1.0 / sum([ f*z for z, f in enumerate(cz_d[1:], 1) ])

def calc_duprate_log(log_cz_d):
    n_clones = 0.0
    n_reads = 0.0
    for log_z, f in enumerate(log_cz_d):
        if log_cz_d[log_z] is None:
            continue
        n_clones += f
        n_reads += f * radinitio_get_clone_class_representative_value_float(log_z, base=LOG_CLASSES_BASE)
    return 1 - n_clones / n_reads

def cz_d_to_reads(cz_d):
    cz_d_reads = [ n * z for z, n in enumerate(cz_d) ]
    cz_d_reads = [ f / sum(cz_d_reads) for f in cz_d_reads ]
    return cz_d_reads

def score_log_cz_distrib(pred_log_cz_d, obs_log_cz_d, method):
    long, short = (
        (obs_log_cz_d, pred_log_cz_d) if len(obs_log_cz_d) >= len(pred_log_cz_d)
        else (pred_log_cz_d, obs_log_cz_d))
    if method == 'duprate':
        score = abs(calc_duprate_log(long) - calc_duprate_log(short))
    elif method  == 'clonefrac_sumsquares':
        clonesum_long = sum([x for x in long if x is not None])
        clonesum_short = sum([x for x in short if x is not None])
        score = 0.0
        for i in range(len(long)):
            if i < len(short):
                assert (long[i] is None) == (short[i] is None)
            if long[i] is None:
                continue
            score += (
                long[i] / clonesum_long
                - (short[i] / clonesum_short if i < len(short) else 0.0)
                ) ** 2
    elif method  == 'clonefrac_overlap':
        clonesum_long = sum([x for x in long if x is not None])
        clonesum_short = sum([x for x in short if x is not None])
        score = 0.0
        for i in range(len(short)):
            assert (long[i] is None) == (short[i] is None)
            if short[i] is None:
                continue
            score += min(long[i] / clonesum_long, short[i] / clonesum_short)
        score = 1.0 - score
    elif method  == 'readfrac_sumsquares':
        # @NR 2021-10-11: Seems to work okay in combination with shgo-sobol.
        readsum_long = sum([
            x * radinitio_get_clone_class_representative_value_float(i, base=LOG_CLASSES_BASE)
            for i, x in enumerate(long) if x is not None])
        readsum_short = sum([
            x * radinitio_get_clone_class_representative_value_float(i, base=LOG_CLASSES_BASE)
            for i, x in enumerate(short) if x is not None])
        score = 0.0
        for i in range(len(long)):
            if i < len(short):
                assert (long[i] is None) == (short[i] is None)
            if long[i] is None:
                continue
            z = radinitio_get_clone_class_representative_value_float(i, base=LOG_CLASSES_BASE)
            score += (
                long[i] * z / readsum_long
                - (short[i] * z / readsum_short if i < len(short) else 0.0)
                ) ** 2
    elif method  == 'readfrac_overlap':
        # @NR 2021-10-11: This seems to work poorly. Don't use.
        readsum_long = sum([
            x * radinitio_get_clone_class_representative_value_float(i, base=LOG_CLASSES_BASE)
            for i, x in enumerate(long) if x is not None])
        readsum_short = sum([
            x * radinitio_get_clone_class_representative_value_float(i, base=LOG_CLASSES_BASE)
            for i, x in enumerate(short) if x is not None])
        score = 0.0
        for i in range(len(short)):
            assert (long[i] is None) == (short[i] is None)
            if short[i] is None:
                continue
            z = radinitio_get_clone_class_representative_value_float(i, base=LOG_CLASSES_BASE)
            score += min(long[i] * z / readsum_long, short[i] * z / readsum_short)
        score = 1.0 - score
    return score

def cz_d_overlap(predicted_cz_d, obs_cz_d):
    # Calculate the overlap area between the two read-wise frequency distributions.
    obs = cz_d_to_reads(obs_cz_d)
    obs = [ x / sum(obs) for x in obs]
    predicted = cz_d_to_reads(predicted_cz_d)
    predicted = [ x / sum(predicted) for x in predicted]
    while len(obs) < len(predicted):
        obs.append(0.0)
    while len(obs) > len(predicted):
        predicted.append(0.0)
    area_overlap = sum([
        min(predicted[i], obs[i])
        for i in range(len(predicted)) ])
    assert 0.0 <= area_overlap <= 1.0
    return area_overlap

def optimize_ratio(obs_cz_d, ampl_cz_d, args):
    obs_log_cz_d = radinitio_log_convert_clone_dist(obs_cz_d, LOG_CLASSES_BASE)
    def f(logratio):
        seq_log_cz_d = radinitio_log_convert_clone_dist(
            generate_cz_distrib(math.exp(logratio), ampl_cz_d, LOG_CLASSES_BASE),
            LOG_CLASSES_BASE)
        return score_log_cz_distrib(obs_log_cz_d, seq_log_cz_d, 'readfrac_sumsquares')
    logratio_bounds = (math.log(args.ratio_min), math.log(args.ratio_max))
    ratio_opt = scipy.optimize.minimize_scalar(f, method='bounded', bounds=logratio_bounds)
    if not ratio_opt.success:
        sys.exit('ERROR: Optimizer failed.')
    return math.exp(ratio_opt.x)

def optimize_ratio_noise(obs_cz_d, args):
    # @NR 2021-10-24: I'm not sure where to write this so I'm putting it here.
    # scipy.optimize.shgo() sometimes raises:
    #     "ValueError: `x0` violates bound constraints."
    # with `_minimize_slsqp()` in the stack. This appears to be a bug in Scipy
    # (c.f. https://github.com/scipy/scipy/issues/11403#issuecomment-717676023).
    # that was resolved by commit https://github.com/scipy/scipy/pull/13009,
    # which is included in scipy >= v1.6.0.
    # p.s. It's possible to get around the bug by fiddling with parameter
    # boundaries on the command line; in my example simply adding
    # `--loggamma-stdev-min 0.05` gave me a complete run. (This is instead of
    # the default 0.01; observed values are often ~0.50, for AMRO 0.60 and 0.64
    # for the half and full datasets respectively).
    obs_log_cz_d = radinitio_log_convert_clone_dist(obs_cz_d, LOG_CLASSES_BASE)
    model = copy.deepcopy(args.model)
    logratio_bounds = (math.log(args.ratio_min), math.log(args.ratio_max))
    model_bounds = model.get_optimizable_parameters_bounds()
    def f(x):
        ratio = math.exp(x[0])
        logging.debug('model.set_optimizable_parameters({})'.format(list(x[1:])))
        model.set_optimizable_parameters(x[1:])
        ampl_cz_d = model.get_ampl_cz_d(LOG_CLASSES_BASE)
        seq_log_cz_d = radinitio_log_convert_clone_dist(
            generate_cz_distrib(ratio, ampl_cz_d, LOG_CLASSES_BASE),
            LOG_CLASSES_BASE)
        return score_log_cz_distrib(obs_log_cz_d, seq_log_cz_d, 'readfrac_sumsquares')
    optim = scipy.optimize.shgo(f, [logratio_bounds] + model_bounds,
        sampling_method='sobol')
    if not optim.success:
        sys.exit('ERROR: Optimizer failed.')
    model.set_optimizable_parameters(optim.x[1:])
    return math.exp(optim.x[0]), model

def write_tsv_output(o_tsv_file, obs_cz_d, pred_cz_d, n_clones):
    obs_cz_d_reads = cz_d_to_reads(obs_cz_d)
    pred_cz_d_reads = cz_d_to_reads(pred_cz_d)
    n_reads = n_clones / (1.0 - calc_duprate(obs_cz_d))
    print('clone_size', 'obs_n_reads', 'obs_n_clones', 'pred_frac_reads', 'pred_freq_clones',
        sep='\t', file=o_tsv_file)
    for z in range(len(obs_cz_d)):
        if n_clones >= 2:
            print('{}\t{:d}\t{:d}\t{:.6g}\t{:.6g}'.format(
                z,
                round(obs_cz_d_reads[z] * n_reads),
                round(obs_cz_d[z] * n_clones),
                pred_cz_d_reads[z] if len(pred_cz_d_reads) > z else 0.0,
                pred_cz_d[z] if len(pred_cz_d) > z else 0.0
                ), file=o_tsv_file)
        else:
            print('{}\t{:.6g}\t{:.6g}\t{:.6g}\t{:.6g}'.format(
                z,
                obs_cz_d_reads[z],
                obs_cz_d[z],
                pred_cz_d_reads[z] if len(pred_cz_d_reads) > z else 0.0,
                pred_cz_d[z] if len(pred_cz_d) > z else 0.0
                ), file=o_tsv_file)

def draw_png_output(o_png_file, obs_cz_d, pred_cz_d, n_clones):
    obs_cz_d_reads = cz_d_to_reads(obs_cz_d)
    pred_cz_d_reads = cz_d_to_reads(pred_cz_d)
    n_reads = n_clones / (1.0 - calc_duprate(obs_cz_d))
    n_clones_pred = n_reads * (1.0 - calc_duprate(pred_cz_d))

    # Histogram, reads view
    plt.bar(
        range(len(obs_cz_d_reads)),
        [f * n_reads for f in obs_cz_d_reads],
        width=1.0, color='#888888', linewidth=None)
    # Histogram, clones view
    plt.bar(
        range(len(obs_cz_d)),
        [f * n_clones for f in obs_cz_d],
        width=1.0, color='#555555', linewidth=None)
    # Model line, reads view
    plt.plot(
        range(1, len(pred_cz_d_reads)),
        [f * n_reads for f in pred_cz_d_reads[1:]],
        'D-', color='black', lw=1.0, markersize=2.0)
    # Model line, clones view
    plt.plot(
        range(1, len(pred_cz_d)),
        [ f * n_clones_pred for f in pred_cz_d[1:] ],
        'D--', color='black', lw=1.0, markersize=2.0)
    # Axes, etc.
    # For xmax, use 5 times the clone size of a mean read.
    xmax = round(5.0 * sum(
        [ z * obs_cz_d_reads[z] / sum(obs_cz_d_reads)
        for z in range(len(obs_cz_d_reads)) ]))
    ymax = 1.2 * n_reads * max(max(obs_cz_d_reads), max(pred_cz_d_reads))
    ymax_right = ymax / n_reads
    plt.xticks(
        range(1, xmax)
        if xmax < 30
        else [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000])
    plt.axis([ 0.5, 0.5 + xmax, 0, ymax ])
    # plt.title('Observed & predicted PCR clone size distribution')
    plt.xlabel('PCR clone size')
    plt.ylabel('Count of reads / clones')
    plt.legend(
        (
            'fitted model (reads)',
            'fitted model (clones)',
            'observed (reads)',
            'observed (clones)'),
        loc='upper right')
    right_axis = plt.twinx()
    right_axis.set_ylabel('Fraction of reads')
    right_axis.set_ylim(0, ymax_right)
    plt.tight_layout()
    plt.savefig(o_png_file, dpi=300)
    plt.close()

def draw_ampl_factors_hist(o_png_file, ampl_cz_d, log_base):
    bins = [ radinitio_get_sizes_in_clone_class(log_a, log_base)
        for log_a in range(len(ampl_cz_d)) ]
    assert all([ (bins[log_a] is None) == (ampl_cz_d[log_a] is None)
        for log_a in range(len(ampl_cz_d)) ])
    # Add one more bin, so we can compute the last width.
    log_a = len(bins) - 1
    while True:
        log_a += 1
        bins.append(radinitio_get_sizes_in_clone_class(log_a, log_base))
        if bins[-1] is not None:
            break
    left_pos = np.array([ b[0] for b in bins if b is not None ], dtype=np.float)
    # Scale by the mean amplification factor & log the axis (natural log).
    left_pos /= radinitio_calc_amplification_factor(ampl_cz_d, log_base)
    left_pos = np.log(left_pos)
    widths = left_pos[1:] - left_pos[:-1]
    left_pos = left_pos[:-1]
    probs = [ p for p in ampl_cz_d if p is not None ]
    assert len(probs) == len(left_pos) == len(widths)
    # Draw the histogram.
    plt.bar(left_pos, probs, width=widths)
    plt.axis([
        np.log(1e-3), np.log(1e3),
        0, 1.2 * max(probs)])
    plt.xlabel('log(amplification factor)')
    plt.ylabel('Density')
    # plt.xticks...
    plt.savefig(o_png_file, dpi=300)
    plt.close()

##################################################
##      (copy-pasted RADinitio functions)       ##
##################################################

def radinitio_get_sizes_in_clone_class(log_a, base):
    assert log_a >= 0
    clone_class = range(
        math.ceil(base ** log_a),
        math.ceil(base ** (log_a + 1)) )
    if not clone_class:
        return None
    return clone_class

def radinitio_get_clone_class_representative_value(log_a, base):
    if radinitio_get_sizes_in_clone_class(log_a, base) is None:
        return None
    return round(base ** (log_a + 0.5))

def radinitio_get_clone_class_representative_value_float(log_a, base):
    sizes = radinitio_get_sizes_in_clone_class(log_a, base)
    return None if sizes is None else (sizes.start + sizes.stop - 1) / 2

def radinitio_log_convert_clone_dist(clone_size_distrib, base):
    # generate empy distribution of size x, where x is the log of the biggest clone in the original distribution
    a_max = len(clone_size_distrib) - 1
    log_clone_size_distrib = []
    for log_a in range(math.floor(math.log(a_max, base)) + 1):
        log_clone_size_distrib.append(
            0.0 if radinitio_get_sizes_in_clone_class(log_a, base) else None)
    for a, prob in enumerate(clone_size_distrib):
        if a == 0:
            continue
        log_a = math.floor(math.log(a, base))
        log_clone_size_distrib[log_a] += prob
    # assert 1.0-1e-9 < sum(log_clone_size_distrib) < 1.0+1e-9
    return log_clone_size_distrib

def radinitio_calc_amplification_factor(ampl_cz_d, base):
    ampl_factor = 0.0
    for log_a, prob in enumerate(ampl_cz_d):
        a = radinitio_get_clone_class_representative_value(log_a, base)
        if a is None:
            assert prob is None or prob == 0.0
            continue
        ampl_factor += a * prob
    return ampl_factor

def generate_cz_distrib(depth_complexity_ratio, ampl_cz_d, base):
    ampl_factor = radinitio_calc_amplification_factor(ampl_cz_d, base)
    # precompute the p(seq_cz=s|ampl_cz=a)
    max_s = 300 # Max size of sequenced clones; this impacts performance.
    p_s_a = []
    for log_a in range(len(ampl_cz_d)):
        a = radinitio_get_clone_class_representative_value(log_a, base)
        p_s_a.append(
            None if a is None
            else scipy.stats.poisson.pmf(
                range(max_s), (depth_complexity_ratio * a / ampl_factor)))
    # Compute the distribution.
    seq_cz_d = []
    sum_p = 0.0
    for s in range(max_s):
        p = 0.0
        for log_a in range(len(ampl_cz_d)):
            a = radinitio_get_clone_class_representative_value(log_a, base)
            if a is None:
                continue
            p += ampl_cz_d[log_a] * p_s_a[log_a][s]
        seq_cz_d.append(p)
        # Break when values are getting too small.
        sum_p += p
        if sum_p > 0.999 and p < 1e-5:
            break
    if s >= max_s - 1:
        logging.warning(
            'The clone size distribution extended past the hard-coded maximum clone size, {}; at sum_probs = {:.6f}'
            .format(max_s, sum(seq_cz_d)))
    # Trucate the distribution at 0 & rescale it.
    logging.debug('generate_cz_distrib(): sum(seq_cz_d) = {:.6f}'.format(sum(seq_cz_d)))
    seq_cz_d[0] = 0.0
    s = sum(seq_cz_d)
    seq_cz_d = [ p / s for p in seq_cz_d ]
    assert len(seq_cz_d) >= 2
    return seq_cz_d
