from math import pow, sqrt
from imageHandler import ImageHandler, Map

elevations = []

class Configuration:
    Y_DISTANCE = 10.29
    X_DISTANCE = 7.55

    IH = None

    def __init__(self, row: int, col: int, parent: object, goal: object) -> None:
        self.row, self.col= row, col
        #print(row, col)
        #print(len(elevations[17]))
        self.height = elevations[row][col]
        self.terrain = Configuration.IH.getPixel(row, col)
        #if self.terrain == Map.EASY_FOREST: print("EASY FOREST")
        #print(self.terrain)
        
        if parent is None:
            self.cost = 0
            self.distance = 0
        else:
            # try to encorpoarte whether downhill or uphill
            dist = self.getDistance(parent)
            self.distance = parent.distance + dist
            self.cost = parent.cost + dist * ((self.getSpeed(self.terrain) + self.getSpeed(parent.terrain)) / 2)  #* self.incline(parent.height) # this will be changed later for speeds

        if goal is None:
            self.fitness = -1
        else:
            self.fitness = self.cost + self.getDistance(goal) * 1

        self.goal = goal

    def incline(self, height: float) -> float:
        # makes it much slower for some reason
        if self.height > height:
            return .9
        elif self.height < height:
            return 1.1
        return 1

    @staticmethod
    def generate_elevation(fileName: str) -> None:
        with open(fileName, "r") as file:
            for line in file.readlines():
                ary = [float(element) for element in line.split()]
                elevations.append(ary[:-5])

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
            return 0.5
        return 1

    def generate_neigh(self) -> list:
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
        return hash(self.terrain) + self.row + self.col
    
    def __eq__(self, __value: object) -> bool:
        result = False
        if isinstance(__value, Configuration):
            result = self.row == __value.row and self.col == __value.col
        return result
    
    def __lt__(self, other):
        return self.fitness < other.fitness
    
    def __str__(self) -> str:
        return "(" + str(self.row) + ", " + str(self.col) + \
            ") with cost = " + str(self.cost) + " distance = " + str(self.distance) + \
            " fitness = " + str(self.fitness) + " terrain = " + str(self.terrain) + \
            " DTG = " + str(self.getDistance(self.goal))

    pass