class Node:
    """
    A singular linked node
    """

    def __init__(self, data: object) -> None:
        """Generates a node

        Args:
            data (object): the value of the node
        """
        self.data = data
        self.next = None

class LinkedList():
    """A linked list that contains node of generic types
    """
    head = None
    size = 0

    def insert(self, data: object) -> None:
        """ Inserts an element at the start of the Linked List

        Args:
            data (object): the value being inserted
        """
        self.size += 1
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        else:
            new_node.next = self.head
            self.head = new_node

    def get(self, index: int) -> object:
        """
        Gets an element from the linked list at a specific index

        Args:
            index (int): the index of the element starting at 0

        Returns:
            object: the value of the returned element
        """
        current = self.head
        i = 0
        while i != index:
            current = current.next
            i += 1
        return current.data
