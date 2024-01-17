import pygame
import os

from ClueEnums import Characters, Weapons, Rooms

CARD_DIM = (300, 400)
path = os.path.dirname(os.path.realpath(__file__)) + "\\assets\\"
CHARACTER_FILENAMES = ["Red.png", "Green.png", "Blue.png", "Yellow.png", "White.png", "Purple.png"]

def loadandscale(path, w, h):
	img = pygame.image.load(path)
	scaledimg = pygame.transform.scale(img, (w, h))
	return scaledimg

# def initCards(num_players)
# def initCards(player_objects) where player_objects is a list of players that have a player.character attribute
def initCards(n_characters):
    cards = {}

    player_cards = []
    #Players
    for i in range(n_characters):
        character_card = Card(loadandscale(path + CHARACTER_FILENAMES[i], CARD_DIM[0], CARD_DIM[1]), Characters(i))
        cards[Characters(i)] = character_card
        player_cards.append(character_card)

    #Weapons
    Candle = Card(loadandscale(path + 'CandleStick.png', CARD_DIM[0], CARD_DIM[1]), Weapons.CANDLESTICK)
    cards[Weapons.CANDLESTICK] = Candle
    Revolver = Card(loadandscale(path + 'Revolver.png', CARD_DIM[0], CARD_DIM[1]), Weapons.REVOLVER)
    cards[Weapons.REVOLVER] = Revolver
    Ropes = Card(loadandscale(path + 'Ropes.png', CARD_DIM[0], CARD_DIM[1]), Weapons.ROPE)
    cards[Weapons.ROPE] = Ropes
    Lead = Card(loadandscale(path + 'Lead.png', CARD_DIM[0], CARD_DIM[1]), Weapons.LEADPIPE)
    cards[Weapons.LEADPIPE] = Lead
    Knife = Card(loadandscale(path + 'Knife.png', CARD_DIM[0], CARD_DIM[1]), Weapons.KNIFE)
    cards[Weapons.KNIFE] = Knife
    Wrench = Card(loadandscale(path + 'Wrench.png', CARD_DIM[0], CARD_DIM[1]), Weapons.WRENCH)
    cards[Weapons.WRENCH] = Wrench

    #Rooms
    Study = Card(loadandscale(path + 'Study.png', CARD_DIM[0], CARD_DIM[1]), Rooms.STUDY)
    cards[Rooms.STUDY] = Study
    Lounge = Card(loadandscale(path + 'Lounge.png', CARD_DIM[0], CARD_DIM[1]), Rooms.LOUNGE)
    cards[Rooms.LOUNGE] = Lounge
    Ballroom = Card(loadandscale(path + 'Ballroom.png', CARD_DIM[0], CARD_DIM[1]), Rooms.BALLROOM)
    cards[Rooms.BALLROOM] = Ballroom
    Library = Card(loadandscale(path + 'Library.png', CARD_DIM[0], CARD_DIM[1]), Rooms.LIBRARY)
    cards[Rooms.LIBRARY] = Library
    BilliardsRoom = Card(loadandscale(path + 'BilliardsRoom.png', CARD_DIM[0], CARD_DIM[1]), Rooms.BILLIARD)
    cards[Rooms.BILLIARD] = BilliardsRoom
    Hall = Card(loadandscale(path + 'Hall.png', CARD_DIM[0], CARD_DIM[1]), Rooms.HALL)
    cards[Rooms.HALL] = Hall
    DiningRoom = Card(loadandscale(path + 'DiningRoom.png', CARD_DIM[0], CARD_DIM[1]), Rooms.DINING)
    cards[Rooms.DINING] = DiningRoom
    Conservatory = Card(loadandscale(path + 'Conservatory.png', CARD_DIM[0], CARD_DIM[1]), Rooms.CONSERVATORY)
    cards[Rooms.CONSERVATORY] = Conservatory
    Kitchen = Card(loadandscale(path + 'Kitchen.png', CARD_DIM[0], CARD_DIM[1]), Rooms.KITCHEN)
    cards[Rooms.KITCHEN] = Kitchen

    weapon_cards = [Candle, Knife, Ropes, Revolver, Lead, Wrench]
    room_cards = [Study, Lounge, Ballroom, Library, BilliardsRoom, Hall, DiningRoom, Conservatory, Kitchen]

    deck = CardDeck(cards, player_cards, weapon_cards, room_cards)
    return deck

class Card(pygame.Surface):
    def __init__(self, image, card_id):
        pygame.Surface.__init__(self, CARD_DIM)
        self.blit(image, (0, 0))
        self.id = card_id

class CardDeck:
    def __init__(self, card_dict, player_cards, weapon_cards, room_cards):
        self.card_dict = card_dict
        self.player_cards = player_cards
        self.weapon_cards = weapon_cards
        self.room_cards = room_cards