import mss as mss
from PIL import Image
from live_scanner.modules import guiUtils


class ScreenshotService:
    def __init__(self, frameWidth):
        self.screen_width, self.screen_height = guiUtils.getScreenSize()
        self.mss_obj = mss.mss()
        self.frameWidth = frameWidth

    def take(self, fromX, fromY, toX, toY):
        with self.mss_obj as sct:
            monitor = {"top": fromY, "left": fromX, "width": toX, "height": toY}
            raw = sct.grab(monitor)

            img = Image.frombytes("RGB", raw.size, raw.rgb)
            height = int(self.frameWidth / img.width * img.height)
            img = img.resize((self.frameWidth, height))
            return img
