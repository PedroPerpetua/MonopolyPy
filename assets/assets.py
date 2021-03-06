import pygame as pg
import os

class Colors:
	COLORKEY = (255, 0, 255)
	BG_COLOR = (143, 188, 114)
	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)
	SELECTED = (204, 204, 0)
	LIGHT_GRAY = (128, 128, 128)
	LIGHT_CYAN = (153, 255, 255)
	BROWN = (51, 25, 0)
	LIGHT_BLUE = (102, 178, 255)
	MAGENTA = (204, 0, 204)
	ORANGE = (204, 102, 0)
	RED = (255, 0, 0)
	YELLOW = (204, 204, 0)
	GREEN = (0, 128, 0)
	BLUE = (48, 79, 254)

	@staticmethod
	def get_color(string):
		if string in ["BROWN", "LIGHT_BLUE", "MAGENTA", "ORANGE", "RED", "YELLOW", "GREEN", "BLUE"]:
			return getattr(Colors, string)
		raise ValueError

class Assets:
	#Common to both
	ICONS = {"SMALL": ["Dummy!"], "MEDIUM": ["Dummy!"], "LARGE": ["Dummy!"]}
	APP_ICON = None
	APP_LOGO = None
	HELP_SELECTED = None
	HELP_UNSELECTED = None
	RETURN_SELECTED = None
	RETURN_UNSELECTED = None
	ABOUT = None
	GIT_SELECTED = None
	GIT_UNSELECTED = None

	ARIAL = None
	PIXEL = None

	# Server Specific
	LOCKED_SLOT = None
	START_SELECTED = None
	START_UNSELECTED = None
	MINUS_SELECTED = None
	MINUS_UNSELECTED = None
	PLUS_SELECTED = None
	PLUS_UNSELECTED = None
	GAME_STARTED = None
	QUIT_SELECTED = None
	QUIT_UNSELECTED = None
	INTERNET_SELECTED = None
	INTERNET_UNSELECTED = None
	X_SELECTED = None
	X_UNSELECTED = None


	# Client Specific
	CONNECT_SELECTED = None
	CONNECT_UNSELECTED = None
	SUBMIT_SELECTED = None
	SUBMIT_UNSELECTED = None

	CORNER_START = None
	CORNER_JAIL = None
	CORNER_FREEPARKING = None
	CORNER_GOTOJAIL = None
	HOTEL_VERTICAL = None
	HOTEL_HORIZONTAL = None
	HOUSE_EMPTY = None
	HOUSE_FILLED = None
	MORTAGED = None
	COMMUNITY_CHEST = None
	LUCK = None
	COMPANY_ELECTRICITY = None
	COMPANY_WATER = None
	TAX_LUXURY = None
	TAX_INCOME = None
	TRAIN = None

