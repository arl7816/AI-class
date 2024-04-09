# generate a tree with depth 2 that figures out 

from Structs import DTree
from AdaBoost import AdaBoost
from DTreeInterface import print2D, inOrder
from DataManager import DataManager

def main() -> None:

    data = DataManager().getContent("Lab3/data.txt")

    print(len(data))

    tree = DTree(data[:4200], "en", "nl", 10)
    boosted = AdaBoost(data[:4200], 10, "en", "nl")

    print("Training Error DTree:", tree.test(data[:4200]), "%")
    print("Testing Error Dtree:", tree.test(data[4200:]), "%")

    print("Training AdaBoost:", boosted.test(data[:4200]), "%")
    print("Testing AdaBoost:", boosted.test(data[4200:]), "%")


    return

if __name__ == "__main__":
    main()