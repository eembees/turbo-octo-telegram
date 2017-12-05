import os
from glob import glob
import numpy as np
import string
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import tkFileDialog
from tkFileDialog import askopenfile     # Open dialog box

def get_file_name():
    root = Tk()
    root.filename = tkFileDialog.askopenfilename(initialdir = os.getcwd(),
                                                title = "Select file",)
    return(root.filename)

def getrms(array):
    N = float(len(array))
    mean = sum(array)/N
    resi = [x - mean for x in array]
    rms  = sum([x**2 for x in resi])/N
    return mean, rms, resi

def save_rms(fname, mu, rms, resi):
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


if __name__ == '__main__':
    save_rms = 1
    dir_to_save = './results/pend/'

    # file_to_use = get_file_name()
    filenames = glob('./data/pend/*')
    for file_to_use in filenames:
        print(file_to_use, type(file_to_use))

        raw       = np.loadtxt(file_to_use)
        raw_time  = np.array([el[1] for el in raw])
        time_diff = np.ediff1d(raw_time)

        mu, rms, resi = getrms(time_diff)

        if save_rms:
            name_to_save = file_to_use.replace('.dat','').replace('./data/pend/','')
            file_to_save = dir_to_save + name_to_save + '_rms.txt'
            with open(file_to_save, 'w') as f:
                print file_to_save
                f.write('Mean ' + str(mu) + '\n')
                f.write('RMS: ' + str(rms) + '\n')
                for i in resi:
                    f.write(str(i) + '\n')
