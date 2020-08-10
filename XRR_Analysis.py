import numpy as np
import matplotlib.pyplot as plt
from csaps import CubicSmoothingSpline
from scipy.signal import argrelextrema 
from math import pi
import re
import zscan_fun 
import file_reading
from scipy.stats import linregress

#ask user for input values 
#user_lambda = input("Enter lambda (Angstroms) ")
#B = input("Enter sample length (mm) ")
#step_size = input("Enter step size (deg/step) ")
#scan_speed = input("Enter scan speed (deg/min) ")
#sample_name = input("Enter sample name ")
 
sample_name = "testing"
step_size = .02
scan_speed = .25
user_lambda = 1.54184 
B = 10

#open files 
zscan = open('ATXG data/Zscan.dat', 'r')
xrr_spec = open('ATXG data/spec_XRR.dat', 'r')
xrr_bkg = open('ATXG data/BKG_XRR.dat', 'r')

#zscan = open('Smartlab data/Zscan_0007_Scan2020Jan23-191605.dat', 'r')
#zscan = open('Zscan_1.DAT', 'r')
#zscan = open('Zscan_2.DAT', 'r')
#zscan = open('Zscan_XRR_0009_Scan2020Feb07-220747.DAT', 'r')

#read files into lists, turn lists into numpy matrices
zscan_z, zscan_cps = file_reading.pull_data(zscan)
spec_theta, spec_cps = file_reading.pull_data(xrr_spec)
bkg_theta, bkg_cps = file_reading.pull_data(xrr_bkg)  

#apply filter if necessary 
zscan_cps = zscan_cps * 770.53
#mult for zscan only!!! maybe don't worry...maybe do....tell user to use automatic filter or nah....

#get the effective beam height, z locations where linear drop starts and ends, STB intensity 
stb_inten, effective_beam_height = zscan_fun.stb_intensity_and_eff_beam_height(zscan_z, zscan_cps)
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

norm_reflectivity = highest_cps / stb_inten
error_bars = np.sqrt((spec_cps * step_size * 60 / scan_speed) + (bkg_cps * step_size * 60 / scan_speed)) / stb_inten
print(error_bars)

plt.figure()
plt.plot(spec_q, np.log10(norm_reflectivity))
plt.xlabel("q (Angstroms)")
plt.ylabel("Reflectivity")
plt.title("q vs normalized intensity")
plt.figure()
plt.errorbar(spec_q[5:], np.log10(norm_reflectivity[5:]), yerr=np.log10(error_bars[5:]))
#plt.errorbar(spec_q[5:], (norm_reflectivity[5:]), yerr=error_bars[5:])
#plt.xlabel("q (Angstroms)")
#plt.ylabel("Reflectivity")
#plt.title("q vs normalized intensity")
plt.show()

norm_reflectivity = norm_reflectivity[4:]
renorm_reflect = norm_reflectivity / np.amax(norm_reflectivity)
dq = .00778 
renorm_reflect_error = renorm_reflect * .05 

#naming convention 
#f = open("insert_name_here", "w")
#for 
#ya anyway write to file

#f = open("%s_XRR.txt" % (sample_name), "x")
#for (q, r, er) in zip(spec_q[4:], renorm_reflect, renorm_reflect_error):
#    f.write('{0} {1} {2} {3}\n'.format(q, r, er, dq))
#f.close()
