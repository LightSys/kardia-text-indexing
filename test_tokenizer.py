import unittest
import importers.txt_importer as txt
from tokenizer import tokenize

class TestImporters(unittest.TestCase):

    def test_test(self):
        """test test.txt file. handles issues of capitalization, contractions, and some punctuation."""
        text = txt.importer('test_files/test.txt')
        expected = [["hello", "test", "file", "text", "importer"],
                    ["really", "whole", "lot", "hey"],
                    ["exist"]]
        actual = tokenize(text)
        self.assertEqual(actual, expected)

    def test_small(self):
        """test small.txt file"""
        text = txt.importer('test_files/small.txt')
        expected = [["multiple", "line"], ["text", "file"]]
        actual = tokenize(text)
        self.assertEqual(actual, expected)

    def test_professional(self):
        """test Professional_Test_Txt.txt file"""
        text = txt.importer('test_files/Professional_Test_Txt.txt')
        expected = [["uwu"], ["quick", "brown", "fox", "jumped", "lazy", "dog"],
                    ["wonder", "would", "potentially", "break", "system"],
                    ["smiley", "face"],
                    ["gotta", "make"],
                    ["looooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["oooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["oooooooooooooooooooooooooooooooooooooooooooo"],
                    ["oooooooooooooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["oooooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["oooooooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["oooooooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["nnnnnnnnnnnnnnnnnnnnnnnnnnngggggggggggggggggggggg"],
                    ["gggggggggggggggggggggggggggggggggggggggggggggggggg"],
                    ["gggggggggggggggggggggggggggggggggggggggggggg"],
                    ["okay", "way", "woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["welp", "that's"]]
        actual = tokenize(text)
        self.assertEqual(actual, expected)

    def test_hyphens_and_nums(self):
        """test file hyphens_and_nums.txt. tests hyphens, numbers, and smart quotes"""
        text = txt.importer('test_files/hyphens_and_nums.txt')
        expected = [["co", "creators", "ice", "cream", "happy"],
                    ["people", "buy", "cones", "day", "sales", "went"],
                    ["23", "last", "45", "years"],
                    ["especially", "noticeable", "2019", "yum"],
                    ["user", "littlesnowman", "88", "like", "cold", "like", "ice", "cream"],
                    ["quoth", "littlesnowman", "88", "almost", "good", "raspberries"],
                    ["got", "99", "problems", "ice", "cream", "aint", "one"]]
        actual = tokenize(text)
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()