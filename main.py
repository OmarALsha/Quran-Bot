import os
import discord
from discord.ext import commands

# Load OPUS library
discord.opus.load_opus('libopus.so.0')
if not discord.opus.is_loaded():
    print("❌ Opus failed to load.")
else:
    print("✅ Opus loaded successfully.")

# Bot credentials
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
VC_CHANNEL_ID = int(os.getenv("VC_CHANNEL_ID"))

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ Guild not found.")
        return
    channel = guild.get_channel(VC_CHANNEL_ID)
    if not isinstance(channel, discord.VoiceChannel):
        print("❌ Channel not valid.")
        return
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio("https://qurango.net/radio/makkah"),
            after=lambda e: print("✅ Done playing"))

bot.run(TOKEN)
