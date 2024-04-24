import pickle

class Manager:
    def __init__(self) -> None:
        pass

    # Serialize the object
    # my_object = MyClass("example")
    # with open("serialized_object.pickle", "wb") as f:
    #     pickle.dump(my_object, f)

    # # Retrieve the serialized object
    # with open("serialized_object.pickle", "rb") as f:
    #     retrieved_object = pickle.load(f)

    @staticmethod
    def save(obj, name: str):
        with open(name, "wb") as file:
            pickle.dump(obj, file)

    @staticmethod
    def restore(name: str):
        loaded = None
        with open(name, "rb") as file:
            loaded = pickle.load(file)
        return loaded
        