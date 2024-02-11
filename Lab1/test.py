from Configuration import Configuration


def main():
    Configuration.generate_elevation(".\\testcases (1)\\testcases\stripWater\\mpp.txt")
    Configuration.generate_terrain(".\\testcases (1)\\testcases\\stripWater\\terrain.png")

    config1 = Configuration(0, 0, None, None)
    config2 = Configuration(0,0, config1, None)

    print(config1 == config2)

    theMap = {}

    theMap[config1] = 1
    theMap[config2] = 2

    print(theMap)


    return

main()