import time

from pynput import mouse, keyboard

import pygame

from Constants import WHITE, RED, BLUE, BLACK, BORDER_RADIUS

from Drawable import Drawable

class MultiLineTextScroller(Drawable):
    def __init__(self, size, position, font, label, screen):
        Drawable.__init__(self, size, position)
        self.font = font
        self.line_height = font.get_height()
        self.screen = screen

        # Label information
        # The rendered label
        label_obj = self.font.render(label, True, BLACK)
        self.blit(label_obj, (size[0] // 2 - label_obj.get_width() // 2, BORDER_RADIUS))
        # The border around the label
        label_border = pygame.Rect(0, 0, size[0], self.line_height + BORDER_RADIUS * 2)
        pygame.draw.rect(self, BLACK, label_border, BORDER_RADIUS)

        # Text information
        # The text to be displayed
        self.text = ""
        # The colors to draw lines in
        self.colors = []
        # The surface to render the text to
        self.text_surface = pygame.Surface((size[0] - BORDER_RADIUS * 2, size[1] * 100))
        # The area in which the text is displayed
        self.text_box = pygame.Rect(BORDER_RADIUS, label_border.height + BORDER_RADIUS, size[0] - BORDER_RADIUS * 2, size[1] - label_border.height - BORDER_RADIUS * 2)
        # The border around the area in which the text is displayed
        self.text_border = pygame.Rect(0, label_border.height, size[0], size[1] - label_border.height)
        pygame.draw.rect(self, BLACK, self.text_border, BORDER_RADIUS)

        # Scroll information
        # The current scroll position
        self.scroll_y = 0
        # The current max scroll position (based on the current amount of text)
        self.scroll_limit = 0
        # The absolute max scroll position (based on the size of the text surface)
        self.scroll_max_y = self.text_surface.get_height() - self.text_box.height

        self.update()

    def addChar(self, char):
        self.text += char
        self.update(True)

    def deleteChar(self):
        self.text = self.text[:-1]
        self.update(True)

    def addLine(self, line, color=BLACK):
        self.colors.append(color)
        if self.text == "":
            self.text += line
        else:
            self.text += "\n" + line
        self.update(True)

    def scroll(self, dy):
        self.scroll_y -= dy * 10
        self.scroll_y = min(max(self.scroll_y, 0), self.scroll_limit)
        self.update()

    def renderText(self, jump_to_end):
        self.text_surface.fill(WHITE)
        pos = (0, 0)
        lines = self.text.split("\n")
        for i in range(len(lines)):
            color = BLACK
            if len(self.colors) != 0:
                color = self.colors[i]
            if i != 0:
                pos = (0, pos[1] + self.line_height)
            words = lines[i].split(" ")
            for word in words:
                word += " "
                word_object = self.font.render(word, True, color)
                if pos[0] + word_object.get_width() > self.text_box.width:
                    pos = (0, pos[1] + self.line_height)
                self.text_surface.blit(word_object, pos)
                pos = (pos[0] + word_object.get_width(), pos[1])
        self.scroll_limit = min(max(0, pos[1] + self.line_height - self.text_box.height), self.scroll_max_y)
        if jump_to_end:
            self.scroll_y = self.scroll_limit
        return pos

    def update(self, jump_to_end=False):
        self.renderText(jump_to_end)
        text_rect = pygame.Rect((0, self.scroll_y), self.text_box.size)
        self.blit(self.text_surface, self.text_box.topleft, text_rect)
        self.draw(self.screen)


class Notepad(MultiLineTextScroller):
    def __init__(self, size, position, font, screen):
        self.active = False
        MultiLineTextScroller.__init__(self, size, position, font, "Notepad", screen)

    def activate(self):
        self.active = True
        self.update()

    def deactivate(self):
        self.active = False
        self.update()

    def update(self, jump_to_end=False, override_cursor=False):
        cursor_pos = self.renderText(jump_to_end)
        if self.active and not override_cursor:
            cursor_rect = pygame.Rect(cursor_pos[0] - 5, cursor_pos[1], 5, self.line_height)
            pygame.draw.rect(self.text_surface, RED, cursor_rect)
            """
            cursor = self.font.render("|", True, RED)
            self.text_surface.blit(cursor, (cursor_pos[0] - cursor.get_width(), cursor_pos[1]))
            """
        text_rect = pygame.Rect((0, self.scroll_y), self.text_box.size)
        self.blit(self.text_surface, self.text_box.topleft, text_rect)
        border_color = BLACK
        if self.active:
            border_color = BLUE
        pygame.draw.rect(self, border_color, self.text_border, BORDER_RADIUS)
        self.draw(self.screen)