#!/usr/bin/env python

# ----------------------------------------------------------------------------------- #
#  Simple stopwatch macro, writing result into a file (to be read by analysis program)
#
#  Author: Troels C. Petersen (Niels Bohr Institute)
#  Date:   25-11-2016
#
# ----------------------------------------------------------------------------------- #

from time import time

with open("timer_output.dat", "w") as outfile : 
    now = time()
    laptime = 0.0
    counter = 0
    while( raw_input( "%4d \t %10.4f \t Laptime by enter, Exit by key+enter \t"%(counter, laptime) ) is "" ) : 
        counter += 1
        laptime = time()-now
        outfile.write("%4d \t %10.4f \n"%(counter, laptime))
