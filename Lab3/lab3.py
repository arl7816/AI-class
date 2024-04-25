# generate a tree with depth 2 that figures out 

from Structs import DTree
from AdaBoost import AdaBoost
from DTreeInterface import print2D, inOrder
from DataManager import DataManager
from Manager import Manager
import sys

def train(examples: str, output: str, learningType: str):
    """Trains a given model on some dataset

    Args:
        examples (str): the file containing examples
        output (str): the name of the file to save the model to
        learningType (str): either dt (decision tree) or ada (adaboosting)
    """
    data = DataManager().getContent(examples)

    tree = None
    if learningType == "dt":
        tree = DTree(data, "en", "nl", 20, file = examples)
    elif learningType == "ada":
        tree = AdaBoost(data, 50, "en", "nl", examples)
    
    Manager.save(tree, output)

def predict(hypoth: str, inputs: str) -> None:
    """
    Prints out the predicted language of a sentence
    Either being english or dutch

    Args:
        hypoth (str): the model on which we run
        inputs (str): the file containing the sentences, if none is given uses the file it was 
        trained on.
    """
    tree = Manager.restore(hypoth)

    mana = DataManager()

    if inputs is not None:

        with open(inputs, "r", encoding="utf8") as file:
            #print(file.readlines())
            for line in file.readlines():
                if line == "":
                    continue

                line = line.strip()
                prased = mana.parseLine(line, "hi")

                print(tree.answer(prased[:-1]))
    else:
        for line in DataManager().getContent(tree.file):
            print(tree.answer(line.split()[:-1]))

def main() -> None:
    """
    main runner for the program in which you can choose to do 
    two things. Either train a model on a adaboost or dt model

    args: 
    <command> <args>

    training args entail <example file> <model file name> <dt | ada>

    predict args <model name (optional)> <input file>
    """

    if sys.argv[1] == "train":
        # examples, output file, learning type
        train(sys.argv[2], sys.argv[3], sys.argv[4])

    elif sys.argv[1] == "predict":
        # tree file, inputs
        if len(sys.argv) < 4:
            predict("best.model", sys.argv[2])
            return
        predict(sys.argv[2], sys.argv[3])

    return

if __name__ == "__main__":
    main()