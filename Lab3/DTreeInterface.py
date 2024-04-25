from abc import ABC, abstractmethod
from DataManager import DataManager

COUNT = [10]

def print2DUtil(root: any, space: int) -> None:
    """
    prints a 2d representation of a tree

    Args:
        root (any): the root node
        space (int): the amount space between each node
    """
    # Base case
    if (root == None):
        return
    
    # Increase distance between levels
    space += COUNT[0]
    
    # Process right child first
    print2DUtil(root.yes, space)
    
    # Print current node after space
    # count
    print()
    for i in range(COUNT[0], space):
        print(end=" ")
    
    if root.isResponse:
        print(root.value)
    else:
        print(DataManager.TEMPLATE[root.value])
    #print(type(root.value))
    
    # Process left child
    print2DUtil(root.no, space)
    
    # Wrapper over print2DUtil()

def print2D(root: any) -> None:
    """prints a 2d representation of a tree

    Args:
        root (any): the root of the tree
    """
    
    # space=[0]
    # Pass initial space count as 0
    print2DUtil(root, 0)

def inOrder(root) -> None:
    """prints the tree in an in order sequence

    Args:
        root (any): the root of the tree
    """
    if root.no is not None: inOrder(root.no)
    print(root.value)
    if root.yes is not None: inOrder(root.yes)

class Example:
    """
    A single example used to train on
    """
    def __init__(self, inputs: list[str], weight = 1) -> None:
        """constructo 

        Args:
            inputs (list[str]): the set of attributes
            weight (int, optional): the weight of this example point. Defaults to 1.
        """
        self.inputs = inputs[:-1]
        self.classification = inputs[-1]
        self.weight = weight

class Node:
    """A node for our Dtrees
    """
    def __init__(self, value: int, no = None, yes = None, isResponse = False):
        """constructor

        Args:
            value (int): the value of the node (leaf nodes can be any type))
            no (any, optional): the left branch. Defaults to None.
            yes (any, optional): the right branch. Defaults to None.
            isResponse (bool, optional): is this a leaf node. Defaults to False.
        """
        self.value = value
        self.no = no
        self.yes = yes
        self.isResponse = isResponse

class DTreeCore(ABC):
    """
    Provides some core implementation for a model
    """
    def __init__(self, positive: str, negative: str, file: str) -> None:
        """constructor

        Args:
            positive (str): the postive output
            negative (str): the negative output
            file (str): the file the model is being trained on
        """
        self.positive = positive
        self.negative = negative
        self.file = file
        pass
    
    @abstractmethod
    def answer(self, input: list[str]) -> any:
        """abstract method which predicts whether some input is either pos or neg

        Args:
            input (list[str]): the set of attributes

        Returns:
            any: either the pos or neg answer
        """
        pass

    def getPos(self) -> any: return self.positive
    def getNeg(self) -> any: return self.negative

    def divide(self, a: float, b : float) -> float:
        """divides two numbers
        if b is 0, than a is divided by a small number

        Args:
            a (float): the numerator
            b (float): the denomenator

        Returns:
            float: the result of the division
        """
        return a / b if b != 0 else a / 0.00001

    def test(self, examples: list[list[str]]) -> float:
        """
        Gets the percent error on a given set of data

        Args:
            examples (list[list[str]]): list of inputs in the form of arrays
            NOTE: the final element of each row must be the answer

        Returns:
            float: the percentage of cases failed
        """
        n = len(examples)
        correct = 0

        for example in examples:
            example = example.split()
            if self.answer(example[:-1]) == example[-1]:
                correct += 1
        
        return 100 - (correct / n * 100)
    
    def testAnswer(self, example: list[str]) -> bool:
        """checks if the answer is correct or not

        Args:
            example (list[str]): the input of attributes along with the answer

        Returns:
            bool: true if the prediction is correct, false otherwise
        """
        expected = example[-1]
        return self.answer(example[:-1]) == expected
    