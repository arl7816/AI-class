from PIL import Image
import io
import pathlib

class Map:
    PATH_COLOR = (118, 63, 231)
    OPEN_LAND = (248,148,18)
    ROUGH_MEADOW = (255,192,0)
    EASY_FOREST = (255,255,255)
    SLOW_FOREST = (2,208,60)
    WALK_FOREST = (2,136,40)
    IMPASSIBLE =  (5,73,24)
    WATER = (0,0,255)
    ROAD = (71,51,3)
    FOOTPATH = (0,0,0)
    OUT_OF_BOUNDS = (205,0,101)


class ImageHandler:
    @staticmethod
    def checkPath(fileName: str) -> bool:
        return pathlib.Path(fileName).exists()

    @staticmethod
    def quickShow(fileName: str) -> None:
        with Image.open(pathlib.Path(fileName)) as img:
            img = img.convert("RGB")
            img.show()

    def __init__(self, fileName: str):
        self.img = Image.open(pathlib.Path(fileName))
        self.img = self.img.convert("RGB")

    def constructPath(self, path: list[tuple]) -> None:
        pixels = self.img.load()

        for stop in path:
            pixels[stop[0], stop[1]] = Map.PATH_COLOR

    def saveImg(self, fileName: str) -> None:
        self.img.save(fileName)

    def getWidth(self) -> int:
        return self.img.size[0]

    def getHeight(self) -> int:
        return self.img.size[1]
    
    def getPixel(self, row: int, col: int) -> tuple[int, int, int]:
        return self.img.load()[row,col]

    def showImg(self):
        self.img.show()
    
    def close(self):
        self.img.close()