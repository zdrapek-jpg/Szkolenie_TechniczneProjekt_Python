import os

import pyautogui


# Check Existance of files and their paths (relative)
def find_file(filename,path):
    i=0
    for root,dir,files in os.walk(path):
        if filename in files:
            return os.path.join(root,filename)

        for d in dir:
            for root2,dir2,files2 in os.walk(os.path.join(root,d)):
                if filename in files:
                    return os.path.join(root2, filename)

    return None

#Check Existance of directories and their paths (relative)
def find_dir(dir_name,path):
    for root,dir,files in os.walk(path):
        if dir_name in dir:
            return os.path.join(root,dir_name)
    return None


from tkinter import messagebox
# set message box and label color after
def set_message_error(name, info :  str)-> memoryview:
    messagebox.showerror(name,info)
    return
def set_message_info(name, info :  str)-> memoryview:
    messagebox.showinfo(name,info)
    return
def set_message_warning(name, info :  str)-> memoryview:
    messagebox.showwarning(name,info)
    return

# screen sizes and display in front
def display_screen_size(main=True):
    import pyautogui
    screen_width ,screen_height  = pyautogui.size()
    center_x = int(screen_width/4)
    center_y = int(screen_height/4)
    if main:
        return [center_x -100,int(center_y / 2 - 100),center_x+100,200]
    return [center_x-100 ,int(center_y / 2 - 100),center_x+500,250]




#check regular expression for mail regex
import re
def regex_for_mail(mail :str) -> bool:
    pattern =r'^[a-zA-Z0-9_+=&*%$#@!]{4,}@[A-Za-z0-9]+\.[a-zA-Z0-9]{2,}$'
    return re.match(pattern, mail) is  not None


import math

# Function to create a dictionary from the text
def dict_from_text(pattern: str) -> dict:
    dictionary = {}
    for char in pattern.lower():
        if char in dictionary:
            dictionary[char] += 1
        else:
            dictionary[char] = 1
    if ' ' in dictionary:
        del dictionary[' ']
    return dictionary
print(dict_from_text("PTU B"))
print(dict_from_text("SUMA PTU"))
print(dict_from_text("SUMA PLN"))
print(dict_from_text("SPRZEDAŻ OPODATKOWANA A"))
print(dict_from_text("Sprzed. opod PTU A"))
# Function to create vectors from two dictionaries
def vectorization(dict1: dict, dict2: dict) -> tuple:
    all_keys = set(dict1.keys()).union(set(dict2.keys()))
    vector1 = [dict1.get(key, 0) for key in all_keys]
    vector2 = [dict2.get(key, 0) for key in all_keys]
    return vector1, vector2


# Function to calculate cosine similarity between two vectors
def cos_similarity(vectors: tuple) -> float:
    vector1, vector2 = vectors

    # Calculate dot product
    dot_product = sum(v1 * v2 for v1, v2 in zip(vector1, vector2))

    # Calculate magnitudes
    magnitude1 = math.sqrt(sum(v1 ** 2 for v1 in vector1))
    magnitude2 = math.sqrt(sum(v2 ** 2 for v2 in vector2))

    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    # Calculate and return cosine similarity
    return dot_product / (magnitude1 * magnitude2)



# Assercje sprawdzające czy wszystkie pliki potrzebne znajdują się w danej lokalizacji

assert(find_file('Tests.py','C:\Program Files\Pulpit\Projekt Szkolenie Techniczne'))==  "C:\Program Files\Pulpit\Projekt Szkolenie Techniczne\Tests.py"
assert(find_dir('OCR_Model','C:\Program Files\Pulpit\Projekt Szkolenie Techniczne\\'))==  "C:\Program Files\Pulpit\Projekt Szkolenie Techniczne\OCR_Model"
assert(find_dir('Images','C:\Program Files\Pulpit\Projekt Szkolenie Techniczne\\'))==  "C:\Program Files\Pulpit\Projekt Szkolenie Techniczne\Images"
assert(find_dir('Output_Images','C:\Program Files\Pulpit\Projekt Szkolenie Techniczne\\'))==  "C:\Program Files\Pulpit\Projekt Szkolenie Techniczne\Output_Images"
assert(find_file("paragon6.jpg",'C:\Program Files\Pulpit\Projekt Szkolenie Techniczne\\'))=="C:\Program Files\Pulpit\Projekt Szkolenie Techniczne\Paragons\paragon6.jpg"
assert(find_file('mymodel_retrained.h5','C:\Program Files\Pulpit\Projekt Szkolenie Techniczne\\'))=="C:\Program Files\Pulpit\Projekt Szkolenie Techniczne\OCR_Model\mymodel_retrained.h5"

# Assercje dla Maili
assert(regex_for_mail("pawelek1929wp.pl")) == False
assert(regex_for_mail("paw@gmil.om")) == False
assert(regex_for_mail("ankas1969@gmai.com"))== True
assert(regex_for_mail("pawel1@o2.pl"))==True

