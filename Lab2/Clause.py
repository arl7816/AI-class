from Predicates import Predicate
from copy import deepcopy

class Clause():
    """
    Contains a singular clause such that our KB may use CNF form
    """
    @staticmethod
    def init(predicates: set, variables: set, constants: set, functions: set):
        """
        Sets the global variables needed by predicates

        Args:
            predicates (set): the set of known predicates
            variables (set): the set of known varaibles
            constants (set): the set of known constants
            functions (set): the set of known functions
        """
        Predicate.init(predicates, variables, constants, functions)

    def __init__(self, clause: str) -> None:
        """The constructor for a given clause

        Args:
            clause (str): the clause in a string form
        """
        self.statement = tuple(sorted([Predicate(n) for n in clause.split()]))

    def __add__(self, other) -> list:
        """
        Performs logic on two clauses such that if they unify and 
        negate eachother, they contradict and form a new clause(s)

        Args:
            other (Clause): the other clause

        Raises:
            TypeError: if other is not a clause, will raise error

        Returns:
            list[clauses]: a new list of clauses 
        """
        if isinstance(other, str):
            return self.__str__() + other.__str__()

        if not(isinstance(other, Clause)):
            raise TypeError("Other must be a clause")

        result = []

        
        if self == other:
            return [self]
        
        for pred1 in self.statement:
            for pred2 in other.statement:
                negation = pred1.checkNegation(pred2)
                if negation:
                    newStatement1 = self.getLst(pred1)

                    newStatement2 = other.getLst(pred2)

                    unifyStatements = newStatement1 + newStatement2

                    unifyStatements = self.doUnify(unifyStatements, pred1, pred2)
                    unifyStatements = self.doUnify(unifyStatements, pred2, pred1)

                    newClause = Clause("")
                    newClause.statement = tuple(sorted(unifyStatements))

                    result.append(newClause)
        
        return result
    
    def replaceAll(self, unified: list, variable: list[str], constant: str, function = None) -> list:
        """replaces all instances of an argument with another

        Args:
            unified (list[clause]): the combined version of two clauses
            variable (list[str]): the list of arguments that will be replaced
            constant (str): what they will be replaced with (if None, then will create a new varaible and replace it with that)
            function (str, optional): if replaced with function replaces arguments like such. Defaults to None.

        Returns:
            list[clause]: the updated (unified) version of the clause 
        """
        cpy = unified[:]
        if constant is None:
            constant = Predicate.newVari()
        for pred in cpy:
            for index, arg in enumerate(pred.arguments):
                if arg in variable:
                    pred.arguments[index] = constant
                    if function is not None:
                        pred.functions[index] = function
        return cpy

    def doUnify(self, lst: list, pred1: Predicate, pred2: Predicate) -> list:
        """
        Unifies a given clause

        NOTE: order matters so its expected to do both\n
        doUnify(p1, p2) and doUnify(p2, p1)

        Args:
            lst (list[Clause]): the lst to unify
            pred1 (Predicate): the first predicate
            pred2 (Predicate): the second predicate

        Returns:
            list[clause]: the unified version of the clause
        """
        if pred1.arguments is None or pred2.arguments is None: return lst

        cpy = deepcopy(lst)

        for index, arg in enumerate(pred1.arguments):
            # one is a variable and the other is constant
            if pred1.isVarible(arg) and pred1.isConstant(pred2.arguments[index]) \
                and not(pred1.isFunction(index)) and not(pred2.isFunction(index)):
                cpy = self.replaceAll(cpy, [arg], pred2.arguments[index])

            # both are free variables
            elif pred1.isVarible(arg) and pred1.isVarible(pred2.arguments[index]) \
                and not(pred1.isFunction(index)) and not(pred2.isFunction(index)):
                cpy = self.replaceAll(cpy, [arg, pred2.arguments[index]], None)
            
            #one is a free variable, the other is a function
            elif pred2.isFunction(index) and pred1.isVarible(arg) and pred2.isVarible(pred2.arguments[index]):
                cpy = self.replaceAll(cpy, [arg], pred2.arguments[index], pred2.functions[index])

            # one is a free varaible while the other is a constant function
            elif pred1.isVarible(arg) and not(pred1.isFunction(index)) and \
                pred2.isFunction(index) and pred2.isConstant(pred2.arguments[index]):
                cpy = self.replaceAll(cpy, [arg], pred2.arguments[index], pred2.functions[index])

            

        return cpy

    def removeDuplicates(self, lst: list) -> list:
        """removes duplicates from a given list

        Args:
            lst (list): the list in quesiton

        Returns:
            list: a list with its duplicates removed
        """
        return list(set(lst))

    def getLst(self, cancel = None) -> list:
        """
        Gets the statements within the clause

        Args:
            cancel (predicate, optional): removes the first occurence of that element. Defaults to None.

        Returns:
            list: a list of clauses
        """
        newLst = list(self.statement[:])
        if cancel is not None:
            newLst.remove(cancel)
        return newLst

    def isEmpty(self) -> bool:
        """
        Checks if a given clause is empty

        Returns:
            bool: true if the clause is a condiction (empty) false otherwise
        """
        return len(self.statement) == 0

    def __str__(self) -> str:
        """Gets the string representation of a clause

        Returns:
            str: takes the form: [p1, p2, p3, ..., pn]
        """
        return str(tuple([p.__str__() for p in self.statement]))
    
    def __eq__(self, __value: object) -> bool:
        """checks if two clauses are equal

        Args:
            __value (Clause): the other clause

        Returns:
            bool: true if self = __value, false otherwise
        """
        result = False

        if (isinstance(__value, Clause)):
            return self.statement == __value.statement
        
        return result
    
    def __hash__(self) -> int:
        """Gets the hash code of the clause

        Returns:
            int: the hashcode
        """
        return hash(self.statement)