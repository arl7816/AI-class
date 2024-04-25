from Structs import DTree
from math import log, log1p, sqrt
from copy import deepcopy
from DTreeInterface import DTreeCore, Node, Example, print2D

class Hypothesis:
    """
    Class for a given hypothesis
    """
    def __init__(self, weight: float, tree: DTree) -> None:
        """
        Constructor

        Args:
            weight (float): the weight of the hypothesis
            tree (DTree): the Dtree linked to the hypothesis
        """
        self.weight = weight
        self.tree = tree

class AdaBoost(DTreeCore):
    """
    Performs an adaboost on mulitple Dtrees
    """
    def __init__(self, data: list[str], K: int, positive: str, negative: str, file: str) -> None:
        """
        constructor for a given adaboost

        Args:
            data (list[str]): the data used to train on
            K (int): the number of hypothsis to be generated
            positive (str): one of the two outputs
            negative (str): the other output
            file (str): the file used to be trained on. 
        """
        super().__init__(positive, negative, file)
        self.H = self.boost(data, K)

    @staticmethod
    def normalizeArray(lst: list[float]) -> list[float]:
        """
        Normalizes the array such that sum(lst) = 1

        Args:
            lst (list[float]): the array to be normalized

        Returns:
            list[float]: the normalized array
        """
        lst = deepcopy(lst)
        mag = sum(lst)

        for index in range(len(lst)):
            lst[index] /= mag
        return lst

    def answer(self, input: list[str]) -> any:
        """
        gets the predicted value from a singular input

        Args:
            input (list[str]): the input in a array of words

        Returns:
            any: either your postive or negative answer
        """
        z = 0
        for h in self.H:
            z += h.weight * (1 if h.tree.answer(input) == self.positive else -1)

        if z > 0: return self.getNeg()
        return self.getPos()
    
    
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

    def boost(self, data: list[str], K: int) -> list[Hypothesis]:
        """performs the general adaboost algorithm

        Args:
            data (list[str]): the data being trained on
            K (int): the number of hypothsis being trained on 

        Returns:
            list[Hypothesis]: a list of hypothesis. 
        """
        startWeight = 1 / len(data)
        exampleWeights = [startWeight for _ in range(len(data))]

        H = []

        for k in range(K):
            h = Hypothesis(startWeight, DTree(data, "en", "nl", 10, exampleWeights))

            err = 0

            for index, example in enumerate(data):
                if h.tree.testAnswer(example) == False:
                    err += exampleWeights[index]
            deltaW = self.divide(err, 1 - err)
            for index, example in enumerate(data):
                if h.tree.testAnswer(example) == True:
                    print(k, "is true")
                    exampleWeights[index] *= deltaW
            
            # Normalize the weights
            exampleWeights = AdaBoost.normalizeArray(exampleWeights)

            W = self.divide(1 - err, err)
            h.weight = .5 * log1p(W)
            H.append(h)
        
        return H


        