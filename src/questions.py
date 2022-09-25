# Convert nasty JSON-encoded text (or doubly encoded?) back to their proper text
# In hindsight this didn't need to be it's own file, probably

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


print(cleanup('The movie &quot;The Lord of the Rings&quot; is one of the best ever made.'))
print(cleanup('My name&#039;s Brad, how &#039;bout you?'))
print(cleanup('Which of these languages was NOT included in the 2016 song &quot;Don&#039;t Mind&quot; by Kent Jones?'))
