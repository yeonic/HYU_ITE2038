from source.bpt.tree import BpTree
from queue import Queue


class DatMan:
    __slots__ = ["dat_file"]

    def __init__(self, dat_file: str):
        self.dat_file = dat_file

    def load_tree(self):
        insert_queue = Queue()
        try:
            # read .dat and put entities in the insert_queue
            with open(self.dat_file, 'r', newline='') as f:
                for line in f:
                    insert_queue.put(line.rstrip())

            # first line of .dat is single integer, which is order of tree
            # if content of the first line is not integer, it raises ValueError -> return False
            order = int(insert_queue.get())
            loaded_tree = BpTree(order)

            # get items one-by-one from the insert_queue
            # then insert the items into the tree in order of 'order' var above
            while not insert_queue.empty():
                key_val = insert_queue.get().split(',')
                loaded_tree.insert(int(key_val[0]), int(key_val[1]))

            return loaded_tree

        # when we cannot read or find .dat file in the same dir
        except FileNotFoundError:
            return False

        # when the first line of .dat is not single integer
        except ValueError:
            return False

    def write_tree(self, tree: BpTree):
        with open(self.dat_file, 'w', newline='') as f:
            # order of tree is recorded on the first line
            f.write(str(tree.order) + '\n')
            node = tree.root

            if not node:
                return False

            # write leftmost leaf to rightmost leaf
            # like range-searching from the smallest node to the largest node

            # overall tree shape may differ from the initial insertion
            # but we can sure that all the keys from the insertion are saved in the .dat

            # non-traverse
            while not node.is_leaf:
                node = node.contents[0].value

            # leaf-traverse
            # which is similar to range search
            # data is saved in 'key,value'-form
            while node is not None:
                for i in range(0, len(node.contents)):
                    f.write(str(node.contents[i].key) + ',' + str(node.contents[i].value) + '\n')
                node = node.r

        return True
