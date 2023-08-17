from pathlib import Path

import yaml
from discord import Intents
from discord.ext.commands import Bot, Context

from plugins._lang import text


config = yaml.safe_load(open("./config.yaml"))

intents = Intents.all()
bot = Bot(command_prefix="$", intents=intents)


@bot.command()
async def sync_command(ctx: Context) -> None:
    assert ctx.author.name in config["superusers"]
    await bot.tree.sync()
    await ctx.send(text("sync-command"))


for path in Path("plugins").glob("[!_]*"):
    exec(f"from plugins.{path.stem} import {path.stem} as command")
    bot.hybrid_command(path.stem)(eval("command"))
    exec("del command")

bot.run(config["token"])
