import json
import re
import smtplib
import ssl
import tkinter as tk
import pyperclip
from email.message import EmailMessage
from tkinter import ttk, messagebox

import numpy as np
import ttkbootstrap as ttk

from Preprocess_Class import Preprocessing, OCR_tesseract, OCR_Window
from sympy import symbols, solve, sympify
import time



class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
          # Adjusted size to 450x340
        new_row = ttk.Frame(self)
        ttk.Button(new_row, text="OCR_Handwritten",command=self.open_OCR_window,width=18).pack(side='left',padx=10)
        new_row.pack(pady=10)
        ttk.Button(new_row, text="OCR_tesseract", command=self.open_Ocr_tesseract, width=18).pack(side='left', padx=10)
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
        # model
    def open_OCR_window(self):
        second_window = OCR_Window(self,"OCR window","OCR")
        #done
    def open_Ocr_tesseract(self):
        second_window = OCR_tesseract(self,"OCR_tesseract","Tesseract")
        #almost done
    def open_Preprocessing_window(self):
        second_window = Preprocessing(self,"Preprocessing window", "preprocess")
        # not done
    def open_Alogrithms_window(self):
        secondview = Algorithms(self)
        # done
    def open_MailSender_window(self):
        secondview= Mail_sender(self)
        #not done
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

        def bubble_sort(self,data):
            start = time.time()
            n = len(data)
            for i in range(n):
                for j in range(0, n - i - 1):
                    if data[j] > data[j + 1]:
                        data[j], data[j + 1] = data[j + 1], data[j]
            end = time.time()
            return data,(end-start)

        def merge_sort(arr):
            start =time.time()
            if len(arr) <= 1:
                return arr

            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]

            left_half = merge_sort(left_half)
            right_half = merge_sort(right_half)
            sorted_arr = merge(left_half, right_half)
            end = time.time()
            return sorted_arr, end - start

        def merge(self, left, right):
            result = []
            left_idx, right_idx = 0, 0

            while left_idx < len(left) and right_idx < len(right):
                if left[left_idx] < right[right_idx]:
                    result.append(left[left_idx])
                    left_idx += 1
                else:
                    result.append(right[right_idx])
                    right_idx += 1

            result.extend(left[left_idx:])
            result.extend(right[right_idx:])
            end = time.time()
            return result
        def quick_sort(self,arr):
            start =time.time()

            if len(arr) <= 1:
                return arr

            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]

            sorted_arr = left + middle + right
            end = time.time()
            return sorted_arr, end- start

        def algorithms(self):
            pass




