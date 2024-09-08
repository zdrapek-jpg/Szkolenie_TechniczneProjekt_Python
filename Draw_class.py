import tkinter as tk
from tkinter import ttk
import sys
import re
import numpy as np
from matplotlib import pyplot as plt
from Functions import display_screen_size
from sympy import symbols, solve, sympify

x,y,w,h = display_screen_size()
class Draw(tk.Toplevel):
    def __init__(self,parent,window_title):
        super().__init__(parent)
        self.title(window_title)
        self.geometry(f"{x}x{y+70}+{w}-{h+450}")
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
        self.zero_write.pack(side='left',padx=15)
        self.min_max = ttk.Label(self,text="punkty na x")
        self.min_max.pack(side='left',padx=15)

        ttk.Button(self,text="Exit" ,command= lambda: self.destroy()).pack(side='bottom',pady=20,padx=10)

    def set_error_message(self, error, color):
        # Update error label text and background color
        self.error_Label.config(text=error,background=color)
        return


    def process_function(self):
        function_equation = self.input_function.get()
        try:
            x_range = self.input_min_max.get().split(",")
            x_min, x_max = float(x_range[0]), float(x_range[1])
        except ValueError:
            self.set_error_message("Data must be two numbers separated by a comma, e.g., -10,-3", "red")
            return None

        # Detect the variable used in the function equation
        pattern = re.search(r'x|z|q|m|y', function_equation)
        if pattern:
            variable = pattern.group()
            print(f"Variable found: {variable}")
        else:
            self.set_error_message("No valid variable found in the function equation", "red")
            return None

        # Generate the x values for plotting
        x_values = np.linspace(x_min, x_max, 100)

        try:
            # Convert the string equation to a sympy expression
            expression = sympify(function_equation)

            # Evaluate the function for the x values
            y_values = [float(expression.subs(x, val)) for val in x_values]

            # Solve the equation for zero points
            zero_points = solve(expression, x)
            if zero_points:
                self.zero_write.config(text=f"Zero points: \n{zero_points}")
            else:
                self.zero_write.config(text="No zero points found")

            # Determine the min and max of y for plot scaling
            y_min, y_max = min(y_values), max(y_values)
            self.min_max.config(text=f"Max: {y_max}\nMin: {y_min}")

            # Plot the function
            fig, ax = plt.subplots()
            ax.plot(x_values, y_values, color='green')
            ax.axhline(0, color='orange', lw=2)  # Horizontal line at y=0
            ax.set_xlim(x_min - 2, x_max + 1)
            ax.set_ylim(y_min - 5, y_max + 5)
            plt.show()

        except Exception as e:
            self.set_error_message(f"An error occurred: {e}", "red")

