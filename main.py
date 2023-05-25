bot_token = 'MTExMTM4NTI1MjA0OTQ2NTM4Ng.GMufO7.g0CYvdyK7duHrWfllyFP6Bw4pYNLsRWcnNa-Uk'
permissions_integer = 35201790082624
client_id = 1111385252049465386
client_secret = "MQ31zXnTiOQqcgnPzjscVZ3Uor8PYF3-'"
oauth_url = 'https://discord.com/oauth2/authorize?client_id=1111385252049465386&scope=bot&permissions=35201790082624'
oauth_url = f"https://discord.com/oauth2/authorize?client_id={client_id}&scope=bot&permissions={permissions_integer}"



import discord
from discord.ext import commands
import yt_dlp as youtube_dl

intents = discord.Intents(131071)

class MyClient(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        print(f"Received a message from {message.author}: {message.content} in Channel: {message.channel}")
        await self.process_commands(message)

bot = MyClient(command_prefix='!', intents=intents)

@bot.command()
async def play(ctx, *, query=None):
    if query is None:
        await ctx.send("Please provide a search query or YouTube video URL.")
        return

    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client:
        if voice_client.is_playing():
            await ctx.send("I'm currently playing a song.")
            return
        elif voice_client.channel != ctx.author.voice.channel:
            await voice_client.disconnect()
        # else:
        #     voice_client.stop()
    else:
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("You must be in a voice channel to use this command.")
            return
        voice_client = await voice_channel.connect()

    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'default_search': 'ytsearch',
        'ignoreerrors': True,  # Ignore extraction errors
        'download': True  # Download audio in the background
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                url = info['entries'][0]['url']
                # url = info['requested_downloads'][0]['formats'][0]['url']
                print(url)
                FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=1"'}
                voice_client.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
            else:
                await ctx.send("No videos found for the provided query.")
        except youtube_dl.utils.RegexNotFoundError as e:
            print(e)
            await ctx.send("Failed to extract video information. Please try again with a different video.")
        except TypeError as e:
            print(e)
            await ctx.send("Failed to retrieve video URL. Please try again with a different video.")

@bot.command()
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Music playback stopped")
    else:
        await ctx.send("There is no music playing.")

@bot.command()
async def leave(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_connected():
        await voice_client.disconnect()

@bot.command()
async def pause(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Music playback paused.")
    else:
        await ctx.send("There is no music playing.")

@bot.command()
async def resume(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Music playback resumed.")
    else:
        await ctx.send("There is no paused music.")

@bot.command()
async def skip(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Skipped the current song.")
    else:
        await ctx.send("No song is currently playing.")

bot.run(bot_token)
