from PIL import Image
import pathlib
from DataStructs import LinkedList

class Map:
    """
    Enumerator for all path types and their RGB values such that

    <type> : (int, int, int)
    """
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
    """
    Handles an image using the Pillow package
    """

    @staticmethod
    def checkPath(fileName: str) -> bool:
        """
        STATIC checks if a file path exists

        Args:
            fileName (str): the file path

        Returns:
            bool: true if the file path exists, false otherwise
        """
        return pathlib.Path(fileName).exists()

    @staticmethod
    def quickShow(fileName: str) -> None:
        """
        STATIC displays an image file

        Args:
            fileName (str): the file path to the image
        """
        with Image.open(pathlib.Path(fileName)) as img:
            img = img.convert("RGB")
            img.show()

    def __init__(self, fileName: str):
        """Creates an Image handler

        Args:
            fileName (str): the file path to the image
        """
        self.img = Image.open(pathlib.Path(fileName))
        self.img = self.img.convert("RGB")

    def constructPath(self, path: LinkedList) -> None:
        """
        Draws a path onto a given image

        NOTE: this does not change the orginal image, you must save the image afterward

        Args:
            path (LinkedList[Configuration]): a list of nodes to draw on the image 
        """
        pixels = self.img.load()

        current = path.head
        while current is not None:
            pixels[current.data.row, current.data.col] = Map.PATH_COLOR
            current = current.next

    def saveImg(self, fileName: str) -> None:
        """
        Saves the image to another file path

        Pre:
            the image has been changed in some way

        Post:
            the image in saved. If the file already exist, then it overrides it, otherwise, creates it

        Args:
            fileName (str): the file path for the image to be saved to
        """
        self.img.save(fileName)

    def getWidth(self) -> int:
        """Gets the width of the image

        Returns:
            int: the width of the image in pixels
        """
        return self.img.size[0]

    def getHeight(self) -> int:
        """Gets the height of the image

        Returns:
            int: the height of the image in pixels
        """
        return self.img.size[1]
    
    def getPixel(self, row: int, col: int) -> tuple[int, int, int]:
        """Gets the RGB value of the pixel

        Args:
            row (int): the y coordinate of the pixel
            col (int): the x coordinate of the pixel

        Returns:
            tuple[int, int, int]: the RGB representation of the pixel color
        """
        return self.img.load()[row,col]

    def showImg(self):
        """Displays the image
        """
        self.img.show()
    
    def close(self):
        """Closes the file

        Pre:
            the file is open
        Post:
            the file is closed
        """
        self.img.close()