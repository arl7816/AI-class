from Structs import DTree
from math import log, log1p, sqrt
from copy import deepcopy
from DTreeInterface import DTreeCore, Node, Example, print2D

class Hypothesis:
    def __init__(self, weight, tree: DTree) -> None:
        self.weight = weight
        self.tree = tree

class AdaBoost(DTreeCore):

    def __init__(self, data: list[str], K: int, positive: str, negative: str) -> None:
        super().__init__(positive, negative)
        self.H = self.boost(data, K)

    @staticmethod
    def normalizeArray(lst: list[float]) -> list[float]:
        lst = deepcopy(lst)
        mag = sum(lst)

        for index in range(len(lst)):
            lst[index] /= mag
        return lst

    def answer(self, input: list[str]) -> any:
        z = 0
        for h in self.H:
            z += h.weight * (1 if h.tree.answer(input) == self.positive else -1)

        if z > 0: return self.getPos()
        return self.getNeg()
    
    
    def test(self, examples: list[list[str]]) -> float:
        n = len(examples)
        correct = 0

        for example in examples:
            example = example.split()
            if self.answer(example[:-1]) == example[-1]:
                correct += 1
        
        return 100 - (correct / n * 100)

    def boost(self, data: list[str], K: int) -> list[Hypothesis]:
        startWeight = 1 / len(data)
        exampleWeights = [startWeight for _ in range(len(data))]

        H = []

        for k in range(K):
            #print(exampleWeights)
            h = Hypothesis(startWeight, DTree(data, "en", "nl", 10, exampleWeights))

            #print(k, "generated", print2D(h.tree.root))

            err = 0

            for index, example in enumerate(data):
                if h.tree.testAnswer(example) == False:
                    err += exampleWeights[index]
            deltaW = err / (1 - err)
            for index, example in enumerate(data):
                if h.tree.testAnswer(example) == True:
                    print(k, "is true")
                    exampleWeights[index] *= deltaW
            
            # Normalize the weights
            exampleWeights = AdaBoost.normalizeArray(exampleWeights)

            W = (1 - err) / err
            h.weight = .5 * log1p(W)
            H.append(h)

        #print(exampleWeights)
        
        return H


        