import os
import discord
from discord.ext import commands

# Get environment variables
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
VC_CHANNEL_ID = int(os.getenv("VC_CHANNEL_ID"))

# Check and load Opus
if not discord.opus.is_loaded():
    try:
        discord.opus.load_opus("libopus.so.0")
        print("✅ Opus loaded successfully.")
    except Exception as e:
        print(f"❌ Failed to load Opus: {e}")
else:
    print("✅ Opus already loaded.")

# Set up intents
intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

# Set up bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ Guild not found. Check GUILD_ID.")
        return

    channel = guild.get_channel(VC_CHANNEL_ID)
    if not isinstance(channel, discord.VoiceChannel):
        print("❌ Voice channel not found or invalid. Check VC_CHANNEL_ID.")
        return

    try:
        vc = await channel.connect()
        vc.play(
            discord.FFmpegPCMAudio("https://qurango.net/radio/makkah"),
            after=lambda e: print("✅ Finished playing.")
        )
        print("🎧 Now playing Quran radio in voice channel.")
    except Exception as e:
        print(f"❌ Failed to connect/play audio: {e}")

bot.run(TOKEN)
