#this script should import data from the experiment (both measured by hand and
# from the incline measurement tool) and return acceleration and

import iminuit
import probfit
import numpy as np
from glob import glob
from quick_maths import quick_maths
import glob

#files = glob('./data/*.dat')

#for f in files:

#    array=np.loadtxt(f)
#    print array


# Manual measurements:
# all measurements [[measure],[uncert]]

diam_ball_1 = [[14.9,15.0,14.98,15.1,15.0],[0.05,0.05,0.08,0.2,0.1]]
diam_ball_2 = [[10.9,10.2,10.9,11.0,11.0],[0.1,0.4,0.05,0.05,0.05]]

rail_width = [[6.0,6.1,6.0,6.0,6.1],[0.05,0.05,0.05,0.1,0.08]]

#angles

angle_b4flip_b4turn = [[83.5,82.9,83.1,83.0,83.4],[1.0,0.3,0.2,0.5,0.3]]
angle_b4flip_turnd = [[83.0,83.2,83.5,83.5,83.2],[0.2,0.3,0.2,0.5,0.3]]

angle_flipd_b4turn = [[84.9,85.0,85.2,85.1,84.7],[0.5,0.5,0.3,0.2,0.5]]
angle_flipd_turnd = [[82.7,83.5,82.5,82.5,82.9],[0.5,0.5,0.3,0.2,0.5]]

# rail distances

d_start = [[99.5,99.8,99.5,99.7,99.5],[0.5,0.2,0.5,0.3,0.3]]
d_p1 = [[230.5,230.0,229.0,230.5,230.0],[0.5,0.2,0.5,0.3,0.2]]
d_p2 = [[378.5,378.2,378.5,378.4,378.0],[0.5,0.2,0.5,0.3,0.5]]
d_p3 = [[537.0,536.8,537.0,536.6,537.7],[0.5,0.2,0.5,0.3,0.5]]
d_p4 = [[704.5,704.6,704.5,704.8,704.7],[0.5,0.2,0.5,0.3,0.2]]
d_p5 = [[882.5,882.2,882.5,882.9,882.8],[0.5,0.2,0.5,0.3,0.2]]

#list of lists for easier coding

listlist = [diam_ball_1,diam_ball_2,rail_width,angle_b4flip_b4turn,angle_b4flip_turnd,angle_flipd_b4turn,angle_flipd_turnd,d_start,d_p1,d_p2,d_p3,d_p4,d_p5]





# stats [mu,sigma,chi_square,n_deg_of_freedom,prob] from Magnus

stats_diam_ball1 = quick_maths(listlist[0][0],listlist[0][1])
stats_diam_ball2 = quick_maths(listlist[1][0],listlist[1][1])

stats_rail_width = quick_maths(listlist[2][0],listlist[2][1])

stats_angle_b4flip_b4turn = quick_maths(listlist[3][0],listlist[3][1])
stats_angle_b4flip_turnd = quick_maths(listlist[4][0],listlist[4][1])
stats_angle_flipd_b4turn = quick_maths(listlist[5][0],listlist[5][1])
stats_angle_flipd_turnd = quick_maths(listlist[6][0],listlist[6][1])

stats_d_start = quick_maths(listlist[7][0],listlist[7][1])
stats_d_p1 = quick_maths(listlist[8][0],listlist[8][1])
stats_d_p2 = quick_maths(listlist[9][0],listlist[9][1])
stats_d_p3 = quick_maths(listlist[10][0],listlist[10][1])
stats_d_p4 = quick_maths(listlist[11][0],listlist[11][1])
stats_d_p5 = quick_maths(listlist[12][0],listlist[12][1])

stats_list = []

stats_list.append(stats_diam_ball1)
stats_list.append(stats_diam_ball2)
stats_list.append(stats_rail_width)
stats_list.append(stats_angle_b4flip_b4turn)
stats_list.append(stats_angle_b4flip_turnd)
stats_list.append(stats_angle_flipd_b4turn)
stats_list.append(stats_angle_flipd_turnd)
stats_list.append(stats_d_start)
stats_list.append(stats_d_p1)
stats_list.append(stats_d_p2)
stats_list.append(stats_d_p3)
stats_list.append(stats_d_p4)
stats_list.append(stats_d_p5)


print(stats_list)


#print(stats_d_p5)
