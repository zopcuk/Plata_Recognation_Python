from tkinter import *
from tkinter import ttk
import threading
from PIL import Image, ImageTk
import cv2
import process
cap = cv2.VideoCapture(0)
class App(threading.Thread):

    def __init__(self, tk_frame):
        self.frame = tk_frame
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        while True:
            global cap
            ret, frame1 = cap.read()
            if ret:

                frame2 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame2)
                #img = img.resize((300, 300), Image.BICUBIC)
                tkimage1 = ImageTk.PhotoImage(img)
                video_label.configure(image=tkimage1)
                video_label.image = tkimage1
                video_label.pack(anchor=NW, expand=TRUE)

class App2(threading.Thread):
    def __init__(self, tk_namelbl):
        self.namelbl = tk_namelbl
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        while True:
            global cap
            ret, frame3 = cap.read()
            if ret:
                frame3, screenCnt, detected = process.pre_proc(frame3)
                if detected==1:
                    PlateText, PlateCrop = process.reading(frame3, screenCnt)
                    if PlateText != None:
                        print(PlateText)
                        img = cv2.cvtColor(PlateCrop, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(img)
                        img1 = img.resize((217, 50), Image.ANTIALIAS)
                        tkimage2 = ImageTk.PhotoImage(img1)
                        namelbl.configure(image=tkimage2)
                        namelbl.image = tkimage2
                        namelbl.pack()

root = Tk()

#APP2 = App2(root)


content = ttk.Frame(root,padding=(3,3,12,12))
frame = ttk.Frame(content,width=200, height=100)
video_label = Label(frame)
#video_label.image=""


namelbl1 = ttk.Label(content)
namelbl = ttk.Label(namelbl1)
name = ttk.Entry(content,width=36)

ok = ttk.Button(content, text="Okay")
cancel = ttk.Button(content, text="Cancel")

content.grid(column=0, row=0, sticky=(N, S, E, W))
frame.grid(column=0, row=0, columnspan=5, rowspan=4, sticky=(N, S, E, W))
#video_label.grid(column=0, row=0, columnspan=5, rowspan=2, sticky=(N, S, E, W))
namelbl1.grid(column=5, row=0, columnspan=2, sticky=(N, W), padx=5)
name.grid(column=5, row=1, columnspan=2, sticky=(N, W), pady=5, padx=5)

ok.grid(column=5, row=3)
cancel.grid(column=6, row=3)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)

APP = App(frame)
APP2 = App2(namelbl)

root.mainloop()