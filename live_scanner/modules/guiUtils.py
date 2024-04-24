from screeninfo import get_monitors


def centerOnStart(win, windowWidth, windowHeight):
    w, h = getScreenSize()
    x = int((w / 2) - (windowWidth / 2))
    y = int((h / 2) - (windowHeight / 2))

    win.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, x, y))


def getScreenSize():
    for m in get_monitors():
        if m.is_primary:
            return m.width, m.height
