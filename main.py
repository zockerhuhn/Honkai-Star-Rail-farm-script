from PIL import ImageGrab
from PIL import Image
from PIL import ImageShow
import pygame
import pygame_menu as pm
import numpy as np
import cv2 as cv
import pytesseract
import pyautogui
from time import sleep as delay


#global variables
Failed:bool = False
FailReason:str=""
AmountCollected = 0
AmountToCollect:int
CurrentState = "Temp"
image: Image.Image
FailCounter:int = 0
SettingsData:None
UseReserve:bool = False
UseFuel:bool = False
UseStellarJade:bool = False
ExitGameAfterCompletion:bool = False
mode:int
CharacterToIgnore:str
SupportCharacter:int

pygame.init() 

# Screen 
WIDTH, HEIGHT = 750, 600
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

DownedConfirmButton:tuple = 1178, 819

DownedConfirmWindow:tuple = 858, 256, 1066, 287

DownedNoRessourcesWindow:tuple = 1040, 561, 1324, 588

CombatStartButton:tuple = 1600, 980

AddSupportButton:tuple = 1710, 740

FirstSupportChar:tuple = 300, 230

SupportOffset:int = 140

SupportConfirmButton:tuple = 1674, 984

def set_settings():
    """
    Sets the global variables according to what was set in the settings
    """
    global SettingsData
    global UseReserve
    global UseFuel
    global UseStellarJade
    global ExitGameAfterCompletion
    global mode
    global CharacterToIgnore
    global AmountToCollect
    global SupportCharacter
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
    if SettingsData["AmountToCollect"] == "":
        FailReason = "Amount to collect setting is empty"
        Failed = True
        return
    AmountToCollect = int(SettingsData["AmountToCollect"])
    SupportCharacter = int(SettingsData["SupportChar"][1])


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
        int(pytesseract.image_to_string(image, lang='eng', config='--psm 6').split(" ")[1])
        TwoRows = False
    except:
        image = ImageGrab.grab(bbox=RewardTwoShape)
        try:
            int(pytesseract.image_to_string(image, lang='eng', config='--psm 6').split(" ")[1])
            TwoRows = True
        except:
            FailCounter += 1
            if FailCounter >= FailCountMax:
                FailReason = f"failed {FailCounter} times which is over max amount ({FailCountMax})"
                Failed = True
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
            image.save("C:\\Users\\Anwender\\AppData\\Local\\Temp\\screenshot_temp.png")
            cvimage =  np.array(image) 
            # Convert RGB to BGR 
            cvimage = cvimage[:, :, ::-1].copy()
            rarity = determine_rarity(cvimage)
            match rarity:
                case 4:
                    AmountCollected += int(rewards[1]) + float(int(rewards[2])/3) + float(int(rewards[3])/9)
                case 3:
                    AmountCollected += float(int(rewards[1])/3) + float(int(rewards[2])/9)
                case _:
                    Failed = True
                    FailReason = "Unknown Rarity, made it into calculation"
        case 1:
            AmountCollected += int(rewards[1])
        case 2:
            AmountCollected += 1
        case _:
            raise Exception("invalid mode")


def heal():
    global image, AmountCollected, AmountToCollect, Failed, FailReason
    for i in range(4):
        pyautogui.press(str(i+1))
        delay(1)
        image = ImageGrab.grab(DownedConfirmWindow)
        if "Quick" in pytesseract.image_to_string(image, lang='eng', config='--psm 6'):
            pyautogui.click(DownedConfirmButton)
            image = ImageGrab.grab(DownedNoRessourcesWindow)
            print(pytesseract.image_to_string(image, lang='eng', config='--psm 6'))
            if "No" in pytesseract.image_to_string(image, lang='eng', config='--psm 6'):
                FailReason = "No revive ressources"
                Failed = True
                break
            print(f"revived {i+1}")
        delay(3)


