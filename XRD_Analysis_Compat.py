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
from scipy.optimize import curve_fit
import config

def init_data(zscan=0, xrd_spec=0, xrd_bkg=0, xrd_rock=0):
    # read files into lists, turn lists into numpy matrices
    if zscan !=0:
        zscan_z, zscan_cps = file_reading.pull_data(zscan)
    else:
        config.xrd_no_zscan = 1
        zscan_z = []
        zscan_cps = [] 
    if xrd_spec !=0:
        spec_theta, spec_cps = file_reading.pull_data(xrd_spec)
    else:
        spec_theta = []
        spec_cps = []
    if xrd_bkg != 0:
        bkg_theta, bkg_cps = file_reading.pull_data(xrd_bkg) 
    else:
        config.xrd_no_bkg = 1
        bkg_theta = []
        bkg_cps = []
    if xrd_rock != 0:
        rock_theta, rock_cps = file_reading.pull_data(xrd_rock)
    else:
        rock_theta = []
        rock_cps = []
    return (zscan_z, zscan_cps), (spec_theta, spec_cps), (bkg_theta, bkg_cps), (rock_theta, rock_cps)

"""
def init_data_without_bkg(zscan, xrd_spec):
    # read files into lists, turn lists into numpy matrices
    zscan_z, zscan_cps = file_reading.pull_data(zscan)
    spec_theta, spec_cps = file_reading.pull_data(xrd_spec)
    config.xrd_no_bkg = 1
    bkg_theta = []
    bkg_cps = []
    return (zscan_z, zscan_cps), (spec_theta, spec_cps), (bkg_theta, bkg_cps)
"""

#def pull_vars():

def zscan_func(zscan_z, zscan_cps):
    #get the effective beam height, STB intensity 
    stb_inten, effective_beam_height, z_1, z_2, reduced_z, inter, slope = zscan_fun.stb_intensity_and_eff_beam_height(zscan_z, zscan_cps) 
    return stb_inten, effective_beam_height, z_1, z_2, reduced_z, inter, slope

def plot_XRD_data(spec_theta, bkg_theta, spec_cps, bkg_cps, stb_inten):
    #Specular & background 
    spec_q = 4 * pi * np.sin(np.deg2rad(spec_theta / 2)) / config.user_lambda
    if config.xrd_no_bkg == 0:
        bkg_q = 4 * pi * np.sin(np.deg2rad(bkg_theta / 2)) / config.user_lambda

    #difference between specular cps and background cps; normalize by STB intensity 
    if config.xrd_no_bkg == 0:
        diff_cps = spec_cps - bkg_cps
    else:
        diff_cps = spec_cps 

    norm_reflectivity = diff_cps / stb_inten

    #compute error bars 
    if config.xrd_no_bkg == 0:
        error_bars = np.sqrt((spec_cps * config.step_size * 60 / config.scan_speed) + (bkg_cps * config.step_size * 60 / config.scan_speed)) / stb_inten
    else:
        error_bars = np.sqrt((spec_cps * config.step_size * 60 / config.scan_speed)) / stb_inten

    return spec_q, norm_reflectivity, error_bars

def save_specular_file(two_theta, spec_q, reflectivity, error, f):
    #write data to text file for motofit to use
    #maybe do a version or hash thing where if there's already a file created, another w/ a diff suffix can be created 
    #choose where to save to?
    #f = open("%s_XRR.txt" % (config.sample_name), "x")
    for (th, q, r, er) in zip(two_theta, spec_q, reflectivity, error):
        f.write('{0} {1} {2} {3}\n'.format(th, q, r, er))
    f.close()

def save_rocking_file(theta, reflectivity, error, f):
    for (th, r, er) in zip(theta, reflectivity, error):
        f.write('{0} {1} {2}\n'.format(th, r, er))
    f.close()
"""
def bragg_peak_analysis_with_bkg(spec_theta, bkg_theta, spec_cps, bkg_cps, stb_inten):
    #Specular & background 
    spec_q = 4 * pi * np.sin(np.deg2rad(spec_theta / 2)) / config.user_lambda
    bkg_q = 4 * pi * np.sin(np.deg2rad(bkg_theta / 2)) / config.user_lambda

    #difference between specular cps and background cps; normalize by STB intensity 
    diff_cps = spec_cps - bkg_cps
    norm_reflectivity = diff_cps / stb_inten

    #compute error bars 
    error_bars = np.sqrt((spec_cps * config.step_size * 60 / config.scan_speed) + (bkg_cps * config.step_size * 60 / config.scan_speed)) / stb_inten

    #find the start and end indices of the bragg peak
    bragg_start_ind, bragg_end_ind = XRD_fun.find_bragg_peak_user_assist(spec_q, norm_reflectivity)

    #reduce the data to only the bragg peak -- this is the data to be used when Gaussian fitting the bragg peak 
    bragg_refl = norm_reflectivity[bragg_start_ind:bragg_end_ind]
    bragg_q = spec_q[bragg_start_ind:bragg_end_ind]

    #Gaussian fit the bragg peak. Area (10) may need to be changed between this, rocking curve, substrate peak, etc. Try integrating
    p0 = [np.average([bragg_refl[0], bragg_refl[bragg_refl.size - 1]]), 10, (bragg_q[0] - bragg_q[bragg_q.size - 1]) / 2, np.average([bragg_q[0], bragg_q[bragg_q.size - 1]])]
    coeff, var_matrix = curve_fit(XRD_fun.gauss, bragg_q, bragg_refl, p0=p0)
    fit = XRD_fun.gauss(bragg_q, *coeff)

    #FWHM 
    FWHM = abs(np.sqrt(2 * np.log(2)) * coeff[2])

    #vertical domain size 
    vert_domain_size = 2 * pi * 0.94 / np.sqrt(np.power(FWHM, 2) - np.power(config.spec_res, 2))
"""

