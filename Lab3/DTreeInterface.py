from abc import ABC, abstractmethod
from DataManager import DataManager

COUNT = [10]

def print2DUtil(root, space):
 
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

def print2D(root):
    
    # space=[0]
    # Pass initial space count as 0
    print2DUtil(root, 0)

def inOrder(root):
    if root.no is not None: inOrder(root.no)
    print(root.value)
    if root.yes is not None: inOrder(root.yes)

class Example:
    def __init__(self, inputs: list[str], weight = 1) -> None:
        self.inputs = inputs[:-1]
        self.classification = inputs[-1]
        self.weight = weight

class Node:
    def __init__(self, value: int, no = None, yes = None, isResponse = False):
        self.value = value
        self.no = no
        self.yes = yes
        self.isResponse = isResponse

class DTreeCore(ABC):
    def __init__(self, positive: str, negative: str) -> None:
        self.positive = positive
        self.negative = negative
        pass
    
    @abstractmethod
    def answer(self, input: list[str]) -> any:
        pass

    def getPos(self) -> any: return self.positive
    def getNeg(self) -> any: return self.negative

    def test(self, examples: list[list[str]]) -> float:
        n = len(examples)
        correct = 0

        for example in examples:
            example = example.split()
            if self.answer(example[:-1]) == example[-1]:
                correct += 1
        
        return 100 - (correct / n * 100)
    
    def testAnswer(self, example: list[str]) -> bool:
        expected = example[-1]
        return self.answer(example[:-1]) == expected
    