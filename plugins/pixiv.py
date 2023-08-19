import re
from datetime import datetime
from dateutil.tz import gettz
from functools import partial
from io import BytesIO
from random import choice

import aiohttp
from discord import File
from discord.ext.commands import Context

from ._command import hybrid_command
from ._lang import text


@hybrid_command
async def pixiv(
    ctx: Context,
    pid: int,
    p: int = 0
) -> None:
    """Get a image by pid."""

    ext = choice(["png", "jpg", "gif"])     # All of these are OK.
    url = text(".proxy-url", pid=pid, p=p, ext=ext)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if "x-origin-url" not in response.headers.keys():
                await ctx.send(text(".no-exist"))
                return
            await ctx.defer()
            origin_url = response.headers["x-origin-url"]
            content = await response.read()
        pattern = (
            r"https://i\.pximg\.net/img-original/img/"
            r"(\d{4})/(\d{2})/(\d{2})/(\d{2})/(\d{2})/(\d{2})"
            r"/(\d+)_p(\d+)\.(png|jpg|gif)"
        )
        assert (match := re.match(pattern, origin_url))
        *times, pid, p, ext = [match[i] for i in range(1, 10)]
        time = datetime(*map(int, times), 0, gettz("Japan"))
        _text = partial(text, time=time, pid=pid, p=int(p), ext=ext, url=url)
        await ctx.send(_text(".text"), file=File(
            BytesIO(content),
            filename=_text(".filename"),
            description=_text(".description")
        ))
