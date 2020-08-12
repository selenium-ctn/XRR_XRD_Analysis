from scipy.signal import argrelextrema 
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
