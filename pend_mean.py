import numpy as np
from glob import glob
from quick_maths import quick_maths


def pend_mean(files,sigmas,printing=False):
    if len(files)==1:
        ## Method one: Taking time and returning results for each individual experiment
        with files[0] as i:
            raw       = np.loadtxt(i)
            raw_time  = np.array([el[1] for el in raw])
            time_diff = np.ediff1d(raw_time)

        sigmas = np.ones(len(time_diff))*sigmas
        wt_mu, sigma_mu, chi_sq, N_DOF, prob = quick_maths(time_diff, sigmas, printing)
    else:
        ## Method two: Taking time and returning for all experiments
        all_time = []
        for i in files:
            raw       = np.loadtxt(i)
            raw_time  = np.array([el[1] for el in raw])
            time_diff = np.ediff1d(raw_time)

            all_time.append(time_diff)

        flat_time = [item for sublist in all_time for item in sublist]
        all_sigmas = np.ones(len(flat_time))*sigmas
        wt_mu, sigma_mu, chi_sq, N_DOF, prob = quick_maths(flat_time, all_sigmas, printing)
    return(wt_mu, sigma_mu, chi_sq, N_DOF, prob)



if __name__ == '__main__':
    ## variables
    sigmas = 0.07  #0.06977244  # 0.07 -> ~50% prob
    filenames = glob('./data/pend/*')

    m,s,chisq,dof,prob = pend_mean(filenames,sigmas, printing=True)

    # print('{0:.64f}'.format(prob))
