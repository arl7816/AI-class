class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList():
    head = None
    size = 0

    def insert(self, data):
        self.size += 1
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        else:
            new_node.next = self.head
            self.head = new_node

    def get(self, index: int) -> object:
        current = self.head
        i = 0
        while i != index:
            current = current.next
            i += 1
        return current.data
