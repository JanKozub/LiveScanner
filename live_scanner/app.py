import tkinter as tk
from tkinter import TOP


def centerOnStart(win, w, h):
    x = int((win.winfo_screenwidth() / 2) - (w / 2))
    y = int((win.winfo_screenheight() / 2) - (h / 2))

    win.geometry("{}x{}+{}+{}".format(w, h, x, y))


window = tk.Tk()
window.title("Live scanner")
window.resizable(False, False)
centerOnStart(window, 800, 600)

frame = tk.Frame(window)
frame.place(in_=window, anchor="center", relx=.5, rely=.5)


def takeAScreenshot():
    print("1")


def loadAnImage():
    print("2")


button1 = tk.Button(frame, width=50, height=10, text="Take a screenshot", command=takeAScreenshot)
button1.pack(side=TOP)

button2 = tk.Button(frame, width=50, height=10, text="Load an image", command=loadAnImage)
button2.pack(side=TOP)

window.mainloop()
