# generate a tree with depth 2 that figures out 

from Structs import DTree
from AdaBoost import AdaBoost
from DTreeInterface import print2D, inOrder
from DataManager import DataManager
from Manager import Manager
import sys

def train(examples: str, output: str, learningType):
    data = DataManager().getContent(examples)

    tree = None
    if learningType == "dt":
        tree = DTree(data, "en", "nl", None)
    elif learningType == "ada":
        tree = AdaBoost(data, 50, "en", "nl")
    
    Manager.save(tree, output)

def predict(hypoth: str, inputs: str) -> None:
    tree = Manager.restore(hypoth)

    for line in DataManager().getContent(inputs):
        print(tree.answer(line.split()[:-1]))

def main() -> None:
    data = DataManager().getContent("Lab3/data.txt")

    tree = DTree(data[:4200], "en", "nl", None)
    boosted = AdaBoost(data[:4200], 25, "en", "nl")

    print("Training Error DTree:", tree.test(data[:4200]), "%")
    print("Testing Error Dtree:", tree.test(data[4200:]), "%")

    print("Training AdaBoost:", boosted.test(data[:4200]), "%")
    print("Testing AdaBoost:", boosted.test(data[4200:]), "%")

    #print2D(tree.root)

    # Manager.save(tree, "tree")
    # tree2 = Manager.restore("tree")

    # print("seri", tree2.test(data[4200:]), "%")

    
    # if sys.argv[1] == "train":
    #     # examples, output file, learning type
    #     train(sys.argv[2], sys.argv[3], sys.argv[4])

    # elif sys.argv[1] == "predict":
    #     # tree file, inputs
    #     predict(sys.argv[2], sys.argv[3])

    return

if __name__ == "__main__":
    main()