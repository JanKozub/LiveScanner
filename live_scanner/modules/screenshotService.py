import mss as mss
from PIL import Image
from live_scanner.modules import guiUtils


class ScreenshotService:
    def __init__(self, windowWidth, windowHeight, window):
        self.screen_width, self.screen_height = guiUtils.getScreenSize()
        self.screen_scale = guiUtils.getScreenScale(window)
        self.mss_obj = mss.mss()
        self.frameWidth = int(windowWidth * 0.9)
        self.frameHeight = int(windowHeight * 0.9)

    def take(self, fromX, fromY, toX, toY):
        with self.mss_obj as sct:
            monitor = {"top": fromY * self.screen_scale, "left": fromX * self.screen_scale,
                       "width": toX * self.screen_scale, "height": toY * self.screen_scale}
            raw = sct.grab(monitor)
            img = Image.frombytes("RGB", raw.size, raw.rgb)

            if img.width > self.frameWidth:
                height = int(self.frameWidth / img.width * img.height)
                img = img.resize((self.frameWidth, height))
            elif img.height > self.frameHeight:
                width = int(self.frameHeight / img.height * img.width)
                img = img.resize((self.frameHeight, width))

            return img
