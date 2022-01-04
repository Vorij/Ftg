
# by @Friendly_userbot - @IO3EP
import asyncio
import ast
import time
import logging
from io import BytesIO
from telethon.tl import functions
from .. import loader, utils

logger = logging.getLogger(__name__)

try:
    from PIL import Image
except ImportError:
    pil_installed = False
else:
    pil_installed = True


@loader.tds
class AutoProfileMod(loader.Module):
    """Автоматическое изменения вашего профиля"""
    strings = {"name": "AutoProfile",
               "missing_pil": "<b>Вы не установили Pillow</b>",
               "missing_pfp": "<b>У Вас нет фото в профиле, которое нужно поворачивать</b>",
               "invalid_args": "<b>Отсутствуют параметры, прочтите документацию:</b>\n<code>.help AutoProfile</code>",
               "invalid_degrees": "<b>Недопустимое количество градусов для поворота фото, прочтите документацию:</b>\n<code>.help AutoProfile</code>",
               "invalid_delete": "<b>Уточните, удалять предыдущие фото или нет</b>\n<code>.autopfp 60 True/False</code>",
               "enabled_pfp": "<b>Вращение фото в профиле включено</b>",
               "pfp_not_enabled": "<b>Вращение фото в профиле НЕ включено</b>",
               "pfp_disabled": "<b>Вращение фото в профиле отключено</b>",
               "missing_time": "<b>Вы не указали:</b> <code>{time}</code>",
               "enabled_bio": "<b>Время в био включено</b>",
               "bio_not_enabled": "<b>Время в био НЕ включено</b>",
               "disabled_bio": "<b>Время в био отключено</b>",
               "enabled_name": "<b>Время в имени включено</b>",
               "name_not_enabled": "<b>Время в имени НЕ включено</b>",
               "disabled_name": "<b>Время в имени отключено</b>",
               "how_many_pfps": "<b>Укажите, сколько фото в профиле нужно удалить</b>\n<code>.delpfp 1</code>",
               "invalid_pfp_count": "<b>Недействительное количество фото в профиле, которые нужно удалить</b>\n<code>.delpfp 1</code>",
               "removed_pfps": "<b>В профиле удаленно фото {}</b>"}

    def __init__(self):
        self.bio_enabled = False
        self.name_enabled = False
        self.pfp_enabled = False
        self.raw_bio = None
        self.raw_name = None

    async def client_ready(self, client, db):
        self.client = client

    async def autopfpcmd(self, message):
        """Поворачивает фото каждую минуту:
		   .autopfp <градусы> <удалять предыдущие фото или нет>

		   Градусы: 60, 10, так далее
		   Удалять: True/False"""

        if not pil_installed:
            return await utils.answer(message, self.strings("missing_pil", message))

        if not await self.client.get_profile_photos("me", limit=1):
            return await utils.answer(message, self.strings("missing_pfp", message))

        msg = utils.get_args(message)
        if len(msg) != 2:
            return await utils.answer(message, self.strings("invalid_args", message))

        try:
            degrees = int(msg[0])
        except ValueError:
            return await utils.answer(message, self.strings("invalid_degrees", message))

        try:
            delete_previous = ast.literal_eval(msg[1])
        except (ValueError, SyntaxError):
            return await utils.answer(message, self.strings("invalid_delete", message))

        with BytesIO() as pfp:
            await self.client.download_profile_photo("me", file=pfp)
            raw_pfp = Image.open(pfp)

            self.pfp_enabled = True
            pfp_degree = 0
            await self.allmodules.log("start_autopfp")
            await utils.answer(message, self.strings("enabled_pfp", message))

            while self.pfp_enabled:
                pfp_degree = (pfp_degree + degrees) % 360
                rotated = raw_pfp.rotate(pfp_degree)
                with BytesIO() as buf:
                    rotated.save(buf, format="JPEG")
                    buf.seek(0)

                    if delete_previous:
                        await self.client(functions.photos.
                                          DeletePhotosRequest(await self.client.get_profile_photos("me", limit=1)))

                    await self.client(functions.photos.UploadProfilePhotoRequest(await self.client.upload_file(buf)))
                    buf.close()
                await asyncio.sleep(60)

    async def stopautopfpcmd(self, message):
        """Отключает поворот фото"""

        if self.pfp_enabled is False:
            return await utils.answer(message, self.strings("pfp_not_enabled", message))
        else:
            self.pfp_enabled = False

            await self.client(functions.photos.DeletePhotosRequest(
                await self.client.get_profile_photos("me", limit=1)
            ))
            await self.allmodules.log("stop_autopfp")
            await utils.answer(message, self.strings("pfp_disabled", message))

    async def autobiocmd(self, message):
        """Включает время в био:
			.autobio '<любой текст {time}>'"""

        msg = utils.get_args(message)
        if len(msg) != 1:
            return await utils.answer(message, self.strings("invalid_args", message))
        raw_bio = msg[0]
        if "{time}" not in raw_bio:
            return await utils.answer(message, self.strings("missing_time", message))

        self.bio_enabled = True
        self.raw_bio = raw_bio
        await self.allmodules.log("start_autobio")
        await utils.answer(message, self.strings("enabled_bio", message))

        while self.bio_enabled is True:
            current_time = time.strftime("%H:%M")
            bio = raw_bio.format(time=current_time)
            await self.client(functions.account.UpdateProfileRequest(
                about=bio
            ))
            await asyncio.sleep(60)

    async def stopautobiocmd(self, message):
        """Отключает время в био"""

        if self.bio_enabled is False:
            return await utils.answer(message, self.strings("bio_not_enabled", message))
        else:
            self.bio_enabled = False
            await self.allmodules.log("stop_autobio")
            await utils.answer(message, self.strings("disabled_bio", message))
            await self.client(functions.account.UpdateProfileRequest(about=self.raw_bio.format(time="")))

    async def autonamecmd(self, message):
        """Включает время в имени:
			.autoname '<любое имя {time}>'"""

        msg = utils.get_args(message)
        if len(msg) != 1:
            return await utils.answer(message, self.strings("invalid_args", message))
        raw_name = msg[0]
        if "{time}" not in raw_name:
            return await utils.answer(message, self.strings("missing_time", message))

        self.name_enabled = True
        self.raw_name = raw_name
        await self.allmodules.log("start_autoname")
        await utils.answer(message, self.strings("enabled_name", message))

        while self.name_enabled is True:
            current_time = time.strftime("%H:%M")
            name = raw_name.format(time=current_time)
            await self.client(functions.account.UpdateProfileRequest(
                first_name=name
            ))
            await asyncio.sleep(60)

    async def stopautonamecmd(self, message):
        """Отключает время в имени"""

        if self.name_enabled is False:
            return await utils.answer(message, self.strings("name_not_enabled", message))
        else:
            self.name_enabled = False
            await self.allmodules.log("stop_autoname")
            await utils.answer(message, self.strings("disabled_name", message))
            await self.client(functions.account.UpdateProfileRequest(
                first_name=self.raw_name.format(time="")
            ))

    async def delpfpcmd(self, message):
        """Удаляет в профиле фото:
		.delpfp <количество в цифрах>"""

        args = utils.get_args(message)
        if not args:
            return await utils.answer(message, self.strings("how_many_pfps", message))
        try:
            pfps_count = int(args[0])
        except ValueError:
            return await utils.answer(message, self.strings("invalid_pfp_count", message))
        if pfps_count < 0:
            return await utils.answer(message, self.strings("invalid_pfp_count", message))
        if pfps_count == 0:
            pfps_count = None

        to_delete = await self.client.get_profile_photos("me", limit=pfps_count)
        await self.client(functions.photos.DeletePhotosRequest(to_delete))

        await self.allmodules.log("delpfp")
        await utils.answer(message, self.strings("removed_pfps", message).format(len(to_delete)))
