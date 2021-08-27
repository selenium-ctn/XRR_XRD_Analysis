import file_reading
import numpy as np
from math import pi 

names_file = open("C:/Users/selin/Documents/BEDZYK RESEARCH/temp.txt")
nbo2_dir = "C:/Users/selin/Documents/BEDZYK RESEARCH/NbO2"

user_lambda = 1.540562

for line in names_file:
    line = line[1:]
    line = line.strip("\n")
    oline = nbo2_dir + line
    oline = open(oline, 'r')
    twotheta, cps = file_reading.pull_data(oline)
    spec_q = 4 * pi * np.sin(np.deg2rad(twotheta / 2)) / user_lambda
    n = oline.name[46:54]
    if n == "06162021":
        if oline.name == "C:/Users/selin/Documents/BEDZYK RESEARCH/NbO2/06162021_NbO2/PLD06152021_2_C_Al2O3_650C_10mTorr7percent/FULLXRD_0016_Scan2021Jun16-163811.txt":
            STB = 1.0045*10**8
        else:
            STB = 1.11*10**8
    elif n == "06222021":
        STB = 4.83*10**7
    elif n == "06232021":
        STB = 7.906*10**7
    elif n == "06282021":
        STB = 1.635*10**8
    elif n == "06292021":
        STB = 1.56*10**8
    elif n == "07192021":
        STB = 1.50*10**8 
    elif n == "07202021":
        STB = 1.47*10**8
    elif n == "07222021":
        STB = 1.421*10**8
    elif n == "07232021":
        STB = 1.362*10**8 
    elif n == "07292021":
        STB = 1.518*10**8
    elif n == "08272021":
        STB = 7.55*10**7 
    
    refl = cps / STB 

    sh = oline.name[60:]
    ind = sh.find("/")
    temp_n = "C:/Users/selin/Documents/BEDZYK RESEARCH/NbO2/NbO2_XRD/" + oline.name[60:(60+ind)] +".txt"
    f = open(temp_n, "w")
    for (th, q, r) in zip(twotheta, spec_q, refl):
        f.write('{0} {1} {2}\n'.format(th, q, r))
    f.close()

