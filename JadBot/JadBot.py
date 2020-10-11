# Work with Python 3.6
import requests
import pprint
from bs4 import BeautifulSoup
import urllib

from random import randint
from time import sleep

import asyncio
import aiocron
import aiohttp
import json

import discord
from discord.ext import commands

from db.jbotdb import JadDbHandler

#~~~~~~~~~~~~~~~~~~~#
# Initiate database #
#~~~~~~~~~~~~~~~~~~~#
JBOT_DB = CharDbHandler()
print("[+] Started main DB")
#~~~~~~~~~~~~~~#
# End database #
#~~~~~~~~~~~~~~#

BOT_PREFIX=("!osrs ", "/osrs ", "!jadbot ","/jadbot ","/")
TOKEN='XXXX'

bot = commands.Bot(command_prefix=BOT_PREFIX)
print("[+] Successfully attached bot!")

#~~~~~~~~~~~~~~~~~~~~~~#
# Main command handler #
#~~~~~~~~~~~~~~~~~~~~~~#
@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if '/' in message.content:
		allowed_slash_cmds = ['hiscore','hiscores','pray']
		if message.content.split('/')[1] in allowed_slash_cmds or len(message.content.split()) > 1:
			await bot.process_commands(message)
	else:
		await bot.process_commands(message)
	return
#~~~~~~~~~~~~~~~~~~~~~#
# end command handler #
#~~~~~~~~~~~~~~~~~~~~~#


#~~~~~~~~~~~~~~#
# Begin /hello #
#~~~~~~~~~~~~~~#
@bot.command(name	= 'hello',
	description	= "Introduce yourself to the bot and learn a lil something",
	brief		= "Hi there, `JadBot`! :)",
	pass_context	= True)
#@bot.command(name='hello',pass_context=True)
async def hello_cmd(context):
	# print('Function called by ' + context.message.author)
	msg = 'Hello ' + context.message.author.mention + ', I am `JadBot`!  Type in the command `!JadBot help` to learn more!'
	# await bot.send_message(message.channel, msg)
	await context.send(msg)
#~~~~~~~~~~~~#
# Emd /hello #
#~~~~~~~~~~~~#


#~~~~~~~~~~~~~~~~~#
# Begin /hiscores #
#~~~~~~~~~~~~~~~~~#
# Supporting commands
#def dice_roll(sides):
#	return randint(1,sides)

@bot.command(name	= 'hiscores',
	description	= "Return high scores of a character",
	brief		= "View highscores",
	aliases		= ['h','hiscore'],
	pass_context	= True)
async def roll_cmd(context,*char_args):
	legal_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 -"

	# get arguements passed
	osrs_char = ' '.join(char_args)

	# Validate character name passed
	for i in osrs_char:
		valid = False
		for j in legal_chars:
			if i == j:
				valid = True
				break
		if valid is False:
			await context.send("Invalid character name.")
			return

	URL  = 'https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal'
	DATA = 'user1=' + urllib.parse.quote(osrs_char) + '&submit=Search'

	print("JadBot started searching for '" + osrs_char + "'...")
	async with context.typing():
		try:
			r = requests.post(url=URL,data=DATA,timeout=50)
		except requests.exceptions.RequestException as e:
			await context.send("Request timed out, most likely the OSRS hiscores functionality is suffering. :(")
			return
	print("JadBot done searching...")

	char_exist = "No player <b>&quot;" + osrs_char + "&quot;</b> found"

	# Check if user does not exist
	if char_exist in r.text:
		await context.send("Could not find player named **" + osrs_char + "** :(")
		return

	soup = BeautifulSoup(r.text, "lxml")

	skill_row = []

	for table_row in soup.select("table tr"):
		cells = table_row.findAll('td')

		if len(cells) == 5:
			if cells[1].text != '':
				skill = []
				img_link = True
				for cell in cells:
					if img_link is True:
						skill.append(cell.img)
						img_link = False
					else:
						skill.append(cell.text.strip("\n"))
				skill_row.append(skill)

	### START MSG ###
	msg = ""
	msg = msg + "```~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
	msg = msg + "Hiscores for:   " + osrs_char + "\n"
	msg = msg + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
	msg = msg + "Skill          Rank        Level    Total Exp\n"
	msg = msg + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
	#           "Construction   11,111,111  99       4,600,000,000"
	for skill in skill_row:
		skill_name = str(skill[1])
		ranking = str(skill[2])
		level = str(skill[3])
		total_exp = str(skill[4])
		msg = msg + skill_name + (15-len(skill_name))*' '
		msg = msg + ranking + (12-len(ranking))*' '
		msg = msg + level + (9-len(level))*' '
		msg = msg + total_exp + '\n'
	msg = msg + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
	msg = msg + "```"
	### END MSG ###

	#print(msg)
	#pp = pprint.PrettyPrinter(indent=8)
	#pp.pprint(skill_row)

	await context.send(msg)
	# attempt to roll the dice!
