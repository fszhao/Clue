import os
import pickle
from Player import Player
import Information as info
import Wrapper as wrap
from socket import *
import asyncio
from ClueEnums import Characters, Rooms, Weapons
import random
import time


class PlayerClient:
    def __init__(self, number, writer):
        self.number = number
        self.writer = writer
        self.name = ''
        self.character = None

    # method to send server any msg type usinga wrapper
    async def sendMsg(self,msg):
        data_string = pickle.dumps(msg)
        self.writer.write(data_string)
        await self.writer.drain()

class Game():
    def __init__(self):
        self.info = info.Information()
        self.active_player = 0
        self.clients = []
        self.lost = 0

    # method called in order to begin the player 
    # turn sequence and starting the game    
    async def start_game(self, client):
        print("game started")
        self.assign_cards_and_case()
        writes = []
        for cl in self.clients:      
            msg = wrap.HeaderNew(wrap.MsgGameStart(cl.character,self.info))
            writes.append(cl.sendMsg(msg))
        #send out msg to all players that game is starting and allow player 1 to move

        await asyncio.gather(*writes)
        
        print("server client number: " + str(client.number))
        if client.number == 0:
            msg = wrap.HeaderNew(wrap.MsgStartTurn())
            print("server->client: " + str(msg))
            await client.sendMsg(msg)

    # Ends current players turn and sends server updated info class
    async def end_turn(self, client):
        player_count = len(self.clients)
        self.active_player = (client.number + 1) % player_count
        next_player = self.clients[self.active_player]
        msg = wrap.HeaderNew(wrap.MsgNextTurn(next_player.name))
        await self.broadcastMsg(msg)
        time.sleep(0.2)
        msg = wrap.HeaderNew(wrap.MsgStartTurn())
        await next_player.sendMsg(msg)

    # method to updated player location for GUI to eventually see and use to
    # move the char then ends the turn
    async def move(self, client, data):
        if client.number == self.active_player:
            print("server: " +str(data.location))
            print("server: " + str(data.name))
            print("length of store players: " + str(len(self.info.storeAllPlayers)))
            self.info.updatePlayer(data)
            
            locations = self.info.getCurrentLocations()
            msg = wrap.HeaderNew(wrap.MsgPassInformation(self.info))
            await self.broadcastMsg(msg)
            print("server:" + str(locations))
            
    def assign_cards_and_case(self):
        character_cards = []
        for i in range(len(self.clients)):
            character_cards.append(Characters(i))
        weapon_cards = [w for w in Weapons]
        room_cards = [r for r in Rooms]
        case_character = random.choice(character_cards)
        character_cards.remove(case_character)
        case_weapon = random.choice(weapon_cards)
        weapon_cards.remove(case_weapon)
        case_room = random.choice(room_cards)
        room_cards.remove(case_room)
        self.info.case_file = {"player" : case_character, "weapon" : case_weapon, "location" : case_room}
        print(self.info.case_file)
        character_cards.extend(weapon_cards)
        character_cards.extend(room_cards)
        for player,client in zip(self.info.storeAllPlayers, self.clients):
            cards = random.sample(character_cards, 3)
            for card in cards:
                character_cards.remove(card)
            player.cards = cards
            client.character.cards = cards

    async def broadcastMsg(self,msg):
        writes = []
        for client in self.clients:      
            writes.append(client.sendMsg(msg))

        await asyncio.gather(*writes)

