import numpy as np
from pend_functions import *

filename = get_file_name()

popt, perr = pend_get_periods_least_sq(filename)

print popt, perr
