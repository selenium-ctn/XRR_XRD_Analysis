import numpy as np
from csaps import CubicSmoothingSpline
from scipy.signal import argrelextrema 
import matplotlib.pyplot as plt
from scipy.stats import linregress

def stb_intensity_and_eff_beam_height(z, cps):
    """Determines the straight to beam intensity and effective beam height from XRR zscan data.

    z = numpy array of z data, cps = numpy array of cps data.
    Returns tuple: stb, effective beam height
    """
    #take first derivative of zscan 
    first_deriv = np.gradient(cps, z)
    linspace_z = np.linspace(z[0], z[z.size - 1], z.size)

    #apply smoothing curve to first derivative (first derivative is very noisy/choppy, could not analyze well without this)
    d1_fun = CubicSmoothingSpline(z, first_deriv, smooth=0.99995).spline
    d1 = d1_fun(linspace_z)

    #find minimum, increase z values until y-value of 0 is reached (this would be the lower plateau in the original zscan curve; 
    #where slope = 0). Record that index
    min_pos_d1 = d1.argmin()
    curr_val = d1[min_pos_d1]
    curr_index = min_pos_d1
    while curr_val < 0 and (curr_index < d1.size - 1):
        curr_index = curr_index + 1
        curr_val = d1[curr_index]

    if curr_index != (d1.size - 1):
        end_ind_d1 = curr_index - 1
    else: 
        end_ind_d1 = curr_index

    #from minimum, decrease z values until y-value of 0 is reached (this would be the upper plateau in the original zscan curve; 
    #where slope = 0). Record that index. Also record the corresponding z value. 
    curr_val = d1[min_pos_d1]
    curr_index = min_pos_d1
    while curr_val < 0 and (curr_index > 0):
        curr_index = curr_index - 1
        curr_val = d1[curr_index]

    stb_plat_z_val = linspace_z[curr_index]
    if curr_index != 0:
        start_ind_d1 = curr_index + 1
    else: 
        start_ind_d1= curr_index

    #reduce the data so the plateaus are omitted. This isn't the linear portion of the data though, just the data without the plateaus.
    #in order to find the linear drop potion of the data, take the second derivative. 
    reduced_d1 = d1[start_ind_d1:end_ind_d1]
    reduced_z = linspace_z[start_ind_d1:end_ind_d1]
    d2 = np.gradient(reduced_d1, reduced_z)
    min_pos_d2 = d2.argmin()
    max_pos_d2 = d2.argmax()

    #filter the original z data. Only include the linear potion, which is roughly the data between the second derivative min and max. 
    #take 4 data points off the end of each side to make it more linear. 
    filter_arr = (z >= reduced_z[min_pos_d2 + 4]) & (z <= reduced_z[max_pos_d2 - 4])
    new_z = z[filter_arr]
    new_cps = cps[filter_arr]

    #do a linear regression on the filtered data set to get the slope and the intercept 
    slope, inter, r_value, p_value, std_err = linregress(new_z, new_cps)

    #calculate the STB intensity 
    stb = STB_intensity(z, cps, stb_plat_z_val)

    #calculate the z values from the linear regression when cps = STB intensity and cps = 0
    z_1 = (stb - inter) / slope
    z_2 = - inter / slope 

    return stb, abs(z_1 - z_2)
        
def STB_intensity(z_arr, cps_arr, z_end_val):
    """Determines the straight to beam intensity from XRR zscan data.

    cps_arr = numpy array of cps data, z_end_val = the last 
    value of the high plateau
    """
    curr_pos = z_arr.size - 1
    curr_val = z_arr[curr_pos]
    while curr_val > z_end_val: 
        curr_val = z_arr[curr_pos]
        curr_pos = curr_pos - 1
    
    end_pos = curr_pos + 1
    reduced_cps = cps_arr[0:end_pos]

    return np.mean(reduced_cps)
