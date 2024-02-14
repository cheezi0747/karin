import asyncio
import discord
from datetime import datetime, timedelta, timezone
from discord.ext import commands
import os

BUY_CHANNEL_ID = int(os.getenv("BUY_CHANNEL_ID"))
SELL_CHANNEL_ID = int(os.getenv("SELL_CHANNEL_ID"))
ARCHIVE_CHANNEL_ID = int(os.getenv("ARCHIVE_CHANNEL_ID"))

OLD_THREAD_ALERT_TITLE=os.getenv("OLD_THREAD_ALERT_TITLE")
OLD_THREAD_ALERT_BODY=os.getenv("OLD_THREAD_ALERT_BODY")

class Cleanup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_thread_age_and_delete(self):
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)

        async def process_channel(channel_id):
            channel = discord.utils.get(self.bot.get_all_channels(), id=channel_id)
            if channel:
                for thread in channel.threads:
                    if thread.created_at < thirty_days_ago:
                        await self.delete_thread(thread)

        await asyncio.gather(
            process_channel(BUY_CHANNEL_ID),
            process_channel(SELL_CHANNEL_ID)
        )

    async def delete_thread(self, thread):
        await self.send_embed_message(thread.owner,OLD_THREAD_ALERT_TITLE,OLD_THREAD_ALERT_BODY, discord.Color.purple())
        await thread.delete()

    async def send_embed_message(self, user, title, description, color):
        embed = discord.Embed(title=title, description=description, color=color)
        await user.send(embed=embed)

    async def setup_check_thread_age_and_delete_task(self):
        while True:
            await self.check_thread_age_and_delete()
            await asyncio.sleep(3600) # Check every hour

async def setup(bot):
    cleanup_cog = Cleanup(bot)
    await bot.add_cog(cleanup_cog)
    await cleanup_cog.setup_check_thread_age_and_delete_task()