from source.bpt.treeNode import BpNode, NodeContent
from source.bpt.treeConfig import *
from typing import Optional


class BpTree:
    __slots__ = ["root", "order"]

    def __init__(self, m):
        self.root: Optional[BpNode] = None
        self.order = m

    # find methods
    def find_leaf(self, key):
        current = self.root
        while not current.is_leaf:
            res = current.search_at_node(key)

            if res.index == len(current.contents):
                current = current.r
                continue

            current = current.contents[res.index].value

        return current

    # insertion related methods
    def create_new_tree(self, key, value):
        self.root = BpNode(self.order)
        self.root.contents.append(NodeContent(key, value))

    def insert(self, key, value):
        if self.root is None:
            return self.create_new_tree(key, value)

        leaf = self.find_leaf(key)
        res = leaf.search_at_node(key)

        if res.exit_code == KEY_ALREADY_EXISTS:
            return self.root

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
