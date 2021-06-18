# Test file takes command line.
from game import Tictactoe, Player


def testLocation(n, expected):
    if Tictactoe.locationToIndex(n) != expected:
        print(f"ERROR on testLocation({n}), expected {expected}, got {game.locationToIndex(n)}")

def testWinner(expected):
    game = Tictactoe()
    game.createBoard(n=3)
    if winner != expected:
        print(f"ERROR on testWinner, expected {expected}, got {winner}")



