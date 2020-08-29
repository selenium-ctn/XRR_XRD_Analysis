import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, LabelFrame

class GUI:
    def __init__(self, master):
        self.master = master 
        self.button = ttk.Button(text = "Select zscan file",command = self.fileDialogZscan)
        self.button.pack()

    def fileDialogZscan(self):
        global zscan
            #zscan = "empty"
        zscan = filedialog.askopenfile(initialdir = "/", title="Select zscan file", filetypes = (("dat files","*.dat"),("text files","*.txt"), ("all files","*.*")), mode="r")
  
root = tk.Tk()
gui = GUI(root)
root.mainloop()