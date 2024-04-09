from PIL import ImageGrab
from PIL import Image
from PIL import ImageShow
import pytesseract
from pyautogui import moveTo
testing = True

#These are settings, change these to your needs
UseReserve = True
UseFuel = False
UseStellarJade = False 
"""
WARNING, THIS ALLOWS THE SCRIPT TO SPEND STELLAR JADE ON TRAILBLAZE POWER
"""


#global variables
AmountCollected = 0
CurrentState = "Temp"


#change this if your screen has different dimensions
MonitorDefaultWidth = 1920
MonitorDefaultHeight = 1080
CheckForScreenSize = True 
"""
Automatically check screen dimensions if true
"""
if CheckForScreenSize:
	image = ImageGrab.grab()
	MonitorDefaultWidth = image.size[0]
	MonitorDefaultHeight = image.size[1]


#some other settings that shouldn't be changed
ReplenishTrailblazePowerWidthStart = int(MonitorDefaultWidth/4.8)
ReplenishTrailblazePowerHeightStart = int(MonitorDefaultHeight/3.6)
ReplenishTrailblazePowerWidthEnd = int(MonitorDefaultWidth/1.2631578947)
ReplenishTrailblazePowerHeightEnd = int(MonitorDefaultHeight/1.3846153846)
replenishTrailblazePowerUseWidthHeight = True

ChallengeCompletedWidthStart = int(MonitorDefaultWidth/4.8)
ChallengeCompletedHeightStart = int(MonitorDefaultHeight/2.0769230769)
ChallengeCompletedWidthEnd = int(MonitorDefaultWidth/2.2068965517)
ChallengeCompletedHeightEnd = int(MonitorDefaultHeight/2.16)
ChallengeCompletedUseWidthHeight = True

PausePixelX = int(MonitorDefaultWidth/1.0212765957)
PausePixelY = int(MonitorDefaultHeight/36)


def update_situation():
	"""
	Updates the Global Variable CurrentState to the current state of the game
	"""
	global CurrentState
	image = Image.open("Example_replenish-trailblaze-power_noreserve.png")
	#image = Image.open("Example_infight_noauto.jpg")
	#image = ImageGrab.grab()
	PausePixel = image.getpixel((PausePixelX,PausePixelY))
	AddedValue = 0
	if PausePixel is tuple:
		for i in PausePixel:
			AddedValue += i
		if AddedValue >= 300:
			CurrentState = "InCombat"
			return
	elif PausePixel is int:
		if PausePixel >= 100:
			CurrentState = "InCombat"
			return
	ImageString = pytesseract.image_to_string(image, lang='eng')
	if "Challenge Completed" in ImageString:
		CurrentState = "ChallengeCompleted"
		return
	if "Replenish Trailblaze Power" in ImageString:
		CurrentState = "ReplenishTrailblazePower"
		return
	print("Unknown State; Trying to find state again")
	update_situation()


def readscreen(situation:str = "default"):
	"""
	Reads the screen and returns the image as a PIL image object. situation limits the amount of pixel read onscreen to only the amount of pixels necessary for that situation
	"""
	match situation:
		case "default":
			x1 = 0
			y1 = 0
			x2 = MonitorDefaultWidth 
			y2 = MonitorDefaultHeight
		case "ReplenishTrailblazePower":
			x1 = ReplenishTrailblazePowerWidthStart
			y1 = ReplenishTrailblazePowerHeightStart
			x2 = ReplenishTrailblazePowerWidthEnd
			y2 = ReplenishTrailblazePowerHeightEnd 
		case "ChallengeCompleted":
			x1 = ChallengeCompletedWidthStart
			y1 = ChallengeCompletedHeightStart
			x2 = ChallengeCompletedWidthEnd
			y2 = ChallengeCompletedHeightEnd
		case _:
			print(f"Situation {situation} not found, using whole screen")
			x1 = 0
			y1 = 0
			x2 = MonitorDefaultWidth
			y2 = MonitorDefaultHeight
	if testing:
		return Image.open("Example_replenish-trailblaze-power_reserve.jpg")
	#ImageShow.show(ImageGrab.grab(bbox=(x1,y1,x2,y2)))
	return (ImageGrab.grab(bbox = (x1,y1,x2,y2)))


#AmountToCollect = int(input("Specify amount of ressources to collect (use 0 for infinite or relics)"))
update_situation()
print(CurrentState)
while True:
	pass
#print(pytesseract.image_to_string(readscreen("ReplenishTrailblazePower")))
