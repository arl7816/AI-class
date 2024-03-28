from copy import deepcopy

class Predicate:
    """
    A single predicate under the CNF form for either predicates or FOL
    """
    predicates = None
    variables = None
    constants = None
    functions = None

    newVariStr = "UHAUHA"
    nextVariInt = 0

    @staticmethod
    def init(newPredicates: set, newVariables: set, newConstants: set, functions: set):
        """
        Sets the default values for predicates, variables, constants, and functions that
        a predicate may fall under. 

        Args:
            newPredicates (set): shared predicates
            newVariables (set): shared variables
            newConstants (set): shared constants
            functions (set): shared functions
        """
        Predicate.predicates = newPredicates
        Predicate.variables = newVariables
        Predicate.constants = newConstants
        Predicate.functions = functions


    @staticmethod
    def newVari() -> str:
        """Creates a new variable within the KB

        Returns:
            str: the new variable
        """
        Predicate.nextVariInt += 1
        newVari = Predicate.newVariStr + str(Predicate.nextVariInt)

        Predicate.variables.add(newVari)
        return newVari

    def __init__(self, value: str) -> None:
        """
        Constructor for a given predicate within a clause

        Args:
            value (str): the value of the predicate
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
        """
        Prints out the constants, variables, and predicates that are known and shared
        statically. 
        """
        print(Predicate.constants)
        print(Predicate.variables)
        print(Predicate.predicates)

    def isVarible(self, argument: str) -> bool:
        """
        Checks if a given predicate uses a free variable

        Args:
            argument (str): the argument in question

        Returns:
            bool: true if the argument is a free variable, false otherwise. 
        """
        return argument in Predicate.variables
    
    def isConstant(self, argument: str) -> bool:
        """Checks to see if a given argument is a constant

        Args:
            argument (str): the argument in question

        Returns:
            bool: true if the argument is a constant, false otherwise
        """
        return argument in Predicate.constants

    def getValue(self) -> str:
        """Gets the value of the predicate

        Returns:
            str: predicates value
        """
        return self.value
    
    def unify(self, argument1: str, argument2: str, other = None , index = None) -> bool:
        """
        determines if two arguments within a predicate can be unified

        Args:
            argument1 (str): the first argument
            argument2 (str): the argument being compared to
            other (Predicate, optional): the predicate containing argument 2. Defaults to None.
            index (int, optional): the index of the function used by argument 2. Defaults to None.

        Returns:
            bool: true if the two arguments can be unified, false otherwise
        """
        #print("checking", argument1, "with", argument2, "using", Predicate.variables)

        # can assume arguments are same and predicate is same

        # they are both predicates, they are already unified must unify
        # [p] [!p]
        if argument1 is None and argument2 is None: return True

        # both are varaibles and thus can be replaced with another free variable
        # [p(x1)] [p(x2)]
        if (argument1 in Predicate.variables or argument2 in Predicate.variables) and \
                (not(self.isFunction(index)) and not(other.isFunction(index))): 
            return True

        # one of them is a function in general while the other is a constant
        # [p(F(x1))] [p(KIM)] --> F(x1) can never take the form KIM
        if self.isFunction(index) and self.isConstant(argument2) or \
            other.isFunction(index) and self.isConstant(argument1):
            #print("Well Im here now for ", self, "and", other)
            return False
        
        # both are constant but one is a function
        # [p(F(KIM))] [P(KIM)]
        if self.isConstant(argument1) and self.isConstant(argument2) and \
            (self.isArgFunction(argument1) or other.isFunction(index)):
                return False
        
        # if one is a free variable and the other is a constant function
        # they can unify
        # [p(x1)][p(SKF(KIM))]
        if self.isVarible(argument1) and other.isConstant(argument2) and other.isFunction(index) or \
            other.isVarible(argument2) and self.isConstant(argument1) and self.isFunction(index):
                return True

        #print("Im here: argument is function for argument2 is", other.isFunction(index), "for argument", argument2)
        return argument1 == argument2
    
    def unifyAll(self, other) -> bool:
        """Checks if two predicates can be unifed

        Args:
            other (Predicate): the predicate being unified with

        Returns:
            bool: true if all arguments between the two may be unified
        """
        if self.arguments is None and other.arguments is None: return True

        for index in range(len(self.arguments)):
            if not self.unify(self.arguments[index], other.arguments[index], other, index):
                return False
        return True

    def checkNegation(self, other) -> bool:
        """checks if two given predicates are both negation of eachother
        and that they unify

        Args:
            other (Predicate): the other predicate in question

        Returns:
            bool: true if they unify and are negations of eachother, false otherwise
        """
        if isinstance(other, Predicate):
            if self.pred == other.pred and self.unifyAll(other):
                return self.negation == True and other.negation == False or \
                self.negation == False and other.negation == True
        
        return False
    
    def getArgumentsAsString(self) -> list:
        """Gets the arguments of the Predicate as a deep copy,
        refitting them so that they also showcase their functions

        Returns:
            list[str]: the string representation of the arguments
        """
        args = deepcopy(self.arguments)
        for index in range(len(args)):
            if index in self.functions:
                args[index] = str(self.functions[index]) + "(" + str(args[index]) + ")"
        return str(args)

    def isFunction(self, index: int) -> bool:
        """checks to see if a argument within self is a 
        function

        Args:
            index (int): the index of the argument

        Returns:
            bool: true if a function, false otherwise
        """
        return index in self.functions
    
    def isArgFunction(self, arg: str) -> bool:
        """checks to see if a argument within self is a function

        Args:
            arg (str): the argument

        Returns:
            bool: true if a function, false otherwise
        """
        try:
            return self.isFunction(self.arguments.index(arg))
        except:
            return False
    
    def __eq__(self, __value: object) -> bool:
        """checks to see if two predicates are the same

        Args:
            __value (object): the object being compared to

        Returns:
            bool: true if the predicates are identical, false otherwise
        """
        result = False

        if isinstance(__value, Predicate):
            #return self.value == __value.value
            return self.negation == __value.negation and self.pred == __value.pred and \
                self.arguments == __value.arguments and self.functions == __value.functions

        return result
    
    def __lt__(self, __value: object) -> bool:
        """checks if this predicate is less then another predicate

        Args:
            __value (Predicate): the object being compared to

        Raises:
            TypeError: if __value is not of type Predicate

        Returns:
            bool: true if self < __value, false otherwise
        """
        if isinstance(__value, Predicate):
            return self.pred < __value.pred
        raise TypeError("Cant compare predicate with other type")
    
    def __hash__(self) -> int:
        """Generates the hash code of the given Predicate

        Returns:
            int: the hash code
        """
        return hash(self.pred) + hash(self.negation) + \
            hash(tuple(self.arguments)) if self.arguments is not None else 0 + \
                hash(frozenset(self.functions.values()))

    def __str__(self) -> str:
        return ("!" if self.negation else "") + self.pred + "(" + self.getArgumentsAsString() + ")"