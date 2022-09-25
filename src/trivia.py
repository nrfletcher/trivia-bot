import requests

# API interaction takes place here
# Create an extensible way to add additional trivia questions later on
# Should do all the heavy lifting to reduce massive code blocks in main


def default_answer_no_url():

    # Code needed to make API GET request and format into a dictionary holding data
    response = requests.get("https://opentdb.com/api.php?amount=1&category=18&difficulty=hard&type=multiple")
    query = response.json()
    data = query['results'][0]

    # All possible return options for our query
    question = query['results'][0]['question']
    question_category = query['results'][0]['category']
    question_type = query['results'][0]['type']
    question_difficulty = query['results'][0]['difficulty']
    question_answer = query['results'][0]['correct_answer']
    incorrect_answers = query['results'][0]['incorrect_answers']

    # Confirm all information adds up (incorrect answers should be a list of strings)
    print(question)
    print(question_answer)
    print(question_difficulty)
    print(question_type)
    print(question_category)
    print(incorrect_answers)


def default_answer_url_provided(url):

    # Affirming that link is proper value
    if isinstance(url, str):

        # This repeats functionality of above with an url provided (should explain itself)
        response = requests.get(url)
        query = response.json()
        data = query['results'][0]

        # All return values
        question = query['results'][0]['question']
        question_category = query['results'][0]['category']
        question_type = query['results'][0]['type']
        question_difficulty = query['results'][0]['difficulty']
        question_answer = query['results'][0]['correct_answer']
        incorrect_answers = query['results'][0]['incorrect_answers']

        # Same functionality, maybe rewrite to not have redundant code (?) Come back later
        print(question)
        print(question_answer)
        print(question_difficulty)
        print(question_type)
        print(question_category)
        print(incorrect_answers)
    else:
        raise TypeError('This function requires a string url input')


def question_tolist(url):
    if isinstance(url, str):

        # List for now, consider going to hashmap implementation instead
        response = requests.get(url)
        query = response.json()
        data = query['results'][0]

        # Get trivia question and convert to a list for ease of access
        question = query['results'][0]['question']
        question_category = query['results'][0]['category']
        question_type = query['results'][0]['type']
        question_difficulty = query['results'][0]['difficulty']
        question_answer = query['results'][0]['correct_answer']
        incorrect_answers = query['results'][0]['incorrect_answers']
        return [question, question_category, question_type, question_difficulty, question_answer, incorrect_answers]
    else:
        raise TypeError('This function requires a string url input')


def get_question(url):
    if not isinstance(url, str):
        raise TypeError('This needs to be a string url')
    else:
        # Shortened, only need essential information for our main
        response = requests.get(url)
        query = response.json()
        question = query['results'][0]['question']
        question_answer = query['results'][0]['correct_answer']
        incorrect_answers = query['results'][0]['incorrect_answers']
        choices = incorrect_answers
        choices.append(question_answer)

        # Get our question more readable for our Discord API layer
        return {'question': question, 'answer': question_answer, 'choices': choices}


def random_question():
    return get_question("https://opentdb.com/api.php?amount=1")
    # Accesses a random difficulty random category question from OpenTDB