def mainloop():
    global AmountCollected, image, AmountToCollect, Failed, FailReason, ExitGameAfterCompletion, CurrentState, SupportCharacter
    delay(3)
    while not Failed:
        update_situation()
        print(CurrentState)
        match CurrentState:
            case "InCombat":
                delay(3)
                continue
            case "ChallengeCompleted":
                update_rewardcount()
                if AmountCollected >= AmountToCollect:
                    print(f"Collected enough ressources ({(int(AmountCollected*100))/100}), terminating...")
                    if ExitGameAfterCompletion:
                        close_game()
                        break
                    delay(0.5)
                    pyautogui.moveTo(x= StopButtonX,y= BothButtonY)
                    pyautogui.click()
                    break
                else:
                    print(f"reached {(int(AmountCollected*100))/100}/{AmountToCollect} ressources, starting again...")
                    pyautogui.moveTo(AgainButtonX,BothButtonY)
                    pyautogui.click()
                    delay(1)
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
                    pyautogui.click()
                else:
                    FailReason = "Can't use any replenishment"
                    Failed = True
                    pyautogui.click(760,735)
                    delay(0.75)
                    pyautogui.click(StopButtonX,BothButtonY)
                    break
                pyautogui.click()
                delay(0.75)
                pyautogui.click()
                delay(0.75)
                pyautogui.click(AgainButtonX,BothButtonY)
                delay(0.75)
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
                    pyautogui.click(764,675)
                    delay(0.75)
                    pyautogui.click(StopButtonX, BothButtonY)
                    delay(2)
                    heal()
                    if not Failed:
                        pyautogui.write('f')
                        delay(1.5)
                        pyautogui.click(CombatStartButton)
                        delay(0.5)
                        if SupportCharacter >= 1:
                            pyautogui.click(AddSupportButton)
                            delay(0.5)
                            pyautogui.click(FirstSupportChar[0], FirstSupportChar[1]+(SupportOffset*(SupportCharacter-1)))
                            delay(0.5)
                            pyautogui.click(SupportConfirmButton)
                            delay(0.5)
                        pyautogui.click(CombatStartButton)


def GUI(): #https://www.geeksforgeeks.org/create-settings-menu-in-python-pygame/
    type =     [("different rarity", "materials"), 
                ("one rarity", "weekly"), 
                ("count cycles", "relics")] 
 
    ressources = [("Reserve", "resereve"),
                    ("Fuel", "fuel"),
                    ("Stellar-Jade", "stellar-jade")]
    
    SupportCharIndex = [("None", "0"),
                    ("1", "1"),
                    ("2", "2"),
                    ("3", "3"),
                    ("4", "4"),
                    ("5", "5"),
                    ("6", "6"),]

    def setSettings():
        global SettingsData
        SettingsData = settings.get_input_data()

    def start():
        setSettings()
        pygame.quit()
        set_settings()
        mainloop()
        if Failed:
            print(f"Failed to collect enough ressources ({(int(AmountCollected*100))/100}/{AmountToCollect}), reason: {FailReason}")
            input()
        elif not ExitGameAfterCompletion:
            input()
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
    
    settings.add.dropselect(title="Support Character", items=SupportCharIndex, 
                            dropselect_id="SupportChar", default=0,selection_box_height=5) 

    
    settings.add.dropselect_multiple(title="Allowed Replenishment-ressources", items=ressources,
                                    dropselect_multiple_id="AllowedRessources",
                                    open_middle=True, max_selected=0, default=0,
                                    selection_box_height=4)
 
    settings.add.text_input(title="Character to ignore when down (case sensitive) :", textinput_id="IgnoreChar") 
 
    settings.add.toggle_switch( 
        title="Close game when done", default=False, toggleswitch_id="ExitAfterCompletion") 

    settings.add.text_input(title="Amount of ressources to farm/cycles to complete :", textinput_id="AmountToCollect") 

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

    mainMenu.add.label(title="Please check settings if this is your first time using this script") 

    mainMenu.add.button(title="Start", action=start, 
                        font_color=WHITE, background_color=RED) 
    mainMenu.mainloop(screen) 

 
if __name__ == "__main__":
    GUI()