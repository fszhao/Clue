# Colors   
BLACK = (0, 0, 0)
MID_GRAY = (127, 127, 127)
GRAY = (191, 191, 191)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Lobby information
LOBBY_SIZE = (700, 700)
NAME_PROMPT = "Please enter a character name between 1 and 8 characters."
ROOM_CODE_PROMPT = "Please enter a 4 character room code."
START_WAIT_MESSAGE = "Waiting for the game to start..."

# GUI dialogue and message text
GAME_START_MESSAGE = "The game has started!"
PICK_ACTION_MESSAGE = "Pick an action to take!"
ACTION_CONF = "Are you sure you want to "
ACTION_MESSAGE = "You have chosen to "
PICK_MOVE_MESSAGE = "Click on a location to move!"
MOVE_CONF = "Are you sure you want to move to the "
MOVE_MESSAGE = "You moved to the "
PICK_SUGGESTION_MESSAGE = "Pick a player card, weapon card, and location card to make a suggestion!"
PICK_ACCUSATION_MESSAGE = "Pick a player card, weapon card, and location card to make an accusation!"

# GUI font information
GUI_FONT_SIZES = [16, 24, 32, 40, 48]
GUI_FONT_THRESHOLDS = [0, 1280, 1600, 1920, 2560]
GUI_FONT_PATH = "\\assets\\Quikhand.ttf"

# General display information
BORDER_RADIUS = 1
BORDER_DIAMETER = 2

DIALOGUE_BORDER_RADIUS = 5
DIALOGUE_BORDER_DIAMETER = 10

# Map asset and size information
BACKGROUND_ASSET_FILE_PATH = "\\assets\\background_asset.png"
OVERLAY_ASSET_FILE_PATH = "\\assets\\overlay_asset.png"
MAP_SIZE = (1152, 896)

# Location asset information
ROOM_SIZE = (256, 192)
H_HALLWAY_SIZE = (160, 64)
V_HALLWAY_SIZE = (64, 128)
ROOM_CAPTION_OFFSET = (167, 206)
CAPTION_WIDTH = 96
V_WALL_WIDTH = 7
ROOM_PLAYER_OFFSETS = [(96, 32), (96, 96), (32, 32), (32, 96), (160, 32), (160, 96)]
H_HALLWAY_PLAYER_OFFSET = (48, 0)
V_HALLWAY_PLAYER_OFFSET = (0, 32)
LOCATION_DATA_FILE_PATH = "\\assets\\location_assets_data.json"
LOCATION_ASSET_FILE_PATH = "\\assets\\location_assets.png"

# Character asset information
CHARACTER_ASSET_FILE_PATH = "\\assets\\character_assets.png"
NUM_CHARACTERS = 4
CHARACTER_ASSET_SIZE = (64, 64)
CHARACTER_NAME_FONT_SIZE = 18

# Control panel information
ACTION_OPTION_TEXT = ["Move", "Suggest", "Accuse", "End Turn"]