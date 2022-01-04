# by @Friendly_userbot - @ForceBrain

from asyncio import sleep
import logging
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class MsgEditMod(loader.Module):
    """Редактирует сообщение"""  # Translateable due to @loader.tds
    strings = {"name": "MsgEdit"}

    @loader.unrestricted  # Security setting to change who can use the command (defaults to owner | sudo)
    async def msgeditcmd(self, message):
        """.msgedit раз два"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, "Нет слов")
            return
        if len(args) == 1:
            await utils.answer(message, "Нужно минимум два слова")
            return
        big = False if args == [] else True
        for _ in range(10):
           for c in args:
               await message.edit(c+("" if not big else "&NoBreak;"))
               await sleep(0.4)
