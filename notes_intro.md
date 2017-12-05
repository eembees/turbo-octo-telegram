# Notes
pendulum formula:
g = L(2pi/T)²
sigma_g_sq = (2pi/T)^4*sigma_L_sq + (-2*L*((2pi)^2)T^3)^2 * sigma_T_sq

## ball on incline
assume:
sigma_t = 1/40000 s --> 0
sigma_d = 1 mm

only one uncertainty: sigma_d

### DOF
5 data points
fitted with:
d(t) = x_o + v_o*t + a*t^2
3 parameters:
DOF = 2

chi_sq_optimal = 2


# Script
'''
Input:
x_i     list of points
sigma_i list of uncertainties
print   bool, whether or not to print

Output
mu        weighted mean
sigma_mu  uncertainty on wt mean
chi_sq
N_DOF
prob
'''
