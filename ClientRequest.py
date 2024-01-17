from enum import Enum

class ClientRequests(Enum):
    LOBBYINIT = 0
    LOBBYNAME = 1
    LOBBYSTART = 2
    LOBBYWAIT = 3
    LOBBYQUIT = 4
    GUIINIT = 5
    GUIUPDATE = 6
    PLAYERACTION = 7
    PLAYERMOVE = 8
    PLAYERSUGGESTION = 9
    PLAYERACCUSATION = 10
    GUIMESSAGE = 11
    GUIQUIT = 12
    NEXTPLAYER = 13

class ClientRequest:
    def __init__(self, request_id):
        self.id = request_id

class LobbyInitRequest(ClientRequest):
    def __init__(self):
        ClientRequest.__init__(self, ClientRequests.LOBBYINIT)

class NameRequest(ClientRequest):
    def __init__(self):
        ClientRequest.__init__(self, ClientRequests.LOBBYNAME)

class StartRequest(ClientRequest):
    def __init__(self):
        ClientRequest.__init__(self, ClientRequests.LOBBYSTART)

class WaitRequest(ClientRequest):
    def __init__(self):
        ClientRequest.__init__(self, ClientRequests.LOBBYWAIT)

class LobbyQuitRequest(ClientRequest):
    def __init__(self):
        ClientRequest.__init__(self, ClientRequests.LOBBYQUIT)

class GUIInitRequest(ClientRequest):
    def __init__(self, player, player_list):
        ClientRequest.__init__(self, ClientRequests.GUIINIT)
        self.player = player
        self.player_list = player_list

class UpdateRequest(ClientRequest):
    def __init__(self, player_list):
        ClientRequest.__init__(self, ClientRequests.GUIUPDATE)
        self.player_list = player_list

class ActionRequest(ClientRequest):
    def __init__(self, valid_actions):
        ClientRequest.__init__(self, ClientRequests.PLAYERACTION)
        self.valid_actions = valid_actions

class MoveRequest(ClientRequest):
    def __init__(self, valid_moves):
        ClientRequest.__init__(self, ClientRequests.PLAYERMOVE)
        self.valid_moves = valid_moves

class SuggestionRequest(ClientRequest):
    def __init__(self, location):
        ClientRequest.__init__(self, ClientRequests.PLAYERSUGGESTION)
        self.location = location

class AccusationRequest(ClientRequest):
    def __init__(self):
        ClientRequest.__init__(self, ClientRequests.PLAYERACCUSATION)

class MessageRequest(ClientRequest):
    def __init__(self, message_text, message_color):
        ClientRequest.__init__(self, ClientRequests.GUIMESSAGE)
        self.message_text = message_text
        self.message_color = message_color

class GUIQuitRequest(ClientRequest):
    def __init__(self):
        ClientRequest.__init__(self, ClientRequests.GUIQUIT)

class NextPlayerRequest(ClientRequest):
    def __init__(self):
        ClientRequest.__init__(self, ClientRequests.NEXTPLAYER)