from matplotlib import pyplot as plt
class Draw(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("330x400")
        self.title("Drawing Function")
        self.minsize(230, 300)

        self.framefunction = ttk.Frame(self)
        self.framefunction.pack(padx=10,pady=10)
        self.label_function = ttk.Label(master=self.framefunction, text="wzór funkcji 1 zmienna", background='gray18')
        self.label_function.pack(side='left', pady=15)
        self.input_function =ttk.Entry(self.framefunction)
        self.input_function.pack(pady=10,padx=10, side="left")

        self.frame   =ttk.Frame(self)
        self.frame.pack(pady=10,padx=10)
        self.label_x = ttk.Label(master=self.frame, text="przedział na x min,max", background='gray18')
        self.label_x.pack(side='left',pady=15)
        self.entry = ttk.Entry(self.frame)
        self.entry.pack(side="left",padx=5,pady=5)

        ttk.Button(self,text="draw",command=lambda:self.process_function()).pack(padx=10,pady=10)
        self.zero_write = ttk.Label(self, text="", background='gray18')
        self.zero_write.pack(pady=15)
        self.min_max =  ttk.Label(self, text="", background='gray18')
        self.min_max.pack()
        ttk.Button(self, text='Exit', command=self.destroy).pack(side='bottom', pady=20)
        self.config(background='grey13')
    def set_error_message(self,error,message):
        messagebox.showinfo(error, message)
        return None


    def process_function(self):
        function_eqasion = self.input_function.get()
        try:
            x = self.entry.get().split(",")
            print(float(x[0]),float(x[1]))

            x_sym = np.linspace(int(x[0]),int(x[1]),100)
        except ValueError:
            self.set_error_message("ValueError","dane muszą być 2 liczbamiz przecinkiem -10,-3")
            return None

        try:
            # Convert string expression to a function of x


            # Use re.search to find the first variable in the equation
            pattern = re.search(r'x|z|q|m|y', function_eqasion)
            y = [eval(function_eqasion, {"x": val, "np": np}) for val in x_sym]
        except Exception as e:
            self.set_error_message('Error',"błąd, nie znaleziono zmiennej")
        try:
            if pattern:
                # Extract the variable found
                variable = pattern.group()
                print(f"Variable found: {variable}")
                x = symbols(variable)

                # Convert the string equation to a sympy expression
                expression = sympify(function_eqasion)

                # Solve the equation
                result = solve(expression, x)
                self.zero_write.config(text=f"{result}")
            else: self.zero_write.config(text= "brak miejsc zerowych")
            print(y)




            x_min, x_max = min(x_sym), max(x_sym)
            y_min, y_max = min(y), max(y)
            self.min_max.config(text=f"max : {y_max}  \n min : {y_min}")

            fig, ax = plt.subplots()

            ax.plot(x_sym, y, color='green')
            ax.plot(x_sym, [0 for i in range(len(y))], color='orange')
            ax.set_xlim(x_min-2, x_max+1)
            ax.set_ylim(y_min-5, y_max+5 )

            plt.show()

        except Exception as e:
            self.set_error_message(e,"błąd w rysowaniu funkcji "+e)

class Frame(ttk.Frame):
    def __init__(self,parent,label_name,button_name):
        super().__init__(parent)
        self.config(height=100)
        self.columnconfigure((0,1),uniform="a",weight=1)
        self.rowconfigure((0,1),uniform='a',weight=1)
        self.email = tk.StringVar()
        ttk.Label(self,text=label_name).grid(row=0,column=0)

        self.enter_mail =ttk.Entry(self,textvariable=self.email)
        self.enter_mail.grid(row=0,column=1)

        self.button_check_mail =  ttk.Button(self,text='check_mail',command=lambda : self.check_mail())
        self.button_check_mail.grid(row=1,column=0)

        self.correct_label = ttk.Label(self,text='')
        self.correct_label.grid(row=1,column=1)


        self.config(padding=20, borderwidth=20, border=3)

    def set_error_message(self,error_main,information):
        messagebox.showinfo(error_main, information)
    def check_mail(self):
        if self.check_send_mail(self.enter_mail.get()):
            self.correct_label.config(text="Correct format", background="green")
            return True
        self.correct_label.config(text="incorrect format", background="red")
        return False
    def check_send_mail(self, email):
        # Email regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None




class Mail_sender(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("560x670")
        self.minsize(350,535)
        self.title("Send Mail")
        self.config(background="gray12")
        self.Frame1 = Frame(self,"mail author","check mail")
        self.Frame1.pack()
        self.Frame2 = Frame(self,"target mail","check mail")
        self.Frame2.pack()
        ttk.Label(self,text="title").pack(pady=15)
        self.title_email = ttk.Entry(self ).pack()
        ttk.Label(self,text="message").pack(pady=15)
        self.message_body = ttk.Entry(self).pack()
        ttk.Label(self, text="special_password").pack(pady=15)

        self.password  =ttk.Entry(self)
        self.password.pack()
        ttk.Button(self,text="Send",command= self.mail_sender).pack(pady=15)
        ttk.Button(self,text='Exit',command=self.destroy).pack(side='right',padx=25)
    def mail_sender(self):
        try:
            with open("Email_config/email.json", "r") as email_file:
                mail_holder = json.load(email_file)
        except Exception as e:
            self.Frame1.set_error_message("configuration", f"Error reading configuration file: {e}")
            return

        try:
            first =self.Frame1.check_mail()
            if first:
                self.Frame1.correct_label.config(text="Correct format", background="green")
                flag = True
            else:
                self.Frame1.correct_label.config(text="wrong format", background="red")
            second = self.Frame2.check_mail()
            if second:
                self.Frame2.correct_label.config(text="Correct format", background="green")
                flag2 = True
            else:
                self.Frame2.correct_label.config(text="wrong format", background="red")

        except Exception as e:
            print(f"Error: {e}")
            self.Frame1.set_error_message("niepowodzenie przy wczytaniu",e)
            return
        try:
            if first and second :
                em = EmailMessage()
                em['From'] = self.Frame1.enter_mail.get()
                em['To'] = self.Frame2.enter_mail.get()
                # do sprawdzenia co pobiera
                em['Subject'] = self.title_email.get()
                if self.title_email.get() ==None or self.title_email.get() =="":
                    em['Subject'] = pyperclip.copy()
                em.set_content(self.message_body.get())
                print(self.Frame1.enter_mail.get()+"\n"+self.Frame2.enter_mail.get()+"\n"+self.title_email.get()+"\n"+self.message_body.get())
                context = ssl.create_default_context()
                # poczta emeil musi być otwarta na aplikacje i posiadać toked ktory należy uzupełnić,to nie hasło do poczty
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                    server.login(self.Frame1.enter_mail.get(), self.password.get())
                    server.send_message(em)

        except AttributeError as e:
            self.Frame1.set_error_message("Attribute Error", f"function or call   with  {e}")
        except smtplib.SMTPException as e:
            self.Frame1.set_error_message("Error", f"SMTP error occurred: {e}")
        except NameError:
            self.Frame1.set_error_message("Error with smtp","Authentication error: check import smtp ")
        except Exception as e:
            print(f"Error sending email not available: {e}")
            self.Frame1.set_error_message("sending not available",e)








