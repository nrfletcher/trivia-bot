import mysql.connector

""" SQL Database Interaction
    This is a MySQL relational database for storing user statistics and user server permissions amongst other things
    
    We have the ability to:
    * Add users, get user(s), update user information columns, get user specific data, as well as general data 
    
    notes:
        pip install mysql-connector-python
        create user 'user'@'host' identified with authentication_plugin by '272'; ~ otherwise drop plugin
        grant all privileges on *.* to 'user'@'host' with grant option;
        flush privileges (don't forget), now dc root use user """


def connection():
    try:
        db = mysql.connector.connect(user='riley272', password='272', host='localhost', database='trivia')
        cursor = db.cursor()
        print('success')
    except mysql.connector.Error as err:

        """ 1049 unknown database
            1045 access denied (typically wrong password or wrong user)
            2005 unknown SQL host (typically wrong, should be localhost) """

        print(err)
    else:
        print('done')
        cursor.close()
        db.close()


''' Initial adding of a user to the db, occurs when they first answer a question '''


def add_user_to_db(user_name, discord_id):
    try:
        # user_id is auto incremented
        db = mysql.connector.connect(user='riley272', password='272', host='localhost', database='trivia')
        cursor = db.cursor()
        add_user = ("INSERT INTO user(name, discord_id) values('" + user_name + "','" + discord_id + "');")
        cursor.execute(add_user)
        # autocommit for innodb
        db.commit()

    except mysql.connector.Error as err:
        print(err)
    else:
        cursor.close()
        db.close()


''' Retrieves all users in our database
    We do not add users to our db for joining, but for answering questions so only users who have answered
    a question will be in our db '''


def get_users():
    try:
        db = mysql.connector.connect(user='riley272', password='272', host='localhost', database='trivia')
        cursor = db.cursor()
        query = ("SELECT name, user_id, discord_id FROM user;")
        cursor.execute(query)
        for (name, user_id, discord_id) in cursor:
            print(name + ' ' + str(user_id) + ' ' + discord_id)

    except mysql.connector.Error as err:
        print(err)
    else:
        cursor.close()
        db.close()


''' Gets all user data via discord ID '''


def get_user(discord_id, name):
    try:
        db = mysql.connector.connect(user='riley272', password='272', host='localhost', database='trivia')
        cursor = db.cursor()

        query = ("SELECT user_id from user where discord_id = '" + discord_id + "' and name = '" + name + "';")
        cursor.execute(query)
        for (user_id) in cursor:
            # user_id is a tuple, so we take the id ([0]) and then cast back to str since id is an int in db
            return 'id: ' + str(user_id[0])

    except mysql.connector.Error as err:
        print(err)
    else:
        cursor.close()
        db.close()


''' Applicable to all genres: increases users genre count for answers '''


