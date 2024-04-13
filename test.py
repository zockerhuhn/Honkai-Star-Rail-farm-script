from PIL import ImageGrab
from PIL import ImageOps
from PIL import ImageShow
import time
import pytesseract

time.sleep(5)
image = ImageGrab.grab(bbox=(670,495,1190,525))
#print(str(image.getpixel((1662,65))))
#ImageShow.show(image)
image = ImageOps.solarize(image)
ImageShow.show(image)
print(pytesseract.image_to_string(image, lang='eng', config='--psm 6'))