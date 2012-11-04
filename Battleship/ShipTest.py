import unittest
from ship import Fleet
from board import Board


class TestShip(unittest.TestCase):

    def setUp(self):
        """Set up a premade made fleet object."""

        self.ship = Fleet(Board(10))
        self.ship.fleet = {"DEST1": {(1, 2): "SUNK", (1, 3): "SUNK"}, \
                          "DEST2": {(0, 0): "HIT", (0, 1): "DEST2"}, \
                          "DEST3": {(0, 3): "DEST3", (0, 4): "DEST3"}, \
                          "SUBM1": {(2, 1): "SUBM1", (2, 2): "SUBM1", \
                                     (2, 3): "SUBM1"}}

    def tearDown(self):
        """Clean up."""

        self.ship = None

    def testIsShipDeadNoShip(self):
        """Test if a ship is dead if the ship does not exist."""

        self.assertEqual(self.ship.is_ship_dead("IDONTEXIST"), None, \
                         "IDONTEXIST is not a ship in the fleet.")

    def testIsShipDeadCase1(self):
        """Test if a ship is dead if it has only been hit once."""

        self.assertFalse(self.ship.is_ship_dead("DEST2"), \
                         "DEST2 is dead, not alive.")

    def testIsShipDeadCase2(self):
        """Test if a ship is dead if it has been sunk."""

        self.assertTrue(self.ship.is_ship_dead("DEST1"), \
                        "DEST1 is dead, not alive.")

    def testIsShipDeadCase3(self):
        """Test if a ship is dead if it has not been hit."""

        self.assertFalse(self.ship.is_ship_dead("DEST3"), \
                         "DEST3 is still alive, not dead.")

    def testIsFLeetDeadNoShips(self):
        """Test if the fleet is dead if it has no ships."""

        self.ship.fleet = {}
        self.assertEqual(self.ship.is_fleet_dead(), None, "There are no ships")

    def testIsFleetDeadCase1(self):
        """Test if fleet is dead if one ship has been sunk."""

        self.assertFalse(self.ship.is_fleet_dead(), "Not all ships are dead")

    def testIsFleetDeadCase2(self):
        """Test if fleet is dead if all ship have been sunk."""

        for i in self.ship.fleet:
            for j in self.ship.fleet[i]:
                self.ship.fleet[i][j] = "SUNK"
        self.assertTrue(self.ship.is_fleet_dead(), "All ships should be dead")

    def testIsFleetDeadCase3(self):
        """Test if fleet is dead if only one ship is alive."""

        for i in self.ship.fleet:
            for j in self.ship.fleet[i]:
                self.ship.fleet[i][j] = "SUNK"
        self.ship.fleet["DEST1"][(1, 2)] = "DEST1"
        self.assertFalse(self.ship.is_fleet_dead(),\
                         "DEST1 is still alive")

    def testNameShipFirstShip(self):
        """Test the name of first ship of the kind."""

        name = self.ship.name_ship(5)
        self.assertEqual(self.ship.name_ship(5), "CARR1", \
                         "ship name should be CARR1, not %s." % (str(name)))

    def testNameShipExistingShip(self):
        """Test the name of the second ship of the same kind."""

        name = self.ship.name_ship(2)
        self.assertEqual(name, "DEST4", \
                         "ship name should be DEST4, not %s." % (str(name)))

    def testNameShipNoneExistant(self):
        """Test the name of the ship with a length that does not exist."""

        name = self.ship.name_ship(0)
        self.assertEqual(name, None, \
                         "ship name should return None, not %s." % (str(name)))

    def testAddShipDown(self):
        """Test if the ship is added correctly in Down direction."""

        self.ship.add_ship("DEST4", 3, 3, 2, "D")
        self.assertTrue("DEST4" in self.ship.fleet, \
                        "DEST4 is not in the fleet")
        self.assertTrue((3, 3) in self.ship.fleet["DEST4"], \
                        "(3,3) should be a co-ord of DEST4, not %s." \
                        % (str(self.ship.fleet["DEST4"])))
        self.assertTrue((3, 4) in self.ship.fleet["DEST4"], \
                        "(3,4) should be a co-ord of DEST4, not %s." \
                        % (str(self.ship.board)))

    def testAddShipUp(self):
        """Test if the ship is added correctly in Up direction."""

        self.ship.add_ship("SUBM2", 5, 7, 3, "U")
        self.assertTrue("SUBM2" in self.ship.fleet, \
                        "SUBM2 is not in the fleet")
        self.assertTrue((5, 7) in self.ship.fleet["SUBM2"], \
                        "(5,7) should be a co-ord of SUMB2, not %s." \
                        % (str(self.ship.fleet["SUBM2"])))
        self.assertTrue((5, 6) in self.ship.fleet["SUBM2"], \
                        "(5,6) should be a co-ord of SUMB2, not %s." \
                        % (str(self.ship.fleet["SUBM2"])))
        self.assertTrue((5, 5) in self.ship.fleet["SUBM2"], \
                        "(5,5) should be a co-ord of SUMB2, not %s." \
                        % (str(self.ship.fleet["SUBM2"])))

    def testAddShipLeft(self):
        """ Test if the ship is added correcty in Left direction."""

        self.ship.add_ship("SUBM2", 5, 7, 3, "L")
        self.assertTrue("SUBM2" in self.ship.fleet, \
                        "SUBM2 is not in the fleet")
        self.assertTrue((5, 7) in self.ship.fleet["SUBM2"], \
                        "(5,7) should be a co-ord of SUMB2, not %s." \
                        % (str(self.ship.fleet["SUBM2"])))
        self.assertTrue((4, 7) in self.ship.fleet["SUBM2"], \
                        "(4,7) should be a co-ord of SUMB2, not %s." \
                        % (str(self.ship.fleet["SUBM2"])))
        self.assertTrue((3, 7) in self.ship.fleet["SUBM2"], \
                        "(3,7) should be a co-ord of SUMB2, not %s." \
                        % (str(self.ship.fleet["SUBM2"])))

    def testAddShipRight(self):
        """Test if the ship is added correctly in Right direction."""

        self.ship.add_ship("SUBM2", 5, 7, 3, "R")
        self.assertTrue("SUBM2" in self.ship.fleet, \
                        "SUBM2 is not in the fleet")
        self.assertTrue((5, 7) in self.ship.fleet["SUBM2"], \
                        "(5,7) should be a co-ord of SUMB2, not %s." \
                        % (str(self.ship.fleet["SUBM2"])))
        self.assertTrue((6, 7) in self.ship.fleet["SUBM2"], \
                        "(6,7) should be a co-ord of SUMB2, not %s." \
                        % (str(self.ship.fleet["SUBM2"])))
        self.assertTrue((7, 7) in self.ship.fleet["SUBM2"], \
                        "(7,7) should be a co-ord of SUMB2, not %s." \
                        % (str(self.ship.fleet["SUBM2"])))


if __name__ == "__main__":
    unittest.main()
