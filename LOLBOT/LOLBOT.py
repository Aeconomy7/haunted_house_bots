# Work with Python 3.6
import requests

import asyncio
import aiohttp
import json
import re
import random

import urllib.parse

import discord
from discord.ext import commands

from db.loldb import LolDbHandler

from riotwatcher import LolWatcher, ApiError

# INITIATE DB
LOL_DB = LolDbHandler()
LOL_DB.__enter__()
# END INITIATE


BOT_PREFIX=("!lolbot ","/lolbot ","/lol")
TOKEN='XXXX'
PROXY_MODE=0
lol_watcher = LolWatcher('XXXX')
REGION='na1'
bot = commands.Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if '/' in message.content:
		allowed_slash_cmds = ['']
		if message.content.split('/')[1] in allowed_slash_cmds or len(message.content.split()) > 1:
			await bot.process_commands(message)
	else:
		await bot.process_commands(message)
	return

#~~~~~~~~~~~~~~#
# Begin /hello #
#~~~~~~~~~~~~~~#
@bot.command(name	= 'hello',
	description	= "Introduce yourself to the bot and learn a lil something",
	brief		= "Hi there, `LOLBOT`! :)",
	pass_context	= True)
#@bot.command(name='hello',pass_context=True)
async def hello_cmd(context):
	# print('Function called by ' + context.message.author)
	msg = 'Hello ' + context.message.author.mention + ', I am `LOLBOT`!  Type in the command `!LOLBOT help` to learn more!'
	# await bot.send_message(message.channel, msg)
	await context.send(msg)
#~~~~~~~~~~~~#
# Emd /hello #
#~~~~~~~~~~~~#


#~~~~~~~~~~~~~#
# Begin /rank #
#~~~~~~~~~~~~~#
# rank command:
# params:
#	summoner_name 	= string
@bot.command(name	= 'rank',
	description	= "Return rank and top champion winrates (NA ONLY)!!!!!!",
	brief		= "RANKED",
	aliases		= [],
	pass_context	= True)
async def rank_cmd(context,*rank_args):
	requests.packages.urllib3.disable_warnings()

	summoner_name = ' '.join(rank_args)
	summoner_name_enc = urllib.parse.quote(summoner_name)

	# Get Summoner
	try:
		summoner = lol_watcher.summoner.by_name(REGION, summoner_name_enc)
	except ApiError as err:
		if err.summoner.status_code == 429:
			await context.send("Too many requests, not enough cooks...")
			return
		elif err.summoner.status_code == 404:
			await context.send("Could not find ranked history for summoner `" + summoner_name + "` :(")
			return


	# Fetch ranked data
	try:
		response = lol_watcher.league.by_summoner(REGION,summoner['id'])
	except ApiError as err:
		if err.response.status_code == 429:
			await context.send("Too many requests, not enough cooks...")
			return
		elif err.response.status_code == 404:
			await context.send("Could not find ranked history for summoner `" + summoner_name + "` :(")
			return



	# Successful return message
	msg = ""
	msg += "```"
	try:
		for i in response:
			summoner_name = i['summonerName']
			if i['queueType'] == "RANKED_SOLO_5x5":
				winrate = (i['wins']/(i['wins']+i['losses']))*100
				msg += "[SOLO/DUO]: " + i['tier'] + " " + i['rank'] + " " + str(i['leaguePoints']) + "LP, " + str(i['wins']) + " W / " + str(i['losses']) + " L (" + str(round(winrate,2)) + "%)\n"
			if i['queueType'] == "RANKED_FLEX_SR":
				winrate = (i['wins']/(i['wins']+i['losses']))*100
				msg += "[FLEXEMSs]: " + i['tier'] + " " + i['rank'] + " " + str(i['leaguePoints']) + "LP, " + str(i['wins']) + " W / " + str(i['losses']) + " L (" + str(round(winrate,2)) + "%)\n"
	except:
		await context.send("Could not find ranked history for summoner `" + summoner_name + "` :(")
		return
	msg += "```"

	if msg == "``````":
		await context.send("Could not find ranked history for summoner `" + summoner_name + "` :(")
		return
	else:
		rank_embed = discord.Embed(title=summoner_name + "'s Rank Stats", description=msg, color=random.randrange(1,16777214))

	await context.send(embed=rank_embed)
	print("[+] Successfully found ranking of summoner '" + summoner_name + "'")
	#await context.send (msg)

	return
#~~~~~~~~~~~#
# End /rank #
#~~~~~~~~~~~#


#~~~~~~~~~~~~~~~~#
# Begin /compete #
#~~~~~~~~~~~~~~~~#
# rank command:
# params:
#	action		= string (add / remove)
#       summoner_name   = string
@bot.command(name	= 'compete',
	description	= "Add or remove summoner from rank competition",
	brief		= "COMPETE",
	aliases		= [],
	pass_context	= True)
async def join_compete_cmd(context,*rank_args):
	print(rank_args[0])
	return
#~~~~~~~~~~~~~~#
# End /compete #
#~~~~~~~~~~~~~~#



#~~~~~~~~~~~~~~~#
# Begin /update #
#~~~~~~~~~~~~~~~#
# update command:
# params:
# 	- summoner name
@bot.command(name       = 'update',
	description     = "Update rank history of summoner",
	brief           = "UPDATE",
	aliases         = [],
	pass_context    = True)
async def update_cmd(context,*update_args):
	requests.packages.urllib3.disable_warnings()

	summoner_name = urllib.parse.quote(' '.join(update_args))

	# CACHE MECHANISM
	#with open("/home/sc00by/Documents/Programming/Discord/haunted_house_bots/LOLBOT/_summoner.cache","r") as f:
	#	for line in f:
	#		if line.split(":")[0] == summoner_name:
	#			summid = line.split(":")[1]
	#f.close()

	# DATABASE CACHE MECHANISM
	summoner = LOL_DB.get_summoner(summoner_name)

	# NO CACHE HIT
	#if summoner == None:
#		
#	else:
#		update_status = update_rank_history(summid)
#		if update_status == "FAIL":
#			await context.send("Error updating ranked history for `" + summoner_name + "`")
#		else:
#		

#~~~~~~~~~~~~~#
# End /update #
#~~~~~~~~~~~~~#




#~~~~~~~~~~~~~~~~#
# Begin /hiscore #
#~~~~~~~~~~~~~~~~#

#~~~~~~~~~~~~~~#
# End /hiscore #
#~~~~~~~~~~~~~~#





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

print("[+] Bot started")
bot.run(TOKEN)