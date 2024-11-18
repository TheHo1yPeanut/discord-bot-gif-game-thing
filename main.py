import discord
import asyncio
import aiohttp
from discord.ext import commands
from discord import ui
import random
from datetime import datetime

from bs4 import BeautifulSoup 
import requests 
import re 

intents = discord.Intents.default()
intents.message_content = True

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

@bot.command()
async def GIFgame(ctx: commands.Context):
    word = await get_word()
    doc = getHTMLdocument(f"https://tenor.com/search/{word}")
    randSoup = BeautifulSoup(doc, "html.parser")

    gifLink = randSoup.find("figure").find("a")["href"]

    await ctx.send(f"https://tenor.com{gifLink}")
    await ctx.send("What is this GIF called?")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        response = await bot.wait_for("message", check=check, timeout=30)  # 30-second timeout
        responseDoc = getHTMLdocument(f"https://tenor.com/search/{response.content}")
        responseSoup = BeautifulSoup(responseDoc, "html.parser")
        figures = responseSoup.find_all("figure", limit=20)

        for i in range(20):
            if figures[i].find("a")["href"] == gifLink:
                await ctx.send("You win!")

        await ctx.send(f"response registered")
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Please try again.")


def get_token() -> str:
    with open(TOKEN_FILE, mode="r") as tokenfile:
        token = tokenfile.read().strip()
    return token



bot.run(get_token())