import unittest
from board import Board


class TestBoard(unittest.TestCase):

    def setUp(self):
        """Set up an empty 10x10 board."""

        self.board = Board(10)

    def tearDown(self):
        """Clean up."""

        self.board = None

    def testRandomBoardNoShips(self):
        """Test making a random board with no ships."""

        self.board.random_board(0, 0, 0, 0)
        self.assertEqual(self.board.board, {}, "Board should be empty not %s."\
                          % (str(self.board.board)))

    def testRandomBoardOneShip(self):
        """Test making a random board with a single ship."""

        self.board.random_board(1, 0, 0, 0)
        self.assertTrue("DEST1" in self.board.board.values(), \
                        "DEST1 should be on the board, not %s."\
                        % (str(self.board.board.values())))
        self.assertEqual(len(self.board.board), 2, \
                         "Board should have 2 co-ord, not %d." \
                         % (len(self.board.board)))

    def testRandomBoardTwoCarrier(self):
        """Test making a random 6x6 board with 2 carriers."""

        self.board = Board(6)
        self.board.random_board(0, 0, 0, 2)
        self.assertTrue("CARR1" in self.board.board.values(), \
                        "CARR1 should be on the board, not %s."\
                        % (str(self.board.board.values())))
        self.assertEqual(len(self.board.board), 10, \
                         "Board should have 5 co-ord, not %d." \
                         % (len(self.board.board)))

    def testRandomMultipleSameShips(self):
        """Test making a random board with multiples of the same ship."""

        self.board.random_board(2, 0, 0, 0)
        self.assertTrue("DEST1" in self.board.board.values(), \
                        "DEST1 should be on the board, not %s."\
                        % (str(self.board.board.values())))
        self.assertTrue("DEST2" in self.board.board.values(), \
                        "DEST2 should be on the board, not %s."\
                        % (str(self.board.board.values())))
        self.assertEqual(len(self.board.board), 4, \
                         "Board should have 4 co-ord, not %d." \
                         % (len(self.board.board)))

    def testRandomDifferentShips(self):
        """Test making a random board with all different types of ships."""

        self.board.random_board(1, 1, 1, 1)
        self.assertTrue("DEST1" in self.board.board.values(), \
                        "DEST1 should be on the board, not %s."\
                        % (str(self.board.board.values())))
        self.assertTrue("SUBM1" in self.board.board.values(), \
                        "DEST2 should be on the board, not %s."\
                        % (str(self.board.board.values())))
        self.assertTrue("BATT1" in self.board.board.values(), \
                        "BATT1 should be on the board, not %s."\
                        % (str(self.board.board.values())))
        self.assertTrue("CARR1" in self.board.board.values(), \
                        "CARR1 should be on the board, not %s."\
                        % (str(self.board.board.values())))
        self.assertEqual(len(self.board.board), 14, \
                         "Board should have 14 different co-ord, not %d." \
                         % (len(self.board.board)))

    def testRandomOnBoard(self):
        """Test making a random board with multiple different types of ship."""

        self.board.random_board(2, 2, 2, 2)
        for coord in self.board.board:
            self.assertTrue(0 <= coord[0] <= 9,\
                            "Coord %s is outside the board." % (str(coord)))
            self.assertTrue(0 <= coord[1] <= 9, \
                            "Co-ord %s is outside the board." % (str(coord)))

    def testCheckValidSpace(self):
        """Test to see if a ship can be placed at an empty cordinate."""

        self.assertTrue(self.board.check(5, 5, 2, "U"), "Co-ord is free, \
        should have returned True.")

    def testCheckFirstCoordOverlap(self):
        """Test a ship starting from another ship, moving to a free space."""

        self.board.board = {(0, 0): "DEST1", (0, 1): "DEST1"}
        self.assertFalse(self.board.check(0, 0, 2, "D"), \
                         "Co-ord is taken, should have returned False.")

    def testCheckSecondCoordOverlap(self):
        """Test a ship start from a free space, moving to an occupied space."""

        self.board.board = {(0, 0): "DEST1", (0, 1): "DEST1"}
        self.assertFalse(self.board.check(1, 1, 2, "U"), \
                         "Co-ord is taken, should have returned False.")

    def testCheckStartOffBoard(self):
        """Test a ship starting off the board, moving onto the board."""

        self.assertFalse(self.board.check(10, 10, 2, "U"), \
                         "Co-ord starts off the board, \
                         should have returned False.")

    def testCheckEndOffBoard(self):
        """Test a ship starting on a free space, moving out of the board."""

        self.assertFalse(self.board.check(9, 9, 2, "R"), \
                         "Co-ord off the board, should have returned False.")


if __name__ == "__main__":
    unittest.main()
