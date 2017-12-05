import numpy as np
from glob import glob

from pend_functions import *


path = get_file_location()
all_files = glob(path + '/*.dat')

n_files = len(all_files)

periods = np.zeros(n_files)
errors  = np.zeros(n_files)

for i in range(n_files):
    popt, perr = pend_get_periods_least_sq(all_files[i])
    periods[i] = popt[0]
    errors[i]  = perr[0]

print(periods, errors)
