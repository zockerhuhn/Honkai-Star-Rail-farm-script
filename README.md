I am not liable for any inconvenience the script might cause including spending ressources.

# Features

## Working
Restart combat after done with challenge.

Automatically refresh trailblaze power according to your settings (you decide what kind of ressources can be used).

Exit the challenge completed screen when desired amount of rewards or waves are reached

Close game after reaching desired reward amount if that setting is set to true

Decide a character which gets ignored when they are down

supports farming materials, relics and bosses. Setting it to relics only counts waves so you can use it for any activity with the normal challenge completed screen

## Planned
Revive characters that got downed in combat

# Known Issues
Does not yet retry if the whole team dies

# How to use

## Installing the script

Go to the releases page and download the newest release (link:https://github.com/zockerhuhn/Honkai-Star-Rail-farm-script/releases)

Download the zip and extract it

run main.exe in the \dist\main folder as administrator

_The script needs administrator access to use the mouse in Star Rail. Star Rail for some reason requieres this_

__Your Antivirus might stop you from running the script, here is why: To make the script accessible to anyone I have to compile the python script to an exe, this way it can run on any pc. Windows and other Antivirus programs do not like this kind of exe (which is a good but in this case unfortunate thing) and stop it from running. If you don't want to run the script because of this 


## Using the script
To change settings open the folder where the script is installed and right click the settings.py file. Select open with and open it with a Texteditor of your choice (the default editor of windows should work fine)

To start the script run the main.exe file as administrator. (_For some reason Star Rail requieres you to have administrator privileges to use the mouse while tabbed into the game_)

Change the settings to your needs

In Star Rail start your desired combat _domain_, choose your characters and enter combat (turn on autoplay)

Press start in the window with the settings, tab into Star Rail and you're good to go, the script will stop as soon as the desired reward amount is reached.

To end the script early simply go into the Terminal and press 'ctrl + c'

## Updating the script

To update the script simply go to the releases site again and download the new updatet version. (remember to delete the old version to not waste space on your harddrive) _depending on how difficult it is I might add an installer in the future that updates automatically 

# FAQ 

## Will I be banned for using this script?
While I can't and won't gurantee anything, probably not. I have been testing and using this script since over 2 months now and haven't been banned. All this script does is take Screenshots of small regions of the screen and use tesseract to read the text onscreen. Then it imitates a mouse and presses the right buttons according to the state of the game in the screenshot. You can test this by simply looking at a screenshot instead of ingame and the script won't know the difference.
