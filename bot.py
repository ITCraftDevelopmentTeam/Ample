from importlib import import_module
from pathlib import Path

import yaml
from discord import Intents
from discord.ext.commands import Bot, Context, Command, HybridCommand

from plugins._lang import text


config = yaml.safe_load(open("./config.yaml"))

intents = Intents.all()
bot = Bot(command_prefix="$", intents=intents)


@bot.command()
async def sync_command(ctx: Context) -> None:
    if str(ctx.author) in config["superusers"]:
        await bot.tree.sync()
        await ctx.send(text("sync-command"))


for path in Path("plugins").glob("[!_]*"):
    module = import_module(f"plugins.{path.stem}")
    commands = getattr(module, "__commands", set())
    hybrid_commands = getattr(module, "__hybrid_commands", set())

    for command in commands:
        bot.add_command(Command(command))
    for hybrid_command in hybrid_commands:
        bot.add_command(HybridCommand(hybrid_command))


bot.run(config["token"])
