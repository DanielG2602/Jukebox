import discord
from discord.ext import commands
import yt_dlp 

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.queues = {} 
        
        self.YTDL_OPTIONS = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

    
    async def play_next_task(self, ctx):
        self.start_playback(ctx)

    def start_playback(self, ctx):
        guild_id = ctx.guild.id
        
        if not self.queues.get(guild_id):
            print(f"Fila vazia para a guilda {guild_id}. Parando reprodução.")
            return

        track = self.queues[guild_id].pop(0) 
        
        source = discord.FFmpegOpusAudio(
            track['source'], 
            **self.FFMPEG_OPTIONS, 
            executable='ffmpeg'
        )

        ctx.voice_client.play(
            source, 
            after=lambda e: self.bot.loop.create_task(self.play_next_task(ctx))
        )
        
        self.bot.loop.create_task(
            ctx.send(f"▶️ Tocando agora: **{track['title']}**")
        )

    @commands.command(name='entrar', help='Faz o bot entrar no seu canal de voz.')
    async def join(self, ctx):
        if not ctx.author.voice:
            await ctx.send(f"**{ctx.author.name}**, você precisa estar em um canal de voz primeiro!")
            return

        channel = ctx.author.voice.channel
        
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()

        await ctx.send(f"Conectado ao canal: **{channel.name}**!")


    @commands.command(name='sair', aliases=['dc'], help='Faz o bot sair do canal de voz.')
    async def sair(self, ctx):
        if ctx.voice_client:
            guild_id = ctx.guild.id
            
            if guild_id in self.queues:
                del self.queues[guild_id]

            await ctx.voice_client.disconnect()
            await ctx.send("Desconectado e filas limpas. Tchau!")
        else:
            await ctx.send("Eu não estou em um canal de voz neste servidor.")
            
            
    @commands.command(name='play', help='Toca uma música ou adiciona-a à fila (ex: !play Despacito)')
    async def play(self, ctx, *, search: str):
        if not ctx.voice_client:
            await self.join(ctx)

        if ctx.voice_client is None:
            return

        await ctx.send(f"🔎 Procurando por: `{search}`...")

        try:
            with yt_dlp.YoutubeDL(self.YTDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
                
                source_url = info['url']
                title = info['title']
                
            guild_id = ctx.guild.id
            if guild_id not in self.queues:
                self.queues[guild_id] = []
            
            self.queues[guild_id].append({'source': source_url, 'title': title})

            if not ctx.voice_client.is_playing():
                self.start_playback(ctx)
            else:
                await ctx.send(f"➕ Adicionado à fila: **{title}**")

        except Exception as e:
            await ctx.send(f"❌ Erro ao buscar/tocar a música. Verifique se o **FFmpeg** está instalado e no PATH. Erro: {e}")
            print(f"Erro detalhado de reprodução: {e}")
            
    @commands.command(name='skip', help='Pula a música atual e toca a próxima na fila.')
    async def skip(self, ctx):
        if ctx.voice_client is None or not ctx.voice_client.is_connected():
            return await ctx.send("Eu não estou conectado a um canal de voz.")

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭️ Música pulada!")
        else:
            await ctx.send("Nenhuma música está tocando no momento.")
            
    @commands.command(name='pause', help='Pausa a música que está tocando.')
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Música pausada!")
        else:
            await ctx.send("Nenhuma música está tocando para pausar.")

    @commands.command(name='resume', help='Retoma a música que está pausada.')
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Música retomada!")
        else:
            await ctx.send("A música não está pausada.")
            
    @commands.command(name='queue', aliases=['fila'], help='Mostra a lista de músicas na fila.')
    async def queue(self, ctx):
        guild_id = ctx.guild.id
        
        if not self.queues.get(guild_id):
            return await ctx.send("A fila de músicas está vazia! Adicione algo com `!play`.")

        fila = [f"{i+1}. {track['title']}" for i, track in enumerate(self.queues[guild_id])]
        
        queue_list = "\n".join(fila)

        embed = discord.Embed(
            title="🎶 Fila de Reprodução",
            description=f"**Músicas:**\n{queue_list}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='stop', help='Para a música atual e limpa toda a fila.')
    async def stop(self, ctx):
        guild_id = ctx.guild.id
        
        if ctx.voice_client:
            if guild_id in self.queues:
                self.queues[guild_id].clear()
                
            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                ctx.voice_client.stop()
            
            await ctx.send("🛑 Reprodução interrompida e fila limpa!")
        else:
            await ctx.send("Eu não estou em um canal de voz.")


async def setup(bot):
    await bot.add_cog(MusicCog(bot))