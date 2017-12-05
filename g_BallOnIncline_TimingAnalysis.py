#!/usr/bin/env python

# ----------------------------------------------------------------------------------- #
#  Python macro for reading text (ASCII) file from LabView for ball rolling down incline,
#  extracking the times of ball passage (written to file) and producing plots.
#
#  The reason for this to be a separate program is the length of the execution time
#  for this process, which keeps the rest of the analysis from being ~instantaneous.
#
#  Author: Troels C. Petersen (petersen@nbi.dk),
#          Vojtech Pacik (vojtech.pacik@nbi.ku.dk)
#  Date:   16th of November 2017
# ----------------------------------------------------------------------------------- #

from __future__ import print_function, division
from glob import glob
import numpy as np                                      # Matlab like syntax for linear algebra and functions
import matplotlib.pyplot as plt                         # Plots and figures like you know them from Matlab
from iminuit import Minuit, describe, Struct
from probfit import BinnedLH, Chi2Regression, Extended  # Helper tool for fitting
from math import sqrt, cos, sin, tan, pi
from scipy import stats

from pend_functions import get_file_location



plt.close('all')                                        # To close all open figures



# ----------------------------------------------------------------------------------- #
# Input values & parameters & settings
# ----------------------------------------------------------------------------------- #

SavePlots = False        # For now, don't save plots (once you trust your code, switch on)
Verbose = 0#True           # For now, print a lot of output (once you trust your code, switch off)
Nverbose = 5             # But only print a lot for the first 5 entries




# ----------------------------------------------------------------------------------- #
def ProcessTimes( datafile = "", time_res=1.0/40000.0, verbose=True ) :
#
# Process a data file with measured times and voltages from gates, finding the position
# of the five peaks corresponding to ball passages.
# ----------------------------------------------------------------------------------- #

    # Make (empty) list for storing the values:
    volt = []
    time = []

    with open(datafile, "rU") as f:
        for i,line in enumerate(f) :      # Loop over lines in file
            line = line.strip()           # This removes all "codes" that may be put into the file.
            line = line.split()           # This splits the line at all spaces, and makes a list.

            time.append(float(line[0]))   # Measured time
            volt.append(float(line[1]))   # Corresponding voltage

            # Write out the first measurements (just a sanity check):
            if (verbose and i < Nverbose ) :
                print("  {0:2d}. events read:  t = {1:9.6f}   vol = {2:12.8f}".format(i, time[-1], volt[-1]))

    # Total number of voltage & times entries
    Npoints = len(time)
    print("  Number of entries in total: {0:6d}".format(Npoints))

    # Tranforming python list to numpy array for better performance
    np_volt = np.array(volt)
    np_time = np.array(time)

    t_min = np_time[0]     # first measured time
    t_max = np_time[-1]    # last measured time

    # Plotting voltage vs. time
    fig, ax = plt.subplots(figsize=(12,6))
    ax.scatter(np_time, np_volt, marker='.', color='blue', s=15)
    ax.set_title('Voltage vs. time')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Voltage [V]')
    plt.tight_layout()
    #plt.show(block=False)     # in terminal, continue code after showing figure
    if ( SavePlots ) :
        fig.savefig("figures/voltage_time_"+str(file[24:-4])+".pdf", dpi=600)
    plt.close()

    # Time step given by difference between two times:
    time_step = time[1] - time[0]
    print("  Time step: {0:6f}".format(time_step))


    # Getting time when the ball passes the middle of a gate:
    # -------------------------------------------------------
    # METHOD: For each passage, 4 anchor times are found given the voltage threshold level (thrs_level):
    #         Two at rising edge and two on falling edge:
    #           thrs_level above minimum \ below maximum measured voltage.
    # Then the time when ball passed the middle is estimated as arithmetic mean of these four anchor times.

    # Translating threshold levels for "anchor" points on raising and falling edge to voltage
    thrs_level = 0.1                    # This is just a choice! Test impact of variation (i.e. to 0.05, 0.2)!
    v_min = np.amin(np_volt)
    v_max = np.amax(np_volt)
    volt_range = v_max - v_min
    volt_thrs  = thrs_level * volt_range

    # Anchor voltage values:
    volt_thrs_high = v_max - volt_thrs
    volt_thrs_low = v_min + volt_thrs

    print("  Measured voltage range :\t {2:6f}\t min {0:6f}\t max {1:6f}".format(v_min,v_max,volt_range))
    print("  Threshold voltages (threshold level {2:1.2f}) :\t low {0:1.3f}\t high {1:1.3f}".format(volt_thrs_low,volt_thrs_high,thrs_level))

    # Lists of times for voltage anchors & ball passing times:
    time_anchor = []
    time_passing = []
    err_time_passing = []

    for entry in range(len(np_time)) :

        # Testing times on a rising voltage edge:
        # ---------------------------------------
        # First time above 'volt_thrs_low' limit
        if ( np_volt[entry] > volt_thrs_low and np_volt[entry-1] < volt_thrs_low ) :
            time_anchor.append(np_time[entry])
            continue

        # first time above 'volt_thrs_high' limit
        if ( np_volt[entry] > volt_thrs_high and np_volt[entry-1] < volt_thrs_high ) :
            time_anchor.append(float(np_time[entry]))
            continue

        # Testing times on a falling voltage edge:
        # ----------------------------------------
        # First time bellow 'volt_thrs_high' limit
        if ( np_volt[entry] < volt_thrs_high and np_volt[entry-1] > volt_thrs_high ) :
            time_anchor.append(float(np_time[entry]))
            continue

        # First time bellow 'volt_thrs_low' limit
        if ( np_volt[entry] < volt_thrs_low and np_volt[entry-1] > volt_thrs_low ) :
            time_anchor.append(float(np_time[entry]))

        # At this point we reached the end of one impuls (ball passed through)
        # and the time_anchor should have four entries:
        if ( len(time_anchor) == 4 ) :
            mu_t = (time_anchor[0] + time_anchor[1] + time_anchor[2] + time_anchor[3]) / 4.0
            err_mu_t = time_res               # This is the resolution, i.e. absolute minimum error
            time_passing.append(mu_t)
            err_time_passing.append(err_mu_t)
            print("    Passing time :\t {0:1.4f} +- {1:1.4f} s".format(mu_t, err_mu_t))

            # Clearing list of anchors for this impuls:
            del time_anchor[:]

            # Check if all 5 times are found (there is 5 gates). If so, exit the for loop:
            if ( len(time_passing) == 5) :
                if (verbose) :
                    print("    Found all 5 passing times for all 5 gates. Good! Any additional gates are ignored!")
                break

    # Returns the list of passing times and its uncertainty:
    return [ time_passing , err_time_passing ]




