from tkinter import Tk, Label
from PIL import ImageGrab, ImageTk, Image

class GuiUtils:
    """
    A utility class for common GUI operations.

    Methods
    -------
    centerOnStart(win: Tk, windowWidth: int, windowHeight: int):
        Centers the window on the screen at startup.

    getScreenSize():
        Returns the size of the screen.

    getScreenScale(window: Tk):
        Returns the screen scale based on the window.

    clearLayout(window: Tk):
        Clears all widgets from the given window.

    resizeImageToParentSize(img: Image, parentWidth: int, parentHeight: int):
        Resizes an image to fit within the given parent dimensions.

    scaleByWidth(img: Image, parentWidth: int):
        Scales an image to the given width, maintaining aspect ratio.

    scaleByHeight(img: Image, parentHeight: int):
        Scales an image to the given height, maintaining aspect ratio.

    changeImage(image: Image, imagebox: Label):
        Updates the Label widget with the given image.

    saveImage(image):
        Saves the given image to a file.
    """

    @staticmethod
    def centerOnStart(win: Tk, windowWidth: int, windowHeight: int):
        """
        Centers the window on the screen at startup.

        Parameters
        ----------
        :param win: Tk
            The main application window.
        :param windowWidth: int
            The width of the window.
        :param windowHeight: int
            The height of the window.
        """
        w, h = GuiUtils.getScreenSize()[0] * GuiUtils.getScreenScale(win), GuiUtils.getScreenSize()[1] * GuiUtils.getScreenScale(win)
        x = int((w / 2) - (windowWidth / 2))
        y = int((h / 2) - (windowHeight / 2))

        win.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, x, y))

    @staticmethod
    def getScreenSize():
        """
        Returns the size of the screen.

        Returns
        -------
        :return: tuple[int, int]
            Width and height of the screen.
        """
        return ImageGrab.grab().size

    @staticmethod
    def getScreenScale(window: Tk):
        """
        Returns the screen scale based on the window.

        Parameters
        ----------
        :param window: Tk
            The main application window.

        Returns
        -------
        :return: float
            The scale factor of the screen.
        """
        return window.winfo_screenwidth() / GuiUtils.getScreenSize()[0]

    @staticmethod
    def clearLayout(window: Tk):
        """
        Clears all widgets from the given window.

        Parameters
        ----------
        :param window: Tk
            The main application window.
        """
        for widget in window.winfo_children():
            widget.pack_forget()

    @staticmethod
    def resizeImageToParentSize(img: Image, parentWidth: int, parentHeight: int):
        """
        Resizes an image to fit within the given parent dimensions.

        Parameters
        ----------
        :param img: Image
            The image to resize.
        :param parentWidth: int
            The width of the parent container.
        :param parentHeight: int
            The height of the parent container.

        Returns
        -------
        :return: Image
            The resized image.
        """
        if img.width > parentWidth:
            img = GuiUtils.scaleByWidth(img, parentWidth)
        elif img.height > parentHeight:
            img = GuiUtils.scaleByHeight(img, parentHeight)
        else:
            img = GuiUtils.scaleByWidth(img, parentWidth)

        return img

    @staticmethod
    def scaleByWidth(img: Image, parentWidth: int):
        """
        Scales an image to the given width, maintaining aspect ratio.

        Parameters
        ----------
        :param img: Image
            The image to scale.
        :param parentWidth: int
            The width to scale the image to.

        Returns
        -------
        :return: Image
            The scaled image.
        """
        height = int(parentWidth / img.width * img.height)
        return img.resize((parentWidth, height))

    @staticmethod
    def scaleByHeight(img: Image, parentHeight: int):
        """
        Scales an image to the given height, maintaining aspect ratio.

        Parameters
        ----------
        :param img: Image
            The image to scale.
        :param parentHeight: int
            The height to scale the image to.

        Returns
        -------
        :return: Image
            The scaled image.
        """
        width = int(parentHeight / img.height * img.width)
        return img.resize((parentHeight, width))

    @staticmethod
    def changeImage(image: Image, imagebox: Label):
        """
        Updates the Label widget with the given image.

        Parameters
        ----------
        :param image: Image
            The image to display.
        :param imagebox: Label
            The Label widget to update.
        """
        img = ImageTk.PhotoImage(image=image)
        imagebox.config(image=img, width=img.width(), height=img.height())
        imagebox.image = img

    @staticmethod
    def saveImage(image):
        """
        Saves the given image to a file.

        Parameters
        ----------
        :param image: Image
            The image to save.
        """
        image.save("screenshot.png")