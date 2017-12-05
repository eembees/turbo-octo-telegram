#!/usr/bin/env python

# --------------------------------------------------------- #
#  Python/ROOT script to fit and illustrate period measurement.
#   
#  Author: Troels C. Petersen (Niels Bohr Institute)
#  Date:   25-11-2015
# --------------------------------------------------------- #

from ROOT import *        # Import ROOT libraries (to use ROOT)
import math               # Import MATH libraries (for extended MATH functions)
from array import array   # Import the concept of arrays (needed in TGraphErrors)

Blinding  = True          # Determining if random offset is added to result for blinding
SavePlots = False         # Determining if plots are saved or not

gStyle.SetOptStat("")
gStyle.SetOptFit(0)
# gStyle.SetStatFormat("8.6g");

gStyle.SetStatX(0.49)
gStyle.SetStatY(0.88)

# Text to write on the plot:
text = TLatex()
text.SetNDC()
text.SetTextFont(72)
text.SetTextColor(1)




# --------------------------------------------------------- #
# Draw output - simulated example measurements:
# --------------------------------------------------------- #

count  = array("f")
ecount = array("f")
time   = array("f")
etime  = array("f")
timeres  = array("f")
etimeres = array("f")

with open('data_Pendulum_example.txt', 'r') as file:
    for line in file:
        line = line.strip()
        line = line.split()

        count.append(float(line[0]))    # Record the count
        ecount.append(0.0)              # Set the error on the count to 0
        time.append(float(line[1]))     # Record the time (in seconds)
        etime.append(0.05)              # I GUESS the error on the time to be 0.05 second!
                                        # This of course has to be revisited and measured...
        print "  Count number: %3.0f    time measurement (s): %5.2f"%(count[-1], time[-1])

# The estimated error "etime" can first be set to "an estimate", and from the result of
# running this macro the first time, you can set this correctly, and rerun it!

maxx = float(len(count)+1)  # Make the plot a little beyond the number of points!
miny = -18.0
maxy =  65.0
canvas = TCanvas( "canvas", "canvas", 50, 50, 900, 600 )
canvas.DrawFrame(0.0, miny, 26.0, maxy)
graph_time = TGraphErrors(len(count), count, time, ecount, etime)
graph_time.GetXaxis().SetRangeUser(0.0, maxx)
graph_time.GetYaxis().SetRangeUser(miny, maxy)
graph_time.SetTitle("")
graph_time.GetXaxis().SetTitle("Measurement number")
graph_time.GetYaxis().SetTitle("Time elapsed (s)")
graph_time.SetMarkerStyle(20)
graph_time.SetMarkerSize(0.8)

# Fit the data to a line, and get the period from the slope:
fit_time = TF1("fit_time", "[0] + [1]*x", 0.5, len(count)+0.5)
fit_time.SetParameters(0.0, 7.0)
fit_time.SetParNames("Offset (s)", "Period (s)")
fit_time.SetLineColor(kRed)
fit_time.SetLineWidth(2)
graph_time.Fit("fit_time", "R")
print

# Find the residuals, and display them on the same graph with scale on right side.
# Scale values and errors up by factor, to match new scale (i.e. be visible):
factor = 50.0        # OK, so we scale up the residuals by a factor 100, and put an axis
                      # with a scale of 200 smaller on the right side of the plot.

hist_timeres = TH1F("hist_timeres", "", 15, -0.30, 0.30)
for i in range (0, len(count)) :
    timeres.append(factor * (time[i] - fit_time.Eval(count[i])))
    etimeres.append(factor * etime[i])
    hist_timeres.Fill(timeres[-1]/factor)
    print "  %2d:  count %2d   t = %6.2f     t_fit = %6.2f     t_resi = %4.2f += %4.2f "%(i, count[i], time[i],  fit_time.Eval(count[i]), timeres[-1], etimeres[-1])

graph_timeres = TGraphErrors(len(count), count, timeres, ecount, etimeres)
graph_timeres.SetLineColor(kBlue)
graph_timeres.SetLineWidth(2)
graph_timeres.SetMarkerStyle(20)
graph_timeres.SetMarkerSize(0.8)

graph_time.Draw("AP same")
graph_timeres.Draw("P same")



# Draw an axis on the right side (scaled by "factor"):
min = -0.30
max =  0.30
axis = TGaxis(maxx, min*factor, maxx, max*factor, min, max, 510, "+L");
# axis.SetTitle("Time residual (s)")
axis.SetTitleOffset(1.3)
axis.SetTitleColor(kBlue)
axis.CenterTitle()
axis.SetLineColor(kBlue);
axis.SetLineWidth(2);
axis.SetLabelColor(kBlue);
axis.Draw();

# Draw a line a zero for the residuals:
line = TLine(0.0, 0.0, maxx, 0.0)
line.Draw()

# Text:
text.SetTextSize(0.030)
text.DrawLatex(0.14, 0.85, "Result of the fit:")
text.SetTextSize(0.045)
text.DrawLatex(0.14, 0.80, "Offset = %6.4f #pm %6.4f s"%(fit_time.GetParameter(0), fit_time.GetParError(0)))
text.SetTextColor(kRed)
text.DrawLatex(0.14, 0.75, "Period = %6.4f #pm %6.4f s"%(fit_time.GetParameter(1), fit_time.GetParError(1)))

text.SetTextColor(kBlack)
text.SetTextSize(0.030)
text.DrawLatex(0.14, 0.69, "Uncertainty on time measurements")
text.DrawLatex(0.14, 0.66, "obtained from RMS of residuals")
# text.SetTextSize(0.045)
# text.DrawLatex(0.14, 0.60, "#sigma(t) = 0.06 s")


text.SetTextSize(0.04)
text.SetTextColor(kRed)
text.DrawLatex(0.54, 0.84, "Time measurements (s)")

text.SetTextSize(0.04)
text.SetTextColor(kBlue)
text.DrawLatex(0.67, 0.15, "Time residuals (s)")

text.SetTextSize(0.022)
text.SetTextColor(kBlack)
text.DrawLatex(0.68, 0.675, "Distribution of time residuals")


# Draw histogram in its on pad:
pad = TPad("pad", "", 0.65, 0.35, 0.89, 0.67, 0, 0, 0);
pad.SetTopMargin(0.0);
pad.SetLineColor(0);
pad.SetFillColor(0);
pad.GetFrame().SetFillColor(0);
pad.GetFrame().SetBorderSize(0);
pad.GetFrame().SetLineColor(kWhite);
pad.Draw();
pad.cd(); 

fit_timeres = TF1("fit_timeres", "gaus", -0.25, 0.25)
hist_timeres.Fit("fit_timeres", "RL")
hist_timeres.GetXaxis().SetTitle("Time residual (s)")
hist_timeres.GetYaxis().SetTitle("Frequency")
hist_timeres.Draw("e")

canvas.Update()
if (SavePlots):
    canvas.SaveAs("fit_period.pdf")


# --------------------------------------------------------- #
raw_input('Press Enter to exit')
