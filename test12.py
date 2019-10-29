# importing only those functions 
# which are needed 
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

# creating tkinter window 
root = Tk()

image = Image.open("akiyo.jpg")
image = Image.fromarray(image)
photo = PhotoImage(image)


label = Label(image=photo)
label.image = photo # keep a reference!
label.pack()
mainloop()