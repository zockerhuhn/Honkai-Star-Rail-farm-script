from settings import UseReserve, UseFuel, UseStellarJade, ExitGameAfterCompletion,SkipRewardCount,Acheron,Argenti,Arlan,Asta,Bailu,Black_Swan,Blade,Bronya,Clara,Dan_Heng,Dan_Heng_Imbibitor_Lunae,Dr_Ratio,Firefly,Fu_Xuan,Gallagher,Gepard,Guinaifen,Hanya,Herta,Himeko,Hook,Huohuo,Jing_Yuan,Jingliu,Kafka,Luka,Luocha,Lynx,March_7th,Misha,Natasha,Pela,Qingque,Ruan_Mei,Sampo,Seele,Serval,Silver_Wolf,Sparkle,Sushang,Tingyun,Topaz_and_Numby,Trailblazer,Welt,Xueyi,Yanqing,Yukong
from PIL import ImageGrab
from PIL import Image
from PIL import ImageShow
import pygame
import pygame_menu as pm
import numpy as np
import cv2 as cv
import pytesseract
import pyautogui
import time


#global variables
AmountCollected = 0
CurrentState = "Temp"
image: Image.Image
FailCounter:int = 0
SettingsData:None
UseReserve:bool
UseFuel:bool
UseStellarJade:bool
ExitGameAfterCompletion:bool
mode:int
CharacterToIgnore:str

pygame.init() 

# Screen 
WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 

# Standard RGB colors 
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255) 
CYAN = (0, 100, 100) 
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 


#some other settings that shouldn't be changed
RewardOneShape:tuple = 668, 580, 1254, 599

RewardTwoShape:tuple = 548, 520, 1373, 539

PausePixelX = 1662
PausePixelY = 65

StopButtonX = 720
BothButtonY = 950
AgainButtonX = 1210

Downtext:tuple = 670, 495, 1190, 525

Jarilo_VIX = 330
Jarilo_VIY = 405

StarRailMapX = 1670
StarRailMapY = 140

FirstItemShapeTwoRows:tuple = 634, 502, 659, 612
FirstItemShapeOneRow:tuple = 848, 496, 867, 579

def set_settings():
	global SettingsData
	global UseReserve
	global UseFuel
	global UseStellarJade
	global ExitGameAfterCompletion
	global mode
	global CharacterToIgnore
	print(SettingsData["AllowedRessources"])
	for i in SettingsData["AllowedRessources"][len(SettingsData["AllowedRessources"])-1]:
		match i:
			case 0:
				UseReserve=True
			case 1:
				UseFuel=True
			case 2:
				UseStellarJade=True
			case _:
				raise Exception("Allowed ressources has an invalid set ressource")
	ExitGameAfterCompletion=SettingsData["ExitAfterCompletion"]
	mode = SettingsData["ChallengeType"][len(SettingsData["ChallengeType"])-1]
	CharacterToIgnore = SettingsData["IgnoreChar"]
 
		

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


def mse(imageA, imageB): #https://github.com/CelestialCrafter/hsr-auto-auto-battle/blob/master/main.py#L3
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	print(err)
	return err


def determine_rarity(imageA):
	FourStar = cv.imread("Comparison-Examples/Example_Item-4Star.png")
	ThreeStar = cv.imread("Comparison-Examples/Example_Item-3Star.png")
	if mse(imageA, FourStar) > mse(imageA, ThreeStar):
		return 3
	else:
		return 4


def update_rewardcount():
	TwoRows:bool
	global AmountCollected
	global AmountToCollect
	global image
	FailCountMax:int = 5
	image = ImageGrab.grab(bbox=RewardOneShape)
	global FailCounter
	try:
		print(int(pytesseract.image_to_string(image, lang='eng', config='--psm 6').split(" ")[1]))
		TwoRows = False
	except:
		image = ImageGrab.grab(bbox=RewardTwoShape)
		try:
			print(int(pytesseract.image_to_string(image, lang='eng', config='--psm 6').split(" ")[1]))
			TwoRows = True
		except:
			FailCounter += 1
			if FailCounter >= FailCountMax:
				print(f"failed {FailCounter} times which is over max amount ({FailCountMax}), terminating...")
				raise IndexError
			print(f"somehow didn't find a reward for single and double row, trying again {FailCounter}/{FailCountMax}")
			update_rewardcount()
			return()
	rewards:list = pytesseract.image_to_string(image, lang='eng', config='--psm 6').split(" ")
	match mode:
		case 0:
			if TwoRows:
				image = ImageGrab.grab(bbox = FirstItemShapeTwoRows)
			else:
				image = ImageGrab.grab(bbox = FirstItemShapeOneRow)
			image.save("temp/screenshot_temp.png")
			cvimage = cv.imread("temp/screenshot_temp.png")
			rarity = determine_rarity(cvimage)
			match rarity:
				case 4:
					AmountCollected += int(rewards[1]) + float(int(rewards[2])/3) + float(int(rewards[3])/9)
				case 3:
					AmountCollected += float(int(rewards[1])/3) + float(int(rewards[2])/9)
				case _:
					raise Exception("Unknown Rarity, made it into calculation")
		case 1:
			AmountCollected += rewards[1]
		case 2:
			AmountCollected += 1
		case _:
			raise Exception("invalid mode")
			

