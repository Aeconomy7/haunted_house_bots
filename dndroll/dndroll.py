# Work with Python 3.6
import random
import discord

BOT_PREFIX=("@dndroll","!dndroll","/dndroll")
TOKEN = 'NzIzMDA5NTE1MDI0NDE2Nzk0.XurbSg.u-F29WhncOs9I-jTH4SYkJxVv0A'

client = discord.Client()

@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return

#~~~~~~~~~~~~~~#
# Begin /hello #
#~~~~~~~~~~~~~~#
@client.command(
	name		= 'hello',
	description	= "Introduce yourself to the bot and learn a lil something",
	brief		= "Hi there, `dndroll`! :)",
	pass_context	= True)

async def hello(context):
	msg = 'Hello ' + context.message.author.mention + ', welcome to `dndroll`, type in the command `!dmdroll help` to learn more!  This bot is best used to roll to solve arguements'.format(message)
	await client.send_message(message.channel, msg)
#~~~~~~~~~~~~#
# Emd /hello #
#~~~~~~~~~~~~#

#~~~~~~~~~~~~~#
# Begin /roll #
#~~~~~~~~~~~~~#
@client.command(
	name		= 'roll',
	description	= "Roll a dice, any number of sides 1-199999!",
	brief		= "Rolls dice d1-d199999",
	pass_context	= True)

async def roll(context,*dice_args):
	dice_cmd	= format(len(args).join(args))
	# YOU ARE HERE

# print ready status
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

# list servers using bot
async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

client.loop.create_task(list_servers())
client.run(TOKEN)
