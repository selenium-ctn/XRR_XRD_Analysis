import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from scipy.interpolate import interp1d
from scipy.ndimage import median_filter

zscan = open('Smartlab data/ZscanSTBXRR_0014_Scan2020Jan24-124745.dat', 'r')
xrr_spec = open('Smartlab data/spec2Pt111_Al2O3_006_1.dat', 'r')
xrr_bkg = open('Smartlab data/bkg2Pt111_Al2O3_006.dat', 'r')
# not sure if this is the right set of files lol 

# read files into lists, turn lists into numpy matrices
zscan_z  = []
zscan_cps = []
for line in zscan:
    if line[0] != "*" and line[0] != "#":
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
    if line[0] != "*" and line[0] != "#":
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
    if line[0] != "*" and line[0] != "#":
        theta, cps = line.split(' ')
        cps = cps.strip('\n')
        bkg_theta.append(float(theta))
        bkg_cps.append(float(cps))

xrr_bkg.close()
bkg_theta = np.array(bkg_theta)
bkg_cps = np.array(bkg_cps)        

print(zscan_z)
print(zscan_cps)
#print(spec_theta)
#print(spec_cps)
#print(bkg_theta)
#print(bkg_cps)

#my_pwlf = pwlf.PiecewiseLinFit(zscan_z, zscan_cps)
#breaks = my_pwlf.fit(3)
#print(breaks)

first_deriv = np.gradient(zscan_cps, zscan_z)

test = scipy.signal.savgol_filter(zscan_cps, 101, polyorder=7, deriv=0)
testgrad = np.gradient(test, zscan_z) 

tst = scipy.ndimage.median_filter(zscan_cps, size=5)
tstg = np.gradient(tst, zscan_z)

tstgg = scipy.ndimage.median_filter(tstg, size=5)
tstg2 = scipy.signal.savgol_filter(tstg, 101, polyorder=7, deriv=0)

tstggg = scipy.ndimage.median_filter(first_deriv, size=5)
z2 = np.linspace(zscan_z[0], zscan_z[zscan_z.size - 1], zscan_z.size)
plt.plot(zscan_z, zscan_cps)
plt.plot(zscan_z, tst)
plt.plot(zscan_z, test)
plt.figure()
#plt.plot(zscan_z, ftwo(x2))
#plt.figure()
plt.plot(zscan_z, first_deriv)
plt.plot(zscan_z, tstg)
plt.plot(zscan_z, tstg2)
plt.plot(zscan_z, testgrad)
#plt.plot(zscan_z, tstgg)
#plt.plot(zscan_z, tstggg)
plt.figure()
plt.plot(zscan_z, np.gradient(tstg2, zscan_z))
#plt.figure()
plt.show()




