import numpy as np
import matplotlib.pyplot as plt
from csaps import CubicSmoothingSpline
from scipy.signal import argrelextrema 
from math import pi
import re
import zscan_fun 
import file_reading

#user_lambda = input("Enter lambda ")
#B = input("Enter sample length ")
user_lambda = 1.54184 
B = 10

#zscan = open('Smartlab data/ZscanSTBXRR_0014_Scan2020Jan24-124745.dat', 'r')
#xrr_spec = open('Smartlab data/spec2Pt111_Al2O3_006_1.dat', 'r')
#xrr_bkg = open('Smartlab data/bkg2Pt111_Al2O3_006.dat', 'r')
# not sure if this is the right set of files lol 
# it's not hehe

zscan = open('ATXG data/Zscan.dat', 'r')
xrr_spec = open('ATXG data/spec_XRR.dat', 'r')
xrr_bkg = open('ATXG data/BKG_XRR.dat', 'r')

#zscan = open('Smartlab data/Zscan_0007_Scan2020Jan23-191605.dat', 'r')
#zscan = open('Zscan_1.DAT', 'r')
#zscan = open('Zscan_2.DAT', 'r')
#zscan = open('Zscan_XRR_0009_Scan2020Feb07-220747.DAT', 'r')

# read files into lists, turn lists into numpy matrices
zscan_z, zscan_cps = file_reading.pull_data(zscan)
spec_theta, spec_cps = file_reading.pull_data(xrr_spec)
bkg_theta, bkg_cps = file_reading.pull_data(xrr_bkg)      

#get the effective beam height, z locations where linear drop starts and ends, STB intensity 
z_val_1, z_val_2, effective_beam_height = zscan_fun.eff_beam_height(zscan_z, zscan_cps)
stb_inten = zscan_fun.STB_intensity(zscan_z, zscan_cps, min(z_val_1, z_val_2))
print(effective_beam_height)
print(stb_inten)

#plot z vs cps 
plt.plot(zscan_z, zscan_cps)
plt.xlabel("z (mm)")
plt.ylabel("cps")
plt.title("zscan")

#still need: beautify graph, test effective beam height with
#multiple files, make sure edge cases are covered, tuple never has more 
#than one value, etc 

#Specular & background 
spec_q = 4 * pi * np.sin(np.deg2rad(spec_theta / 2)) / user_lambda
bkg_q = 4 * pi * np.sin(np.deg2rad(bkg_theta / 2)) / user_lambda
diff_cps = spec_cps - bkg_cps

#Geometrical correction
gc_cps = (effective_beam_height / ( B * np.sin(np.deg2rad(spec_theta /  2)))) * diff_cps

plt.figure()
#plt.plot(spec_q, np.log10(spec_cps))
#plt.plot(bkg_q, np.log10(bkg_cps))

plt.plot(spec_q, np.log10(diff_cps))
#spec q and bkg q should be the same right? 
plt.plot(spec_q, np.log10(gc_cps))

highest_cps = np.maximum(diff_cps, gc_cps)
plt.plot(spec_q, np.log10(highest_cps))

norm_inten = highest_cps / stb_inten

plt.figure()
plt.plot(spec_q, np.log10(norm_inten))
plt.show()

#naming convention 
#f = open("insert_name_here", "w")
#for 
#ya anyway write to file