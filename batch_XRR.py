import glob
import XRR_Analysis_Compat as XAC
import os
import config 

config.step_size = 0.02
config.scan_speed = 2
config.user_lambda = 1.5412
config.B = 8
config.filter = 1.000000

path = "C:\\Users\\selin\\Downloads\\PLD02172021_NbSe2_500C_Al2O3\\PLD02172021_NbSe2_500C_Al2O3\\"
#bkgd_files = glob.glob(path + '*XRRBkgd*.dat')
#spec_files = glob.glob(path + 'XRRSpec*.dat')
#zscan_files = glob.glob(path + 'Zscan*.dat')
scan_number = 13 + 1 #add 1
print(os.path.exists(path + "XRR_motofit"))

for i in range(1, scan_number):
    print(i)
    print(glob.glob(path + 'Zscan*' + str(i) + '_00' +'*.dat')[0])
    zscan, spec, bkg = XAC.init_data(open(glob.glob(path + 'Zscan*' + str(i) + '_00' +'*.dat')[0]), open(glob.glob(path + 'XRRSpec*' + str(i) + '_00' + '*.dat')[0]),  open(glob.glob(path + 'XRRBkgd*' + str(i) + '_00' + '*.dat')[0]))
    stb_inten, effective_beam_height, z_1, z_2, reduced_z, inter, slope = XAC.zscan_func(zscan[0], zscan[1])
    spec_q, renorm_reflect, renorm_reflect_error, dq, error_bars, orig_norm_reflectivity = XAC.spec_bkg_func(stb_inten, effective_beam_height, spec[0], spec[1], bkg[0], bkg[1])
    XAC.save_motofit_file_batch(spec_q, renorm_reflect, renorm_reflect_error, dq, path + "XRR_motofit/", str(i))
