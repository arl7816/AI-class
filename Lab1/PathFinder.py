#from Classes import Queue, LinkedList
import sys
from Configuration import Configuration
import heapq
from DataStructs import LinkedList

def construct_path(visited: str, start: Configuration, goal: Configuration) -> LinkedList:
    path = LinkedList()
    
    path.insert(goal)

    current = visited[goal]

    while current != start:
        path.insert(current)
        current = visited[current]
    
    path.insert(current)
    
    return path

def find_path(start_coors: tuple[int, int], goal_coors: tuple[int, int], elevation_file: str, terrain_file: str, print_test = False) -> list:
    Configuration.generate_elevation(elevation_file)
    Configuration.generate_terrain(terrain_file)

    goal = Configuration(goal_coors[0], goal_coors[1], None, None)
    start = Configuration(start_coors[0], start_coors[1], None, goal)
    
    li = [start]
    heapq.heapify(li)
    visited = {}
    current = None

    visited[start] = start

    while True:
        if len(li) == 0:
            break
        current = heapq.heappop(li)

        if current == goal:
            Configuration.IH.close()
            
            if print_test:
                print("Found goal of " + str(current))
            
            return construct_path(visited, start, current)

        for config in current.generate_neigh():
            if config not in visited:
                if print_test:
                    print(config)
                heapq.heappush(li, config)
                visited[config] = current
        
        
    
    Configuration.IH.close()
    return None