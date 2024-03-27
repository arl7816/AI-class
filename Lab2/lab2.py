from KnowledgeBase import KnowledgeBase
import sys
from Clause import Clause

def main() -> None:
    manager = KnowledgeBase("Lab2/testcases (1)/functions/f2.cnf")
    #manager = KnowledgeBase(sys.argv[1])

    #print(manager)

    if manager.isSat():
        print("yes")
    else:
        print('no')

    #print(manager.contains("!animal(Kim) "))
    print(manager)

    #c1 = Clause("!sprint(t0) !rain(t0)")
    #c2 = Clause("sprint(A) sprint(B)")
    #result = c1 + c2
    #print([str(p) for p in result])

    return

if __name__ == "__main__":
    main()