import mysql.connector

''' Database interaction logic for admin GUI
    get_users() returns all users and their respective data 
    change_admin_rights() takes a user id (user) and a command (enable or disable)
    This allows an admin to change user permissions without having direct access to the database
    '''


def get_users():
    try:
        db = mysql.connector.connect(user='riley272', password='272', host='localhost', database='trivia')
        cursor = db.cursor()
        query = ("SELECT name, user_id, discord_id FROM user;")
        cursor.execute(query)

        users = []
        for (name, user_id, discord_id) in cursor:
            users.append([name, user_id, discord_id])

        cursor.close()
        db.close()
        return users

    except mysql.connector.Error as err:
        print(err)


def change_admin_rights(user, command):
    try:
        db = mysql.connector.connect(user='riley272', password='272', host='localhost', database='trivia')
        cursor = db.cursor()
        query = None

        if command == 'enable':
            query = ("UPDATE user SET admin = 1 WHERE user_id = " + str(user))
            cursor.execute(query)
        else:
            query = ("UPDATE user SET admin = 0 WHERE user_id = " + str(user) + ';')
            cursor.execute(query)

    except mysql.connector.Error as err:
        print(err)
    else:
        cursor.close()
        db.close()
