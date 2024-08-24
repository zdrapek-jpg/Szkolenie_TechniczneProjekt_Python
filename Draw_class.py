import tkinter as tk
from tkinter import ttk
import sys

import numpy as np
from matplotlib import pyplot as plt
from Functions import display_screen_size
x,y,w,h = display_screen_size()
class Draw(tk.Toplevel):
    def __init__(self,parent,window_title):
        super().__init__(parent)
        self.title(window_title)
        self.geometry(f"{x}x{y+50}+{w}-{h+330}")
        self.minsize(350,370)
        self.frame_function = ttk.Frame(self)
        self.frame_function.pack()
        self.label_function = ttk.Label(self.frame_function,text="wzór funkcji (1 zmienna) :")
        self.label_function.pack(side="left",pady=15)
        self.input_function = ttk.Entry(self.frame_function)
        self.input_function.pack(side='left',padx=10,pady=10)

        self.frame = ttk.Frame(self)
        self.label_min_max = ttk.Label(self.frame, text="przedział na x min,max :")
        self.label_min_max.pack(side="left", pady=5,padx=10)
        self.input_min_max = ttk.Entry(self.frame)
        self.input_min_max.pack(side='left', padx=10, pady=5)
        self.frame.pack()

        ttk.Button(self,text="Draw",command= lambda : self.process_function()).pack(padx=10,pady=15)
        self.error_Label = ttk.Label(self, text="")
        self.error_Label.pack(pady=5)

        self.zero_write = ttk.Label(self,text="min max:")
        self.zero_write.pack(side='left')
        self.zero_update = ttk.Label(self,text="punkty na x")
        self.zero_update.pack(side='left')

        ttk.Button(self,text="Exit" ,command= lambda: sys.exit()).pack(side='bottom',pady=10,padx=10)

    def set_error_message(self, error, color):
        # Update error label text and background color
        self.error_Label.config(text=error,background=color)
        return


    def process_function(self):
        function_equasion = self.input_function.get()
        try:
            x_range = self.input_min_max.get().split(",")
            x_min,x_max =float(x_range[0]),float(x_range[1])
            print(x_min,x_max)
            range_on_x = np.linspace(x_min,x_max)

            function  = compile(function_equasion)
            self.set_error_message("Function and range cucessfully loadaed!","blue")
        except ValueError as e :
            self.set_error_message(e,"red")

        except Exception as exc:
            self.set_error_message(exc,"red")

