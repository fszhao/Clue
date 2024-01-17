import os
import json

import pygame

from Errors import RoomOverflowError

from Constants import GRAY, BLACK, BORDER_RADIUS
from Constants import ROOM_SIZE, H_HALLWAY_SIZE, V_HALLWAY_SIZE, ROOM_CAPTION_OFFSET, CAPTION_WIDTH, V_WALL_WIDTH
from Constants import ROOM_PLAYER_OFFSETS, H_HALLWAY_PLAYER_OFFSET, V_HALLWAY_PLAYER_OFFSET
from Constants import LOCATION_DATA_FILE_PATH, LOCATION_ASSET_FILE_PATH

from ClueEnums import Locations

from Drawable import Drawable

# Base class for all locations
class LocationSprite(Drawable):
    def __init__(self, image, position, size, collision_box):
        Drawable.__init__(self, size, position, True)
        self.image = image
        self.collision_box = collision_box

    def clearPlayers(self):
        raise NotImplementedError

    def addPlayer(self, player):
        raise NotImplementedError

    def drawPlayers(self):
        raise NotImplementedError

    def update(self):
        self.blit(self.image, (0, 0))
        self.drawPlayers()

# Subclass of LocationSprite for rooms
class RoomSprite(LocationSprite):
    def __init__(self, image, position, collision_box, caption):
        size = (ROOM_SIZE[0] + V_WALL_WIDTH, ROOM_CAPTION_OFFSET[1] + caption.get_height())
        LocationSprite.__init__(self, image, position, size, collision_box)
        self.caption = caption
        self.players = []

    # Empties the list of players currently in the room
    def clearPlayers(self):
        self.players = []

    # Adds a player to the room if there are less than 4 currently
    # in it
    def addPlayer(self, player):
        self.players.append(player)

    # Renders the players currently in the room
    def drawPlayers(self):
        for index,player in enumerate(self.players):
            self.blit(player, ROOM_PLAYER_OFFSETS[index])

    def update(self):
        LocationSprite.update(self)
        self.blit(self.caption, ROOM_CAPTION_OFFSET)

# Subclass of LocationSprite for hallways
class HallwaySprite(LocationSprite):
    def __init__(self, image, position, size, collision_box, player_offset):
        LocationSprite.__init__(self, image, position, size, collision_box)
        self.player = None
        self.player_offset = player_offset

    # Removes any player currently in the hallway
    def clearPlayers(self):
        self.player = None

    # Adds a player to the hallway if there is not one already
    def addPlayer(self, player):
        if self.player is not None:
            raise RoomOverflowError
        self.player = player

    # Renders a player in the hallway
    def drawPlayers(self):
        if self.player is not None:
            self.blit(self.player, self.player_offset)

# Loads all location sprites and returns them as an (id, locationSprite) dictionary
def initLocationSprites(scale):
    font = pygame.font.SysFont(None, 16)
    location_data_path = os.path.dirname(os.path.realpath(__file__)) + LOCATION_DATA_FILE_PATH
    with open(location_data_path) as data_file:
        location_data = json.load(data_file)
    asset_path = os.path.dirname(os.path.realpath(__file__)) + LOCATION_ASSET_FILE_PATH
    asset_sheet = pygame.image.load(asset_path)
    location_sprites = {}

    for index,data_dict in enumerate(location_data):
        asset_pos = tuple(int(num) for num in data_dict["asset"].replace('(', '').replace(')', '').split(', '))
        position = tuple(int(num) for num in data_dict["position"].replace('(', '').replace(')', '').split(', '))
        if data_dict["type"] == "room":
            text_obj = font.render(data_dict["name"], True, BLACK)
            caption = pygame.Surface((CAPTION_WIDTH, text_obj.get_height() + BORDER_RADIUS * 2))
            caption.fill(GRAY)
            pygame.draw.rect(caption, BLACK, pygame.Rect(0, 0, CAPTION_WIDTH, text_obj.get_height() + BORDER_RADIUS * 2), BORDER_RADIUS)
            caption.blit(text_obj, (CAPTION_WIDTH // 2 - text_obj.get_width() // 2, BORDER_RADIUS))
            image = pygame.Surface(ROOM_SIZE).convert()
            image.blit(asset_sheet, (0, 0), pygame.Rect(asset_pos, ROOM_SIZE))
            collision_box = pygame.Rect((position[0] * scale, position[1] * scale), (ROOM_SIZE[0] * scale, ROOM_SIZE[1] * scale))
            location_sprites[Locations(index)] = RoomSprite(image, position, collision_box, caption)
        elif data_dict["type"] == "horizontal":
            image = pygame.Surface(H_HALLWAY_SIZE).convert()
            image.blit(asset_sheet, (0, 0), pygame.Rect(asset_pos, H_HALLWAY_SIZE))
            collision_box = pygame.Rect((position[0] * scale, position[1] * scale), (H_HALLWAY_SIZE[0] * scale, H_HALLWAY_SIZE[1] * scale))
            location_sprites[Locations(index)] = HallwaySprite(image, position, H_HALLWAY_SIZE, collision_box, H_HALLWAY_PLAYER_OFFSET)
        else:
            image = pygame.Surface(V_HALLWAY_SIZE).convert()
            image.blit(asset_sheet, (0, 0), pygame.Rect(asset_pos, V_HALLWAY_SIZE))
            collision_box = pygame.Rect((position[0] * scale, position[1] * scale), (V_HALLWAY_SIZE[0] * scale, V_HALLWAY_SIZE[1] * scale))
            location_sprites[Locations(index)] = HallwaySprite(image, position, V_HALLWAY_SIZE, collision_box, V_HALLWAY_PLAYER_OFFSET)

    return location_sprites