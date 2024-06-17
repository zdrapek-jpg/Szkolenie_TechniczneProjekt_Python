import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from PIL import Image,UnidentifiedImageError


class ImageEditor(tk.Toplevel):

    def __init__(self,parent,title,):
        super().__init__(parent)
        self.title(title)
        self.minsize(400,450)
        self.geometry("430x480")

        # entry to input path
        self.input_label = ttk.Entry(self)
        self.input_label.pack(pady=10,padx=5)

        # Button to load image
        self.load_button = ttk.Button(self, text="Load Image",command=self.Image_transform)
        self.load_button.pack(pady=10,padx=5)
        #error label
        self.errors = ttk.Label(self, text="")
        self.errors.pack(padx=10, pady=10)
        #progress bar variables
        self.scale_float_x_begin = tk.IntVar(value=0)
        self.scale_float_x_end = tk.IntVar(value=0)
        self.scale_float_y_begin = tk.IntVar(value=0)
        self.scale_float_y_end = tk.IntVar(value=0)
        #listening for variables
        self.scale_float_x_begin.trace("w", self.update_entries)
        self.scale_float_x_end.trace("w", self.update_entries)
        self.scale_float_y_begin.trace("w", self.update_entries)
        self.scale_float_y_end.trace("w", self.update_entries)


        #frame for x,y size  label-> scale->scale->entry X2
        self.frame = ttk.Frame(self)
        self.frame.pack(padx=10,pady=10)
        self.frame.config(height=200)
        self.frame.columnconfigure((0, 1), uniform="a", weight=1)
        self.frame.rowconfigure((0,3), uniform='a', weight=1)
        #etykieta
        ttk.Label(self.frame, text="x: beginXend").grid(column=0, row=0)

        self.scale_on_x_begin = ttk.Scale(master=self.frame,command= lambda value: print(self.scale_float_x_begin.get()),
                               from_=0,
                               to=200,
                               length=100,
                               orient='horizontal',
                               variable=self.scale_float_x_begin)
        self.scale_on_x_begin.grid(column=0,row=1,padx=5,pady=5)
        self.scale_on_x_begin["state"] = "disable"
        self.scale_on_x_end = ttk.Scale(master=self.frame, command=lambda value: print(self.scale_float_x_end.get()),
                                          from_=0,
                                          to=200,
                                          length=100,
                                          orient='horizontal',
                                          variable=self.scale_float_x_end)
        self.scale_on_x_end.grid(column=0, row=2, padx=10,pady=10)
        self.scale_on_x_end["state"] = "disable"

        self.entry_image_width=  ttk.Entry(self.frame,text = "0X0")
        self.entry_image_width.grid(column=0,row=3,pady=5,padx=5)

        ttk.Label(self.frame,text = "y: beginXend").grid(column=1,row=0)
        self.scale_on_y_begin = ttk.Scale(master=self.frame, command=lambda value: print(self.scale_float_y_begin.get()),
                               from_=0,
                               to=200,
                               length=100,
                               orient='horizontal',
                               variable=self.scale_float_y_begin)
        self.scale_on_y_begin.grid(column=1,row=1,padx=10,pady=10)
        self.scale_on_y_begin["state"] = "disable"
        self.scale_on_y_end = ttk.Scale(master=self.frame, command=lambda value: print(self.scale_float_y_end.get()),
                                     from_=0,
                                     to=200,
                                     length=100,
                                     orient='horizontal',
                                     variable=self.scale_float_y_end)
        self.scale_on_y_end.grid(column=1, row=2, padx=5,pady=5)
        self.scale_on_y_end["state"] = "disable"

        self.entry_image_height = ttk.Entry(self.frame, text = "0X0")
        self.entry_image_height.grid(column=1,row=3,pady=5,padx=5)

        # combobox values and variable
        tryby= ["PNG", "JPG", "JPEG", "TIFF", "PPM", "GIF"]
        self.string_typy_variable = tk.StringVar(value=tryby[0])


        self.combo = ttk.Combobox(self,textvariable=self.string_typy_variable,width=18)
        self.combo['values']=tryby
        self.combo.pack(pady=20)
        #final button and save image
        self.save_image = ttk.Button(self,text="save Image",command=self.save_image)
        self.save_image.pack(padx=10)
        self.save_image['state']="disable"

        #exit for this window
        ttk.Button(self,text="exit",command = self.destroy).pack(side="right",pady=10,padx=10)
        self.mainloop()

    # Method to load and display image information
    def Image_info(self):
        try:
            image_path = self.input_label.get()
            Im_open = Image.open(image_path)
            size_x, size_y = Im_open.size
            info = Im_open.format_description.split(" ")
            self.errors.config(text="Image loaded successfully", background="green")
            return [size_x, size_y, info[0]]
        except FileNotFoundError as e:
            self.errors.config(text=f"Image Not Found: {e}", background="red")
        except UnidentifiedImageError as e:
            self.errors.config(text=f"Unsupported Image: {e}", background="red")
        except Exception as e:
            self.errors.config(text=f"An Error Occurred: {e}", background="red")
        return None



    def Image_transform(self):
        try:
            if self.Image_info()!=None:
                x,y,type = self.Image_info()
                self.scale_on_x_begin['state'] = 'enable'
                self.scale_on_x_end['state'] = 'enable'
                self.scale_on_y_begin['state'] = 'enable'
                self.scale_on_y_end['state'] = 'enable'
                self.save_image['state'] = 'enable'
                self.scale_on_x_begin.configure(from_=0,to=int(x),length=100)
                self.scale_on_x_end.configure(from_=int(100), to=int(x), length=100)
                self.scale_on_y_begin.configure(from_=0, to=int(y), length=100)
                self.scale_on_y_end.configure(from_=int(100), to=int(y), length=100)


        except:
            print("mistake")

    def update_entries(self, *args):
        # Calculate and update the width and height labels based on the scale values
        if self.scale_float_x_begin.get()<self.scale_float_x_end.get() and  self.scale_float_y_begin.get()<self.scale_float_y_end.get():
            width_value = str(self.scale_float_x_begin.get()) +"X"+ str(self.scale_float_x_end.get())
            height_value = str(self.scale_float_y_begin.get()) +"X"+ str(self.scale_float_y_end.get())


            self.entry_image_width.config(text=str(width_value))
            self.entry_image_height.config(text=str(height_value))
            return (self.scale_float_x_begin.get(),self.scale_float_x_end.get(),self.scale_float_y_begin.get(),self.scale_float_y_end.get())
        else:
            self.errors.config(text="Niepoprawny rozmiar obrazu do cięcia")
    def save_image(self):
        path =self.input_label.get()
        image = Image.open(path)
        crop_dims = self.update_entries()
        if crop_dims is None:
            return

        try:
            # get the format from the combobox
            image_format = self.combo.get().upper()
            #(x,x,y,y)
            image_sizes = self.update_entries()

            # save path "Output_Images/cropped_image.png"
            save_path = f"Output_Images/cropped_image.{image_format.lower()}"


            # crop and save the image
            cropped_image = image.crop(image_sizes)
            cropped_image.save(save_path)
            messagebox.showinfo("Success", f"Image saved as {save_path}")
        except Exception as e:
            self.errors.config(text=f"An error occurred: {e}", background="red")



