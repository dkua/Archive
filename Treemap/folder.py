class Folder(object):
    '''A Folder node in a tree.'''

    def __init__(self, name, path):
        '''(Node, str, str) -> NoneType
        Create a node with name, path, no size, co-ordinates, or children.'''

        self.name = name
        self.path = path
        self.size = None
        self.cord = None
        self.items = []

    def __str__(self):
        s = "Name: " + str(self.name) + "  Path: " + str(self.path) + \
                "  Size: " + str(self.size) + " bytes"
        return s


class File(Folder):
    '''A File leaf of a Folder Tree.'''

    def __init__(self, name, path, size):
        '''(Node, str, str, int) -> NoneType
        Create a node with name, path, size, and no co-ordinates.'''

        super(File, self).__init__(name, path)
        self.size = size

    def __str__(self):
        return super(File, self).__str__()
