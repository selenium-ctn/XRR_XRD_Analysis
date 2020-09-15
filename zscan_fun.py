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
    slope, inter, _, _, _ = linregress(new_z, new_cps)

    #calculate the STB intensity 
    filter_arr = (z <= stb_plat_z_val)
    stb_reduced_cps = cps[filter_arr]
    stb = np.mean(stb_reduced_cps)

    #calculate the z values from the linear regression when cps = STB intensity and cps = 0
    z_1 = (stb - inter) / slope
    z_2 = - inter / slope 

    #plot z vs cps 
    #plt.plot(z, cps)
    #plt.xlabel("z (mm)")
    #plt.ylabel("cps")
    #plt.title("zscan")

    #plt.figure()
    #plt.plot(z, cps)
    #plt.vlines(z_1, 0, stb, linestyles='dashed')
    #plt.vlines(z_2, 0, stb, linestyles='dashed')
    #plt.hlines(stb, z[0], z_1, color="black")
    #plt.hlines(0, z_2, z[z.size - 1], color="black")
    #plt.plot(reduced_z, inter + slope * reduced_z)
    #plt.text(1, 1, "effective beam height = %d" % abs(z_1 - z_2)) #transform axes from data coords to axis coords!
    #plt.xlabel("z (mm)")
    #plt.ylabel("cps")
    #plt.title("zscan")

    return stb, abs(z_1 - z_2), z_1, z_2, reduced_z, inter, slope
        
