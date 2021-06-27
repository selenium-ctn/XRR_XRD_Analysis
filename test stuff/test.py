import numpy as np
import matplotlib.pyplot as plt
import re

testfile = open('EXAMPLEErrorAnalysis.txt', 'r')

def pull_data(file):
    """Pulls data from a file that should go into two arrays

    file = file to be read 
    Returns tuple with two numpy arrays
    """
    array1 = []
    array2 = []
    array3 = []
    exclude = re.compile(r"[\d-]")

    for line in file:
        if exclude.match(line):
            var1, var2, var3 = line.split()
            var3 = var3.strip('\n')
            array1.append(float(var1))
            array2.append(float(var2))
            array3.append(float(var3))

    file.close()
    array1 = np.array(array1)
    array2 = np.array(array2)
    array3 = np.array(array3)
    return array1, array2, array3 

v1, v2, v3 = pull_data(testfile)

#plt.errorbar(v1, np.log10(v2), yerr=np.log10(v3))
plt.errorbar(v1, v2, yerr=v3)
plt.yscale("log")
plt.show()