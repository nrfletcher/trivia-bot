''' Helper function for converting JSON into proper text format
    When retrieving from API special characters don't appear to translate properly '''

def cleanup(string):
    new_string = string
    # Only instances seen so far
    if '&#039;' in string:
        new_string = new_string.replace('&#039;', '\'')
    if '&quot;' in string:
        new_string = new_string.replace('&quot;', '"')
    return new_string


def cleanup_test(string='&quot; empty space &#039;'):
    print('The movie &quot;The Lord of the Rings&quot; is one of the best ever made.')


def tests():
    print(cleanup('The movie &quot;The Lord of the Rings&quot; is one of the best ever made.'))
    print(cleanup('My name&#039;s Brad, how &#039;bout you?'))
    print(cleanup('Which of these languages was NOT included in the 2016 song &quot;Don&#039;t Mind&quot; by Kent Jones?'))
