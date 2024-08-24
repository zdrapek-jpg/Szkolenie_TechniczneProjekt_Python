import tkinter as ttk
import cv2
import numpy as np
from Class_Frame import Frame_Ocr
from Functions import display_screen_size
from rembg import remove

x,y,w,h = display_screen_size(False)

class Preprocessing(ttk.Toplevel):
    def __init__(self,parent,welcome):
        super().__init__(parent)
        self.title(welcome)
        self.minsize(350,450)
        self.geometry(f"{x}x{y}+{w-770}-{h}")
        self.Main = Frame_Ocr(self,"filepath for process image","","Load File")
        self.Main.pack(padx=5,pady=5,ipady=4)

        # grif for menu buttons
        self.MenuFrame= ttk.Frame(self)

        self.MenuFrame.columnconfigure((0,1),pad=10,uniform='a',weight=1)
        self.MenuFrame.rowconfigure((0,1,2),uniform='a',weight=1,pad=5)

        ttk.Button(self.MenuFrame,text="threshold",width=15,
                   command= lambda: self.show_write_process_image("t")).grid(row=0 , column=0)
        ttk.Button(self.MenuFrame, text="no noise", width=15,
                   command=lambda: self.show_write_process_image("n")).grid(row=0, column=1)
        ttk.Button(self.MenuFrame, text="dilated", width=15,
                   command=lambda: self.show_write_process_image("d")).grid(row=1, column=0)
        ttk.Button(self.MenuFrame, text="remove bcg", width=15,
                   command=lambda: self.show_write_process_image("r")).grid(row=1, column=1)
        ttk.Button(self.MenuFrame, text="countours", width=15,
                   command=lambda: self.show_write_process_image("c")).grid(row=2, column=0)
        ttk.Button(self.MenuFrame, text="animated", width=15,
                   command=lambda: self.show_write_process_image("a")).grid(row=2, column=1)


        ttk.Button(self, text="Exit", command=self.destroy).pack(side='bottom', pady=10, padx=15)
        self.MenuFrame.pack(pady=10,padx=10)


    def show_write_process_image(self,parameter_choice):
        into = self.Main.process_Image_before()

        if into ==None :
            self.Main.set_error_message("path is empty youre stuck","blue")
        text_path = into.split('.')[0]
        text = text_path.split("/")[-1]
        image_to_save =None
        into = cv2.imread(into)

        if parameter_choice == "t":
            gray_image = cv2.cvtColor(into,cv2.COLOR_BGR2GRAY)
            _, image_to_save = cv2.threshold(gray_image,140,255,cv2.THRESH_BINARY)
            print("Threshold")
            header = "threshold_image"

        if parameter_choice=="n":
            kernal = np.ones((1,1),np.uint8)
            image = cv2.dilate(into,kernal,iterations=1)
            image = cv2.erode(image,kernal,iterations=1)
            image = cv2.morphologyEx(image,cv2.MORPH_CLOSE,kernal)
            image_to_save = cv2.medianBlur(image,3)
            header = "no_noise"
            print("no noise")

        if parameter_choice == "d":
            kernal = np.ones((2,2),np.uint8)
            image_to_save = cv2.dilate(into,kernal,iterations=1)
            header = "dilated"
            print("dilated")

        if parameter_choice == "r":
            try:
                output = remove(into)
                output = np.array(output)
                image_to_save = output
                header = "remove_background"
            except ModuleNotFoundError as e:
                self.Main.set_error_message(f"rembg not found {e}","red")
                print("brak biblioteki ")

        elif parameter_choice == "c":
            gray = cv2.cvtColor(into, cv2.COLOR_BGR2GRAY)
            gray_blur = cv2.medianBlur(gray, 3)
            image_to_save = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9,7)
            header = "contours"
            print("Contours")

        elif parameter_choice == "a":
            blur_value = 7
            line_size = 11
            total_color = 20

            gray = cv2.cvtColor(into,cv2.COLOR_BGR2GRAY)
            gray_blur = cv2.medianBlur(gray,blur_value)
            edges = cv2.adaptiveThreshold(gray_blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,line_size,blur_value)
            data = np.float32(into).reshape(-1,3)
            criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,10,0.001)

            # K MEANS ALGORITHM
            ret, label, center = cv2.kmeans(data,total_color,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
            center = np.uint8(center)
            result = center[label.flatten()]
            image_to_save = result.reshape(into.shape)

            #correct bilateralFilter call
            blurred = cv2.bilateralFilter(image_to_save,7,200,200)
            image_to_save = cv2.bitwise_and(blurred,blurred,mask=edges)
            header = "animated"
            print("animated")
        cv2.imwrite(f"Output_Images/{text}_{header}.png",image_to_save)
        cv2.imshow(header,image_to_save)
        cv2.waitKey(0)
        cv2.destroyAllWindows()








