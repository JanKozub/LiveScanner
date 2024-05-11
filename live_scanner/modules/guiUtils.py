from tkinter import Tk, Label
from PIL import ImageGrab, ImageTk, Image


def centerOnStart(win: Tk, windowWidth: int, windowHeight: int):
    w, h = getScreenSize()[0] * getScreenScale(win), getScreenSize()[1] * getScreenScale(win)
    x = int((w / 2) - (windowWidth / 2))
    y = int((h / 2) - (windowHeight / 2))

    win.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, x, y))


def getScreenSize():
    return ImageGrab.grab().size


def getScreenScale(window: Tk):
    return window.winfo_screenwidth() / getScreenSize()[0]


def clearLayout(window: Tk):
    for widget in window.winfo_children():
        widget.pack_forget()


def resizeImageToParentSize(img: Image, parentWidth: int, parentHeight: int):
    if img.width > parentWidth:
        img = scaleByWidth(img, parentWidth)
    elif img.height > parentHeight:
        img = scaleByHeight(img, parentHeight)
    else:
        img = scaleByWidth(img, parentWidth)

    return img


def scaleByWidth(img: Image, parentWidth: int):
    height = int(parentWidth / img.width * img.height)

    return img.resize((parentWidth, height))


def scaleByHeight(img: Image, parentHeight: int):
    width = int(parentHeight / img.height * img.width)

    return img.resize((parentHeight, width))


def changeImage(image: Image, imagebox: Label):
    img = ImageTk.PhotoImage(image=image)
    imagebox.config(image=img, width=img.width(), height=img.height())
    imagebox.image = img


def saveImage(image):
    image.save("screenshot.png")
