# Work with Python 3.6
import sys
import string

import urllib.parse
import requests

import asyncio
import aiohttp
import json

import discord
from discord.ext import commands

BOT_PREFIX=("!moviebot ","/moviebot ","!movie ","/movie ")
TOKEN='XXXX'
OMDB_API_KEY='565e94d0'

bot = commands.Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	await bot.process_commands(message)
	return


#~~~~~~~~~~~~~~#
# Begin /hello #
#~~~~~~~~~~~~~~#
@bot.command(name	= 'hello',
	description	= "Introduce yourself to the bot and learn a lil something",
	brief		= "Hi there, `MovieNightBot`! :)",
	pass_context	= True)
#@bot.command(name='hello',pass_context=True)
async def hello_cmd(context):
	# print('Function called by ' + context.message.author)
	msg = 'Hello ' + context.message.author.mention + ', I am `MovieNightBot`!  Type in the command `!moviebot help` to learn more!'
	# await bot.send_message(message.channel, msg)
	await context.send(msg)
#~~~~~~~~~~~~#
# Emd /hello #
#~~~~~~~~~~~~#


#~~~~~~~~~~~~#
# Begin help #
#~~~~~~~~~~~~#
# Remove previous help command
#bot.remove_command("help")

#@bot.command(name 	= 'help',
#	pass_context	= True)
#async def help_cmd(context):
#	msg	= ("```Usage: `!moviebot [cmd]` || `/moviebot [cmd]` || `!movie [cmd]` || `/movie [cmd]`\n\n"
#	"Available commands (`[cmd]`):\n"
#	"\t`hello` : Say hello to `MovieNightBotot`!\n```"
#	await context.send(msg)
#~~~~~~~~~~~#
# End /help #
#~~~~~~~~~~~#


#~~~~~~~~~~~~~#
# Begin /vote #
#~~~~~~~~~~~~~#
@bot.command(name	= 'vote',
	description	= "Vote for your movie that you want to watch for movie night!",
	brief		= "Cast your movie vote",
	aliases		= ['v','cast','castvote'],
	pass_context	= True)
async def vote_cmd(context,*movie_args):
	# get arguements passed
	movie_name = ' '.join(movie_args)

	if movie_name is '':
		await context.send("Please supply a movie name :)")
		return

	# Debug note
	print("[?] " + str(context.message.author) + " is attempting to cast thier vote for '" + movie_name + "'")

	# Cross reference IMDB for movie name
	#print('Checking movie name: ' + movie_name)

	URL = 'http://www.omdbapi.com'
	PARAMS = {
		"apikey":OMDB_API_KEY,
		"t":movie_name
	}

	r = requests.get(url=URL,params=PARAMS)

	if r.content == b'{"Response":"False","Error":"Movie not found!"}':
		await context.send("[-] No movie found named `" + movie_name + "` :(")
		return

	r_json = r.json()

	if movie_name.lower() != str(r_json["Title"]).lower():
		await context.send("[-] No movie found named `" + movie_name + "` :(")
		return

	movie_name = str(r_json["Title"])

	# Check if user already has cast vote
	votes = open("movie_votes.txt","r")
	lines = votes.readlines()
	votes.close()
	vote_rewrite = open("movie_votes.txt","w")
	for line in lines:
		fs = line.split(':')
		user = fs[0]
		movie = fs[1].strip("\n")
		if user == str(context.message.author):
			print("[!] " + str(context.message.author) + " changing vote: '" + movie.replace("_"," ") + "' -> '" + movie_name + "'")
		else:
			vote_rewrite.write(line)
	vote_rewrite.close()

	# Add movie vote and discord name to file
	with open("movie_votes.txt","a") as f:
		f.write(str(context.message.author) + ":" + movie_name.replace(" ","_") + "\n")
		await context.send("Successfully cast your movie vote for '" + movie_name + "'!")
		print("[+] Successfully cast new movie vote: " + str(context.message.author) + ":" + movie_name.replace(" ","_"))
#~~~~~~~~~~~#
# End /vote #
#~~~~~~~~~~~#

#~~~~~~~~~~~~~~~#
# Begin /status #
#~~~~~~~~~~~~~~~#
@bot.command(name       = 'status',
	description     = "View everyone's current vote!",
	brief           = "List all current movie votes",
	aliases         = ['s','current'],
	pass_context    = True)
async def status_cmd(context):
	msg = "Currently the movie votes are as stands:\n```"

	with open("movie_votes.txt","r") as f:
		for line in f:
			msg = msg + line.split(":")[0].split("#")[0] + (32-len(line.split(":")[0]))*' ' + " : " + line.split(":")[1].replace("_"," ")

	msg = msg + "```"
	await context.send(msg)
#~~~~~~~~~~~~~#
# End /status #
#~~~~~~~~~~~~~#

# print ready status
@bot.event
async def on_ready():
	print('BOT ACTIVATED: ' + str(bot.user.name) + ' | ' + str(bot.user.id))
	print('------+++++++++++++++++++++++++++++++++++++++++------')

print("[+] Bot started")
bot.run(TOKEN)
