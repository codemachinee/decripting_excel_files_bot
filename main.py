from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
import asyncio
import os
from paswords import *
token = lemonade
bot = Bot(token=token)
dp = Dispatcher()
from function import modify_files_in_zip


@dp.message(F.document, F.chat.type == 'private')
async def chek_message(v):
    file_id = v.document.file_id
    upload_file_name = f"{v.document.file_name}"
    file = await bot.get_file(file_id)
    file_path = file.file_path
    if '.xls' in v.document.file_name:
        await bot.download_file(file_path, upload_file_name)
        os.rename(upload_file_name, f'{upload_file_name}.zip')
        zip_file_path = f'{upload_file_name}.zip'
        await bot.send_message(v.chat.id, 'Анализ файла...')
        await modify_files_in_zip(bot, v, zip_file_path)
    else:
        await bot.send_message(v.chat.id, "неверный формат файла")


@dp.message(Command(commands='start'))
async def start(message):
    await bot.send_message(message.chat.id, f'Я бот вскрывающий защиту с excel файлов.'
                                            f' Размер файла не должен превышать 50 Мб (ограничение Телеграм)'
                                            f' Отправьте мне файл и я его разблокирую.\n\n'
                                            f'бот разработан @hlapps')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')