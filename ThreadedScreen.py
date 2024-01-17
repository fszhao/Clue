from threading import Lock

import pygame

from Constants import WHITE, BORDER_RADIUS

# Screen class for updating the display from multiple threads
class ThreadedScreen():
    def __init__(self, size=None):
        # Initialize the screen at the given size, or as a fullscreen
        # display if no size is provided
        self.screen = None
        if size is None:
            self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(size)
        self.screen.fill(WHITE)

        # Lock to prevent concurrent access
        self.lock = Lock()

    # Getter for the size of the display
    def get_size(self):
        return self.screen.get_size()

    # Method to draw to the display. The lock must be acquired before
    # any drawing can occur. The lock is released after drawing is 
    # complete.
    def blit(self, drawable, drawable_pos, draw_rect=None):
        self.lock.acquire()
        try:
            if draw_rect is not None:
                self.screen.blit(drawable, drawable_pos, draw_rect)
                pygame.display.update(draw_rect)
            else:
                self.screen.blit(drawable, drawable_pos)
                pygame.display.update()
        finally:
            self.lock.release()

    # Method to draw a rectangle on the display. The lock must be
    # acquired before any drawing can occur. The lock is released after
    # drawing is complete.
    def drawRect(self, rect, color, border_width):
        self.lock.acquire()
        try:
            pygame.draw.rect(self.screen, color, rect, border_width)
            pygame.display.update()
        finally:
            self.lock.release()

    # Method to safely close the display window
    def close(self):
        pygame.display.quit()