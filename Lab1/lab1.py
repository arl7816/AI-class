from imageHandler import ImageHandler as IH
from PathFinder import find_path
from Configuration import Configuration
from DataStructs import LinkedList
from time import time
import heapq

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

def generate_paths(locals: list[int, int], elevation_file: str, terrain_file: str) -> list[LinkedList]:
    paths = []
    for index in range(0, len(locals) - 1):
        paths.append(find_path(locals[index], locals[index+1], elevation_file, terrain_file, False))
        print("Found a path")
    return paths

def draw_path(paths: list[LinkedList], terrain_file: str, output_file: str):
    img = IH(terrain_file)
    
    for found_path in paths:
        img.constructPath(found_path)
    
    img.saveImg(output_file)
    img.close()

def main() -> None:
    file1 = "Lab1\\examples\\brown-out.png"
    file2 = "Lab1\\examples\\brown-out-2.png"

    img = IH(file1)

    print(img.getPixel(230, 327))
    print(img.getPixel(276, 279))

    desired_locals = getLocals("Lab1\\examples\\complexPath.txt")
    print(desired_locals)

    current = time()
    found_path = generate_paths(desired_locals, "Lab1\\examples\\terrain.txt", file1)
    print("Time: " + str(time() - current) + "s")
    
    draw_path(found_path, file1, file2)

    print(get_distance_for_path(found_path))

    return 

if __name__ == "__main__":
    main()