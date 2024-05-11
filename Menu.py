import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from Preprocess_Class import SecondView,Preprocessing,Ocr_Window
import re
import json
import smtplib
import ssl
from email.message import EmailMessage
class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
          # Adjusted size to 450x340
        new_row = ttk.Frame(self)
        ttk.Button(new_row, text="OCR",command=self.open_OCR_window,width=18).pack(side='left',padx=10)
        new_row.pack(pady=10)
        new_row2 = ttk.Frame(self)
        ttk.Button(new_row2, text="Preprocessing",command=self.open_Preprocessing_window).pack(side='left',padx=10)
        ttk.Button(new_row2, text="Draw",command=self.open_Drawing_window).pack(side='left')
        new_row2.pack(pady=10)
        new_row3 = ttk.Frame(self)
        ttk.Button(new_row3, text="Algorithms",command=self.open_Alogrithms_window).pack(side='left',padx=10)
        ttk.Button(new_row3, text="Mail Sender",command=self.open_MailSender_window).pack(side='left')
        new_row3.pack(pady=10)
        self.config(width=230, height=170, padding=20)
    def open_OCR_window(self):
        second_window = Ocr_Window(self,"OCR WINDOW","OCR")
    def open_Preprocessing_window(self):
        second_window = Preprocessing(self,"Preprocessing window", "preprocess")
    def open_Alogrithms_window(self):
        secondview = Algorithms(self)
    def open_MailSender_window(self):
        secondview= Mail_sender(self)
    def open_Drawing_window(self):
        secondview = Draw(self)


class Algorithms(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Algorithms")
        self.geometry("350x450")
        self.minsize(230, 340)
        ttk.Label(self, text="past data", background='gray19').pack()
        ttk.Entry(self).pack(pady=15)
        ttk.Label(self, text="czas", background='gray19').pack()
        ttk.Label(self, text="złożoność", background='gray19').pack(pady=15)
        ttk.Button(self, text="Exit", command=self.destroy).pack(side='bottom', pady=20)
        self.config(background='gray16')


class Draw(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("350x320")
        self.title("Drawing Function")
        self.minsize(230, 200)
        ttk.Entry(self, text="d").pack()
        ttk.Label(self, text="dsg", background='gray18').pack(pady=15)
        ttk.Label(self, text="", background='gray18').pack()
        ttk.Button(self, text='Exit', command=self.destroy).pack(side='bottom', pady=20)
        self.config(background='grey13')


class Frame(ttk.Frame):
    def __init__(self,parent,label_name,button_name,command):
        super().__init__(parent)
        self.config(height=100)
        self.columnconfigure((0,1),uniform="a",weight=1)
        self.rowconfigure((0,1),uniform='a',weight=1)
        self.email = tk.StringVar()
        ttk.Label(self,text=label_name).grid(row=0,column=0)
        self.enter_mail =ttk.Entry(self,textvariable=self.email)
        self.enter_mail.grid(row=0,column=1)
        ttk.Button(self,text=button_name,command=self.get_text_from_label).grid(row=1,rowspan=2)
        self.config(padding=20,borderwidth=20,border=3 )
    def get_text_from_label(self):
        return  self.enter_mail.get()


   # def get_mail(self):



class Mail_sender(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("560x670")
        self.minsize(350,535)
        self.title("Send Mail")
        self.config(background="gray12")
        self.Frame1 = Frame(self,"author mail","check mail",'komenda')
        self.Frame1.pack()
        self.Frame2 = Frame(self,"target mail","check mail",'komenda')
        self.Frame2.pack()
        ttk.Label(self,text="title").pack(pady=15)
        ttk.Entry(self ).pack()
        ttk.Label(self,text="message").pack(pady=15)
        ttk.Entry(self).pack()
        ttk.Label(self, text="special_password").pack(pady=15)

        self.password  =ttk.Entry(self)
        self.password.pack()
        ttk.Button(self,text="Send",command= self.check_send_mail).pack(pady=15)
        ttk.Button(self,text='Exit',command=self.destroy).pack(side='right',padx=25)

    def mail_sender(self):
        # wczytanie informacji
        # obiekt z konta servera  smtp
        sender_email = mail_holder['sender_email']
        password = mail_holder['password']  ### KUUUUUURWAAAAAAAAA
        receiver_email = mail_holder['receiver_email']
        subject = "wiadomość"
        body = f""
        em = EmailMessage()
        em['From'] = sender_email
        em['To'] = receiver_email
        em['subject'] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender_email, 'chip dnwx grdh ozxq')
            server.send_message(em)

    def check_send_mail(self):
        # Access the get_text_from_label method of the Frame instances
        email1 = self.Frame1.get_text_from_label()
        email2 = self.Frame2.get_text_from_label()
        password = self.password.get()
        ### mail
        mailRegex = re.compile(r"""
        ([a-zA-Z0-9._!#$%&+-]+)
        (@)
        ([a-zA-Z0-9._#$%&+-]+)
        """, re.VERBOSE)
        can_send_Mail = True
        for i in email1,email2:
            dopasowania = []
            for grupa in mailRegex.findall(email1):
                string = ""
                for element in grupa:
                    string += element
                dopasowania.append(string)
            if dopasowania!= i:
                Can_send_Mail = False
        if can_send_Mail:
            print("wysyłam maila")
            self.mail_sender()
        else:
            print("nie wysle")
        print("Email 1:", email1)
        print("Email 2:", email2)
        print("password",password)




