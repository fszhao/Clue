import time
from threading import Thread

import pygame

from Constants import GRAY, BLACK, BORDER_RADIUS

from Drawable import Drawable

class PlayerInfoDisplay(Drawable, Thread):
    def __init__(self, size, position, player_sprites, player, font, screen):
        self.screen = screen
        Drawable.__init__(self, size, position)
        Thread.__init__(self, daemon=True)
        self.fill(GRAY)

        # Player info box sizes and rectangles
        data_size = (size[0] // 2, size[1])
        self.left_data = pygame.Rect((0, 0), data_size)
        right_data = pygame.Rect((data_size[0], 0), data_size)

        # Player info text
        player_name = font.render(player.name, True, BLACK)
        player_character = font.render(player.character.text, True, BLACK)
        player_info = pygame.Surface((max(player_name.get_width(), player_character.get_width()), font.get_height() * 2), pygame.SRCALPHA)
        player_info.blit(player_name, (player_info.get_width() // 2 - player_name.get_width() // 2, 0))
        player_info.blit(player_character, (player_info.get_width() // 2 - player_character.get_width() // 2, font.get_height()))
        player_info_pos = (right_data.centerx - player_info.get_width() // 2, right_data.centery - player_info.get_height() // 2)

        # Render borders
        pygame.draw.rect(self, BLACK, right_data, BORDER_RADIUS)
        self.blit(player_info, player_info_pos)

        # Player image stuff
        self.player_sprites = player_sprites
        self.num_players = len(self.player_sprites)
        self.curr_player = 0
        self.walking_images = self.player_sprites[self.curr_player].walking_images
        self.left_image = self.player_sprites[self.curr_player - 1].image
        self.right_image = self.player_sprites[(self.curr_player + 1) % self.num_players].image
        self.current_image = 0
        self.image_size = (data_size[0] // 2, size[1])
        self.image_pos = (self.left_data.centerx - self.image_size[0] // 2, self.left_data.centery - self.image_size[1] // 2)
        self.side_size = (self.image_size[0] // 2, self.image_size[1] // 2)
        self.left_pos = (self.image_pos[0] - self.side_size[0], self.left_data.centery - self.side_size[1] // 2)
        self.right_pos = (self.image_pos[0] + self.image_size[0], self.left_data.centery - self.side_size[1] // 2)

        self.start()

    def next_player(self):
        self.curr_player = (self.curr_player + 1) % self.num_players
        self.walking_images = self.player_sprites[self.curr_player].walking_images
        self.left_image = self.player_sprites[self.curr_player - 1].image
        self.right_image = self.player_sprites[(self.curr_player + 1) % self.num_players].image

    def run(self):
        while True:
            image = self.walking_images[self.current_image]
            self.current_image = (self.current_image + 1) % len(self.walking_images)
            pygame.draw.rect(self, GRAY, self.left_data)
            self.blit(pygame.transform.smoothscale(image, self.image_size), self.image_pos)
            self.blit(pygame.transform.smoothscale(self.left_image, self.side_size), self.left_pos)
            self.blit(pygame.transform.smoothscale(self.right_image, self.side_size), self.right_pos)
            pygame.draw.rect(self, BLACK, self.left_data, BORDER_RADIUS)
            self.draw(self.screen)
            time.sleep(0.2)
        