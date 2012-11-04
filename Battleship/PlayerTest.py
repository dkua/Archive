import unittest
from player import *


class TestPlayer(unittest.TestCase):

    def setUp(self):
        """Set up a new player with an empty board."""

        self.p1 = Player("A", 10)

    def tearDown(self):
        """Clean up."""

        self.p1 = None

    def testFireHit(self):
        """Test fire method and hit a ship."""

        self.p1.board.board = {(0, 0): "DEST1", (0, 1): "DEST1"}
        self.p1.fleet.fleet = {"DEST1": {(0, 0): "DEST1", (0, 1): "DEST1"}}
        self.p1.fire(0, 0)
        self.assertEqual(self.p1.fleet["DEST1"][0, 0], "HIT", "(0,0) \
        should have been HIT instead of %s." % (str(self.p1.board[0, 0])))

    def testFireMiss(self):
        """Test fire method but miss everything."""

        self.p1.board.board = {(0, 0): "DEST1", (0, 1): "DEST1"}
        self.p1.fleet.fleet = {"DEST1": {(0, 0): "DEST1", (0, 1): "DEST1"}}
        self.p1.fire(1, 1)
        self.assertEqual(self.p1.board[1, 1], "MISS", "(0,0) should have \
        been MISS instead of %s." % (str(self.p1.board[1, 1])))

    def testFireSunk(self):
        """Test fire and sink a ship."""

        self.p1.board.board = {(0, 0): "HIT", (0, 1): "DEST1"}
        self.p1.fleet.fleet = {"DEST1": {(0, 0): "HIT", (0, 1): "DEST1"}}
        self.p1.fire(0, 1)
        self.assertEqual(self.p1.fleet["DEST1"][0, 0], "SUNK", "(0,0)\
        should have been SUNK instead of %s." % (str(self.p1.board[0, 0])))
        self.assertEqual(self.p1.fleet["DEST1"][0, 1], "SUNK", "(0,1) \
        should have been SUNK instead of %s." % (str(self.p1.board[0, 1])))

    def testFireInvaludCord(self):
        """Test fire with invalid cord."""

        self.p1.board.board = {(0, 0): "DEST1", (0, 1): "DEST1"}
        self.p1.fleet.fleet = {"DEST1": {(0, 0): "DEST1", (0, 1): "DEST1"}}
        self.p1.fire(10, 10)
        self.assertEqual(self.p1.board.board, {(0, 0): "DEST1", (0, 1): \
                                               "DEST1"}, "Board should be \
                                               unchanged, invalid input. \
                         not %s." % (str(self.p1.board.board)))


if __name__ == "__main__":
    unittest.main()
