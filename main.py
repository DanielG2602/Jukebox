import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event 
async def on_ready():
    print(f'Login efetuado como: {bot.user.name}')
    
    try:
        await bot.load_extension("cogs.music_cog")
        print("Módulo 'cogs.music_cog' carregado com sucesso.")
    except Exception as e:
        print(f"ERRO ao carregar o módulo de música: {e}")
    
    print('--------------------------------')

bot.run(TOKEN)