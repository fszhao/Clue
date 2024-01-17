from ClueEnums import Locations
import ClueEnums

studyList = [Locations.HW1, Locations.HW3, Locations.KITCHEN]
hall1List = [Locations.STUDY, Locations.HALL]
hallList = [Locations.HW1, Locations.HW2, Locations.HW4]
hall2List = [Locations.HALL, Locations.LOUNGE]
loungeList = [Locations.HW2, Locations.HW5, Locations.CONSERVATORY]

hall3List = [Locations.STUDY, Locations.LIBRARY]
hall4List = [Locations.HALL, Locations.BILLIARD]
hall5List = [Locations.LOUNGE, Locations.DINING]

libraryList = [Locations.HW3, Locations.HW6, Locations.HW8]
hall6List = [Locations.LIBRARY, Locations.BILLIARD]
billiardRoomList = [Locations.HW4, Locations.HW6, Locations.HW7, Locations.HW9]
hall7List = [Locations.BILLIARD, Locations.DINING]
diningRoom = [Locations.HW5, Locations.HW7, Locations.HW10]

hall8List = [Locations.LIBRARY, Locations.CONSERVATORY]
hall9List = [Locations.BILLIARD, Locations.BALLROOM]
hall10List = [Locations.DINING, Locations.KITCHEN]

conservatoryList = [Locations.HW8, Locations.HW11, Locations.LOUNGE]
hall11List = [Locations.CONSERVATORY, Locations.BALLROOM]
ballroomList = [Locations.HW9, Locations.HW11, Locations.HW12]
hall12List = [Locations.BALLROOM, Locations.KITCHEN]
kitchenList = [Locations.HW10, Locations.HW12, Locations.STUDY]

cornerRooms = [Locations.STUDY, Locations.LOUNGE, Locations.CONSERVATORY, Locations.KITCHEN]

MOVEDICT = {
    Locations.HW1:hall1List, Locations.HW2:hall2List, Locations.HW3:hall3List, Locations.HW4:hall4List, Locations.HW5:hall5List, Locations.HW6:hall6List,
    Locations.HW7:hall7List, Locations.HW8:hall8List, Locations.HW9:hall9List, Locations.HW10:hall10List, Locations.HW11:hall11List, Locations.HW12:hall12List,
    Locations.STUDY:studyList, Locations.HALL:hallList, Locations.LOUNGE:loungeList,
    Locations.LIBRARY:libraryList, Locations.BILLIARD:billiardRoomList, Locations.DINING:diningRoom,
    Locations.CONSERVATORY:conservatoryList, Locations.BALLROOM:ballroomList, Locations.KITCHEN:kitchenList
}

def determineValidMoves(player, players):
    valid_moves = MOVEDICT[player.location]
    if ClueEnums.isRoom(player.location):
        for p in players:
            if not ClueEnums.isRoom(p.location) and p.location in valid_moves:
                valid_moves.remove(p.location)
    return valid_moves