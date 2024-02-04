class Configuration:
    def __init__(self, cost: float, coordinate: tuple[int, int], heuristic: float) -> None:
        self.cost = cost
        self.value = (coordinate[0], coordinate[1])
        self.fitness = self.cost + heuristic

    def generate_neigh(self) -> list:
        return []

    pass