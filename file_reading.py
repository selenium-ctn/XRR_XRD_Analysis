import re
import numpy as np
import config

def pull_data(file, pull_vars):
    """Pulls data from a file that should go into two arrays

    file = file to be read 
    Returns tuple with two numpy arrays
    """
    array1 = []
    array2 = []
    #only reads lines beginning with a number or a negative sign 
    exclude = re.compile(r"[\d-]")

    for line in file:
        if exclude.match(line):
            var1, var2 = line.split()
            var2 = var2.strip('\n')
            array1.append(float(var1))
            array2.append(float(var2))
        elif pull_vars:
            if ";Speed" in line:
                __, speed = line.split("=")
                scan_speed = float(speed) 
                config.scan_speed = scan_speed
            if "*MEAS_SCAN_SPEED " in line:
                __, speed = line.split()
                scan_speed = float(speed.strip("\"")) 
                config.scan_speed = scan_speed
            if ";Width" in line:
                __, width = line.split("=")
                step_size = float(width) 
                config.step_size = step_size
            if "*MEAS_SCAN_STEP " in line:
                __, width = line.split()
                step_size = float(width.strip("\"")) 
                config.step_size = step_size

    file.close()
    array1 = np.array(array1)
    array2 = np.array(array2)
    return array1, array2