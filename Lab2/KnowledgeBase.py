from Clause import Clause

class KnowledgeBase():
    """
    Manages the knowledge base

    NOTE: it is assumed that only one instance of the knowledge base is being used and
    interacted with in a given process
    """
    # every clause within the knowledge base
    kb = []
    # known clauses
    known = set()

    # clause combinations tested
    actions = set()

    variables = set()
    constants = set()
    predicates = set()
    functions = set()

    def __init__(self, filename: str) -> None:
        """
        Constructs the knowledge base. 
        Post-Cond: Updates the known variables, constants, predicates, and functions 
        statically.

        Args:
            filename (str): the file path containing the initial knowledge base
        """
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
        """
        Determines if a knowledge base is satisfiable.
        POST-COND: the knowledge base is updated to include new 
        clauses, but only ones that can be formed via unification


        Returns:
            bool: false if a empty clause is found, true otherwise
        """
        for clause1 in self.kb:
            for cluase2 in self.kb:
                if clause1 == cluase2: continue

                """if (clause1, cluase2) not in self.actions \
                    or (cluase2, clause1) not in self.actions:
                    self.actions.add((clause1, cluase2))
                else:
                    continue"""

                result = clause1 + cluase2
                for cl in result:

                    if cl.isEmpty(): 
                        return False

                    if cl not in self.known:
                        self.known.add(cl)
                        self.kb.append(cl)

                        #return False

        return True


    def getKB(self) -> list:
        """Gets the knowledge base

        Returns:
            list[Clause]: An array of clauses
        """
        return self.kb
    
    def __str__(self) -> str:
        """
        Returns the string representation of the knowledge base

        Returns:
            str: takes the form KB:\n
            <Clause1>\n
            <Clause2>\n
            ...\n
            <ClauseN>
        """
        returnStr = "KB:\n"
        for clause in self.kb:
            returnStr += str(clause) + "\n"
        return returnStr

