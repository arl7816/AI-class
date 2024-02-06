from imageHandler import ImageHandler as IH
from PathFinder import find_path
from Configuration import Configuration

import heapq

def main() -> None:
    path = "Lab1\\examples\\brown-out.png"
    path2 = "Lab1\\examples\\brown-out-2.png"

    for config in find_path((168, 236), (178, 222), "Lab1\\examples\\terrain.txt", path):
        print(config)
    



    return 

if __name__ == "__main__":
    main()