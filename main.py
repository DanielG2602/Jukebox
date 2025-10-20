import os
import discord
from discord.ext import commands

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN') 
if not DISCORD_TOKEN:
    print("ERRO: A variável de ambiente DISCORD_TOKEN não foi encontrada. Verifique o arquivo .env.")
    exit()

intents = discord.Intents.default()
intents.message_content = True 
intents.voice_states = True 
intents.members = True 

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event 
async def on_ready():
    print('--------------------------------')
    print(f'✅ Login efetuado como: {bot.user.name}')
    
    try:
        await bot.load_extension("cogs.music_cog")
        print("🎶 Módulo 'cogs.music_cog' carregado com sucesso.")
    except Exception as e:
        print(f"❌ ERRO ao carregar o módulo de música: {e}")
    
    print('--------------------------------')

bot.run(DISCORD_TOKEN)
