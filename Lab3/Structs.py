import numpy as np
from numpy import ndarray
from copy import deepcopy
from math import log
from DTreeInterface import DTreeCore, Node, Example

class DTree(DTreeCore):
    def __init__(self, data: list[str], positive: str, negative: str, maxDepth = 10, exampleWeight = None) -> None:
        super().__init__(positive, negative)
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

    def majority(self, examples: list[Example]) -> Node:
        numPos = 0
        numNeg = 0
        for example in examples:
            if example.classification == self.getPos(): numPos += 1
            if example.classification == self.getNeg(): numNeg += 1
        
        result = Node(self.getPos() if numPos > numNeg else self.getNeg(), isResponse=True)
        return result
    
    @staticmethod
    def information(n): 
        if n == 0: return 1029012901
        return log(1 / n, 2)

    @staticmethod
    def entropy(p) -> float:
        return p * DTree.information(p) + (1 - p) * DTree.information(1 - p)


    def Remainder(self, examples: list[Example], state: str, question: int, p: float, n: float, exampleWeights: list[float]) -> float:
        pk = 0
        nk = 0

        for i, example in enumerate(examples):
            if example.inputs[question] == state:
                if example.classification == self.getNeg():
                    nk += exampleWeights[i]
                else:
                    pk += exampleWeights[i]

        div = pk + nk
        if div == 0:
            div = 1
        return ((pk + nk) / (p + n)) * DTree.entropy(pk / div)

    def importance(self, question: int, examples: list[Example], exampleWeights: list[float]) -> float:
        # gets gain
        gain = 0
        total_weight = sum(exampleWeights)
        n, p = 0, 0

        for i, example in enumerate(examples):
            if example.classification == self.getNeg():
                n += exampleWeights[i]
            else:
                p += exampleWeights[i]

        gain = DTree.entropy(p / total_weight)

        remainder = (p + n) / total_weight * \
                    (self.Remainder(examples, "False", question, p, n, exampleWeights) * 
                     self.Remainder(examples, "True", question, p, n, exampleWeights))

        return gain - remainder

    def maximizeImportance(self, questions: list[int], examples: list[Example], exampleWeights: list[float]) -> int:
        best = [0, -1]
        for question in questions:
            result = self.importance(question, examples, exampleWeights)
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
        
        return node.value


    def DLT(self, examples: list[Example], attributes: list[int], parent_examples: list[Example], 
            maxDepth: int, exampleWeights = None) -> Node:
        if exampleWeights is None: exampleWeights = [1]*len(examples)
        if maxDepth is None: maxDepth = len(attributes)

        # check if all the same classification
        if (DTree.checkAllClassSame(examples)):
            return self.majority(examples)
        
        if len(attributes) == 0:
            return self.majority(examples)

        if (len(examples) == 0):
            return self.majority(parent_examples)
        
        if maxDepth == 0:
            return self.majority(examples)

        # get the question with the most importance
        q = self.maximizeImportance(attributes, examples, exampleWeights)

        # generate node
        tree = Node(q)

        # get all of my no and yes children (ignore the weights)
        noChildren = [example for i, example in enumerate(examples) if example.inputs[q] == "False"]
        noWeights = [weight for i, weight in enumerate(exampleWeights) if examples[i].inputs[q] == "False"]
        yesChildren = [example for i, example in enumerate(examples) if example.inputs[q] == "True"]
        yesWeights = [weight for i, weight in enumerate(exampleWeights) if examples[i].inputs[q] == "True"]


        attributes.remove(q)

        # construct the left and right nodes
        tree.no = self.DLT(noChildren, deepcopy(attributes), examples, maxDepth - 1, noWeights)
        #tree.no = self.DLT()
        tree.yes = self.DLT(yesChildren, deepcopy(attributes), examples, maxDepth - 1, yesWeights)

        return tree

        