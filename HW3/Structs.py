import numpy as np
from numpy import ndarray
from copy import deepcopy
from math import log


def vectorize(lst: list) -> ndarray:
    return np.array(lst)

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

class DTree:
    def __init__(self, data: list[str], maxDepth = 10) -> None:
        self.examples = [Example(dataPoint.split()) for dataPoint in data]
        self.root = self.DLT(self.examples, [i for i in range(len(self.examples[0].inputs))], None, maxDepth)

    @staticmethod
    def checkAllClassSame(examples: list[Example]) -> bool:
        if len(examples) == 0: return True

        check = examples[0].classification
        result = True
        for example in examples: 
            if example.classification != check:
                result = False
                break
        return result

    @staticmethod
    def majority(examples: list[Example]) -> Node:
        numA = 0
        numB = 0
        for example in examples:
            if example.classification == "A": numA += 1
            if example.classification == "B": numB += 1
        
        result = Node("A" if numA > numB else "B", isResponse=True)
        return result
    
    @staticmethod
    def information(n): 
        if n == 0: return 1029012901
        return log(1 / n, 2)

    @staticmethod
    def entropy(p) -> float:
        return p * DTree.information(p) + (1 - p) * DTree.information(1 - p)

    @staticmethod
    def Remainder(examples: list[Example], state: str, question: int, p: int, n: int) -> float:
        pk = 0
        nk = 0

        for example in examples:
            if example.inputs[question] == state:
                if example.classification == "B":
                    nk += 1
                else:
                    pk += 1

        div = pk + nk
        if div == 0: div = 1
        return ((pk + nk) / (p + n)) * DTree.entropy(pk / div)

    @staticmethod
    def importance(question: int, examples: list[Example]) -> float:
        # gets gain
        gain = 0
        n, p = 0,0
        for example in examples:
            if example.classification == "B":
                n += 1
            else:
                p += 1
        
        gain = DTree.entropy(p / (p + n))

        remainder = DTree.Remainder(examples, "False", question, p, n) * DTree.Remainder(examples, "True", question, p, n)

        return gain - remainder
    
    @staticmethod
    def maximizeImportance(questions: list, examples: list[Example]) -> int:
        best = [0, -1]
        for index, question in enumerate(questions):
            result = DTree.importance(question, examples)
            if result > best[1]:
                best[0] = question
                best[1] = result
        return best[0]

    def answer(self, input: list[str], node = None):
        if node is None:
            node = self.root

        if not(node.isResponse):
            if input[node.value] == "False":
                return self.answer(input, node.no)
            if input[node.value] == "True":
                return self.answer(input, node.yes)
        
        #print(node.value)
        
        return node.value

    def testAnswer(self, input: list[str], node = None) -> bool:
        expected = input[-1]
        return self.answer(input[:-1], node) == expected

    def test(self, examples: list[list[str]]) -> float:
        n = len(examples)
        correct = 0

        for example in examples:
            example = example.split()
            if self.answer(example[:-1]) == example[-1]:
                correct += 1
        
        return correct / n * 100

    def DLT(self, examples: list[Example], attributes: list[int], parent_examples: list[Example], maxDepth: int) -> Node:
        # check if all the same classification
        if maxDepth == 0:
            return DTree.majority(examples)

        if (DTree.checkAllClassSame(examples)):
            return DTree.majority(examples)
        
        if len(attributes) == 0:
            return DTree.majority(examples)

        if (len(examples) == 0):
            return DTree.majority(parent_examples)

        # get the question with the most important
        q = DTree.maximizeImportance(attributes, examples)
        tree = Node(q)

        noChildren = deepcopy([_ for _ in filter(lambda ex: ex.inputs[q] == "False", examples)])
        yesChildren = deepcopy([_ for _ in filter(lambda ex: ex.inputs[q] == "True", examples)])
        attributes.remove(q)

        tree.no = self.DLT(noChildren, deepcopy(attributes), examples, maxDepth - 1)
        tree.yes = self.DLT(yesChildren, deepcopy(attributes), examples, maxDepth - 1)

        return tree

        