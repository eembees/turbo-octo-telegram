#!/usr/bin/env python

# ----------------------------------------------------------------------------------- #
#
#  ROOT macro for reading text (ASCII) file from LabView for ball rolling down incline.
#
#  Author: Troels C. Petersen (NBI)
#  Email:  petersen@nbi.dk
#  Date:   16th of November 2016
#
# ----------------------------------------------------------------------------------- #

from ROOT import *
import math


# ----------------------------------------------------------------------------------- #
# Define a small simple function:
def sqr( a ) : return a*a
# ----------------------------------------------------------------------------------- #

# Setting of general plotting style:
gStyle.SetCanvasColor(0)
gStyle.SetFillColor(0)

# Setting what to be shown in statistics box:
gStyle.SetOptStat("e")
gStyle.SetOptFit(1111)


SavePlots = False

# Set constants and define variables and histograms:
Nevents    = 0
lowhigh    = 0       # To begin with, the voltage (vol) is low (i.e. no ball passing!)
limit_vol  = 0.0     # Define SOME LEVEL (your choice!) at which "the ball passes"
dt = 1.0 / 40000.0   # The time between measurements (for 40 kHz running)

# Make (empty) lists for the time and voltage measurements:
t = []
vol = []


#---------------------------------------------------------------------------------- 
# File to read:
#---------------------------------------------------------------------------------- 

with open("data_RollingBall_example.txt", "rU") as file : 
    for ievent, line in enumerate(file) :         # Loop over lines in file
        line = line.strip()           # This removes all "codes" that may be put into the file.
        line = line.split()           # This splits the line at all spaces, and makes a list.
        t.append(float(line[0]))      # Measured time (s)
        vol.append(float(line[1]))    # Measured voltage (V)
        Nevents = ievent              # Note the last entry's number

        # Register when the voltage rises and falls:
        # ------------------------------------------
        # Put your own code here...

        # Write out the first 10 measurements:
        if ievent < 10 : print"  %2d. events read:  t = %9.6f   vol = %12.8f"%(ievent, t[-1], vol[-1])

    print "  Number of entries in total: %6d \n"%Nevents


#---------------------------------------------------------------------------------- 
# Define and fill histograms:
#---------------------------------------------------------------------------------- 

t_min = 0.0
t_max = dt * float(Nevents-1)

# The voltage happens to be measured on a "strange" scale, carefully included in the histogram definition:
Hist_vol  = TH1F("Hist_vol" , "Hist_vol;Voltage (arbitrary scale);Number of entries", 6400, 0.0, 4.0)

# Define the histogram to include all data:
Hist_tvol = TH1F("Hist_tvol", "Hist_tvol;time (s);Voltage (V)", Nevents+1, t_min-dt/2, t_max+dt/2)

for ievent in xrange(len(vol)) :
    Hist_vol.Fill(vol[ievent])                        # Voltage measured.
    Hist_tvol.SetBinContent(ievent+1, vol[ievent])    # Voltage measured vs. time.
    Hist_tvol.SetBinError(ievent+1, 0.002)            # Voltage uncertainty on that measurement.
                                                      # Note that bin 0 is the "underflow" bin!


#---------------------------------------------------------------------------------- 
# Fit and Plot:
#---------------------------------------------------------------------------------- 

# Draw the voltage distribution (to see the precision and to define "low" and "high" voltage):
c0 = TCanvas("c0", "", 50, 20, 600, 400)

Hist_vol.GetXaxis().SetRangeUser(0.225, 0.245)   # Zoom in on the "low voltage" part.
fitGauss = TF1("fitGauss", "gaus", 0.23, 0.24)   # Gaussian fit (NOTE: range).
fitGauss.SetLineColor(4)
fitGauss.SetLineWidth(2)
Hist_vol.Fit("fitGauss", "RL")
Hist_vol.Draw()

c0.Update()
if (SavePlots) : c1.SaveAs("Fig_RollingBall_VoltageDistribution.pdf")


#---------------------------------------------------------------------------------- 

gStyle.SetStatX(0.32);    # Position of top right corner.
gStyle.SetStatY(0.85);

# Drawing time series:
c1 = TCanvas("c1", "", 100, 50, 1200, 500)
Hist_tvol.Draw()

c1.Update()
if (SavePlots) : c1.SaveAs("Fig_RollingBall_TimeSeries.pdf")


#---------------------------------------------------------------------------------- 
# Your analysis here:
#---------------------------------------------------------------------------------- 

# Lots of code and calculations...


g      = 9.8   # Get your own number!
stat_g = 0.1
syst_g = 0.1

print "  Result: g = %6.4f +- %6.4f (stat) +- %6.4f (syst) m/s^-2"%(g, stat_g, syst_g)

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
# ----------------------------------------------------------------------------------- #
