import asyncio
import json
import time
from os import getenv
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from dotenv import load_dotenv, find_dotenv
from ppp import check_new_updates
from kbds.reply import get_keyboard

load_dotenv(find_dotenv())

TOKEN = getenv('TOKEN')

USER_ID = getenv('USER_ID')

bot = Bot(token=TOKEN)

dp = Dispatcher()


@dp.message(CommandStart())
async def start_mes(message: types.Message):
    await message.answer(
        '<b>👋🏽 Добро пожаловать на News Bot! </b>\n✉️ С помощью этого бота, Вы сможете узнавать про самые свежие новости! ',
        parse_mode=ParseMode.HTML, reply_markup=get_keyboard('🗞 Новости'))



@dp.message(F.text == '🗞 Новости')
async def get_news(message: types.Message):
    with open('news.json', encoding='UTF-8') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = f'<i>{v["article_data"]}\n</i>' \
               f'<b>{v["article_title"]}\n</b>' \
               f'{v["article_url"]}'
        time.sleep(3)

        await message.answer(news, parse_mode=ParseMode.HTML)


@dp.message(F.text == '⚡️ Свежие новости')
async def get_fresh_news(message: types.Message):
    fresh_news = check_new_updates()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f'<i>{v["article_data"]}\n</i>' \
                   f'<b>{v["article_title"]}\n</b>' \
                   f'{v["article_url"]}'
            time.sleep(3)

            await message.answer(news, parse_mode=ParseMode.HTML)
    else:
        await message.answer('🙁 Новых новостей пока нет, ожидайте!')

async def news_every_n_time():
    while True:
        fresh_news = check_new_updates()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f'<i>{v["article_data"]}\n</i>' \
                       f'<b>{v["article_title"]}\n</b>' \
                       f'{v["article_url"]}'

                await bot.send_message(USER_ID, news, disable_notification=True, parse_mode=ParseMode.HTML)
        else:
            await bot.send_message(USER_ID, 'Пока нет свежих новостей', disable_notification=True)

        await asyncio.sleep(30)


async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_n_time())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
