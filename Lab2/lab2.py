from KnowledgeBase import KnowledgeBase
import sys
from Clause import Clause

def main() -> None:
    """
    In charge of checking whether or not a Knowledge base is satisible
    Usage <filname>
    - Filename is the path to the knowledge base
    """
    manager = KnowledgeBase(sys.argv[1])


    if manager.isSat():
        print("yes")
    else:
        print('no')

    return

if __name__ == "__main__":
    main()