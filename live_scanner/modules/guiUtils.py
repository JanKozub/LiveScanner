import tkinter

from PIL import ImageGrab, ImageTk


def centerOnStart(win: tkinter.Tk, windowWidth: int, windowHeight: int):
    w, h = getScreenSize()[0] * getScreenScale(win), getScreenSize()[1] * getScreenScale(win)
    x = int((w / 2) - (windowWidth / 2))
    y = int((h / 2) - (windowHeight / 2))

    win.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, x, y))


def getScreenSize():
    return ImageGrab.grab().size


def getScreenScale(window: tkinter.Tk):
    return window.winfo_screenwidth() / getScreenSize()[0]


def clearLayout(window: tkinter.Tk):
    for widget in window.winfo_children():
        widget.pack_forget()


def changeImage(image: tkinter.Image, imagebox: tkinter.Label):
    img = ImageTk.PhotoImage(image=image)
    imagebox.config(image=img, width=img.width(), height=img.height())
    imagebox.image = img


def saveImage(image):
    image.save("screenshot.png")
