import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, LabelFrame
import XRR_Analysis_Compat as XAC 
#import sys
#import os
#import subprocess

class GUI:
    def __init__(self, master):
        global tk_zscan
        tk_zscan = tk.StringVar()
        tk_zscan.set("No file chosen")
        self.master = master 
        master.title("XRR/XRD Data Reduction")
        tabControl = ttk.Notebook(root)
        xrr_tab = ttk.Frame(tabControl)
        xrd_tab = ttk.Frame(tabControl)
        tabControl.add(xrr_tab, text='XRR')
        tabControl.add(xrd_tab, text='XRD')
        tabControl.pack(expand=1, fill="both")
        tabControl.grid(sticky="W")
        self.button = ttk.Button(xrr_tab, text = "Select zscan file",command = self.fileDialogZscan)
        self.button.grid(pady=2.5, sticky="W", row=1, column=0)
        self.label = ttk.Label(xrr_tab, textvariable=tk_zscan)
        #self.label.grid(row=1, column=1)
        #self.button.pack()
        #self.label = ttk.Label(xrr_tab, text=zscan)
        #self.label.pack()
        self.button = ttk.Button(xrr_tab, text = "Select specular file",command = self.fileDialogSpec)
        self.button.grid(pady=2.5, sticky="W")
        self.button = ttk.Button(xrr_tab, text = "Select background file",command = self.fileDialogBkg)
        self.button.grid(pady=2.5, sticky="W")
        self.button = ttk.Button(text = "Run",command = self.run)
        #self.button.pack()

    def fileDialogZscan(self):
        global zscan
        #zscan = "empty"
        zscan = filedialog.askopenfile(initialdir = "/", title="Select zscan file", filetypes = (("dat files","*.dat"),("text files","*.txt"), ("all files","*.*")), mode="r")
        #if zscan != "empty":
         #   tk_zscan.set(zscan)
        #printtext(zscan)
        #test2.zscan = zscan

    def fileDialogSpec(self):
        global spec
        #subprocess.run('python test3.py')
        #os.system('python test3.py')
        spec= filedialog.askopenfile(initialdir = "/", title="Select specular file", filetypes = (("dat files","*.dat"),("text files","*.txt"), ("all files","*.*")), mode="r")
        #print(self.spec)

    def fileDialogBkg(self):
        global bkg
        bkg= filedialog.askopenfile(initialdir = "/", title="Select background file", filetypes = (("dat files","*.dat"),("text files","*.txt"), ("all files","*.*")), mode="r")

    def run(self):
        zscan_data, spec_data, bkg_data = XAC.init_data(zscan, spec, bkg)
        stb_inten, effective_beam_height = XAC.zscan_func(zscan_data[0], zscan_data[1])
        renorm_reflect, renorm_reflect_error, dq = XAC.spec_bkg_func(stb_inten, effective_beam_height, spec_data[0], spec_data[1], bkg_data[0], bkg_data[1])
        print(renorm_reflect)

        

root = tk.Tk()
gui = GUI(root)
root.mainloop()