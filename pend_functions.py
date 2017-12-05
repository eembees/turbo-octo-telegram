## functions.py
## by Magnus Berg Sletfjerding
###############################
'''
Importing all packages needed for functions to work
'''
from __future__ import division

import os
from glob import glob
import string
import numpy as np
from scipy.optimize import curve_fit

from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import tkFileDialog
from tkFileDialog import askopenfile     # Open dialog box

from quick_maths import quick_maths

'''
File management
'''
def get_file_name():
    root = Tk()
    root.withdraw()     # Withdraw the empty dialog box
    root.filename = tkFileDialog.askopenfilename(initialdir = os.getcwd(),
                                                title = "Select file",)
    return(root.filename)

def get_file_location():
    file_found = get_file_name()
    dirpath = os.path.dirname(file_found)
    return dirpath

'''
Errors
'''
def get_sigmas(array, sigmas):
    return np.ones(len(array))*sigmas


'''
Printing and saving
'''
def nice_string_output(names, values, extra_spacing = 2):
    max_values = len(max(values, key=len))
    max_names = len(max(names, key=len))
    string = ""
    for name, value in zip(names, values):
        string += "{0:s} {1:>{spacing}} \n".format(name, value,
                   spacing = extra_spacing + max_values + max_names - len(name))
    return string[:-2]

def pend_save_rms(fname, mu, rms, resi):
    ## Starts by making sure right dir used
    if 'data' in fname:
        fname = fname.replace('data','results')
    if fname.endswith('.dat'):
        fname = fname.replace('.dat','.txt')
    ## Open
    with open(fname, 'w') as f:
        print fname
        f.write('Mean ' + str(mu) + '\n')
        f.write('RMS: ' + str(rms) + '\n')
        for i in resi:
            f.write(str(i) + '\n')
    pass


'''
Period
'''
def pend_get_periods(filename):
    ## gets periods out of the file specified
    ## takes difference between each time, then adds it to the next using np.roll
    raw       = np.loadtxt(filename)
    raw_time  = np.array([el[1] for el in raw])
    time_diff = np.ediff1d(raw_time)
    period_ts = time_diff + np.roll(time_diff,1)
    return period_ts

def pend_get_periods_least_sq(filename):
    raw       = np.loadtxt(filename)
    raw_count = np.array([el[0] for el in raw])
    raw_time  = np.array([el[1] for el in raw])
    raw_half  = raw_count / 2
    def pfunc(x, a, b):
        return a * x + b
    popt, pcov = curve_fit(pfunc, raw_half, raw_time)
    perr = np.sqrt(np.diag(pcov))

    return popt, perr

def pend_split_periods(periods):
    ## Taking time and returning period for all experiments combined
    flat_set_1 = periods[0::2]
    flat_set_2 = periods[1::2]
    return flat_set_1,flat_set_2


'''
calculate g
'''

def pend_calc_g(length, sigma_length, period, sigma_period):
    g       = length*(2*np.pi/period)**2
    sigma_g_sq = (2*np.pi/length)**4 * sigma_length + \
                 (-2*length*((2*np.pi)**2)*length**3)**2 * sigma_period

    return g, sigma_g_sq
