from math import pow, sqrt
from imageHandler import ImageHandler, Map

class Configuration:
    X_DISTANCE = 10.29
    Y_DISTANCE = 7.55

    elevations = []
    IH = None

    def __init__(self, row: int, col: int, parent: object, goal: object) -> None:
        self.row, self.col= row, col
        self.height = Configuration.elevations[row][col]
        self.terrain = Configuration.IH.getPixel(row, col)
        
        if parent is None:
            self.cost = 0
        else:
            self.cost = parent.cost + self.getDistance(parent) + self.getSpeed(self.terrain) # this will be changed later for speeds

        if goal is None:
            self.fitness = -1
        else:
            self.fitness = self.cost + self.getDistance(goal)

        self.goal = goal

    @staticmethod
    def generate_elevation(fileName: str) -> None:
        with open(fileName, "r") as file:
            for line in file.readlines():
                Configuration.elevations.append([float(element) for element in line.split()])

    @staticmethod
    def generate_terrain(file_name: str) -> None:
        Configuration.IH = ImageHandler(file_name)

    def getDistance(self, otherConfig) -> float:
        x = pow(self.X_DISTANCE * (self.col - otherConfig.col), 2)
        y = pow(self.Y_DISTANCE * (self.row - otherConfig.row), 2)
        z = pow((self.height - otherConfig.height), 2)
        return sqrt(x + y + z)
    
    def isGoal(self) -> bool:
        return self == self.goal
    
    def getSpeed(self, terrain: tuple[int, int, int]) -> int:
        return 0

    def generate_neigh(self) -> list:
        lst = []
        col = self.col
        row = self.row
        height = self.height

        max_width = len(Configuration.elevations[0]) - 1
        max_height = len(Configuration.elevations) - 1

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
        return hash(self.terrain) + self.row + self.col + hash(self.cost) + hash(self.fitness)
    
    def __eq__(self, __value: object) -> bool:
        result = False
        if isinstance(__value, Configuration):
            result = self.row == __value.row and self.col == __value.col and self.height == __value.height
        return result
    
    def __lt__(self, other):
        return self.fitness < other.fitness
    
    def __str__(self) -> str:
        return "(" + str(self.row) + " , " + str(self.col) + ")"

    pass