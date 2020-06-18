# Work with Python 3.6
import random
import asyncio
import aiohttp
import json
import discord
from discord.ext import commands

BOT_PREFIX=("!dndbot ","/dndbot ")
TOKEN = 'XXXX'

bot = commands.Bot(command_prefix=BOT_PREFIX)

#@bot.event
#async def on_message(message):
	# we do not want the bot to reply to itself
#	if message.author == bot.user:
#		return

#~~~~~~~~~~~~~~#
# Begin /hello #
#~~~~~~~~~~~~~~#
@bot.command(name	= 'hello',
	description	= "Introduce yourself to the bot and learn a lil something",
	brief		= "Hi there, `dndbot`! :)",
	pass_context	= True)
#@bot.command(name='hello',pass_context=True)
async def hello_cmd(context):
	# print('Function called by ' + context.message.author)
	msg = 'Hello ' + context.message.author.mention + ', I am `dndbot`!  Type in the command `!dndbot help` to learn more!'
	# await bot.send_message(message.channel, msg)
	await bot.say(msg)
#~~~~~~~~~~~~#
# Emd /hello #
#~~~~~~~~~~~~#


#~~~~~~~~~~~~#
# Begin help #
#~~~~~~~~~~~~#
# Remove previous help command
bot.remove_command("help")

@bot.command(name 	= 'help',
	pass_context	= True)
async def help_cmd(context):
	msg	= ("```Usage: `!dndbot [cmd]` OR `/dndbot [cmd]`\n\n"
	"Available commands (`[cmd]`):\n"
	"\t`hello` : Say hello to `dndbot`!\n"
	"\t`roll`  : Roll a dice regularly (Ex: `!dndbot roll d20+2`)```")
	await bot.say(msg)
#~~~~~~~~~~~#
# End /help #
#~~~~~~~~~~~#


#~~~~~~~~~~~~~#
# Begin /roll #
#~~~~~~~~~~~~~#
@bot.command(name	= 'roll',
	description	= "Roll a dice, any number of sides 1-199999!",
	brief		= "Rolls dice d1-d199999",
	pass_context	= True)
async def roll_cmd(context,*dice_args):
	dice_roll = [' '.join(tups) for tups in dice_args]
	print(dice_roll)
	# dice_cmd	= format(len(dice_args).join(dice_args))
	# YOU ARE HERE
	# await bot.say(dice_cmd)
#~~~~~~~~~~~#
# End /roll #
#~~~~~~~~~~~#


# print ready status
@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')

# list servers using bot
#async def list_servers():
#    await bot.wait_until_ready()
#    while not bot.is_closed:
#        print("Current servers:")
#        for server in bot.servers:
#            print(server.name)
#        await asyncio.sleep(600)

#bot.loop.create_task(list_servers())

print("Running bot")
bot.run(TOKEN)
