from queue import Queue
from typing import NewType

# this file contains variables
# will be shared inside 'bpt' package

# Consts related to NodeSearchDTO
SEARCH_SUCCEED = -1
SEARCH_SUCCEED_EOC = -1.1
SEARCH_FAILED = -2
KEY_ALREADY_EXISTS = -2.1
NODE_IS_FULL = -2.2
TREE_NOT_EXIST = -2.3

# Consts related to CheckSibDTO
BORROW_KEY = 85
MERGE = 57


# Data Transfer Objects(DTOs)
class NodeSearchDTO:
    __slots__ = ["exit_code", "index"]

    def __init__(self, code, index=None):
        self.exit_code = code
        self.index = index


# member var sib_pos: indicates where the sib locates. can be 'l' or 'r'
# member var par_pos: index of parent node content, between self and sib
class CheckSibDTO:
    __slots__ = ["sib_pos", "cmd", "par_pos"]

    def __init__(self, sib_pos: str, cmd: str, par_pos: int):
        self.sib_pos = sib_pos
        self.cmd = cmd
        self.par_pos = par_pos


# Util functions
def queue_to_str(queue: Queue):
    if queue.empty():
        return ''

    ret_str = str(queue.get())
    while not queue.empty():
        ret_str = ret_str + ',' + str(queue.get())

    ret_str = ret_str + '\n'
    return ret_str
