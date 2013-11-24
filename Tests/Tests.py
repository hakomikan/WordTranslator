import unittest
import doctest

from WordTranslator import *
import WordTranslator

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(WordTranslator))
    return tests

class TestWordTranslator(unittest.TestCase):
    def setUp(self):
        pass

    def test_Basic(self):
        source = ["It", "BabyBed","AliceBed","Car","Sedan","Mimic"]
        replacing = {"It":"Display",
                     "Baby":"Alice",
                     "Car":"Sedan"}
        duplicatables = ["Sedan"]
        untranslations = ["Mimic"]
        replaced,duplicated,untranslated = TranslateWords(source,replacing,duplicatables,untranslations)

        self.assertEqual(replaced[source[0]], "Display")
        self.assertEqual(replaced[source[1]], "AliceBed")
        self.assertIn("Bed", untranslated)
        self.assertIn("AliceBed", duplicated)
        self.assertNotIn("Sedan", duplicated)
        self.assertNotIn("Mimic", untranslated)            

if __name__ == '__main__':
    unittest.main()
