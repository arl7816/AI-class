import pickle

class Manager:
    """Manages the saved version of the models
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    def save(obj: any, name: str) -> None:
        """saves the object

        Args:
            obj (any): the object being saved
            name (str): the name of the file it is being saved to
        """
        with open(name, "wb") as file:
            pickle.dump(obj, file)

    @staticmethod
    def restore(name: str) -> None:
        """retreives an object

        Args:
            name (str): the name of the file

        Returns:
            any: the object being requested
        """
        loaded = None
        with open(name, "rb") as file:
            loaded = pickle.load(file)
        return loaded
        