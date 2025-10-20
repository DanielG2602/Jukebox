import os
import discord
from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event 
async def on_ready():
    print(f'{bot.user.name} funcionando!')
    print('--------------------------------\n')

@bot.command(name='entrar', help='Faz o bot entrar no canal de voz atual do solicitante.')
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send(f"{ctx.author.name} não está conectado a um canal de voz.")
        return

    channel = ctx.author.voice.channel
    
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
        await ctx.send(f"Movido para o canal: **{channel}**!")
    else:
        await channel.connect()
        await ctx.send(f"Conectado ao canal: **{channel}**!")

@bot.command(name='sair', help='Faz o bot sair do canal de voz atual.')
async def sair(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Desconectado do canal de voz. Tchau!")
    else:
        await ctx.send("Eu não estou em um canal de voz neste servidor.")
        

bot.run(TOKEN)