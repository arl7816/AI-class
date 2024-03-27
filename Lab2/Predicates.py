from copy import deepcopy

class Predicate:
    predicates = None
    variables = None
    constants = None
    functions = None

    @staticmethod
    def init(newPredicates: set, newVariables: set, newConstants: set, functions: set):
        Predicate.predicates = newPredicates
        Predicate.variables = newVariables
        Predicate.constants = newConstants
        Predicate.functions = functions


    def __init__(self, value: str) -> None:
        """
        Predicate
        Variable | Constant
        Negation

        Args:
            value (str): _description_
        """
        self.value = value

        # list of dict thats map a arg index to a function
        self.functions = dict()

        self.negation = (self.value[0] == "!")

        tempValue = value[:].removeprefix("!")

        index = tempValue.find("(")
        if index == -1:
            self.pred = tempValue
            self.arguments = None
            return
        
        self.pred = tempValue[:index]
        self.arguments = tempValue[index+1:-1].split(",")

        for index, arg in enumerate(self.arguments):
            testFunctionIndex = arg.find("(")
            if testFunctionIndex == -1:
                continue
            self.functions[index] = arg[:testFunctionIndex]
            self.arguments[index] = arg[testFunctionIndex + 1: -1]


    @staticmethod
    def proof():
        print(Predicate.constants)
        print(Predicate.variables)
        print(Predicate.predicates)

    def isVarible(self, argument: str) -> bool:
        return argument in Predicate.variables
    
    def isConstant(self, argument: str) -> bool:
        return argument in Predicate.constants

    def getValue(self) -> str:
        return self.value
    
    def unify(self, argument1: str, argument2: str) -> bool:
        #print("checking", argument1, "with", argument2, "using", Predicate.variables)

        if argument1 is None and argument2 is None: return True

        if argument1 in Predicate.variables or argument2 in Predicate.variables: return True

        return argument1 == argument2
    
    def unifyAll(self, other) -> bool:
        if self.arguments is None and other.arguments is None: return True

        for index in range(len(self.arguments)):
            if not self.unify(self.arguments[index], other.arguments[index]):
                return False
        return True

    def checkNegation(self, other):
        if isinstance(other, Predicate):
            if self.pred == other.pred and self.unifyAll(other):
                return self.negation == True and other.negation == False or \
                self.negation == False and other.negation == True
        
        return False
    
    def getArgumentsAsString(self) -> list:
        args = deepcopy(self.arguments)
        for index in range(len(args)):
            if index in self.functions:
                args[index] = str(self.functions[index]) + "(" + str(args[index]) + ")"
        return str(args)

    def isFunction(self, index: int) -> bool:
        return index in self.functions
    
    def isArgFunction(self, arg: str) -> bool:
        return self.isFunction(self.arguments.index(arg))
    
    def __eq__(self, __value: object) -> bool:
        result = False

        if isinstance(__value, Predicate):
            #return self.value == __value.value
            return self.negation == __value.negation and self.pred == __value.pred and \
                self.arguments == __value.arguments

        return result
    
    def __lt__(self, __value: object) -> bool:
        if isinstance(__value, Predicate):
            return self.pred < __value.pred
        raise TypeError("Cant compare predicate with other type")
    
    def __hash__(self) -> int:
        return hash(self.pred) + hash(self.negation) + \
            hash(tuple(self.arguments)) if self.arguments is not None else 0

    def __str__(self) -> str:
        return ("!" if self.negation else "") + self.pred + "(" + self.getArgumentsAsString() + ")"