import pyperclip
import re
class Bill_recognization:
    count = 0
    Bills = []
    def __init__(self,text):
        self.text = text
        Bill_recognization.count+=1
        Bill_recognization.Bills.append(text)
    @classmethod
    def load_images(self):
        for  i in range(0,8):
            # import form Preprocess_Class.py
            text = OCR_tesseract.cv2And_pytesseract_preprocessing(f"Paragons/paragon{i}.jpg")
            Bill_recognization.Bills.append(text)
            if text == None or len(text) < 10:
                text == "None"

        with open("tesseract_paragons_recognization.txt", "w",encoding="utf-8") as file_open:

            for line in Bill_recognization.Bills:
                file_open.write(line + '\n\n\n\n\n')
    @classmethod
    def Bill_regex(cls,text):

        #3 działy  :::
        #1 informacje wstępne o  sprzedawcy
        #2 inforamcja na temat zakupów najważniejsza część
        #3 informacje o cenie i o podatkach + data/kod qr
        #podział po nowej lini tak aby odzielić 3 części z czego pierwsza jest do momentu natrafienia na format cenowy
        t= [line for line in  text.split("\n") if len(line)>2]
        return t



t = """ 
80-410 GDAŃSK
Tel: 0483414002 Fax: 0483410350
NIP. 684-001-04-59
dn.14r12.21 wydr.1129
PARAGON FISKALNY

WODA MINERAL. 1,5L 3*2,00=6,00C
PIZZA 1*5,00=5,00A
JABŁKA 1,84 * 2,99 = 5,50 B
RABAT 105 NA JABŁKA -0,55
PODSUMA 15,95
RAZEM DO OBNIŻKA ŚWIĄTECZNA 16,50
RABAT OBNIŻKA ŚWIĄTECZNA -1,65
RAZEM DO PROM. 3 WCENIE 2 6,00
RABAT PROM. 3 WCENIE 2 -2,00
Sp.op.A 4,50 PTU A=22,00% 0,81
Sp.op.B 4,50 PTU B= 7,00% 0,29
Sp.op.C 3,40 PTU C= 0,00% 0,00

Razem PTU 1,10
SUMA PLN 12,30
ZAPŁACONO GOTÓWKĄ PLN 12,30
0036/0041 0130 SZEF 9:48

PL BAQ 00000000 """

print(Bill_recognization.Bill_regex(t))