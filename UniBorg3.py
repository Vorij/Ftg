# by @Friendly_userbot - @ForceBrain
from asyncio import sleep
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantsBots
from uniborg.util import admin_cmd
from .. import loader, utils

@borg.on(admin_cmd("tagall"))
async def _(event):
    """.tagall <причина пинга> - Пингует всех участников группы"""
    if event.fwd_from:
        return
    mentions = utils.get_args_raw(event.message.message)
    counter = 0
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat):
        mentions += f"\n[{x.first_name}](tg://user?id={x.id})"
        counter += 1
        if counter == 5:
            await event.reply(mentions)
            counter = 0
            mentions = utils.get_args_raw(event.message.message)
            await sleep(3)
    if counter == 0:
        await event.delete()
        return
    await event.reply(mentions)
    await event.delete()


@borg.on(admin_cmd("tagadmin"))
async def _(event):
    """.tagadmin <причина пинга> - Пингует админов группы"""
    if event.fwd_from:
        return
    mentions = utils.get_args_raw(event.message.message)
    counter = 0
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f"\n[{x.first_name}](tg://user?id={x.id})"
        counter += 1
        if counter == 5:
            reply_message = None
            if event.reply_to_msg_id:
                reply_message = await event.get_reply_message()
                await reply_message.reply(mentions)
            else:
                await event.reply(mentions)
            counter = 0
            mentions = utils.get_args_raw(event.message.message)
            await sleep(2)
    reply_message = None
    if counter == 0:
        await event.delete()
        return
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()

@borg.on(admin_cmd("tagbot"))
async def _(event):
    """.tagbot <причина пинга> - Пингует ботов которые в группе"""
    if event.fwd_from:
        return
    mentions = utils.get_args_raw(event.message.message)
    counter = 0
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsBots):
        mentions += f"\n[{x.first_name}](tg://user?id={x.id})"
        counter += 1
        if counter == 5:
            reply_message = None
            if event.reply_to_msg_id:
                reply_message = await event.get_reply_message()
                await reply_message.reply(mentions)
            else:
                await event.reply(mentions)
            counter = 0
            mentions = utils.get_args_raw(event.message.message)
            await sleep(2)
    reply_message = None
    if counter == 0:
        await event.delete()
        return
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()
