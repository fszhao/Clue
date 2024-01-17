import os

import pygame

from Constants import WHITE, CHARACTER_ASSET_FILE_PATH, NUM_CHARACTERS, CHARACTER_ASSET_SIZE, CHARACTER_NAME_FONT_SIZE

# Basic player Sprite class consisting of a player image and username caption
class PlayerSprite(pygame.Surface):
    def __init__(self, text_obj, character_image, walking_images):
        pygame.Surface.__init__(self, CHARACTER_ASSET_SIZE, pygame.SRCALPHA)
        self.convert()

        self.image = pygame.Surface(CHARACTER_ASSET_SIZE, pygame.SRCALPHA)
        self.image.blit(character_image, (0, -6))
        
        self.blit(character_image, (0, 0))
        self.blit(text_obj, (self.get_width() // 2 - text_obj.get_width() // 2, 0))

        self.walking_images = walking_images

# Loads all player sprites
def initPlayerSprites(players):
    font = pygame.font.SysFont(None, CHARACTER_NAME_FONT_SIZE)
    asset_path = os.path.dirname(os.path.realpath(__file__)) + CHARACTER_ASSET_FILE_PATH
    asset_sheet = pygame.image.load(asset_path)
    player_sprites = {}

    for player in players:
        image = pygame.Surface(CHARACTER_ASSET_SIZE, pygame.SRCALPHA)
        asset_rect = pygame.Rect((0, CHARACTER_ASSET_SIZE[1] * player.character.value), CHARACTER_ASSET_SIZE)
        image.blit(asset_sheet, (0, 0), asset_rect)
        walking_images = []
        for i in range(9):
            walking_image = pygame.Surface(CHARACTER_ASSET_SIZE, pygame.SRCALPHA)
            walking_image_rect = pygame.Rect((i * 64, CHARACTER_ASSET_SIZE[1] * player.character.value + 6), CHARACTER_ASSET_SIZE)
            walking_image.blit(asset_sheet, (0, 0), walking_image_rect)
            walking_images.append(walking_image)
        text_obj = font.render(player.name, True, WHITE)
        player_sprites[player.character] = PlayerSprite(text_obj, image, walking_images)

    return player_sprites