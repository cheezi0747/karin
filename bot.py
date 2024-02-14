import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the Discord token from the environment
TOKEN = os.getenv('DISCORD_TOKEN')

# Define the intents
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

# Load the market module
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await load_modules()

async def load_modules():
    try:
        await bot.load_extension('cleanup')
        await bot.load_extension('market')
    
    except Exception as e:
        print(f'Failed to load modules: {e}')

# Run the bot with your token
bot.run(TOKEN)