#~~~~~~~~~~~~~~~#
# End /hiscores #
#~~~~~~~~~~~~~~~#


# print ready status
@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')

# list servers using bot
async def list_servers():
	await bot.wait_until_ready()
	while not bot.is_closed:
		print("#~~~~~~~~~~~~~~~~~~~~~#")
		print("[?] Current servers:")
		for server in bot.servers:
			print(server.name)
		print("#~~~~~~~~~~~~~~~~~~~~~#")
        await asyncio.sleep(600)

#~~~~~~~~~~~~~~~~~~#
# Event JAD-ATTACK #
#~~~~~~~~~~~~~~~~~~#
#@bot.event
async def jad_attack():

	# JAD IS MAD
	print("[!] JAD IS ABOUT TO ATTACK...")

#	channel_id 	= 751847219518242935 # Enter channel ID here (will be the channel where movies are announced)
	channel_id	= 752590414699167814 # Test channel
#	role_id		= 751833828729028729 # Enter role ID here (will be mentioned when movie is picked)
	role_id		= 723296898852716667 # Test role

	jad_target = ''

	# Roll random jad attack (mage/range)
	jad_attack = randint(0,1)
	jad_attack_type = ''

	# Get channel
	channel = bot.get_channel(channel_id)

	# Select random character to target
	char_target = DB.__random_char()

	# SLEEP BETWEEN JAD ATTACKS
	await asyncio.sleep(7)
	# 1.5 to 7 hours
	#await asyncio.sleep(randint(5400,25200))

	if jad_attack == 0:
		# Range attack
		jad_attack_type = 'ranged'
		with open('img/jad/jad_ranged_attack.gif') as f:
			picture = discord.File(f)
			msg = "**Jad** is targeting **" + str(char_target) + "** with a **" + jad_attack_type + "** attack!!!  Quick, pray **" + jad_attack_type + "**!"
			print("[+] " + msg.strip('*',''))
			await channel.send(channel, picture, msg)
	elif jad_attack == 1:
		# Mage attack
		jad_attack_type = 'mage'
		with open('img/jad/jad_magic_attack.gif') as f:
			picture = discord.File(f)
			msg = "**Jad** is targeting **" + str(char_target) + "** with a **" + jad_attack_type + "** attack!!!  Quick, pray **" + jad_attack_type + "**!"
			print("[+] " + msg.strip('*',''))
			await channel.send(channel, picture, msg)
	elif jad_attack == 2:
		# Melee attack (not yet implemented)
		jad_attack_type = 'melee'
		#msg = "**Jad** is targeting **" + str(char_target) + "** with a **" + jad_attack_type + "** attack!!!  Quick, pray **" + jad_attack_type + "**!"
	else:
		print("[-] Encountered an error with jad_attack")
		return

	async with context.typing():
		await asyncio.sleep(15)



	# JAD IS SLEEPY
	print("[!] JAD IS DONE ATTACKING!")

#~~~~~~~~~~~~~~~~#
# End JAD-ATTACK #
#~~~~~~~~~~~~~~~~#

#bot.loop.create_task(list_servers())
bot.loop.create_task(jad_attack())

print("[+] Bot started")
bot.run(TOKEN)
