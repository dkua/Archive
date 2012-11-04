import os
import os.path
from folder import *


def build_tree(d):
    '''str -> tree
    Returns a tree of files and directories in directory d, recursively.'''

    path, name = os.path.split(d)
    size = os.path.getsize(d)

    if os.path.isdir(d):
        node = Folder(name, path)
        node.size = size
        for f in os.listdir(d):
            try:
                subitem = build_tree(os.path.join(d, f))

                if subitem and subitem.size != 0:
                    node.items.append(subitem)
                    node.size += subitem.size
            except:
                continue

    # Sorts files by size in descending order.
        node.items[:] = sorted(node.items, key=lambda item: item.size, \
                reverse=True)
        return node

    elif os.path.isfile(d):
        leaf = File(name, path, size)
        return leaf
