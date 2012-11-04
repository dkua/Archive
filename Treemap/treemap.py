from Tkinter import *
from tree import *
from tile import *
import tkFileDialog
import tkMessageBox as box
import subprocess
import sys
import os


class Menu(Frame):

    def __init__(self, parent):
        '''(Frame, root) -> NoneType
        Create a centred Frame with parent, width, and height.'''

        Frame.__init__(self, parent)
        self.parent = parent
        self.width = self.parent.winfo_screenwidth()
        self.height = self.parent.winfo_screenheight()
        self.centerWindow()

    def centerWindow(self):
        '''Centres the window in the screen.'''

        w = 400
        h = 550
        x = (self.width - w) / 2
        y = (self.height - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def main_menu(self):
        '''Create menu.'''

        # Build Menu Layout
        self.parent.title("CSCA48 A2: Treemaps")
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=1)
        self.pack(fill=BOTH, expand=1)

        # Title
        self.title = Label(frame, text="Assignment 2", font=("Helvetica", 36))
        self.title.pack(side=TOP)
        authors = "David Kua (998484536)" + "\n \n" + "Jason Liw (999058488)"
        self.title = Label(frame, text=authors, font=("Helvetica", 16))
        self.title.pack(side=TOP, pady=10)

        # Select Directory
        self.label = Label(frame, text="Select a directory")
        self.label.pack(side=TOP, pady=10)

        self.folder = StringVar()

        select_button = Button(frame, text="Browse", command=self.get_dir)
        select_button.pack(side=TOP, pady=10)

        # Select Screen Size
        self.label = Label(frame, text="Select a screen width")
        self.label.pack(side=TOP)

        self.w = IntVar()

        width = Scale(frame, from_=0, to=self.width, orient=HORIZONTAL, \
                      length=300, command=self.get_width)
        width.pack(side=TOP, pady=10)

        self.label = Label(frame, text="Select a screen height")
        self.label.pack(side=TOP)

        self.h = IntVar()

        height = Scale(frame, from_=0, to=self.height, orient=HORIZONTAL, \
                       length=300, command=self.get_height)
        height.pack(side=TOP, pady=10)

        # Select Colour
        self.label = Label(frame, text="Uncheck for non-random colours")
        self.label.pack(side=TOP, pady=5)

        self.colour = BooleanVar()

        cb = Checkbutton(frame, text="Random Colour", variable=self.colour)
        cb.select()
        cb.pack(side=TOP)

        # Select Algorithm
        s = "Uncheck to use squarifying tiling algorithm (random color only)"
        self.label = Label(frame, text= s)
        self.label.pack(side=TOP, pady=5)

        self.tile = BooleanVar()

        cb = Checkbutton(frame, text="Basic Tiling", variable=self.tile)
        cb.select()
        cb.pack(side=TOP)

        # Close Button
        close_button = Button(self, text="Close", command=self.quit)
        close_button.pack(side=RIGHT, padx=5, pady=5)

        # Start Button
        start_button = Button(self, text="Start", command=self.start)
        start_button.pack(side=RIGHT)

    def dirError(self):
        box.showerror("Error", "Could not open directory, please try again")

    def get_dir(self):
        dirname = tkFileDialog.askdirectory()  # Opens file broswer.
        if dirname != "":
            self.folder.set(dirname)
        else:
            self.dirError()

    def get_width(self, val):
        self.w.set(val)

    def get_height(self, val):
        self.h.set(val)

    def get_colour(self, val):
        self.colour.set(val)

    def start(self):
        try:
            tree = build_tree(self.folder.get())
            if self.colour.get() == 1:
                colour = True
            else:
                colour = False
            if self.tile.get() == 1:
                alg = True
            else:
                alg = False
        except:
            return self.dirError()
        main_loop(tree, self.w.get(), self.h.get(), colour, alg)


def open_folder(tree, cord):
    '''(tree, (int, int)) -> Folder
    Opens the containing folder of the file at mouseclick.'''

    x, y = cord
    if type(tree) is File:
        if sys.platform.startswith("win"):  # Check if Windows system.
            os.startfile(tree.path)
        elif sys.platform.startswith("darwin"):  # Check if OSX system.
            subprocess.call(["open", "-R", tree.path])
    elif type(tree) is Folder:
        for item in tree.items:
            if item.cord:
                a, b, c, d = item.cord
                # Check if co-ordinates belong to any of the children.
                if x in range(int(a), int(c)) and y in range(int(b), int(d)):
                    open_folder(item, cord)


def blit_text(tree, cord, screen, height):
    '''(tree, (int, int), Surface, int) -> NoneType
    Blits message text and information text of the file the mouse is currently
    hovering over.'''

    x, y = cord
    font = pygame.font.Font(None, 16)
    pos1 = (1, height - font.get_linesize() * 2)
    pos2 = (1, height - font.get_linesize())

    if type(tree) is File:
        line1 = font.render("Click to open folder!", 1, (255, 255, 255))
        line2 = font.render(str(tree), 1, (255, 255, 255))
        screen.blit(line1, pos1)
        screen.blit(line2, pos2)
    elif type(tree) is Folder:
        for item in tree.items:
            if item.cord:
                a, b, c, d = item.cord
                # Check if co-ordinates belong to any of the children.
                if x in range(int(a), int(c)) and y in range(int(b), int(d)):
                    blit_text(item, cord, screen, height)


def main_loop(tree, width, height, colour, alg):
    '''(tree, int, int, bool) -> NoneType
    Runs Pygame and tiles the treemap in window of given width and height.'''

    h = height + 28  # Adds space to bottom of screen for blitted text.
    pygame.init()
    screen = pygame.display.set_mode((width, h))

    # Chooses tiling algorithm.
    if alg is True:
        tile(tree, 0, 0, width, height, screen, colour)  # Build basic treemap.
    else:
        square(tree, width, height, screen)

    screen2 = screen.copy()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:  # Blit file under mouse.
            screen.blit(screen2, (0, 0))
            blit_text(tree, event.pos, screen, h)
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Open file clicked.
            open_folder(tree, event.pos)
        pygame.display.flip()

if __name__ == "__main__":
    root = Tk()
    menu = Menu(root)
    menu.main_menu()
    root.mainloop()
    root.destroy()
