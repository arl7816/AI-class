#from Classes import Queue, LinkedList
import sys
from Configuration import Configuration
import heapq


def find_path(start: Configuration, goal: Configuration) -> list:
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
            #return construct_path(visited, start, goal)
            print("found")
            return

        for config in current.generate_neigh():
            if config not in visited:
                heapq.heappush(li, config)
                visited[config] = current
        
    return None