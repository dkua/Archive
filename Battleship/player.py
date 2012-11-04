import board
import ship
import battleship
import random


class Player(object):
    """Player class contains methods for play and move history list."""

    def __init__(self, name, size):

        self.name = name
        self.size = size
        self.board = board.Board(size)
        self.fleet = self.board.fleet
        self.history = []

    def turn(self, opp):
        """Player's turn loop."""

        self.opp = opp
        if isinstance(self, Ai):
            coord = self.move()
        else:
            coord = battleship.man_coord(self.size)
        opp.fire(coord[0], coord[1])

        if isinstance(self, Ai):
            return
        else:
            print "\n%s and %s, please switch." % (self.name, opp.name)
            print "Press Enter to continue. "
            battleship.cont()

    def add_history(self, move):
        """Appends the co-ordinate tuple to history if it was a hit."""

        if len(self.history) > 11:
            del self.history[0]
        self.history.append(move)

    def fire(self, x, y):
        """Returns False if co-ordinate has been attacked previously, returns \
        True if ship is hit, 'SUNK' if ship is sunk, or 'MISS' if co-ordinate \
        is empty."""

        if (x, y) in self.board:
            name = self.board[x, y]
            if name == "MISS":
                print "\nInvalid move, please try again."
                return self.turn(self.opp)
            ship = self.fleet[name]
            if ship[x, y] == "HIT" or ship[x, y] == "SUNK":
                print "\nInvalid move, please try again."
                return self.turn(self.opp)
            else:
                ship[x, y] = "HIT"
                self.add_history((x, y))
                if self.fleet.is_ship_dead(name):
                    print "\n%s has been sunk." % name
                return
        elif (x, y) not in self.board and x < self.size and y < self.size:
            self.board[x, y] = "MISS"
            print "\nMISS"
        else:
            return


class Ai(Player):
    """Ai subclass of Player class. Contains different move algorithms for \
            different Ais."""

    def __init__(self, name, size):
        if name == 1:
            name = "Random"
        elif name == 2:
            name = "Random+"
        elif name == 3:
            name = "SmartRandom"
            self.moves = []
        super(Ai, self).__init__(name, size)

    def turn(self, opp):
        Player.turn(self, opp)

    def fire(self, x, y):
        Player.fire(self, x, y)

    def add_history(self, move):
        Player.add_history(self, move)

    def move(self):
        """Returns a tuple of co-ordinates depending on the type of Ai."""

        if self.name == "Random":
            return battleship.rand_coord(self.size)
        elif self.name == "Random+":
            coord = battleship.rand_coord(self.size)
            if coord in self.opp.board:
                square = self.opp.board[coord]
                if square != "HIT" or square != "SUNK" or square != "MISS":
                    return coord
            return coord
        elif self.name == "SmartRandom":
            if self.opp.history != []:
                x = self.opp.history[-1][0]
                y = self.opp.history[-1][1]
                self.opp.history.pop()
                if self.opp.board[x, y] == "SUNK":
                    self.moves = []
                else:
                    if y + 1 <= self.size - 1:
                        self.moves += [(x, y + 1)]
                    if y - 1 >= 0:
                        self.moves += [(x, y - 1)]
                    if x + 1 <= self.size - 1:
                        self.moves += [(x + 1, y)]
                    if x - 1 >= 0:
                        self.moves += [(x - 1, y)]
            if self.moves == []:
                self.moves += [battleship.rand_coord(self.size)]
            index = random.choice(self.moves)
            coord = self.moves.pop(self.moves.index(index))
            return coord
