from source.bpt.tree import BpTree
from queue import Queue


class DatMan:
    __slots__ = ["dat_file"]

    def __init__(self, dat_file: str):
        self.dat_file = dat_file

    def load_tree(self):
        insert_queue = Queue()
        try:
            with open(self.dat_file, 'r', newline='') as f:
                for line in f:
                    insert_queue.put(line.rstrip())

            order = int(insert_queue.get())
            loaded_tree = BpTree(order)

            while not insert_queue.empty():
                key_val = insert_queue.get().split(',')
                loaded_tree.insert(int(key_val[0]), int(key_val[1]))

            return loaded_tree

        except FileNotFoundError:
            return False

    def write_tree(self, tree: BpTree):
        with open(self.dat_file, 'w', newline='') as f:
            f.write(str(tree.order) + '\n')
            node = tree.root

            if not node:
                return

            while not node.is_leaf:
                node = node.contents[0].value

            while node is not None:
                for i in range(0, len(node.contents)):
                    f.write(str(node.contents[i].key) + ',' + str(node.contents[i].value) + '\n')
                node = node.r

        return True
