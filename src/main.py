from trivia import random_question, get_question_response
import discord
from questions import cleanup

# Setting token for API interaction and setting our bot (client) permissions to Intents.all()
# Intents was changed in Discord API recently, changes functionality of permissions via developer panel
TOKEN = '...'
client = discord.Client(intents=discord.Intents.all())


# on_ready() is the default client event run on each initial startup of our bot instance
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


# Member join client event, can specify channel
@client.event
async def on_member_join(member):
    # This ID points to general chat guild ID
    channel = client.get_channel(1020438015031660617)
    name = member.display_name
    joined = member.joined_at
    await channel.send('Welcome ' + name + ', you joined the server on ' + str(joined))
    return


# Any messages received from our client
@client.event
async def on_message(message):
    # Let's set variables for important data here
    # Avoid chaos later, ignore Discord IDs under the assumption that multiple users will not have the same name
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    # Log information (internal)
    print(f'{username}: {user_message} ({channel})')

    # We do not want to interact with our own bot messages, this prevents any chance of infinite loops
    if message.author == client.user:
        return

    # Our function for handling the retrieval of a randomized or specified trivia question
    async def get_question():
        # Will return a hashmap (dict) of question, choices, and correct answer
        question = get_question_response(user_message.lower())
        # Separate dictionary values for readability
        prompted_question = question['question']
        choices = question['choices']
        answer = question['answer']
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
            return ['correct', answer_normal]
        else:
            return ['false', answer_normal]

    # All messages received in general chat (ID does not correlate to channel.name directly)
    if message.channel.name == 'general':
        if user_message.lower() == '!hello':
            await message.channel.send(f'Hello {username}!')
            return

        elif user_message.lower() == '!bye':
            await message.channel.send(f'See you later {username}!')

        # Functionality testing
        elif user_message.lower() == '!random':
            response = f'This is a random number: {random_question.randrange(1000000)}'
            await message.channel.send(response)
            return

        # If we get a question request get an answer and return value from get_question
        # Check correctness and use embed for response
        elif '!question' in user_message.lower():
            answer_data = await get_question()
            response = answer_data[0]
            correct_answer = answer_data[1]

            if response == 'correct':
                embed = discord.Embed(title='Correct answer!', color=discord.Color.green())
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title='Wrong answer!',
                                      description='Sorry, the correct answer is ' + correct_answer,
                                      color=discord.Color.red())
                await message.channel.send(embed=embed)

            return

    # Testing guild channel exclusivity (shouldn't matter?)
    if user_message.lower() == '!anywhere':
        await message.channel.send('This can be used anywhere')
        return

# Runs bot
client.run(TOKEN)

