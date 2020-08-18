from scipy.signal import argrelextrema, find_peaks, peak_prominences, find_peaks_cwt, peak_widths
import heapq 
import numpy as np
from math import pi
import matplotlib.pyplot as plt

def find_bragg_peak(q, cps):
    """Determines the q values that mark the beginning and the end of the Bragg peak 

    z = numpy array of q data, cps = numpy array of cps data.
    Returns 
    """

    #take the first derivative of q vs cps
    first_deriv = np.gradient(cps, q)

    #find the locations of the two lowest local minima 
    d1_min_pos, d1_2_min_pos = find_2_smallest_or_largest_loc(first_deriv, np.less, heapq.nsmallest)

    #find where the minima "end" (where the curve crosses 0, starting from the minima and increasing q)
    end_ind_d1_min_1 = find_peak_end(first_deriv, d1_min_pos)
    end_ind_d1_min_2 = find_peak_end(first_deriv, d1_2_min_pos)

    #print([q[end_ind_d1_min_1], q[end_ind_d1_min_2]])

    #find the locations of the two largest local maxima 
    d1_max_pos, d1_2_max_pos = find_2_smallest_or_largest_loc(first_deriv, np.greater, heapq.nlargest)

    #find where the maxima "end" (where the curve crosses 0, starting from the maxima and decreasing q)
    start_ind_d1_max_1 = find_peak_start(first_deriv, d1_max_pos)
    start_ind_d1_max_2 = find_peak_start(first_deriv, d1_2_max_pos)

    #print([q[start_ind_d1_max_1], q[start_ind_d1_max_2]])

    #pair off the minima and maxima; the closest minima and maxima = a pair 
    pair_1 = (min(start_ind_d1_max_1, start_ind_d1_max_2), min(end_ind_d1_min_1, end_ind_d1_min_2))
    pair_2 = (max(start_ind_d1_max_1, start_ind_d1_max_2), max(end_ind_d1_min_1, end_ind_d1_min_2))

    #find the pair with the widest distance between the start and the ends of the extrema pairs 
    if abs(pair_1[0] - pair_1[1]) > abs(pair_2[0] - pair_2[1]):
        bragg_pair = pair_1
    else:
        bragg_pair = pair_2

    plt.figure()
    plt.plot(q, first_deriv)
    plt.vlines(q[start_ind_d1_max_2], first_deriv[d1_min_pos], first_deriv[d1_max_pos], linestyles='dashed')
    plt.vlines(q[start_ind_d1_max_1], first_deriv[d1_min_pos], first_deriv[d1_max_pos], linestyles='dashed')
    plt.vlines(q[end_ind_d1_min_2], first_deriv[d1_min_pos], first_deriv[d1_max_pos], linestyles='dashed')
    plt.vlines(q[end_ind_d1_min_1], first_deriv[d1_min_pos], first_deriv[d1_max_pos], linestyles='dashed')

    return bragg_pair

def find_2_smallest_or_largest_loc(arr, npfun, heapfun):
    """Finds the 2 smallest or 2 largest local minima or maxima in an array

    arr = initial array, npfun = numpy function (either np.less or np.greater), heapfun = heap function (either heapq.nsmallest or heapq.nlargest)
    Returns tuple with the most extreme value's position first and the second most extreme value's position second
    """
    #find the indices of the local minima/maxima
    loc_m_pos = argrelextrema(arr, npfun)
    loc_m_pos, = loc_m_pos

    #create an array of the values of the local minima/maxima 
    loc_m_val = arr[loc_m_pos]

    #find the two smallest or largest extrema, find their locations in the original array 
    arr_2 = heapfun(2, loc_m_val)
    arr_1_pos = np.where( loc_m_val == arr_2[0])
    arr_1_pos = loc_m_pos[arr_1_pos]
    arr_2_pos = np.where(loc_m_val == arr_2[1])
    arr_2_pos = loc_m_pos[arr_2_pos]

    return arr_1_pos, arr_2_pos

