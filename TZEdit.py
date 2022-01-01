# by @Friendly_user_bot - @ForceBrain

import logging
from .. import loader, utils
import time, os

logger = logging.getLogger(__name__)

@loader.tds
class TZEditMod(loader.Module):
    """Меняет часовой пояс. Модуль сделал @Friendly_user_bot - @ForceBrain"""  # Translateable due to @loader.tds
    strings = {"name": "TZEdit"}

    @loader.unrestricted  # Security setting to change who can use the command (defaults to owner | sudo)
    async def tzcmd(self, message):
        """.tz Europe/Moscow\nen.m.wikipedia.org/wiki/List_of_tz_database_time_zones"""
        args = utils.get_args(message)
        if not args or len(args) > 1:
            await utils.answer(message, ".tz Europe/Moscow\nen.m.wikipedia.org/wiki/List_of_tz_database_time_zones")
        else:
            time.strftime('%X %x %Z')
            os.environ['TZ'] = utils.get_args_raw(message)
            time.tzset()
            await utils.answer(message, utils.get_args_raw(message) + '\n' + time.strftime('%X %x %Z'))

