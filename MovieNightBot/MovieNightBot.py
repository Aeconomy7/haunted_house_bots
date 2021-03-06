# Work with Python 3.6
import sys
import string
import time
import random
from datetime import datetime, timedelta

import urllib.parse
import requests

import emoji

import asyncio
import aiocron
import aiohttp
import json

import discord
from discord.ext import commands
from discord.utils import get

BOT_PREFIX=("!moviebot ","/moviebot ","!movie ","/movie ")
TOKEN='XXXX'
OMDB_API_KEY='565e94d0'


### BEGIN MISC FUNCTIONS ###

def aggressive_url_encode(string):
	return "".join("%{0:0>2}".format(format(ord(char), "x")) for char in string)

### END MISC FUNCTIONS ###



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

	# Check if this movie has already beeen watched
	with open("watched.txt","r") as f:
		for line in f:
			if line.strip("\n").replace("_"," ").lower() == movie_name.strip("\n").lower():
				await context.send("**" + line.strip("\n").replace("_"," ") + "** has already been watched! :D")
				return

	# Check if this is already user's vote
	with open("movie_votes.txt","r") as f:
		for line in f:
			if line.split("///")[0] == str(context.message.author):
				if line.split("///")[1].strip("\n").replace("_"," ").lower() == movie_name.strip("\n").lower():
					await context.send("**" + line.split("///")[1].strip("\n").replace("_"," ") + "** is currently your vote!")
					return


	changed_vote = ""
	chng = False

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
			changed_vote = movie.replace("_"," ")
			chng = True
			print("[!] " + str(context.message.author) + " changing vote: '" + changed_vote + "' -> '" + movie_name + "'")
		else:
			vote_rewrite.write(line)
	vote_rewrite.close()

	# Add movie vote and discord name to file
	with open("movie_votes.txt","a") as f:
		f.write(str(context.message.author) + "///" + movie_name.replace(" ","_") + "\n")
		if chng is False:
			await context.send("Successfully cast your movie vote for **" + movie_name + "**!")
		else:
			await context.send("Successfully changed your vote from **" + changed_vote + "** to **" + movie_name + "**")
		print("[+] Successfully cast new movie vote: " + str(context.message.author) + ":" + movie_name.replace(" ","_"))

	return
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


#~~~~~~~~~~~~~~~~~#
# Begin /synopsis #
#~~~~~~~~~~~~~~~~~#
@bot.command(name	= 'overview',
	description	= "Get a brief synopsis of a movie.",
	brief		= "Get a synopsis",
	aliases		= ['synopsis','plot'],
	pass_context	= True)
async def synopsis_cmd(context,*movie_args):
	msg = ""

	movie_name = ' '.join(movie_args)

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

	movie_title	= str(r_json["Title"])
	movie_year	= str(r_json["Year"])
	movie_plot 	= str(r_json["Plot"])
	movie_directors	= str(r_json["Director"])
	movie_writers	= str(r_json["Writer"])
	movie_actors	= str(r_json["Actors"])

	msg = msg + "```" + movie_title + " (" + movie_year + ")\n\n"
	msg = msg + "Directed by:  " + movie_directors + "\n"
	msg = msg + "Written by:   " + movie_writers + "\n"
	msg = msg + "Starring:     " + movie_actors + "\n\n"
	msg = msg + "Synopsis:\n" + movie_plot + "```"

	print("[+] Fetched overview for '" + movie_title + "'")

	await context.send(msg)
#~~~~~~~~~~~~~~~#
# End /synopsis #
#~~~~~~~~~~~~~~~#


#~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Begin task: movie select #
#~~~~~~~~~~~~~~~~~~~~~~~~~~#
# NOTE: Make sure to enter channel / role ID in proper fields below
#@bot.event
#@aiocron.crontab('* * * * *')
@aiocron.crontab('0 18 * * fri')
async def select_movie():
	# UPDATE: these channel/role ids are specific to the developers discord and should be updated
	#	  to your own channel which you want movie select on
	channel_id = [751847219518242935,758054279092109354] # Enter channel ID here (will be the channel where movies are announced)
#	channel_id = 752590414699167814 # Test channel
	role_id    = [751833828729028729,775541628668608532] # Enter role ID here (will be mentioned when movie is picked)
