import numpy as np
import matplotlib.pyplot as plt
from csaps import CubicSmoothingSpline
from scipy.signal import argrelextrema 
import zscan_fun 
from math import pi

#user_lambda = input("Enter lambda ")
#B = input("Enter sample length ")
user_lambda = 1.54184 
B = 10

#zscan = open('Smartlab data/ZscanSTBXRR_0014_Scan2020Jan24-124745.dat', 'r')
#xrr_spec = open('Smartlab data/spec2Pt111_Al2O3_006_1.dat', 'r')
#xrr_bkg = open('Smartlab data/bkg2Pt111_Al2O3_006.dat', 'r')
# not sure if this is the right set of files lol 

zscan = open('ATXG data/Zscan.dat', 'r')
xrr_spec = open('ATXG data/spec_XRR.dat', 'r')
xrr_bkg = open('ATXG data/BKG_XRR.dat', 'r')

#zscan = open('Smartlab data/Zscan_0007_Scan2020Jan23-191605.dat', 'r')
#zscan = open('Zscan_1.DAT', 'r')
#zscan = open('Zscan_2.DAT', 'r')
#zscan = open('Zscan_XRR_0009_Scan2020Feb07-220747.DAT', 'r')

# read files into lists, turn lists into numpy matrices
# possibly change so that symbols to ignore are more general? / ask Carlos
# if there are any others? 
zscan_z  = []
zscan_cps = []
for line in zscan:
    if line[0] != "*" and line[0] != "#" and line[0] != ";":
        z, cps = line.split(' ')
        cps = cps.strip('\n')
        zscan_z.append(float(z))
        zscan_cps.append(float(cps))

zscan.close()
zscan_z = np.array(zscan_z)
zscan_cps = np.array(zscan_cps)

spec_theta  = []
spec_cps = []
for line in xrr_spec:
    if line[0] != "*" and line[0] != "#" and line[0] != ";":
        theta, cps = line.split(' ')
        cps = cps.strip('\n')
        spec_theta.append(float(theta))
        spec_cps.append(float(cps))

xrr_spec.close()
spec_theta = np.array(spec_theta)
spec_cps = np.array(spec_cps)

bkg_theta  = []
bkg_cps = []
for line in xrr_bkg:
    if line[0] != "*" and line[0] != "#" and line[0] != ";":
        theta, cps = line.split(' ')
        cps = cps.strip('\n')
        bkg_theta.append(float(theta))
        bkg_cps.append(float(cps))

xrr_bkg.close()
bkg_theta = np.array(bkg_theta)
bkg_cps = np.array(bkg_cps)        

#print(zscan_z)
#print(zscan_cps)
#print(spec_theta)
#print(spec_cps)
#print(bkg_theta)
#print(bkg_cps)

z_val_1, z_val_2, effective_beam_height = zscan_fun.eff_beam_height(zscan_z, zscan_cps)
stb_inten = zscan_fun.STB_intensity(zscan_z, zscan_cps, min(z_val_1, z_val_2))
print(effective_beam_height)
print(stb_inten)

plt.plot(zscan_z, zscan_cps)
plt.xlabel("z (mm)")
plt.ylabel("cps")
plt.title("zscan")

#still need: beautify graph, STB intensity, test effective beam height with
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