from Clause import Clause

class KnowledgeBase():
    kb = []
    known = set()
    actions = set()

    variables = set()
    constants = set()
    predicates = set()
    functions = set()

    def __init__(self, filename: str) -> None:
        with open(filename, "r") as file:
            lines = file.readlines()

            for pred in lines[0].split()[1:]:
                if pred[-1] == "\n":
                    pred = pred.removesuffix("\n")
                self.predicates.add(pred)       
            

            for vari in lines[1].split()[1:]:
                if vari[-1] == "\n":
                    vari.removesuffix("\n")
                self.variables.add(vari)

            
            for const in lines[2].split()[1:]:
                if const[-1] == "\n":
                    const.removesuffix("\n")
                self.constants.add(const)

            for funct in lines[3].split()[1:]:
                if funct[-1] == "\n":
                    funct.removesuffix("\n")
                self.functions.add(funct)

            for line in lines[5:]:
                self.kb.append(Clause(line[:-1]))
                self.known.add(self.kb[-1])
            
            Clause.init(self.predicates, self.variables, self.constants, self.functions)


    def isSat(self) -> bool:
        for clause1 in self.kb:
            for cluase2 in self.kb:
                if clause1 == cluase2: continue

                if (clause1, cluase2) not in self.actions \
                    or (cluase2, clause1) not in self.actions:
                    self.actions.add((clause1, cluase2))
                else:
                    continue

                result = clause1 + cluase2
                for cl in result:
                    #print(cl + " checking")

                    if cl.isEmpty(): 
                        return False

                    if cl not in self.known:
                        #print(cl + " has been found using" + str(clause1) + " and " + str(cluase2))
                        self.known.add(cl)
                        self.kb.append(cl)

                        #return False

        return True

    def contains(self, pred: str) -> bool:
        return pred in self.known

    def getKB(self) -> list:
        return self.kb
    
    def __str__(self) -> str:
        returnStr = "KB:\n"
        for clause in self.kb:
            returnStr += str(clause) + "\n"
        return returnStr

