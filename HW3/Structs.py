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
    def __init__(self, data: list[str], maxDepth = 10, exampleWeight = None) -> None:
        self.examples = [Example(dataPoint.split()) for dataPoint in data]
        self.root = self.DLT(self.examples, [i for i in range(len(self.examples[0].inputs))], None, maxDepth, exampleWeight)

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
    def Remainder(examples: list[Example], state: str, question: int, p: float, n: float, exampleWeights: list[float]) -> float:
        pk = 0
        nk = 0

        for i, example in enumerate(examples):
            if example.inputs[question] == state:
                if example.classification == "B":
                    nk += exampleWeights[i]
                else:
                    pk += exampleWeights[i]

        div = pk + nk
        if div == 0:
            div = 1
        return ((pk + nk) / (p + n)) * DTree.entropy(pk / div)

    @staticmethod
    def importance(question: int, examples: list[Example], exampleWeights: list[float]) -> float:
        # gets gain
        gain = 0
        total_weight = sum(exampleWeights)
        n, p = 0, 0

        for i, example in enumerate(examples):
            if example.classification == "B":
                n += exampleWeights[i]
            else:
                p += exampleWeights[i]

        gain = DTree.entropy(p / total_weight)

        remainder = (p + n) / total_weight * \
                    (DTree.Remainder(examples, "False", question, p, n, exampleWeights) * 
                     DTree.Remainder(examples, "True", question, p, n, exampleWeights))

        return gain - remainder

    @staticmethod
    def maximizeImportance(questions: list[int], examples: list[Example], exampleWeights: list[float]) -> int:
        best = [0, -1]
        for question in questions:
            result = DTree.importance(question, examples, exampleWeights)
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
        
        return 100 - (correct / n * 100)

    def DLT(self, examples: list[Example], attributes: list[int], parent_examples: list[Example], 
            maxDepth: int, exampleWeights = None) -> Node:
        if exampleWeights is None: exampleWeights = [1]*len(examples)

        # check if all the same classification
        if (DTree.checkAllClassSame(examples)):
            return DTree.majority(examples)
        
        if len(attributes) == 0:
            return DTree.majority(examples)

        if (len(examples) == 0):
            return DTree.majority(parent_examples)
        
        if maxDepth == 0:
            return DTree.majority(examples)

        # get the question with the most importance
        q = DTree.maximizeImportance(attributes, examples, exampleWeights)
        tree = Node(q)

        noChildren = [example for i, example in enumerate(examples) if example.inputs[q] == "False"]
        noWeights = [weight for i, weight in enumerate(exampleWeights) if examples[i].inputs[q] == "False"]
        yesChildren = [example for i, example in enumerate(examples) if example.inputs[q] == "True"]
        yesWeights = [weight for i, weight in enumerate(exampleWeights) if examples[i].inputs[q] == "True"]

        attributes.remove(q)

        tree.no = self.DLT(noChildren, deepcopy(attributes), examples, maxDepth - 1, noWeights)
        tree.yes = self.DLT(yesChildren, deepcopy(attributes), examples, maxDepth - 1, yesWeights)

        return tree

        