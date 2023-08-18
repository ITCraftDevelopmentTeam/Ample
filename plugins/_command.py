import sys


def command(func):
    frame = sys._getframe(1)
    if "__discord_commands" not in frame.f_globals.keys():
        frame.f_globals["__discord_commands"] = set()
    frame.f_globals["__discord_commands"].add(func)
    return func


def hybrid_command(func):
    frame = sys._getframe(1)
    if "__discord_hybrid_commands" not in frame.f_globals.keys():
        frame.f_globals["__discord_hybrid_commands"] = set()
    frame.f_globals["__discord_hybrid_commands"].add(func)
    return func
