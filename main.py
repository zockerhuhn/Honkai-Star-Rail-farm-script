from settings import UseReserve, UseFuel, UseStellarJade, ExitGameAfterCompletion
from PIL import ImageGrab
from PIL import Image
from PIL import ImageShow
import pytesseract
import pyautogui
import time
testing = True

#These are settings, change these to your needs
UseReserve = True
UseFuel = False
UseStellarJade = False 
"""
WARNING, THIS ALLOWS THE SCRIPT TO SPEND STELLAR JADE ON TRAILBLAZE POWER
"""
ExitGameAfterCompletion = False
"""
If set to true the script closes the whole game after it is done collecting the desired rewards
"""


#global variables
AmountCollected = 0
CurrentState = "Temp"
image: Image.Image


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

ChallengeCompletedWidthStart = int(MonitorDefaultWidth/4.8)
ChallengeCompletedHeightStart = int(MonitorDefaultHeight/2.0769230769)
ChallengeCompletedWidthEnd = int(MonitorDefaultWidth/2.2068965517)
ChallengeCompletedHeightEnd = int(MonitorDefaultHeight/2.16)
ChallengeCompletedUseWidthHeight = True

RewardWidthStart = int(MonitorDefaultWidth/5.1891891892)
RewardHeightStart = int(MonitorDefaultHeight/1.0536585366)
RewardWidthEnd = int(MonitorDefaultWidth/1.3287197232)
RewardHeightEnd = int(MonitorDefaultHeight/1.4025974026)

PausePixelX = int(MonitorDefaultWidth/1.0212765957)
PausePixelY = int(MonitorDefaultHeight/36)

StopButtonX = int(MonitorDefaultWidth*0.375)
BothButtonY = int(MonitorDefaultHeight/1.1368421053)
AgainButtonX = int(MonitorDefaultWidth*0.640625)


def update_situation():
	"""
	Updates the Global Variable CurrentState to the current state of the game
	"""
	global CurrentState
	global image
	#image = Image.open("Example_ChallengeCompleted.png")
	#image = Image.open("Example_replenish-trailblaze-power_noreserve.png")
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
	ImageShow.show(image)
	update_situation()


def close_game():
	pyautogui.keyDown('alt')
	pyautogui.press('f4')
	pyautogui.keyUp('alt')

def update_rewardcount():
	global AmountCollected
	global AmountToCollect
	global image
	#image = ImageGrab.grab(bbox = (RewardWidthStart,RewardHeightStart,RewardWidthEnd,RewardHeightEnd))
	image = Image.open("Example_Rewards_norelics3.png")
	AmountCollected += int(pytesseract.image_to_string(image, lang='eng', config='--psm 6').split(" ")[1])


AmountToCollect = 9#int(input("Specify amount of ressources to collect (use 0 for infinite or relics)"))
#image = Image.open("Example_ChallengeCompleted.png")
x = 0
while True:
	image = Image.open("Example_ChallengeCompleted.png")
	if x == 2:
		image = Image.open("Example_replenish-trailblaze-power_reserve.jpg")
	update_situation()
	print(CurrentState)
	match CurrentState:
		case "InCombat":
			time.sleep(5)
			continue
		case "ChallengeCompleted":
			update_rewardcount()
			if AmountCollected >= AmountToCollect:
				print(f"Collected enough ressources ({AmountCollected}), terminating...")
				if ExitGameAfterCompletion:
					close_game()
					break
				#pyautogui.moveTo(StopButtonX,BothButtonY)
				pyautogui.click()
				break
			else:
				print(f"reached {AmountCollected}/{AmountToCollect} ressources, starting again...")
				#pyautogui.moveTo(AgainButtonX,BothButtonY)
				pyautogui.click()
				x += 1
				continue
		case "ReplenishTrailblazePower":
			#move mouse to replenish button
			pyautogui.click()
			ReplenishString = pytesseract.image_to_string(Image.open("Example_replenish-trailblaze-power_reserve.jpg"), 'eng')
			if "Reserved" in ReplenishString and UseReserve:
				print("Using reserve to replenish Trailblaze Power")
				pyautogui.click()
			elif "Exchange" in ReplenishString and UseFuel:
				pyautogui.click()
				print("Using fuel to replenish Trailblaze Power")
			else:
				print(f"Can't use any replenishment, reached {AmountCollected}/{AmountToCollect}, ending...")
				if ExitGameAfterCompletion:
					close_game()
					break
				#move mouse to cancel button
				pyautogui.click()
			#move mouse to confirm button
			pyautogui.click()
			time.sleep(0.75)
			pyautogui.click()
			x += 1
			continue