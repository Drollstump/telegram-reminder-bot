import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = "8413287318:AAE50xxcMcSO6LxteUysG2azKsN1Y5Bg60E"

bot = Bot(token=TOKEN)
dp = Dispatcher()

reminders = []


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Салам! Я reminder bot 😎\n\n"
        "Команды:\n"
        "/start - запуск\n"
        "/help - помощь\n"
        "/about - о боте\n"
        "/add HH:MM текст - добавить напоминание\n"
        "/list - список напоминаний"
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Команды:\n"
        "/start - запуск\n"
        "/help - помощь\n"
        "/about - о боте\n"
        "/add HH:MM текст - добавить напоминание\n"
        "Пример: /add 22:30 do homework\n"
        "/list - показать напоминания"
    )


@dp.message(Command("about"))
async def about_command(message: Message):
    await message.answer("This is a Telegram reminder bot built with Python and aiogram.")


@dp.message(Command("add"))
async def add_reminder(message: Message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            raise ValueError

        _, time_str, *text_parts = parts
        reminder_time = datetime.strptime(time_str, "%H:%M").time()
        reminder_text = " ".join(text_parts)

        reminders.append(
            {
                "time": reminder_time,
                "text": reminder_text,
                "chat_id": message.chat.id,
                "sent": False,
            }
        )

        await message.answer(f"✅ Reminder added for {time_str}: {reminder_text}")
    except ValueError:
        await message.answer("❌ Use this format: /add HH:MM text\nExample: /add 22:30 do homework")


@dp.message(Command("list"))
async def list_reminders(message: Message):
    user_reminders = [r for r in reminders if r["chat_id"] == message.chat.id]

    if not user_reminders:
        await message.answer("У тебя пока нет напоминаний.")
        return

    response = "📋 Your reminders:\n"
    for i, reminder in enumerate(user_reminders, start=1):
        response += f"{i}. {reminder['time'].strftime('%H:%M')} - {reminder['text']}\n"

    await message.answer(response)


@dp.message()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")


async def reminder_checker():
    while True:
        now = datetime.now().strftime("%H:%M")

        for reminder in reminders:
            reminder_time = reminder["time"].strftime("%H:%M")
            if reminder_time == now and not reminder["sent"]:
                await bot.send_message(
                    reminder["chat_id"],
                    f"⏰ Reminder: {reminder['text']}"
                )
                reminder["sent"] = True

        await asyncio.sleep(30)


async def main():
    asyncio.create_task(reminder_checker())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())