import tkinter as tk
from tkinter import ttk
import cv2
import keras
import sympy
from rembg import remove
import ttkbootstrap as ttk
from PIL import Image, UnidentifiedImageError
import imutils
import pytesseract
import os
import numpy as np
import pyperclip
from imutils.contours import sort_contours
from  keras.models import load_model
class OCR_tesseract(tk.Toplevel):
    def __init__(self,parent,welcome,type):
        super().__init__(parent)
        self.title(welcome)
        self.geometry("400x450")
        self.minsize(340,280)
        ttk.Label(self,text=f"write filepath to file for {type}").pack(pady=10,padx=10)
        self.input_label = ttk.Entry(self, text="",validate='focus')
        self.input_label.pack()
        ttk.Button(self, text="Load file", command= lambda:self.cv2And_pytesseract_preprocessing()).pack(pady=10, padx=10)
        ttk.Button(self, text="Exit", command=self.destroy).pack(side='bottom', pady=10,padx=15)
        self.config(padx=10,pady=10)
        self.errors =  ttk.Label(self,text="")
        self.errors.pack(pady=10, padx=10)


    @classmethod
    def processImage(self,input_label,errors):
        into = input_label.get()
        if not os.path.exists(into):
            errors.config(text="Error: The file or file path does not exist",background="red")
            print("Error: The file does not exist")
            return None

        try:
            img = Image.open(into)
            img.verify()  # Verify that it is an image
            return into
        except UnidentifiedImageError:
            errors.config(text="Error: The file is not a valid image",background="red")
            print("Error: The file is not a valid image")

        except Exception as e:
            errors.config(text=f"An unexpected error occurred: {e}",background="red")
            print(f"An unexpected error occurred: {e}")
        return None

    def cv2And_pytesseract_preprocessing(self):
        into = self.processImage(self.input_label,self.errors)
        if into==None:
            return
        try:
            # preprocessing
            orig = cv2.imread(into)
            image = orig.copy()

            self.errors.config(text="Image loaded successfully", background="green")
        except:
            self.errors.config(text="error with processing, cv2", background="red")
            return None
        image = imutils.resize(image, width=500)
        ratio = orig.shape[1] / float(image.shape[1])
        # convert the image to grayscale, blur it slightly, and then apply
        # edge detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
        edged = cv2.Canny(blurred, 75, 200)
        # check to see if we should show the output of our edge detection
        # procedure
        debug = 1
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        # initialize a contour that corresponds to the receipt outline
        receiptCnt = None
        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # if our approximated contour has four points, then we can
            # assume we have found the outline of the receipt
            if len(approx) == 4:
                receiptCnt = approx
                break
        # if the receipt contour is empty then our script could not find the
        # outline and we should be notified
        if receiptCnt is None:
            self.errors.configure(
                text="Could not find receipt outline.Try debugging your edge detection and contour steps.",
                background="red")
            raise Exception(("Could not find receipt outline. "
                            "Try debugging your edge detection and contour steps."))
            # check to see if we should draw the contour of the receipt on the
            # image and then display it to our screen
        if debug > 0:
            output = image.copy()
            cv2.drawContours(output, [receiptCnt], -1, (0, 255, 0), 2)
        options = "--oem 3 --psm 4 -l pol"
        try:
            text = pytesseract.image_to_string(
                cv2.cvtColor(output, cv2.COLOR_BGR2RGB),
                config=options)
            self.input_label.config(text=str(text))

        except:
            self.errors.config(text= "tesseract in not found or wrong configured",background="red")
            pass

        print(text)
        if len(text)<2:
            self.errors.config(text="there in no data that war read from image ",background="red")
            return
        pyperclip.copy(text)



class OCR_Window(tk.Toplevel):
    def __init__(self,parent,welcome,type):
        super().__init__(parent)
        self.title(welcome)
        self.geometry("400x450")
        self.minsize(340, 280)
        ttk.Label(self, text=f"write filepath to file for {type}").pack(pady=10, padx=10)
        self.input_label = ttk.Entry(self, validate='focus')
        self.input_label.pack()
        ttk.Button(self, text="Load file",command= lambda: self.process_with_ocr()).pack(pady=10, padx=10)
        ttk.Button(self, text="Exit", command=self.destroy).pack(side='bottom', pady=10, padx=15)
        self.config(padx=10, pady=10)
        self.model = ttk.Label(self, text="")
        self.model.pack(pady=10, padx=10)
        self.errors = ttk.Label(self, text="")
        self.errors.pack(pady=10, padx=10)


    def process_with_ocr(self):
        try:
            model = load_model("OCR_model/mymodel_retrained.h5")
            self.model.config(text ="Model loaded successfully",background="green")
        except Exception as e:
            print("Error", f"Error loading model: {e}")
            self.model.config(text="Model load fail", background="red")
            return

        image_path = OCR_tesseract.processImage(self.input_label,self.errors)

        image = cv2.imread(image_path)

        if image is None:
            print(f"Error: Unable to read image at {image_path}")
            self.errors.config(text=f"Unable to read file {image_path}", background="red")
            return

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

            if (w >= 10 and w <= 150) and (h >= 30 and h <= 120) or (w >= 8 and w <= 150) and (h >= 35 and h <= 120):
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
            cv2.imwrite("Output_Images/boxes.png",image )
            cv2.waitKey(0)
            self.model.config(text ="Model loaded successfully",background='green')
            self.errors.config(text="no errors")
        except Exception as e :
            self.errors.config(text=f"exception with {e}")



