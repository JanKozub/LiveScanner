import tkinter as tk
from PIL import Image, ImageTk
from live_scanner.modules import screenshotService, guiUtils, scanner


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.screenshotService = screenshotService.ScreenshotService()
        self.scanner = scanner.Scanner()
        self.lastScreenshot = None
        self.lastDisplayedImage = None
        self.editLoopStopper = False

        windowWidth = int(1920 * guiUtils.getScreenScale(self.window))
        windowHeight = int(1080 * guiUtils.getScreenScale(self.window))
        screenshotWidth, screenshotHeight = int(windowWidth * 0.9), int(((windowWidth * 0.8) / 16) * 9)

        self.window.title("Live scanner")
        self.window.resizable(False, False)
        self.window.minsize(width=windowWidth, height=windowHeight)
        guiUtils.centerOnStart(self.window, windowWidth, windowHeight)

        frame = tk.Frame(self.window)
        frame.pack(side=tk.BOTTOM)

        self.takeButton = tk.Button(frame, width=20, height=3, text="Take a screenshot",
                                    command=lambda: self.takeAScreenshot(screenshotWidth, screenshotHeight))
        self.takeButton.grid(row=0, column=0, padx=5, pady=5)

        self.editButton = tk.Button(frame, width=20, height=3, text="Start Edit", command=self.startEditImage)
        self.editButton.grid(row=0, column=1, padx=5, pady=5)

        self.saveButton = tk.Button(frame, width=20, height=3, text="Save", command=self.saveImage)
        self.saveButton.grid(row=0, column=2, padx=5, pady=5)

        self.loadButton = tk.Button(frame, width=20, height=3, text="Load", command=self.loadImage)
        self.loadButton.grid(row=0, column=3, padx=5, pady=5)

        self.imagebox = tk.Label(self.window, width=screenshotWidth, height=screenshotHeight, text="Image")
        self.imagebox.pack()

        self.window.mainloop()

    def takeAScreenshot(self, w, h):
        self.lastScreenshot = self.screenshotService.take(w, h)
        image = ImageTk.PhotoImage(self.lastScreenshot)
        self.imagebox.config(image=image)
        self.imagebox.image = image

    def loadImage(self):
        print("load")

    def startEditImage(self):
        if self.lastScreenshot is not None:
            self.scanner.startScanner()
            self.editLoopStopper = False
            self.editButton.config(text="Stop Edit", command=self.stopEditImage)
            self.editLoop()

    def stopEditImage(self):
        self.scanner.stopScanner()
        self.editLoopStopper = True
        self.editButton.config(text="Start Edit", command=self.startEditImage)

    def editLoop(self):
        if self.editLoopStopper is True:
            return

        capturedImage = Image.fromarray(self.scanner.getImage())
        mergedImages = Image.fromarray(self.scanner.mergeImages(self.lastScreenshot, capturedImage))
        self.lastDisplayedImage = mergedImages

        frame = ImageTk.PhotoImage(image=mergedImages)
        self.imagebox.config(image=frame)
        self.imagebox.image = frame
        self.imagebox.after(10, self.editLoop)

    def saveImage(self):
        self.lastDisplayedImage.save("screenshot.png")


gui = GUI()
