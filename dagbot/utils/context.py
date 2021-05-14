import discord
from discord.ext import commands


class MyContext(commands.Context):
    async def send(self, content=None, *, tts=False,
                   embed: discord.Embed = None, file=None, files=None,
                   delete_after=None, nonce=None, allowed_mentions=None):
        bot = self.bot

        if content:
            for key, val in bot.data.items():
                if key not in ["imgflipuser", "database"]:
                    content = content.replace(val, f"[ Omitted {key} ]")
        else:
            content = ""
        if embed:
            desc = embed.description
            if desc:
                for key, val in bot.data.items():
                    if key not in ["imgflipuser", "database"]:
                        desc = desc.replace(val, f"[ Ommited {key}]")
                embed.description = desc
            embed.color = self.guild.me.color
            if len(embed) > 2048:
                return await super().send("This embed is a little too large "
                                          "to send.")
        if len(content) > 2000:
            return await super().send("Little long there woul you like me to "
                                      "upload this?")

        return await super().send(content, file=file, embed=embed, files=files,
                                  delete_after=delete_after, nonce=nonce,
                                  allowed_mentions=allowed_mentions, tts=tts)

    async def safe_send(self, yes):
        await super().send("Yes this method is cool")
