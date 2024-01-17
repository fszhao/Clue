import pygame

from MultiLineTextScrollers import MultiLineTextScroller, Notepad

class InformationCenter():
    def __init__(self, size, position, font, screen):
        half_size = (size[0], size[1] // 2)
        self.message_queue = MultiLineTextScroller(half_size, position, font, "Messages", screen)
        notepad_pos = (position[0], position[1] + half_size[1])
        self.notepad = Notepad(half_size, notepad_pos, font, screen)

        self.screen = screen

    def postMessage(self, text, color):
        self.message_queue.addLine(text, color)

    def click(self, event:pygame.event.Event):
        if self.notepad.active and not self.notepad.rect.collidepoint(event.pos):
            self.notepad.deactivate()
        elif not self.notepad.active and self.notepad.rect.collidepoint(event.pos):
            self.notepad.activate()

    def scroll(self, event:pygame.event.Event):
        pos = pygame.mouse.get_pos()
        if self.message_queue.rect.collidepoint(pos):
            self.message_queue.scroll(event.y)
        elif self.notepad.rect.collidepoint(pos):
            self.notepad.scroll(event.y)

    # Key listener methods
    def press(self, event:pygame.event.Event):
        if event.key == pygame.K_BACKSPACE:
            self.notepad.deleteChar()
        elif event.key == pygame.K_SPACE:
            self.notepad.addChar(" ")
        elif event.key == pygame.K_RETURN:
            self.notepad.addChar("\n")
        else:
            try:
                self.notepad.addChar(event.unicode)
            except:
                pass

    def handle_event(self, event:pygame.event.Event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.click(event)
        elif event.type == pygame.KEYDOWN:
            self.press(event)

    def draw(self):
        self.notepad.update()
        self.message_queue.update()

    # Method to safely end key/mouse listener threads
    def quit(self):
        return