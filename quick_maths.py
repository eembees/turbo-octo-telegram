## quick_maths.py
## by Magnus Berg Sletfjerding (eembees@gmail.com)
##################
from math import *
from scipy import stats

def quick_maths(x_i, sigma_i, print_function=False):
    '''
    Input:
    x_i         list of points
    sigma_i     list of uncertainties
    print       bool, whether or not to print

    Output:
    wt_mu        weighted mean
    sigma_mu     uncertainty on wt mean
    chi_sq       chi squared
    N_DOF        degrees of freedom
    prob         probability of chi_sq with N_DOF
    '''
    ## Wt Mean:
    wt_list = [1 / s**2 for s in sigma_i]   ## List of weights
    wt_sum  = sum(wt_list)                  ## Sum of weights
    wt_mu   = sum([x * wt for x, wt in zip(x_i,wt_list)]) / wt_sum

    ## uncertainty
    sigma_mu = sqrt(1/wt_sum)

    ## Chi Squared
    residuals = [wt_mu - x for x in x_i]
    chi_sq    = sum([res**2 * wt for res,wt in zip(residuals,wt_list)])

    ## Number of degrees of freedom
    N_DOF = len(x_i) - 1

    ## Probability
    prob =  stats.chi2.sf(chi_sq, N_DOF) # The chi2 probability given N degrees of freedom (Ndof)

    ## Printing
    if print_function:
        names  = ['Weighted mean','Uncertainty','Chi Squared','Number of Degrees of Freedom','Probability']
        values = [wt_mu, sigma_mu, chi_sq, N_DOF, prob]
        max_values = len(max([str(n) for n in values], key=len))
        max_names = len(max(names, key=len))
        extra_spacing = 2
        string = ""
        for name, value in zip(names, values):
            string += "{0:s} {1:>{spacing}} \n".format(name, value,
                       spacing = extra_spacing + max_values + max_names - len(name))
        print(string)

    return [wt_mu, sigma_mu, chi_sq, N_DOF, prob]
'''
Test
'''
if __name__ == '__main__':
    import numpy.random as r
    import numpy as np
    mu  = 8.3
    sig = 0.1
    N   = 10001
    printing = True

    x_i = r.normal(mu,sig,N)
    sigmas = np.ones(N)*sig
    #sigmas = r.random(N)*sig

    quick_maths(x_i,sigmas, printing)
