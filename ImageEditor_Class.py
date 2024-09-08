import tkinter as tk
from tkinter import ttk
import ttkbootstrap
from PIL import Image, UnidentifiedImageError
from tkinter import messagebox
import os
from Frame_Class import Frame_Ocr

class ImageEditor(tk.Toplevel):
    def __init__(self, parent, titlee, type):
        super().__init__(parent)

        self.title(titlee)
        self.minsize(400, 450)
        self.geometry("400x520")

        self.Main = Frame_Ocr(self, f"Write filepath to file for {type}", "Errors", "Load file", function=self.load_image)
        self.Main.pack(pady=5, padx=5)

        # Variables for scale
        self.scale_x_begin = tk.IntVar(value=0)
        self.scale_x_end = tk.IntVar(value=1)
        self.scale_y_begin = tk.IntVar(value=0)
        self.scale_y_end = tk.IntVar(value=1)

        self.scale_x_begin.trace('w', self.update_entries)
        self.scale_x_end.trace('w', self.update_entries)
        self.scale_y_begin.trace('w', self.update_entries)
        self.scale_y_end.trace('w', self.update_entries)

        # Frame for x, y size labels and scales
        self.frame = ttk.Frame(self, height=200)
        self.frame.pack(padx=10, pady=10)
        self.frame.columnconfigure((0, 1), uniform='a', weight=1)
        self.frame.rowconfigure((0, 1, 2), uniform='a', weight=1)

        # x axis scales and entries
        ttk.Label(self.frame, text="X: Begin - End").grid(column=0, row=0)

        self.scale_x_begin_widget = ttk.Scale(self.frame, from_=0, to=200, length=100, orient='horizontal',
                                              variable=self.scale_x_begin)
        self.scale_x_begin_widget.grid(column=0, row=1, padx=5, pady=5)
        self.scale_x_begin_widget["state"] = "disabled"

        self.scale_x_end_widget = ttk.Scale(self.frame, from_=0, to=200, length=100, orient='horizontal',
                                            variable=self.scale_x_end)
        self.scale_x_end_widget.grid(column=0, row=2, padx=10, pady=10)
        self.scale_x_end_widget["state"] = "disabled"

        self.entry_image_width = ttk.Entry(self.frame, state='readonly')
        self.entry_image_width.grid(column=0, row=3, pady=5, padx=5)

        # Y axis scales and entries
        ttk.Label(self.frame, text="Y: Begin - End").grid(column=1, row=0)

        self.scale_y_begin_widget = ttk.Scale(self.frame, from_=0, to=200, length=100, orient='horizontal',
                                              variable=self.scale_y_begin)
        self.scale_y_begin_widget.grid(column=1, row=1, padx=10, pady=10)
        self.scale_y_begin_widget["state"] = "disabled"

        self.scale_y_end_widget = ttk.Scale(self.frame, from_=0, to=200, length=100, orient='horizontal',
                                            variable=self.scale_y_end)
        self.scale_y_end_widget.grid(column=1, row=2, padx=5, pady=5)
        self.scale_y_end_widget["state"] = "disabled"

        self.entry_image_height = ttk.Entry(self.frame, state='readonly')
        self.entry_image_height.grid(column=1, row=3, pady=5, padx=5)

        # Combobox for image formats
        image_formats = ["PNG", "JPG", "JPEG", "TIFF", "PPM", "GIF"]
        self.image_format_var = tk.StringVar(value=image_formats[0])
        self.format_combobox = ttk.Combobox(self, textvariable=self.image_format_var, values=image_formats, width=18)
        self.format_combobox.pack(pady=20)

        # Save button
        self.save_image_button = ttk.Button(self, text="Save Image", command=self.save_image)
        self.save_image_button.pack(padx=10)
        self.save_image_button['state'] = "disabled"

        ttk.Button(self, text="Exit", command=lambda: self.destroy()).pack(side="bottom", pady=10, padx=15)

        self.loaded_image = None
        self.image_path = None

    def load_image(self):
        try:
            print("wykonuje sie ")
            path = self.Main.process_Image_before(self.loaded_image)
            self.image_path = path
            self.loaded_image = Image.open(path)
            width, height = self.loaded_image.size
            if path:

                self.scale_x_begin_widget["state"] = "normal"
                self.scale_x_end_widget["state"] = "normal"
                self.scale_y_begin_widget["state"] = "normal"
                self.scale_y_end_widget["state"] = "normal"
                self.save_image_button["state"] = "normal"

                self.scale_x_begin_widget.config(from_=0, to=width-2)
                self.scale_x_end_widget.config(from_=0, to=width)
                self.scale_y_begin_widget.config(from_=0, to=height-2)
                self.scale_y_end_widget.config(from_=0, to=height)

        except FileNotFoundError as ex:
            self.Main.set_error_message(f"Image not found: {ex}", "red")
        except UnidentifiedImageError as uex:
            self.Main.set_error_message(f"Unsupported image: {uex}", "red")
        except Exception as exc:
            self.Main.set_error_message(f"Error occurred: {exc}", "red")

    def update_entries(self, *args):
        try:
            if (self.scale_x_begin_widget.get() < self.scale_x_end_widget.get() and
                    self.scale_y_begin_widget.get() < self.scale_y_end_widget.get()):
                width_value = f"{self.scale_x_begin.get()}-{self.scale_x_end.get()}"
                height_value = f"{self.scale_y_begin.get()}-{self.scale_y_end.get()}"

                self.entry_image_width.config(state='normal')
                self.entry_image_height.config(state='normal')
                self.entry_image_width.delete(0, tk.END)
                self.entry_image_height.delete(0, tk.END)
                self.entry_image_width.insert(0, width_value)
                self.entry_image_height.insert(0, height_value)
                self.entry_image_height.config(state='readonly')
                self.entry_image_width.config(state='readonly')
                self.Main.set_error_message("scale is correct for cropping","green")
            else:
                self.Main.set_error_message("Error: Incorrect scale values", "orange")
        except Exception as e:
            self.Main.set_error_message(f"Error: Incorrect scale values - {e}", "orange")

    def save_image(self):
        try:
            if self.loaded_image is None:
                self.Main.set_error_message("No image loaded", "red")
                return

            crop_dimensions = (self.scale_x_begin.get(), self.scale_y_begin.get(),
                               self.scale_x_end.get(), self.scale_y_end.get())
            cropped_image = self.loaded_image.crop(crop_dimensions)

            image_format = self.image_format_var.get().lower()
            save_directory = "Output_Images"
            os.makedirs(save_directory, exist_ok=True)
            save_path = f"{save_directory}/cropped_image.{image_format}"
            cropped_image.save(save_path)
            messagebox.showinfo("Save Successful", f"Image saved as {save_path}")
        except Exception as e:
            self.Main.set_error_message(f"Image not saved: {e}", "blue")
