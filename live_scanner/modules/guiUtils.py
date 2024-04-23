def centerOnStart(win, w, h):
    x = int((win.winfo_screenwidth() / 2) - (w / 2))
    y = int((win.winfo_screenheight() / 2) - (h / 2))

    win.geometry("{}x{}+{}+{}".format(w, h, x, y))