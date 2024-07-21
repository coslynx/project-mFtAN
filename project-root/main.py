import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Create bot instance
intents = discord.Intents.default()
intents.members = True  # Enable member intents to access member data
intents.message_content = True  # Enable message content intents for message processing
bot = commands.Bot(command_prefix="!", intents=intents)

# Load cogs
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded cog: {filename[:-3]}")

# Connect to the database
# ... (Implement database connection logic using PyMySQL, psycopg2, or pymongo)

# Start the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)