import tkinter as tk
from tkinter import ttk
import cv2
import pytesseract
import ttkbootstrap as ttk
from PIL import Image

print(f" aktualna wersja pytesseract : {pytesseract.get_tesseract_version()}")
import tensorflow as tf
import ttkbootstrap
import matplotlib

print("TensorFlow version:", tf.__version__)
print("Tkinter version:", tk.TkVersion)
print("ttkbootstrap version:", ttkbootstrap.__version__)
print("Tesseract version:", pytesseract.get_tesseract_version())
print("Pillow version:", Image.__version__)
print("OpenCV version (cv2):", cv2.__version__)
print("Matplotlib version:", matplotlib.__version__)

class Ocr_Window(tk.Toplevel):
    def __init__(self,parent,welcome,type):
        super().__init__(parent)
        self.title(welcome)
        self.geometry("400x450")
        self.minsize(340,280)
        ttk.Label(self,text=f"write filepath to file for {type}").pack(pady=10,padx=10)
        self.input_label = ttk.Entry(self, textvariable="",validate='focus')
        self.input_label.pack()
        ttk.Button(self, text="Load file", ).pack(pady=10, padx=10)
        ttk.Button(self, text="Exit", command=self.destroy).pack(side='bottom', pady=10,padx=15)
        self.config(padx=10,pady=10)

class SecondView(tk.Toplevel):
    def __init__(self,parent,welcome,type):
        super().__init__(parent)
        self.title(welcome)
        self.geometry("400x450")
        self.minsize(340,280)
        ttk.Label(self,text=f"write filepath to file for {type}").pack(pady=10,padx=10)
        self.input_label = ttk.Entry(self, textvariable="a ",validate='focus')
        self.input_label.pack()
        ttk.Button(self, text="Load file", ).pack(pady=10, padx=10)
        ttk.Button(self, text="Exit", command=self.destroy).pack(side='bottom', pady=10,padx=15)
        self.config(padx=10,pady=10)

class Preprocessing(SecondView):
    def __init__(self, parent, welcome, type):
        super().__init__(parent, welcome, type)
        Menu_Frame = ttk.Frame(self,padding=10)
        self.minsize(300,460)

        Menu_Frame.columnconfigure((0,1),pad=10,uniform='a',weight=1)
        Menu_Frame.rowconfigure((0,1,2), uniform='a',weight=1,pad=5)
        ttk.Button(Menu_Frame, text="treshold",width=12,command=self.show_write_Processing("treshold")).grid(row=0,column=0,)
        ttk.Button(Menu_Frame, text="no noise",width=12,command=self.show_write_Processing("no_noise")).grid(row=0,column=1)
        ttk.Button(Menu_Frame, text="dilated",width=12,command=self.show_write_Processing("dilated")).grid(row=1, column=0)
        ttk.Button(Menu_Frame, text="cos",width=12,command=self.show_write_Processing("cos")).grid(row=1, column=1)
        ttk.Button(Menu_Frame, text="contours",width=12,command=self.show_write_Processing("contours")).grid(row=2, column=0 )
        ttk.Button(Menu_Frame, text="animated",width=12,command=self.show_write_Processing("animated")).grid(row=2, column=1)
        Menu_Frame.pack(padx=10,pady=5)








    def show_write_Processing(self, function):
        #filePath = self.filePath.get()  # Get file path from instance variable
        if False:
            img = Image.open(filePath)

            if function == "threshold":
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
                cv2.imshow('Thresholded Image', thresholded)
                print("Thresholding successful")
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            elif function == "no_noise":
                print("Noise removal not implemented yet")
            # Add other image processing functions



