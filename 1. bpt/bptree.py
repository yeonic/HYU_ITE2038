from source.bpt.tree import BpTree

# entry point of the project
if __name__ == '__main__':
    tree = BpTree(4)
    tree.insert(2, 1000)
    tree.insert(3, 100)
    tree.insert(67, 100)
    tree.insert(33, 100)
    tree.insert(31, 100)
    tree.insert(39, 100)
    tree.insert(73, 100)
    tree.insert(83, 100)
    tree.insert(23, 100)
    print()
