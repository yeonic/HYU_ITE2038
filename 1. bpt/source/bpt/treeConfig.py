from queue import Queue

# this file contains variables
# will be shared inside 'bpt' package

# Consts related to searching inside node
SEARCH_SUCCEED = -1
SEARCH_SUCCEED_EOC = -1.1
SEARCH_FAILED = -2
KEY_ALREADY_EXISTS = -2.1
NODE_IS_FULL = -2.2
TREE_NOT_EXIST = -2.3


# Data Transfer Objects(DTOs)
class NodeSearchDTO:
    __slots__ = ["exit_code", "index"]

    def __init__(self, code, index=None):
        self.exit_code = code
        self.index = index


# Util functions
def queue_to_str(queue: Queue):
    if queue.empty():
        return ''

    ret_str = str(queue.get())
    while not queue.empty():
        ret_str = ret_str + ',' + str(queue.get())

    ret_str = ret_str + '\n'
    return ret_str
