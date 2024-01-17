import os
import pickle
import Player as pl
import Wrapper as wrap
import Information as info
import Lobby
import asyncio
import ClueEnums
from ClueEnums import Actions, LobbyButtons
import AdjList
import time
from Constants import RED, GREEN, BLACK
import threading
from ClientRequest import *
import pygame
import os

player = pl.Player()


class Client(threading.Thread):
    def __init__(self, request_queue):
        threading.Thread.__init__(self)
        self.running = False
        self.info = info.Information()
        self.validMoves = []
        self.actionList = []
        self.lost = False
        self.myNumber = None
        self.suggested = False
        self.soundVolume = 0.0 # sound volume as fraction of 100 (0.01 --> 1%)
        self.musicVolume = 0.0 # music volume as fraction of 100 (0.03 --> 3%)
        self.repeat = -1 # music repeat setting (-1 means infinite repeat)
        sound_path = os.path.dirname(os.path.realpath(__file__)) + "\\sounds\\"

        # initializes all game action sounds
        self.suggest_sound = pygame.mixer.Sound(sound_path + 'Suggest.wav')
        self.accuse_sound = pygame.mixer.Sound(sound_path + 'Accuse.wav')
        self.move_sound = pygame.mixer.Sound(sound_path + 'Move.wav')
        self.won_sound = pygame.mixer.Sound(sound_path + 'Won.wav')
        self.lost_sound = pygame.mixer.Sound(sound_path + 'Lost.wav')

        # initializes in game soundtrack and starts playing music
        pygame.mixer.music.load(sound_path + "Clue-Less_Soundtrack.mp3")
        self.change_volume()
        pygame.mixer.music.play(self.repeat)

        # GUI request queue
        self.request_queue = request_queue

        # GUI response
        self.response = None
        self.response_lock = threading.Lock()

    def change_volume(self, dv=0):
        if dv < 0 and self.soundVolume > 0:
            self.soundVolume -= 0.01
            self.musicVolume -= 0.01
        elif dv > 0 and self.musicVolume < 1:
            self.soundVolume += 0.01
            self.musicVolume += 0.01
        pygame.mixer.Sound.set_volume(self.suggest_sound, self.soundVolume)
        pygame.mixer.Sound.set_volume(self.accuse_sound, self.soundVolume)
        pygame.mixer.Sound.set_volume(self.move_sound, self.soundVolume)
        pygame.mixer.Sound.set_volume(self.won_sound, self.soundVolume)
        pygame.mixer.Sound.set_volume(self.lost_sound, self.soundVolume)
        pygame.mixer.music.set_volume(self.musicVolume)

    async def handle_server(self,reader,writer):
        # start the lobby
        self.request_queue.put(LobbyInitRequest())
        # get name from lobby
        self.request_queue.put(NameRequest())
        name = self.getGUIResponse()

        player.name = name
        player.location = "ballroom"
        # send msg across pipe to update server player
        msgWrap = wrap.MsgUpdatePlayer(player)
        helper = wrap.HeaderNew(msgWrap)
        data_string = pickle.dumps(helper)
        writer.write(data_string)

        buf = 2048

        while self.running:
            # async wait to read data from server and process them below
            # based on msg.id
            data = await reader.read(buf)
            data_var = pickle.loads(data)
            print("Received message from server: " + str(data_var.id))
            if (data_var.id == 103):
                # Player number received from server
                print(f"Client Player Number: {data_var.data.playerNum}")
                self.myNumber = data_var.data.playerNum
                if(data_var.data.playerNum == 0):
                    # Player 1, give start button (now called getStart())
                    start = False
                    while not start:
                        self.request_queue.put(StartRequest())
                        response = self.getGUIResponse()
                        if response == LobbyButtons.VOLUP:
                            self.change_volume(1)
                        elif response == LobbyButtons.VOLDOWN:
                            self.change_volume(-1)
                        else:
                            start = True
                    data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgLobbyReady()))
                    writer.write(data_string)
                else:
                    start = False
                    while not start:
                        self.request_queue.put(StartRequest())
                        response = self.getGUIResponse()
                        if response == LobbyButtons.VOLUP:
                            self.change_volume(1)
                        elif response == LobbyButtons.VOLDOWN:
                            self.change_volume(-1)
                        else:
                            start = True
                    self.request_queue.put(WaitRequest()) 

            # General location update message (new locations in storeAllPlayers)   
            elif( data_var.id == 501):
                self.info = data_var.data.info
                self.request_queue.put(UpdateRequest(self.info.storeAllPlayers))

            # Game start message
            elif(data_var.id == 100):
                self.request_queue.put(LobbyQuitRequest())
                self.info = data_var.data.gameInfo
                self.request_queue.put(GUIInitRequest(data_var.data.indviPlayer,self.info.storeAllPlayers))

            # Next player's turn
            elif(data_var.id == 110):
                player_name = data_var.data.name
                self.request_queue.put(MessageRequest("It's " + player_name + "'s turn!", BLACK))
                self.request_queue.put(NextPlayerRequest())

            # Turn start message for this client's player
            elif(data_var.id == 105):
                self.request_queue.put(MessageRequest("Your turn has begun!", GREEN))
                self.suggested = False
                self.validMoves = AdjList.determineValidMoves(self.info.storeAllPlayers[self.myNumber], self.info.storeAllPlayers)

                if (self.lost and len(self.validMoves) == 0):
                    self.actionList = [Actions.ENDTURN]
                elif (self.lost):
                    self.actionList = [Actions.MOVE]
                elif (len(self.validMoves) == 0 and ClueEnums.isRoom(self.info.storeAllPlayers[self.myNumber].location)):
                    self.actionList = [Actions.ACCUSE, Actions.SUGGEST, Actions.ENDTURN]
                elif (len(self.validMoves) == 0):
                    self.actionList = [Actions.ACCUSE, Actions.ENDTURN]
                elif (ClueEnums.isRoom(self.info.storeAllPlayers[self.myNumber].location)):
                    self.actionList = [Actions.MOVE, Actions.ACCUSE, Actions.SUGGEST]
                else:
                    self.actionList = [Actions.MOVE, Actions.ACCUSE]

                self.request_queue.put(ActionRequest(self.actionList))
                action = self.getGUIResponse()
                self.actionList.remove(action)
                msg = self.handleAction(action)
                writer.write(msg)
                
            # Turn continue message for this client's player
            elif(data_var.id == 106):
                if (ClueEnums.isRoom(self.info.storeAllPlayers[self.myNumber].location)):
                    # According to the project description, one suggestion per turn
                    if (Actions.SUGGEST not in self.actionList and not self.lost and not self.suggested):
                        self.actionList.append(Actions.SUGGEST)
                    elif (Actions.SUGGEST in self.actionList and self.lost):
                        self.actionList.remove(Actions.SUGGEST)
                else:
                    if Actions.SUGGEST in self.actionList:
                        self.actionList.remove(Actions.SUGGEST)

                if (len(self.actionList) == 0 or Actions.MOVE not in self.actionList):
                    self.actionList.append(Actions.ENDTURN)

                self.request_queue.put(ActionRequest(self.actionList))
                action = self.getGUIResponse()
                self.actionList.remove(action)
                msg = self.handleAction(action)
                writer.write(msg)

            # Suggestion response message (somebody, maybe this client, made a suggestion
            # and now the server is broadcasting to all clients what the suggestion was and
            # if it was correct)
            elif(data_var.id == 201):
                suggestion_text = data_var.data.name + " suggested that it was "
                suggestion_text += data_var.data.suggestion["player"].text
                suggestion_text += " in the " + data_var.data.suggestion["location"].text
                suggestion_text += " with the " + data_var.data.suggestion["weapon"].text + "!"
                self.request_queue.put(MessageRequest(suggestion_text, BLACK))
                disproven_text = data_var.data.name + " was "
                if data_var.data.disprov_card is None:
                    disproven_text += "not "
                disproven_text += "disproven."
                self.request_queue.put(MessageRequest(disproven_text, BLACK))
                # If this client made the suggestion, then this player gets to see which card
                # and which player disproved it (if any)
                if data_var.data.disprov_card is not None and data_var.data.playerNum == self.myNumber:
                    disproven_text = data_var.data.disprov_player.name + " disproved your suggestion with the "
                    disproven_text += data_var.data.disprov_card.text + " card."
                    self.request_queue.put(MessageRequest(disproven_text, BLACK))

            # Game lost message (somebody, maybe this client, made an incorrect accusation
            # and now the server is broadcasting to all clients what the accusation was
            # and that it was incorrect)
            elif(data_var.id == 6666):
                if data_var.data.name == player.name:
                    pygame.mixer.Sound.play(self.lost_sound)
                accusation_text = data_var.data.name + " accused "
                accusation_text += data_var.data.accusation["player"].text
                accusation_text += " in the " + data_var.data.accusation["location"].text
                accusation_text += " with the " + data_var.data.accusation["weapon"].text + "!"
                self.request_queue.put(MessageRequest(accusation_text, BLACK))
                lost_text = data_var.data.name + " lost the game!"
                self.request_queue.put(MessageRequest(lost_text, BLACK))
                # If this client made the accusation, then set the lost flag to True
                if data_var.data.playerNum == self.myNumber:
                    self.lost = True

            # Game lost all message (every client has made an incorrect accusation and now
            # the server is broadcasting to all clients that the game is over)
            elif(data_var.id == 6667):
                pygame.mixer.Sound.play(self.lost_sound)
                lost_text = "Everybody has made an incorrect accusation - nobody wins!"
                self.request_queue.put(MessageRequest(lost_text, RED))
                case_file_text = "You should have guessed that is was "
                case_file_text += data_var.data.caseFile["player"].text + " in the "
                case_file_text += data_var.data.caseFile["location"].text + " with the "
                case_file_text += data_var.data.caseFile["weapon"].text + "!"
                self.request_queue.put(MessageRequest(case_file_text, RED))

                # Give players time to see the lost message and then quit the game
                time.sleep(5)
                self.request_queue.put(GUIQuitRequest())
                self.running = False

            # Game won message (somebody, maybe this client, made a correct accusation and
            # now the server is broadcasting to all clients what the accusation was and
            # that it was correct and ended the game
            elif(data_var.id == 7777):
                if data_var.data.name == player.name:
                    pygame.mixer.Sound.play(self.won_sound)
                won_message = data_var.data.name + " won!"
                self.request_queue.put(MessageRequest(won_message, GREEN))
                accusation_text = "It was " + data_var.data.accusation["player"].text
                accusation_text += " in the " + data_var.data.accusation["location"].text
                accusation_text += " with the " + data_var.data.accusation["weapon"].text + "!"
                self.request_queue.put(MessageRequest(accusation_text, GREEN))

                # Give players time to see the won message and then quit the game
                time.sleep(5)
                self.request_queue.put(GUIQuitRequest())
                self.running = False

            else:
                pass

        # Close server connection
        writer.close()
        await writer.wait_closed()

    def getGUIResponse(self):
        response = None
        while response is None:
            self.response_lock.acquire()
            try:
                response = self.response
                if response is not None:
                    self.response = None
            finally:
                self.response_lock.release()
        return response
    
    # Handle any player action and return the response message to be sent back to the
    # server
    def handleAction(self, action):
        # Handle a move action
        if action == Actions.MOVE:
            pygame.mixer.Sound.play(self.move_sound)
            player = self.info.storeAllPlayers[self.myNumber]
            self.request_queue.put(MoveRequest(self.validMoves))
            move = self.getGUIResponse()
            if ClueEnums.isRoom(move) is True:
                self.suggested = False
            player.location = move
            data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgMovePlayer(player)))
            return data_string
        # Handle a suggest action
        elif action == Actions.SUGGEST:
            pygame.mixer.Sound.play(self.suggest_sound)
            self.suggested = True
            location = self.info.storeAllPlayers[self.myNumber].location
            self.request_queue.put(SuggestionRequest(location))
            suggestion = self.getGUIResponse()
            data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgSuggest(suggestion)))
            return data_string
        # Handle an accuse action
        elif action == Actions.ACCUSE:
            pygame.mixer.Sound.play(self.accuse_sound)
            self.request_queue.put(AccusationRequest())
            accusation = self.getGUIResponse()
            data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgAccuse(accusation)))
            return data_string
        # Handle an end turn action
        else:
            self.request_queue.put(MessageRequest("Your turn has ended.", RED))
            data_string = pickle.dumps(wrap.HeaderNew(wrap.MsgEndTurn()))
            return data_string

        
    # method to connect the client to the server.
    async def runClient(self,host,port):
        self.running = True
        reader, writer = await asyncio.open_connection(
            host,port
        )
        await self.handle_server(reader, writer)

    def run(self):
        asyncio.run(self.runClient("73.243.41.224", 87))