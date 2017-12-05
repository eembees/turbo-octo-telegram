#!/usr/bin/env python

# --------------------------------------------------------- #
#  Simple python script to calculate g from pendulum data.
#
#  Author: Troels C. Petersen (Niels Bohr Institute)
#  Date:   16-11-2016
#
#  Run by: ./g_Pendulum.py
# --------------------------------------------------------- #

from ROOT import *        # Import ROOT libraries (to use ROOT)
import math               # Import MATH libraries (for extended MATH functions)
from array import array   # Import the concept of arrays (needed in TGraphErrors)

SavePlots = False         # Determining if plots are saved or not

# Statistics and fitting results:
gStyle.SetOptStat("emr")
gStyle.SetOptFit(1111)
gStyle.SetStatX(0.52);    # Position of top right corner.
gStyle.SetStatY(0.85);

# Used for text in plots:
text = TLatex()           # Define a text (to be put in plots)
text.SetNDC()             # Define all positions to be in a "unit canvas", i.e. [0,1]x[0,1]


# --------------------------------------------------------- #
# Read the data:
# --------------------------------------------------------- #

# Define four arrays containing count and time (with errors):
# They will be used to draw and fit a graph below!
countP  = array("f")
ecountP = array("f")
timeP   = array("f")
etimeP  = array("f")


# filename =
# Open the data file. The below lines may NOT read your data format,
# but should be modifiable to do so:
with open('data_Pendulum_example.txt', 'rU') as file:
    for line in file:
        line = line.strip()              # This removes all "codes" that may be put into the file.
        line = line.split()           # This splits the line at all ":", so that you now have
                                         # a list of numbers in "line", which you can choose from.

        # First entry is the counter, and third and fourth, minutes and seconds, so:
        countP.append(float(line[0]))    # Record the count
        ecountP.append(0.0)              # Set the error on the count to 0
        timeP.append(float(line[1]))     # Record the time (in seconds)
        etimeP.append(0.05)              # I GUESS the error on the time to be 0.05 second!
                                         # This of course has to be revisited and measured...

        # Always print to see, if this is reasonable:
        print "  Count number: %3.0f    time measurement (s): %5.2f"%(countP[-1], timeP[-1])


# --------------------------------------------------------- #
# Draw output:
# --------------------------------------------------------- #

canvasP = TCanvas( "canvasP", "canvasP", 50, 50, 1200, 600 )

graph_P = TGraphErrors(len(countP), countP, timeP, ecountP, etimeP)

fit_P = TF1("fit_P", "[0] + [1]*x", 0, len(countP)+1)     # A line as fitting function.
fit_P.SetParameters(0.0, 4.0)         # Set starting values of parameter [0] and [1] to 0 and 4.0
fit_P.SetLineColor(kRed)              # Set the line color to red.
fit_P.SetLineWidth(2)                 # Set the line width to 2.

graph_P.Fit("fit_P", "R")             # Make the fit with the range as set.
graph_P.Draw("AP")                    # Draw the axis and points of the graph.

text.SetTextSize(0.045)
text.DrawLatex(0.20, 0.15, "NOTE: Measurement uncertainty set to 0.05s by hand! Please adjust...")

canvasP.Update()
if (SavePlots):
    canvas.SaveAs("fit_Period.pdf")   # Save plot (format follow extension name)


raw_input('Press Enter to exit')