class SecondView(tk.Toplevel):
    def __init__(self, parent, welcome, type):
        super().__init__(parent)
        self.title(welcome)
        self.geometry("400x450")
        self.minsize(340, 280)
        ttk.Label(self, text=f"write filepath to file for {type}").pack(pady=10, padx=10)
        self.input_label = ttk.Entry(self)
        self.input_label.pack()
        self.check_image = ttk.Button(self, text="Load file", command=self.process_image)
        self.check_image.pack(pady=10, padx=10)
        ttk.Button(self, text="Exit", command=self.destroy).pack(side='bottom', pady=10, padx=15)
        self.config(padx=10, pady=10)
        self.errors = ttk.Label(self, text='')
        self.errors.pack(pady=10, padx=10)

    def process_image(self):
        into = self.input_label.get()

        if not os.path.exists(into):
            self.errors.config(text="Error: The file or file path does not exist")
            print("Error: The file does not exist")
            return None

        try:
            #verify the image
            img = Image.open(into)
            img.verify()
            img = cv2.imread(into)
            self.errors.config(text="Image loaded successfully")
            return img
        except UnidentifiedImageError:
            self.errors.config(text="Error: The file is not a valid image")
            print("Error: The file is not a valid image")
        except Exception as e:
            self.errors.config(text=f"An unexpected error occurred: {e}")
            print(f"An unexpected error occurred: {e}")
        return None

class Preprocessing(SecondView):
    def __init__(self, parent, welcome, type):
        super().__init__(parent, welcome, type)
        self.Menu_Frame = ttk.Frame(self, padding=10)
        self.minsize(300, 460)
        #grid configuration
        self.Menu_Frame.columnconfigure((0, 1), pad=10, uniform='a', weight=1)
        self.Menu_Frame.rowconfigure((0, 1, 2), uniform='a', weight=1, pad=5)

        ttk.Button(self.Menu_Frame, text="Threshold", width=12,
                   command=lambda: self.show_write_Processing("threshold")).grid(row=0, column=0)
        ttk.Button(self.Menu_Frame, text="No noise", width=12,
                   command=lambda: self.show_write_Processing("no_noise")).grid(row=0, column=1)
        ttk.Button(self.Menu_Frame, text="Dilated", width=12,
                   command=lambda: self.show_write_Processing("dilated")).grid(row=1, column=0)
        ttk.Button(self.Menu_Frame, text="Remove background", width=12,
                   command=lambda: self.show_write_Processing("remove_background")).grid(row=1, column=1)
        ttk.Button(self.Menu_Frame, text="Contours", width=12,
                   command=lambda: self.show_write_Processing("eroded")).grid(row=2, column=0)
        ttk.Button(self.Menu_Frame, text="Animated", width=12,
                   command=lambda: self.show_write_Processing("animated")).grid(row=2, column=1)
        self.Menu_Frame.pack(padx=10, pady=5)
    def show_write_Processing(self, function):
        image = self.process_image()
        if image is None:
            return
        text =self.input_label.get().split('.')[0]

        if function == "threshold":
            print("Threshold")
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, im_bw = cv2.threshold(gray_image, 140, 255, cv2.THRESH_BINARY)
            cv2.imwrite(f"Output_Images/{text}bw_image.png", im_bw)
            cv2.imshow("Threshold Image", im_bw)  # Show image
            cv2.waitKey(0)

        elif function == "no_noise":
            print("No noise")
            kernel = np.ones((1, 1), np.uint8)
            image = cv2.dilate(image, kernel, iterations=1)
            image = cv2.erode(image, kernel, iterations=1)
            image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
            image = cv2.medianBlur(image, 3)
            cv2.imwrite(f"Output_Images/{text}no_noise.png", image)
            cv2.imshow("No Noise Image", image)
            cv2.waitKey(0)


        elif function == "dilated":
            print("Dilated")
            kernel = np.ones((2, 2), np.uint8)
            dilated_image = cv2.dilate(image, kernel, iterations=1)
            cv2.imwrite(f"Output_Images/{text}dilated_image.png", dilated_image)
            cv2.imshow("Dilated Image", dilated_image)
            cv2.waitKey(0)


        elif function == "remove_background":
            print("Remove background")
            try:
                output = remove(image)
                output = np.array(output)
                cv2.imwrite(f"Output_Images/{text}removed_bg.png", output)
                cv2.imshow("Removed Background", output)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            except ModuleNotFoundError:
                self.errors.config(text="Error: Library 'rembg' not found")
                print("Library 'rembg' not found")

        elif function == "eroded":
            print("Eroded")
            kernel = np.ones((2, 2), np.uint8)
            eroded_image = cv2.erode(image, kernel, iterations=1)
            cv2.imwrite(f"Output_Images/{text}eroded_image.png", eroded_image)
            cv2.imshow("Eroded Image", eroded_image)
            cv2.waitKey(0)


        elif function == "animated":
            print("Animated")
            # Config
            blur_value = 7
            line_size = 11


            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_blur = cv2.medianBlur(gray, blur_value)
            edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size,
                                          blur_value)

            data = np.float32(image).reshape((-1, 3))
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.001)
            total_color = 20

            # K-Means
            ret, label, center = cv2.kmeans(data, total_color, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            center = np.uint8(center)
            result = center[label.flatten()]
            img = result.reshape(image.shape)

            # correct bilateralFilter call
            blurred = cv2.bilateralFilter(img, 7, 200, 200)

            cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

            # savee cartoon image
            cv2.imwrite(f"Output_Images/{text}animated_image.png", cartoon)

            # display cartoon image
            cv2.imshow("Cartoon look like image", cartoon)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            self.errors.config(text="Unknown processing function", background="red")

