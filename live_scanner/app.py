import tkinter as tk
from PIL import Image, ImageTk
from live_scanner.modules import screenshotService, guiUtils, scanner


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.screenshotService = screenshotService.ScreenshotService()
        self.scanner = scanner.Scanner()
        self.displayedImage = None

        windowWidth, = int(1920 * guiUtils.getScreenScale(self.window))
        windowHeight = int(1080 * guiUtils.getScreenScale(self.window))
        screenshotWidth, screenshotHeight = int(windowWidth * 0.9), int(((windowWidth * 0.8) / 16) * 9)

        self.window.title("Live scanner")
        self.window.resizable(False, False)
        self.window.minsize(width=windowWidth, height=windowHeight)
        guiUtils.centerOnStart(self.window, windowWidth, windowHeight)

        frame = tk.Frame(self.window)
        frame.pack(side=tk.BOTTOM)

        self.takeButton = tk.Button(frame, width=30, height=3, text="Take a screenshot",
                                    command=lambda: self.takeAScreenshot(screenshotWidth, screenshotHeight))
        self.takeButton.pack(side=tk.LEFT, padx=5, pady=5)

        self.loadButton = tk.Button(frame, width=30, height=3, text="Load", command=self.loadImage)
        self.loadButton.pack(side=tk.RIGHT, padx=5, pady=5)

        self.editButton = tk.Button(frame, width=30, height=3, text="Edit", command=self.editImage)
        self.editButton.pack(side=tk.RIGHT, padx=5, pady=5)

        self.imagebox = tk.Label(self.window, width=screenshotWidth, height=screenshotHeight, text="Image")
        self.imagebox.pack()

        self.window.mainloop()

    def takeAScreenshot(self, w, h):
        self.displayedImage = self.screenshotService.take(w, h)
        image = ImageTk.PhotoImage(self.displayedImage)
        self.imagebox.config(image=image)
        self.imagebox.image = image

    def loadImage(self):
        print("load")

    def editImage(self):
        if self.displayedImage is not None:
            self.scanner.startScanner()
            capturedImage = Image.fromarray(self.scanner.getImage())
            mergedImages = Image.fromarray(self.scanner.mergeImages(self.displayedImage, capturedImage))

            frame = ImageTk.PhotoImage(image=mergedImages)
            self.imagebox.config(image=frame)
            self.imagebox.image = frame

            self.imagebox.after(10, self.editImage)


gui = GUI()
