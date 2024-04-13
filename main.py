from settings import UseReserve, UseFuel, UseStellarJade, ExitGameAfterCompletion
from PIL import ImageGrab
from PIL import Image
from PIL import ImageShow
import pytesseract
import pyautogui
import time


#global variables
AmountCollected = 0
CurrentState = "Temp"
image: Image.Image


#change this if your screen has different dimensions
# MonitorDefaultWidth = 1920
# MonitorDefaultHeight = 1080
# CheckForScreenSize = True
# """
# Automatically check screen dimensions if true
# """
# if CheckForScreenSize:
# 	image = ImageGrab.grab()
# 	MonitorDefaultWidth = image.size[0]
# 	MonitorDefaultHeight = image.size[1]


#some other settings that shouldn't be changed
RewardWidthStart = 668 #548
RewardHeightStart = 581 #520
RewardWidthEnd = 1254 #1373
RewardHeightEnd = 599 #539

PausePixelX = 1662
PausePixelY = 65

StopButtonX = 720
BothButtonY = 950
AgainButtonX = 1210


def update_situation():
	"""
	Updates the Global Variable CurrentState to the current state of the game
	"""
	global CurrentState
	global image
	image = ImageGrab.grab()
	PausePixel = image.getpixel((PausePixelX,PausePixelY))
	print(str(PausePixel))
	AddedValue = 0
	ImageString = pytesseract.image_to_string(image, lang='eng')
	if "Challenge Completed" in ImageString:
		CurrentState = "ChallengeCompleted"
		return
	if "Replenish Trailblaze Power" in ImageString:
		CurrentState = "ReplenishTrailblazePower"
		return
	for i in PausePixel:
		AddedValue += i
	if AddedValue >= 580:
		CurrentState = "InCombat"
		return
	print("Unknown State; Trying to find state again")
	update_situation()


def close_game():
	pyautogui.keyDown('alt')
	pyautogui.press('f4')
	pyautogui.keyUp('alt')

def update_rewardcount():
	global AmountCollected
	global AmountToCollect
	global image
	image = ImageGrab.grab(bbox = (RewardWidthStart,RewardHeightStart,RewardWidthEnd,RewardHeightEnd))
	print(pytesseract.image_to_string(image, lang='eng', config='--psm 6').split(" ")[1])
	try:
		AmountCollected += int(pytesseract.image_to_string(image, lang='eng', config='--psm 6').split(" ")[1])
	except:
		pass


AmountToCollect = int(input("Specify amount of ressources to collect (use 0 for infinite or relics)"))
x = 0
time.sleep(3)
while True:
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
				pyautogui.moveTo(x= StopButtonX,y= BothButtonY)
				pyautogui.click()
				break
			else:
				print(f"reached {AmountCollected}/{AmountToCollect} ressources, starting again...")
				pyautogui.moveTo(AgainButtonX,BothButtonY)
				pyautogui.click()
				x += 1
				continue
		case "ReplenishTrailblazePower":
			pyautogui.moveTo(1180,735)
			ReplenishString = pytesseract.image_to_string(image, 'eng')
			if "Reserved" in ReplenishString and UseReserve:
				print("Using reserve to replenish Trailblaze Power")
				pyautogui.click()
			elif "Exchange" in ReplenishString and UseFuel:
				pyautogui.click()
				print("Using fuel to replenish Trailblaze Power")
			elif "Consume" in ReplenishString and UseStellarJade:
				print("Using Stellar Jade to replenish Trailblaze Power")
			else:
				print(f"Can't use any replenishment, reached {AmountCollected}/{AmountToCollect}, ending...")
				if ExitGameAfterCompletion:
					close_game()
					break
				pyautogui.moveTo(760,735)
				pyautogui.click()
				pyautogui.moveTo(x= StopButtonX,y= BothButtonY)
				pyautogui.click()
			pyautogui.moveTo(1185,795)
			pyautogui.click()
			time.sleep(0.75)
			pyautogui.click()
			pyautogui.moveTo(AgainButtonX, BothButtonY)
			pyautogui.click()
			continue