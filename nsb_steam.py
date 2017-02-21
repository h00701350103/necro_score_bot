import urllib
import urllib.request
import os
import codecs
import json
import re
import time
import sys

#from nsb_config import options


def fetchUrl(url, path=None):
    tries = 10
    while True:
        try:
            if path:
                urllib.request.urlretrieve(url, path)
            else:
                return urllib.request.urlopen(url)
            break
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            tries -= 1
            print('Catched "' + str(e) + '" fetching', url, 'trying', tries, 'more times in 5 seconds')
            time.sleep(5)
            if tries == 0:
                raise LookupError('Failed to fetch', url)
        except:
            tries -= 1
            print('Catched unexpected error: "' + str(sys.exc_info()[0]) + '" fetching', url, 'trying', tries, 'more times in 5 seconds')
            print(sys.exc_info())
            time.sleep(5)
            if tries == 0:
                raise LookupError('Failed to fetch leaderboard at ' + url)


def boardUrl(lbid, start, end):
    baseUrl = 'http://steamcommunity.com/stats/247080/leaderboards/'
    return baseUrl + str(lbid) + '/?xml=1&start=%d&end=%d'%(start, end)

def leaderboardUrl():
    return 'http://steamcommunity.com/stats/247080/leaderboards/?xml=1'

def decodeResponse(response, re_codec='utf-8'):
    data = response.read()
    text = data.decode(re_codec)
    return text

#def downloadIndex(path):
#    boardFile = path + 'leaderboards.xml'
#    fetchUrl(leaderboardsurl, boardFile)

def getTwitterHandle(id, twitit):
    url = 'http://steamcommunity.com/profiles/' + str(id)
    text = decodeResponse(fetchUrl(url), 'latin-1')

    match = re.search(r"twitter\.com\\/(?P<handle>\w+)\\\"", text)
    if match is None:
        return match
    else:
        handle = match.group('handle')
    
    if not twitit:
        print('Warning: unverified handle')
        return handle
    if twitit.checkTwitterHandle(handle):
        return handle
    else:
        print(handle, 'in steam profile but not valid')
        return None

def steamname(steam_id, key):
    #STEAMKEY = options['steam_key']
    STEAMKEY = key
    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%d'%(STEAMKEY, steam_id)
    response = fetchUrl(url)
    reader = codecs.getreader('utf-8')
    obj = json.load(reader(response))
    return obj['response']['players'][0]['personaname']

def steamtime(steam_id, key):
    """
    Returns number of minutes played necrodancer, or None if profile is set to private.
    """
    STEAMKEY = key
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%d&format=json'%(STEAMKEY, steam_id)
    response = fetchUrl(url)
    reader = codecs.getreader('utf-8')
    obj = json.load(reader(response))
    if 'games' in obj['response']:
        for game in obj['response']['games']:
            if game['appid'] == 247080:
                return game['playtime_forever']
    else:
        print(steam_id, 'has private profile')
    return None

def known_cheater(steam_id):
    file = 'known_cheaters.txt'
    if not os.path.isfile(file):
        file = os.path.dirname(os.path.realpath(__file__)) + '/' + file


    with open(file, 'r') as f:
        for line in f:
            if int(line) == steam_id:
                return True
    return False
