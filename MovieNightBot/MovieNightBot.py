# Work with Python 3.6
import sys
import string
import time
import random
from datetime import datetime, timedelta

import urllib.parse
import requests

import asyncio
import aiocron
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
		fs = line.split('///')
		user = fs[0]
		movie = fs[1].strip("\n")
		if user == str(context.message.author):
			print("[!] " + str(context.message.author) + " changing vote: '" + movie.replace("_"," ") + "' -> '" + movie_name + "'")
		else:
			vote_rewrite.write(line)
	vote_rewrite.close()

	# Add movie vote and discord name to file
	with open("movie_votes.txt","a") as f:
		f.write(str(context.message.author) + "///" + movie_name.replace(" ","_") + "\n")
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
			msg = msg + line.split("///")[0].split("#")[0] + (32-len(line.split("///")[0]))*' ' + " : " + line.split("///")[1].replace("_"," ").strip("\n") + "\n"

	msg = msg + "```"
	await context.send(msg)
#~~~~~~~~~~~~~#
# End /status #
#~~~~~~~~~~~~~#



#~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Begin task: movie select #
#~~~~~~~~~~~~~~~~~~~~~~~~~~#
# NOTE: Make sure to enter channel / role ID in proper fields below
#@bot.event
#@aiocron.crontab('0 7 * * sun')
@aiocron.crontab('* * * * *')
async def select_movie():
#	channel_id = 751847219518242935 # Enter channel ID here (will be the channel where movies are announced)
	channel_id = 729104553638625310 # Test channel
#	role_id    = 751833828729028729 # Enter role ID here (will be mentioned when movie is picked)
	role_id    = 723181617090396261 # Test role

	vote_no = 0
	all_votes = []

	msg = ""

	# Get channel
	channel = bot.get_channel(channel_id)

	with open("movie_votes.txt","r") as f:
		for line in f:
			vote = {
				'discord_name':'',
				'movie_name':''
			}

			vote['discord_name'] = line.split("///")[0].split("#")[0]
			vote['movie_name'] = line.split("///")[1].strip("\n")

			all_votes.append(vote)

			print("Loaded vote: " + str(vote))

	print("Total number of votes: " + str(len(all_votes)))

	# Main logic
	if len(all_votes) == 0:
		msg = msg + "No movies have been voted for :("
		await channel.send(msg)
		return
	elif len(all_votes) == 1:
		msg = msg + "There is only **1** vote this week!  The chosen movie is: `" + all_votes[0]['movie_name'] + "` (vote cast by `" + all_votes[0]['discord_name'] + "`)"
		await channel.send(msg)
		return
	else:
		print("range of random.sample: " + str(range(0,len(all_votes))))

		# Change last number here to add in more movies to decision pool
		rand_nums = random.sample(range(0,len(all_votes)),2)

		print("rand_nums: " + str(rand_nums))

		# Check if the random movie choices are the same (THIS IS NOT DYNAMIC RN, if you change the number of movies
		# in the decision pool, you will need to update this
		if all_votes[rand_nums[0]]['movie_name'] == all_votes[rand_nums[1]]['movie_name']:
			msg = msg + "<@&" + str(role_id) + ">'s!!!  Votes are in and the poll is closed!  As a matter of fact, the same movie has been randomly chosen **twice** so it is automatically the chosen movie.  The randomly selected movie is:\n\n **" + all_votes[rand_nums[0]]['movie_name'] + "**"
			await channel.send(msg)
			return

		msg = msg + "<@&" + str(role_id) + ">'s!!!  Votes are in and the poll is closed!  The movies being passed to the council are as follows:\n```"

		i = 0
		for num in rand_nums:
			i = i + 1
			msg = msg + "   " + str(i) + ") " + all_votes[num]['movie_name'] + " (vote cast by " + all_votes[num]['discord_name'] + ")\n"

		msg = msg + "```"

		await channel.send(msg)
		return


	#await channel.send(msg)

	# HArd CoDEd lIke A ReaL PRoGameR
	#for server in bot.servers:
	#	for channel in server.channels:
	#		if channel.name == channel_name:
	#			break

	# Testing
	# channel = bot.get_channel(channel_id)
	# await channel.send('Minute cronjob with aiocron~')

#~~~~~~~~~~~~~~~~~~~~~~~~#
# End task: movie select #
#~~~~~~~~~~~~~~~~~~~~~~~~#



# print ready status
@bot.event
async def on_ready():
	print('BOT ACTIVATED: ' + str(bot.user.name) + ' | ' + str(bot.user.id))
	print('------+++++++++++++++++++++++++++++++++++++++++------')

print("[+] Bot started")
bot.run(TOKEN)
