# generate a tree with depth 2 that figures out 

from Structs import DTree
from AdaBoost import AdaBoost
from DTreeInterface import print2D, inOrder
from DataManager import DataManager
from matplotlib import pyplot as plt
from Plot import Plotter
from DataPoint import Data

def doPlot(training: list[float], testing: list[float], 
           trainingAda: list[float], testAda: list[float]) -> None:
    plotter = Plotter()

    trainingX = [i for i in range(1, len(training) + 1)]
    testX = [i for i in range(1, len(testing) + 1)]

    trainingData = Data((trainingX, training))
    testingData = Data((testX, testing))

    trainingAdaData = Data((
        [i * 5 for i in range(len(trainingAda))],
        trainingAda
    ))

    testAdaData = Data((
        [i * 5 for i in range(len(testAda))],
        testAda
    ))

    plotter.plot((1, 2, 1), trainingData, "red", "training", key = "base")
    plotter.plot((1,2,1), testingData, "blue", "test")

    plotter.subplots["base"].grid()
    plotter.subplots["base"].legend()
    plotter.set_labels("base", "Max Depth", "Error %", "DTree testing")

    plotter.plot((1,2,2), trainingAdaData, "red", "training", key = "ada")
    plotter.plot((1,2,2), testAdaData, "blue", "test", key = "ada")
    plotter.set_labels("ada", "K", "Error %", "Adaboosting testing")

    plotter.subplots["ada"].grid()
    plotter.subplots["ada"].legend()

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

    ada = AdaBoost(data[:4200], 50, "en", "nl")
    HAda = []
    trainingAda = []
    testAda = []

    for i in range(0, 105, 5):
        tree = AdaBoost(data[:4200], i, "en", "nl")
        HAda.append(tree)
        trainingAda.append(tree.test(data[:4200]))
        testAda.append(tree.test(data[4200:]))
        print("Ada of K =", i, "complete")

    doPlot(training, test, trainingAda, testAda)

    return

if __name__ == "__main__":
    main()