from KnowledgeBase import KnowledgeBase
import sys
from Clause import Clause

def main() -> None:
    """
    In charge of checking whether or not a Knowledge base is satisible
    Usage <filname>
    - Filename is the path to the knowledge base
    """
    #manager = KnowledgeBase("Lab2/testcases (1)/functions/f3.cnf")
    #manager = KnowledgeBase("Lab2/testcases (1)/prop/p01.cnf")
    manager = KnowledgeBase(sys.argv[1])

    #print(manager)

    if manager.isSat():
        print("yes")
    else:
        print('no')

    #print(manager.contains("!animal(Kim) "))
    #print(manager)

    """c2 = Clause("loves(SKF0(Kim),Kim)")
    c1 = Clause("!loves(x5,Kim)")
    result = c1 + c2
    print("Length of result", result[0].isEmpty())
    print("Final result:", [str(p) for p in result])"""

    return

if __name__ == "__main__":
    main()