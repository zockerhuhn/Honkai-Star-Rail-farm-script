from PIL import Image, ImageGrab
from time import sleep
sleep(1)
im = ImageGrab.grab(bbox=(788,496,807,579))
im.save("Comparison-Examples/test.png")
