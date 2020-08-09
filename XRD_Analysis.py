import numpy as np
import matplotlib.pyplot as plt
import re
import zscan_fun 
import file_reading
from math import pi
from scipy.signal import argrelextrema 
import heapq 
from csaps import CubicSmoothingSpline
import XRD_fun

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

bragg_start_ind, bragg_end_ind = XRD_fun.find_bragg_peak(spec_q, diff_cps)

print((spec_q[bragg_start_ind], spec_q[bragg_end_ind]))
first_deriv = np.gradient(diff_cps, spec_q)
plt.plot(spec_q, np.log10(diff_cps))
plt.figure()
plt.plot(spec_q, first_deriv)
#plt.plot(linspace_q, d1)
plt.show()