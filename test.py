from PIL import ImageGrab
import time

time.sleep(5)
image = ImageGrab.grab()
print(str(image.getpixel((1662,65))))