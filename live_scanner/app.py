from tkinter import Tk, Image, Label, Button, Canvas, Frame, BOTTOM, Scale, HORIZONTAL
from PIL import Image
from live_scanner.modules.guiUtils import GuiUtils
from live_scanner.modules.screenshotService import ScreenshotService as ScreenshotService
from live_scanner.modules.scannerservice import ScannerService
from pynput import mouse
import numpy as np


class GUI:
    """
        A class is used to create GUI

        Attributes
        ----------
        window: Tk
            Main GUI window
        windowSize: tuple[int, int]
            Size of the main GUI window
        lastScreenshot: Image
            Last screenshot taken(default Image.new('RGB', (0, 0)))
        lastDisplayedImage: Image
            Last image displayed for user(default Image.new('RGB', (0, 0)))
        imageComponent: Label
            Main component in which image is displayed(default Label(self.window, width=90, height=80))
        cropBackground: Canvas
            Background component displayed when taking cropped screenshot(default tkinter.Canvas)
        self.croppingRect: int
            Rect displayed as selected area on cropBackground(default cropBackground.create_rectangle(0, 0, 0, 0, fill="red"))
        startSelectPosition: tuple[int, int]
            Cords of first selected position during cropping(default (0, 0))
        editLoopStopper: bool
            Stopper for editing loop(default False)
        configLoopStopper: bool
            Stopper for config loop(default False)
        isMousePressed: bool
            Status of mouse left button(default False)
        isSelectionStarted: bool
            Status of selection (default False)
        colorValues: [array, array]
            values of configured colors(default np.load('./resources/colors.npy'))
        screenshotService: ScreenshotService
            class responsible for taking screenshots(default ScreenshotService)
        scannerService: ScannerService
            class of camera scanner(default ScannerService)
        mouseListener: mouse.Listener
            class responsible for mouse inputs(default mouseListener)

        Methods
        -------
        updateScreenshotSize(self, event):
            Sets new screenshot size after resizing of window
        onSliderChange(self, value, position):
            Update colors value after changing slider value
        saveConfig(self):
            Saves values of sliders to file
        createDefaultLayout(self):
            Refreshes layout to default layout
        startMouseEvent(self):
            Starts listening on mouse event
        takeAScreenshot(self, fromX: int, fromY: int, toX: int, toY: int):
            Takes new screenshot and displays it on layout
        onMouseMove(self, xPos: int, yPos: int):
            On mouse move
        onMouseClick(self, mouse_position_x: int, mouse_position_y: int, button: mouse.Button, is_pressed: bool):
            On mouse click event
        takeACropScreenshot(self):
            Takes cropped screenshot and displays it on layout
        loadImage(self):
            Loads Image from memory
        startEdit(self, button: Button):
            Starts editing loop
        stopEdit(self, button: Button):
            Stops editing loop
        editLoop(self):
            Loop responsible for refreshing editing based on camera input
        startColorConfig(self, button: Button):
            Starts configuration loop
        stopColorConfig(self, button: Button):
            Stops configuration loop
        colorConfigLoop(self):
            Loop responsible for configuring colors
        """

    def __init__(self):
        self.window: Tk = Tk()
        self.windowSize: tuple[int, int] = \
            (int(1800 * GuiUtils.getScreenScale(self.window)), int(1400 * GuiUtils.getScreenScale(self.window)))
        self.lastScreenshot: Image = Image.new('RGB', (0, 0))
        self.lastDisplayedImage: Image = Image.new('RGB', (0, 0))

        self.imageComponent: Label = Label(self.window, width=90, height=80)
        self.cropBackground: Canvas = Canvas(self.window, width=self.window.winfo_screenwidth(),
                                             height=self.window.winfo_screenheight(), bg='#000000')
        self.croppingRect: int = self.cropBackground.create_rectangle(0, 0, 0, 0, fill="red")
        self.startSelectPosition: tuple[int, int] = (0, 0)
        self.editLoopStopper: bool = False
        self.configLoopStopper: bool = False
        self.isMousePressed: bool = False
        self.isSelectionStarted: bool = False

        self.colorValues: [np.array, np.array] = np.load('./resources/colors.npy')
        self.screenshotService: ScreenshotService = ScreenshotService(self.window, self.imageComponent)
        self.scannerService: ScannerService = ScannerService(self.colorValues)
        self.mouseListener: mouse.Listener = mouse.Listener()

        self.window.title("Live scanner")
        self.window.bind('<Configure>', self.updateScreenshotSize)
        self.createDefaultLayout()
        self.window.mainloop()

    def updateScreenshotSize(self, event: {}):
        """Updates displayed screenshot size according to window size

                Parameters
                ----------
                :param event: dict
                    Passed by default
        """

        self.imageComponent.configure(height=event.width)
        if self.lastScreenshot.width != 0:
            img = GuiUtils.resizeImageToParentSize(self.lastScreenshot, self.imageComponent.winfo_width(),
                                                   self.imageComponent.winfo_height())
            GuiUtils.changeImage(img, self.imageComponent)

    def onSliderChange(self, value, position):
        """Updates color values based on slider change

                        Parameters
                        ----------
                        :param value: int
                            New value from the slider
                        :param position: int
                            Position/index of the slider
        """

        if position < 3:
            self.colorValues[0][position] = value
        else:
            self.colorValues[1][position - 3] = value

    def saveConfig(self):
        """Saves the current color configuration to a file."""

        np.save('./resources/colors', self.colorValues)

    def createDefaultLayout(self):
        """Creates the default layout for the application window."""

        self.window.overrideredirect(False)
        self.window.wm_state("normal")
        GuiUtils.centerOnStart(self.window, self.windowSize[0], self.windowSize[1])
        frame: Frame = Frame(self.window)
        frame.pack(side=BOTTOM)

        self.imageComponent.config(highlightbackground="white", highlightcolor="white", highlightthickness=2)
        self.imageComponent.pack(side="top", fill="x", expand=False)

        screenSize = GuiUtils.getScreenSize()
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
                            command=lambda: GuiUtils.saveImage(self.lastDisplayedImage))
        saveButton.grid(row=0, column=4, padx=5, pady=5)

        configureButton = Button(frame, width=13, height=3, text="Start Config",
                                 command=lambda: self.startColorConfig(configureButton))
        configureButton.grid(row=0, column=5, padx=5, pady=5)

        saveConfigButton = Button(frame, width=13, height=3, text="Save Config", command=self.saveConfig)
        saveConfigButton.grid(row=0, column=6, padx=5, pady=5)

        s1 = Scale(frame, from_=0, to=179, orient=HORIZONTAL, command=lambda v: self.onSliderChange(v, 0))
        s1.set(self.colorValues[0][0])
        s1.grid(row=0, column=7, padx=5, pady=5)

        s2 = Scale(frame, from_=0, to=255, orient=HORIZONTAL, command=lambda v: self.onSliderChange(v, 1))
        s2.set(self.colorValues[0][1])
        s2.grid(row=1, column=7, padx=5, pady=5)

        s3 = Scale(frame, from_=0, to=255, orient=HORIZONTAL, command=lambda v: self.onSliderChange(v, 2))
        s3.set(self.colorValues[0][2])
        s3.grid(row=0, column=8, padx=5, pady=5)

        s4 = Scale(frame, from_=0, to=179, orient=HORIZONTAL, command=lambda v: self.onSliderChange(v, 3))
        s4.set(self.colorValues[1][0])
        s4.grid(row=1, column=8, padx=5, pady=5)

        s5 = Scale(frame, from_=0, to=255, orient=HORIZONTAL, command=lambda v: self.onSliderChange(v, 4))
        s5.set(self.colorValues[1][1])
        s5.grid(row=0, column=9, padx=5, pady=5)

        s6 = Scale(frame, from_=0, to=255, orient=HORIZONTAL, command=lambda v: self.onSliderChange(v, 5))
        s6.set(self.colorValues[1][2])
        s6.grid(row=1, column=9, padx=5, pady=5)

        self.window.config(bg="systemWindowBackgroundColor")
        self.window.attributes("-alpha", 1)

    def startMouseEvent(self):
        """Starts listening to mouse events."""

        self.mouseListener = mouse.Listener(on_move=self.onMouseMove, on_click=self.onMouseClick)
        self.mouseListener.start()

    def takeAScreenshot(self, fromX: int, fromY: int, toX: int, toY: int):
        """Takes a screenshot of the specified area.

                        Parameters
                        ----------
                        :param fromX: int
                            Starting x-coordinate for the screenshot
                        :param fromY: int
                            Starting y-coordinate for the screenshot
                        :param toX: int
                            Ending x-coordinate for the screenshot
                        :param toY: int
                            Ending y-coordinate for the screenshot
        """

        self.lastScreenshot = self.screenshotService.take(fromX, fromY, toX, toY)
        GuiUtils.changeImage(self.lastScreenshot, self.imageComponent)

    def onMouseMove(self, xPos: int, yPos: int):
        """Handles the mouse move event for cropping.

                        Parameters
                        ----------
                        :param xPos: int
                            Current x-coordinate of the mouse
                        :param yPos: int
                            Current y-coordinate of the mouse
        """

        if self.isMousePressed:
            self.cropBackground.coords(self.croppingRect, self.startSelectPosition[0], self.startSelectPosition[1],
                                       xPos, yPos)
            self.isSelectionStarted = True
        elif self.isSelectionStarted:
            self.isSelectionStarted = False
            GuiUtils.clearLayout(self.window)
            self.createDefaultLayout()
            self.takeAScreenshot(self.startSelectPosition[0], self.startSelectPosition[1], xPos, yPos)
            self.mouseListener.stop()

    def onMouseClick(self, mouse_position_x: int, mouse_position_y: int, button: mouse.Button, is_pressed: bool):
        """Handles the mouse click event.

                       Parameters
                       ----------
                       :param mouse_position_x: int
                           x-coordinate of the mouse click
                       :param mouse_position_y: int
                           y-coordinate of the mouse click
                       :param button: mouse.Button
                            element that was clicked
                       :param is_pressed: bool
                           Indicates if the button is pressed
        """

        if button == button.left:
            self.isMousePressed = is_pressed

            if is_pressed:
                self.startSelectPosition = (mouse_position_x, mouse_position_y)

    def takeACropScreenshot(self):
        """Prepares the interface for taking a cropped screenshot."""

        GuiUtils.clearLayout(self.window)

        self.window.overrideredirect(True)
        self.window.wm_state("zoomed")
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.cropBackground.configure(bg="white")
        self.cropBackground.coords(self.croppingRect, 0, 0, 0, 0)
        self.cropBackground.pack()

        self.window.config(bg="white")
        self.window.attributes("-alpha", 0.25)

        self.startMouseEvent()

    def loadImage(self):
        """Loads an image from memory."""

        self.takeAScreenshot(0, 0, 0, 0)

    def startEdit(self, button: Button):
        """Starts the editing loop.

                        Parameters
                        ----------
                        :param button: Button
                            Element that triggered this function
         """

        if self.lastScreenshot is not None:
            self.scannerService.startScanner()
            self.editLoopStopper = False
            button.config(text="Stop Edit", command=lambda: self.stopEdit(button))
            self.editLoop()

    def stopEdit(self, button: Button):
        """Stops the editing loop.

                        Parameters
                        ----------
                        :param button: Button
                            Element that triggered this function
        """

        self.scannerService.stopScanner()
        self.editLoopStopper = True
        button.config(text="Start Edit", command=lambda: self.startEdit(button))

    def editLoop(self):
        """Continuously updates the image being edited."""

        if self.editLoopStopper is True:
            return

        capturedImage = Image.fromarray(self.scannerService.getFinalImage())
        mergedImages = Image.fromarray(self.scannerService.mergeImages(self.lastScreenshot, capturedImage))
        self.lastDisplayedImage = mergedImages

        GuiUtils.changeImage(mergedImages, self.imageComponent)
        self.imageComponent.after(10, lambda: self.editLoop())

    def startColorConfig(self, button: Button):
        """Starts the color configuration loop.

                        Parameters
                        ----------
                        :param button: Button
                            Element that triggered this function
        """

        self.configLoopStopper = False
        self.scannerService.startScanner()
        button.config(text="Stop Config", command=lambda: self.stopColorConfig(button))
        self.colorConfigLoop()

    def stopColorConfig(self, button: Button):
        """Stops the color configuration loop.

                        Parameters
                        ----------
                        :param button: Button
                            Element that triggered this function
        """

        self.scannerService.stopScanner()
        self.configLoopStopper = True
        button.config(text="Start Config", command=lambda: self.startColorConfig(button))

    def colorConfigLoop(self):
        """Continuously updates the image for color configuration."""

        if self.configLoopStopper is True:
            return

        capturedImage = Image.fromarray(self.scannerService.getColorsImage(self.colorValues[0], self.colorValues[1]))
        GuiUtils.changeImage(capturedImage, self.imageComponent)
        self.imageComponent.after(10, lambda: self.colorConfigLoop())


gui = GUI()
