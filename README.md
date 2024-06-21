This script is still in development
I am not liable for any inconvenience the script might cause including spending ressources.

# FAQ 

## Will I be banned for using this script?
While I can't and won't gurantee anything, probably not. I have been testing and using this script since over 2 months now and haven't been banned. All this script does is take Screenshots of small regions of the screen and use tesseract to read the text onscreen. Then it imitates a mouse and presses the right buttons according to the state of the game in the screenshot. You can test this by simply looking at a screenshot instead of ingame and the script won't know the difference.

# Features

## Working
Restart combat after done with challenge.

Exit the challenge completed screen when desired reward amount is reached (view issues)

Close game after reaching desired reward amount if setting is set to true

Decide which characters to ignore when they are down

supports relic domains if setting _SkipRewardCount_ is True

## Planned
Revive downed characters during combat

Start multiple from user specified reward challenges back to back

# Known Issues
If challenging _domains_ with rewards that can differ in rarity the script always uses the rarest drop that got obtained and adds it to the Collected counter. This will be fixed in the future

# How to use
Since the script is currently still in development this is a bit complicated, but possible.

## Installing the script

### install general software
Install git on your PC

Install Python on your PC (available in the microsoft store)

Install tesseract OCR (__Do not change the path of this installation or the script will break__ (_if you know what you're doing you can change this but you will also have to change the path in the script_))
Direct install link: https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe
__This software is used to read the text and numbers from the screen by taking a screenshot of the specific area and then using tesseract to analyse it__

### Clone the repository
Choose where you want to install the script (I recommend documents or desktop) (It will install in a new folder, you don't have to create one)

Press 'WIN + r' on your keyboard and enter cmd, this should open up a terminal

Enter 'cd [your_chosen_path]'

Enter 'git clone https://github.com/zockerhuhn/Honkai-Star-Rail-farm-script.git'

## Using the script
To change settings open the folder where the script is installed and right click the settings.py file. Select open with and open it with a Texteditor of your choice (the default editor of windows should work fine)

To start the script press the Windows key and enter cmd in the search, right click it, then press run as administrator and confirm. (_For some reason Star Rail requieres you to have administrator privileges to use the mouse while tabbed into the game_)

__This part will change as more features are implemented__

In Star Rail start your desired combat _domain_ (see known issues for reward layer amount), choose your characters and enter combat

Enter 'cd [the folder that you installed the script into]' into your terminal

Enter 'python main.py' into the terminal

The terminal should now ask you how many rewards you want to farm, type the desired amount (as numbers, __not alphabetically__) and press enter

Tab into Star Rail and you're good to go, the script will stop as soon as the desired reward amount is reached.

To end the script early simply go back into the Terminal and press 'ctrl + c'

## Updating the script
To update the script repeat steps 1-3 of the _Clone the repository_ step

Open cmd and enter 'cd [the folder where you installed the script]'

Enter 'git pull --f --prune'

This should update the script but might also reset your settings (depending on the update) so remember to check them again
