import tkinter as tk 
from tkinter import ttk
import sys
import  ttkbootstrap as ttk



from Menu import Menu
# all windows inherit after this theme
window  = ttk.Window(themename="darkly")
window.title("Szkolenie Techniczne")
window.geometry("650x560")
window.minsize(350,300)
menu = Menu(window)
exit_button = ttk.Button(window,width=20,text="EXIT",command=lambda: sys.exit())

menu.pack()
exit_button.pack(side='right',padx=5,pady=5,)

window.mainloop()