# def heal():
# 		pyautogui.press('m')
# 		time.sleep(1.5)
# 		pyautogui.click(StarRailMapX,StarRailMapY)
# 		pyautogui.moveRel(1000,0)
# 		time.sleep(2.5)
# 		pyautogui.moveRel(-1,0)
# 		pyautogui.dragRel(-1000,0, 2, mouseDownUp=False)
# 		pyautogui.click(Jarilo_VIX,Jarilo_VIY)


def farm():
	if mode == 2:
		AmountToCollect = int(input("Specify amount of cycles\n"))
	else:
		AmountToCollect = int(input("Specify amount of ressources to collect\n"))
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
					print(f"Collected enough ressources ({(int(AmountCollected*100))/100}), terminating...")
					if ExitGameAfterCompletion:
						close_game()
						break
					time.sleep(0.5)
					pyautogui.moveTo(x= StopButtonX,y= BothButtonY)
					pyautogui.click()
					break
				else:
					print(f"reached {(int(AmountCollected*100))/100}/{AmountToCollect} ressources, starting again...")
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
					print(f"Can't use any replenishment, reached {(int(AmountCollected*100))/100}/{AmountToCollect}, ending...")
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
				image = ImageGrab.grab(bbox=Downtext)
				CharName = pytesseract.image_to_string(image, lang='eng', config='--psm 6').split(" ")[0]
				print(f"{CharName} is currently downed, ")
				if CharName==CharacterToIgnore:
					print("ignoring...")
					pyautogui.click(1185,679)
					continue
				else:
					print("stopping...")
					pyautogui.moveTo(764,675)
					pyautogui.click()
					time.sleep(0.2)
					pyautogui.moveTo(StopButtonX, BothButtonY)
					pyautogui.click()
					time.sleep(2)
					if ExitGameAfterCompletion:
						close_game()
					break


def main(): #https://www.geeksforgeeks.org/create-settings-menu-in-python-pygame/
	type =     [("materials", "materials"), 
				("weekly", "weekly"), 
				("relics", "relics")] 
 
	ressources = [("Reserve", "resereve"),
				  ("Fuel", "fuel"),
				  ("Stellar-Jade", "stellar-jade")]

	def setSettings():
		global SettingsData
		SettingsData = settings.get_input_data()

	def start():
		pygame.quit()
		setSettings()
		set_settings()
		farm()
		exit()

	settings = pm.Menu(title="Settings", 
					width=WIDTH, 
					height=HEIGHT, 
					theme=pm.themes.THEME_GREEN) 

	settings._theme.widget_font_size = 25
	settings._theme.widget_font_color = BLACK 
	settings._theme.widget_alignment = pm.locals.ALIGN_LEFT 

	settings.add.dropselect(title="Challenge type", items=type, 
							dropselect_id="ChallengeType", default=0,selection_box_height=4) 
	settings.add.dropselect_multiple(title="Allowed Replenishment-ressources", items=ressources,
									dropselect_multiple_id="AllowedRessources",
									open_middle=True, max_selected=0, default=0,
									selection_box_height=4)
 
	settings.add.text_input(title="Character to ignore when down (case sensitive) :", textinput_id="IgnoreChar") 
 
	settings.add.toggle_switch( 
		title="Close game when  done", default=False, toggleswitch_id="ExitAfterCompletion") 

	settings.add.button(title="Restore Defaults", action=settings.reset_value, 
						font_color=WHITE, background_color=RED) 
	settings.add.button(title="Return To Main Menu", 
						action=pm.events.BACK, align=pm.locals.ALIGN_CENTER) 

	mainMenu = pm.Menu(title="Main Menu", 
					width=WIDTH, 
					height=HEIGHT, 
					theme=pm.themes.THEME_GREEN) 

	mainMenu._theme.widget_alignment = pm.locals.ALIGN_CENTER 

	pygame.display.set_caption("HSR farming script")

	mainMenu.add.button(title="Settings", action=settings, 
						font_color=WHITE, background_color=GREEN) 

	mainMenu.add.label(title="") 

	mainMenu.add.button(title="Start", action=start, 
						font_color=WHITE, background_color=RED) 
	mainMenu.mainloop(screen) 

 
if __name__ == "__main__":
	main()