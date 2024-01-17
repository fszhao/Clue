# Basic error to be raised when no valid actions are provided on a player's turn
class NoPossibleActionError(Exception):
    def __init__(self):
        print("No possible actions were provided!")

# Basic error to be raised when too many players are in one location
class RoomOverflowError(Exception):
    def __init__(self):
        print("Too many players in a room!")