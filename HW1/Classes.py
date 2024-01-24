class Node:
    def __init__(self, value: object, left_link: object, right_link) -> None:
        self.value = value
        self.right_link = right_link
        self.left_link = left_link
        return
    
    def set_right_link(self, link: object) -> None:
        self.right_link = link
        return
    
    def set_left_link(self, link: object) -> None:
        self.left_link = link
        return
    
    def get_right_link(self) -> object:
        return self.right_link
    
    def get_left_link(self) -> object:
        return self.left_link

    def get_value(self) -> object:
        return self.value

class LinkedList:
    def __init__(self) -> None:
        self.size = 0
        self.root = None

    def add(self, value: object) -> None:
        self.size += 1
        if self.size == 1:
            self.root = Node(value, None, None)
            return
        
        self.root = Node(value, None, self.root)

    def print_list(self) -> None:
        statement = ""
        current = self.root
        while current is not None:
            statement += current.get_value()
            current = current.get_right_link()
            if current is not None: statement += " -> "
        print(statement)
    


class Queue:
    def __init__(self) -> None:
        self.size = 0
        self.start = None
        self.end = None

    def print_queue(self) -> None:
        current = self.end
        while current is not None:
            print(current.get_value())
            current = current.get_right_link()

    def enqueue(self, value: object) -> None:
        self.size += 1
        if self.size == 1:
            self.start = Node(value, None, None)
            self.end = self.start
            return
        
        self.end = Node(value, None, self.end)
        self.end.get_right_link().set_left_link(self.end)
        return
    
    def dequeue(self) -> object:
        result = self.start.get_value()

        self.size -= 1
        if self.size == 0:
            self.start, self.end = None, None
            return result
    
        self.start = self.start.get_left_link()
        self.start.set_right_link(None)

        return result
    
    def peek(self) -> object:
        return self.start.get_value()
    
    def get_size(self) -> int:
        return self.size