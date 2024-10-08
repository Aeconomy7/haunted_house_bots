from riotwatcher import LolWatcher, ApiError
import riotwatcher

lol_watcher = LolWatcher('RGAPI-a24735ad-0081-4bd1-97f4-c2142461d95f')

my_region = 'na1'

me = lol_watcher.summoner.by_name(my_region, 'sc00by')
print(me + "\n=========================================================")

# all objects are returned (by default) as a dict
# lets see if i got diamond yet (i probably didnt)
my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
print(my_ranked_stats + "\n=========================================================")



# First we get the latest version of the game from data dragon
versions = lol_watcher.data_dragon.versions_for_region(my_region)
champions_version = versions['n']['champion']

# Lets get some champions
current_champ_list = lol_watcher.data_dragon.champions(champions_version)
print(current_champ_list + "\n=========================================================")


# For Riot's API, the 404 status code indicates that the requested data wasn't found and
# should be expected to occur in normal operation, as in the case of a an
# invalid summoner name, match ID, etc.
#
# The 429 status code indicates that the user has sent too many requests
# in a given amount of time ("rate limiting").

#try:
#    response = lol_watcher.summoner.by_name(my_region, 'this_is_probably_not_anyones_summoner_name')
#except ApiError as err:
#    if err.response.status_code == 429:
#        print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
#        print('this retry-after is handled by default by the RiotWatcher library')
#        print('future requests wait until the retry-after time passes')
#    elif err.response.status_code == 404:
#        print('Summoner with that ridiculous name not found.')
#    else:
#        raise
