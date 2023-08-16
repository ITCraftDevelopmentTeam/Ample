from datetime import datetime
from dateutil.tz import gettz
from functools import partial
from io import BytesIO
from typing import Literal, Optional, cast

import aiohttp
from discord import File
from discord.ext.commands import Context

from ._lang import text


tz = gettz("PRC")


async def setu(
    ctx: Context,
    r18: Literal["False", "True", "All"] = "False",
    num: Optional[int] = None,
    uid: Optional[int] = None,
    keyword: Optional[str] = None,
    tag: Optional[str] = None,
    exclude_ai: Optional[bool] = None
) -> None:
    _text = partial(text, ctx)
    if not ctx.channel.nsfw and r18 != "False":
        r18 = "False"
        await ctx.send(_text("setu.sfw"))
    else:
        await ctx.defer()
    async with aiohttp.ClientSession() as session:
        url = "https://api.lolicon.app/setu/v2"
        params = dict(filter(lambda x: x[1], {
            "r18": ["False", "True", "All"].index(r18),
            "num": num,
            "uid": uid,
            "keyword": keyword,
            "tag": tag,
            "excludeAI": "true" if exclude_ai else None
        }.items()))
        async with session.get(url=url, params=params) as response:
            data: dict = await response.json()
        if data["error"]:
            await ctx.send(_text("setu.error.api", data=data))
            return
        for pic in cast(list[dict], data["data"]):
            time = datetime.fromtimestamp(pic["uploadDate"] / 1000, tz)
            _text_ = partial(_text, **pic, time=time)
            url = cast(dict[str, str], pic["urls"])["original"]
            async with session.get(url) as response:
                content = await response.read()
            if len(content) == 58:
                if (p := pic["p"]):
                    url = f"https://pixiv.re/{pic['pid']}-{p + 1}.{pic['ext']}"
                else:
                    url = f"https://pixiv.re/{pic['pid']}.{pic['ext']}"
                async with session.get(url) as response:
                    content = await response.read()
            await ctx.send(_text_("setu.text", url=url), file=File(
                BytesIO(content),
                filename=_text_("setu.filename"),
                description=_text_("setu.description")
            ))
