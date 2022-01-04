"""
    Copyright 2021 t.me/innocoffee
    Licensed under the Apache License, Version 2.0
    
    Author is not responsible for any consequencies caused by using this
    software or any of its parts. If you have any questions or wishes, feel
    free to contact Dan by sending pm to @innocoffee_alt.
"""

#<3 title: AntiArabBot
#<3 pic: https://img.icons8.com/fluency/48/000000/mosque.png
#<3 desc: В группах удаляет сообщения содержащие арабские символовы, так же форварды(пересылки) от обычных ботов. Модуль перевел на русский и улучшил @Friendly_userbot - @ForceBrain 

from .. import loader, utils
import telethon
import logging
import os
import time
import re

logger = logging.getLogger(__name__)


@loader.tds
class AntiArabBotMod(loader.Module):
    """В группах удаляет сообщения содержащие арабские символовы, так же форварды(пересылки) от обычных ботов. Модуль перевел на русский и улучшил @Friendly_userbot - @ForceBrain"""
    strings = {
        'name': 'AntiArabBot', 
        'as_on': 'Анти-Араб/Бот в этом чате, <b>включен</b>\nПо умолчанию выполняю действие: <b>{}</b>',
        'as_off': 'Анти-Араб/Бот в этом чате, <b>отключен</b>',
        'arab_detected': '👳🏾‍♂ <a href="tg://user?id={}">{}</a> {}\n\n♨️ Достали арабы? напишите мне в лс, я помогу!', 
        'args': 'Вы не указали после команды, какое мне выполнять действие: <code>warn | delmsg | mute | kick | ban</code>',
        'action_set': 'Установлено действие: <b>{}</b>',
        'range_set': 'Текущий лимит <b>{}</b> на <b>{}</b>'
    }

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.me = str((await client.get_me()).id)
        self.chats = db.get('AntiArabBot', 'chats', {})


    async def antiarabcmd(self, message):
        """.antiarab - Включение и отключение в группе"""
        chat = str(utils.get_chat_id(message))
        if chat not in self.chats:
            self.chats[chat] = 'ban'
            await utils.answer(message, self.strings('as_on', message).format('ban'))
        else:
            del self.chats[chat]
            await utils.answer(message, self.strings('as_off', message))

        self.db.set('AntiArabBot', 'chats', self.chats)

    async def arabactioncmd(self, message):
        """.arabaction <warn | delmsg | mute | kick | ban> - Установливает действие в группе"""
        args = utils.get_args_raw(message)
        chat = str(utils.get_chat_id(message))
        if args not in ['warn', 'delmsg', 'mute', 'kick', 'ban']:
            await utils.answer(message, self.strings('args', message))
            return

        self.chats[chat] = args
        self.db.set('AntiArabBot', 'chats', self.chats)
        await utils.answer(message, self.strings('action_set', message).format(args))


    async def arabchatscmd(self, message):
        """.arabchats - Группы где включен Анти-Араб/Бот"""
        res = f"Анти-Араб/Бот включен в группах: <b>{len(self.chats)}</b>👳🏾‍♂\n"
        for chat in self.chats:
            chat_obj = await self.client.get_entity(int(chat))
            if getattr(chat_obj, 'title', False):
                chat_name = chat_obj.title
                action = self.chats[chat]
            else:
                chat_name = chat_obj.first_name

            res += f"<code>{chat_name}</code> - {action}" + "\n"

        await utils.answer(message, res)


    async def watcher(self, message):
        try:
            cid = str(utils.get_chat_id(message))

            if cid not in self.chats:
                return

            action = self.chats[cid]
            user = message.from_id

            user_obj = await self.client.get_entity(int(user))
            user_name = ('@'+user_obj.username if user_obj.username is not None else user)
            isbot = (message.sender.bot if message.sender.bot is False else message.forwards if message.forwards is None else "botfor")
            to_check = getattr(message, 'message', '') + getattr(message, 'caption', '') + (message.forward.chat.title if getattr(message, 'forward', None) is not None and getattr(message.forward, 'chat', None) is not None and getattr(message.forward.chat, 'title', None) is not None else '')
            if isbot == "botfor":
            	await message.delete()
            elif len(re.findall('[\u4e00-\u9fff]+', to_check)) == 0 and len(re.findall('[\u0621-\u064A]+', to_check)) == 0:
                return

            try:
                await message.delete()
            except:
                pass

            self.warn = ('warn' in self.allmodules.commands)

            if action == "delmsg":
                msgdel = await self.client.send_message(int(cid), self.strings('arab_detected').format(user, user_name, '<b>удалил сообщение</b> в этом чате араба'))
                time.sleep(6)
                await msgdel.delete()
            elif action == "kick":
                await self.client.kick_participant(int(cid), int(user))
                msgdel = await self.client.send_message(int(cid), self.strings('arab_detected').format(user, user_name, '<b>кикнул</b> из этого чата араба'))
                time.sleep(5)
                await msgdel.delete()
            elif action == "ban":
                await self.client(telethon.tl.functions.channels.EditBannedRequest(int(cid), int(user), telethon.tl.types.ChatBannedRights(until_date=time.time() + 3600 * 48 + 2, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)))
                msgdel = await self.client.send_message(int(cid), self.strings('arab_detected').format(user, user_name, '<b>дал бан</b> в этом чате арабу'))
                time.sleep(5)
                await msgdel.delete()
            elif action == "mute":
                await self.client(telethon.tl.functions.channels.EditBannedRequest(int(cid), int(user), telethon.tl.types.ChatBannedRights(until_date=time.time() + 3600 * 48 + 2, send_messages=True)))
                msgdel = await self.client.send_message(int(cid), self.strings('arab_detected').format(user, user_name, '<b>дал мут</b> в этом чате арубу'))
                time.sleep(5)
                await msgdel.delete()
            elif action == "warn":
                if not self.warn:
                    await self.client.send_message(int(cid), self.strings('arab_detected').format(user, user_name, '<b>арабские символы запрещены</b> в этом чате'))
                else:
                    warn_msg = await self.client.send_message(int(cid), f'.warn {user} арабские символы')
                    await self.allmodules.commands['warn'](warn_msg)
                    await self.client.send_message(int(cid), self.strings('arab_detected').format(user, user_name, '<b>арабские символы запрещены</b> в этом чате'))
            else:
                await self.client.send_message(int(cid), self.strings('arab_detected').format(user, user_name, 'Просто остынь'))
        except:
            logger.exception('error')
            pass
