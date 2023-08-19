from datetime import datetime
from dateutil.tz import gettz
from functools import partial
from io import BytesIO
from typing import Literal, Optional, cast

import aiohttp
from discord import File
from discord.ext.commands import Context

from ._command import hybrid_command
from ._lang import text
from ._store import Json


@hybrid_command
async def setu(
    ctx: Context,
    r18: Literal["False", "True", "All"] = "False",
    num: Optional[int] = None,
    uid: Optional[int] = None,
    keyword: Optional[str] = None,
    tag: Optional[str] = None,
    exclude_ai: bool = False
) -> None:
    """Get a random `setu`."""

    # for channels that are `sfw`
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
            "tag": tag and tag.split("&"),
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

        Json("setu.history.json", list)[str(ctx.author)].append(params)
        Json("setu.count.json", int)[str(ctx.author)] += len(data["data"])

        for pic in cast(list[dict], data["data"]):
            time = datetime.fromtimestamp(pic["uploadDate"]/1000, gettz("PRC"))
            _text = partial(text, **pic, time=time)
            url = cast(dict[str, str], pic["urls"])["original"]
            async with session.get(url) as response:
                content = await response.read()

            if not response.headers["Content-Type"].startswith("image/"):
                url = _text("pixiv.proxy-url", **pic)
                async with session.get(url) as response:
                    content = await response.read()

            await ctx.send(_text(".text", url=url), file=File(
                BytesIO(content),
                filename=_text(".filename"),
                description=_text(".description")
            ))


@hybrid_command
async def setu_rank(ctx: Context) -> None:
    """Get the ranking of `setu` usage."""

    await ctx.send(text(".rank", rank=Json("setu.count.json")))