def find_peak_start(arr, index):
    """Determines the start index of a maxima peak, for these purposes, the place where the peak crosses 0 

    z = np array of data (here, first derivative), index = index of top of peak (maxima)
    Returns start index of peak 
    """

    curr_index = index
    curr_val = arr[index]
    while curr_val > 0:
        curr_index = curr_index - 1
        curr_val = arr[curr_index]

    if curr_val == 0:
        return curr_index
    else: 
        return curr_index + 1

def find_peak_end(arr, index):
    """Determines the end index of a minima peak, for these purposes, the place where the peak crosses 0 

    z = np array of data (here, first derivative), index = index of bottom of peak (minima)
    Returns end index of peak 
    """

    curr_index = index
    curr_val = arr[index]
    while curr_val < 0:
        curr_index = curr_index + 1
        curr_val = arr[curr_index]

    if curr_val == 0:
        return curr_index
    else: 
        return curr_index - 1

def gauss(x, *p):
    y0, A, w, xc = p 
    return y0 + (A / (w * np.sqrt(pi / 2))) * np.exp(-2 * np.power((x - xc), 2) / np.power(w, 2))
    #return [y0 + A / (w * np.sqrt(pi / 2)) * exp(-2 * ((x_i - xc)**2) / (w**2)) for x_i in x]

def lorentz(x, *p):
    y0, A, w, xc = p
    return y0 + (2 * A / pi) * (w / (4 * np.power((x - xc), 2) + np.power(w, 2)))

