import pyautogui
import mss as mss
from PIL import Image
class ScreenshotService:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

        self.mss_obj = mss.mss()

    def take(self, frameWidth):
        with self.mss_obj as sct:
            monitor = {"top": 0, "left": 0, "width": self.screen_width, "height": self.screen_height}
            raw = sct.grab(monitor)

            img = Image.frombytes("RGB", raw.size, raw.rgb)
            height = int(frameWidth / img.width * img.height)
            img = img.resize((frameWidth, height))
            return img
