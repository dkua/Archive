from __future__ import with_statement
import random
import player
import board
import ship
import sys


def cont():
    """NoneType -> str
    Allows 'Press Enter to continue.' functionality."""

    try:
        input = raw_input()
    except Exception:
        pass


def rand_coord(n):
    """(int) -> tuple
    Returns a random tuple of n - 1 range."""

    x = random.randint(0, n - 1)
    y = random.randint(0, n - 1)
    return x, y


def rand_dir():
    """NoneType -> str
    Returns a random direction as a string."""

    return random.choice(["U", "D", "L", "R"])


def print_file(f, anykey):
    """NoneType -> str
    Prints each line of the selected file. If anykey is True, user presses \
            Enter to move on."""

    print ""
    with open(f) as f:
        for line in f:
            sys.stdout.write(line)
            if anykey is True:
                cont()
                continue
    print "\n"


def quit():
    """Exits program."""

    question = "\nAre you sure you want to exit?\n 1. Yes \n 2. No \n"
    choice = valid(question, 1, 2)
    if choice is 1:
        print "\nThanks for playing! Goodbye!\n"
        sys.exit()
    else:
        pass


def valid(question, first, last):
    """Returns choice if input is valid."""

    while 1:
        try:
            choice = input(question)
            if choice < first or choice > last or not isinstance(choice, int):
                print "\nInvalid input, please try again."
            else:
                return choice
        except Exception:
            print "\nInvalid input, please try again."


def start_menu():
    """Set up the game settings."""

    # Print main menu.
    print "-" * 8 + "Main Menu" + "-" * 8
    print "1. Start Game"
    print "2. Instructions"
    print "3. Credits"
    print "4. Extensions"
    print "5. Quit"
    choice = valid("\nWhat would you like to do? ", 1, 5)

    if choice == 1:  # Choose game settings.

        # Setup the game.
        print "\n" + "-" * 8 + "Select Game Type" + "-" * 8
        print "1. Quick Game"
        print "2. Manual"
        game_type = valid("\nSelect your game type: ", 1, 2)

        if game_type == 1:
            size = 10
        elif game_type == 2:
            size = valid("\nSelect a board size from 2 to 100000: ", 2, 100000)

        # Select Player 1.
        print "\n" + "-" * 8 + "Select Player" + "-" * 8
        print "1. Human"
        print "2. Computer"
        hero_type = valid("\nSelect player type: ", 1, 2)

        if hero_type == 1:  # Input human player name.
            name1 = raw_input("\nWhat is Player 1's name: ")
            player1 = player.Player(name1, size)
        elif hero_type == 2:  # Select AI type.
            print "\n" + "-" * 8 + "Select AI" + "-" * 8
            print "1. Random"
            print "2. Random+"
            print "3. SmartRandom"
            name1 = valid("\nChoose the AI: ", 1, 3)
            player1 = player.Ai(name1, size)

        # Select Player 2.
        print "\n" + "-" * 8 + "Select Opponent" + "-" * 8
        print "1. Human"
        print "2. Computer"
        opp_type = valid("\nSelect your oppenent: ", 1, 2)

        if opp_type == 1:  # Input human player name.
            name2 = raw_input("\nWhat is Player 2's name: ")
            player2 = player.Player(name2, size)
        elif opp_type == 2:  # Select AI type.
            print "\n" + "-" * 8 + "Select AI" + "-" * 8
            print "1. Random"
            print "2. Random+"
            print "3. SmartRandom"
            name2 = valid("\nChoose the AI: ", 1, 3)
            player2 = player.Ai(name2, size)

        if game_type == 1:  # Basic game with random placement.
            player1.board.random_board(1, 2, 2, 1)
            player2.board.random_board(1, 2, 2, 1)
        elif game_type == 2:
            n = _fleet(size)  # Helper function asks for the size of the fleet.

            # Select type of placement.
            print "\n" + "-" * 8 + "Select Type of Placement" + "-" * 8
            print "1. Random"
            print "2. Manual"
            place = valid("\nChoose placement: ", 1, 2)

            if place == 1 or hero_type == 2:  # Random placement for all.
                player1.board.random_board(n[0], n[1], n[2], n[3])
                player2.board.random_board(n[0], n[1], n[2], n[3])
            elif place == 2:  # Manual placement.
                if opp_type == 2:  # Random placement of computer ships.
                    player2.board.random_board(n[0], n[1], n[2], n[3])
                else:

                    # Ask for manual placement of Player 1"s ships.
                    print "*" * 50
                    print "\n%s, please place your ships.\n" % name1
                    print "*" * 50
                    _place(player1, size, 2, n[0])
                    _place(player1, size, 3, n[1])
                    _place(player1, size, 4, n[2])
                    _place(player1, size, 5, n[3])

                    # Switch players for placement.
                    print "\n%s and %s, please switch." % (name1, name2)
                    print "Press Enter to continue. "
                    cont()

                    # Asks for manual placement of Player 2"s ships.
                    print "*" * 50
                    print "\n%s, please place your ships.\n" % name2
                    print "*" * 50
                    _place(player2, size, 2, n[0])
                    _place(player2, size, 3, n[1])
                    _place(player2, size, 4, n[2])
                    _place(player2, size, 5, n[3])

        run_game(player1, player2)  # Play the game!

    elif choice == 2:  # Read the instructions.
        print_file("./media/instructions.txt", True)
        start_menu()
    elif choice == 3:  # Read the credits.
        print_file("./media/credits.txt", True)
        start_menu()
    elif choice == 4:  # Read about the extensions.
        print_file("extensions.txt", True)
        start_menu()
    elif choice == 5:  # Quit the game.
        quit()
        print ""
        start_menu()


