from source.bpt.tree import BpTree
from source.fileman.csvman import CsvMan

# entry point of the project
if __name__ == '__main__':
    tree = BpTree(4)
    csv_manager = CsvMan('./input.csv')
    csv_manager.read_input()

    while not csv_manager.task_queue.empty():
        key_val = csv_manager.task_queue.get().split(',')
        tree.insert(int(key_val[0]), int(key_val[1]))

    tree.delete(29)
    tree.delete(38)
    tree.delete(100)
    tree.delete(40)
    print('a')
