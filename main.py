from settings import UseReserve, UseFuel, UseStellarJade, ExitGameAfterCompletion,SkipRewardCount,Acheron,Argenti,Arlan,Asta,Bailu,Black_Swan,Blade,Bronya,Clara,Dan_Heng,Dan_Heng_Imbibitor_Lunae,Dr_Ratio,Firefly,Fu_Xuan,Gallagher,Gepard,Guinaifen,Hanya,Herta,Himeko,Hook,Huohuo,Jing_Yuan,Jingliu,Kafka,Luka,Luocha,Lynx,March_7th,Misha,Natasha,Pela,Qingque,Ruan_Mei,Sampo,Seele,Serval,Silver_Wolf,Sparkle,Sushang,Tingyun,Topaz_and_Numby,Trailblazer,Welt,Xueyi,Yanqing,Yukong
from PIL import ImageGrab
from PIL import Image
#from PIL import ImageShow #for testing
import pytesseract
import pyautogui
import time


#global variables
AmountCollected = 0
CurrentState = "Temp"
image: Image.Image
FailCounter:int = 0
# UseReserve:bool
# UseFuel:bool
# UseStellarJade:bool
# ExitGameAfterCompletion:bool
# SkipRewardCount:bool
# CharactersToIgnore:list


#some other settings that shouldn't be changed
RewardWidthStartOne = 668 
RewardHeightStartOne = 581 
RewardWidthEndOne = 1254 
RewardHeightEndOne = 599 

RewardWidthStartTwo = 548
RewardHeightStartTwo = 520
RewardWidthEndTwo = 1373
RewardHeightEndTwo = 539

PausePixelX = 1662
PausePixelY = 65

StopButtonX = 720
BothButtonY = 950
AgainButtonX = 1210

DownedTextStartX = 670
DownedTextStartY = 495
DownedTextEndX = 1190
DownedTextEndY = 525


# def import_settings():
#     global UseReserve
#     global UseFuel
#     global UseStellarJade
#     global ExitGameAfterCompletion
#     global SkipRewardCount
#     global CharactersToIgnore
#     with open("general_settings.txt","r") as GeneralSettings:
#         GeneralSettings=GeneralSettings.read().split(":")
#         for i in range(len(GeneralSettings)):
#             if (i+1)%2==0:
#                 match i+1:
#                     case 2:
#                         UseReserve = eval(GeneralSettings[i])
#                     case 4:
#                         UseFuel = eval(GeneralSettings[i])
#                     case 6:
#                         UseStellarJade = eval(GeneralSettings[i])
#                     case 8:
#                         ExitGameAfterCompletion = eval(GeneralSettings[i])
#                     case 10:
#                         SkipRewardCount = eval(GeneralSettings[i])
#     with open("characters_to_ignore.txt","r") as CharacterIgnoreList:
#         CharactersToIgnore=CharacterIgnoreList.read().split("\n")[1].split(";")
        
        

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
	global FailCounter
	FailCountMax:int = 5
	image = ImageGrab.grab(bbox = (RewardWidthStartOne,RewardHeightStartOne,RewardWidthEndOne,RewardHeightEndOne))
	try:
		print(int(pytesseract.image_to_string(image, lang='eng', config='--psm 6').split(" ")[1]))
	except:
		image = ImageGrab.grab(bbox = (RewardWidthStartTwo,RewardHeightStartTwo,RewardWidthEndTwo,RewardHeightEndTwo))
		try:
			print(int(pytesseract.image_to_string(image, lang='eng', config='--psm 6').split(" ")[1]))
		except:
			FailCounter += 1
			if FailCounter >= FailCountMax:
				print(f"failed {FailCounter} times which is over max amount ({FailCountMax}), terminating...")
				raise IndexError
			print(f"somehow didn't find a reward for single and double row, trying again {FailCounter}/{FailCountMax}")
			update_rewardcount()
			return
	AmountCollected += int(pytesseract.image_to_string(image, lang='eng', config='--psm 6').split(" ")[1])
	FailCounter = 0



if __name__ == "__main__":
	# import_settings()
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
					print(f"Collected enough ressources ({AmountCollected}), terminating...")
					if ExitGameAfterCompletion:
						close_game()
						break
					time.sleep(0.5)
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
				print(f"{CharName} is currently downed, ")
				IgnoreChar=False
				# for i in CharactersToIgnore:
				# 	x=0
				# 	for y in CharName:
				# 		if y in i:
				# 			x+1
				# 	if x>=len(y)-1:
				# 		IgnoreChar=True
				# 		break
				# if IgnoreChar:
				# 	print("ignoring...")
				# 	pyautogui.moveTo(1185,679)
				# 	pyautogui.click()
				# 	continue
				if eval(CharName):
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
					break