def run_game(p1, p2):
    """The main game loop."""

    turn = 1
    while 1:

        # Player 1's Loop.
        print ""
        print "\nRound %s: %s's turn." % (turn, p1.name)
        print "\n" + "--------%s's Board--------" % p1.name
        p2.board.display(False)
        print "\n" + "--------%s's Board--------" % p2.name
        p1.board.display(True)
        p1.turn(p2)
        if p2.fleet.is_fleet_dead() is True:
            winner = p1.name
            break

        # Player 2's loop.
        print ""
        print "\nRound %s: %s's turn." % (turn, p2.name)
        print "\n" + "--------%s'sBboard--------" % p2.name
        p1.board.display(False)
        print "\n" + "--------%s's Board--------" % p1.name
        p2.board.display(True)
        p2.turn(p1)
        if p1.fleet.is_fleet_dead() is True:
            winner = p2.name
            break

        turn += 1

    print_file("./media/ending.txt", False)
    print "%s is the winner!" % winner


def _fleet(size):
    """Helper function asks user for input and returns a tuple of \
            the number of ships."""

    print "\n" + "-" * 8 + "Select Fleet" + "-" * 8
    dests = valid("\nNumber of Destroyers: ", 0, 100000)
    subs = valid("\nNumber of Submarines: ", 0, 100000)
    batts = valid("\nNumber of Battleships: ", 0, 100000)
    carrs = valid("\nNumber of Carriers: ", 0, 100000)
    navy = (dests, subs, batts, carrs)
    fleet_size = dests * 2 + subs * 3 + batts * 4 + carrs * 5

    if fleet_size < 2:
        print "\nSorry, you have too little ships, please try again."
        return fleet(size)
    elif fleet_size <= ((size ** 2) / 2):
        return navy
    else:
        print "\nSorry, you have too many ships, please try again."
        return fleet(size)


def man_coord(size):
    """(int) -> tuple
    Returns co-ordinates that the player is asked to input."""

    print "\n" + "-" * 8 + "Select Co-ordinate" + "-" * 8
    x = valid("\nSelect x co-ordinate: ", 0, size - 1)
    y = valid("\nSelect y co-ordinate: ", 0, size - 1)
    return (x, y)


def man_dir():
    """NoneType -> str
    Returns the direction chosen by the player as a string."""

    print "\n" + "-" * 8 + "Select Direction" + "-" * 8
    print "1. Up"
    print "2. Down"
    print "3. Left"
    print "4. Right"
    choice = valid("\nSelect direction: ", 1, 4)

    if choice == 1:
        direct = "U"
    elif choice == 2:
        direct = "D"
    elif choice == 3:
        direct = "L"
    elif choice == 4:
        direct = "R"
    return direct


def _place(player, size, length, number):
    """Helper functions checks and places the ships where the player \
            chooses if the move is legal."""

    if number == 0:
        return
    name = player.name
    ship = player.board.fleet.name_ship(length)
    print "\n%s, please place your %s. (Length: %s)\n" % (name, ship, length)

    player.board.display(True)

    coord = man_coord(size)
    x = coord[0]
    y = coord[1]
    direct = man_dir()

    if player.board.check(x, y, length, direct) is True:
        name = player.fleet.name_ship(length)
        player.fleet.add_ship(name, x, y, length, direct)
        return _place(player, size, length, number - 1)
    print "\nSorry, that ship won't fit, please try again."
    return _place(player, size, length, number)


if __name__ == "__main__":
    while 1:
        print_file("./media/title.txt", False)
        start_menu()
        break
    print "\nPress Enter to go back to start menu. "
    cont()
    start_menu()
