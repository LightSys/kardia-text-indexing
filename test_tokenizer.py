import unittest
import importers.txt_importer as txt
from tokenizer import tokenize

class TestImporters(unittest.TestCase):

    def test_test(self):
        """test test.txt file. handles issues of capitalization, contractions, and some punctuation."""
        text = txt.importer('test_files/test.txt')
        expected = [["hello", "this", "is", "a", "test", "file", "for", "my", "text", "importer"],
                    ["i", "don't", "really", "do", "a", "whole", "lot", "but", "hey"],
                    ["i", "exist"],
                    []]  # because the last line of the file is empty
        actual = tokenize(text)
        self.assertEqual(actual, expected)

    def test_small(self):
        """test small.txt file"""
        text = txt.importer('test_files/small.txt')
        expected = [["this", "is"], ["a", "multiple", "line"], ["text", "file"], []]
        actual = tokenize(text)
        self.assertEqual(actual, expected)

    def test_professional(self):
        """test Professional_Test_Txt.txt file"""
        text = txt.importer('test_files/Professional_Test_Txt.txt')
        expected = [["uwu"], ["the", "quick", "brown", "fox", "jumped", "over", "the", "lazy", "dog"],
                    ["i", "wonder", "what", "would", "potentially", "break", "this", "system"],
                    ["how", "about", "a", "smiley", "face"],
                    ["other", "than", "that", "we", "just", "gotta", "make", "this"],
                    ["looooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["oooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["ooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["oooooooooooooooooooooooooooooooooooooooooooo"],
                    ["o"],
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
                    ["okay", "so", "what", "about", "this", "way", "woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"],
                    ["welp", "that's", "about", "it"],
                    []]
        actual = tokenize(text)
        self.assertEqual(actual, expected)

    def test_hyphens_and_nums(self):
        """test file hyphens_and_nums.txt. tests hyphens, numbers, and smart quotes"""
        text = txt.importer('test_files/hyphens_and_nums.txt')
        expected = [["co", "creators", "of", "ice", "cream", "are", "happy"],
                    ["some", "people", "buy", "cones", "a", "day", "and", "sales", "went", "up"],
                    ["23", "in", "the", "last", "45", "years", "this", "was"],
                    ["especially", "noticeable", "in", "2019", "yum"],
                    ["user", "littlesnowman", "88", "doesn't", "like", "the", "cold", "but", "he", "does", "like", "ice", "cream"],
                    ["quoth", "littlesnowman", "88", "it's", "almost", "as", "good", "as", "raspberries"],
                    ["i", "got", "99", "problems", "but", "ice", "cream", "aint", "one"]]
        actual = tokenize(text)
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()