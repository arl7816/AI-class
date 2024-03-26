import unittest
from KnowledgeBase import KnowledgeBase


class TestProp(unittest.TestCase):
    def getFileName(self, test: str) -> str:
        return "Lab2/testcases (1)/prop/p" + test +".cnf"

    def test_p01(self):
        kb = KnowledgeBase(self.getFileName("01"))
        self.assertEqual(kb.isSat(), True)

    def test_p02(self):
        kb = KnowledgeBase(self.getFileName("02"))
        self.assertEqual(kb.isSat(), False)
    
    def test_p03(self):
        kb = KnowledgeBase(self.getFileName("03"))
        self.assertEqual(kb.isSat(), True)

    def test_p04(self):
        kb = KnowledgeBase(self.getFileName("04"))
        self.assertEqual(kb.isSat(), False)
    
    def test_p05(self):
        kb = KnowledgeBase(self.getFileName("05"))
        self.assertEqual(kb.isSat(), True)
    
    def test_p06(self):
        kb = KnowledgeBase(self.getFileName("06"))
        self.assertEqual(kb.isSat(), True)

    def test_p07(self):
        kb = KnowledgeBase(self.getFileName("07"))
        self.assertEqual(kb.isSat(), False)

    def test_p08(self):
        kb = KnowledgeBase(self.getFileName("08"))
        self.assertEqual(kb.isSat(), True)

    def test_p09(self):
        kb = KnowledgeBase(self.getFileName("09"))
        self.assertEqual(kb.isSat(), False)
    
    def test_p10(self):
        kb = KnowledgeBase(self.getFileName("10"))
        self.assertEqual(kb.isSat(), False)
    
    def test_p11(self):
        kb = KnowledgeBase(self.getFileName("11"))
        self.assertEqual(kb.isSat(), False)

    def test_p13(self):
        kb = KnowledgeBase(self.getFileName("13"))
        self.assertEqual(kb.isSat(), False)


if __name__ == "__main__":
    unittest.main()