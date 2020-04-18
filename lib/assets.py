import pygame as pg
import os

COLORKEY = (255, 0, 255)

class Assets:
	#Common to both
	ICON1 = None
	ICON2 = None
	ICON3 = None
	ICON4 = None
	ICON5 = None
	ICON6 = None
	ICON7 = None
	ICON8 = None
	ICONS = None

	APP_ICON = None
	APP_LOGO = None

	ARIAL = None

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
	PIXEL = None

	# Client Specific
	CORNER_JAIL = None
	CORNER_FREEPARKING = None
	CORNER_GOTOJAIL = None
	CORNER_START = None

	HOTEL_LANDSCAPE = None
	HOTEL_PORTRAIT = None
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

def import_assets(app, screen_size=None):

	def load_image(image_name):
		image = pg.image.load("assets/images/" + image_name + ".png").convert()
		image.set_colorkey(COLORKEY)
		# Because all images (except the icons) are done to a 1920x1080 resolution, we have to scale them.
		if screen_size:
			w, h = screen_size
			pg.transform.scale(image, (int(w / 1920), int(h / 1080)))
		return image

	def load_icon(icon_name):
		icon = pg.image.load("assets/images/" + icon_name + ".png")
		icon.set_colorkey(COLORKEY)
		return icon

	def load_font(font_name):
		if not os.path.isfile("assets/fonts/" + font_name + ".ttf"):
			font = pg.font.match_font(font_name)
		else:
			font = "assets/fonts/" + font_name + ".ttf"
		return font
		
	if app == "Server":
		Assets.APP_ICON = load_icon("server/app_icon")
		Assets.APP_LOGO = load_image("server/app_logo")

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
		Assets.PIXEL = load_font("pixel")


	elif app == "Client":
		Assets.APP_ICON = load_icon("client/app_icon")
		Assets.APP_LOGO = load_image("client/app_logo")

		Assets.CORNER_JAIL = load_image("client/corner_jail")
		Assets.CORNER_FREEPARKING = load_image("client/corner_freeparking")
		Assets.CORNER_GOTOJAIL = load_image("client/corner_gotojail")
		Assets.CORNER_START = load_image("client/corner_start")

		Assets.HOTEL_LANDSCAPE = load_image("client/hotel_landscape")
		Assets.HOTEL_PORTRAIT = load_image("client/hotel_portrait")
		Assets.HOUSE_EMPTY = load_image("client/house_empty")
		Assets.HOUSE_FILLED = load_image("client/house_filled")
		Assets.MORTAGED = load_image("client/mortaged")

		Assets.COMMUNITY_CHEST = load_image("client/community_chest")
		Assets.LUCK = load_image("client/luck")
		Assets.COMPANY_ELECTRICITY = load_image("client/company_electricity")
		Assets.COMPANY_WATER = load_image("client/company_water")
		Assets.TAX_LUXURY = load_image("client/tax_luxury")
		Assets.TAX_INCOME = load_image("client/tax_income")
		Assets.TRAIN = load_image("client/train")
	else:
		raise ImportError
	#Comon to both
	Assets.ICON1 = load_image("icon_1")
	Assets.ICON2 = load_image("icon_2")
	Assets.ICON3 = load_image("icon_3")
	Assets.ICON4 = load_image("icon_4")
	Assets.ICON5 = load_image("icon_5")
	Assets.ICON6 = load_image("icon_6")
	Assets.ICON7 = load_image("icon_7")
	Assets.ICON8 = load_image("icon_8")
	Assets.ICONS = ["Dummy!", Assets.ICON1, Assets.ICON2, Assets.ICON3, Assets.ICON4, Assets.ICON5, Assets.ICON6, Assets.ICON7, Assets.ICON8]
	Assets.ARIAL = load_font("arial")