# NOTE: SIZES ARE SCALLED TO 1280:720 SCREENS
SIDE_LARGE = 98
SIDE_SMALL = 56
SIZE = 2 * SIDE_LARGE + 9* SIDE_SMALL
BORDER_SIZE = 1
TOOLTIP_SIZE = (476, 100)
TOOLTIP_POS = (int(SIZE/2) - int(TOOLTIP_SIZE[0]/2),SIZE - SIDE_LARGE - TOOLTIP_SIZE[1] - 10)

PLAYER_SIZE = 16
IMAGE_SIZE = 32
HOUSE_SIZE = 13

PLAYER_POSITIONS_OFFSET = [ "Dummy!",
							# 1-4 Players
							[(-int(PLAYER_SIZE/2),-int(PLAYER_SIZE/2))],
							[(-PLAYER_SIZE, -int(PLAYER_SIZE/2)), (0, -int(PLAYER_SIZE/2))],
							[(-PLAYER_SIZE, -PLAYER_SIZE), (0, -PLAYER_SIZE), (-int(PLAYER_SIZE/2), 0)],
							[(-PLAYER_SIZE, -PLAYER_SIZE), (0, -PLAYER_SIZE), (-PLAYER_SIZE, 0), (0, 0)],
							# 5-8 Players
							[(-PLAYER_SIZE, -PLAYER_SIZE), (0, -PLAYER_SIZE), (-PLAYER_SIZE, 0), (0, 0),
							(-int(PLAYER_SIZE/2),-int(PLAYER_SIZE/2))],
							[(-PLAYER_SIZE, -PLAYER_SIZE),(0, -PLAYER_SIZE), (-PLAYER_SIZE, 0), (0, 0),
							(-PLAYER_SIZE, -int(PLAYER_SIZE/2)), (0, -int(PLAYER_SIZE/2))],
							[(-PLAYER_SIZE, -PLAYER_SIZE), (0, -PLAYER_SIZE), (-PLAYER_SIZE, 0), (0, 0),
							(-PLAYER_SIZE, -PLAYER_SIZE), (0, -PLAYER_SIZE), (-int(PLAYER_SIZE/2), 0)],
							[(-PLAYER_SIZE, -PLAYER_SIZE), (0, -PLAYER_SIZE), (-PLAYER_SIZE, 0), (0, 0),
							(-PLAYER_SIZE, -PLAYER_SIZE), (0, -PLAYER_SIZE), (-PLAYER_SIZE, 0), (0, 0)]
							]
							
IMAGE_OFFSET = (-int(IMAGE_SIZE/2), -int(IMAGE_SIZE/2))

HOUSE_OFFSETS = {
				"L": {"x": ["Dummy!"] + [(SIDE_LARGE - BORDER_SIZE*2) - HOUSE_SIZE for _ in range(5)],
						"y": ["Dummy!"] + [i * HOUSE_SIZE for i in range(4)] + [0]},
				"R": {"x": ["Dummy!"] + [0 for _ in range(5)],
						"y": ["Dummy!"] + [i* HOUSE_SIZE for i in range(4)] + [0]},
				"T": {"x": ["Dummy!"] + [i * HOUSE_SIZE for i in range(4)] + [0],
						"y": ["Dummy!"] + [(SIDE_LARGE - BORDER_SIZE*2) - HOUSE_SIZE for _ in range(5)]},
				"B": {"x":["Dummy!"] + [i * HOUSE_SIZE for i in range(4)] + [0],
						"y": ["Dummy!"] + [0 for _ in range(5)]}
				}

CENTER_OFFSETS = {
				"L": (int((SIDE_LARGE - BORDER_SIZE*2 - HOUSE_SIZE)/2), int((SIDE_SMALL - BORDER_SIZE*2)/2)),
				"R": (int((SIDE_LARGE - BORDER_SIZE*2 - HOUSE_SIZE)/2) + HOUSE_SIZE, int((SIDE_SMALL - BORDER_SIZE*2)/2)),
				"T": (int((SIDE_SMALL - BORDER_SIZE*2)/2), int((SIDE_LARGE - BORDER_SIZE*2 - HOUSE_SIZE)/2)),
				"B": (int((SIDE_SMALL - BORDER_SIZE*2)/2), int((SIDE_LARGE - BORDER_SIZE*2 - HOUSE_SIZE)/2) + HOUSE_SIZE)
				}

def get_rgb(string):
	'''
	Returns the RGB code of the color named. If not recognized, returns white.
	'''
	if string == "brown":
		return (51,25,0)
	elif string == "light-blue":
		return (102,178,255)
	elif string == "magenta":
		return (204, 0, 204)
	elif string == "orange":
		return (204, 102, 0)
	elif string == "red":
		return (255, 0, 0)
	elif string == "yellow":
		return (204, 204, 0)
	elif string == "green":
		return (0, 128, 0)
	elif string == "blue":
		return (48, 79, 254)
	return (0,0,0)