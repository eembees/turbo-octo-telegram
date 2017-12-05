import numpy as np
from glob import glob
from quick_maths import quick_maths

def get_pend_periods(fname):
    raw       = np.loadtxt(fname)
    raw_time  = np.array([el[1] for el in raw])
    time_diff = np.ediff1d(raw_time)
    period_ts = time_diff + np.roll(time_diff,1)
    return period_ts
## Taking time and returning period for all experiments combined
def split_pend_periods(periods):
    flat_set_1 = periods[0::2]
    flat_set_2 = periods[1::2]
    return flat_set_1,flat_set_2

def get_sigmas(sigmas, array):
    return np.ones(len(array))*sigmas


if __name__ == '__main__':
    from get_rms import get_file_name
    fname = get_file_name()
    # filenames = glob('./data/pend/*')
    ## variables
    sigmas = 0.06  #0.06977244  # 0.07 -> ~50% prob on the half period

    # Do script
    p       = get_pend_periods(fname)
    p1, p2  = split_pend_periods(p)
    sig1    = get_sigmas(sigmas, p1)
    sig2    = get_sigmas(sigmas, p2)

    print(p1, sig1)
    quick_maths(p1,sig1, True)
