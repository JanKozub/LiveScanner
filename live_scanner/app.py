import tkinter as tk
from PIL import Image, ImageTk
from live_scanner.modules import screenshotService, guiUtils, scanner
from pynput import mouse


class GUI:
    def __init__(self):
        # self.windowWidth = int(1800 * guiUtils.getScreenScale(self.window))
        # self.windowHeight = int(1400 * guiUtils.getScreenScale(self.window))
        self.windowWidth = 800
        self.windowHeight = 600

        self.window = tk.Tk()
        self.screenshotService = screenshotService.ScreenshotService(int(self.windowWidth * 0.9))
        self.scanner = scanner.Scanner()
        self.lastScreenshot = None
        self.lastDisplayedImage = None
        self.editLoopStopper = False

        self.window.title("Live scanner")
        self.window.resizable(False, False)

        self.imagebox = None
        self.canvas = None
        self.rect = None
        self.isMousePressed = False
        self.startSelectPosition = (0, 0)
        self.isSelectionStarted = False
        self.mouseListener = mouse.Listener(
            on_move=self.onMouseMove,
            on_click=self.onMouseClick)
        self.mouseListener.start()

        self.createDefaultLayout()
        self.window.mainloop()

    def createDefaultLayout(self):
        guiUtils.centerOnStart(self.window, self.windowWidth, self.windowHeight)
        frame = tk.Frame(self.window)
        frame.pack(side=tk.BOTTOM)

        self.imagebox = tk.Label(self.window, width=90, height=80, text="Image")
        self.imagebox.config(highlightbackground="white", highlightcolor="white", highlightthickness=2)
        self.imagebox.pack()

        takeButton = tk.Button(frame, width=13, height=3, text="Take a screenshot",
                               command=lambda: self.takeAScreenshot(0, 0,
                                                                    guiUtils.getScreenSize()[0],
                                                                    guiUtils.getScreenSize()[1]))
        takeButton.grid(row=0, column=0, padx=5, pady=5)

        cropButton = tk.Button(frame, width=13, height=3, text="Crop screenshot", command=self.takeACropScreenshot)
        cropButton.grid(row=0, column=1, padx=5, pady=5)

        loadButton = tk.Button(frame, width=13, height=3, text="Load screenshot", command=self.loadImage)
        loadButton.grid(row=0, column=2, padx=5, pady=5)

        editButton = tk.Button(frame, width=13, height=3, text="Start Edit",
                               command=lambda: self.startEditImage(editButton))
        editButton.grid(row=0, column=3, padx=5, pady=5)

        saveButton = tk.Button(frame, width=13, height=3, text="Save", command=self.saveImage)
        saveButton.grid(row=0, column=4, padx=5, pady=5)

        self.window.config(bg="black")
        self.window.attributes("-alpha", 1)

    def clearLayout(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def takeAScreenshot(self, fromX, fromY, toX, toY):
        self.lastScreenshot = self.screenshotService.take(fromX, fromY, toX, toY)
        image = ImageTk.PhotoImage(self.lastScreenshot)
        self.imagebox.config(image=image, width=image.width(), height=image.height())
        self.imagebox.image = image

    def onMouseMove(self, xPos, yPos):
        if self.isMousePressed:
            self.canvas.coords(self.rect, self.startSelectPosition[0], self.startSelectPosition[0], xPos, yPos)

            self.isSelectionStarted = True
        elif self.isSelectionStarted is True:
            self.isSelectionStarted = False
            self.clearLayout()
            self.createDefaultLayout()
            self.takeAScreenshot(self.startSelectPosition[0], self.startSelectPosition[1], xPos, yPos)

    def onMouseClick(self, mouse_position_x, mouse_position_y, button, is_pressed):
        if button == button.left:
            self.isMousePressed = is_pressed

            if is_pressed:
                self.startSelectPosition = (mouse_position_x, mouse_position_y)

    def takeACropScreenshot(self):
        self.clearLayout()

        self.window.overrideredirect(True)
        self.window.wm_state("zoomed")
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.canvas = tk.Canvas(self.window, width=screen_width, height=screen_height, bg='#000000')
        self.canvas.configure(bg="white")
        self.canvas.pack()
        self.rect = self.canvas.create_rectangle(0, 0, 0, 0, fill="red")

        self.window.config(bg="white")
        self.window.attributes("-alpha", 0.25)

    def loadImage(self):
        print("load")

    def startEditImage(self, button):
        if self.lastScreenshot is not None:
            self.scanner.startScanner()
            self.editLoopStopper = False
            button.config(text="Stop Edit", command=lambda: self.stopEditImage(button))
            self.editLoop()

    def stopEditImage(self, button):
        self.scanner.stopScanner()
        self.editLoopStopper = True
        button.config(text="Start Edit", command=lambda: self.startEditImage(button))

    def editLoop(self):
        if self.editLoopStopper is True:
            return

        capturedImage = Image.fromarray(self.scanner.getImage())
        mergedImages = Image.fromarray(self.scanner.mergeImages(self.lastScreenshot, capturedImage))
        self.lastDisplayedImage = mergedImages

        frame = ImageTk.PhotoImage(image=mergedImages)
        self.imagebox.config(image=frame)
        self.imagebox.image = frame
        self.imagebox.after(10, lambda: self.editLoop())

    def saveImage(self):
        self.lastDisplayedImage.save("screenshot.png")


gui = GUI()
