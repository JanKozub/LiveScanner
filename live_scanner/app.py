import tkinter as tk
from PIL import ImageTk
import screenshotService
import guiUtils

screenshotService = screenshotService.ScreenshotService()
window = tk.Tk()

window.title("Live scanner")
window.resizable(False, False)
guiUtils.centerOnStart(window, 800, 600)

frame = tk.Frame(window)
frame.pack(side=tk.BOTTOM)


def takeAScreenshot():
    image = ImageTk.PhotoImage(screenshotService.take())
    imagebox.config(image=image)
    imagebox.image = image


takeButton = tk.Button(frame, width=30, height=3, text="Take a screenshot", command=takeAScreenshot)
takeButton.pack(side=tk.LEFT, padx=5, pady=5)


def loadAnImage():
    print("2")


loadButton = tk.Button(frame, width=30, height=3, text="Load an image", command=loadAnImage)
loadButton.pack(side=tk.RIGHT, padx=5, pady=5)

imagebox = tk.Label(window, width=700, height=400, text="Image")
imagebox.pack()

window.mainloop()