def import_assets(app):

	def load_image(image_name, convert=True):
		if convert:
			image = pg.image.load("assets/images/" + image_name + ".png").convert()
		else:
			image = pg.image.load("assets/images/" + image_name + ".png")
		image.set_colorkey(Colors.COLORKEY)
		return image

	def load_icon(icon_number):
		for size in ["SMALL", "MEDIUM", "LARGE"]:
			icon = pg.image.load("assets/images/icons/icon_" + str(icon_number) + "_" + size + ".png").convert()
			icon.set_colorkey(Colors.COLORKEY)
			Assets.ICONS[size] += [icon]

	def load_font(font_name):
		if not os.path.isfile("assets/fonts/" + font_name + ".ttf"):
			font = pg.font.match_font(font_name)
		else:
			font = "assets/fonts/" + font_name + ".ttf"
		return font
		
	if app == "Server":
		Assets.APP_ICON = load_image("server/app_icon", False)
		Assets.APP_LOGO = load_image("server/app_logo")
		Assets.HELP_SELECTED = load_image("server/help_selected")
		Assets.HELP_UNSELECTED = load_image("server/help_unselected")
		Assets.ABOUT = load_image("server/about")
		Assets.GIT_SELECTED = load_image("server/git_selected")
		Assets.GIT_UNSELECTED = load_image("server/git_unselected")

		Assets.LOCKED_SLOT = load_image("server/slot_locked")
		Assets.START_SELECTED = load_image("server/start_selected")
		Assets.START_UNSELECTED = load_image("server/start_unselected")
		Assets.MINUS_SELECTED = load_image("server/minus_selected")
		Assets.MINUS_UNSELECTED = load_image("server/minus_unselected")
		Assets.PLUS_SELECTED = load_image("server/plus_selected")
		Assets.PLUS_UNSELECTED = load_image("server/plus_unselected")
		Assets.GAME_STARTED = load_image("server/game_started")
		Assets.QUIT_SELECTED = load_image("server/quit_selected")
		Assets.QUIT_UNSELECTED = load_image("server/quit_unselected")
		Assets.RETURN_SELECTED = load_image("server/return_selected")
		Assets.RETURN_UNSELECTED = load_image("server/return_unselected")
		Assets.INTERNET_SELECTED = load_image("server/internet_selected")
		Assets.INTERNET_UNSELECTED = load_image("server/internet_unselected")
		Assets.X_SELECTED = load_image("server/x_selected")
		Assets.X_UNSELECTED = load_image("server/x_unselected")	

	elif app == "Client":
		Assets.APP_ICON = load_image("client/app_icon", False)
		Assets.APP_LOGO = load_image("client/app_logo")
		Assets.HELP_SELECTED = load_image("client/help_selected")
		Assets.HELP_UNSELECTED = load_image("client/help_unselected")
		Assets.RETURN_SELECTED = load_image("client/return_selected")
		Assets.RETURN_UNSELECTED = load_image("client/return_unselected")
		Assets.ABOUT = load_image("client/about")
		Assets.GIT_SELECTED = load_image("client/git_selected")
		Assets.GIT_UNSELECTED = load_image("client/git_unselected")

		Assets.CONNECT_SELECTED = load_image("client/connect_selected")
		Assets.CONNECT_UNSELECTED = load_image("client/connect_unselected")
		Assets.SUBMIT_SELECTED = load_image("client/submit_selected")
		Assets.SUBMIT_UNSELECTED = load_image("client/submit_unselected")

		Assets.CORNER_JAIL = load_image("client/board/corner_jail")
		Assets.CORNER_FREEPARKING = load_image("client/board/corner_freeparking")
		Assets.CORNER_GOTOJAIL = load_image("client/board/corner_gotojail")
		Assets.CORNER_START = load_image("client/board/corner_start")
		Assets.HOTEL_VERTICAL = load_image("client/board/hotel_vertical")
		Assets.HOTEL_HORIZONTAL = load_image("client/board/hotel_horizontal")
		Assets.HOUSE_EMPTY = load_image("client/board/house_empty")
		Assets.HOUSE_FILLED = load_image("client/board/house_filled")
		Assets.MORTAGED = load_image("client/board/mortaged")
		Assets.COMMUNITY_CHEST = load_image("client/board/community_chest")
		Assets.LUCK = load_image("client/board/luck")
		Assets.COMPANY_ELECTRICITY = load_image("client/board/company_electricity")
		Assets.COMPANY_WATER = load_image("client/board/company_water")
		Assets.TAX_LUXURY = load_image("client/board/tax_luxury")
		Assets.TAX_INCOME = load_image("client/board/tax_income")
		Assets.TRAIN = load_image("client/board/train")
		Assets.X_SELECTED = load_image("client/x_selected")
		Assets.X_UNSELECTED = load_image("client/x_unselected")
	#Comon to both
	Assets.PIXEL = load_font("Pixel")
	Assets.ARIAL = load_font("arial")
	for i in range(1, 9):
		load_icon(i)