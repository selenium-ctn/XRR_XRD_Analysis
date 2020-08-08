import numpy as np
import matplotlib.pyplot as plt
import re
import zscan_fun 
import file_reading
from math import pi
from scipy.signal import argrelextrema 
import heapq 
from csaps import CubicSmoothingSpline

#user_lambda = input("Enter lambda (Angstroms) ")
user_lambda = 1.54184 

zscan = open('Smartlab data/ZscanSTBXRR_0014_Scan2020Jan24-124745.dat', 'r')
xrr_spec = open('Smartlab data/spec2Pt111_Al2O3_006_1.dat', 'r')
xrr_bkg = open('Smartlab data/bkg2Pt111_Al2O3_006.dat', 'r')
#right set of data? Who knows lolol 

# read files into lists, turn lists into numpy matrices
zscan_z, zscan_cps = file_reading.pull_data(zscan)
spec_theta, spec_cps = file_reading.pull_data(xrr_spec)
bkg_theta, bkg_cps = file_reading.pull_data(xrr_bkg)  

#get the effective beam height, z locations where linear drop starts and ends, STB intensity 
z_val_1, z_val_2, effective_beam_height = zscan_fun.eff_beam_height(zscan_z, zscan_cps)
stb_inten = zscan_fun.STB_intensity(zscan_z, zscan_cps, min(z_val_1, z_val_2))

#Specular & background 
spec_q = 4 * pi * np.sin(np.deg2rad(spec_theta / 2)) / user_lambda
bkg_q = 4 * pi * np.sin(np.deg2rad(bkg_theta / 2)) / user_lambda
diff_cps = spec_cps - bkg_cps
norm_reflectivity = diff_cps / stb_inten

first_deriv = np.gradient(diff_cps, spec_q)
#min_pos_d1 = first_deriv.argmin()

loc_min_pos_d1 = argrelextrema(first_deriv, np.less)
loc_min_pos_d1, = loc_min_pos_d1
loc_min_val_d1 = first_deriv[loc_min_pos_d1]

d1_2_smallest = heapq.nsmallest(2, loc_min_val_d1)
d1_min_pos = np.where( loc_min_val_d1 == d1_2_smallest[0])
d1_min_pos = loc_min_pos_d1[d1_min_pos]
d1_2_min_pos = np.where(loc_min_val_d1 == d1_2_smallest[1])
d1_2_min_pos = loc_min_pos_d1[d1_2_min_pos]

curr_index = d1_min_pos
curr_val = first_deriv[d1_min_pos]
while curr_val <= 0:
    curr_index = curr_index + 1
    curr_val = first_deriv[curr_index]

end_ind_d1_min_1 = curr_index - 1

curr_index = d1_2_min_pos
curr_val = first_deriv[d1_2_min_pos]
while curr_val <= 0:
    curr_index = curr_index + 1
    curr_val = first_deriv[curr_index]

end_ind_d1_min_2 = curr_index - 1

print([spec_q[end_ind_d1_min_1], spec_q[end_ind_d1_min_2]])

loc_max_pos_d1 = argrelextrema(first_deriv, np.greater)
loc_max_pos_d1, = loc_max_pos_d1
loc_max_val_d1 = first_deriv[loc_max_pos_d1]

d1_2_largest = heapq.nlargest(2, loc_max_val_d1)
d1_max_pos = np.where( loc_max_val_d1 == d1_2_largest[0])
d1_max_pos = loc_max_pos_d1[d1_max_pos]
d1_2_max_pos = np.where(loc_max_val_d1 == d1_2_largest[1])
d1_2_max_pos = loc_max_pos_d1[d1_2_max_pos]

curr_index = d1_max_pos
curr_val = first_deriv[d1_max_pos]
while curr_val >= 0:
    curr_index = curr_index - 1
    curr_val = first_deriv[curr_index]

end_ind_d1_max_1 = curr_index + 1

curr_index = d1_2_max_pos
curr_val = first_deriv[d1_2_max_pos]
while curr_val >= 0:
    curr_index = curr_index - 1
    curr_val = first_deriv[curr_index]

end_ind_d1_max_2 = curr_index + 1

print([spec_q[end_ind_d1_max_1], spec_q[end_ind_d1_max_2]])

plt.plot(spec_q, np.log10(diff_cps))
plt.figure()
plt.plot(spec_q, first_deriv)
#plt.plot(linspace_q, d1)
plt.show()