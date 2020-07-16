import numpy as np

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

#print(zscan_z)
#print(zscan_cps)
print(spec_theta)
print(spec_cps)
print(bkg_theta)
print(bkg_cps)



