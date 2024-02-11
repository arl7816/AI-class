from imageHandler import ImageHandler as IH
from PathFinder import find_path
from Configuration import Configuration
from DataStructs import LinkedList
from time import time
import heapq
import sys

def get_distance_for_path(paths: list[LinkedList]) -> int:
    total = 0
    for path in paths:
        total += path.get(path.size - 1).distance
    return total

def getLocals(file_name: str) -> list[int, int]:
    desired_locals = []
    with open(file_name, "r") as file:
        for line in file.readlines():
            local = line.split()
            desired_locals.append((int(local[0]), int(local[1])))
    return desired_locals

def generate_paths(locals: list[int, int], elevation_file: str, terrain_file: str, show = False) -> list[LinkedList]:
    paths = []
    for index in range(0, len(locals) - 1):
        paths.append(find_path(locals[index], locals[index+1], elevation_file, terrain_file, show))
    return paths

def draw_path(paths: list[LinkedList], terrain_file: str, output_file: str):
    img = IH(terrain_file)
    
    for found_path in paths:
        img.constructPath(found_path)
    
    img.saveImg(output_file)
    img.close()

def main() -> None:
    # terrain-image, elevation-file, path-file, output-image-filename.
    
    #file1, file2 = sys.argv[1], sys.argv[4]
    file1, file2 = "Lab1\\testcases (1)\\testcases\\stripElevation\\terrain.png", 'Lab1\\testcases (1)\\testcases\stripElevation\\terrainOut.png'

    img = IH(file1)

    desired_locals = getLocals('Lab1\\testcases (1)\\testcases\\stripElevation\\path.txt')
    #desired_locals = getLocals(sys.argv[3])

    #current = time()
    found_path = generate_paths(desired_locals, 'Lab1\\testcases (1)\\testcases\stripElevation\\mpp.txt', file1, False)
    #found_path = generate_paths(desired_locals, sys.argv[2], file1)
    #print("Time: " + str(time() - current) + "s")
    
    draw_path(found_path, file1, file2)

    print(get_distance_for_path(found_path))

    #print("Serp", get_distance_for_path(found_path))

    return 

if __name__ == "__main__":
    main()