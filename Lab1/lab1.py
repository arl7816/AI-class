from imageHandler import ImageHandler as IH
from PathFinder import find_path
from DataStructs import LinkedList
import sys


def get_distance_for_path(paths: list[LinkedList]) -> int:
    """
    Gets the distance total distance from a list of paths 

    Args:
        paths (list[LinkedList[Configuration]]): A list of paths

    Returns:
        int: the total distance traveled
    """
    total = 0
    for path in paths:
        total += path.get(path.size - 1).distance
    return total

def getLocals(file_name: str) -> list[int, int]:
    """
    Gets the coordinates the user wants to get visit

    Args:
        file_name (str): the file containing the desired places to visit 

    Returns:
        list[tuple[int, int]]: a list of tuples containing the x and y 
        coordinates the user wishes to visit along the path
    """
    desired_locals = []
    with open(file_name, "r") as file:
        for line in file.readlines():
            local = line.split()
            desired_locals.append((int(local[0]), int(local[1])))
    return desired_locals

def generate_paths(locals: list[int, int], elevation_file: str, terrain_file: str, show = False) -> list[LinkedList]:
    """
    generates a path through a set of desired locations via an A* algorithim

    Args:
        locals (list[tuple[int, int]]): a list of tuples containting the x and y coordinates the user wishes to visit
        elevation_file (str): the file containing elevation data
        terrain_file (str): the file containing the image representing the image
        show (bool, optional): Display information about visited nodes during the search. Defaults to False. 

    Returns:
        list[LinkedList[Configuration]]: The collection of paths from each coordinate to the next
    """
    paths = []
    for index in range(0, len(locals) - 1):
        paths.append(find_path(locals[index], locals[index+1], elevation_file, terrain_file, show))
    return paths

def draw_path(paths: list[LinkedList], terrain_file: str, output_file: str):
    """
    Draws a collection of paths on an image

    Args:
        paths (list[LinkedList[Configuration]]): the collection of paths
        terrain_file (str): the starting image file
        output_file (str): file location of the desired image
    
    Post:
        If the output_file exists, it is overriden, otherwise, it gets created
    """
    img = IH(terrain_file)
    
    for found_path in paths:
        img.constructPath(found_path)
    
    img.saveImg(output_file)
    img.close()

def main() -> None:
    """
    Generates a path between points using A* using the command line prompts
    * terrain-image, elevation-file, path-file, output-image-filename.
    """

    file1, file2 = sys.argv[1], sys.argv[4]

    img = IH(file1)

    desired_locals = getLocals(sys.argv[3])

    found_path = generate_paths(desired_locals, sys.argv[2], file1)
    
    draw_path(found_path, file1, file2)

    print(get_distance_for_path(found_path))

    return 

if __name__ == "__main__":
    main()