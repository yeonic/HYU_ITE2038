from source.bpt.treeNode import BpNode, NodeContent
from source.bpt.treeConfig import *
from typing import Optional
from queue import Queue

# import sys
# sys.setrecursionlimit(100000)


class BpTree:
    __slots__ = ["root", "order"]

    def __init__(self, m):
        self.root: Optional[BpNode] = None
        self.order = m

    # 1. search methods

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

        return ret_string

    # 2. insertion related method
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
        if not parent.is_full():
            return self.insert_to_non_leaf(split_node_content, parent)

        # case) when the parent full and will overflow
        else:
            non_leaf = self.insert_to_non_leaf(split_node_content, parent)
            non_leaf_split = non_leaf.split_node()
            return self.insert_splitee_to_parent(non_leaf_split, non_leaf.parent)

        # 3. deletion related methods
    def delete(self, key):
        # find
        leaf = self.find_leaf(key)
        res = leaf.search_at_node(key)
        rm_idx = res.index

        # if key doesn't exist -> return root
        if not res.exit_code == KEY_ALREADY_EXISTS:
            print('The key is not found in this tree.')
            return self.root

        # delete at the leaf
        deleted_key = leaf.contents[rm_idx].key
        leaf.contents = leaf.contents[:rm_idx] + leaf.contents[rm_idx+1:]

        # when underflow doesn't occur
        # -> check if root needs to be updated.
        # -> then update parent
        # root update and parent update are exclusive
        if not leaf.now_underflow():
            if not leaf.update_parent(rm_idx, deleted_key):
                return self.update_root(deleted_key, leaf)
            return

        # call function rebalance_tree
        # which contains merging, redistribution operation
        return self.rebalance_tree(deleted_key, leaf)

    def update_root(self, deleted_key, leaf: BpNode):
        idx_tb_updated = self.root.search_key_non_leaf(deleted_key)

        if type(idx_tb_updated) == bool and not idx_tb_updated:
            return False

        self.root.contents[idx_tb_updated].key = leaf.contents[0].key
        return True

    def rebalance_tree(self, deleted_key, current_node: BpNode):
        if current_node is self.root:
            # set self.root as child of the current current_node
            self.root = self.root.contents[0].value
            return

        check_res = current_node.check_siblings(deleted_key)

        if check_res.cmd == BORROW_KEY:
            return self.redistribute_node(current_node, deleted_key, check_res)

        if check_res.cmd == MERGE:
            merge_del_key = self.merge_node(current_node, deleted_key, check_res)

            if current_node.parent.now_underflow():
                return self.rebalance_tree(merge_del_key, current_node.parent)

    def redistribute_node(self, current_node: BpNode, deleted_key: int, check_res: CheckSibDTO):
        sandwiched_parent = current_node.parent.contents[check_res.par_pos]
        len_of_parent = len(current_node.parent.contents)
        if not current_node.is_leaf:
            if check_res.sib_pos == 'l':
                giver = sandwiched_parent.value
                moved_key = giver.contents[len(giver.contents) - 1].key

                # patch node content which l_sibling gave
                new_content = NodeContent(sandwiched_parent.key, giver.r)
                sandwiched_parent.key = moved_key
                current_node.contents = [new_content] + current_node.contents[0:]

                if current_node.r is None:
                    current_node.r = current_node.contents[1].key
                    current_node.contents.pop()

                # update parent
                current_node.contents[0].value.parent = current_node

                giver.r = giver.contents[len(giver.contents) - 1].value

                giver.contents.pop()
            else:
                giver = current_node.parent.contents[check_res.par_pos + 1].value if check_res.par_pos < len_of_parent - 1 else current_node.parent.r
                content_to_be_moved = giver.contents[0]

                current_node.contents[0].key = sandwiched_parent.key
                current_node.r = content_to_be_moved.value

                # update parent
                current_node.r.parent = current_node

                sandwiched_parent.key = content_to_be_moved.key
                giver.contents = giver.contents[1:]
            return

        if check_res.sib_pos == 'l':
            # give the largest content of giver
            giver = sandwiched_parent.value
            content_to_be_moved = giver.contents.pop()

            # update parent
            sandwiched_parent.key = content_to_be_moved.key

            # give the key to sibling
            giver.r.put_content_to_leaf(content_to_be_moved)

        else:
            # give the smallest content of giver
            giver = current_node.parent.contents[check_res.par_pos + 1].value if check_res.par_pos < len_of_parent - 1 else current_node.parent.r
            content_to_be_moved = giver.contents[0]
            giver.contents = giver.contents[1:]

            # update parent
            sandwiched_parent.key = giver.contents[0].key
            sandwiched_parent.value.put_content_to_leaf(content_to_be_moved)

        if not current_node.update_parent(0, deleted_key):
            return self.update_root(deleted_key, current_node)

    def merge_node(self, current_node: BpNode, deleted_key, check_res: CheckSibDTO):
        len_of_parent = len(current_node.parent.contents)
        sandwiched_idx = check_res.par_pos
        sandwiched_parent = current_node.parent.contents[sandwiched_idx]
        deleted_parent_key = sandwiched_parent.key

        # when the merge occurred in non-leaf node
        if not current_node.is_leaf:
            if len_of_parent == 1:
                if check_res.sib_pos == 'r':
                    r_sibling = current_node.parent.r
                    current_node.contents[0].key = sandwiched_parent.key
                    r_sibling.contents[0].value.parent = current_node
                    current_node.contents = current_node.contents + r_sibling.contents
                    current_node.r = r_sibling.r
                    current_node.r.parent = current_node

                    self.update_root(deleted_key, current_node)

                else:
                    l_sibling = current_node.parent.contents[0].value
                    down_content = NodeContent(sandwiched_parent.key, l_sibling.r)

                    l_sibling.contents.append(down_content)

                    if current_node.r is None:
                        l_sibling.r = current_node.contents[0].value
                    else:
                        l_sibling.r = current_node.r
                        l_sibling.contents = l_sibling.contents + current_node.contents
                    l_sibling.r.parent = l_sibling

                current_node.parent.r = None
                current_node.parent.contents[0].key = None

            else:
                if check_res.sib_pos == 'r':
                    r_sibling = current_node.parent.contents[sandwiched_idx + 1].value
                    current_node.contents[0].key = sandwiched_parent.key
                    current_node.contents = current_node.contents + r_sibling.contents
                    current_node.r = r_sibling.r

                    current_node.parent.contents = current_node.parent.contents[1:]
                else:
                    l_sibling = sandwiched_parent.value
                    l_sibling_r = l_sibling.r

                    current_node.contents[0].key = sandwiched_parent.key
                    l_sibling.r = current_node.contents[0].value
                    current_node.contents[0].value = l_sibling_r

                    l_sibling.contents = l_sibling.contents + current_node.contents
                    l_sibling.parent.contents[sandwiched_idx + 1].value = l_sibling

                    l_sibling.parent.contents = l_sibling.parent.contents[:sandwiched_idx] + l_sibling.parent.contents[sandwiched_idx+1:]

        else:
            if check_res.sib_pos == 'r':
                r_sibling = current_node.r

                # merge two nodes
                current_node.contents = current_node.contents + r_sibling.contents
                current_node.r = r_sibling.r

                if len_of_parent == 1:
                    current_node.parent.r = None
                    current_node.parent.contents[0].key = None
                else:
                    current_node.parent.contents[sandwiched_idx + 1].value = current_node
                    current_node.parent.contents = current_node.parent.contents[sandwiched_idx + 1:]
                self.update_root(deleted_key, current_node)

            else:
                l_sibling = sandwiched_parent.value

                # merge two nodes
                l_sibling.contents = l_sibling.contents + current_node.contents
                l_sibling.r = current_node.r

                if len_of_parent == 1:
                    l_sibling.parent.r = None
                    l_sibling.parent.contents[0].key = None
                else:
                    if sandwiched_idx < len_of_parent - 1:
                        current_node.parent.contents[sandwiched_idx + 1].value = l_sibling
                    else:
                        current_node.parent.r = l_sibling

                    current_node.parent.contents = current_node.parent.contents[:sandwiched_idx] + current_node.parent.contents[sandwiched_idx+1:]

                l_sibling.parent = current_node.parent

                if not current_node.update_parent(0, deleted_key):
                    self.update_root(deleted_key, current_node)

        # delete key of sandwiched_parent
        # this key is used to call rebalance tree recursively
        return deleted_parent_key
