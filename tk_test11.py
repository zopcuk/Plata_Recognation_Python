from tkinter import *
from tkinter import ttk
import threading
from PIL import Image, ImageTk
import cv2
import process
from datetime import datetime
from tkinter import messagebox
import time

cap = cv2.VideoCapture(0)


class App(threading.Thread):

    def __init__(self, tk_frame):
        self.frame = tk_frame
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        try:
            while root.winfo_exists():
                global cap
                ret, frame1 = cap.read()
                if ret:
                    #print(frame.winfo_width())
                    frame2 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame2)
                    img = img.resize((frame.winfo_width(), frame.winfo_height()), Image.BICUBIC)
                    tkimage1 = ImageTk.PhotoImage(img)
                    video_label.configure(image=tkimage1)
                    video_label.image = tkimage1
                    video_label.pack(anchor=NW, expand=TRUE)
                elif root.winfo_exists():
                    #messagebox.showerror(title='Camera disconnect', message='Please check camera connection.')
                    answer = messagebox.askretrycancel("Camera disconnect", "Do you want to try that again?")
                    if answer:
                        cap = cv2.VideoCapture(0)
                    else:
                        quit_()
                root.protocol("WM_DELETE_WINDOW", destroy_)
                if root.winfo_exists():
                    root.update()
        except:
            pass


class App2(threading.Thread):
    def __init__(self, tk_namelbl):
        self.namelbl = tk_namelbl
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        i=0
        try:
            while root.winfo_exists():
                print("1")
                global cap
                ret, frame3 = cap.read()
                #print(frame3.shape)
                if ret:
                    frame3, screenCnt, detected = process.pre_proc(frame3)
                    if detected==1:
                        PlateText, PlateCrop = process.reading(frame3, screenCnt)
                        if PlateText != None:
                            now = datetime.now()
                            s1 = now.strftime("%m/%d/%Y--%H:%M:%S")
                            print(PlateText)
                            tree.insert('', 0, 'plate{}'.format(i), text=PlateText, values=s1)
                            i+=1
                            img = cv2.cvtColor(PlateCrop, cv2.COLOR_BGR2RGB)
                            img = Image.fromarray(img)
                            img1 = img.resize((217, 50), Image.ANTIALIAS)
                            tkimage2 = ImageTk.PhotoImage(img1)
                            namelbl.configure(image=tkimage2)
                            namelbl.image = tkimage2
                            namelbl.pack()
                #root.protocol("WM_DELETE_WINDOW", destroy_)
                root.update()
        except:
            pass

'''class App3(threading.Thread):

    def __init__(self, tk_frame):
        self.frame = tk_frame
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.start()
    def stop(self):
        self.event.set()

    def run(self):
        while True:
            if root.winfo_exists() != 1:
                print("1")'''


def quit_():
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.quit()

def destroy_():
    quit_()
    return None






root = Tk()


root.geometry("750x400")
root.minsize(750, 400)
content = ttk.Frame(root, padding=(3,3,3,3))
frame = ttk.Frame(content)
video_label = Label(frame)
#video_label.image=""


img1 = Image.open('bekleniyor.jpg')
img1 = img1.resize((275, 60), Image.ANTIALIAS)
#img1 = img1.resize((400, 80), Image.ANTIALIAS)
tkimage1 = ImageTk.PhotoImage(img1)

namelbl1 = ttk.Label(content)
namelbl = ttk.Label(namelbl1, image=tkimage1)
namelbl.pack()
#name = ttk.Entry(content,width=36)



tree = ttk.Treeview(content, columns=('date'))
tree.heading('#0',text="Plaka")
tree.heading('#1',text="Date")
tree.column('#0',minwidth=100,width=100)
tree.column('#1',minwidth=100,width=150)

'''for i in range(30):
    tree.insert('', 0, 'plate{}'.format(i), text="10DM897-{}".format(i), values=s1)'''

'''tree.insert('',0,'plate0', text='10DM817', values=s1)
tree.insert('',1,'plate1', text='12ABC123', values=s1)
tree.insert('',2,'plate2', text='85hn25', values=s1)
tree.insert('',3,'plate3', text='85hn25', values=s1)
tree.insert('',4,'plate4', text='85hn25', values=s1)'''

#tree.insert('episodes',1,text='Episodes 82',values=('Jan. 8, 2019',))


ok = ttk.Button(content, text="Okay")
cancel = ttk.Button(content, text="Cancel")

content.grid(column=0, row=0, sticky=(N, S, E, W))
frame.grid(column=0, row=0, columnspan=5, rowspan=4, sticky=(N, S, E, W), padx=5, pady=5)
#video_label.grid(column=0, row=0, columnspan=5, rowspan=2, sticky=(N, S, E, W))
namelbl1.grid(column=5, row=0, columnspan=2, sticky=(N, W, E, S), padx=5, pady=5)
tree.grid(column=5, row=1, columnspan=2, sticky=(N, W, E, S), pady=5, padx=5)
#name.grid(column=5, row=1, columnspan=2, sticky=(N, W), pady=5, padx=5)
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
#APP3 = App3(frame)
root.mainloop()