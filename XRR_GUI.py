import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, LabelFrame
from tkinter.filedialog import asksaveasfile
import XRR_Analysis_Compat as XAC 
import config
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

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
        global tk_filter
        tk_zscan = tk.StringVar()
        tk_spec = tk.StringVar()
        tk_bkg = tk.StringVar()
        tk_samplename = tk.StringVar()
        tk_stepsize = tk.DoubleVar()
        tk_scanspeed = tk.DoubleVar()
        tk_lambda = tk.DoubleVar()
        tk_filter = tk.DoubleVar()
        tk_B = tk.DoubleVar()
        tk_zscan.set("No file chosen")
        tk_spec.set("No file chosen")
        tk_bkg.set("No file chosen")
        tk_samplename.set(config.sample_name)
        tk_stepsize.set(config.step_size)
        tk_scanspeed.set(config.scan_speed)
        tk_lambda.set(config.user_lambda)
        tk_B.set(config.B)
        tk_filter.set(config.filter)
        self.master = master 
        master.title("XRR/XRD Data Reduction")
        tabControl = ttk.Notebook(root)
        self.xrr_tab = ttk.Frame(tabControl)
        self.xrd_tab = ttk.Frame(tabControl)
        xrr_tab = self.xrr_tab 
        xrd_tab = self.xrd_tab 
        tabControl.add(xrr_tab, text='XRR')
        tabControl.add(xrd_tab, text='XRD')
        #tabControl.pack(expand=1, fill="both")
        #tabControl.grid(expand=1, fill="both")
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
        self.label = ttk.Label(xrr_tab, text="Step size")
        self.label.grid(row=8, column=0)
        self.entry = ttk.Entry(xrr_tab, textvariable=tk_stepsize)
        self.entry.grid(row=8, column=1)
        self.label = ttk.Label(xrr_tab, text="Scan speed")
        self.label.grid(row=9, column=0)
        self.entry = ttk.Entry(xrr_tab, textvariable=tk_scanspeed)
        self.entry.grid(row=9, column=1)
        self.label = ttk.Label(xrr_tab, text="Lambda")
        self.label.grid(row=10, column=0)
        self.combobox = ttk.Combobox(xrr_tab, textvariable=tk_lambda, values=[1.540562, 1.54184])
        self.combobox.grid(row=10, column=1)
        self.label = ttk.Label(xrr_tab, text="Sample Length")
        self.label.grid(row=11, column=0)
        self.entry = ttk.Entry(xrr_tab, textvariable=tk_B)
        self.entry.grid(row=11, column=1)
        self.label = ttk.Label(xrr_tab, text="Filter")
        self.label.grid(row=12, column=0)
        self.combobox = ttk.Combobox(xrr_tab, textvariable=tk_filter, values=[0, 770.53])
        self.combobox.grid(row=12, column=1)
        self.button = ttk.Button(xrr_tab, text = "Run",command = self.run)
        self.button.grid()
        self.button = ttk.Button(xrr_tab, text = "Save Motofit File",command = self.save_motofit)
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
        tk_stepsize.set(config.step_size)
        tk_scanspeed.set(config.scan_speed)

    def run(self):
        global spec_q
        global renorm_reflect
        global renorm_reflect_error
        global dq
        config.sample_name = tk_samplename.get()
        config.step_size = tk_stepsize.get()
        config.scan_speed = tk_scanspeed.get()
        config.user_lambda = tk_lambda.get()
        config.B = tk_B.get()
        config.filter = tk_filter.get()
        zscan_data, spec_data, bkg_data = XAC.init_data(zscan, spec, bkg)
        print(zscan_data)
        stb, effective_beam_height, z_1, z_2, reduced_z, inter, slope = XAC.zscan_func(zscan_data[0], zscan_data[1])      
        zscan_plot_str = '\n'.join((
            r'eff beam height=%.2f mm' % (effective_beam_height, ),
            r'STB=%.2f cps' % (stb, )))
        fig = Figure(figsize = (6, 4), dpi = 100)
        plot1 = fig.add_subplot(9, 1, (1,8))
        plot1.plot(zscan_data[0], zscan_data[1])
        plot1.vlines(z_1, 0, stb, linestyles='dashed')
        plot1.vlines(z_2, 0, stb, linestyles='dashed')
        plot1.hlines(stb, zscan_data[0][0], z_1, color="black")
        plot1.hlines(0, z_2, zscan_data[0][zscan_data[0].size - 1], color="black")
        plot1.plot(reduced_z, inter + slope * reduced_z)
        plot1.set(xlabel="z (mm)", ylabel="cps")
        plot1.set_title("zscan")
        plot1.text(0.65, 0.95, zscan_plot_str, transform=plot1.transAxes, fontsize=8, verticalalignment='top')
        canvas = FigureCanvasTkAgg(fig, master=self.xrr_tab)
        canvas.draw()
        canvas.get_tk_widget().grid(column=3, row=1, rowspan=11)
        print(stb)
        toolbarFrame = ttk.Frame(master=self.xrr_tab)
        toolbarFrame.grid(row=12, column=3, padx=0, pady=0)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        toolbar.update()
        spec_q, renorm_reflect, renorm_reflect_error, dq, error_bars, orig_norm_reflectivity = XAC.spec_bkg_func(stb, effective_beam_height, spec_data[0], spec_data[1], bkg_data[0], bkg_data[1])
        fig2 = Figure(figsize=(6, 4), dpi = 100)
        plot2 = fig2.add_subplot(9, 1, (1,8))
        plot2.errorbar(spec_q[2:], orig_norm_reflectivity[2:], yerr=error_bars[2:], ecolor='red')
        plot2.set(xlabel=r'q ($\mathrm{\AA}$)', ylabel="Reflectivity")
        plot2.set_title("q vs Reflectivity")
        plot2.set_yscale("log")
        canvas2 = FigureCanvasTkAgg(fig2, master=self.xrr_tab)
        canvas2.draw()
        canvas2.get_tk_widget().grid(column=3, row=14, rowspan=11)
        toolbarFrame2 = ttk.Frame(master=self.xrr_tab)
        toolbarFrame2.grid(row=26, column=3)
        toolbar2 = NavigationToolbar2Tk(canvas2, toolbarFrame2)
        toolbar2.update()

    def save_motofit(self):
        f = asksaveasfile(mode='w', defaultextension=".txt", initialfile="%s_XRR.txt" % (config.sample_name))
        if f is None:
            return 
        XAC.save_motofit_file(spec_q, renorm_reflect, renorm_reflect_error, dq, f)

root = tk.Tk()
gui = GUI(root)
root.mainloop()