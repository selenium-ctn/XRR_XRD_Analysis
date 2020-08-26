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
 
#init params  
sample_name = "testing"
step_size = .02
scan_speed = .25
user_lambda = 1.54184 
B = 10
filter = 770.53 # or 0 

def init_data(zscan, xrr_spec, xrr_bkg):
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
    zscan_cps = zscan_cps * filter
    #mult for zscan only!!! maybe don't worry...maybe do....tell user to use automatic filter or nah....
    return (zscan_z, zscan_cps), (spec_theta, spec_cps), (bkg_theta, bkg_cps)
