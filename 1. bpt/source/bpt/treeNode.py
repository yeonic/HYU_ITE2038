from math import ceil
from source.bpt.treeConfig import *
from typing import Optional, List, Union


class NodeContent:
    __slots__ = ["key", "value", "temp_r"]

    def __init__(self, key, value, temp_r=None):
        self.key = key
        self.value: Union[int, BpNode] = value
        self.temp_r: Optional[BpNode] = temp_r

    # utils
    def clean_temp_r(self):
        self.temp_r = None


class BpNode:
    __slots__ = ["max_keys", "parent", "is_leaf", "contents", "r"]

    # if leaf==True:
    #   p: [<key, value>]
    #   r: ref of right sibling
    #
    # if leaf==False:
    #   p: [<key, left_child>]
    #   r: ref of rightmost child
    def __init__(self, order, parent=None, contents=None, r=None, leaf=True):
        self.max_keys = order - 1
        self.parent: Optional[BpNode] = parent
        self.is_leaf = leaf
        self.contents: List[Optional[NodeContent]] = contents or []
        self.r: Optional[BpNode] = r

    # 1. searching related methods

    def search_at_node(self, key: int):
        # returning index is the location to be inserted
        # so in the "delete" method of tree, make index 'index = index - 1'
        # if exit_code is KEY_ALREADY_EXISTS, 'i' is the idx where key == self.contents[i].key

        len_of_contents = len(self.contents)
        i = 0

        while i < len_of_contents and key >= self.contents[i].key:
            if self.is_leaf and key == self.contents[i].key:
                return NodeSearchDTO(KEY_ALREADY_EXISTS, i)
            i += 1

        if self.is_full():
            return NodeSearchDTO(NODE_IS_FULL, i)

        if i == len_of_contents:
            return NodeSearchDTO(SEARCH_SUCCEED_EOC, i)

        return NodeSearchDTO(SEARCH_SUCCEED, i)

    # 2. insertion related methods

    # node split method
    # returns 'NodeContent' not 'BpNode'
    # Connect-to-parent operation needs to be executed in other method
    def split_node(self):
        cutting_point = ceil(len(self.contents) / 2)

        right_child = BpNode(order=self.max_keys + 1, contents=self.contents[cutting_point:], r=self.r)
        left_child = BpNode(order=self.max_keys + 1, contents=self.contents[:cutting_point], r=right_child)

        ret_content = NodeContent(key=None, value=left_child, temp_r=right_child)

        if self.is_leaf:
            ret_content.key = right_child.contents[0].key

        else:
            right_child.is_leaf = False
            left_child.is_leaf = False

            discard_pos = len(left_child.contents) - 1
            last_l_content = left_child.contents[discard_pos]
            ret_content.key = last_l_content.key

            left_child.contents = left_child.contents[:discard_pos]
            left_child.r = last_l_content.value

            for item_l in left_child.contents:
                item_l.value.parent = left_child
            left_child.r.parent = left_child

            for item_r in right_child.contents:
                item_r.value.parent = right_child
            right_child.r.parent = right_child

            ret_content.value = left_child
            ret_content.temp_r = right_child

        return ret_content

    # 3. deletion related methods

    def update_parent(self, rm_idx: int, deleted_key: int):
        # when update is not needed
        if not rm_idx == 0 or self.now_underflow():
            return False

        # when deletion occurred in leftmost child
        if deleted_key < self.parent.contents[0].key:
            return False

        # swap key with newly updated child
        tb_updated = self.parent.search_at_node(deleted_key)
        if not tb_updated.exit_code == KEY_ALREADY_EXISTS:
            return False

        # check if deletion occurred in rightmost child
        # if it did, swap key with r
        if tb_updated.index < len(self.parent.contents):
            nc_tb_updated = self.parent.contents[tb_updated.index]
            nc_tb_updated.key = nc_tb_updated.value.contents[0].key
        else:
            nc_tb_updated = self.parent.contents[tb_updated.index - 1]
            nc_tb_updated.key = self.parent.r.contents[0].key

        return True

    def check_siblings(self, deleted_key: int):
        p_res = self.parent.search_at_node(deleted_key)
        len_of_par = len(self.parent.contents)
        idx = p_res.index

        # if self is leftmost node of self.parent
        if idx == 0:
            sibling = self.parent.r if idx >= len_of_par else self.parent.contents[idx+1].value
            return sibling.one_way_check(sib_pos='r', par_pos=idx)

        # if self is rightmost node of self.parent
        elif idx == len_of_par:
            sibling = self.parent.contents[idx - 1].value

            return sibling.one_way_check(sib_pos='l', par_pos=idx-1)

        # self is somewhere-middle node of self.parent
        else:
            # check left sibling
            sibling = self.parent.contents[idx-1].value
            if sibling.can_borrow():
                return CheckSibDTO(sib_pos='l', cmd=BORROW_KEY, par_pos=idx-1)

            # check right sibling
            sibling = self.parent.r if idx + 1 >= len_of_par else self.parent.contents[idx+1].value
            if sibling.can_borrow():
                return CheckSibDTO(sib_pos='r', cmd=BORROW_KEY, par_pos=idx)

            # if nobody lends key
            return CheckSibDTO(sib_pos='l', cmd=MERGE, par_pos=idx-1)

    # check only left sib or right sib
    def one_way_check(self, sib_pos, par_pos: int):
        if self.can_borrow():
            return CheckSibDTO(sib_pos=sib_pos, cmd=BORROW_KEY, par_pos=par_pos)
        return CheckSibDTO(sib_pos=sib_pos, cmd=MERGE, par_pos=par_pos)

    # 4. utils

    def is_full(self):
        if len(self.contents) >= self.max_keys:
            return True
        return False

    # checks if sibling can lend some key
    # expect to be used inside check_siblings
    def can_borrow(self):
        order = self.max_keys + 1
        if len(self.contents) == ceil(order/2) - 1:
            return False
        return True

    # checks if node underflow now
    # expect to be used after deleting
    def now_underflow(self):
        # non-leaf node with no key
        if self.contents[0] is None:
            return True

        order = self.max_keys + 1
        if len(self.contents) < ceil(order / 2) - 1:
            return True
        return False

    # simply put content to leaf
    # without considering any exception
    def put_content_to_leaf(self, content: NodeContent):
        if not self.is_leaf:
            return

        search_res = self.search_at_node(content.key)

        if search_res.exit_code == SEARCH_SUCCEED_EOC:
            self.contents.append(content)

        if search_res.exit_code == SEARCH_SUCCEED:
            self.contents = self.contents[:search_res.index] + [content] + self.contents[search_res.index:]

