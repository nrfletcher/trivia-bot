import mysql.connector

# pip install mysql-connector-python
# create user 'user'@'host' identified with authentication_plugin by '272'; ~ otherwise drop plugin
# grant all privileges on *.* to 'user'@'host' with grant option;
# flush privileges (don't forget), now dc root use user


def connection():
    try:
        db = mysql.connector.connect(user='riley272', password='272', host='localhost', database='trivia')
        cursor = db.cursor()
        print('success')
    except mysql.connector.Error as err:
        # 1049 unknown database
        # 1045 access denied (typically wrong password or wrong user)
        # 2005 unknown SQL host (typically wrong, should be localhost)
        print(err)
    else:
        print('done')
        cursor.close()
        db.close()


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