def update_all_columns(username, discord_id, category):
    try:
        # this all works under the assumption the user exists which should be checked prior
        db = mysql.connector.connect(user='riley272', password='272', host='localhost', database='trivia')
        cursor = db.cursor()
        s = get_user(discord_id, username).split(' ')
        user_id = int(s[1])

        query = ("SELECT questionsanswered FROM user WHERE user_id = " + str(user_id) + ';')
        cursor.execute(query)
        questionsansweredcount = None
        for (questionsanswered) in cursor:
            questionsansweredcount = questionsanswered[0]

        if questionsansweredcount:
            # if value is already present
            present = ("UPDATE user SET questionsanswered = questionsanswered + 1 WHERE user_id = " + str(
                user_id) + ';')
            cursor.execute(present)
            # have to commit any UPDATE commands otherwise won't take effect (this doesn't appear to matter in shell)
            cursor.execute('COMMIT')
        else:
            # we set our initial value to 1
            initialize = ("UPDATE user SET questionsanswered = 1 WHERE user_id = " + str(user_id) + ';')
            cursor.execute(initialize)
            cursor.execute('COMMIT')

        match category:
            case 'Science: Mathematics':
                c_query = ("SELECT math FROM user WHERE user_id = " + str(user_id) + ';')
                cursor.execute(c_query)
                math = None
                for (math) in cursor:
                    math = math[0]

                if math:
                    c_present = ("UPDATE user SET math = math + 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_present)
                    cursor.execute('COMMIT')
                else:
                    c_initialize = ("UPDATE user SET math = 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_initialize)
                    cursor.execute('COMMIT')
            case 'Science: Computers':
                c_query = ("SELECT computers FROM user WHERE user_id = " + str(user_id) + ';')
                cursor.execute(c_query)
                computers = None
                for (computers) in cursor:
                    computers = computers[0]

                if computers:
                    c_present = ("UPDATE user SET computers = computers + 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_present)
                    cursor.execute('COMMIT')
                else:
                    c_initialize = ("UPDATE user SET computers = 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_initialize)
                    cursor.execute('COMMIT')
            case 'Entertainment: Film':
                c_query = ("SELECT film FROM user WHERE user_id = " + str(user_id) + ';')
                cursor.execute(c_query)
                film = None
                for (film) in cursor:
                    film = film[0]

                if film:
                    c_present = ("UPDATE user SET film = film + 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_present)
                    cursor.execute('COMMIT')
                else:
                    c_initialize = ("UPDATE user SET film = 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_initialize)
                    cursor.execute('COMMIT')
            case 'Entertainment: Music':
                c_query = ("SELECT music FROM user WHERE user_id = " + str(user_id) + ';')
                cursor.execute(c_query)
                music = None
                for (music) in cursor:
                    music = music[0]

                if music:
                    c_present = ("UPDATE user SET music = music + 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_present)
                    cursor.execute('COMMIT')
                else:
                    c_initialize = ("UPDATE user SET music = 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_initialize)
                    cursor.execute('COMMIT')
            case 'Entertainment: Video Games':
                c_query = ("SELECT videogames FROM user WHERE user_id = " + str(user_id) + ';')
                cursor.execute(c_query)
                videogames = None
                for (videogames) in cursor:
                    videogames = videogames[0]

                if videogames:
                    c_present = ("UPDATE user SET videogames = videogames + 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_present)
                    cursor.execute('COMMIT')
                else:
                    c_initialize = ("UPDATE user SET videogames = 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_initialize)
                    cursor.execute('COMMIT')
            case 'Entertainment: Television':
                c_query = ("SELECT television FROM user WHERE user_id = " + str(user_id) + ';')
                cursor.execute(c_query)
                television = None
                for (television) in cursor:
                    television = television[0]

                if television:
                    c_present = ("UPDATE user SET television = television + 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_present)
                    cursor.execute('COMMIT')
                else:
                    c_initialize = ("UPDATE user SET television = 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_initialize)
                    cursor.execute('COMMIT')
            case 'Sports':
                c_query = ("SELECT sports FROM user WHERE user_id = " + str(user_id) + ';')
                cursor.execute(c_query)
                sports = None
                for (sports) in cursor:
                    sports = sports[0]

                if sports:
                    c_present = ("UPDATE user SET sports = sports + 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_present)
                    cursor.execute('COMMIT')
                else:
                    c_initialize = ("UPDATE user SET sports = 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_initialize)
                    cursor.execute('COMMIT')
            case 'History':
                c_query = ("SELECT history FROM user WHERE user_id = " + str(user_id) + ';')
                cursor.execute(c_query)
                history = None
                for (history) in cursor:
                    history = history[0]

                if history:
                    c_present = ("UPDATE user SET history = history + 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_present)
                    cursor.execute('COMMIT')
                else:
                    c_initialize = ("UPDATE user SET history = 1 WHERE user_id = " + str(user_id) + ';')
                    cursor.execute(c_initialize)
                    cursor.execute('COMMIT')
            case other:
                pass

    except mysql.connector.Error as err:
        print(err)
    else:
        cursor.close()
        db.close()


''' Increase correct answers for a user count '''


def add_correct(username, discord_id):
    try:
        db = mysql.connector.connect(user='riley272', password='272', host='localhost', database='trivia')
        cursor = db.cursor()
        s = get_user(discord_id, username).split(' ')
        user_id = int(s[1])

        query = ("SELECT correctanswers FROM user WHERE user_id = " + str(user_id) + ';')
        cursor.execute(query)
        correctanswers = None
        for (questionsanswer) in cursor:
            correctanswers = questionsanswer[0]

        if correctanswers:
            # if value is already present
            present = ("UPDATE user SET correctanswers = correctanswers + 1 WHERE user_id = " + str(
                user_id) + ';')
            cursor.execute(present)
            # have to commit any UPDATE commands otherwise won't take effect (this doesn't appear to matter in shell)
            cursor.execute('COMMIT')
        else:
            # we set our initial value to 1
            initialize = ("UPDATE user SET correctanswers = 1 WHERE user_id = " + str(user_id) + ';')
            cursor.execute(initialize)
            cursor.execute('COMMIT')

    except mysql.connector.Error as err:
        print(err)
    else:
        cursor.close()
        db.close()


''' Update users point count for questions answered '''


def update_points(username, discord_id, points):
    try:
        db = mysql.connector.connect(user='riley272', password='272', host='localhost', database='trivia')
        cursor = db.cursor()
        s = get_user(discord_id, username).split(' ')
        user_id = int(s[1])

        query = ("SELECT points FROM user WHERE user_id = " + str(user_id) + ';')
        cursor.execute(query)
        user_points = None
        for (user_points) in cursor:
            user_points = user_points[0]

        if user_points:
            present = ("UPDATE user SET points = points + " + str(points) + " WHERE user_id = " + str(
                user_id) + ';')
            cursor.execute(present)
            cursor.execute('COMMIT')
        else:
            initialize = ("UPDATE user SET points = " + str(points) + " WHERE user_id = " + str(user_id) + ';')
            cursor.execute(initialize)
            cursor.execute('COMMIT')

    except mysql.connector.Error as err:
        print(err)
    else:
        cursor.close()
        db.close()


''' Generate the top (limit) users based off total questions answered correctly '''


def get_top_users(limit):
    try:
        db = mysql.connector.connect(user='riley272', password='272', host='localhost', database='trivia')
        cursor = db.cursor()

        query = ("SELECT name, points FROM user ORDER BY points DESC LIMIT " + str(limit) + ";")
        cursor.execute(query)
        top_users = None
        users_list = []
        points_list = []
        for (top_users) in cursor:
            users_list.append(top_users[0])
            points_list.append(top_users[1])

        cursor.close()
        db.close()
        return [users_list, points_list]

    except mysql.connector.Error as err:
        print(err)


''' Get the answer rate (correct/wrong) of a user via id '''


def answer_rate(name, discord_id):
    try:
        db = mysql.connector.connect(user='riley272', password='272', host='localhost', database='trivia')
        cursor = db.cursor(buffered=True)

        user_id = get_user(discord_id, name).split(' ')
        query = ("SELECT questionsanswered, correctanswers FROM user WHERE "
                 "user_id = " + str(user_id[1]) + ';')
        cursor.execute(query)
        values = []
        for (item) in cursor:
            values.append(item)

        answers = values[0][0]
        correct = values[0][1]

        cursor.close()
        db.close()
        return [answers, correct, round(correct / answers, 3) * 100]

    except mysql.connector.Error as err:
        print(err)


''' Get the specific favorite genre of any user via id '''


def favorite_genre(name, discord_id):
    try:
        db = mysql.connector.connect(user='riley272', password='272', host='localhost', database='trivia')
        cursor = db.cursor(buffered=True)

        user_id = get_user(discord_id, name).split(' ')
        query = ("SELECT computers, film, music, videogames, sports, history, television, math FROM user WHERE "
                 "user_id = " + str(user_id[1]) + ';')
        cursor.execute(query)
        values = []
        for (thing) in cursor:
            values.append(thing)
        numbers = values[0]
        highest = 0
        index = 0
        for i in range(len(numbers)):
            if numbers[i] is not None:
                if numbers[i] > highest:
                    highest = numbers[i]
                    index = i

        favorite = ''
        match index:
            case 0:
                favorite = 'computers'
            case 1:
                favorite = 'film'
            case 2:
                favorite = 'music'
            case 3:
                favorite = 'videogames'
            case 4:
                favorite = 'sports'
            case 5:
                favorite = 'history'
            case 6:
                favorite = 'television'
            case 7:
                favorite = 'math'
            case other:
                pass

        cursor.close()
        db.close()
        return favorite

    except mysql.connector.Error as err:
        print(err)
