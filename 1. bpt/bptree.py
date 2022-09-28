import sys
from source.bpt.tree import BpTree
from source.fileman.csvman import CsvMan
from source.fileman.datman import DatMan


def check_tree(loaded_tree: BpTree):
    if not loaded_tree:
        print('Tree could not be loaded :O')
        print('Please check your index.dat file. Exit program')
        exit()


# entry point of the project
if __name__ == '__main__':
    command = sys.argv[1]
    dat_file = sys.argv[2]
    dat_manager = DatMan(dat_file)

    # creation
    if command == '-c':
        order = int(sys.argv[3])
        new_tree = BpTree(order)
        dat_manager.write_tree(new_tree)
        print('Tree creation is done.')
        exit()

    # insertion
    elif command == '-i':
        tree = dat_manager.load_tree()
        check_tree(tree)

        input_csv = sys.argv[3]
        csv_manager = CsvMan(input_csv)
        csv_manager.read_input()

        size = csv_manager.num_of_items()
        print('Insertion in progress...')
        while not csv_manager.is_queue_empty():
            progress = float((size-csv_manager.num_of_items())/size) * 100
            print(f'Operation {progress:.2f}% completed...', end='\r')
            key_val = csv_manager.task_queue.get().split(',')
            tree.insert(int(key_val[0]), int(key_val[1]))

        dat_manager.write_tree(tree)
        print('Insertion done!')

    # deletion
    elif command == '-d':
        tree = dat_manager.load_tree()
        check_tree(tree)

        print('Range search in progress...')
        print('Tree is building...')
        delete_csv = sys.argv[3]
        csv_manager = CsvMan(delete_csv)
        csv_manager.read_input()
        print('Completed building tree!\n\nNow searching...')

        print('Deletion in progress...')
        while not csv_manager.is_queue_empty():
            del_key = int(csv_manager.task_queue.get())
            tree.delete(int(del_key))

        dat_manager.write_tree(tree)
        print('Deletion done!')
        exit()

    # single key search
    elif command == '-s':
        key = int(sys.argv[3])
        print('Range search in progress...')
        print('Tree is building...')
        tree: BpTree = dat_manager.load_tree()
        check_tree(tree)
        print('Completed building tree!\n\nNow searching...')

        ret_str = tree.single_key_search(key)
        print(ret_str)
        exit()

    elif command == '-r':
        start_key = int(sys.argv[3])
        end_key = int(sys.argv[4])
        print('Range search in progress...')
        print('Tree is building...')
        tree: BpTree = dat_manager.load_tree()
        check_tree(tree)
        print('Completed building tree!\n\nNow searching...')

        ret_str = tree.range_search(start_key, end_key)
        print(ret_str) if ret_str.__len__() != 0 else print('0 key in the given range :(')

    else:
        print('Invalid command!')





