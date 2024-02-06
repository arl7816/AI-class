from imageHandler import ImageHandler as IH
from PathFinder import find_path
from Configuration import Configuration

import heapq

def main() -> None:
    path = "Lab1\\examples\\brown-out.png"
    path2 = "Lab1\\examples\\brown-out-2.png"

    Configuration.generate_elevation("Lab1\\examples\\terrain.txt")

    print(len(Configuration.elevations[0]))
    
    



    return 

if __name__ == "__main__":
    main()