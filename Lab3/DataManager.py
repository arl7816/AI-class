from math import log1p, e, pow
from collections import Counter

class DataManager:
    #TEMPLATE = ["the", "be", "to", "of", "and", 
                #"de/het", "een", "en", "zjin", "van", 
                #"Accents?", "formal"]
    
    TEMPLATE = ["Accents?", 
                "formal > 0.25", "formal > .5", 'formal > .75' ,
                 "e common", "t common", "a common", "o common", "i common",
                 "avg < 5", "5 <= avg < 10", "avg >= 10"]

    

    def convertData(self, data: bool) -> str:
        return "True" if data else "False"
    
    def convertDataAry(self, data: list[bool], result: any) -> list[str]:
        lst = [self.convertData(element) for element in data]
        lst.append(result)
        return lst
    
    def contains(self, sent: str, wrd: str) -> bool:
        return sent.split().count(wrd) >= 1
    
    def mostCommon(self, line: str) -> str:
        res = Counter(line.lower())
        return str(max(res, key=res.get))

    def formal(self, line: str) -> float:
        result = 0

        result += line.count(".") * .5

        result += line.count(",") * 1

        result += line.count(";") * 4

        result += line.count(":") * 4

        result += line.count("'") * 4

        result += line.count("(") * .25
        result += line.count(")") * .25

        result = 1 / (1 + pow(e, -log1p(result)))

        return result
    
    def avgWordLen(self, line: str) -> float:
        lst = [len(wrd) for wrd in line.split()]
        return sum(lst) / len(lst)

    def getContent(self, filename: str) -> list[str]:
        content = []

        with open(filename, "r", encoding="utf8") as file:
            for line in file.readlines():
                result = line[:2]
                line = line[3:]
                line = line.strip()

                lineContent = self.convertDataAry([
                    not(line.isascii()),

                    self.formal(line) > .25,

                    self.formal(line) > .5,

                    self.formal(line) > .75,

                    self.mostCommon(line) == "e",

                    self.mostCommon(line) == "t",

                    self.mostCommon(line) == "a",

                    self.mostCommon(line) == "o",

                    self.mostCommon(line) == "i",

                    self.avgWordLen(line) < 5,

                    self.avgWordLen(line) >= 5 and self.avgWordLen(line) < 10,

                    self.avgWordLen(line) >= 10

                ], result)


                content.append(" ".join(lineContent))

        return content
    