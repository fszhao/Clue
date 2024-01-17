from enum import Enum, IntEnum

class EnumText(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__)
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, text: str):
        self.text = text

class Locations(EnumText):
    STUDY = "study"
    HW1 = "study-hall hallway"
    HALL = "hall"
    HW2 = "hall-lounge hallway"
    LOUNGE = "lounge"
    HW3 = "study-library hallway"
    HW4 = "hall-billiard room hallway"
    HW5 = "lounge-dining room hallway"
    LIBRARY = "library"
    HW6 = "library-billiard room hallway"
    BILLIARD = "billiard room"
    HW7 = "billiard room-dining room hallway"
    DINING = "dining room"
    HW8 = "library-conservatory hallway"
    HW9 = "billiard room-ballroom hallway"
    HW10 = "dining room-kitchen hallway"
    CONSERVATORY = "conservatory"
    HW11 = "conservatory-ballroom hallway"
    BALLROOM = "ballroom"
    HW12 = "ballroom-kitchen hallway"
    KITCHEN = "kitchen"

class Rooms(EnumText):
    STUDY = "study"
    HALL = "hall"
    LOUNGE = "lounge"
    LIBRARY = "library"
    BILLIARD = "billiard room"
    DINING = "dining room"
    CONSERVATORY = "conservatory"
    BALLROOM = "ballroom"
    KITCHEN = "kitchen"

def isRoom(location):
    for room in Rooms:
        if location.text == room.text:
            return True
    return False

def getLocationAsRoom(location):
    for room in Rooms:
        if location.text == room.text:
            return room

class Weapons(EnumText):
    CANDLESTICK = "candlestick"
    REVOLVER = "revolver"
    ROPE = "rope"
    LEADPIPE = "lead pipe"
    KNIFE = "knife"
    WRENCH = "wrench"

class Characters(EnumText):
    MSSCARLET = "Ms. Scarlet"
    REVGREEN = "Rev. Green"
    MRSPEACOCK = "Mrs. Peacock"
    CNLMUSTARD = "Cnl. Mustard"
    MRSWHITE = "Mrs. White"
    PROFPLUM = "Prof. Plum"

class Actions(EnumText):
    MOVE = "move"
    SUGGEST = "suggest"
    ACCUSE = "accuse"
    ENDTURN = "end turn"

class LobbyButtons(Enum):
    NEW = 0
    JOIN = 1
    VOLUP = 2
    VOLDOWN = 3