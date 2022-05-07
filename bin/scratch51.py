import discord, random, asyncio, json, re, sys

root_dir = ".."
bint_dir = "."
conf_dir = root_dir + "/config"
actions_fd = conf_dir + "/actions.json"
messages_fd = conf_dir + "/messages.org"

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        messages = re.split("^- ",open(messages_fd).read())[1:]
        for message in messages:
            trigger = message[0]
            content = message[1:]
            if message.content.startswith(trigger):
                await message.channel.send(content)

#        actions = json.load(actions.json)
#        if message.content.startswith('$quiz1'):
#            no_correct = 0
#            no_questions = len(list(qas.keys()))
#            for question in qas:
#                await message.channel.send(question)
#                def is_correct(m):
#                    return m.author == message.author
#                answer = qas[question]
#                try:
#                    guess = await self.wait_for('message', check=is_correct, timeout=30.0)
#                except asyncio.TimeoutError:
#                    return await message.channel.send('No answer, no fun! You took too long...'.format(answer))
#                if guess.content == answer:
#                    no_correct += 1
#            await message.channel.send("You answered correctly " + str(no_correct) + " questions of " + str(no_questions) + "!")
#
#        if message.content.startswith('$help'):

client = MyClient()
client.run(sys.argv[1])
