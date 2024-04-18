class DataManager:
    TEMPLATE = ["the", "be", "to", "of", "and", 
                "de/het", "een", "en", "zjin", "van", 
                "Accents?", "formal"]
    
    TEMPLATE2 = ["Accents?", "formal", "e >= n", "e most common", ]
    

    def convertData(self, data: bool) -> str:
        return "True" if data else "False"
    
    
    def contains(self, sent: str, wrd: str) -> bool:
        return sent.split().count(wrd) >= 1
    
    
    def getContent(self, filename: str) -> list[str]:
        content = []

        with open(filename, "r", encoding="utf8") as file:
            for line in file.readlines():
                result = line[:2]
                line = line[3:]
                line = line.strip()

                lineContent = [
                    self.convertData(self.contains(line, "the")),
                    self.convertData(self.contains(line, "be")),
                    self.convertData(self.contains(line, "to")),
                    self.convertData(self.contains(line, "of")),
                    self.convertData(self.contains(line, "and")),
                    
                    self.convertData(self.contains(line, "de") or self.contains(line, "het")),
                    self.convertData(self.contains(line, "een")),
                    self.convertData(self.contains(line, "en")),
                    self.convertData(self.contains(line, "zjin")),
                    self.convertData(self.contains(line, "van")),

                    self.convertData(not(line.isascii())),

                    result
                ]

                content.append(" ".join(lineContent))

        return content
    