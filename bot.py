import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import yt_dlp
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🎵 Привет! Я музыкальный бот ***** тебя в рот!\n\n"
        "Просто напиши название песни, и я её найду(нет)!"
    )

@dp.message()
async def search_music(message: types.Message):
    query = message.text
    
    await message.answer("🔍 Ищу музыку, покури пока...")
    
    try:
        # Настройки для скачивания
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'music.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'quiet': True,
        }
        
        # Ищем и скачиваем
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            title = info['entries'][0]['title']
        
        # Доставка трека
        audio_file = types.FSInputFile("music.mp3")
        await message.answer_audio(audio_file, title=title)
        
        # Удаляем файл
        os.remove("music.mp3")
        
    except Exception as e:
        await message.answer("😕 Не удалось найти песню. Попробуй другой запрос!")

async def main():
    print("Оно работает!")
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
