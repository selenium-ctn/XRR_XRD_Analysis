import numpy as np
from csaps import CubicSmoothingSpline
from scipy.signal import argrelextrema 

def eff_beam_height(z, cps):
    """Determines the effective beam height from XRR zscan data.

    z = numpy array of z data, cps = numpy array of cps data.
    """
    first_deriv = np.gradient(cps, z)
    linspace_z = np.linspace(z[0], z[z.size - 1], z.size)

    d1_fun = CubicSmoothingSpline(z, first_deriv, smooth=0.99995).spline
    d1 = d1_fun(linspace_z)

    #edge case never gets above 0 ?
    min_pos_d1 = d1.argmin()
    curr_val = d1[min_pos_d1]
    curr_index = min_pos_d1
    while curr_val < 0:
        curr_index = curr_index + 1
        curr_val = d1[curr_index]

    end_ind_d1= curr_index - 1

    curr_val = d1[min_pos_d1]
    curr_index = min_pos_d1
    while curr_val < 0:
        curr_index = curr_index - 1
        curr_val = d1[curr_index]

    start_ind_d1 = curr_index + 1

    reduced_d1 = d1[start_ind_d1:end_ind_d1]
    reduced_z = linspace_z[start_ind_d1:end_ind_d1]

    d2 = np.gradient(reduced_d1, reduced_z)
    d3 = np.gradient(d2, reduced_z)

    min_pos_d3 = d3.argmin()
    loc_min_d3 = argrelextrema(d3, np.less)
    loc_min_d3, = loc_min_d3
    min_pos_2_d3 = loc_min_d3[0]

    print(d3[min_pos_d3])
    print(d3[min_pos_2_d3])

    for x in loc_min_d3:
        if d3[x] < d3[min_pos_2_d3] and d3[x] > d3[min_pos_d3]:
            min_pos_d3 = x
    
    z_1 = reduced_z[min_pos_d3]
    z_2 = reduced_z[min_pos_2_d3]

    print(z_1, z_2)
    return abs(z_1 - z_2)
        
