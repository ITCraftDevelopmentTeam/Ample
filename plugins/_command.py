import sys


def command(func):
    frame = sys._getframe(1)
    if "__commands" not in frame.f_globals.keys():
        frame.f_globals["__commands"] = set()
    frame.f_globals["__commands"].add(func)
    return func


def hybrid_command(func):
    frame = sys._getframe(1)
    if "__hybrid_commands" not in frame.f_globals.keys():
        frame.f_globals["__hybrid_commands"] = set()
    frame.f_globals["__hybrid_commands"].add(func)
    return func
