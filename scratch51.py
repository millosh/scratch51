import discord
import random
import asyncio

qas = {
    "question1": "a1",
    "question2": "a2",
    "question3": "a3",
}

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

        if message.content.startswith('$quiz1'):
            no_correct = 0
            no_questions = len(list(qas.keys()))
            for question in qas:
                await message.channel.send(question)
                def is_correct(m):
                    return m.author == message.author
                answer = qas[question]
                try:
                    guess = await self.wait_for('message', check=is_correct, timeout=30.0)
                except asyncio.TimeoutError:
                    return await message.channel.send('No answer, no fun! You took too long...'.format(answer))
                if guess.content == answer:
                    no_correct += 1
            await message.channel.send("You answered correctly " + str(no_correct) + " questions of " + str(no_questions) + "!")

        if message.content.startswith('$help'):
            await message.channel.send("""$quiz(index) - Run a quiz you made.
Expect further commands here. The developer is busy with what commands there shall be.""")

client = MyClient()
client.run('OTY5MTkyNzc2MDI3NzU0NTA2.Ymp1HA.x9n4v_SfvLZC3Csc5Y7s21rvA3E')
