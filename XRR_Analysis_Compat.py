import numpy as np
import matplotlib.pyplot as plt
from csaps import CubicSmoothingSpline
from scipy.signal import argrelextrema 
from math import pi
import re
import zscan_fun 
import file_reading
from scipy.stats import linregress
import config

#ask user for input values 
#user_lambda = input("Enter lambda (Angstroms) ")
#B = input("Enter sample length (mm) ")
#step_size = input("Enter step size (deg/step) ")
#scan_speed = input("Enter scan speed (deg/min) ")
#sample_name = input("Enter sample name ")
 
#init params  
#sample_name = "testing"
#step_size = .02
#scan_speed = .25
#user_lambda = 1.54184 
#B = 10
#filter = 770.53 # or 0 

def init_data(zscan=0, xrr_spec=0, xrr_bkg=0):
    # read files into lists, turn lists into numpy matrices
    if zscan !=0:
        zscan_z, zscan_cps = file_reading.pull_data(zscan)
        #apply filter 
        zscan_cps = zscan_cps * config.filter
    else:
        config.xrr_no_zscan = 1
        zscan_z = []
        zscan_cps = [] 
    spec_theta, spec_cps = file_reading.pull_data(xrr_spec)
    bkg_theta, bkg_cps = file_reading.pull_data(xrr_bkg) 

    return (zscan_z, zscan_cps), (spec_theta, spec_cps), (bkg_theta, bkg_cps)

def pull_vars(file):
    file_reading.pull_vars(file)

def zscan_func(zscan_z, zscan_cps):
    #get the effective beam height, STB intensity 
    stb_inten, effective_beam_height, z_1, z_2, reduced_z, inter, slope = zscan_fun.stb_intensity_and_eff_beam_height(zscan_z, zscan_cps) 
    return stb_inten, effective_beam_height, z_1, z_2, reduced_z, inter, slope

def spec_bkg_func(stb_inten, effective_beam_height, spec_theta, spec_cps, bkg_theta, bkg_cps, rem_points=4):
    #specular & background 
    spec_q = 4 * pi * np.sin(np.deg2rad(spec_theta / 2)) / config.user_lambda
    bkg_q = 4 * pi * np.sin(np.deg2rad(bkg_theta / 2)) / config.user_lambda
    diff_cps = spec_cps - bkg_cps

    #geometrical correction
    #account for divide by 0 warning? 
    gc_cps = (effective_beam_height / ( config.B * np.sin(np.deg2rad(spec_theta /  2)))) * diff_cps

    #take the highest values 
    highest_cps = np.maximum(diff_cps, gc_cps)

    #normalize by stb intensity
    norm_reflectivity = highest_cps / stb_inten
    orig_norm_reflectivity = norm_reflectivity

    #compute error bars 
    error_bars = np.sqrt((spec_cps * config.step_size * 60 / config.scan_speed) + (bkg_cps * config.step_size * 60 / config.scan_speed)) / stb_inten

    #exclude first x (default 4) data points (creates a less messy file for motofit). renormalize reflectivity w/ the highest value. 
    #calculate the renormalized reflectivity error. 
    norm_reflectivity = norm_reflectivity[rem_points:]
    renorm_reflect = norm_reflectivity / np.amax(norm_reflectivity)
    dq = .00778 #machine dependent
    renorm_reflect_error = renorm_reflect * .05 

    #change location of dq - should probs be in GUI file 

    return spec_q, renorm_reflect, renorm_reflect_error, dq, error_bars, orig_norm_reflectivity

def save_motofit_file(spec_q, renorm_reflect, renorm_reflect_error, dq, f):
    #write data to text file for motofit to use
    #maybe do a version or hash thing where if there's already a file created, another w/ a diff suffix can be created 
    #choose where to save to?
    #f = open("%s_XRR.txt" % (config.sample_name), "x")
    for (q, r, er) in zip(spec_q[4:], renorm_reflect, renorm_reflect_error):
        f.write('{0} {1} {2} {3}\n'.format(q, r, er, dq))
    f.close()

def save_motofit_file_batch(spec_q, renorm_reflect, renorm_reflect_error, dq, folder, name):
    f = open(folder + "%s_XRR.txt" % name, "x")
    for (q, r, er) in zip(spec_q[4:], renorm_reflect, renorm_reflect_error):
        f.write('{0} {1} {2} {3}\n'.format(q, r, er, dq))
    f.close()
