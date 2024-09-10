import tkinter as tk

import imutils
import numpy as np
import pytesseract
from imutils.contours import  sort_contours
from paragons_preprocessing import *
from Frame_Class import Frame_Ocr
from tkinter import ttk
import cv2

import pyperclip
from Functions import display_screen_size

x, y, w, h = display_screen_size(False)
class OCR_my_model(tk.Toplevel):
    def __init__(self, parent, welcome, type):
        super().__init__(parent)
        self.title(welcome)
        self.minsize(320, 420)
        self.geometry(f"{x}x{y}+{w}-{h-200}")
        self.Main = Frame_Ocr(self,f"write filepath to file for {type}","Errors","Load file",True,"Info for Model")
        self.Main.pack()
        ttk.Button(self,text="process",command=lambda: self.process_cv2_my_model()).pack(padx=5,pady=5)
        ttk.Button(self, text="Exit", command=self.destroy).pack(side='bottom', pady=10, padx=15)

    def process_cv2_my_model(self):
        try:
            into = self.Main.process_Image_before()
            model =self.Main.load_model()
            self.Main.set_error_model("model loaded sucessfull ", "green")
            print("udało się sukces")
        except Exception as e :
            print(' nie udało się stop')
            self.Main.set_error_model(f"model not loadaed {e} ","red")
            return None
        image = cv2.imread(into)
        if image is None:
            print("nie załądowano obrazu 2")
            self.Main.set_error_message("image is None","red")
        self.Main.set_error_message("image loadaed","green")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 30, 150)
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sort_contours(cnts, method="left-to-right")[0]
        chars = []

        for c in cnts:

            (x, y, w, h) = cv2.boundingRect(c)

            if (w >= 10 and w <= 150) and (h >= 30 and h <= 160) or (w >= 8 and w <= 180) and (h >= 35 and h <= 120):
                # extract the character and threshold it to make the character
                # appear as *white* (foreground) on a *black* background, then
                #  width and height of the thresholded image
                roi = gray[y:y + h, x:x + w]
                thresh = cv2.threshold(roi, 0, 255,
                                       cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                (tH, tW) = thresh.shape

                if tW > tH:
                    thresh = imutils.resize(thresh, width=32)
                # otherwise, resize along the height
                else:
                    thresh = imutils.resize(thresh, height=32)
                # re-grab the image dimensions (now that its been resized)
                # and then determine how much we need to pad the width and
                # height such that our image will be 32x32
                (tH, tW) = thresh.shape
                dX = int(max(0, 32 - tW) / 2.0)
                dY = int(max(0, 32 - tH) / 2.0)
                # pad the image and force 32x32 dimensions
                padded = cv2.copyMakeBorder(thresh, top=dY, bottom=dY,
                                            left=dX, right=dX, borderType=cv2.BORDER_CONSTANT,
                                            value=(0, 0, 0))
                padded = cv2.resize(padded, (32, 32))
                # prepare the padded image for classification via  handwriting OCR model
                padded = padded.astype("float32") / 255.0
                padded = np.expand_dims(padded, axis=-1)
                chars.append((padded, (x, y, w, h)))

        # extract the bounding box locations and padded characters
        boxes = [b[1] for b in chars]
        chars = np.array([c[0] for c in chars], dtype="float32")
        # OCR the characters using our handwriting recognition model
        preds = model.predict(chars)
        # define the list of label names
        labelNames = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        labelNames = [l for l in labelNames]
        # loop over the predictions and bounding box locations together
        for (pred, (x, y, w, h)) in zip(preds, boxes):
            i = np.argmax(pred)
            prob = pred[i]
            label = labelNames[i]
            # draw the prediction on the image
            print(f"INFO {label}-  {prob * 100}%")
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, label, (x - 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
                # show image
        try:
            cv2.imshow("Image", image)
            cv2.imwrite("Output_Images/boxes.png", image)
            cv2.waitKey(0)
            print("everything done!")
        except Exception as e:
            self.Main.set_error_message(f"exception with {e}","red")

class OCR_pytesseract(tk.Toplevel):
    def __init__(self, parent, welcome, type):
        super().__init__(parent)
        self.title(welcome)
        self.minsize(300,390)
        self.geometry(f"{x}x{y}+{w+350}-{h+50}")
        self.Main = Frame_Ocr(self,f"write filepath to file for {type}","Errors","Load file")
        self.Main.pack()
        ttk.Button(self,text="process", command= lambda:self.cv2_pytesseract_preprocessing()).pack(padx=5,pady=5)
        ttk.Button(self, text="Exit", command=self.destroy).pack(side='bottom', pady=10, padx=15)
    def cv2_pytesseract_preprocessing(self):
        into = self.Main.process_Image_before()
        if into == None:
            return
        try:
            orgin_image = cv2.imread(into)
            image_copy = orgin_image.copy()

            self.Main.set_error_message("image loaded and read successfull ","green")
        except:
            self.Main.set_error_message("image not  readed", "red")
            return None
        image = imutils.resize(image_copy,width=500)
        ratio = orgin_image.shape[1]/float(image.shape[1])

        # convert image to gryscale blur and add edge detection
        gray =cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        image_blurred = cv2.GaussianBlur(gray,(5,5,),0)
        edges = cv2.Canny(image_blurred,76,200)

        #processing countours
        counturs = cv2.findContours(edges.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        counturs = imutils.grab_contours(counturs)
        counturs = sorted(counturs,key=cv2.contourArea,reverse=True)

        for c in counturs:
            #approximate countours
            peri = cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,0.02*peri,True)

            # if we found approximate countour with 4 points we found the outline of recipe
            if len(approx)==4:
                recpipeCountour = approx
                break

        # if the recipe countour is empty  script con't find countours and we shoul be notified
        if recpipeCountour is None:
            self.Main.set_error_message("countours of image not found", "red")
            raise Exception("Counld not found receipt outline ")

        #preprocess image with pytesseract
        output = image.copy()
        cv2.drawContours(output,[recpipeCountour],-1,(0,255,0),2)
        try:
            # Perform OCR on the grayscale image
            text_from_pytesseract = pytesseract.image_to_string(
                cv2.cvtColor(output, cv2.COLOR_BGR2GRAY),
                config="--oem 3 --psm 4 -l pol")
            pyperclip.copy(text_from_pytesseract)
            text = paragon_transoformations.split_paragon(text_from_pytesseract)
            print(paragon_transoformations.patterns_finding(text))


        except:
            self.Main.set_error_message("pytesseract not found or not configured","red")