import numpy as np

from quick_maths import quick_maths

# Set data
angle_b4flip_b4turn = [[83.5,82.9,83.1,83.0,83.4],[1.0,0.3,0.2,0.5,0.3]]
angle_b4flip_turnd = [[83.0,83.2,83.5,83.5,83.2],[0.2,0.3,0.2,0.5,0.3]]

angle_flipd_b4turn = [[84.9,85.0,85.2,85.1,84.7],[0.5,0.5,0.3,0.2,0.5]]
angle_flipd_turnd = [[82.7,83.5,82.5,82.5,82.9],[0.5,0.5,0.3,0.2,0.5]]


mu_angle_preflip_preturn, sigma_angle_preflip_preturn, _, _, _, = quick_maths(angle_b4flip_b4turn[0], angle_b4flip_b4turn[1],1)
mu_angle_preflip_posturn, sigma_angle_preflip_postturn, _, _, _, = quick_maths(angle_b4flip_turnd[0], angle_b4flip_turnd[1],1)

mu_angle_preflip = (mu_angle_preflip_posturn + mu_angle_preflip_preturn) / 2.
print('Average of angles before flip = {} degrees'.format(mu_angle_preflip))

mu_angle_postflip_preturn, sigma_angle_postflip_preturn, _, _, _, = quick_maths(angle_flipd_b4turn[0],angle_flipd_b4turn[1],1)
mu_angle_postflip_posturn, sigma_angle_postflip_posturn, _, _, _, = quick_maths(angle_flipd_turnd[0],angle_flipd_turnd[1],1)

mu_angle_postflip = (mu_angle_postflip_posturn + mu_angle_postflip_preturn) / 2.
print('Average of angles after flip = {} degrees'.format(mu_angle_postflip))

delta_angle = (mu_angle_preflip - mu_angle_postflip) / 2.
print('Delta of angles after flip = {} degrees'.format(delta_angle))

print('relative uncertainty is {}'.format(abs(delta_angle/((mu_angle_preflip+mu_angle_postflip)/2))))
