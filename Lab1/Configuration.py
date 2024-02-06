from math import pow, sqrt
from imageHandler import ImageHandler, Map

class Configuration:
    X_DISTANCE = 10.29
    Y_DISTANCE = 7.55

    elevations = []

    def __init__(self, coordinates: tuple[int, int, int], terrain: tuple[int, int, int], parent: object, goal: object) -> None:
        self.coordinates = coordinates
        self.terrain = terrain
        
        if parent is None:
            self.cost = 0
        else:
            self.cost = self.getDistance(parent) + self.getSpeed(terrain) # this will be changed later for speeds

        if goal is None:
            self.fitness = -1
        else:
            self.fitness = self.cost + self.getDistance(goal)

        self.goal = goal

    @staticmethod
    def generate_elevation(fileName: str):
        with open(fileName, "r") as file:
            for line in file.readlines():
                Configuration.elevations.append([float(element) for element in line.split()])


    def getDistance(self, otherConfig) -> float:
        x = pow(self.X_DISTANCE * (self.coordinates[0] - otherConfig.coordinates[0]), 2)
        y = pow(self.X_DISTANCE * (self.coordinates[1] - otherConfig.coordinates[1]), 2)
        z = pow(self.X_DISTANCE * (self.coordinates[2] - otherConfig.coordinates[2]), 2)
        return sqrt(x + y + z)
    
    def isGoal(self) -> bool:
        return self == self.goal
    
    def getSpeed(self, terrain: tuple[int, int, int]) -> int:
        return 0

    def generate_neigh(self, terrain: list[list[int]], img: ImageHandler) -> list:
        lst = []

        # above

        # below

        # right

        # left

        return lst
    
    def __hash__(self) -> int:
        return hash(self.terrain) + hash(self.coordinates) + self.cost + self.fitness
    
    def __eq__(self, __value: object) -> bool:
        result = False
        if isinstance(__value, Configuration):
            result = self.coordinates[0] == __value.coordinates[0] and self.coordinates[1] == __value.coordinates[1] and self.coordinates[2] == __value.coordinates[2]
        return result
    
    def __lt__(self, other):
        return self.fitness < other.fitness

    pass