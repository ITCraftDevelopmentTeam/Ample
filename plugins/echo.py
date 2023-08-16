import re

from discord.ext.commands import Context

from ._lang import parse


async def echo(ctx: Context, message: str) -> None:
    message = re.sub(
        "```py(thon)?(.*?)```", string=message, flags=re.DOTALL,
        repl=lambda match: "{{" + (match[2] or "") + "}}"
    )
    await ctx.send("\n".join(map(
        lambda x: f"> {x}",
        parse(message, ctx).split("\n")
    )))
