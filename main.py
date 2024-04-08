from PIL import ImageGrab
from PIL import Image
import pytesseract
from pytesseract.pytesseract import string

#global variables
image = None
AmountToCollect:int

#These are settings, change these to your needs
UseReserve = True
UseFuel = False
UseStellarJade = False 
"""
WARNING, THIS ALLOWS THE SCRIPT TO SPEND STELLAR JADE ON TRAILBLAZE POWER
"""

#change this if your screen has different dimensions
MonitorDefaultWidth = 1920
MonitorDefaultHeight = 1080

#
ReplenishTrailblazePowerHeightStart = int(MonitorDefaultHeight/4.8)
ReplenishTrailblazePowerWidthStart = int(MonitorDefaultWidth/1.3935483871)
ReplenishTrailblazePowerHeightEnd = int(MonitorDefaultHeight/1.2631578947)
ReplenishTrailblazePowerWidthEnd = int(MonitorDefaultHeight/3.6)
replenishTrailblazePowerUseWidthHeight = True

def readscreen(situation:str = "default"):
	"""
	Reads the screen and returns the image as a PIL image object. situation limits the amount of pixel read onscreen to only the amount of pixels necessary for that situation
	"""
	match situation:
		case "default":
			x1 = MonitorDefaultHeight
			y1 = 0
			x2 = 0 
			y2 = MonitorDefaultWidth
		case "ReplenishTrailblazePower":
			x1 = ReplenishTrailblazePowerWidthStart
			y1 = ReplenishTrailblazePowerHeightStart
			x2 = ReplenishTrailblazePowerWidthEnd
			y2 = ReplenishTrailblazePowerHeightEnd 
		case _:
			print(f"Situation {situation} not found, using whole screen")
			x1 = MonitorDefaultHeight
			y1 = 0
			x2 = 0
			y2 = MonitorDefaultWidth
	return (ImageGrab.grab(bbox = (x1,y1,x2,y2)))


AmountToCollect = int(input("Specify amount of ressources to collect (use 0 for infinite or relics)"))
while True:
	
#print(image.getpixel((1,1079)))
#print(pytesseract.image_to_string(image))