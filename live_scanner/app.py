from tkinter import Tk, Image, Label, Button, Canvas, Frame, BOTTOM
from PIL import Image
from live_scanner.modules import guiUtils
from live_scanner.modules.screenshotService import ScreenshotService as ScreenshotService
from live_scanner.modules.scanner import Scanner as Scanner
from pynput import mouse


class GUI:
    def __init__(self):
        self.window: Tk = Tk()
        self.windowWidth: int = int(1800 * guiUtils.getScreenScale(self.window))
        self.windowHeight: int = int(1400 * guiUtils.getScreenScale(self.window))
        self.scanner: Scanner = Scanner()
        self.lastScreenshot: Image = None
        self.lastDisplayedImage: Image = None
        self.editLoopStopper: bool = False

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
        self.mouseListener: mouse.Listener

        self.screenshotService: ScreenshotService = ScreenshotService(self.window, self.imagebox)

        self.createDefaultLayout()
        self.window.mainloop()

    def updateScreenshotSize(self, event):
        self.imagebox.configure(height=event.width)
        if self.lastScreenshot is not None:
            img = guiUtils.resizeImageToParentSize(self.lastScreenshot, self.imagebox.winfo_width(),
                                                   self.imagebox.winfo_height())
            guiUtils.changeImage(img, self.imagebox)

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

        saveButton = Button(frame, width=13, height=3, text="Save",
                            command=lambda: guiUtils.saveImage(self.lastDisplayedImage))
        saveButton.grid(row=0, column=4, padx=5, pady=5)

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
            button.config(text="Stop Edit", command=lambda: self.stopEditImage(button))
            self.editLoop()

    def stopEditImage(self, button: Button):
        self.scanner.stopScanner()
        self.editLoopStopper = True
        button.config(text="Start Edit", command=lambda: self.startEdit(button))

    def editLoop(self):
        if self.editLoopStopper is True:
            return

        capturedImage = Image.fromarray(self.scanner.getImage())
        mergedImages = Image.fromarray(self.scanner.mergeImages(self.lastScreenshot, capturedImage))
        self.lastDisplayedImage = mergedImages

        guiUtils.changeImage(mergedImages, self.imagebox)
        self.imagebox.after(10, lambda: self.editLoop())


gui = GUI()
