# Python program to create a basic settings menu using the pygame_menu module 

import pygame 
import pygame_menu as pm 

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

def start():
    pass

def main(): 
	type =     [("materials", "materials"), 
				("weekly", "weekly"), 
				("relics", "relics")] 
 
	ressources = [("Reserve", "resereeeeeve"),
                  ("Fuel", "fuel"),
                  ("Stellar-Jade", "stellar-jade")]

	# def printSettings(): 
	# 	print("\n\n") 
	# 	settingsData = settings.get_input_data() 

	# 	for key in settingsData.keys(): 
	# 		print(f"{key}\t:\t{settingsData[key]}") 

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
									open_middle=True, max_selected=0, default=1,
									selection_box_height=4)
 
	settings.add.text_input(title="Character to ignore when down (case sensitive) :", textinput_id="IgnoreChar") 
 
	settings.add.toggle_switch( 
		title="Close game when  done", default=False, toggleswitch_id="ExitaAfterCompletion") 

	# settings.add.button(title="Print Settings", action=printSettings, 
	# 					font_color=WHITE, background_color=GREEN) 
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

	mainMenu.add.button(title="Start", action=start(), 
						font_color=WHITE, background_color=RED) 
	mainMenu.mainloop(screen) 

main()