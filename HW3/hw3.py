# generate a tree with depth 2 that figures out 

from Structs import DTree
from AdaBoost import AdaBoost

COUNT = [10]

def print2DUtil(root, space):
 
    # Base case
    if (root == None):
        return
    
    # Increase distance between levels
    space += COUNT[0]
    
    # Process right child first
    print2DUtil(root.yes, space)
    
    # Print current node after space
    # count
    print()
    for i in range(COUNT[0], space):
        print(end=" ")
    print(root.value)
    
    # Process left child
    print2DUtil(root.no, space)
    
    # Wrapper over print2DUtil()

def print2D(root):
    
    # space=[0]
    # Pass initial space count as 0
    print2DUtil(root, 0)

def inOrder(root):
    if root.no is not None: inOrder(root.no)
    print(root.value)
    if root.yes is not None: inOrder(root.yes)

def main() -> None:
    
    with open("HW3/data.txt") as file:
        contents = [line.strip() for line in file.readlines()]
        Dtree = DTree(contents, 1)
        print2D(Dtree.root)

        print("doing adaboost")
        boost = AdaBoost(contents, 10000)

        #print("Printing my adaboost")
        #for h in boost.H:
            #print2D(h.tree.root)

    print("Training Percent error is", str(Dtree.test(contents)) +  "% for DTree")
    print("Training Percent error is", str(boost.test(contents)) + "% for AdaBoost")
    #print(boost.testAnswer("False False True False False False False True B".split()))

    with open("HW3/test.txt") as file:
        contents2 = [line.strip() for line in file.readlines()]
        print("Test Percent error is", str(Dtree.test(contents2)) +  "% for DTree")
        print("Test Percent error is", str(boost.test(contents2)) + "% for AdaBoost")

    return

if __name__ == "__main__":
    main()