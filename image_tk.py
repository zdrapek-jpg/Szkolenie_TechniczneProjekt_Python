import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from PIL import Image, UnidentifiedImageError


class ImageEditor(tk.Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        self.minsize(400, 450)
        self.geometry("430x480")
        # Entry to input image path
        self.input_label = ttk.Entry(self)
        self.input_label.pack(pady=10, padx=5)

        # Button to load image
        self.load_button = ttk.Button(self, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10, padx=5)
        # Label to display errors
        self.errors = ttk.Label(self, text="")
        self.errors.pack(padx=10, pady=10)
        # Variables for scales
        self.scale_x_begin = tk.IntVar(value=0)
        self.scale_x_end = tk.IntVar(value=0)
        self.scale_y_begin = tk.IntVar(value=0)
        self.scale_y_end = tk.IntVar(value=0)
        # Trace variables to update entries
        self.scale_x_begin.trace("w", self.update_entries)
        self.scale_x_end.trace("w", self.update_entries)
        self.scale_y_begin.trace("w", self.update_entries)
        self.scale_y_end.trace("w", self.update_entries)

        # Frame for x, y size labels and scales
        self.frame = ttk.Frame(self)
        self.frame.pack(padx=10, pady=10)
        self.frame.config(height=200)
        self.frame.columnconfigure((0, 1), uniform="a", weight=1)
        self.frame.rowconfigure((0, 3), uniform='a', weight=1)

        # X axis scales and entries
        ttk.Label(self.frame, text="X: Begin - End").grid(column=0, row=0)

        self.scale_x_begin_widget = ttk.Scale(self.frame, from_=0, to=200, length=100, orient='horizontal', variable=self.scale_x_begin)
        self.scale_x_begin_widget.grid(column=0, row=1, padx=5, pady=5)
        self.scale_x_begin_widget["state"] = "disabled"

        self.scale_x_end_widget = ttk.Scale(self.frame, from_=0, to=200, length=100, orient='horizontal', variable=self.scale_x_end)
        self.scale_x_end_widget.grid(column=0, row=2, padx=10, pady=10)
        self.scale_x_end_widget["state"] = "disabled"

        self.entry_image_width = ttk.Entry(self.frame, state='readonly')
        self.entry_image_width.grid(column=0, row=3, pady=5, padx=5)

        # Y axis scales and entries
        ttk.Label(self.frame, text="Y: Begin - End").grid(column=1, row=0)

        self.scale_y_begin_widget = ttk.Scale(self.frame, from_=0, to=200, length=100, orient='horizontal', variable=self.scale_y_begin)
        self.scale_y_begin_widget.grid(column=1, row=1, padx=10, pady=10)
        self.scale_y_begin_widget["state"] = "disabled"

        self.scale_y_end_widget = ttk.Scale(self.frame, from_=0, to=200, length=100, orient='horizontal', variable=self.scale_y_end)
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

        # Exit button
        ttk.Button(self, text="Exit", command=self.destroy).pack(side="right", pady=10, padx=10)

    def load_image(self):
        try:
            image_path = self.input_label.get()
            image = Image.open(image_path)
            width, height = image.size

            # Enable scales
            self.scale_x_begin_widget["state"] = "normal"
            self.scale_x_end_widget["state"] = "normal"
            self.scale_y_begin_widget["state"] = "normal"
            self.scale_y_end_widget["state"] = "normal"
            self.save_image_button["state"] = "normal"

            # Update scales range
            self.scale_x_begin_widget.config(from_=0, to=width)
            self.scale_x_end_widget.config(from_=0, to=width)
            self.scale_y_begin_widget.config(from_=0, to=height)
            self.scale_y_end_widget.config(from_=0, to=height)

            self.errors.config(text="Image loaded successfully", background="green")
        except FileNotFoundError as e:
            self.errors.config(text=f"Image Not Found: {e}", background="red")
        except UnidentifiedImageError as e:
            self.errors.config(text=f"Unsupported Image: {e}", background="red")
        except Exception as e:
            self.errors.config(text=f"An Error Occurred: {e}", background="red")

    def update_entries(self, *args):
        try:
            if self.scale_x_begin.get() < self.scale_x_end.get() and self.scale_y_begin.get() < self.scale_y_end.get():
                width_value = f"{self.scale_x_begin.get()} - {self.scale_x_end.get()}"
                height_value = f"{self.scale_y_begin.get()} - {self.scale_y_end.get()}"

                self.entry_image_width.config(state='normal')
                self.entry_image_height.config(state='normal')
                self.entry_image_width.delete(0, tk.END)
                self.entry_image_height.delete(0, tk.END)
                self.entry_image_width.insert(0, width_value)
                self.entry_image_height.insert(0, height_value)
                self.entry_image_width.config(state='readonly')
                self.entry_image_height.config(state='readonly')
            else:
                self.errors.config(text="Invalid image size for cropping", background="red")
        except Exception as e:
            self.errors.config(text=f"An Error Occurred: {e}", background="red")

    def save_image(self):
        try:
            image_path = self.input_label.get()
            image = Image.open(image_path)

            crop_dims = (self.scale_x_begin.get(), self.scale_y_begin.get(), self.scale_x_end.get(), self.scale_y_end.get())
            cropped_image = image.crop(crop_dims)

            image_format = self.image_format_var.get().lower()
            save_path = f"Output_Images/cropped_image.{image_format}"
            cropped_image.save(save_path)
            messagebox.showinfo("Success", f"Image saved as {save_path}")
        except Exception as e:
            self.errors.config(text=f"An error occurred: {e}", background="red")



