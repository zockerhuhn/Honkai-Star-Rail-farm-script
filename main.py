from PIL import ImageGrab
from PIL import ImageShow
from PIL import Image
import pytesseract

image = Image.open("Screenshot 2024-03-07 133600.png")
#ImageShow.show(image)
#print(image.getpixel((1,1079)))
print(pytesseract.image_to_string(image))