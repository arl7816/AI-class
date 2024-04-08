from Structs import DTree, Example, Node
from math import log1p, sqrt
from copy import deepcopy

class Hypothesis:

    def __init__(self, weight, tree: DTree) -> None:
        self.weight = weight
        self.tree = tree

class AdaBoost:

    def __init__(self, data: list[str], maxDepth = 10) -> None:
        self.H = self.boost(data, 1000)

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
            z += h.weight * (1 if h.tree.answer(input) == "A" else -1)

        if z > 0: return "A"
        return "B"
    
    def testAnswer(self, example: list[str]) -> bool:
        expected = example[-1]
        return self.answer(example[:-1]) == expected
    
    def test(self, examples: list[list[str]]) -> float:
        n = len(examples)
        correct = 0

        for example in examples:
            example = example.split()
            if self.answer(example[:-1]) == example[-1]:
                correct += 1
        
        return correct / n * 100

    def boost(self, data: list[str], K: int) -> list[Hypothesis]:
        startWeight = 1 / len(data)
        exampleWeights = [startWeight for _ in range(len(data))]

        H = []

        for k in range(K):
            h = Hypothesis(startWeight, DTree(data, 1))

            err = 0.0000001

            for index, example in enumerate(data):
                if h.tree.testAnswer(example) == False:
                    err += exampleWeights[index]
            deltaW = err / (1 - err)
            for index, example in enumerate(data):
                if h.tree.testAnswer(example) == True:
                    exampleWeights[index] *= deltaW
            
            # normalize the weights
            exampleWeights = AdaBoost.normalizeArray(exampleWeights)

            h.weight = .5 * log1p((1 - err) / err)
            H.append(h)
        return H


        