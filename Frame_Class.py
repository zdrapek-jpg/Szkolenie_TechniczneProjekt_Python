from tkinter import ttk
import os
from PIL import Image, UnidentifiedImageError
import re

class Frame_Ocr(ttk.Frame):
    def __init__(self, parent, input_label_name, errors_name, button_name, at=False, errors_name_model=None,function="t"):
        super().__init__(parent)
        self.errors_model = None




        self.input_label = ttk.Label(self, text=input_label_name)
        self.input_label.pack(pady=10, padx=10)

        self.input_entry = ttk.Entry(self, text="", validate='focus')
        self.input_entry.pack()
        if function=="t":
            polecenie = self.process_Image_before
        else:
            polecenie = function

        ttk.Button(self, text=button_name, command=polecenie).pack(pady=10, padx=10)

        self.errors = ttk.Label(self, text=errors_name)
        self.errors.pack(pady=10, padx=10)

        if at:
            self.errors_model = ttk.Label(self, text=errors_name_model)
            self.errors_model.pack(pady=10, padx=10)



    def get_input(self):
        return self.input_entry.get()

    def set_error_message(self, text, color):
        self.errors.configure(text=text, background=color)

    def set_error_model(self, text, color):
        if self.errors_model:
            self.errors_model.config(text=text, background=color)

    def process_Image_before(self,function=None):
        input_path = self.get_input()
        if not os.path.exists(input_path):
            self.set_error_message("Nie ma pliku", "red")
            print("Error: File or File Path does not exist")
            return None
        try:
            img = Image.open(input_path)
            img.verify()
            self.set_error_message("plik załadowano", "green")
            if function :
                function()
            return input_path
        except UnidentifiedImageError as e:
            self.set_error_message("file is not valid image", "red")
            print("Error: file is not a valid image", e)
        return None

    def load_model(self):
        model = None
        try:
            from keras.models import load_model
            model = load_model("OCR_Model/mymodel_retrained.h5")
            self.set_error_model("model załadowany prawidłowo", "green")
        except Exception as e:
            print("Error: model not loaded", e)
            self.set_error_model(f"Error: model nie załadowany {e}", "red")
        return model


class Frame_Mail(ttk.Frame):
    def __init__(self,parent,label_name):
        super().__init__(parent)
        self.config(height=100)
        self.columnconfigure((0,1),uniform="a",weight=1)
        self.rowconfigure((0,1),uniform='a',weight=1)

        ttk.Label(self,text=label_name).grid(row=0,column=0)

        self.enter_mail =ttk.Entry(self)
        self.enter_mail.grid(row=0,column=1)

        self.button_check_mail =  ttk.Button(self,text='check_mail',command=lambda : self.set_main_label_info())
        self.button_check_mail.grid(row=1,column=0)

        self.correct_label = ttk.Label(self,text='error')
        self.correct_label.grid(row=1,column=1)


        self.config(padding=20, borderwidth=20, border=3)

    def set_error_message(self,error_main,color):
        self.correct_label.configure(text=error_main,background =color)
        return None
    def get_mail(self):
        return self.enter_mail.get()


    def set_main_label_info(self):
        if self.check_send_mail():
            self.set_error_message("mail correct","green")
            return
        self.set_error_message("mail not correct","red")
    def check_send_mail(self):
        email = self.enter_mail.get()
        # Email regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

