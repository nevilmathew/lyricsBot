# bot.py
import os
import requests, json 
from discord.ext import commands
from dotenv import load_dotenv
from youtube_search import YoutubeSearch
import youtube_dl
import discord
from lyrics import lyrics

def songinfo(name):
    results = YoutubeSearch(name, max_results=1).to_json()
    yt_id = str(json.loads(results)['videos'][0]['id'])
    yt_url = 'https://www.youtube.com/watch?v='+yt_id
    video = youtube_dl.YoutubeDL({}).extract_info(yt_url, download=False)
    title = video["track"]
    artist = video["artist"]
    #Uncomment the below lines to use lyrics.ovh
    #song_id = '/'+artist+'/'+title 
    #request = requests.get('https://api.lyrics.ovh/v1'+song_id)
    #lyric = request.json()
    lyric = lyrics(artist,title) #Get lyrics via Genius
    return str(lyric)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

bot = commands.Bot(command_prefix='!')

@bot.command(name='play')
async def test(ctx, *, arg):
    lyr=songinfo(arg)
    if len(lyr) >= 2000:
        lyr_first = lyr[:len(lyr)//2]
        lyr_second =  lyr[len(lyr)//2:]
        embedVar = discord.Embed(title="Lyrics", description= lyr_first, color=242424)
        await(await (ctx.send(embed=embedVar))).delete(delay=300.0)
        embedVar2 = discord.Embed(title="..", description=lyr_second, color=242424)
        await(await (ctx.send(embed=embedVar2))).delete(delay=300.0)
    else:
        lyr_first = lyr
        lyr_first = lyr
        embedVar = discord.Embed(title="Lyrics", description=lyr, color=242424)
        await(await (ctx.send(embed=embedVar))).delete(delay=300.0)

bot.run(TOKEN)