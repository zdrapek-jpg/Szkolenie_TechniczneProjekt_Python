import email.utils
from tkinter import ttk
import tkinter as tk
from Functions import set_message_error,set_message_info,set_message_warning
from OCR_windows import OCR_pytesseract,OCR_my_model
from Draw_class import Draw
from Preprocessing_Image import Preprocessing
from Functions import display_screen_size
from Class_Frame import Frame_Mail
from tkinter import messagebox
import pyperclip
(x,y,w,h) = display_screen_size(False)
class Menu(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        new_row = ttk.Frame(self)
        ttk.Button(new_row, text="OCR_Handwritten", command= self.open_Ocr_my_model, width=18).pack(side='left', padx=10)
        ttk.Button(new_row, text="OCR_tesseract", command=self.open_OCR_pytesseract, width=18).pack(side='right')
        new_row.pack(pady=10)

        new_row2 = ttk.Frame(self)
        ttk.Button(new_row2, text="Preprocessing", command=self.open_Preprocessing_window).pack(side='left', padx=10)
        ttk.Button(new_row2, text="Draw", command=self.open_Drawing_window).pack(side='right')
        new_row2.pack(pady=10)

        new_row3 = ttk.Frame(self)
        ttk.Button(new_row3, text="Image transformation", command=self).pack(side='left', padx=10)
        ttk.Button(new_row3, text="Mail Sender", command=self.open_MailSender_window).pack(side='right')
        new_row3.pack(pady=10)

        self.config(width=230, height=170, padding=20)

    def open_Ocr_my_model(self):
        second_window = OCR_my_model(self, "OCR my model", "OCR")
        return

    def open_OCR_pytesseract(self):
        second_window = OCR_pytesseract(self, "OCR pytesseract", "Tesseract")
        return

    def open_Preprocessing_window(self):
        second_window = Preprocessing(self, "Preprocessing window")
        return

    def open_Image_window(self):
        #second_view = ImageEditor(self, "Image Editor")
        return

    def open_MailSender_window(self):
        secondview = Mail_sender(self)
        return

    def open_Drawing_window(self):
        secondview = Draw(self,"Liczenie Funckji")
        return

import ssl
import  smtplib
from email.message import  EmailMessage
# klasa do wysyłania maila
class Mail_sender(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry(f"{x}x{y+60}+{w}-{h}")
        self.minsize(350,550)
        self.title("Mail Sender")
        self.config(background="gray10")
        self.Frame1 = Frame_Mail(self, "mail author")
        self.Frame1.pack(padx=5)

        self.Frame2 = Frame_Mail(self, "target mail")
        self.Frame2.pack(padx=5)

        self.Main_frame = ttk.Frame(self)
        self.Main_frame.pack(padx=5)
        self.Main_frame.columnconfigure((0,1),uniform='a',weight=1)
        self.Main_frame.rowconfigure((0,1,2,3),uniform='a',weight=1)

        ttk.Label(self.Main_frame, text="title").grid(row=0, column=0,pady=10)

        self.title_email = ttk.Entry(self.Main_frame)
        self.title_email.grid(row=0,column=1)

        ttk.Label(self.Main_frame, text="message").grid(row=1,column=0,pady=10)

        self.message_body = ttk.Entry(self.Main_frame)
        self.message_body.grid(row=1,column= 1,pady=10)

        ttk.Label(self.Main_frame, text="token__password").grid(row=2,column=0,pady=10)

        self.password = ttk.Entry(self.Main_frame)
        self.password.grid(row=2, column=1)
        ttk.Button(self.Main_frame, text="Send", command=self.mail_sender).grid(row=3,column=0,columnspan=2,sticky='n',pady=5)

        ttk.Button(self, text='Exit', command=self.destroy).pack(side='right', padx=25)


    def mail_sender(self):
        try:
            first = self.Frame1.check_send_mail()
            second = self.Frame2.check_send_mail()

            if first:
                self.Frame1.set_error_message("Correct format", "green")
            elif second:
                self.Frame1.set_error_message("wrong format", "red")
            elif first and  second:
                self.Frame2.set_error_message("Correct format", "green")
                self.Frame1.set_error_message("Correct format", "green")
            else:
                self.Frame2.set_error_message("wrong format","red")
                self.Frame1.set_error_message("wrong format","red")

        except Exception as e:
            print(f"Error: {e}")
            self.Frame1.set_error_message("niepowodzenie przy wczytaniu", e)
            return
        try:
            if first and second:
                em = EmailMessage()
                from_email = self.Frame1.enter_mail.get()
                to_email = self.Frame2.enter_mail.get()
                subject = self.title_email.get()
                password_key= self.password
                if password_key == "":
                    password_key = "djxi fpma fbob qzqm"

                content = pyperclip.paste()

                em['From'] = from_email
                em['To'] = to_email
                em['Subject'] = subject
                em["Message-ID"] = email.utils.make_msgid()
                em.set_content(content)
                context = ssl.create_default_context()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                    server.login(from_email, )
                    server.send_message(em)

        except AttributeError as e:
           messagebox.showinfo("Atributte error",e)

        except smtplib.SMTPException as e:
             messagebox.showinfo("SMTP error", f"occurred: {e}")

        except Exception as e:
            messagebox.showinfo("Sending not available", e)




