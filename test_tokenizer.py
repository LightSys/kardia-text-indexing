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
        self.assertEqual(expected, actual)

    def test_small(self):
        """test small.txt file"""
        text = txt.importer('test_files/small.txt')
        expected = [["multiple", "line"], ["text", "file"]]
        actual = tokenize(text)
        self.assertEqual(expected, actual)

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
        self.assertEqual(expected, actual)

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
        self.assertEqual(expected, actual)

    def test_phone_nums(self):
        """test file phone_nums.txt. Tests phone numbers"""
        text = txt.importer('test_files/phone_nums.txt')
        expected = [["phone", "number", "000-123-4567"],
                    ["call", "800-222-1359", "surprise"],
                    ["congratulations", "call", "123.456.7890", "prize"],
                    ["business", "card", "says", "800-555-1212x1234"]]
        actual = tokenize(text)
        self.assertEqual(expected, actual)

    def test_emails(self):
        """test file emails.txt. Tests emails"""
        text = txt.importer('test_files/emails.txt')
        expected = [["sending", "message", "recipient@domain.com", "hope", "receive"],
                    ["email", "first_middle-last.@something.net", "hear"],
                    ["need", "email", "2734-whoareyou@somewhere.org"]]
        actual = tokenize(text)
        self.assertEqual(expected, actual)

    def test_urls(self):
        """test file urls.txt. Tests urls"""
        text = txt.importer('test_files/urls.txt')
        expected = [["website", "http://foo.com/blah_blah,", "fun"],
                    ["click", "http://foo.com/blah_blah/-", "awesome"],
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
                    ["https://foo_bar.example.com/"]]
        actual = tokenize(text)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()