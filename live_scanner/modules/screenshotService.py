import tkinter

import mss as mss
from PIL import Image
from live_scanner.modules import guiUtils


class ScreenshotService:
    def __init__(self, window: tkinter.Tk, imagebox: tkinter.Label):
        self.screen_width, self.screen_height = guiUtils.getScreenSize()
        self.screen_scale: float = guiUtils.getScreenScale(window)
        self.mss_obj: mss = mss.mss()
        self.window = window
        self.imagebox = imagebox

    def take(self, fromX: int, fromY: int, toX: int, toY: int):
        with self.mss_obj as sct:
            monitor = {"top": int(fromY * self.screen_scale),
                       "left": int(fromX * self.screen_scale),
                       "width": int((toX - fromX) * self.screen_scale),
                       "height": int((toY - fromY) * self.screen_scale)}
            raw = sct.grab(monitor)
            img = Image.frombytes("RGB", raw.size, raw.rgb)

            return guiUtils.resizeImageToParentSize(img, self.imagebox.winfo_width(), self.imagebox.winfo_height())
