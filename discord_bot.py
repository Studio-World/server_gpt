import os
import discord
from discord.ext import commands

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"[✅] Bot conectado como {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! DAN-XBOX Bot ativo.")

async def start_discord_bot():
    if DISCORD_TOKEN:
        await bot.start(DISCORD_TOKEN)
