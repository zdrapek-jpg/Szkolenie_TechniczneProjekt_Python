import sys
import ttkbootstrap as ttk
from Menu_Class import  Menu
from Functions import display_screen_size

window  = ttk.Window(themename="vapor")
window.title("Projekt w Pythonie")
from Functions import display_screen_size
x,y,w,h = display_screen_size()


window.geometry(f"{x}x{y}+{w}-{h}")
# przycisk wyjścia
exit_button  = ttk.Button(master =window,text ="Exit", command=lambda :sys.exit())
# całe menu
menu_Wyboru = Menu(window)
menu_Wyboru.pack()

# exit button
exit_button.pack(side='right', pady=2,padx=5)

window.minsize(400,420)



window.mainloop()