from tkinter import Tk, Image, Label, Button, Canvas, Frame, BOTTOM, Scale, HORIZONTAL
from PIL import Image
from live_scanner.modules import guiUtils
from live_scanner.modules.screenshotService import ScreenshotService as ScreenshotService
from live_scanner.modules.scanner import Scanner as Scanner
from pynput import mouse
import numpy as np


class GUI:
    def __init__(self):
        self.window: Tk = Tk()
        self.windowWidth: int = int(1800 * guiUtils.getScreenScale(self.window))
        self.windowHeight: int = int(1400 * guiUtils.getScreenScale(self.window))
        self.lastScreenshot: Image = Image.new('RGB', (0, 0))
        self.lastDisplayedImage: Image = Image.new('RGB', (0, 0))
        self.editLoopStopper: bool = False
        self.configLoopStopper: bool = False

        self.window.title("Live scanner")

        screen_width: int = self.window.winfo_screenwidth()
        screen_height: int = self.window.winfo_screenheight()

        self.imagebox: Label = Label(self.window, width=90, height=80)
        self.canvas: Canvas = Canvas(self.window, width=screen_width, height=screen_height, bg='#000000')
        self.rect: int = self.canvas.create_rectangle(0, 0, 0, 0, fill="red")
        self.window.bind('<Configure>', self.updateScreenshotSize)
        self.isMousePressed: bool = False
        self.isSelectionStarted: bool = False
        self.startSelectPosition: tuple[int, int] = (0, 0)
        self.mouseListener: mouse.Listener = mouse.Listener()
        self.colorValues: [np.array, np.array] = np.load('./resources/colors.npy')
        # self.colorValues = [np.array([95, 130, 90]), np.array([180, 255, 255])] // default values

        self.screenshotService: ScreenshotService = ScreenshotService(self.window, self.imagebox)
        self.scanner: Scanner = Scanner(self.colorValues)

        self.createDefaultLayout()
        self.window.mainloop()

    def updateScreenshotSize(self, event):
        self.imagebox.configure(height=event.width)
        if self.lastScreenshot.width != 0:
            img = guiUtils.resizeImageToParentSize(self.lastScreenshot, self.imagebox.winfo_width(),
                                                   self.imagebox.winfo_height())
            guiUtils.changeImage(img, self.imagebox)

    def onChange(self, value, position):
        if position < 3:
            self.colorValues[0][position] = value
        else:
            self.colorValues[1][position - 3] = value

    def saveConfig(self):
        np.save('./resources/colors', self.colorValues)

    def createDefaultLayout(self):
        self.window.overrideredirect(False)
        self.window.wm_state("normal")
        guiUtils.centerOnStart(self.window, self.windowWidth, self.windowHeight)
        frame: Frame = Frame(self.window)
        frame.pack(side=BOTTOM)

        self.imagebox.config(highlightbackground="white", highlightcolor="white", highlightthickness=2)
        self.imagebox.pack(side="top", fill="x", expand=False)

        screenSize = guiUtils.getScreenSize()
        takeButton = Button(frame, width=13, height=3, text="Take a screenshot",
                            command=lambda: self.takeAScreenshot(0, 0, screenSize[0], screenSize[1]))
        takeButton.grid(row=0, column=0, padx=5, pady=5)

        cropButton = Button(frame, width=13, height=3, text="Crop screenshot", command=self.takeACropScreenshot)
        cropButton.grid(row=0, column=1, padx=5, pady=5)

        loadButton = Button(frame, width=13, height=3, text="Load screenshot", command=self.loadImage)
        loadButton.grid(row=0, column=2, padx=5, pady=5)

        editButton = Button(frame, width=13, height=3, text="Start Edit", command=lambda: self.startEdit(editButton))
        editButton.grid(row=0, column=3, padx=5, pady=5)

        saveButton = Button(frame, width=13, height=3, text="Save Screenshot",
                            command=lambda: guiUtils.saveImage(self.lastDisplayedImage))
        saveButton.grid(row=0, column=4, padx=5, pady=5)

        configureButton = Button(frame, width=13, height=3, text="Start Config",
                                 command=lambda: self.startColorConfig(configureButton))
        configureButton.grid(row=0, column=5, padx=5, pady=5)

        saveConfigButton = Button(frame, width=13, height=3, text="Save Config", command=self.saveConfig)
        saveConfigButton.grid(row=0, column=6, padx=5, pady=5)

        s1 = Scale(frame, from_=0, to=179, orient=HORIZONTAL, command=lambda v: self.onChange(v, 0))
        s1.set(self.colorValues[0][0])
        s1.grid(row=0, column=7, padx=5, pady=5)

        s2 = Scale(frame, from_=0, to=255, orient=HORIZONTAL, command=lambda v: self.onChange(v, 1))
        s2.set(self.colorValues[0][1])
        s2.grid(row=1, column=7, padx=5, pady=5)

        s3 = Scale(frame, from_=0, to=255, orient=HORIZONTAL, command=lambda v: self.onChange(v, 2))
        s3.set(self.colorValues[0][2])
        s3.grid(row=0, column=8, padx=5, pady=5)

        s4 = Scale(frame, from_=0, to=179, orient=HORIZONTAL, command=lambda v: self.onChange(v, 3))
        s4.set(self.colorValues[1][0])
        s4.grid(row=1, column=8, padx=5, pady=5)

        s5 = Scale(frame, from_=0, to=255, orient=HORIZONTAL, command=lambda v: self.onChange(v, 4))
        s5.set(self.colorValues[1][1])
        s5.grid(row=0, column=9, padx=5, pady=5)

        s6 = Scale(frame, from_=0, to=255, orient=HORIZONTAL, command=lambda v: self.onChange(v, 5))
        s6.set(self.colorValues[1][2])
        s6.grid(row=1, column=9, padx=5, pady=5)

        self.window.config(bg="systemWindowBackgroundColor")
        self.window.attributes("-alpha", 1)

    def startMouseEvent(self):
        self.mouseListener = mouse.Listener(on_move=self.onMouseMove, on_click=self.onMouseClick)
        self.mouseListener.start()

    def takeAScreenshot(self, fromX: int, fromY: int, toX: int, toY: int):
        self.lastScreenshot = self.screenshotService.take(fromX, fromY, toX, toY)
        guiUtils.changeImage(self.lastScreenshot, self.imagebox)

    def onMouseMove(self, xPos: int, yPos: int):
        if self.isMousePressed:
            self.canvas.coords(self.rect, self.startSelectPosition[0], self.startSelectPosition[1], xPos, yPos)
            self.isSelectionStarted = True
        elif self.isSelectionStarted:
            self.isSelectionStarted = False
            guiUtils.clearLayout(self.window)
            self.createDefaultLayout()
            self.takeAScreenshot(self.startSelectPosition[0], self.startSelectPosition[1], xPos, yPos)
            self.mouseListener.stop()

    def onMouseClick(self, mouse_position_x: int, mouse_position_y: int, button: mouse.Button, is_pressed: bool):
        if button == button.left:
            self.isMousePressed = is_pressed

            if is_pressed:
                self.startSelectPosition = (mouse_position_x, mouse_position_y)

    def takeACropScreenshot(self):
        guiUtils.clearLayout(self.window)

        self.window.overrideredirect(True)
        self.window.wm_state("zoomed")
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.canvas.configure(bg="white")
        self.canvas.coords(self.rect, 0, 0, 0, 0)
        self.canvas.pack()

        self.window.config(bg="white")
        self.window.attributes("-alpha", 0.25)

        self.startMouseEvent()

    def loadImage(self):
        print("load")

    def startEdit(self, button: Button):
        if self.lastScreenshot is not None:
            self.scanner.startScanner()
            self.editLoopStopper = False
            button.config(text="Stop Edit", command=lambda: self.stopEdit(button))
            self.editLoop()

    def stopEdit(self, button: Button):
        self.scanner.stopScanner()
        self.editLoopStopper = True
        button.config(text="Start Edit", command=lambda: self.startEdit(button))

    def editLoop(self):
        if self.editLoopStopper is True:
            return

        capturedImage = Image.fromarray(self.scanner.getFinalImage())
        mergedImages = Image.fromarray(self.scanner.mergeImages(self.lastScreenshot, capturedImage))
        self.lastDisplayedImage = mergedImages

        guiUtils.changeImage(mergedImages, self.imagebox)
        self.imagebox.after(10, lambda: self.editLoop())

    def startColorConfig(self, button: Button):
        self.configLoopStopper = False
        self.scanner.startScanner()
        button.config(text="Stop Config", command=lambda: self.stopColorConfig(button))
        self.colorConfigLoop()

    def stopColorConfig(self, button: Button):
        self.scanner.stopScanner()
        self.configLoopStopper = True
        button.config(text="Start Config", command=lambda: self.startColorConfig(button))

    def colorConfigLoop(self):
        if self.configLoopStopper is True:
            return

        capturedImage = Image.fromarray(self.scanner.getColorsImage(self.colorValues[0], self.colorValues[1]))
        guiUtils.changeImage(capturedImage, self.imagebox)
        self.imagebox.after(10, lambda: self.colorConfigLoop())


gui = GUI()
