from math import log1p, e, pow
from collections import Counter

class DataManager:
    """
    Manages the Data's conversions and parses for training both the adaboost and Dtree models
    """
    
    """
    Template used for representing the attributes of each input. 
    """
    TEMPLATE = ["Accents?", 
                "formal > 0.25", "formal > .5", 'formal > .75' ,
                 "e common", "t common", "a common", "o common", "i common",
                 "avg < 5", "5 <= avg < 10", "avg >= 10", 
                 
                 "v > 1", "th > 2",
                 "ij > 1", "sch > 1"
                 "combo > 1",
                 "vowel freq (en) > .3", "conso freq (en) > 0.3",
                 "t-ending >= .1", "t-ending >= .25", "t-ending >= 0.05"]

    

    def convertData(self, data: bool) -> str:
        """
        Converts a True or False statement to a string

        Args:
            data (bool): the boolean value

        Returns:
            str: either "True" or "False"
        """
        return "True" if data else "False"
    
    def convertDataAry(self, data: list[bool], result: any) -> list[str]:
        """
        converts all elements in an array of boolean to string true or falses
        in addition to the output

        Args:
            data (list[bool]): an array of boolean values
            result (any): the pos or neg output of the input array

        Returns:
            list[str]: an array that dt and ada can use to learn from
        """
        lst = [self.convertData(element) for element in data]
        lst.append(result)
        return lst
    
    def countRepeats(self, line: str) -> int:
        """
        Counts the number of repeats letters within the word 
        s.t aabbc = 2 due to aa and bb being repeated

        Args:
            line (str): the sentence

        Returns:
            int: the number of repeats
        """
        lowerLine = line.lower()
        alp = [chr(i) + chr(i) for i in range(ord("a"), ord("z") + 1)]
        count = 0
        for combo in alp:
            if combo in lowerLine:
                count += 1
        return count
    
    def contains(self, sent: str, wrd: str) -> bool:
        """checks if some given string is within another

        Args:
            sent (str): the senetence being checked
            wrd (str): the subset being checked for

        Returns:
            bool: true if wrd is within sent, false otherwise
        """
        return sent.split().count(wrd) >= 1
    
    def mostCommon(self, line: str) -> str:
        """gets the most common letter within a string

        Args:
            line (str): the sentence

        Returns:
            str: the most common character within the sentence
        """
        res = Counter(line.lower())
        return str(max(res, key=res.get))

    def formal(self, line: str) -> float:
        """
        Gets the level of formality for the sentence where certain characters have more weight than others. 
        For ex, a ',' has a weight of 1 while a ':' has a weight of 4

        Args:
            line (str): the sentence being checked

        Returns:
            float: a proportion between 0 and 1 (inclusive)
        """
        result = 0

        result += line.count(".") * .5

        result += line.count(",") * 1

        result += line.count(";") * 4

        result += line.count(":") * 4

        result += line.count("'") * 1

        result += line.count("(") * .25
        result += line.count(")") * .25

        result += line.count("!") * 2
        result += line.count("?") * 2

        result = 1 / (1 + pow(e, -log1p(result)))

        return result
    
    def avgWordLen(self, line: str) -> float:
        """gets the average word length within a given sentence

        Args:
            line (str): the sentence being checked

        Returns:
            float: the average length of the words
        """
        lst = [len(wrd) for wrd in line.split()]
        return sum(lst) / len(lst)
    
    def calculateVowelConsonantFrequencies(self, text: str, language: set[str]) -> tuple[float, float]: 
        """
        Gets the proportion of vowels and consonants for a given language within a sentence

        Args:
            text (str): the sentence being checked
            language (set[str]): the set of vowels for a given language

        Returns:
            float, float: the proportion of vowels and consonates. 
        """
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
    
    def getTProp(self, line: str) -> float:
        """gets the proportion of words ending in t's

        Args:
            line (str): the sentence

        Returns:
            float: the proportion of words ending in t's to total number of words
        """
        lst = line.split()
        return len(
            [wrd for wrd in lst if wrd.lower()[-1] == "t"]
        ) / len(lst)


    def parseLine(self, line: str, result: any) -> list[str]:
        """parses a line into a sequence of true or false statment for the models to train on. 

        Args:
            line (str): the sentence being parsed
            result (any): the output of the sentence

        Returns:
            list[str]: _description_
        """
        common = self.mostCommon(line)

        englishVowels = {'a', 'e', 'i', 'o', 'u'}
        dutch_vowels = {'a', 'e', 'i', 'o', 'u', 'y'}

        return self.convertDataAry([
                    not(line.isascii()),

                    self.formal(line) > .25,

                    .25 < self.formal(line) <= .5,

                    .5 < self.formal(line) > .75,

                    common == "e",

                    common == "t",

                    common == "a",

                    common == "o",

                    common == "i",

                    self.avgWordLen(line) < 5,

                    self.avgWordLen(line) >= 5 and self.avgWordLen(line) < 10,

                    self.avgWordLen(line) >= 10,

                    # line.lower().count("e") > 5,

                    line.lower().count("v") > 2,

                    line.lower().count("th") < 1,

                    # line.lower().count("ch") > 2,

                    # line.lower().count("ng") > 2,

                    line.lower().count("ij") < 1,

                    line.lower().count("sch") < 1,

                    line.lower().count("hein") < 1,

                    self.countRepeats(line) > 2,

                    self.calculateVowelConsonantFrequencies(line, englishVowels)[0] > 0.35,

                    # self.calculateVowelConsonantFrequencies(line, englishVowels)[1] > 0.4,

                    0.05 <= self.getTProp(line) < .10,

                    0.1 <= self.getTProp(line) < .25,

                    .25 <= self.getTProp(line) < .5

                ], result)

    def getContent(self, filename: str) -> list[str]:
        """
        Converts the set of data in a file into a seqeucne of attributes that a 
        model can train on. 

        Args:
            filename (str): the file containing the data

        Returns:
            list[str]: a list of attributes to train on
        """
        content = []

        with open(filename, "r", encoding="utf8") as file:
            for line in file.readlines():
                result = line[:2]
                line = line[3:]
                line = line.strip()

                lineContent = self.parseLine(line, result)


                content.append(" ".join(lineContent))

        return content
    