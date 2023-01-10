import numpy as np


def calculate_snr_f_statistics(truth_f: np.ndarray) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray):
    """Calculate statistics of snr_f truth data.

    For now, includes mean and standard deviation of the raw values (usually energy)
    and mean and standard deviation of the dB values (10 * log10).
    """
    classes = truth_f.shape[1]

    snr_mean = np.zeros(classes, dtype=np.float32)
    snr_std = np.zeros(classes, dtype=np.float32)
    snr_db_mean = np.zeros(classes, dtype=np.float32)
    snr_db_std = np.zeros(classes, dtype=np.float32)

    for c in range(classes):
        tmp = truth_f[:, c]
        tmp = np.double(tmp[np.isfinite(tmp)])

        if len(tmp) == 0:
            snr_mean[c] = -np.inf
            snr_std[c] = -np.inf
        else:
            snr_mean[c] = np.mean(tmp)
            snr_std[c] = np.std(tmp, ddof=1)

        tmp2 = 10 * np.ma.log10(tmp).filled(-np.inf)
        tmp2 = tmp2[np.isfinite(tmp2)]

        if len(tmp2) == 0:
            snr_db_mean[c] = -np.inf
            snr_db_std[c] = -np.inf
        else:
            snr_db_mean[c] = np.mean(tmp2)
            snr_db_std[c] = np.std(tmp2, ddof=1)

    return snr_mean, snr_std, snr_db_mean, snr_db_std


def calculate_mapped_snr_f(truth_f: np.ndarray, snr_db_mean: np.ndarray, snr_db_std: np.ndarray) -> np.ndarray:
    """Calculate mapped SNR from standard SNR energy per bin/class."""
    import scipy.special as sc

    old_err = np.seterr(divide='ignore', invalid='ignore')
    num = 10 * np.log10(np.double(truth_f)) - np.double(snr_db_mean)
    den = np.double(snr_db_std) * np.sqrt(2)
    q = num / den
    q = np.nan_to_num(q, nan=-np.inf, posinf=np.inf, neginf=-np.inf)
    mapped_snr_f = 0.5 * (1 + sc.erf(q))
    np.seterr(**old_err)

    return np.float32(mapped_snr_f)
