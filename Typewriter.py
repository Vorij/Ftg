from .. import loader, utils
from asyncio import sleep
@loader.tds
class TypewriterMod(loader.Module):
	"""Печатает по одной букве"""
	strings = {"name": "Typewriter"}
	@loader.owner
	async def typecmd(self, message):
		""".type <текст или ответ>"""
		text = utils.get_args_raw(message)
		if not text:
			reply = await message.get_reply_message()
			if not reply or not reply.message:
				await message.edit("<b>Нужен текст или ответ</b>")
				return
			text = reply.message
		out = ""
		for ch in text:
			out += ch
			if ch not in [" ", "\n"]:
				await message.edit(out+"\u2060")
				await sleep(0.3)