def find_bragg_peak_alt(q, cps):
    #not sure how big I should make the widths....ask Carlos about max bragg peak sizes
    #remove NaN?
    #find the peaks (maxima) in the original data (reflectivity). Use cwt because of the possible noise. orig_peaks = array of positions,
    #referring to positions in the cps array where the peaks are located 
    orig_peaks = find_peaks_cwt(cps, np.linspace(1, 20, num=50))

    #find the peaks (maxima) in the first derivative of the reflectivity data. Use cwt because of the possible noise. peaks_1d = array of 
    #positions, referring to positions in the first_deriv array where the peaks are located 
    first_deriv = np.gradient(cps, q)
    peaks_1d =  find_peaks_cwt(first_deriv, np.linspace(1, 10, num=50))
    #peaks_1d =  find_peaks_cwt(first_deriv, np.linspace(1, 2, num=50))

    #find the widths (and other associtated values) of the peaks in the first dervative. This is more accurate than finding the widths of the peaks in the original 
    #data. rel_height=1 means the left and right bases are being found at the lowest contour lines of the peak  
    widths, width_heights, left_ips, right_ips = peak_widths(first_deriv, peaks_1d, rel_height=1)

    #create an array of the values of the peaks 
    loc_max_vals = first_deriv[peaks_1d]

    #find the two highest peak values 
    max_2_vals = heapq.nlargest(2, loc_max_vals)

    #find the position of the array containing the values of the peaks associated with the highest peak (also corresponds to position
    #in array of positions of peak values in first_deriv)
    loc_max_pos_1 = np.where( loc_max_vals == max_2_vals[0])

    #find position of highest peak in first_deriv array 
    peaks_1d_pos_1 = peaks_1d[loc_max_pos_1]

    #repeat process for second highest peaks 
    loc_max_pos_2 = np.where(loc_max_vals == max_2_vals[1])
    peaks_1d_pos_2 = peaks_1d[loc_max_pos_2]

    #same process as above, but with the original data instead of the first derivative
    loc_max_v = cps[orig_peaks]
    max2vals = heapq.nlargest(2, loc_max_v)
    loc_max_p1 = np.where(loc_max_v == max2vals[0])
    orig_peaks_pos_1 = orig_peaks[loc_max_p1]
    loc_max_p2 = np.where(loc_max_v == max2vals[1])
    orig_peaks_pos_2 = orig_peaks[loc_max_p2]

    #find the positions of the peaks directly preceeding the highest and second highest peaks in the original data
    prev_peak_1_pos = orig_peaks[loc_max_p1[0] - 1]
    prev_peak_2_pos = orig_peaks[loc_max_p2[0] - 1]

    #confirm that both of the highest peaks found in the first derivative correspond to the highest peaks in the original data.
    #do this by seeing if the q values of the first derivative peaks fall between the q value of the peak and its preceeding peak
    #peaks in the first derivative correspond will always correspond to a point on the original data peak before (to the right of) the 
    #highest point of the peak 
    if q[peaks_1d_pos_1] < q[orig_peaks_pos_1] and q[peaks_1d_pos_1] > q[prev_peak_1_pos]:
        bragg_peak_possibility_1 = peaks_1d_pos_1
    elif q[peaks_1d_pos_1] < q[orig_peaks_pos_2] and q[peaks_1d_pos_1] > q[prev_peak_2_pos]:
        bragg_peak_possibility_1 = peaks_1d_pos_1
    else: bragg_peak_possibility_1 = None

    if q[peaks_1d_pos_2] < q[orig_peaks_pos_2] and q[peaks_1d_pos_2] > q[prev_peak_2_pos]:
        bragg_peak_possibility_2 = peaks_1d_pos_2
    elif q[peaks_1d_pos_2] < q[orig_peaks_pos_1] and q[peaks_1d_pos_2] > q[prev_peak_1_pos]:
            bragg_peak_possibility_2 = peaks_1d_pos_2
    else: bragg_peak_possibility_2 = None

    #if both peaks correspond correctly (the substrate peak may or may not register as a highest 1st derivative peak), compare the widths
    #of the peaks in the first derivative. The bragg peak will be the one that is wider
    if bragg_peak_possibility_1 != None and bragg_peak_possibility_2 != None:
        #needs testing...didn't get tested bc substrate peak did not register 
        if widths[loc_max_pos_1] > widths[loc_max_pos_2]:
            bragg_peak_1d = loc_max_pos_1
        else:
            bragg_peak_1d = loc_max_pos_2
    elif bragg_peak_possibility_1 != None:
        bragg_peak_1d = loc_max_pos_1
    elif bragg_peak_possibility_2 != None:
        bragg_peak_1d = loc_max_pos_2

    #adjust for the fact that the widths will sometimes surpass the 0 mark in the first derivative. 
    if first_deriv[left_ips[bragg_peak_1d].astype(np.int)] < 0:
        curr_index = left_ips[bragg_peak_1d].astype(np.int)
        adjust = 0 
        while first_deriv[curr_index] < 0:
            curr_index = curr_index + 1
            adjust = adjust + 1
    
    print((q[curr_index], q[(right_ips[bragg_peak_1d] - adjust + widths[bragg_peak_1d]).astype(np.int)]))
    
    plt.figure()
    plt.plot(q, cps)
    plt.plot(q[orig_peaks], cps[orig_peaks], "x")
    plt.yscale("log")
    #plt.plot(q[lb], cps[lb], 'o')
    #plt.plot(q[rb], cps[rb], 'o')
    plt.figure()
    plt.plot(q, first_deriv)
    plt.plot(q[peaks_1d], first_deriv[peaks_1d], "x")
    plt.hlines(width_heights, q[left_ips.astype(np.int)], q[right_ips.astype(np.int)])

    return curr_index, (right_ips[bragg_peak_1d] - adjust + widths[bragg_peak_1d]).astype(np.int)

def find_bragg_peak_rc(q, cps):
    #use for substrate peaks actually
    orig_peaks = find_peaks_cwt(cps, np.linspace(1, 10, num=50))
    widths, width_heights, left_ips, right_ips = peak_widths(cps, orig_peaks, rel_height=.999)
    print(widths)
    plt.figure()
    plt.plot(q, cps)
    plt.plot(q[orig_peaks], cps[orig_peaks], "x")
    plt.hlines(width_heights, q[left_ips.astype(np.int)], q[right_ips.astype(np.int)])
    plt.yscale("log")
    
    #create an array of the values of the peaks 
    loc_max_vals = cps[orig_peaks]

    #find the two highest peak values 
    max_1_val = heapq.nlargest(1, loc_max_vals)

    #find the position of the array containing the values of the peaks associated with the highest peak (also corresponds to position
    #in array of positions of peak values in first_deriv)
    loc_max_pos_1 = np.where( loc_max_vals == max_1_val[0])

    #find position of highest peak in first_deriv array 
    peaks_pos_1 = orig_peaks[loc_max_pos_1]

    return left_ips[loc_max_pos_1].astype(np.int), right_ips[loc_max_pos_1].astype(np.int)
    