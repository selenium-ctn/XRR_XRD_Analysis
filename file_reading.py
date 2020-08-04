import re
import numpy as np

def pull_data(file):
    """Pulls data from a file that should go into two arrays

    file = file to be read 
    Returns tuple with two numpy arrays
    """
    array1 = []
    array2 = []
    exclude = re.compile(r"[\d-]")

    for line in file:
        if exclude.match(line):
            var1, var2 = line.split(' ')
            var2 = var2.strip('\n')
            array1.append(float(var1))
            array2.append(float(var2))

    file.close()
    array1 = np.array(array1)
    array2 = np.array(array2)
    return array1, array2