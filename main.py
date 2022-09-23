from trivia import random_question, get_question_response
import discord

TOKEN = 'n/a'
client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_member_join(member):
    # General chat
    channel = client.get_channel(1020438015031660617)
    name = member.display_name
    joined = member.joined_at
    await channel.send('Welcome ' + name + ', you joined the server on ' + str(joined))
    return


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    # Log information
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    if message.channel.name == 'general':
        if user_message.lower() == '!hello':
            await message.channel.send(f'Hello {username}!')
            return

        elif user_message.lower() == '!bye':
            await message.channel.send(f'See you later {username}')

        elif user_message.lower() == '!random':
            response = f'This is a random number: {random_question.randrange(1000000)}'
            await message.channel.send(response)
            return

        elif '!question' in user_message.lower():
            question = get_question_response(user_message.lower())
            prompted_question = question['question']
            choices = question['choices']
            answer = question['answer']
            choices_as_string = ''
            for i in range(len(choices)):
                if i == len(choices)-1:
                    choices_as_string += choices[i]
                    continue
                choices_as_string += choices[i]
                choices_as_string += ', '

            await message.channel.send('Question: ' + prompted_question + '\nOptions: ' + choices_as_string)

            await message.channel.send('Answer: ' + answer)
            return

    if user_message.lower() == '!anywhere':
        await message.channel.send('This can be used anywhere')
        return

client.run(TOKEN)

