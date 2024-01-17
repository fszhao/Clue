import math

import pygame

from Constants import WHITE, MID_GRAY, BLACK, RED, BLUE, BORDER_RADIUS, BORDER_DIAMETER, ACTION_OPTION_TEXT

from ClueEnums import Actions

from Drawable import Selectable, GrayOut, Button

class ControlPanel(Selectable):
    def __init__(self, size, position, cards, font):
        Selectable.__init__(self, size, position)
        self.fill(MID_GRAY)

        # Player cards sizes and positions
        card_width = (size[0] - BORDER_RADIUS * 4) // 3
        card_height = 4 * (card_width // 3)
        card_slot_width = card_width + BORDER_RADIUS * 2
        card_slot_height = card_height + BORDER_RADIUS * 2

        left_slot = pygame.Rect(0, 0, card_slot_width, card_slot_height)
        center_slot = pygame.Rect(card_slot_width, 0, card_slot_width, card_slot_height)
        right_slot = pygame.Rect(card_slot_width * 2, 0, card_slot_width, card_slot_height)

        left_card_pos = (left_slot.x + BORDER_RADIUS, BORDER_RADIUS)
        center_card_pos = (center_slot.x + BORDER_RADIUS, BORDER_RADIUS)
        right_card_pos = (right_slot.x + BORDER_RADIUS, BORDER_RADIUS)

        # Render player cards
        pygame.draw.rect(self, BLACK, left_slot, BORDER_RADIUS)
        pygame.draw.rect(self, BLACK, center_slot, BORDER_RADIUS)
        pygame.draw.rect(self, BLACK, right_slot, BORDER_RADIUS)
        self.blit(pygame.transform.smoothscale(cards[0], (card_width, card_height)), left_card_pos)
        self.blit(pygame.transform.smoothscale(cards[1], (card_width, card_height)), center_card_pos)
        self.blit(pygame.transform.smoothscale(cards[2], (card_width, card_height)), right_card_pos)

        # Button sizes and positions
        button_height = (size[1] - card_slot_height) // 4
        self.buttons = []
        self.initButtons((size[0], button_height), card_slot_height, font)

        # Render buttons
        for button in self.buttons:
            self.blit(button, button.position)

    # Helper method to initialize the action buttons
    def initButtons(self, size, start_y, font):
        x = size[0] // 2
        y = start_y + size[1] // 2
        for index,action_text in enumerate(ACTION_OPTION_TEXT):
            text_obj = font.render(action_text, True, BLACK)
            self.buttons.append(Button(text_obj, (x, y), Actions(index), size))
            y += size[1]

    def highlight(self, valid_actions, screen):
        for button in self.buttons:
            if button.return_value not in valid_actions:
                button_true_pos = (self.position[0] + button.position[0], self.position[1] + button.position[1])
                GrayOut(button.size, button_true_pos).draw(screen)
        tl = (self.position[0] + self.buttons[0].position[0] + BORDER_RADIUS, self.position[1] + self.buttons[0].position[1] + BORDER_RADIUS)
        last = self.buttons[len(self.buttons) - 1]
        br = (self.position[0] + last.position[0] + last.size[0] - BORDER_RADIUS, self.position[1] + last.position[1] + last.size[1] - BORDER_RADIUS)
        size = (br[0] - tl[0], br[1] - tl[1])
        screen.drawRect(pygame.Rect(tl, size), BLUE, BORDER_DIAMETER)

    def select(self, action, screen):
        for button in self.buttons:
            if button.return_value == action:
                button_true_pos = (self.position[0] + button.position[0], self.position[1] + button.position[1])
                button_rect = pygame.Rect(button_true_pos, button.size)
                screen.drawRect(button_rect, BLACK, BORDER_RADIUS * 4)

    # Click detection methods for the action buttons
    def getClicked(self, click_pos):
        adj_pos = (click_pos[0] - self.position[0], click_pos[1] - self.position[1])
        for button in self.buttons:
            if button.rect.collidepoint(adj_pos):
                return button.return_value
        return None