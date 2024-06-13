import tkinter as tk
from tkinter import ttk
import sys
import ttkbootstrap as ttk
from Preprocess_Class import OCR_tesseract
from PIL import Image

class ImageEditor(tk.Toplevel):

    def __init__(self,parent):
        super().__init__(parent)
        self.title("Image Editor")
        self.minsize(400,450)
        self.geometry("430x480")
        self


        # Entry to input file path
        self.input_label = ttk.Entry(self,)
        self.input_label.pack(pady=10,padx=5)

        # Button to load image
        self.load_button = ttk.Button(self, text="Load Image",command=self.Image_info())
        self.load_button.pack(pady=10,padx=5)

        self.errors = ttk.Label(self,text="")
        self.errors.pack(padx=10,pady=10)
        #progress bar
        self.scale_float = tk.IntVar(value=12)
        self.progress = ttk.Progressbar(self)
        self.progress.pack(padx=10,pady=10)
        #for x size
        self.scale = ttk.Scale(self,command= lambda value: print(self.scale_float.get()),from_=0,to=200,length=100,orient='vertical',variable=self.scale_float)
        self.scale.pack()

        # Radio buttons for image operations
        tryby = ["png", "jpg", "jpeg", "tiff", "ppm", "gif"]
        string_typy = tk.StringVar(value=tryby[0])

        self.combo = ttk.Combobox(self,textvariable=string_typy,width=18)
        self.combo['values']=tryby
        self.combo.pack(pady=20)
        #exit for this window
        ttk.Button(self,text="exit",command = self.destroy).pack(side="right",pady=10,padx=10)
        self.mainloop()
    def Image_info(self)-> list[int,int,str]:
        #image =OCR_tesseract.processImage(self.input_label,self.errors)
        image = "Images/test2.jpg"
        if image:
            Im_open = Image.open(image)
            size_x,size_y =Im_open.size
            info = Im_open.format_description.split(" ")
            return size_x, size_y, info[0]

    def Image_transform(self):
        pass

