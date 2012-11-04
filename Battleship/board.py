import ship
import battleship


class Board(object):
    """Board class a dictionary containing the fleet class dictionary. \
            Contains all ships and misses."""

    def __init__(self, size):
        """Creates an empty map dictionary of n x n size."""

        self.board = {}
        self.size = size
        self.fleet = ship.Fleet(self.board)

    def __str__(self):
        return str(self.board)

    def __repr__(self):
        return str(self.board)

    def __getitem__(self, coord):
        return self.board[coord]

    def __setitem__(self, coord, value):
        self.board[coord] = value
        return self.board[coord]

    def __contains__(self, coord):
        return coord in self.board

    def display(self, show):
        """NoneType -> str
        Prints out the entire board."""

        print "\n+",
        for i in range(self.size):
            print "%6s" % (str(i)),
        for y in range(self.size):
            print ""
            for x in range(self.size):
                if x == 0:
                    print (y),
                if (x, y) in self.board:
                    ship = self.board[x, y]
                    if ship == "MISS":
                        print "%6s" % (ship),
                    elif self.fleet[ship][x, y] == "HIT":
                        print "%6s" % (self.fleet[ship][x, y]),
                    elif self.fleet[ship][x, y] == "SUNK":
                        print "%6s" % (self.fleet[ship][x, y]),
                    elif show == False:
                        print "%6s" % "~~",
                    else:
                        print "%6s" % (ship),
                else:
                    print "%6s" % ("~~"),
        return

    def random_board(self, dest, sub, batt, carr):
        """Randomly places a given fleet of ships."""

        if dest == 0 and sub == 0 and batt == 0 and carr == 0:
            return
        coord = battleship.rand_coord(self.size)
        direct = battleship.rand_dir()
        if dest > 0:
            length = 2
            name = self.fleet.name_ship(length)
            if self.check(coord[0], coord[1], length, direct) is True:
                self.fleet.add_ship(name, coord[0], coord[1], length, direct)
                return self.random_board(dest - 1, sub, batt, carr)
        elif sub > 0:
            length = 3
            name = self.fleet.name_ship(length)
            if self.check(coord[0], coord[1], length, direct) is True:
                self.fleet.add_ship(name, coord[0], coord[1], length, direct)
                return self.random_board(dest, sub - 1, batt, carr)
        elif batt > 0:
            length = 4
            name = self.fleet.name_ship(length)
            if self.check(coord[0], coord[1], length, direct) is True:
                self.fleet.add_ship(name, coord[0], coord[1], length, direct)
                return self.random_board(dest, sub, batt - 1, carr)
        elif carr > 0:
            length = 5
            name = self.fleet.name_ship(length)
            if self.check(coord[0], coord[1], length, direct) is True:
                self.fleet.add_ship(name, coord[0], coord[1], length, direct)
                return self.random_board(dest, sub, batt, carr - 1)
        return self.random_board(dest, sub, batt, carr)

    def check(self, x, y, length, direction):
        """(ints) -> bool
        Returns a boolean depending on whether the spaces are free."""

        if x > self.size - 1 or x < 0 or y > self.size - 1 or y < 0:
            return False
        if length is 0 and (x, y) not in self.board:
            return True
        if (x, y) in self.board:
            return False
        elif direction is "U":
            return self.check(x, y - 1, length - 1, direction)
        elif direction is "D":
            return self.check(x, y + 1, length - 1, direction)
        elif direction is "L":
            return self.check(x - 1, y, length - 1, direction)
        elif direction is "R":
            return self.check(x + 1, y, length - 1, direction)
