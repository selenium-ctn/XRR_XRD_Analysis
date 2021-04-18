import glob
import XRR_Analysis_Compat as XAC
import os
import config 

config.step_size = 0.02
config.scan_speed = 2
config.user_lambda = 1.5
config.B = 10
config.filter = 1.000000

path = "C:\\Users\\selin\\Downloads\\PLD02212021_NbSe2_100C_r_Al2O3\\PLD02212021_NbSe2_100C_r_Al2O3\\"
#bkgd_files = glob.glob(path + '*XRRBkgd*.dat')
#spec_files = glob.glob(path + 'XRRSpec*.dat')
#zscan_files = glob.glob(path + 'Zscan*.dat')
scan_number = 23
print(glob.glob(path + 'Zscan*' + str(scan_number) + '*.dat')[0])
print(os.path.exists(path + "XRR_motofit"))

for i in range(1, scan_number):
    zscan, spec, bkg = XAC.init_data(open(glob.glob(path + 'Zscan*' + str(i) + '*.dat')[0]), open(glob.glob(path + 'XRRSpec*' + str(i) + '*.dat')[0]),  open(glob.glob(path + 'XRRBkgd*' + str(i) + '*.dat')[0]))
    stb_inten, effective_beam_height, z_1, z_2, reduced_z, inter, slope = XAC.zscan_func(zscan[0], zscan[1])
    spec_q, renorm_reflect, renorm_reflect_error, dq, error_bars, orig_norm_reflectivity = XAC.spec_bkg_func(stb_inten, effective_beam_height, spec[0], spec[1], bkg[0], bkg[1])
    XAC.save_motofit_file_batch(spec_q, renorm_reflect, renorm_reflect_error, dq, path + "XRR_motofit/", str(i))

