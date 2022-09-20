from source.bpt.treeNode import BpNode, NodeContent
from source.bpt.treeConfig import *
from typing import Optional
from queue import Queue


class BpTree:
    __slots__ = ["root", "order"]

    def __init__(self, m):
        self.root: Optional[BpNode] = None
        self.order = m

    # search methods
    def find_leaf(self, key, queue: Queue = None):
        current = self.root
        while not current.is_leaf:
            res = current.search_at_node(key)

            if res.index == len(current.contents):
                queue and queue.put(current.contents[res.index - 1].key)
                current = current.r
                continue

            queue and queue.put(current.contents[res.index].key)
            current = current.contents[res.index].value

        return current

    def single_key_search(self, key):
        traverse_queue = Queue()
        leaf = self.find_leaf(key, traverse_queue)

        res = leaf.search_at_node(key)
        res_idx = res.index
        if not res.exit_code == KEY_ALREADY_EXISTS:
            leaf = leaf.r
            res_idx = 0
            if not leaf.contents[res_idx].key == key:
                return 'NOT FOUND'

        formatted_str = queue_to_str(traverse_queue)
        formatted_str = formatted_str + str(leaf.contents[res_idx].value)

        return formatted_str

    def range_search(self, start_key, end_key):
        leaf = self.find_leaf(start_key)
        res_idx = leaf.search_at_node(start_key).index
        ret_string = ''

        if res_idx == len(leaf.contents):
            leaf = leaf.r
            res_idx = 0

        while leaf.contents[res_idx].key < end_key:
            ret_string = ret_string + str(leaf.contents[res_idx].key) + ',' + str(leaf.contents[res_idx].value) + '\n'
            res_idx += 1

            if res_idx == len(leaf.contents):
                leaf = leaf.r
                res_idx = 0

        ret_string = ret_string + str(leaf.contents[res_idx].key) + ',' + str(leaf.contents[res_idx].value)

        return ret_string

    # insertion related method
    def create_new_tree(self, key, value):
        self.root = BpNode(self.order)
        self.root.contents.append(NodeContent(key, value))

    def insert(self, key, value):
        if self.root is None:
            return self.create_new_tree(key, value)

        leaf = self.find_leaf(key)
        res = leaf.search_at_node(key)

        if res.exit_code == KEY_ALREADY_EXISTS:
            return print('THE KEY is ALREADY_EXIST')

        if res.exit_code == SEARCH_SUCCEED_EOC:
            leaf.contents.append((NodeContent(key, value)))

        if res.exit_code == SEARCH_SUCCEED:
            leaf.contents = leaf.contents[:res.index] + [NodeContent(key, value)] + leaf.contents[res.index:]

        if res.exit_code == NODE_IS_FULL:
            return self.insert_to_leaf_and_split(leaf, res.index, key, value)

    def insert_to_leaf_and_split(self, leaf: Optional[BpNode], index, key, value):
        leaf.contents = leaf.contents[:index] + [NodeContent(key, value)] + leaf.contents[index:]
        split_node_content: NodeContent = leaf.split_node()

        return self.insert_splitee_to_parent(split_node_content, leaf.parent)

    @staticmethod
    def insert_to_non_leaf(content: NodeContent, non_leaf: BpNode):
        res_idx = non_leaf.search_at_node(content.key).index
        content.temp_r.parent = non_leaf
        content.value.parent = non_leaf

        # case1) content is the rightmost
        if content.key >= non_leaf.contents[len(non_leaf.contents) - 1].key:
            non_leaf.contents.append(content)
            non_leaf.r = content.temp_r

        # case2) content is not the rightmost
        else:
            non_leaf.contents = non_leaf.contents[:res_idx] + [content] + non_leaf.contents[res_idx:]
            non_leaf.contents[res_idx + 1].value = non_leaf.contents[res_idx].temp_r

        # if param content is split content of leaf
        # connect leaf to left sibling's r
        if content.value.is_leaf and res_idx > 0:
            non_leaf.contents[res_idx-1].value.r = non_leaf.contents[res_idx].value

        return non_leaf

    def insert_splitee_to_parent(self, split_node_content, parent: BpNode):
        # case) when the node is root
        if not parent:
            new_root = BpNode(self.order, leaf=False)
            new_root.contents.append(split_node_content)
            new_root.r = split_node_content.temp_r

            split_node_content.temp_r.parent = new_root
            split_node_content.value.parent = new_root

            self.root = new_root
            return

        # case) when the parent isn't full
        if not parent.is_node_full():
            return self.insert_to_non_leaf(split_node_content, parent)

        # case) when the parent full and will overflow
        else:
            non_leaf = self.insert_to_non_leaf(split_node_content, parent)
            non_leaf_split = non_leaf.split_node()
            return self.insert_splitee_to_parent(non_leaf_split, non_leaf.parent)


