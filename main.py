# coding=utf-8

import numpy as np
from pprint import pprint

RAND_MIN = -20
RAND_MAX = 20


MIN_VALUE = -(2**31)
MAX_VALUE = 2**31


class Node:
    """
    Non-leaf nodes of the tree
    """
    name: str
    child_nodes: list

    def __init__(self, name):
        self.name = name
        self.child_nodes = []

class LeafNode(Node):
    """
    Leaf nodes of the tree. Unlike non-leaf nodes, leaf nodes have an eval field.
    """
    eval: int

    def __init__(self, name: str, eval: int):
        super().__init__(name)
        self.eval = eval


def gen_tree(depth: int, is_max: bool, br_factor: int, name: str, leaf_values: []) -> Node:
    """
    Generates a tree
    :param depth: the depth of the tree we are generating
    :param is_max: bool, showing whether the first level is Max or Min
    :param br_factor: the branching factor of the tree
    :param name: the name of the node
    :param leaf_values: a list of leaf values. If None is passed, then the leaf values are generated randomly.
    :return: the root node of the generated tree
    """

    if depth == 0:
        if leaf_values is None:
            # generate a random number if the list leaf_values is not specified
            val = np.random.random_integers(low = RAND_MIN, high = RAND_MAX, size = 1)[0]
        else:
            # take the first value from leaf_values, and then delete it
            val = leaf_values[0]
            del leaf_values[0]
        leaf = LeafNode(name, val)
        return leaf

    # create a node
    node = Node(name)
    for i in range(br_factor):
        child_suffix = chr(ord('a') + i) # this is for naming child-nodes
        if not is_max:
            child_suffix = child_suffix.upper()
        child_name = '{}-{}'.format(name, child_suffix)

        # recursively call the gen_tree on all child-nodes, with decreased depth, and flipped is_max
        child_node = gen_tree(depth-1, not is_max, br_factor, child_name, leaf_values)
        # child_node contains the sub-tree starting at node that node, add it to the list of the child_nodes
        # of the current node
        node.child_nodes.append(child_node)

    return node


def print_tree(root_node, spaces: str):
    """
    Prints the tree
    :param root_node: the root node of the tree
    :param spaces: a string containing spaces, used for formatting.
    :return:
    """
    if type(root_node) is LeafNode:
        print('{}{} eval: {}'.format(spaces, root_node.name, root_node.eval))
    else:
        print('{}{}'.format(spaces, root_node.name))
        for child_node in root_node.child_nodes:
            print_tree(child_node, indent(spaces))


def indent(str):
    return str + ' '*2


def alpha_beta(node, alpha: int, beta: int, is_max: bool, spaces: str, verbose: bool = True):
    """
    Does alpha-beta search on a (sub)-tree. This function does not have depth parameter, because the tree we
        are generating has nodes of type LeafNode at the last level. So we search until we see that the type of the
        node is LeafNode
    :param node: the root of the tree where we are doing the search
    :param alpha:
    :param beta:
    :param is_max: if we are at a maximizing or minimizing node
    :param spaces: this is used for formatting
    :param verbose: boolean, shows whether we print during the search process or not.
    :return:
    """

    if type(node) is LeafNode:
        # terminal nodes, take the evaluation
        if verbose:
            print('{}{} eval: {}'.format(spaces, node.name, node.eval))
        return node.eval

    if verbose:
        print('{spaces}node: {name} α:{alpha} β: {beta} is_max: {is_max}'.format(spaces=spaces, name=node.name,
                                                                              alpha=alpha, beta=beta, is_max=is_max))
    if is_max:
        # we are at a max node, look for a value which improves (increases) alpha
        v = MIN_VALUE
        for ch in node.child_nodes:
            ab = alpha_beta(ch, alpha, beta, False, indent(spaces))
            v = max(v, ab)

            if v > alpha:
                if verbose:
                    print('{spaces}{name} updating α: {alpha} -> {v}'.format(spaces=spaces, name=node.name, alpha=alpha,
                                                                             v=v))
                alpha = v

            if beta <= alpha:
                if verbose:
                    print('{spaces}BETA cut-off: α:{alpha} β: {beta}'.format(spaces=spaces, alpha=alpha, beta=beta))
                # perform  a beta cut-off because what we have found is already too good, our opponent is not going to
                # enter this variation
                break  # alpha cut-off
        if verbose:
            print('{spaces}{name} returning value: {v}'.format(spaces=spaces, name=node.name, v=v))
        return v
    else:
        # we are at a min node, look for a value which improves (decreases) beta
        v = MAX_VALUE
        for ch in node.child_nodes:
            ab = alpha_beta(ch, alpha, beta, True, indent(spaces))
            v = min(ab, v)

            if v < beta:
                if verbose:
                    print('{spaces}{name} updating β: {beta} -> {v}'.format(spaces=spaces, name=node.name, beta=alpha,
                                                                            v=v))
                beta = v

            if beta <= alpha:
                # perform an alpha cut-off because what we have found is already too good, our opponent is not going to
                # enter this variation
                if verbose:
                    print('{spaces}ALPHA cut-off: α:{alpha} β: {beta}'.format(spaces=spaces, alpha=alpha, beta=beta))
                break  # beta cut-off
        if verbose:
            print('{spaces}{name} returning value: {v}'.format(spaces=spaces, name=node.name, v=v))
        return v


def alpha_beta_root(node, is_max=True):
    """
    Use this function to make the root call to alpha-beta
    :param node:
    :param is_max:
    :return:
    """
    return alpha_beta(node, MIN_VALUE, MAX_VALUE, is_max, '')


def main():
    #np.random.seed(79878)
    #T = gen_tree(3, True, 3, 'A')
    T = gen_tree(3, True, 3, 'A', [-17, 4, 15, 15, 8, -14, 16, -1, 5, -16, 2, 0, 7, 19, -13, -8, 2, -17, -7, -8, -6, -8, -15, -7, 15, 8, 8])
    print_tree(T, '')
    print()
    print()
    value = alpha_beta_root(T)
    print()
    print('alpha-beta returned {}'.format(value))

if __name__ == '__main__':
    main()
