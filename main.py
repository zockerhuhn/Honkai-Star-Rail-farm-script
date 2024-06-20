from settings import UseReserve, UseFuel, UseStellarJade, ExitGameAfterCompletion,SkipRewardCount,Acheron,Argenti,Arlan,Asta,Bailu,Black_Swan,Blade,Bronya,Clara,Dan_Heng,Dan_Heng_Imbibitor_Lunae,Dr_Ratio,Firefly,Fu_Xuan,Gallagher,Gepard,Guinaifen,Hanya,Herta,Himeko,Hook,Huohuo,Jing_Yuan,Jingliu,Kafka,Luka,Luocha,Lynx,March_7th,Misha,Natasha,Pela,Qingque,Ruan_Mei,Sampo,Seele,Serval,Silver_Wolf,Sparkle,Sushang,Tingyun,Topaz_and_Numby,Trailblazer,Welt,Xueyi,Yanqing,Yukong
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

DownedTextStartX = 670
DownedTextStartY = 495
DownedTextEndX = 1190
DownedTextEndY = 525

Jarilo_VIX = 330
Jarilo_VIY = 405

StarRailMapX = 1670
StarRailMapY = 140


def update_situation():
	"""
	Updates the Global Variable CurrentState to the current state of the game
	"""
	global CurrentState
	global image
	image = ImageGrab.grab()
	PausePixel = image.getpixel((PausePixelX,PausePixelY))
	AddedValue = 0
	ImageString = pytesseract.image_to_string(image, lang='eng')
	if "Challenge Completed" in ImageString:
		CurrentState = "ChallengeCompleted"
		return
	if "Replenish Trailblaze Power" in ImageString:
		CurrentState = "ReplenishTrailblazePower"
		return
	if "downed" in ImageString:
		CurrentState = "DownedChar"
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


def heal():
    pyautogui.press('m')
    time.sleep(1.5)
    pyautogui.click(StarRailMapX,StarRailMapY)
    #pyautogui.moveRel(1000,0)
    time.sleep(2.5)
    pyautogui.moveRel(-1,0)
    pyautogui.dragRel(-1000,0, 2, mouseDownUp=False)
    pyautogui.click(Jarilo_VIX,Jarilo_VIY)

#time.sleep(1)
#heal()
AmountToCollect = int(input("Specify amount of ressources to collect"))
time.sleep(3)
while True:
	update_situation()
	print(CurrentState)
	match CurrentState:
		case "InCombat":
			time.sleep(5)
			continue
		case "ChallengeCompleted":
			if not SkipRewardCount:
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
				time.sleep(1)
				continue
		case "ReplenishTrailblazePower":
			pyautogui.moveTo(1180,735)
			ReplenishString = pytesseract.image_to_string(image, 'eng')
			if "Reserved" in ReplenishString and UseReserve:
				print("Using reserve to replenish Trailblaze Power")
				pyautogui.click()
				pyautogui.moveTo(1185,795)
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
				pyautogui.moveTo(StopButtonX, BothButtonY)
				pyautogui.click()
				break
			pyautogui.click()
			time.sleep(0.75)
			pyautogui.click()
			time.sleep(0.75)
			pyautogui.moveTo(AgainButtonX, BothButtonY)
			pyautogui.click()
			time.sleep(0.75)
			continue
		case "DownedChar":
			image = ImageGrab.grab(bbox=(DownedTextStartX, DownedTextStartY, DownedTextEndX, DownedTextEndY))
			CharName = pytesseract.image_to_string(image, lang='eng', config='--psm 6').split(" ")[0]
			if eval(CharName):
				pyautogui.moveTo(1185,679)
				pyautogui.click()
				continue
			else:
				pyautogui.moveTo(764,675)
				pyautogui.click()
				time.sleep(0.2)
				pyautogui.moveTo(StopButtonX, BothButtonY)
				pyautogui.click()
				time.sleep(2)
				#heal()