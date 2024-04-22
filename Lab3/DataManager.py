from math import log1p, e, pow
from collections import Counter

class DataManager:
    #TEMPLATE = ["the", "be", "to", "of", "and", 
                #"de/het", "een", "en", "zjin", "van", 
                #"Accents?", "formal"]
    
    TEMPLATE = ["Accents?", 
                "formal > 0.25", "formal > .5", 'formal > .75' ,
                 "e common", "t common", "a common", "o common", "i common",
                 "avg < 5", "5 <= avg < 10", "avg >= 10", 
                 
                 "e > 11", "v > 1", "th > 2", "ch > 2", "ng > 2",
                 "combo > 1",
                 "vowel freq (en) > .1", "conso freq (en) > 0.1"]

    

    def convertData(self, data: bool) -> str:
        return "True" if data else "False"
    
    def convertDataAry(self, data: list[bool], result: any) -> list[str]:
        lst = [self.convertData(element) for element in data]
        lst.append(result)
        return lst
    
    def countRepeats(self, line: str) -> int:
        lowerLine = line.lower()
        alp = [chr(i) + chr(i) for i in range(ord("a"), ord("z") + 1)]
        count = 0
        for combo in alp:
            if combo in lowerLine:
                count += 1
        return count
    
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
    
    def calculateVowelConsonantFrequencies(self, text, language):
        vowels = language # Define vowels for the language
        consonants = set('bcdfghjklmnpqrstvwxyz')  # Define consonants for the language

        # Initialize counts
        vowel_count = 0
        consonant_count = 0
        total_characters = 0

        # Count vowels and consonants
        for char in text:
            if char.lower() in vowels:
                vowel_count += 1
            elif char.lower() in consonants:
                consonant_count += 1
            total_characters += 1

        # Normalize frequencies
        if total_characters > 0:
            vowel_frequency = vowel_count / total_characters
            consonant_frequency = consonant_count / total_characters
        else:
            vowel_frequency = 0
            consonant_frequency = 0

        return vowel_frequency, consonant_frequency

    def getContent(self, filename: str) -> list[str]:
        content = []

        with open(filename, "r", encoding="utf8") as file:
            for line in file.readlines():
                result = line[:2]
                line = line[3:]
                line = line.strip()

                common = self.mostCommon(line)

                englishVowels = {'a', 'e', 'i', 'o', 'u'}
                dutch_vowels = {'a', 'e', 'i', 'o', 'u', 'y'}

                lineContent = self.convertDataAry([
                    not(line.isascii()),

                    self.formal(line) > .25,

                    self.formal(line) > .5,

                    self.formal(line) > .75,

                    common == "e",

                    common == "t",

                    common == "a",

                    common == "o",

                    common == "i",

                    self.avgWordLen(line) < 5,

                    self.avgWordLen(line) >= 5 and self.avgWordLen(line) < 10,

                    self.avgWordLen(line) >= 10,

                    line.lower().count("e") > 11,

                    line.lower().count("v") > 1,

                    line.lower().count("th") > 2,

                    line.lower().count("ch") > 2,

                    line.lower().count("ng") > 2,

                    self.countRepeats(line) > 1,

                    self.calculateVowelConsonantFrequencies(line, englishVowels)[0] > 0.3,

                    self.calculateVowelConsonantFrequencies(line, englishVowels)[1] > 0.3

                ], result)


                content.append(" ".join(lineContent))

        return content
    