import requests


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
    if isinstance(url, str):
        response = requests.get(url)
        query = response.json()
        data = query['results'][0]

        question = query['results'][0]['question']
        question_category = query['results'][0]['category']
        question_type = query['results'][0]['type']
        question_difficulty = query['results'][0]['difficulty']
        question_answer = query['results'][0]['correct_answer']
        incorrect_answers = query['results'][0]['incorrect_answers']

        print(question)
        print(question_answer)
        print(question_difficulty)
        print(question_type)
        print(question_category)
        print(incorrect_answers)
    else:
        raise TypeError('This function requires a string url input')


default_answer_url_provided("https://opentdb.com/api.php?amount=1&category=11&difficulty=hard&type=multiple")
