class Node:
    """
    A single doubly linked node
    """
    def __init__(self, value: object, left_link: object, right_link) -> None:
        self.value = value
        self.right_link = right_link
        self.left_link = left_link
        return
    
    def set_right_link(self, link: object) -> None:
        """
        sets the right node

        Args:
            link (object): the new pointee
        """
        self.right_link = link
        return
    
    def set_left_link(self, link: object) -> None:
        """
        Sets the left node

        Args:
            link (object): the new pointee
        """
        self.left_link = link
        return
    
    def get_right_link(self) -> object:
        """
        Gets the right link of the node

        Returns:
            object: the right node
        """
        return self.right_link
    
    def get_left_link(self) -> object:
        """
        Gets the left link of the node

        Returns:
            object: the left node
        """
        return self.left_link

    def get_value(self) -> object:
        """Gets the current value of the node

        Returns:
            object: the data value
        """
        return self.value

class LinkedList:
    """
    A linked list data structure
    """
    def __init__(self) -> None:
        self.size = 0
        self.root = None

    def add(self, value: object) -> None:
        """
        Adds a value to the linked list

        Args:
            value (object): the new value
        """
        self.size += 1
        if self.size == 1:
            self.root = Node(value, None, None)
            return
        
        self.root = Node(value, None, self.root)

    def print_list(self) -> None:
        """
        Prints all values in the linked list in the following manner:
        *start -> ... -> end*
        """
        statement = ""
        current = self.root
        while current is not None:
            statement += current.get_value()
            current = current.get_right_link()
            if current is not None: statement += " -> "
        print(statement)
    

class Queue:
    """A queue data structure
    """
    def __init__(self) -> None:
        self.size = 0
        self.start = None
        self.end = None

    def print_queue(self) -> None:
        """Prints the contents of the queue
        """
        current = self.end
        while current is not None:
            print(current.get_value())
            current = current.get_right_link()

    def enqueue(self, value: object) -> None:
        """Places a value at the end of the queue

        Args:
            value (object): the new value
        """
        self.size += 1
        if self.size == 1:
            self.start = Node(value, None, None)
            self.end = self.start
            return
        
        self.end = Node(value, None, self.end)
        self.end.get_right_link().set_left_link(self.end)
        return
    
    def dequeue(self) -> object:
        """removes the element at the start of the queue

        Returns:
            object: the element that was removed
        """
        result = self.start.get_value()

        self.size -= 1
        if self.size == 0:
            self.start, self.end = None, None
            return result
    
        self.start = self.start.get_left_link()
        self.start.set_right_link(None)

        return result
    
    def peek(self) -> object:
        """ gets the value of the element at the start of the queue

        Returns:
            object: the element at the start of the queue
        """
        return self.start.get_value()
    
    def get_size(self) -> int:
        """Gets the number of elements within the queue

        Returns:
            int: the number of elements within the queue
        """
        return self.size