class Server():

    def __init__(self):
        
        self.running = False
        self.max_players = 6
        self.counter = 0
        self.game = Game()
    
    # this method will create a new player based on connection 
    # anytime someone connects it will create their thread and 
    # set the char with all initial info
    def register_player(self, writer, name):
        player_count = self.counter
        print("Server:The player count is: " + str(player_count))
        if player_count < self.max_players:
            client = PlayerClient(number=player_count, writer=writer)
            self.game.clients.append(client)
            character = Player(name=name, number=client.number, location=self.game.info.startLocations.pop(0), 
                            character=Characters(client.number))
            self.game.info.storeAllPlayers.append(character)
            client.name = name
            client.character = character
            self.counter += 1
            return client, self.game
        else:
            return None

    async def handle_client(self, reader, writer):
        buf = 4096
        data = await reader.read(buf)
        msg = pickle.loads(data)
        print("Server:player name: " + str(msg.data.player.name))
        client, game = self.register_player(writer, msg.data.player.name)
        print("Server:player num: " + str(client.number))
        
        # send player its turn number after intialization.
        msg = wrap.HeaderNew(wrap.MsgPassPlayerNum(client.number,client.character))
        await client.sendMsg(msg)

        # waits to read/ get data from client will then sort the msg wrapper
        # based on msg.id and determine what tasks need to be done
        while self.running and client is not None:
            data = await reader.read(buf)
            msg = pickle.loads(data)
            print("Server recieved " + str(msg.id))
            print("Received message: " + str(msg.data))

            if(msg.id == 1000):
                await game.start_game(client)

            elif(msg.id == 1234):
                print("Normal Message no object message")

            elif(msg.id == 102):
                playerData = msg.data.player
                await game.move(client, playerData)

                # Continue active player's turn
                msg = wrap.HeaderNew(wrap.MsgContinueTurn())
                await client.sendMsg(msg)

            elif(msg.id == 107):
                # suggest stuff
                suggestion = msg.data.suggestion
                disprov_card, disprov_player = self.game.info.checkSuggestion(self.game.active_player, suggestion)
                # Need to broadcast an update
                msg = wrap.HeaderNew(wrap.MsgPassInformation(self.game.info))
                await game.broadcastMsg(msg)
                time.sleep(0.2)
                # Send some response back to the suggesting player
                msg = wrap.HeaderNew(wrap.MsgSuggestResp(disprov_card, disprov_player,self.game.active_player, suggestion, client.character.name))
                await game.broadcastMsg(msg)
                time.sleep(0.2)
                # Continue active player's turn\
                msg = wrap.HeaderNew(wrap.MsgContinueTurn())
                await client.sendMsg(msg)
                
            elif(msg.id == 108):
                # accuse stuff
                accusation = msg.data.accusation
                won = self.game.info.checkAccusation(accusation)
                # Need to broadcast an update
                msg = wrap.HeaderNew(wrap.MsgPassInformation(self.game.info))
                await game.broadcastMsg(msg)
                time.sleep(0.2)
                if won:
                    msg = wrap.HeaderNew(wrap.MsgGameWon(client.character.name, accusation))
                    await game.broadcastMsg(msg)
                else:
                    msg = wrap.HeaderNew(wrap.MsgGameLost(client.character.name,self.game.active_player,accusation))
                    await game.broadcastMsg(msg)
                    time.sleep(0.2)
                    self.game.lost += 1
                    if (self.game.lost == len(self.game.clients)):
                        msg = wrap.HeaderNew(wrap.MsgGameLostAll(self.game.info.case_file))
                        await game.broadcastMsg(msg)

                # Continue active player's turn
                time.sleep(0.2)
                msg = wrap.HeaderNew(wrap.MsgContinueTurn())
                await client.sendMsg(msg)

            elif(msg.id == 109):
                await game.end_turn(client)

            elif(msg.id == 104):
                print("server: " + str(msg.data.player.name))
                client.name = msg.data.player.name
                print("updating PLayer name: " + client.name)
            
            if msg == "exit":
                print("Exiting server...")
                self.running = False

        writer.close()
        await writer.wait_closed()

    # starts server and listens for connection
    async def run(self, host, port):
        self.running = True
        server = await asyncio.start_server(
            self.handle_client, host, port
        )

        async with server:
            await server.serve_forever()

server = Server()
asyncio.run(server.run("0.0.0.0", 87))
