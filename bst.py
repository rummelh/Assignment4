# Name: Hannah Rummel
# OSU Email: rummelh@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 2/27/2023
# Description: bst


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """adds a value to the bst"""
        parent_node = None
        current_node = self._root
        if self._root is None:
            #check to see if tree is empty
            self._root = BSTNode(value)
        else:
            while current_node is not None:
                parent_node = current_node
                if value < current_node.value:
                    current_node = current_node.left
                else:
                    current_node = current_node.right
            if value < parent_node.value:
                parent_node.left = BSTNode(value)
            else:
                parent_node.right = BSTNode(value)


    def remove(self, value: object) -> bool:
        """removes value from BST, returns true if removed"""
        if value == self._root.value and self._root.left == None and self._root.right == None:
            self._root = None
            return True
        current_node = self._root
        previous_node = None
        while current_node is not None:
            if current_node.value == value:
                if current_node.left is None and current_node.right is None:
                    self._remove_no_subtrees(previous_node, current_node)
                    return True
                elif current_node.left is not None and current_node.right is not None:
                    self._remove_two_subtrees(previous_node, current_node)
                    return True
                else:
                    self._remove_one_subtree(previous_node, current_node)
                    return True
            elif value < current_node.value:
                previous_node = current_node
                current_node = current_node.left
            else:
                previous_node = current_node
                current_node = current_node.right
        return False

    # Consider implementing methods that handle different removal scenarios; #
    # you may find that you're able to use some of them in the AVL.          #
    # Remove these comments.                                                 #
    # Remove these method stubs if you decide not to use them.               #
    # Change these methods in any way you'd like.                            #

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """remove node with no subtrees"""
        # remove node that has no subtrees (no left or right nodes)
        if remove_node == self._root:
            self._root = None
            return
        if remove_parent is None:
            self._root =None
            return
        if remove_parent.left == remove_node:
            remove_parent.left = None
        else: remove_parent.right = None



    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """remove node with one subtree and rearranges"""
        # remove node that has a left or right subtree (only)
        if remove_node == self._root:
            if remove_node.left is not None:
                self._root = remove_node.left
            else:
                self._root = remove_node.right
            return
        if remove_node.left is not None:
            add_node = remove_node.left
        else:
            add_node = remove_node.right
        if remove_parent.left == remove_node:
            remove_parent.left = add_node
        else:
            remove_parent.right = add_node

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """removes node with two subtrees and rearranges """
        # remove node that has two subtrees
        # need to find inorder successor and its parent (make a method!)
        right_child = remove_node.right
        current_node = right_child
        inorder_successor_parent = None
        while current_node.left is not None:
            inorder_successor_parent = current_node
            current_node = current_node.left
        inorder_successor = current_node
        inorder_successor_right = inorder_successor.right
        if remove_parent is None:
            self._root = inorder_successor
        elif remove_parent.left == remove_node:
            remove_parent.left = inorder_successor
        else:
            remove_parent.right = inorder_successor
        inorder_successor.left = remove_node.left
        if inorder_successor_right is not None:
            inorder_successor_parent.left = inorder_successor_right
        else:
            remove_node.right = None

    def contains(self, value: object) -> bool:
        """returns true if node is in bst"""
        current_node = self._root
        while current_node is not None:
            if current_node.value == value:
                return True
            elif value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right
        return False
    def inorder_traversal(self) -> Queue:
        """adds inorder traversal to queue"""
        queue = Queue()
        self.traversal_help(self._root, queue)
        return queue
    def traversal_help(self,n, queue):
        """helper method to be able to take a value as an argument and queue"""
        #queue = Queue()
        if n is not None:
            self.traversal_help(n.left, queue)
            queue.enqueue(n.value)
            self.traversal_help(n.right, queue)

    def find_min(self) -> object:
        """finds min value of bst"""
        current_node = self._root
        if current_node is None:
            return None
        while current_node.left is not None:
            current_node = current_node.left
        return current_node.value



    def find_max(self) -> object:
        """finds max value of bst"""
        current_node = self._root
        if current_node is None:
            return None
        while current_node.right is not None:
            current_node = current_node.right
        return current_node.value

    def is_empty(self) -> bool:
        """returns true if bst is empty"""
        if self._root is not None:
            return False
        else:
            return True

    def make_empty(self) -> None:
        """empties bst"""
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
