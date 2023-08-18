from discord.ext.commands import Context

from ._command import hybrid_command
from ._lang import text, LangTag, lang_users


@hybrid_command
async def lang(ctx: Context, lang: LangTag) -> None:
    """Set your local language."""
    lang_users[ctx.author.name] = lang
    await ctx.send(text(".set", lang=lang))
