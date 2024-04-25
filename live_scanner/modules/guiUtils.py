from PIL import ImageGrab

def centerOnStart(win, windowWidth, windowHeight):
    w, h = getScreenSize()[0] * getScreenScale(win), getScreenSize()[1] * getScreenScale(win)
    x = int((w / 2) - (windowWidth / 2))
    y = int((h / 2) - (windowHeight / 2))

    win.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, x, y))


def getScreenSize():
    return ImageGrab.grab().size

def getScreenScale(window):
    return window.winfo_screenwidth() / getScreenSize()[0]