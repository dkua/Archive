class Fleet(object):
    """Fleet class object, a dictionary containing name of ships, \
            as keys and ship dictionaries as values. Ship dictionary \
            contains co-ordinate tuple as keys and ship \
            status as values."""

    def __init__(self, board):
        self.fleet = {}
        self.board = board

    def __repr__(self):
        return str(self.fleet)

    def __str__(self):
        return str(self.fleet)

    def __getitem__(self, ship):
        """(str) -> str
        Returns the ship in the fleet of the same name."""

        return self.fleet[ship]

    def __setitem__(self, ship, value):
        """(str) -> bool
        Creates a ship value with the key string."""

        self.fleet[ship] = value

    def __contains__(self, ship):
        """(str) -> bool
        Returns True if the ship is in the fleet, False otherwise."""

        return ship in self.fleet

    def is_ship_dead(self, name):
        """NoneType -> bool
        Returns True if the ship has been destroyed, False otherwise."""

        if name not in self.fleet:
            return None
        ship = self.fleet[name]
        for item in ship:
            if ship[item] != "HIT" and ship[item] != "SUNK":
                return False
        for item in ship:
            ship[item] = "SUNK"
        return True

    def is_fleet_dead(self):
        """NoneType -> bool
        Returns True if fleet is destroyed, False otherwise."""

        if self.fleet == {}:
            return None
        for ship in self.fleet:
            if self.is_ship_dead(ship) is False:
                return False
        return True

    def name_ship(self, length):
        """Returns the name of the ship depending on given length."""

        i = 1
        for ship in self.fleet:
            if len(self.fleet[ship]) == length:
                i += 1
        i = str(i)
        if length == 2:
            return "DEST" + i
        elif length == 3:
            return "SUBM" + i
        elif length == 4:
            return "BATT" + i
        elif length == 5:
            return "CARR" + i
        return None

    def add_ship(self, name, x, y, length, direction):
        """Adds a ship with given name on given co-ordinates and direction
        to the fleet."""

        if length == 0:
            return
        if name in self.fleet:
            self.fleet[name][x, y] = name
        elif name not in self.fleet:
            self.fleet[name] = {}
            self.fleet[name][x, y] = name
        self.board[x, y] = self.fleet[name][x, y]
        if direction == "U":
            return self.add_ship(name, x, y - 1, length - 1, direction)
        elif direction == "D":
            return self.add_ship(name, x, y + 1, length - 1, direction)
        elif direction == "L":
            return self.add_ship(name, x - 1, y, length - 1, direction)
        elif direction == "R":
            return self.add_ship(name, x + 1, y, length - 1, direction)
