from imageHandler import ImageHandler as IH
from PathFinder import find_path
from Configuration import Configuration

import heapq

def main() -> None:
    path = "Lab1\\examples\\brown-out.png"
    path2 = "Lab1\\examples\\brown-out-2.png"

    """with open("Lab1\\examples\\terrain.txt") as file:
        #lst = list(filter(lambda w: w != "", file.read().split(" ")))
        lst = [float(element) for element in file.read().split(" ") if element != ""]

        print(max(lst) - min(lst))"""
    
    goal = Configuration((2,1,0), (0,0,0), None, None)

    lst = []
    heapq.heapify(lst)

    config1 = Configuration((0,1,2), (0,0,0), None, goal)
    config2 = Configuration((10,80,20), (0,0,0), config1, goal)
    config3 = Configuration((0,2,3), (0,0,0), config1, goal)
    config4 = Configuration((2,3,4), (0,0,0), config2, goal)

    heapq.heappush(lst, config1)
    heapq.heappush(lst, config2)
    
    popped = heapq.heappop(lst)
    print(popped.coordinates, "with a fitness of", popped.fitness)

    heapq.heappush(lst, config4)
    heapq.heappush(lst, config3)

    popped = heapq.heappop(lst)
    print(popped.coordinates, "with a fitness of", popped.fitness)



    return 

if __name__ == "__main__":
    main()