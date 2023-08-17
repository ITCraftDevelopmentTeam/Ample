from datetime import datetime
from dateutil.tz import gettz as tz
from functools import partial
from io import BytesIO
from typing import Literal, cast

import aiohttp
from discord import File
from discord.ext.commands import Context

from ._lang import text


async def setu(
    ctx: Context,
    r18: Literal["False", "True", "All"] = "False",
    num: int = 1,
    uid: int = 0,
    keyword: str = "",
    tag: str = "",
    exclude_ai: bool = False
) -> None:
    if not ctx.channel.nsfw and r18 != "False":
        r18 = "False"
        await ctx.send(text(".sfw"))
    else:
        await ctx.defer()
    async with aiohttp.ClientSession() as session:
        url = "https://api.lolicon.app/setu/v2"
        params = dict(filter(lambda x: x[1], {
            "r18": ["False", "True", "All"].index(r18),
            "num": num,
            "uid": uid,
            "keyword": keyword,
            "tag": tag.split("&"),
            "excludeAI": "true" if exclude_ai else None
        }.items()))
        async with session.get(url=url, params=params) as response:
            data: dict = await response.json()
        if data["error"]:
            await ctx.send(text(".error.api", data=data))
            return
        if not data["data"]:
            await ctx.send(text(".error.no-exist", data=data))
            return
        for pic in cast(list[dict], data["data"]):
            time = datetime.fromtimestamp(pic["uploadDate"] / 1000, tz("PRC"))
            _text = partial(text, **pic, time=time)
            url = cast(dict[str, str], pic["urls"])["original"]
            async with session.get(url) as response:
                content = await response.read()
            if len(content) == 58:
                url = _text("pixiv.proxy-url", **pic)
                async with session.get(url) as response:
                    content = await response.read()
            await ctx.send(_text(".text", url=url), file=File(
                BytesIO(content),
                filename=_text(".filename"),
                description=_text(".description")
            ))
