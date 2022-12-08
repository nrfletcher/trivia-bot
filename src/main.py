import datetime

from trivia import random_question, get_question_response
import discord
from questions import cleanup
from database import *

''' Main program for our Discord bot
    Will handle all direct interaction with user commands and comments '''


''' Setting token for API interaction and setting our bot (client) permissions to Intents.all()
    Intents was changed in Discord API recently, changes functionality of permissions via developer panel '''
TOKEN = 'MTAyMDQzNzM4OTA0NDM1OTE3OA.GGSTcL.TXLZJ2QTzhLQ1Dl1N7uTyPXDyvXei64ClwRdvs'
client = discord.Client(intents=discord.Intents.all())


''' Runs for every initial instantiation of our Discord bot to the server (i.e. on startup) '''
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


''' Occurs for every initial joining to the server of some member '''
@client.event
async def on_member_join(member):
    # This ID points to general chat guild ID
    channel = client.get_channel(1020438015031660617)
    name = member.display_name
    joined = member.joined_at
    await channel.send('Welcome ' + name + ', you joined the server on ' + str(joined))
    return


''' Our base function for receiving messages and interacting with them '''
@client.event
async def on_message(message):
    ''' Let's set variables for important data here
        Avoid chaos later, ignore Discord IDs under the assumption that multiple users will not have the same name '''
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
        # Log information (internal)
    print(f'{username}: {user_message} ({channel})')
    with open('docs/logs.txt', 'w') as f:
        now = datetime.datetime.now()
        f.write(f'{username}: {user_message} ({channel})' + ' ' + str(now))

        # We do not want to interact with our own bot messages, this prevents any chance of infinite loops
    if message.author == client.user:
        return

    async def get_user_id():
        return message.author.id

    ''' Retrieves a question for the user to interact with '''
    async def get_question():
        # Will return a hashmap (dict) of question, choices, and correct answer
        question = get_question_response(user_message.lower())
        # Separate dictionary values for readability
        prompted_question = question['question']
        choices = question['choices']
        answer = question['answer']
        q_category = question['category']
        q_difficulty = question['difficulty']
        prompted_question = cleanup(prompted_question)
        string_answer = answer.lower()
        answer_normal = answer

        choices_lower = []
        for choice in choices:
            choices_lower.append(choice.lower())

        # We are going to use the ASCII values for our letter answers (A, B, C, etc.)
        # Allows for easier user-interaction and flexibility in response
        first_letter = 65
        letter_choices = []
        # Fill out our choices
        for i in range(len(choices)):
            letter_choices.append(chr(first_letter))
            first_letter += 1

        # Want to set our answer as the letter choice of the correct answer
        # These indexes will match, so we use our i value to track the right letter choice
        for i in range(len(choices)):
            if choices[i] == answer:
                answer = letter_choices[i]

        # Iterate through choices and append our letter choice
        counter = 0
        choices_as_string = 'Choices:\n'
        for i in range(len(choices)):
            if i == len(choices) - 1:
                choices_as_string += letter_choices[counter] + '. '
                choices_as_string += choices[i]
                continue
            choices_as_string += letter_choices[counter] + '. '
            choices_as_string += choices[i]
            choices_as_string += '\n'
            counter += 1

        # Embeds are visual fancies for Discord messages
        sembed = discord.Embed(title=prompted_question, description=choices_as_string, color=discord.Color.teal())
        await message.channel.send(embed=sembed)

        user_answer = ''
        answered = False
        while not answered:
            # Check for user answers, once we've received a 'valid' answer we can then check it for correctness
            # We can check for letter answers and text answers concurrently
            user_response = await client.wait_for('message')
            if user_response.content.upper() in letter_choices or user_response.content in choices_lower:
                user_answer = user_response.content.upper()
                break

        if user_answer == answer or user_answer.lower() == string_answer.lower():
            return ['correct', answer_normal, q_category, q_difficulty]
        else:
            return ['false', answer_normal, q_category, q_difficulty]

    # All messages received in general chat (ID does not correlate to channel.name directly)
    if message.channel.name == 'general':
        if user_message.lower() == '!hello':
            await message.channel.send(f'Hello {username}!')
            return

        elif user_message.lower() == '!bye':
            await message.channel.send(f'See you later {username}!')
            return

        elif user_message.lower() == '!id':
            user_id = await get_user_id()
            await message.channel.send(f'{username}: {user_id}')
            return

        # Functionality testing
        elif user_message.lower() == '!random':
            response = f'This is a random number: {random_question.randrange(1000000)}'
            await message.channel.send(response)
            return

        elif user_message.lower() == '!accuracy':
            vals = answer_rate(message.author.name, str(message.author.id))
            sembed = discord.Embed(title='Your question accuracy', description='You\'ve answered ' + str(vals[0])
                                   + ' questions, and gotten ' + str(vals[1]) + ' correct. That\'s an accuracy of '
                                   + str(vals[2]) + '%', color=discord.Color.purple())
            await message.channel.send(embed=sembed)
            return

        elif user_message.lower() == '!favorite':
            favorite = favorite_genre(message.author.name, str(message.author.id))
            sembed = discord.Embed(title='Your favorite genre is:', description=favorite, color=discord.Color.green())
            await message.channel.send(embed=sembed)
            return

        # Let users get leaderboard
        elif '!leaderboard top' in user_message.lower():
            if len(user_message) != 18:
                await message.channel.send('Not a valid command, the form should be \'!get top {number}\'')
                return
            else:
                values = get_top_users(user_message.lower()[17])
                points = ''
                for i in range(len(values[0])):
                    if i == 0:
                        points += ':first_place:' + ' '
                    elif i == 1:
                        points += ':second_place:' + ' '
                    elif i == 2:
                        points += ':third_place:' + ' '
                    else:
                        points += ' ' + str(i + 1) + ': '
                    points += (values[0][i] + ': ' + str(values[1][i])) + ' points'
                    if i > len(values[0]) - 1:
                        continue
                    else:
                        points += '\n'
                embed = discord.Embed(title='Top Trivia Geeks Ranked',
                                      description=points,
                                      color=discord.Color.gold())
                await message.channel.send(embed=embed)
                return

        # If we get a question request get an answer and return value from get_question
        # Check correctness and use embed for response
        elif '!question' in user_message.lower():
            answer_data = await get_question()
            response = answer_data[0]
            correct_answer = answer_data[1]
            category = answer_data[2]
            # use for data update
            difficulty = answer_data[3]
            # use for points
            points = 0
            if difficulty == 'easy':
                points = 1
            elif difficulty == 'medium':
                points = 3
            else:
                points = 5

            # call get_user to retrieve id, if we receive empty string we add user to database
            user_in_db = get_user(str(message.author.id), message.author.name)
            if user_in_db:
                # user exists already, update all info
                update_all_columns(message.author.name, str(message.author.id), category)
            else:
                # user doesn't exist, add to table and update info
                add_user_to_db(message.author.name, str(message.author.id))
                update_all_columns(message.author.name, str(message.author.id), category)

            if response == 'correct':
                add_correct(message.author.name, str(message.author.id))
                update_points(message.author.name, str(message.author.id), points)
                embed = discord.Embed(title='Correct answer!', color=discord.Color.green())
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title='Wrong answer!',
                                      description='Sorry, the correct answer is ' + correct_answer,
                                      color=discord.Color.red())
                await message.channel.send(embed=embed)

            return

    if message.channel.name == 'test-suite':
        if user_message.lower() == '!id_sql':
            # id_sql = await get_id_sql(message.author.name)
            userid = message.author.id
            username = message.author.name
            await message.channel.send(str(username) + ' ' + str(userid))
            return

        if '!add user' in user_message.lower():
            command = user_message.split(' ')
            user = command[2]
            userid = command[3]
            add_user_to_db(user, userid)
            await message.channel.send(f'Added {user} as {userid}')
            return

    ''' Non channel inclusive messages should be permitted in any channel within the server itself '''
    if user_message.lower() == '!anywhere':
        await message.channel.send('This can be used anywhere')
        return

''' Starts up our bot '''
client.run(TOKEN)
