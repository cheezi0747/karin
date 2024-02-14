import os
import discord
from discord.ext import commands
import asyncio
import re

BUY_CHANNEL_ID = int(os.getenv("BUY_CHANNEL_ID"))
SELL_CHANNEL_ID = int(os.getenv("SELL_CHANNEL_ID"))
ARCHIVE_CHANNEL_ID = int(os.getenv("ARCHIVE_CHANNEL_ID"))

PRICE_RECOMMENDATION_TITLE = os.getenv("PRICE_RECOMMENDATION_TITLE")
PRICE_RECOMMENDATION_MESSAGE = os.getenv("PRICE_RECOMMENDATION_MESSAGE")

INVALID_REQUEST_TITLE = os.getenv("INVALID_REQUEST_TITLE")
THREAD_MUST_CONTAIN_IMAGE_MESSAGE = os.getenv("THREAD_MUST_CONTAIN_IMAGE_MESSAGE")
EXISTING_THREAD_ERROR_MESSAGE = os.getenv("EXISTING_THREAD_ERROR_MESSAGE")

channel_colors = {
    SELL_CHANNEL_ID: discord.Color.pink(),
    BUY_CHANNEL_ID: discord.Color.blue()
}

price_patterns = [
    r'\b\d+\s*(kr|kronor|sek|\$)\b',  # Matches numbers followed by currency
    r'(\$|:-)\s*\d+',                   # Matches currency symbols followed by numbers
]

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_deleted_threads = set()

    async def delay(self):
        await asyncio.sleep(1)

    async def send_embed_message(self, user, title, description, color):
        embed = discord.Embed(title=title, description=description, color=color)
        await user.send(embed=embed)

    async def process_message(self, thread, is_sell_channel):
        await self.check_for_existing_thread(thread)
        if is_sell_channel:
            await self.check_attachment(thread)
            await self.check_if_thread_contains_price(thread)
        await self.delay()

    async def check_if_thread_contains_price(self, thread):
        message = thread.starter_message.content
        if not any(re.search(pattern, message, re.IGNORECASE) for pattern in price_patterns):
            await self.send_embed_message(thread.owner, PRICE_RECOMMENDATION_TITLE, PRICE_RECOMMENDATION_MESSAGE, discord.Color.yellow())

    async def check_attachment(self, thread):
        if not thread.starter_message.attachments or \
                not any(attachment.content_type.startswith('image') for attachment in thread.starter_message.attachments):
            await self.delete_thread(thread)
            await self.send_embed_message(thread.owner, INVALID_REQUEST_TITLE, THREAD_MUST_CONTAIN_IMAGE_MESSAGE, discord.Color.red())

    async def check_for_existing_thread(self, thread):
        for existing_thread in thread.parent.threads:
            if existing_thread.owner_id == thread.owner_id and existing_thread.id != thread.id:
                await self.delete_thread(thread)
                await self.send_embed_message(thread.owner, INVALID_REQUEST_TITLE, EXISTING_THREAD_ERROR_MESSAGE.format(thread=thread, existing_thread=existing_thread), discord.Color.red())

    async def delete_thread(self, thread):
        self.bot_deleted_threads.add(thread.id)
        await thread.delete()

    async def post_to_archive(self, title, content, guild, channel):
        archive = guild.get_channel(ARCHIVE_CHANNEL_ID)
        embed = discord.Embed(title=title, description=content, color=channel_colors.get(channel))
        await archive.send(embed=embed)

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        await self.delay()
        is_sell_channel = thread.parent.id == SELL_CHANNEL_ID
        if is_sell_channel or thread.parent.id == BUY_CHANNEL_ID:
            await self.process_message(thread, is_sell_channel)

    @commands.Cog.listener()
    async def on_raw_thread_delete(self, raw_thread):
        await self.delay()
        if raw_thread.parent_id in (BUY_CHANNEL_ID, SELL_CHANNEL_ID):
            if raw_thread.thread.starter_message:
                if raw_thread.thread_id in self.bot_deleted_threads:
                    self.bot_deleted_threads.remove(raw_thread.thread_id)
                    return
                await self.post_to_archive(raw_thread.thread.name,raw_thread.thread.starter_message.content, raw_thread.thread.guild, raw_thread.parent_id)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await self.delay()
        message_thread = message.channel
        if type(message_thread) is discord.TextChannel:
            return
        if message_thread.parent_id in (BUY_CHANNEL_ID, SELL_CHANNEL_ID) \
              and (not message_thread.starter_message or message.id == message_thread.starter_message.id):
                await self.post_to_archive(message_thread.name, message.content, message_thread.guild, message_thread.parent_id)
                await self.delete_thread(message_thread)

async def setup(bot):
    await bot.add_cog(Market(bot))
