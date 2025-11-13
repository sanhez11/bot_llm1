import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден в .env")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY не найден в .env")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)


bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я ДурачокБот \nЗадай вопрос!")


@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer("Просто напиши мне сообщение")


@dp.message()
async def chat(message: types.Message):
    try:
    
        completion = await asyncio.to_thread(
            client.chat.completions.create,
            model="google/gemini-2.0-flash-exp:free",
            messages=[{"role": "user", "content": message.text}]
        )

        reply = completion.choices[0].message.content
        await message.answer(reply)
    except Exception as e:
        await message.answer(" Ошибка при обращении к модели")
        print(f"Ошибка: {e}")


async def main():
    print(" Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
