import unittest
import importers.txt_importer as txt
from tokenizer import tokenize

class TestImporters(unittest.TestCase):

    def test_test(self):
        """test test.txt file. handles issues of capitalization, contractions, and some punctuation."""
        text = txt.importer('test_files/test.txt')
        expected = [["hello", "this", "is", "a", "test", "file", "for", "my", "text", "importer"],
                    ["i", "don't", "really", "do", "a", "whole", "lot", "but", "hey"],
                    ["i", "exist"], []]
        actual = tokenize(text)
        self.assertEqual(expected, actual)

    def test_small(self):
        """test small.txt file"""
        text = txt.importer('test_files/small.txt')
        expected = [["this", "is"], ["a", "multiple", "line"], ["text", "file"], []]
        actual = tokenize(text)
        self.assertEqual(expected, actual)

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
                    ["welp", "that's", "about", "it"], []]
        actual = tokenize(text)
        self.assertEqual(expected, actual)

    def test_hyphens_and_nums(self):
        """test file hyphens_and_nums.txt. tests hyphens, numbers, and smart quotes"""
        text = txt.importer('test_files/hyphens_and_nums.txt')
        expected = [["co", "creators", "of", "ice", "cream", "are", "happy"],
                    ["some", "people", "buy", "cones", "a", "day", "and", "sales", "went", "up"],
                    ["23", "in", "the", "last", "45", "years", "this", "was"],
                    ["especially", "noticeable", "in", "2019", "yum"],
                    ["user", "littlesnowman", "88", "doesn't", "like", "the", "cold", "but", "he", "does", "like", "ice", "cream"],
                    ["quoth", "littlesnowman", "88", "it's", "almost", "as", "good", "as", "raspberries"],
                    ["i", "got", "99", "problems", "but", "ice", "cream", "aint", "one"]]  # no empty list at end because no blank newline at end
        actual = tokenize(text)
        self.assertEqual(expected, actual)

    def test_phone_nums(self):
        """test file phone_nums.txt. Tests phone numbers"""
        text = txt.importer('test_files/phone_nums.txt')
        expected = [["my", "phone", "number", "is", "000-123-4567"],
                    ["call", "800-222-1359", "for", "a", "surprise"],
                    ["congratulations", "call", "123.456.7890", "for", "your", "prize"],
                    ["the", "business", "card", "says", "800-555-1212x1234"], []]
        actual = tokenize(text)
        self.assertEqual(expected, actual)

    def test_emails(self):
        """test file emails.txt. Tests emails"""
        text = txt.importer('test_files/emails.txt')
        expected = [["sending", "a", "message", "to", "recipient@domain.com", "hope", "they", "receive", "it"],
                    ["my", "email", "is", "first_middle-last.@something.net", "did", "you", "hear", "that"],
                    ["i", "need", "email", "from", "2734-whoareyou@somewhere.org"], []]
        actual = tokenize(text)
        self.assertEqual(expected, actual)

    def test_urls(self):
        """test file urls.txt. Tests urls"""
        text = txt.importer('test_files/urls.txt')
        expected = [["website", "http://foo.com/blah_blah,", "fun"],
                    ["click", "on", "http://foo.com/blah_blah/-", "awesome"],
                    ["visit", "http://foo.com/blah_blah_(wikipedia)"],
                    ["http://foo.com/blah_blah_(wikipedia)_(again)"],
                    ["http://www.example.com/wpstyle/?p=364"],
                    ["https://www.example.com/foo/?bar=baz&inga=42&quux"],
                    ["http://userid:password@example.com:8080"],
                    ["http://userid:password@example.com:8080/"],
                    ["http://userid@example.com"],
                    ["http://userid@example.com/"],
                    ["http://userid@example.com:8080"],
                    ["http://userid@example.com:8080/"],
                    ["http://userid:password@example.com"],
                    ["http://userid:password@example.com/"],
                    ["http://142.42.1.1/"],
                    ["http://142.42.1.1:8080/"],
                    ["http://foo.com/blah_(wikipedia)#cite-1"],
                    ["http://foo.com/blah_(wikipedia)_blah#cite-1"],
                    ["http://foo.com/(something)?after=parens"],
                    ["http://code.google.com/events/#&product=browser"],
                    ["http://j.mp"],
                    ["ftp://foo.bar/baz"],
                    ["http://foo.bar/?q=test%20url-encoded%20stuff"],
                    ["http://-.~_!$&'()*+,;=:%40:80%2f::::::@example.com"],
                    ["http://1337.net"],
                    ["http://a.b-c.de"],
                    ["http://223.255.255.254"],
                    ["https://foo_bar.example.com/"], []]
        actual = tokenize(text)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()