# Consider revisiting and implementing some sort of string manipulation algorithm instead
def category_and_difficulty(category, difficulty):

    # Match == switch like in Java
    match difficulty:
        case 'easy':
            match category:
                case 'math':
                    return get_question("https://opentdb.com/api.php?amount=1&category=19&difficulty=easy")
                case 'computers':
                    return get_question("https://opentdb.com/api.php?amount=1&category=18&difficulty=easy")
                case 'film':
                    return get_question("https://opentdb.com/api.php?amount=1&category=10&difficulty=easy")
                case 'music':
                    return get_question("https://opentdb.com/api.php?amount=1&category=12&difficulty=easy")
                case 'videogames':
                    return get_question("https://opentdb.com/api.php?amount=1&category=15&difficulty=easy")
                case 'sports':
                    return get_question("https://opentdb.com/api.php?amount=1&category=21&difficulty=easy")
                case 'history':
                    return get_question("https://opentdb.com/api.php?amount=1&category=23&difficulty=easy")
                case 'television':
                    return get_question("https://opentdb.com/api.php?amount=1&category=14&difficulty=easy")
                case _:
                    return random_question()
        # Splitting up based on difficulty first, should be more efficient than vice versa
        case 'medium':
            match category:
                case 'math':
                    return get_question("https://opentdb.com/api.php?amount=1&category=19&difficulty=medium")
                case 'computers':
                    return get_question("https://opentdb.com/api.php?amount=1&category=18&difficulty=medium")
                case 'film':
                    return get_question("https://opentdb.com/api.php?amount=1&category=10&difficulty=medium")
                case 'music':
                    return get_question("https://opentdb.com/api.php?amount=1&category=12&difficulty=medium")
                case 'videogames':
                    return get_question("https://opentdb.com/api.php?amount=1&category=15&difficulty=medium")
                case 'sports':
                    return get_question("https://opentdb.com/api.php?amount=1&category=21&difficulty=medium")
                case 'history':
                    return get_question("https://opentdb.com/api.php?amount=1&category=23&difficulty=medium")
                case 'television':
                    return get_question("https://opentdb.com/api.php?amount=1&category=14&difficulty=medium")
                case _:
                    return random_question()
        case 'hard':
            match category:
                case 'math':
                    return get_question("https://opentdb.com/api.php?amount=1&category=19&difficulty=hard")
                case 'computers':
                    return get_question("https://opentdb.com/api.php?amount=1&category=18&difficulty=hard")
                case 'film':
                    return get_question("https://opentdb.com/api.php?amount=1&category=10&difficulty=hard")
                case 'music':
                    return get_question("https://opentdb.com/api.php?amount=1&category=12&difficulty=hard")
                case 'videogames':
                    return get_question("https://opentdb.com/api.php?amount=1&category=15&difficulty=hard")
                case 'sports':
                    return get_question("https://opentdb.com/api.php?amount=1&category=21&difficulty=hard")
                case 'history':
                    return get_question("https://opentdb.com/api.php?amount=1&category=23&difficulty=hard")
                case 'television':
                    return get_question("https://opentdb.com/api.php?amount=1&category=14&difficulty=hard")
                case _:
                    return random_question()
        case _:
            return random_question()


# Only have a category parameter to fulfill
def only_category(category):
    match category:
        case 'math':
            return get_question("https://opentdb.com/api.php?amount=1&category=19")
        case 'computers':
            return get_question("https://opentdb.com/api.php?amount=1&category=18")
        case 'film':
            return get_question("https://opentdb.com/api.php?amount=1&category=10")
        case 'music':
            return get_question("https://opentdb.com/api.php?amount=1&category=12")
        case 'videogames':
            return get_question("https://opentdb.com/api.php?amount=1&category=15")
        case 'sports':
            return get_question("https://opentdb.com/api.php?amount=1&category=21")
        case 'history':
            return get_question("https://opentdb.com/api.php?amount=1&category=23")
        case 'television':
            return get_question("https://opentdb.com/api.php?amount=1&category=14")
        case _:
            return random_question()


# Only have a difficulty parameter to fulfill
def only_difficulty(difficulty):
    match difficulty:
        case 'easy':
            return get_question("https://opentdb.com/api.php?amount=1&difficulty=easy")
        case 'medium':
            return get_question("https://opentdb.com/api.php?amount=1&difficulty=medium")
        case 'hard':
            return get_question("https://opentdb.com/api.php?amount=1&difficulty=hard")
        case _:
            return random_question()


def get_question_response(request):
    # Our types provided (we can add more later but this seems sufficient for now)
    categories = ['random', 'math', 'computers', 'film', 'music', 'videogames', 'sports', 'history', 'television']
    difficulties = ['easy', 'medium', 'hard']

    # Use boolean for this?
    category = 'Not provided'
    difficulty = 'Not provided'
    question = ''
    choices = []

    
    for cat in categories:
        if cat in request:
            category = cat

    for dif in difficulties:
        if dif in request:
            difficulty = dif

    # May be redundant with loops? We can probably merge these? Revisit
    if category in categories and difficulty in difficulties:
        return category_and_difficulty(category, difficulty)
    elif category in categories:
        return only_category(category)
    elif difficulty in difficulties:
        return only_difficulty(difficulty)
    else:
        return random_question()