#----------------------------------------------------------------------------------
# Main body of the script
#----------------------------------------------------------------------------------

# List of input file names with voltages and times
# files = [   "data_Example/data_NormDir_MedBall1.txt",
#             "data_Example/data_RevDir_MedBall1.txt" ]

path = get_file_location()
files = glob(path + '/*')

# Loop over different datafiles
for file in files :
    print("\n ========== Processing file '{0:s}' =====================\n".format(file))
    time, err_time = ProcessTimes(file, verbose=Verbose)

    # Save the results into small data files:
    with open( str(file).replace('data','results')+"_SummaryTimes.dat", 'w' ) as file :
        for i in xrange( len(time) ) :
            file.write( "{0:9.6f} \t {1:9.6f} \n".format( time[i], err_time[i] ) )
        file.close()


# Hold script until you want to exit
raw_input( ' ... Press enter to exit ... ' )



# ----------------------------------------------------------------------------------- #
#
# Consideration:
# --------------
# Little intro:
#    Get a feel for the precision on the vol-measurement.
#    (They are in fact discrete with 1600 possible values per unit [0,1]).
#    Measure the uncertainty by plotting the distribution of "low" (or "high") level
#    measurements (i.e. before/between peaks), and look at the RMS. Is the guess good?
#
# Main analysis:
#    Consider the time series - where would you define the voltage at which the ball passes?
#    Does your final result depend on this definition? That would be an obvious systematic
#    uncertainty!
#
# Suggestion:
#    Since this program provides the crossing times for the ball, and also how they
#    change with your definition of crossing, it might be a good idea to include the
#    subsequent calculations/analysis in the program as well (as has already been
#    indicated).
#
# Conclusion:
#    Since the timing uncertainty can be argued to be small, one can deside to disregard
#    it. However, it would be clever to repeat the rolls a few times, just to see the
#    variation in the results, now with the time measurement as the only non-constant
#    input (of course the execution/fallout of the experiment may also change!).
#
# ----------------------------------------------------------------------------------- #
