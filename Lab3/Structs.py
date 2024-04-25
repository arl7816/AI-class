import numpy as np
from numpy import ndarray
from copy import deepcopy
from math import log
from DTreeInterface import DTreeCore, Node, Example

class DTree(DTreeCore):
    """
    Model for a decision tree
    """

    def __init__(self, data: list[str], positive: str, negative: str, maxDepth = 10, exampleWeight = None, file = "") -> None:
        """constructor

        Args:
            data (list[str]): the data to train on
            positive (str): the pos output
            negative (str): the neg output
            maxDepth (int, optional): the max depth of the tree. Defaults to 10.
            exampleWeight (float, optional): the weights of each data point. Defaults to None.
            file (str, optional): the file the data comes from. Defaults to "".
        """
        super().__init__(positive, negative, file)
        self.examples = [Example(dataPoint.split()) for dataPoint in data]
        self.root = self.DLT(self.examples, [i for i in range(len(self.examples[0].inputs))], None, maxDepth, exampleWeight)

    @staticmethod
    def checkAllClassSame(examples: list[Example]) -> bool:
        """checks if all the examples share the same classifier

        Args:
            examples (list[Example]): the group of examples

        Returns:
            bool: true if they are all classified the same, false otherwise
        """
        if len(examples) == 0: return True

        check = examples[0].classification
        result = True
        for example in examples: 
            if example.classification != check:
                result = False
                break
        return result

    def majority(self, examples: list[Example]) -> Node:
        """
        generates a node based on the majority classification

        Args:
            examples (list[Example]): the group of examples

        Returns:
            Node: the new node
        """
        numPos = 0
        numNeg = 0
        for example in examples:
            if example.classification == self.getPos(): numPos += 1
            if example.classification == self.getNeg(): numNeg += 1
        
        result = Node(self.getPos() if numPos > numNeg else self.getNeg(), isResponse=True)
        return result
    
    @staticmethod
    def information(n: float) -> float:
        """calculates the information

        Args:
            n (float): some real number

        Returns:
            float: the information
        """
        if n == 0: return 1029012901
        return log(1 / n, 2)

    @staticmethod
    def entropy(p: float) -> float:
        """calculates the amount of entropy 

        Args:
            p (float): some real number between 0 and 1 (inclusive)

        Returns:
            float: the amount of entropy
        """
        return p * DTree.information(p) + (1 - p) * DTree.information(1 - p)


    def Remainder(self, examples: list[Example], state: str, question: int, p: float, n: float, exampleWeights: list[float]) -> float:
        """calculates the remainder of a given attribute

        Args:
            examples (list[Example]): the group of examples
            state (str): either "True" or "False"
            question (int): the attribute being asked
            p (float): the number of positive classifications from parent
            n (float): the number of negative classifications from parent
            exampleWeights (list[float]): the weights of each example

        Returns:
            float: the remainder given the attribute
        """
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
        """
        calculates the importance of a attribute

        Args:
            question (int): the attribute being used
            examples (list[Example]): the group of examples 
            exampleWeights (list[float]): the weights of each example

        Returns:
            float: the importance
        """
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
        """ gets the attribute which results in the most importance

        Args:
            questions (list[int]): the allowable attributes
            examples (list[Example]): the examples
            exampleWeights (list[float]): the weight of the examples

        Returns:
            int: the index of the attribute which maximizes importance
        """
        best = [0, -1]
        for question in questions:
            result = self.importance(question, examples, exampleWeights)
            if result > best[1]:
                best[0] = question
                best[1] = result
        return best[0]

    def answer(self, input: list[str], node = None):
        """
        gets a prediction given some input

        Args:
            input (list[str]): the input that is being predicted
            node (Node, optional): the current node. Defaults to None.

        Returns:
            any: either a postive or negative answer
        """
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
        """Trains your Dtree on a set of data

        Args:
            examples (list[Example]): the examples being trained on
            attributes (list[int]): the attributes available
            parent_examples (list[Example]): the parents examples
            maxDepth (int): the max depth allowed
            exampleWeights (list[float], optional): the weights of each example. Defaults to None.

        Returns:
            Node: the root node of your Dtree
        """
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

        