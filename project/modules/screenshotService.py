from tkinter import Tk, Label
import mss
from PIL import Image
from project.modules.guiUtils import GuiUtils


class ScreenshotService:
    """
    A class used to handle taking screenshots.

    Attributes
    ----------
    screen_width : int
        The width of the screen.
    screen_height : int
        The height of the screen.
    screen_scale : float
        The scale factor of the screen.
    mss_obj : mss.mss
        The MSS object for screen capturing.
    window : Tk
        The main application window.
    imagebox : Label
        The Label widget to display images.

    Methods
    -------
    take(fromX: int, fromY: int, toX: int, toY: int):
        Takes a screenshot of the specified area and resizes it to fit the image box.
    """

    def __init__(self, window: Tk, imagebox: Label):
        """
        Initializes the ScreenshotService with the provided window and image box.

        Parameters
        ----------
        :param window : Tk
            The main application window.
        :param imagebox : Label
            The Label widget to display images.
        """

        self.screen_width, self.screen_height = GuiUtils.getScreenSize()
        self.screen_scale: float = GuiUtils.getScreenScale(window)
        self.mss_obj: mss = mss.mss()
        self.window = window
        self.imagebox = imagebox

    def take(self, fromX: int, fromY: int, toX: int, toY: int):
        """
        Takes a screenshot of the specified area and resizes it to fit the image box.

        Parameters
        ----------
        :param fromX : int
            The starting x-coordinate of the screenshot area.
        :param fromY : int
            The starting y-coordinate of the screenshot area.
        :param toX : int
            The ending x-coordinate of the screenshot area.
        :param toY : int
            The ending y-coordinate of the screenshot area.

        Returns
        -------
        :return Image
            The screenshot resized to fit the image box.
        """

        with self.mss_obj as sct:
            monitor = {"top": int(fromY * self.screen_scale),
                       "left": int(fromX * self.screen_scale),
                       "width": int((toX - fromX) * self.screen_scale),
                       "height": int((toY - fromY) * self.screen_scale)}
            raw = sct.grab(monitor)
            img = Image.frombytes("RGB", raw.size, raw.rgb)
            return GuiUtils.resizeImageToParentSize(img, self.imagebox.winfo_width(), self.imagebox.winfo_height())
