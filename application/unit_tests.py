import unittest
import analyzer
import scraper

class Test(unittest.TestCase):
    def set_up(self):
        print('Set up')
    
    def test_strip_punctuation(self):
        normal = 'hello, mr jackson.?!@#'
        after = ['h', 'e', 'l', 'l', 'o', '', '', 'm', 'r', '', 'j', 'a', 'c', 'k', 's', 'o', 'n', '', '', '', '', '']
        self.assertEqual(analyzer.strip_punctuation(normal), after)

    
    def test_get_recent_run(self):
        self.assertEqual(analyzer.get_recent_run('./test_data/'),'1568572639')

    def test_get_shops(self):
        key = scraper.get_key()
        shops = [{'count': '1', 'id': '21162039', 'name': 'SmartSVGDesigns', 'listings': '121', 'key': 'bvpvd0ns8aqk63229f9baz9u'},{'count': '2', 'id': '21159771', 'name': 'Roseobelle', 'listings': '32', 'key': 'bvpvd0ns8aqk63229f9baz9u'},{'count': '3', 'id': '21158587', 'name': 'GregorySvg', 'listings': '28', 'key': 'bvpvd0ns8aqk63229f9baz9u'},{'count': '4', 'id': '21155263', 'name': 'CathlenBalonArtSVG', 'listings': '28', 'key': 'bvpvd0ns8aqk63229f9baz9u'},{'count': '5', 'id': '21155083', 'name': 'DELLAJewelryDesigns', 'listings': '34', 'key': 'bvpvd0ns8aqk63229f9baz9u'},{'count': '6', 'id': '21155035', 'name': 'LittleGoblinGarments', 'listings': '27', 'key': 'bvpvd0ns8aqk63229f9baz9u'},{'count': '7', 'id': '21154863', 'name': 'HeArtsandDesign', 'listings': '30', 'key': 'bvpvd0ns8aqk63229f9baz9u'},{'count': '8', 'id': '21153881', 'name': 'BUNGKUSROKOK', 'listings': '27', 'key': 'bvpvd0ns8aqk63229f9baz9u'},{'count': '9', 'id': '21152823', 'name': 'TOEBROOTWORLD', 'listings': '29', 'key': 'bvpvd0ns8aqk63229f9baz9u'},{'count': '10', 'id': '21152773', 'name': 'ArtesianHandcraft', 'listings': '58', 'key': 'bvpvd0ns8aqk63229f9baz9u'}]
        self.assertEqual(analyzer.get_shops('1568572639',key,'./test_data/'), shops)

    def test_get_unique_words(self):
        lcl_set = set()
        lcl_list = ['how', 'friend', 'helo', 'today', 'you', 'hello', 'are', 'heLlo', 'Hello']
        for item in lcl_list:
            lcl_set.add(item)
        test_list = ['Hello','Hello','hello','hello','heLlo','helo','friend','how','are','you','today']
        self.assertEqual(analyzer.get_unique_words(test_list),lcl_set)


    def test_filter_gram(self):
        lcl_gram = [{'word': 'snake', 'count': 849},{'word': 'bird', 'count': 80},{'word': 'lion', 'count': 300},{'word': 'tiger', 'count': 200},{'word': 'cat', 'count': 249},{'word': 'dog', 'count': 149},{'word': 'and', 'count': 549},{'word': 'taco', 'count': 100}]
        expected = [{'word': 'snake', 'count': 849}, {'word': 'lion', 'count': 300}, {'word': 'cat', 'count': 249}, {'word': 'tiger', 'count': 200}, {'word': 'dog', 'count': 149}]
        self.assertEqual(analyzer.filter_gram(lcl_gram), expected)


if __name__ == '__main__':
    unittest.main()