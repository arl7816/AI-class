from matplotlib import pyplot as plt
from DataPoint import Data

class Plotter:

    subplots = {}

    def __init__(self) -> None:
        self.subplots = {}

    def plot(self, trt: tuple, data: Data, color, legend="", marker=None, key=None, linestyle = None):
        if key == None:
            key = trt

        sub = plt.subplot(trt[0], trt[1], trt[2])
        self.subplots[key] = sub

        sub.plot(data.x, data.y, label=legend, color=color, marker=marker, linestyle = linestyle)
        return sub

    def scatter(self, trt: tuple, data: Data, color: str, legend="", marker=None, key=None):
        if key == None:
            key = trt
    
        sub = plt.subplot(trt[0], trt[1], trt[2])
        self.subplots[key] = sub

        sub.scatter(data.x, data.y, label=legend, color=color, marker=marker)
        return sub

    def bar(self, trt: tuple, data: Data, color, legend="", marker="o", key=None):
        if key == None:
            key = trt

        sub = plt.subplot(trt[0], trt[1], trt[2])
        self.subplots[key] = sub

        sub.bar(data.x, data.y, label=legend, color=color)
        return sub

    def set_labels(self, key: str, xlabel: str, ylabel: str, title: str):
        self.subplots[key].set_title(title)
        self.subplots[key].set_xlabel(xlabel)
        self.subplots[key].set_ylabel(ylabel)

    def show(self):
        plt.show()