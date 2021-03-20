from contextlib import suppress

import discord
from discord.ext import commands
from validator_collection import checkers

from dagbot.utils.exceptions import NoImageFound, NoMemberFound

member_converter = commands.UserConverter()
emoji_converter = commands.EmojiConverter()


class UrlValidator:
    async def validate(self, url):
        return checkers.is_url(str(url))


class BetterMemberConverter(commands.Converter):
    async def convert(self, ctx, argument):
        with suppress(Exception):
            mem = await member_converter.convert(ctx, argument)
            return mem
        with suppress(discord.HTTPException):
            mem = await ctx.bot.fetch_user(argument)
            return mem
        raise NoMemberFound(str(argument))


class ImageConverter(commands.Converter):
    async def convert(self, ctx, argument):
        with suppress(NoMemberFound):
            mem = await BetterMemberConverter().convert(ctx, argument)
            return (str(mem.avatar_url_as(static_format='png', size=1024)))
        with suppress(Exception):
            emoji = await emoji_converter.convert(ctx, str(argument))
            return (str(emoji.url))
        if ctx.message.attachments:
            with suppress(Exception):
                return ctx.message.attachments[0].url.replace(".webp", ".png")
        if checkers.is_url(str(argument)):
            return str(argument)
        raise NoImageFound('')


class StaticImageConverter(commands.Converter):
    async def convert(self, ctx, argument):
        with suppress(NoMemberFound):
            mem = await BetterMemberConverter().convert(ctx, argument)
            return (str(mem.avatar_url_as(format="png", static_format='png', size=1024)))
        with suppress(Exception):
            emoji = await emoji_converter.convert(ctx, str(argument))
            return (str(emoji.url_as(format="png")))
        if ctx.message.attachments:
            with suppress(Exception):
                return ctx.message.attachments[0].url.replace(".webp", ".png")
        if checkers.is_url(str(argument)):
            return str(argument)
        raise NoImageFound('')
