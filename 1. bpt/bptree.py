from source.bpt.tree import BpTree
from source.fileman.csvman import CsvMan

# entry point of the project
if __name__ == '__main__':
    tree = BpTree(7)
    csv_manager = CsvMan('./input.csv')
    csv_manager.read_input()

    while not csv_manager.task_queue.empty():
        key_val = csv_manager.task_queue.get().split(',')
        tree.insert(int(key_val[0]), int(key_val[1]))

    print(tree.__slots__)
    print(tree.single_key_search(200))
    print(tree.range_search(4500, 4600))
