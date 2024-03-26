from KnowledgeBase import KnowledgeBase
import sys

def main() -> None:
    #manager = KnowledgeBase("Lab2/testcases (1)/universals/u05.cnf")
    manager = KnowledgeBase(sys.argv[1])

    if manager.isSat():
        print("yes")
    else:
        print('no')

    #print(manager.contains("!animal(Kim) "))

    return

if __name__ == "__main__":
    main()