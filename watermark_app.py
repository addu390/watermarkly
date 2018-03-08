from tkinter import *
#from Tkinter import *
from PIL import Image
from PIL import ImageTk
#import tkFileDialog
from tkinter import filedialog
import cv2
from imutils import paths
import numpy as np
import os

watermark = cv2.imread('/home/adesh/Downloads/02_Computer_Vision_A_Z_Template_Folder/01_all_Modules/watermark/example.png', cv2.IMREAD_UNCHANGED)
(wH, wW) = watermark.shape[:2]

(B, G, R, A) = cv2.split(watermark)
B = cv2.bitwise_and(B, B, mask=A)
G = cv2.bitwise_and(G, G, mask=A)
R = cv2.bitwise_and(R, R, mask=A)
watermark = cv2.merge([B, G, R, A])

def select_image():
    global panelA, panelB
    path = filedialog.askopenfilename()

    if len(path) > 0:
        image = cv2.imread(path)
        (h, w) = image.shape[:2]
        image = np.dstack([image, np.ones((h, w), dtype="uint8") * 255])
        overlay = np.zeros((h, w, 4), dtype="uint8")
        overlay[h - wH - 10:h - 10, w - wW - 10:w - 10] = watermark
        edged = image.copy()
        cv2.addWeighted(overlay, 0.25, edged, 1.0, 0, edged)
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)
        image = ImageTk.PhotoImage(image)
        edged = ImageTk.PhotoImage(edged)

        if panelA is None or panelB is None:
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)
            panelB = Label(image=edged)
            panelB.image = edged
            panelB.pack(side="right", padx=10, pady=10)

        else:
            panelA.configure(image=image)
            panelB.configure(image=edged)
            panelA.image = image
            panelB.image = edged

root = Tk()
panelA = None
panelB = None
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
root.mainloop()