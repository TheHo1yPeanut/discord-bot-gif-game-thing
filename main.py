import discord
import asyncio
import aiohttp
from discord.ext import commands
from discord import ui
import random
from datetime import datetime
from pymongo import MongoClient

from bs4 import BeautifulSoup 
import requests 
import re 

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# region mongoDB technical bs
C_STRING = ""

client = MongoClient(C_STRING)

db = client["DiscordDB"]

collection = db["userData"]

print(collection.find_one({"user":"userID"})["test"])
# endregion

bot = commands.Bot(command_prefix="!", intents = intents)

TOKEN_FILE = "token.txt"

@bot.event
async def on_ready():
    print("Connected")

@bot.command()
async def drSwag(ctx: commands.Context):
    await ctx.send("https://tenor.com/view/dr-house-dr-gregory-house-dr-gregory-gif-13514172004559334125")
    return

async def get_word():
    async with aiohttp.ClientSession() as session:
        word_url = f"https://random-word-api.herokuapp.com/word"
        async with session.get(word_url) as response:
            word = await response.json()
            return word[0]

def getHTMLdocument(url): 
    response = requests.get(url) 
    return response.text 

def userDataHandler(id, win:bool):

    user = collection.find_one({"user":id})

    if(user == None):
        newUser = {
            "user": id,
            "games": 0,
            "score": 0
        }

        collection.insert_one(newUser)

        user = collection.find_one({"user":id})


    if(win):
        collection.update_one({"user":user["user"]},{"$inc": {"score": 1}})
        collection.update_one({"user":user["user"]},{"$inc": {"games": 1}})
    else:
        collection.update_one({"user":user["user"]},{"$inc": {"games": 1}})

@bot.command()
async def GIFgame(ctx: commands.Context):

    word = await get_word()
    doc = getHTMLdocument(f"https://tenor.com/search/{word}")
    randSoup = BeautifulSoup(doc, "html.parser")

    gifLink = randSoup.find("figure").find("a")["href"]

    await ctx.send(f"https://tenor.com{gifLink}")
    await ctx.send("What is this GIF called?")

    def check(message):
        if(message.author == ctx.author and message.channel == ctx.channel):
            ctx.userID = message.author.id
            print(ctx.userID)
            return message.author == ctx.author and message.channel == ctx.channel


    try:
        winstatus = False

        response = await bot.wait_for("message", check=check, timeout=30)  # 30-second timeout
        responseDoc = getHTMLdocument(f"https://tenor.com/search/{response.content}")
        responseSoup = BeautifulSoup(responseDoc, "html.parser")
        figures = responseSoup.find_all("figure", limit=20)

        try:
            for i in range(20):
                if figures[i].find("a")["href"] == gifLink:
                    winstatus = True

            if(winstatus):  
                await ctx.send(f"You win!")
                userDataHandler(ctx.userID, True)
            else:
                await ctx.send(f"You lose ;(")
                userDataHandler(ctx.userID, False)

        except IndexError as e:
            await ctx.send("Sorry this GIF is silly, try again! (this will not affect your winrate)")



        #await ctx.send(f"response registered")
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Please try again.")


@bot.command()
async def userINFO(ctx: commands.Context, user: discord.Member = None):
    if(user != None):
        if(collection.find_one({"user":user.id}) != None):

            games = collection.find_one({"user":user.id})["games"]
            score = collection.find_one({"user":user.id})["score"]
            
            embed = discord.Embed(
                title="Stats",
                color=discord.Color.blue()
            )
            
            embed.add_field(name="Games", value=f"{games}", inline=False)
            embed.add_field(name="Score", value=f"{score}", inline=False)
            embed.add_field(name="Win%", value=f"{(score / games)*100}%", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send("This user has not played before.")
    else:
        await ctx.send("Please tag a user.")

def get_token() -> str:
    with open(TOKEN_FILE, mode="r") as tokenfile:
        token = tokenfile.read().strip()
    return token



bot.run(get_token())