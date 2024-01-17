import Player as pl
import ClueEnums
from ClueEnums import Locations

class Information:
    def __init__(self):
        # Intial data to be updated or pulled
        self.storeAllPlayers = []
        self.currentLocation = []
        self.startLocations = [Locations.HW2, Locations.HW11, Locations.HW8, Locations.HW5, Locations.HW12, Locations.HW3]
        self.case_file = {}

    # when a move option occurs this will update the list of current player locations
    def updateCurrentLocation(self,incomingPlayer):
        player = incomingPlayer
        if(self.currentLocation.__len__() != 0):
            for index, pair in enumerate(self.currentLocation):
                if pair[0] == player.name:
                    print((pair[0],player.location))
                    self.currentLocation[index] = (pair[0],player.location)
                    print(self.currentLocation)
                else:
                    self.currentLocation.append((player.name,player.location))
                    print(self.currentLocation.__len__())
        else:
            self.currentLocation.append((player.name,player.location))
            print(self.currentLocation.__len__())

    # getter to get all player locations
    def getCurrentLocations(self):
        return self.currentLocation

    def updatePlayer(self,incomingPlayer):
        self.storeAllPlayers[incomingPlayer.number] = incomingPlayer


    def teleport(self, suggesting_player, suggestion):
        location = self.storeAllPlayers[suggesting_player].location
        suggested_player_char = suggestion["player"]
        for player in self.storeAllPlayers:
            if player.character == suggested_player_char:
                player.location = location

    def checkSuggestion(self, suggesting_player, suggestion):
        self.teleport(suggesting_player, suggestion)
        player_index = (suggesting_player + 1) % len(self.storeAllPlayers)
        suggestion_cards = suggestion.values()
        while player_index != suggesting_player:
            current_player = self.storeAllPlayers[player_index]
            for card in current_player.cards:
                if card in suggestion_cards:
                    return card, current_player
            player_index = (player_index + 1) % len(self.storeAllPlayers)
        return None, None

    def checkAccusation(self, accusation):
        return accusation["player"] == self.case_file["player"] and \
            accusation["weapon"] == self.case_file["weapon"] and \
            accusation["location"] == self.case_file["location"]