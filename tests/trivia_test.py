import unittest

''' Ensuring that our string corrections work as expected
    Due to the API call format special characters do not come through properly 
    '''


class Question:
    def __init__(self, string):
        self.string = string


def cleanup(string):
    new_string = string
    if '&#039;' in string:
        new_string = new_string.replace('&#039;', '\'')
    if '&quot;' in string:
        new_string = new_string.replace('&quot;', '"')
    return new_string


class TestQuestion(unittest.TestCase):

    def test_quote(self):
        question = Question('The movie &quot;The Lord of the Rings&quot; is one of the best ever made.')
        question = cleanup(question)
        expected = 'The movie "The Lord of the Rings" is one of the best ever made.'
        error = 'These do not match'
        self.assertEqual(question, expected, error)

    def test_apostrophe(self):
        question = Question('My name&#039;s Brad, how &#039;bout you?')
        question = cleanup(question)
        expected = 'My name\'s Brad, how \'bout you?'
        error = 'These do not match'
        self.assertEqual(question, expected, error)

    def test_both_params(self):
        question = Question(
            'Which of these languages was NOT included in the 2016 song &quot;Don&#039;t Mind&quot; by Kent Jones?')
        question = cleanup(question)
        expected = 'My name\'s Brad, how \'bout you?'
        error = 'These do not match'
        self.assertEqual(question, expected, error)


unittest.main()
