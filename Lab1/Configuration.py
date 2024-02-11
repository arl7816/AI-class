from math import pow, sqrt
from imageHandler import ImageHandler, Map

"""Static variable between all Configurations, holds all elevations"""
elevations = []

class Configuration:
    """
    Node representation within our search where it is contained with
    the x,y coordinates on image.
    """

    """
    Y and X constant variables to represent the real life distance of a node moving to another coordinate
    """
    Y_DISTANCE = 10.29
    X_DISTANCE = 7.55


    """A static image shared between all Configurations"""
    IH = None

    def __init__(self, row: int, col: int, parent = None, goal = None) -> None:
        """
        Creates a node within our search tree
        
        Pre:
            both the elevation and terrain have been configured via this classes static functions
        
        Args:
            row (int): the row within our image (y)
            col (int): the column within our image (x)
            parent (Configuration): where did this node travel from. Defaults to None if this is the root node or the goal
            goal (Configuration): what node is considered to be our destination. Defaults to None is this is the goal node
        """
        self.row, self.col= row, col

        # this has been generated in the x y order
        self.height = elevations[row][col]

        # the terrain file is in the normal y x order
        self.terrain = Configuration.IH.getPixel(row, col)
        
        if parent is None:
            self.cost = 0
            self.distance = 0
        else:
            dist = self.getDistance(parent)
            self.distance = parent.distance + dist
            self.cost = parent.cost + dist * ((self.getSpeed(self.terrain) + self.getSpeed(parent.terrain)) / 2)

        if goal is None:
            self.fitness = -1
        else:
            self.fitness = self.cost + self.getDistance(goal) * 1

        self.goal = goal

    @staticmethod
    def transpose(array2: list[list[object]]) -> list[list[object]]:
        """
        STATIC
        Swaps all rows and columns in an array

        Args:
            array2 (list[list[object]]): the array being swapped

        Returns:
            list[list[object]] the array with all rows and columns swapped
        """
        array = array2[:]  # make copy to avoid changing original
        n = len(array)
        for i, row in enumerate(array):
            array[i] = row + [None for _ in range(n - len(row))]

        array = list(zip(*array2))

        for i, row in enumerate(array):
            array[i] = [elem for elem in row if elem is not None]

        return array

    @staticmethod
    def generate_elevation(fileName: str) -> None:
        """
        STATIC Sets the static elevations array so that Configurations can be made

        Post:
            Configurations can be made so long as generate_terrain is called before or after this function

        Args:
            fileName (str): the file name containing the data on the heights of the map
        """
        global elevations
        with open(fileName, "r") as file:
            for line in file.readlines():
                ary = [float(element) for element in line.split()]
                elevations.append(ary[:-5])

        # for the sake of not keeping track of whats x,y or y,x this is 
        # getting transposed so everything is y,x
        elevations = Configuration.transpose(elevations)


    @staticmethod
    def generate_terrain(file_name: str) -> None:
        """
        STATIC confingures the terrain of the map that the node may be on

        Post:
            Configurations can be made so long as generate_elevation is called before or after this function

        Args:
            file_name (str): the image of the terrain itself.
        """
        Configuration.IH = ImageHandler(file_name)


    def getDistance(self, otherConfig) -> float:
        """
        Gets the distance between this node and another node using the following eqation
        
        (deltaX^2 + deltaY^2 + deltaZ^2)^.5


        Args:
            otherConfig (Configuration): the other node

        Returns:
            float: the distance between the nodes
        """
        x = pow(self.X_DISTANCE * (self.col - otherConfig.col), 2)
        y = pow(self.Y_DISTANCE * (self.row - otherConfig.row), 2)
        z = pow((self.height - otherConfig.height), 2)
        return sqrt(x + y + z)
    
    def isGoal(self) -> bool:
        """
        Checks if this node is the goal

        Returns:
            bool: true if it is the goal, false otherwise
        """
        return self == self.goal
    
    def getSpeed(self, terrain: tuple[int, int, int]) -> float:
        """
        Returns a speed mulplier based on the terrain type

        Args:
            terrain (tuple[int, int, int]): a tuple representing the RGB color of the coordinate

        Returns:
            float: 0 < n < infinty
        """
        if terrain == Map.OPEN_LAND:
            return 0.5
        if terrain == Map.ROUGH_MEADOW:
            return 2
        if terrain == Map.EASY_FOREST:
            return 0.5
        if terrain == Map.SLOW_FOREST:
            return 2.5
        if terrain == Map.WALK_FOREST:
            return 1
        if terrain ==  Map.IMPASSIBLE:
            return 1000
        if terrain == Map.WATER:
            return 4
        if terrain == Map.ROAD:
            return 0.5
        if terrain == Map.FOOTPATH:
            return 0.8
        return 1

    def generate_neigh(self) -> list:
        """
        generates the neighbors of the current node in the following order

        (x, y - 1), (x, y + 1), (x + 1, y), (x - 1, y) where able to.

        Returns:
            list[Configuration]: list of new Configurations
        """
        lst = []
        col = self.col
        row = self.row
        height = self.height

        max_width = len(elevations[0]) - 1
        max_height = len(elevations) - 1

        # above
        if row != 0 and Configuration.IH.getPixel(row - 1, col) != Map.OUT_OF_BOUNDS:
            lst.append(Configuration(row - 1, col, self, self.goal))

        # below
        if row != max_height and Configuration.IH.getPixel(row + 1, col) != Map.OUT_OF_BOUNDS:
            lst.append(Configuration(row + 1, col, self, self.goal))

        # right
        if col != max_width and Configuration.IH.getPixel(row, col + 1) != Map.OUT_OF_BOUNDS:
            lst.append(Configuration(row, col + 1, self, self.goal))

        # left
        if col != 0 and Configuration.IH.getPixel(row, col - 1) != Map.OUT_OF_BOUNDS:
            lst.append(Configuration(row, col - 1, self, self.goal))
            

        return lst
    
    def __hash__(self) -> int:
        """ Gets the hashcode of the class

        Returns:
            int: a number specific to this node
        """
        # due to floating point errors, fitness and cost are not taken into account
        return hash(self.terrain) + self.row + self.col
    
    def __eq__(self, __value: object) -> bool:
        """Checks if 2 Configurations are equal to eachother

        Args:
            __value (Configuration): the other node

        Returns:
            bool: true if they have the same coordinates, false otherwise
        """
        result = False
        if isinstance(__value, Configuration):
            result = self.row == __value.row and self.col == __value.col
        return result
    
    def __lt__(self, other) -> bool:
        """
        Checks if our current node is less than another node

        Args:
            other (Configuration): the other node

        Returns:
            bool: true is out fitness is less than the other node, false otherwise
        """
        return self.fitness <= other.fitness
    
    def __str__(self) -> str:
        """
        Gets the string representation of the node

        Returns:
            str: a string in the form of (row, col) with cost = # distance = # fitness = # terrain = <type> DTG = #
        """
        return "(" + str(self.row) + ", " + str(self.col) + \
            ") with cost = " + str(self.cost) + " distance = " + str(self.distance) + \
            " fitness = " + str(self.fitness) + " terrain = " + str(self.terrain) + \
            " DTG = " + str(self.getDistance(self.goal))

    pass