#	role_id    = 723296898852716667 # Test role

	# Announce one hour until movie selection
	role_mention = 0

        # Get channel
	for chnl in channel_id:
		channel = bot.get_channel(chnl)
		#channel = bot.get_channel(channel_id)
		msg = msg + "Only **ONE HOUR** remains until a movie is chosen <@&" + str(role_id[role_mention]) + ">'s!!!  Make sure to get your vote in using `/movie vote [MOVIE_NAME]`!"
		await channel.send(msg)
		role_mention = role_mention + 1
		msg = ""


	# Sleep one hour
	print("[.] Sleeping 1 hour before choosing movie...")
	await asyncio.sleep(3600)
	print("[!] Time to choose the movie!")

	mins_to_movie = 1 # Number of minutes between random movie selection and movie time

	vote_no = 0
	all_votes = []

	# special thanks to Hobro for these cursed react emoji strings
	react_emojis = [
		'1\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}',
		'2\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}',
		'3\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}'
	]

	msg = ""


	with open("movie_votes.txt","r") as f:
		for line in f:
			vote = {
				'discord_name':'',
				'movie_name':''
			}

			vote['discord_name'] = line.split("///")[0].split("#")[0]
			vote['movie_name'] = line.split("///")[1].strip("\n")

			all_votes.append(vote)

			print("[+] Loaded vote from 'movie_votes.txt': " + str(vote))

	print("[?] Total number of votes: " + str(len(all_votes)))

	# Main logic
#	if len(all_votes) == 0:
#		msg = msg + "No movies have been voted for :("
#		await channel.send(msg)
#		return
#	elif len(all_votes) == 1:
#		msg = msg + "<@&" + str(role_id) + ">'s!!!  There is only **1** vote this week!  The chosen movie is: `" + all_votes[0]['movie_name'].replace("_"," ") + "` (vote cast by `" + all_votes[0]['discord_name'] + "`)"
#		await channel.send(msg)
#		return
#	else:
		# Debug
		#print("range of random.sample: " + str(range(0,len(all_votes))))
#		if len(all_votes) == 2:
#			rand_nums = random.sample(range(0,len(all_votes)),2)
#			msg = msg + "<@&" + str(role_id) + ">'s!!!  " + str(len(all_votes)) + " vote(s) are in and the poll is closed!  The **two** movies being passed to the council are as follows:\n```"
#		else:
			# Change last number here to add in more movies to decision pool
#			rand_nums = random.sample(range(0,len(all_votes)),3)
#			msg = msg + "<@&" + str(role_id) + ">'s!!!  " + str(len(all_votes)) + " vote(s) are in and the poll is closed!  The **three** movies being passed to the council are as follows:\n```"

		# Debug
		#print("rand_nums: " + str(rand_nums))

		# Check if the random movie choices are the same (THIS IS NOT DYNAMIC RN, if you change the number of movies
		# in the decision pool, you will need to update this
		#if all_votes[rand_nums[0]]['movie_name'] == all_votes[rand_nums[1]]['movie_name']:
		#	msg = msg + "<@&" + str(role_id) + ">'s!!!  " + str(len(all_votes)) + " vote(s) are in and the poll is closed!  As a matter of fact, the same movie has been randomly chosen **twice** so it is automatically the chosen movie.  The randomly selected movie is:\n\n **" + all_votes[rand_nums[0]]['movie_name'] + "**"
		#	await channel.send(msg)
		#	return


	### NOTE: One random movie:
	rand_nums = random.sample(range(0,len(all_votes)),1)
	with open("watched.txt","a") as f:
		f.write(all_votes[rand_nums[0]]['movie_name'] + "\n")
	# Clear all votes for the movie
	curr_votes = open("movie_votes.txt","r")
	lines = curr_votes.readlines()
	curr_votes.close()

	updated_votes = open("movie_votes.txt","w")
	for line in lines:
		if not all_votes[rand_nums[0]]['movie_name'] in line:
			updated_votes.write(line)
	updated_votes.close()

	# role mention solution
	role_mention = 0

	# Get channel
	for chnl in channel_id:
		print("[!] Sending results to channel id '" + str(chnl) + "'")
		channel = bot.get_channel(chnl)
		#channel = bot.get_channel(channel_id)
		msg = msg + "<@&" + str(role_id[role_mention]) + ">'s!!!  " + str(len(all_votes)) + " vote(s) are in and the poll is closed!  The selected movie is **" + all_votes[rand_nums[0]]['movie_name'].replace("_"," ") + "**.  *NOTE: The selected movie is final.  Overrule implementation coming soon:tm:*"
		await channel.send(msg)
		role_mention = role_mention + 1
		msg = ""

### NOTE: Three random movies:
#		i = 0
#		for num in rand_nums:
#			i = i + 1
#			msg = msg + str(i) + ") " + all_votes[num]['movie_name'].replace("_"," ") + " (vote cast by " + all_votes[num]['discord_name'] + ")\n"

#		msg = msg + "```"

#		msg_react = await channel.send(msg)
#		if len(all_votes) == 2:
#			await msg_react.add_reaction(react_emojis[0])
#			await msg_react.add_reaction(react_emojis[1])
#		else:
#			await msg_react.add_reaction(react_emojis[0])
#			await msg_react.add_reaction(react_emojis[1])
#			await msg_react.add_reaction(react_emojis[2])

		# Sleep until it is movie time
		#await asyncio.sleep(1)

#		one_votes   = 0
#		two_votes   = 0
#		three_votes = 0

#		await asyncio.sleep(5)

#		print(msg_react.id)
		#for react in msg_react.reactions:

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
