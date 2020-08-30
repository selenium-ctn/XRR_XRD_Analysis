import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, LabelFrame
import XRR_Analysis_Compat as XAC 
import config

class GUI:
    def __init__(self, master):
        global tk_zscan
        global tk_spec
        global tk_bkg
        global tk_samplename
        global tk_stepsize 
        global tk_scanspeed
        global tk_lambda 
        global tk_B
        tk_zscan = tk.StringVar()
        tk_spec = tk.StringVar()
        tk_bkg = tk.StringVar()
        tk_samplename = tk.StringVar()
        tk_stepsize = tk.DoubleVar()
        tk_scanspeed = tk.DoubleVar()
        tk_lambda = tk.DoubleVar()
        tk_B = tk.DoubleVar()
        tk_zscan.set("No file chosen")
        tk_spec.set("No file chosen")
        tk_bkg.set("No file chosen")
        tk_samplename.set(config.sample_name)
        tk_stepsize.set(config.step_size)
        tk_scanspeed.set(config.scan_speed)
        tk_lambda.set(config.user_lambda)
        tk_B.set(config.B)
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
        self.label.grid(row=1, column=1)
        #self.button.pack()
        #self.label = ttk.Label(xrr_tab, text=zscan)
        #self.label.pack()
        self.button = ttk.Button(xrr_tab, text = "Select specular file",command = self.fileDialogSpec)
        self.button.grid(pady=2.5, sticky="W", row=2, column=0)
        self.label = ttk.Label(xrr_tab, textvariable=tk_spec)
        self.label.grid(row=2, column=1)
        self.button = ttk.Button(xrr_tab, text = "Select background file",command = self.fileDialogBkg)
        self.button.grid(pady=2.5, sticky="W", row=3, column=0)
        self.label = ttk.Label(xrr_tab, textvariable=tk_bkg)
        self.label.grid(row=3, column=1)
        self.label = ttk.Label(xrr_tab, text="Would you like to import") 
        self.label.grid(row=4, column=1)
        self.label = ttk.Label(xrr_tab, text="parameters from files?")
        self.label.grid(row=5, column=1)
        self.button = ttk.Button(xrr_tab, text = "Import", command = self.importVars)
        self.button.grid(row=6, column=1)
        self.label = ttk.Label(xrr_tab, text="Sample name")
        self.label.grid(row=7, column=0)
        self.entry = ttk.Entry(xrr_tab, textvariable=tk_samplename)
        self.entry.grid(row=7, column=1)
        self.label = ttk.Label(xrr_tab, textvariable=tk_samplename)
        self.label.grid(row=7, column=2)
        self.label = ttk.Label(xrr_tab, text="Step size")
        self.label.grid(row=8, column=0)
        self.entry = ttk.Entry(xrr_tab, textvariable=tk_stepsize)
        self.entry.grid(row=8, column=1)
        self.label = ttk.Label(xrr_tab, textvariable=tk_stepsize)
        self.label.grid(row=8, column=2)
        self.label = ttk.Label(xrr_tab, text="Scan speed")
        self.label.grid(row=9, column=0)
        self.entry = ttk.Entry(xrr_tab, textvariable=tk_scanspeed)
        self.entry.grid(row=9, column=1)
        self.label = ttk.Label(xrr_tab, textvariable=tk_scanspeed)
        self.label.grid(row=9, column=2)
        self.label = ttk.Label(xrr_tab, text="Lambda")
        self.label.grid(row=10, column=0)
        self.entry = ttk.Entry(xrr_tab, textvariable=tk_lambda)
        self.entry.grid(row=10, column=1)
        self.label = ttk.Label(xrr_tab, textvariable=tk_lambda)
        self.label.grid(row=10, column=2)
        self.label = ttk.Label(xrr_tab, text="B")
        self.label.grid(row=11, column=0)
        self.entry = ttk.Entry(xrr_tab, textvariable=tk_B)
        self.entry.grid(row=11, column=1)
        self.label = ttk.Label(xrr_tab, textvariable=tk_B)
        self.label.grid(row=11, column=2)
        self.button = ttk.Button(text = "Run",command = self.run)
        self.button.grid()

    def fileDialogZscan(self):
        global zscan
        zscan = filedialog.askopenfile(initialdir = "/", title="Select zscan file", filetypes = (("dat files","*.dat"),("text files","*.txt"), ("all files","*.*")), mode="r")
        tk_zscan.set(zscan.name)
        #print(zscan)

    def fileDialogSpec(self):
        global spec
        spec= filedialog.askopenfile(initialdir = "/", title="Select specular file", filetypes = (("dat files","*.dat"),("text files","*.txt"), ("all files","*.*")), mode="r")
        tk_spec.set(spec.name)
        #print(self.spec)

    def fileDialogBkg(self):
        global bkg
        bkg= filedialog.askopenfile(initialdir = "/", title="Select background file", filetypes = (("dat files","*.dat"),("text files","*.txt"), ("all files","*.*")), mode="r")
        tk_bkg.set(bkg.name)

    def importVars(self):
        XAC.pull_vars(spec)
        tk_samplename.set(config.sample_name)
        tk_stepsize.set(config.step_size)
        tk_scanspeed.set(config.scan_speed)
        tk_lambda.set(config.user_lambda)
        tk_B.set(config.B)


    def run(self):
        config.sample_name = tk_samplename.get()
        zscan_data, spec_data, bkg_data = XAC.init_data(zscan, spec, bkg)
        stb_inten, effective_beam_height = XAC.zscan_func(zscan_data[0], zscan_data[1])
        renorm_reflect, renorm_reflect_error, dq = XAC.spec_bkg_func(stb_inten, effective_beam_height, spec_data[0], spec_data[1], bkg_data[0], bkg_data[1])
        print(renorm_reflect)


root = tk.Tk()
gui = GUI(root)
root.mainloop()