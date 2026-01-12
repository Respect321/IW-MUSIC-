import discord
from discord.ext import commands
import yt_dlp
import os
import asyncio

# 1. Bot Setup aur Permissions
intents = discord.Intents.default()
intents.message_content = True  # Taki bot commands padh sake
bot = commands.Bot(command_prefix='!', intents=intents)

# 2. Music Download aur Audio Settings
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# 3. Play Command
@bot.command()
async def play(ctx, *, search: str):
    # Voice channel check
    if not ctx.author.voice:
        return await ctx.send("Pehle kisi voice channel mein aao!")

    # Connect to voice
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    
    async with ctx.typing():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                # YouTube par search karega agar link nahi hai toh
                info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
                url = info['url']
                title = info['title']
                source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
                
                ctx.voice_client.stop()
                ctx.voice_client.play(source)
                await ctx.send(f"Now playing: **{title}** 🎶")
            except Exception as e:
                await ctx.send(f"Error: Gaana nahi mil raha.")

# 4. Stop Command
@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Bot disconnect ho gaya!")
    else:
        await ctx.send("Main kisi voice channel mein nahi hoon.")

# 5. Bot Ready Message
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

# 6. Run Bot (Railway Variable TOKEN use karega)
token = os.environ.get('TOKEN')
if token:
    bot.run(token)
else:
    print("Error: TOKEN variable nahi mila! Railway settings check karein.")
  
