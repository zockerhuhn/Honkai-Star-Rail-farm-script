This script is still in development

# Features

## Working
Restart combat after done with challenge.

Exit the challenge completed screen when desired reward amount is reached (view issues)

Close game after reaching desired reward amount if setting is set to true

## Planned
Ignore or heal characters that died during combat

Start multiple from user specified reward challenges back to back

Support for relic _domains_

# Known Issues
If trailblaze power needs to be replenished the script detects the rewards two times. This will be fixed in next update

Currently only supports challenges that have 2 rows long rewards. Support for both will be added

If challenging _domains_ with rewards that can differ in rarity the script always uses the rarest drop that got obtained and adds it to the Collected counter. This will be fixed in the future but might take some time

# How to use
Since the script is currently still in development this is a bit complicated, but possible.

## Installing the script

### install general software
Install git on your PC

Install Python on your PC (available in the microsoft store)

Install tesseract OCR (__Do not change the path of this installation or the script will break__)

### Clone the repository
Choose where you want to install the script (I recommend documents or desktop) (It will install in a new folder, you don'thave to create one)

Press 'WIN + r' on your keyboard and enter cmd, this should open up a terminal

Enter 'cd [your_chosen_path]'

Enter 'git clone https://github.com/zockerhuhn/Honkai-Star-Rail-farm-script.git'

## Using the script

To start the script press the Windows key and enter cmd in the search, then press run as administrator and confirm. (_For some reason Star Rail requieres you to have administrator privileges to use the mouse while tabbed into the game_)

__This part will change as more features are implemented__

In Star Rail start your desired combat _domain_ (currently only supports two layer rewards), choose your characters and enter combat

The Terminal should now ask you how many rewards you want to farm, type the desired amount (as numbers, __not alphabetically__) and press enter

Tab into Star Rail and you're good to go, the script will stop as soon as the desired reward amount is reached.

To end the script early simply go back into the Terminal and press 'ctrl + c'

## Updating the script
To update the script repeat steps 1-3 of the _Clone the repository_ step

Enter [revert command]

Enter 'git clone --prune

This should update the script but also reset your settings so remember to set them again
