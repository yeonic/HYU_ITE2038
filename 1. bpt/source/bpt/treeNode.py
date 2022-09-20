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
    __slots__ = ["num_of_keys", "parent", "is_leaf", "contents", "r"]

    # if leaf==True:
    #   p: [<key, value>]
    #   r: ref of right sibling
    #
    # if leaf==False:
    #   p: [<key, left_child>]
    #   r: ref of rightmost child
    def __init__(self, order, parent=None, contents=None, r=None, leaf=True):
        self.num_of_keys = order - 1
        self.parent: Optional[BpNode] = parent
        self.is_leaf = leaf
        self.contents: List[Optional[NodeContent]] = contents or []
        self.r: Optional[BpNode] = r

    # searching related methods
    def search_at_node(self, key: int):
        len_of_contents = len(self.contents)
        i = 0

        while i < len_of_contents and key >= self.contents[i].key:
            if key == self.contents[i].key:
                return NodeSearchDTO(KEY_ALREADY_EXISTS, i)
            i += 1

        if self.is_node_full():
            return NodeSearchDTO(NODE_IS_FULL, i)

        if i == len_of_contents:
            return NodeSearchDTO(SEARCH_SUCCEED_EOC, i)

        return NodeSearchDTO(SEARCH_SUCCEED, i)

    # node split method
    # returns 'NodeContent' not 'BpNode'
    # Connect-to-parent operation needs to be executed in other method
    def split_node(self):
        cutting_point = ceil(len(self.contents) / 2)

        right_child = BpNode(order=self.num_of_keys + 1, contents=self.contents[cutting_point:], r=self.r)
        left_child = BpNode(order=self.num_of_keys + 1, contents=self.contents[:cutting_point], r=right_child)

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

    # utils
    def is_node_full(self):
        if len(self.contents) >= self.num_of_keys:
            return True
        return False
