import re
from datetime import datetime
from dateutil.tz import gettz as tz
from functools import partial
from io import BytesIO
from random import choice

import aiohttp
from discord import File
from discord.ext.commands import Context

from ._lang import text


async def pixiv(
    ctx: Context,
    pid: int,
    p: int = 0
) -> None:
    ext = choice(["png", "jpg", "gif"])     # All of these are OK.
    url = text(".proxy-url", pid=pid, p=p, ext=ext)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            await ctx.defer()
            content = await response.read()
            origin_url = response.headers["x-origin-url"]
        pattern = (
            r"https://i\.pximg\.net/img-original/img/"
            r"(\d{4})/(\d{2})/(\d{2})/(\d{2})/(\d{2})/(\d{2})"
            r"/(\d+)_p(\d+)\.(png|jpg|gif)"
        )
        assert (matched := re.match(pattern, origin_url))
        matcheds = [matched[i] for i in range(1, 10)]
        for i in range(8):
            matcheds[i] = int(matcheds[i])
        year, month, day, hour, minute, second, pid, p, ext = matcheds
        time = datetime(year, month, day, hour, minute, second, 0, tz("Japan"))
        _text = partial(text, time=time, pid=pid, p=p, ext=ext, url=url)
        await ctx.send(_text(".text"), file=File(
            BytesIO(content),
            filename=_text(".filename"),
            description=_text(".description")
        ))
