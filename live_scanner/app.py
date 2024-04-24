import tkinter as tk
from PIL import ImageTk
from live_scanner.modules import screenshotService, guiUtils

# screenWidth, screenHeight = guiUtils.getScreenSize()
# windowWidth, windowHeight = int(screenWidth * 0.8), int((screenWidth * 0.8) / 16 * 9)
windowWidth, windowHeight = 1920, 1080
screenshotWidth, screenshotHeight = int(windowWidth * 0.9), int(((windowWidth * 0.8) / 16) * 9)

print(screenshotWidth, screenshotHeight)

screenshotService = screenshotService.ScreenshotService()

window = tk.Tk()
window.title("Live scanner")
window.resizable(False, False)
guiUtils.centerOnStart(window, windowWidth, windowHeight)

frame = tk.Frame(window)
frame.pack(side=tk.BOTTOM)


def takeAScreenshot():
    image = ImageTk.PhotoImage(screenshotService.take(screenshotWidth, screenshotHeight))
    imagebox.config(image=image)
    imagebox.image = image


takeButton = tk.Button(frame, width=30, height=3, text="Take a screenshot", command=takeAScreenshot)
takeButton.pack(side=tk.LEFT, padx=5, pady=5)


def loadAnImage():
    print("todo load")


loadButton = tk.Button(frame, width=30, height=3, text="Load an image", command=loadAnImage)
loadButton.pack(side=tk.RIGHT, padx=5, pady=5)

imagebox = tk.Label(window, width=screenshotWidth, height=screenshotHeight, text="Image")
imagebox.pack()

window.mainloop()
