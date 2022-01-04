
# by @Friendly_userbot - @Force_Brain
import io
from .. import loader, utils

@loader.tds
class SaverMod(loader.Module):
    """Сохраняет в избранное самоуничтожающиеся фото и видео. Модуль @Friendly_userbot - @ForceBrain"""
    strings = {"name": "SavesDel"}

    async def client_ready(self, client, db):
        self.db = db

    @loader.owner
    async def savedelcmd(self, m):
        ".savedel <ответ на фото или видео>"
        reply = await m.get_reply_message()
        if not reply or not reply.media or not reply.media.ttl_seconds:
            return await m.edit("Ответ на фото или видео")
        await m.delete()
        new = io.BytesIO(await reply.download_media(bytes))
        new.name = reply if getattr(reply, 'document', reply.file.ext) is None else reply.file.id + reply.file.ext
        await m.client.send_file("me", new, caption=f"<b>[SavesDel]</b> Вы сохранили {'@'+reply.sender.username if reply.sender.username else reply.sender.first_name} <code>{reply.sender.id}</code>\nСекунд: <b>{reply.media.ttl_seconds}</b>")

    @loader.owner
    async def savesdelcmd(self, m):
        ".savesdel - Включает и отключает во всех диалогах автосохранение"
        new_val = not self.db.get("SavesDel", "state", False)
        self.db.set("SavesDel", "state", new_val)
        await utils.answer(m, f"<b>[SavesDel]</b> Статус <pre>{new_val}</pre>")

    async def watcher(self, m):
        if m and m.media and m.media.ttl_seconds and self.db.get("SavesDel", "state", False):
            new = io.BytesIO(await m.download_media(bytes))
            new.name = m if getattr(m, 'document', m.file.ext) is None else m.file.id + m.file.ext
            await m.client.send_file("me", new, caption=f"<b>[SavesDel]</b> Сохранил {'@'+m.sender.username if m.sender.username else m.sender.first_name} | <code>{m.sender.id}</code>\nСекунд: <b>{m.media.ttl_seconds}</b>")
