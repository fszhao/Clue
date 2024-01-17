import Player as pl

class Wrapper:
    def __init__(self):
        print("hello")
# Not implimented    
class MsgGameStart:
    def __init__(self,indviPlayer,gameInfo):
        self.indviPlayer = indviPlayer
        self.gameInfo = gameInfo
        self.clientMessage = " Game is starting"
        print("Server -> client 100")
# Not implimented    
class MsgPlayerReadyResp:
    def __init__(self):
        pass #stuff
# used to update the info class 
class MsgUpdateGame():
    def __init__(self, info):
        self.info = info
# wrapper for starting message
class MsgLobbyReady():
    def __init__(self):
        self.start = "start_game"
    def __str__(self):
        return "msg: start game"
# wrapper used to pass player objects
class MsgMovePlayer():
    def __init__(self, player):
        self.player = player
        print("client -> server 102")

# used to pass player numbers/positions
class MsgPassPlayerNum():
    def __init__(self,num,indviPlayer):
        self.indviPlayer = indviPlayer
        self.playerNum = num
        print("server -> client 103")

# used to update the info class / can be replaced with MsgUpdateGame??
class MsgPassInformation():
    def __init__(self,info):
        print("server -> client: 501")
        self.info = info
# wrapper to update players
class MsgUpdatePlayer():
    def __init__(self,player):
        self.player = player

class MsgStartTurn():
    def __init__(self):
        print("server -> client 105")
        pass

class MsgContinueTurn():
    def __init__(self):
        print("server -> client 106")
        pass

class MsgSuggest():
    def __init__(self, suggestion):
        self.suggestion = suggestion
        print("client -> server 107")

class MsgSuggestResp():
    def __init__(self, disprov_card, disprov_player, playerNum, suggestion, name):
        self.suggestion = suggestion
        self.disprov_card = disprov_card 
        self.disprov_player = disprov_player 
        self.playerNum = playerNum
        self.name = name
        print("server -> client 201")

class MsgAccuse():
    def __init__(self, accusation):
        self.accusation = accusation
        print("client -> server 108")

class MsgEndTurn():
    def __init__(self):
        print("client -> server 109")
        pass

class MsgNextTurn():
    def __init__(self,name):
        self.name = name

class MsgGameWon():
    def __init__(self,name,accusation):
        self.name = name
        self.accusation = accusation

class MsgGameLost():
    def __init__(self,name,playerNum,accusation):
        self.name = name
        self.playerNum = playerNum
        self.accusation = accusation

class MsgGameLostAll():
    def __init__(self, caseFile):
        self.caseFile = caseFile
    
class HeaderNew:
    # dict of keys based on classes to give ids to check later
    ids = {
        MsgGameStart: 100,
        MsgPlayerReadyResp: 101,
        MsgMovePlayer: 102,
        MsgPassPlayerNum: 103,
        MsgUpdatePlayer: 104,
        MsgStartTurn: 105,
        MsgContinueTurn: 106,
        MsgSuggest: 107,
        MsgAccuse: 108,
        MsgEndTurn: 109,
        MsgNextTurn: 110,
        MsgSuggestResp: 201,
        MsgUpdateGame: 500,
        MsgPassInformation: 501,
        MsgLobbyReady: 1000,
        MsgGameLost: 6666,
        MsgGameLostAll: 6667,
        MsgGameWon: 7777,
    }
    
    def __init__(self, data):
        self.id = self.ids.get(type(data), 0)
        # print(self.id)
        self.data = data

