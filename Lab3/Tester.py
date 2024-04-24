# generate a tree with depth 2 that figures out 

from Structs import DTree
from AdaBoost import AdaBoost
from DTreeInterface import print2D, inOrder
from DataManager import DataManager
from matplotlib import pyplot as plt
from Plot import Plotter
from DataPoint import Data

def doPlot(training: list[float], testing: list[float]) -> None:
    plotter = Plotter()

    trainingX = [i for i in range(1, len(training) + 1)]
    testX = [i for i in range(1, len(testing) + 1)]

    trainingData = Data((trainingX, training))
    testingData = Data((testX, testing))

    plotter.plot((1, 1, 1), trainingData, "red", "training", key = "base")
    plotter.plot((1,1,1), testingData, "blue", "test")

    plotter.subplots["base"].grid()
    plotter.subplots["base"].legend()
    plotter.set_labels("base", "Max Depth", "Error %", "DTree testing")

    plotter.show()


    return

def main() -> None:

    data = DataManager().getContent("Lab3/data.txt")

    H = []
    training = []
    test = []
    for i in range(1, len(DataManager.TEMPLATE) + 1):
        tree = DTree(data[:4200], "en", "nl", i)
        H.append(tree)
        training.append(tree.test(data[:4200]))
        test.append(tree.test(data[4200:]))
        print("max depth", i, "complete")

    ada = AdaBoost(data[:4200], 25, "en", "nl")
    print("Training AdaBoost:", ada.test(data[:4200]), "%")
    print("Testing AdaBoost:", ada.test(data[4200:]), "%")

    doPlot(training, test)

    return

if __name__ == "__main__":
    main()