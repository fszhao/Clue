from ctypes import windll, c_int
import time
from queue import Queue
import os

import pygame

from Errors import NoPossibleActionError

from Constants import WHITE, BLACK, GUI_FONT_SIZES, GUI_FONT_THRESHOLDS, GUI_FONT_PATH
from Constants import GAME_START_MESSAGE
from Constants import PICK_ACTION_MESSAGE, ACTION_CONF, ACTION_MESSAGE
from Constants import PICK_MOVE_MESSAGE, MOVE_CONF, MOVE_MESSAGE
from Constants import PICK_SUGGESTION_MESSAGE, PICK_ACCUSATION_MESSAGE

from Drawable import Drawable
from ThreadedScreen import ThreadedScreen
from ClueMap import ClueMap
from PlayerInfoDisplay import PlayerInfoDisplay
from ControlPanel import ControlPanel
from InformationCenter import InformationCenter
from Client import Client
import Card
from Dialogues import ConfirmationDialogue, SuggestionDialogue
from ClientRequest import ClientRequests
from Lobby import Lobby

class ClueGUI():
    def __init__(self):
        windll.shcore.SetProcessDpiAwareness(c_int(1))
        pygame.init()
        self.screen = None

        # Lobby
        self.lobby = None

        # GUI element sizes and positions
        self.gui_size = None
        self.center = None
        self.map_size = None
        self.player_info_size = None
        self.player_info_pos = None
        self.control_size = None
        self.control_pos = None
        self.information_center_size = None
        self.information_center_pos = None

        # Internal display buffer
        self.surface = None

        # Font
        self.font = None

        # Clue Map
        self.clue_map = None

        # Player information
        self.player = None
        self.player_sprite = None

        # Cards
        self.card_deck = None

        # Player Info
        self.player_info_display = None

        # Control Panel
        self.control_panel = None
        
        # Information Center
        self.information_center = None

        # Game control
        self.running = True

        # Client requests
        self.request_queue = Queue()

        # Client
        self.client = Client(self.request_queue)
        self.client.start()

        self.run()

    # Get a font size appropriate to the screen size
    def getFontSize(self):
        gui_width = self.gui_size[0]
        for i in range(len(GUI_FONT_THRESHOLDS) - 1):
            if gui_width >= GUI_FONT_THRESHOLDS[i] and gui_width < GUI_FONT_THRESHOLDS[i+1]:
                return GUI_FONT_SIZES[i]
        return GUI_FONT_SIZES[len(GUI_FONT_SIZES) - 1]

    def initPanelSizes(self):
        panel_width = self.gui_size[0] - self.map_size[0]
        self.player_info_size = (panel_width, (self.player_sprite.image.get_height() // self.player_sprite.image.get_width()) * (panel_width // 4))
        self.player_info_pos = (self.map_size[0], 0)
        half_h = self.gui_size[1] // 2
        self.control_size = (panel_width, half_h - self.player_info_size[1])
        self.control_pos = (self.map_size[0], self.player_info_size[1])
        self.information_center_size = (panel_width, half_h)
        self.information_center_pos = (self.map_size[0], half_h)        

    def initGUI(self, player, player_list):
        self.screen = ThreadedScreen()
        self.player = player
        self.gui_size = self.screen.get_size()
        self.center = (self.gui_size[0] // 2, self.gui_size[1] // 2)
        self.map_size = ((self.gui_size[1] // 7) * 9, self.gui_size[1])
        self.surface = Drawable(self.map_size, (0, 0))
        font_path = os.path.dirname(os.path.realpath(__file__)) + GUI_FONT_PATH
        self.font = pygame.font.Font(font_path, self.getFontSize())
        self.clue_map = ClueMap(self.map_size)
        self.clue_map.initPlayerSprites(player_list)
        self.player_sprite = self.clue_map.getPlayerSprite(self.player.character)
        self.initPanelSizes()
        self.player_info_display = PlayerInfoDisplay(self.player_info_size, self.player_info_pos, list(self.clue_map.player_sprites.values()), self.player, self.font, self.screen)
        self.card_deck = Card.initCards(len(player_list))
        player_cards = [self.card_deck.card_dict[card_name] for card_name in self.player.cards]
        self.control_panel = ControlPanel(self.control_size, self.control_pos, player_cards, self.font)
        self.control_panel.draw(self.screen)
        self.information_center = InformationCenter(self.information_center_size, self.information_center_pos, self.font, self.screen)
        self.updateGUI(player_list)
        self.postMessage(GAME_START_MESSAGE)

    # Clear any dialogues or highlights currently shown
    def clear(self):
        self.surface.draw(self.screen)
        self.control_panel.draw(self.screen)
        self.information_center.draw()

    def updateGUI(self, players):
        self.clue_map.update(players)
        self.clue_map.draw(self.surface)
        self.surface.draw(self.screen)

    def postMessage(self, text, color=BLACK):
        self.information_center.postMessage(text, color)

    # Helper function to get an action/move selection and display the appropriate confirmation dialogue
    def getPlayerResponse(self, valid_actions, click_area, pick_text, conf_text, success_text, move=False):
        if len(valid_actions) == 0:
            raise NoPossibleActionError
        self.postMessage(pick_text)
        click_area.highlight(valid_actions, self.screen)
        if move:
            for i in range(3):
                time.sleep(0.1)
                self.clear()
                time.sleep(0.1)
                click_area.highlight(valid_actions, self.screen)
        done = False
        response = ""
        while not done:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    response = click_area.getClicked(event.pos)
                    if response in valid_actions:
                        click_area.select(response, self.screen)
                        response_conf_text = conf_text + response.text + "?"
                        conf_dialogue = ConfirmationDialogue(self.font, response_conf_text, self.center)
                        conf_dialogue.draw(self.screen)
                        done = conf_dialogue.getResponse()
                        self.clear()
                        if not done:
                            click_area.highlight(valid_actions, self.screen)
                self.information_center.handle_event(event)
        success_text += response.text + "!"
        self.postMessage(success_text)
        return response

    def getSuggestionOrAccusation(self, text, location=None):
        pygame.event.pump()
        suggestion_dialogue = SuggestionDialogue(self.font, text, self.center, self.gui_size[0], self.card_deck, location)
        suggestion_dialogue.draw(self.screen)
        response = suggestion_dialogue.getResponse(self.screen)
        self.clear()
        return response

    def run(self):
        while self.running:
            time.sleep(0.1)
            if self.screen is not None:
                for event in pygame.event.get():
                    self.information_center.handle_event(event)
            if not self.request_queue.empty():
                request = self.request_queue.get()
                print("Client->GUI Request: " + request.id.name)
                self.handleClientRequest(request)

    def handleClientRequest(self, request):
        response = None
        if request.id == ClientRequests.LOBBYINIT:
            self.lobby = Lobby()
        elif request.id == ClientRequests.LOBBYNAME:
            response = self.lobby.getPlayerName()
        elif request.id == ClientRequests.LOBBYSTART:
            response = self.lobby.getStart("FNBC")
        elif request.id == ClientRequests.LOBBYWAIT:
            self.lobby.showWaitingMessage()
        elif request.id == ClientRequests.LOBBYQUIT:
            self.lobby.close()
        elif request.id == ClientRequests.GUIINIT:
            self.initGUI(request.player, request.player_list)
        elif request.id == ClientRequests.GUIUPDATE:
            self.updateGUI(request.player_list)
        elif request.id == ClientRequests.PLAYERACTION:
            response = self.getPlayerResponse(request.valid_actions, self.control_panel, PICK_ACTION_MESSAGE, ACTION_CONF, ACTION_MESSAGE)
        elif request.id == ClientRequests.PLAYERMOVE:
            response = self.getPlayerResponse(request.valid_moves, self.clue_map, PICK_MOVE_MESSAGE, MOVE_CONF, MOVE_MESSAGE, True)
        elif request.id == ClientRequests.PLAYERSUGGESTION:
            response = self.getSuggestionOrAccusation(PICK_SUGGESTION_MESSAGE, request.location)
        elif request.id == ClientRequests.PLAYERACCUSATION:
            response = self.getSuggestionOrAccusation(PICK_ACCUSATION_MESSAGE)
        elif request.id == ClientRequests.GUIMESSAGE:
            self.postMessage(request.message_text, request.message_color)
        elif request.id == ClientRequests.GUIQUIT:
            self.running = False
        elif request.id == ClientRequests.NEXTPLAYER:
            self.player_info_display.next_player()
        if response is not None:
            self.client.response_lock.acquire()
            try:
                self.client.response = response
            finally:
                self.client.response_lock.release()

    def quit(self):
        self.information_center.quit()
        self.screen.close()
        pygame.quit()

ClueGUI().quit()