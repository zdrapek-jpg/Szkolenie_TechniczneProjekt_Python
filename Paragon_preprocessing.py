import re

import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
class Bill_recognization:
    count = 0
    Bills = []
    def __init__(self,text):
        self.text = text
        Bill_recognization.count+=1
        Bill_recognization.Bills.append(text)
    @classmethod
    def load_images(self):
        # preprocess images from Paragons/paragon0-8 and save output to txt file
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
    def check_similarity(cls,line):

        stemmer = nltk.stem.porter.PorterStemmer()
        remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

        def stem_tokens(tokens):
            return [stemmer.stem(item) for item in tokens]

        def normalize(text):
            return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

        vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

        def cosine_sim(text1, text2):
            tfidf = vectorizer.fit_transform([text1, text2])
            return ((tfidf * tfidf.T).A)[0, 1]

        return cosine_sim("PARAGON FISKALNY", line)

    @classmethod
    def Bill_regex(cls,text):

        #3 działy  :::
        #1 informacje wstępne o  sprzedawcy
        #2 inforamcja na temat zakupów najważniejsza część
        #3 informacje o cenie i o podatkach + data/kod qr

        #podział po nowej lini tak aby odzielić 3 części z czego pierwsza jest do momentu natrafienia na format cenowy
        # split text for lists it there is space  from file
        text=  [tekst for tekst in text.split("\n")]
        outside = []
        i=0
        # if line is not empty add to list of lists
        while i<len(text)-1:
            inside=[]
            for j in range(i,len(text)):
                if text[j]!="" and text[j] !=" " and  text[j] !=None  or len(text[j])>4:
                    inside.append(text[j])
                    i+=1
                else:
                    i+=1
                    break
            if len(inside)>=1:
                outside.append(inside)
        owner = []
        products = []
        poczta = []
        real_items = []


        for i in range(len(outside)):
            for j in range(len(outside[i])):
                line = outside[i][j]
                #cosinus similarity dla Paragonu
                if Bill_recognization.check_similarity(line)>0.7:
                    # next list is empty ald line element is empty
                    line= ""
                    outside[i][j]=""
                    if len(outside[i][j+1:])<=1:
                        real_items.append(outside[i+1])
                        outside[i+1]=""
                    else:
                        for x_indexing in range(len(outside[i][j:])):
                            real_items.append(outside[i][j+x_indexing])

                            outside[i][j+x_indexing]= ""

                elif i ==0 and  line !="":
                    if re.search(r'\d{2}-\d{3}\s+[A-Za-z]+', line):
                        poczta.append(str(line))
                        print(f"poczta:   {line:*^30}")
                        continue
                    # list index  0 is always contain information about owner
                    owner.append(str(line))
                    print(f"info:    {line:_^30}")
                    continue

                #regex to find for example 4,55 A  | 123.00 B
                elif re.search(r'\d+[.,:]\d{0,2}\s?|\.?[A-Z]?', line) and line!="":
                    products.append(str(line))
                    print(f"item:    {line:-^30}")
        try:
            if len(real_items[0]) >= 1:
                for it in real_items[0]:
                    print(f"real_item:  {it:#^30}")
        except:
            print("not found items")
        return [owner,
                products,
                poczta,
                real_items[0]]
#
# print(Bill_recognization.Bill_regex('''ELWAB SA
# UL. SMOLEŃSKA 64
#
# 80-410 GDAŃSK
# Tel: 0483414002 Fax: 0483410350
# NIP. 684-001-04-59
# dn.14r12.21 wydr.1129
# PARAGON FISKALNY
#
# WODA MINERAL. 1,5L 3*2,00=6,00C
# PIZZA 1*5,00=5,00A
# JABŁKA 1,84 * 2,99 = 5,50 B
# RABAT 105 NA JABŁKA -0,55
# PODSUMA 15,95
# RAZEM DO OBNIŻKA ŚWIĄTECZNA 16,50
# RABAT OBNIŻKA ŚWIĄTECZNA -1,65
# RAZEM DO PROM. 3 WCENIE 2 6,00
# RABAT PROM. 3 WCENIE 2 -2,00
# Sp.op.A 4,50 PTU A=22,00% 0,81
# Sp.op.B 4,50 PTU B= 7,00% 0,29
# Sp.op.C 3,40 PTU C= 0,00% 0,00
#
# Razem PTU 1,10
# SUMA PLN 12,30
# ZAPŁACONO GOTÓWKĄ PLN 12,30
# 0036/0041 0130 SZEF 9:48
#
# PL BAQ 00000000
# '''))
#
