from Predicates import Predicate
from copy import deepcopy

class Clause():
    @staticmethod
    def init(predicates: set, variables: set, constants: set, functions: set):
        Predicate.init(predicates, variables, constants, functions)

    def __init__(self, clause: str) -> None:
        self.statement = tuple(sorted([Predicate(n) for n in clause.split()]))

    def __add__(self, other) -> list:
        if isinstance(other, str):
            return self.__str__() + other.__str__()

        if not(isinstance(other, Clause)):
            raise TypeError("Other must be a clause")

        result = []
        
        if self == other:
            return [self]
        
        for pred1 in self.statement:
            for pred2 in other.statement:
                if pred1.checkNegation(pred2):
                    #print("Adding", self, "with", other)
                    print(pred1, "and", pred2, "are negations")
                    newStatement1 = self.getLst(pred1)

                    newStatement2 = other.getLst(pred2)

                    #unifyStatements = self.removeDuplicates(newStatement1 + newStatement2)
                    unifyStatements = newStatement1 + newStatement2

                    unifyStatements = self.doUnify(unifyStatements, pred1, pred2)
                    unifyStatements = self.doUnify(unifyStatements, pred2, pred1)

                    newClause = Clause("")
                    newClause.statement = tuple(sorted(unifyStatements))

                    #print("Appending", newClause)
                    result.append(newClause)
        
        return result
    
    def replaceAll(self, unified: list, variable: str, constant: str, function = None) -> list:
        #print("Before:", [str(p) for p in unified])
        #print("Replacing all", variable, "with", constant)
        cpy = unified[:]
        for pred in cpy:
            for index, arg in enumerate(pred.arguments):
                if arg == variable:
                    pred.arguments[index] = constant
                    if function is not None:
                        pred.functions[index] = function
        #print("After", [str(p) for p in unified], "\n")
        return cpy

    def doUnify(self, lst: list, pred1: Predicate, pred2: Predicate) -> list:
        if pred1.arguments is None or pred2.arguments is None: return lst

        cpy = deepcopy(lst)

        for index, arg in enumerate(pred1.arguments):
            if pred1.isVarible(arg) and pred1.isConstant(pred2.arguments[index]) \
                and not(pred1.isFunction(index)) and not(pred2.isFunction(index)):
                cpy = self.replaceAll(cpy, arg, pred2.arguments[index])
            
            if pred2.isFunction(index) and pred1.isVarible(arg) and pred2.isVarible(pred2.arguments[index]):
                print("Have function type of", pred2.functions[index])
                cpy = self.replaceAll(cpy, arg, pred2.arguments[index], pred2.functions[index])

            if pred1.isVarible(arg) and not(pred1.isFunction(index)) and \
                pred2.isFunction(index) and pred2.isConstant(pred2.arguments[index]):
                cpy = self.replaceAll(cpy, arg, pred2.arguments[index], pred2.functions[index])


        return cpy

    def removeDuplicates(self, lst: list) -> list:
        return list(set(lst))

    def getLst(self, cancel = None) -> list:
        newLst = list(self.statement[:])
        if cancel is not None:
            newLst.remove(cancel)
        return newLst

    def isEmpty(self) -> bool:
        return len(self.statement) == 0

    def __str__(self) -> str:
        return str(tuple([p.__str__() for p in self.statement]))
    
    def __eq__(self, __value: object) -> bool:
        result = False

        if (isinstance(__value, Clause)):
            #return hash(self) == hash(__value)
            return self.statement == __value.statement
        
        return result
    
    def __hash__(self) -> int:
        return hash(self.statement)