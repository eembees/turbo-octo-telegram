import numpy as np
from quick_maths import quick_maths as qm
from pend_functions import *

'''
run the script
'''

## Initializing by setting values
h_bloc = [2.47, 2.5, 2.49, 2.49]
s_bloc = [0.05, 0.02, 0.01, 0.02]

h_hook = [4.11,4.13,4.1,4.1,4.13]
s_hook = [0.04,0.05,0.05,0.05,0.02]

h_roof = [324.,	323.9,	323.9,	323.9,	323.9]
s_roof = np.ones(len(h_pend))*0.1

h_pend = np.array([324.0,323.9,323.9,323.9,323.9]) * 0.01
s_pend = np.ones(len(h_pend))*0.1 * 0.01
sigma_t = 0.07 #0.06977244  # 0.07 -> ~50% prob


# gets mean h and corresponding uncertainty
h_mu, h_si, _, _, _ = qm(h_pend, s_pend)

# fname = get_file_name()
fname = './data/pend/magnus_1.dat'

periods = pend_get_periods(fname)

p1,p2 = pend_split_periods(periods)

p1_sig = get_sigmas(p1,sigma_t)
p2_sig = get_sigmas(p2,sigma_t)

p1_mean, p1_sigma, _, _, _ = qm(p1,p1_sig)
p2_mean, p2_sigma, _, _, _ = qm(p2,p2_sig)

print p1_mean,p1_sigma

g1, sigma_g1_sq = pend_calc_g(h_mu, h_si, p1_mean, p1_sigma)
print g1, sigma_g1_sq
