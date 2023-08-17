from discord.ext.commands import Context

from ._lang import text, LangTag, lang_users


async def lang(ctx: Context, lang: LangTag) -> None:
    lang_users[ctx.author.name] = lang
    await ctx.send(text(".set", lang=lang))
