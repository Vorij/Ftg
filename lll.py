
from .. import loader
from asyncio import sleep

def register(cb):
    cb(LoveMod())

class LoveMod(loader.Module):
    """Love"""
    strings = {'name': 'Love'}

    async def lovecmd(self, message):
        """Используй .love"""
        await message.edit("ПОЖАЛУЙСТА ПРОЧТИ ДО КОНЦА")
        await sleep(2)
        await message.edit("...")
        number = 1
        await message.edit(str(number) + "♥ Я")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "🧡 Хочу")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💛 Тебе")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💚 Сказать")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💙 Что")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💜 Ты")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💗 Самая")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💓 Лучшая")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "❤ Ты")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "🧡 Самая")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💖 Милая")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💛 Добрая")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💚 Хорошая")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💙 Красивая")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💜 Улыбнись")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "❣ Ведь")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💗 Тебе идет")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💓 И")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "❤️ Кто-бы")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "🧡 Что бы")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💛 Не говорил")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💚 Знай")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💙 Ты самая")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💖 Прекрасная")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💜 В этом")
        number = number + 1
        await sleep(1)
        await message.edit(str(number) + "💕 Мире")
        number = number + 1
        await sleep(2)
        await message.edit(str(number) + "💞 С любовью")
        number = number + 1
        await sleep(1)
        await message.edit("ТВОЙ ЛЮБИМЫЙ ЧЕЛОВЕК 😘")