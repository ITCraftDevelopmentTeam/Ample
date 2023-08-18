import re

from discord.ext.commands import Context

from ._command import hybrid_command
from ._lang import parse


@hybrid_command
async def echo(ctx: Context, message: str) -> None:
    """Echo~cho~ho~o~"""
    message = re.sub(
        "```py(thon)?(.*?)```", string=message, flags=re.DOTALL,
        repl=lambda match: "{{" + (match[2] or "") + "}}"
    )
    await ctx.send("\n".join(map(
        lambda x: f"> {x}",
        parse(message, ctx).split("\n")
    )))
