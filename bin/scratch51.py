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

        msgs = re.split("(?:\n|^)- ",open(messages_fd).read())[1:]
        for msg in msgs:
            msg = msg.split("\n")
            trigger = msg[0]
            content = "\n".join(msg[1:])
            if message.content.startswith(trigger):
                await message.channel.send(content)

        # dictionary  "actions"
        actions = json.loads(open(actions_fd).read())
        for act in actions:
            action = actions[act]
            trigger = action['keyword']
            action_file = conf_dir + "/" + action['config']
            if message.content.startswith(trigger):
                if action['type'] == 'quiz':
                    # dictionary "quiz"
                    #qf = open(action_file).read()
                    quiz = json.loads(open(action_file).read())
                    questions = quiz['questions']
                    no_correct = 0
                    no_questions = len(list(questions.keys()))
                    no_points = 0
                    max_points = 0
                    for question in questions:
                        max_points += int(questions[question]['points'])
                    for question in questions:
                        await message.channel.send(question)
                        def is_correct(m):
                            return m.author == message.author
                        answer = questions[question]['answer']
                        try:
                            guess = await self.wait_for('message', check=is_correct, timeout=30.0)
                        except asyncio.TimeoutError:
                            return await message.channel.send('No answer, no fun! You took too long...'.format(answer))
                        if guess.content == answer:
                            no_correct += 1
                            no_points += int(questions[question]['points'])
                    await message.channel.send("You answered correctly " + str(no_correct) + " questions of " + str(no_questions) + " and " + str(no_points) + " points of maximum " + str(max_points) + "!")

client = MyClient()
client.run(sys.argv[1])
