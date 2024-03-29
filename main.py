from info_coder import InfoCoder
from database import DataBase
from markup_parser import MarkupParser

import configparser
import aiogram
import asyncio
import os

// third
// step 7.3
config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")
bot = aiogram.bot.Bot(config["Bot"]["token"])
dp = aiogram.dispatcher.Dispatcher(bot)

info_coder = InfoCoder()
db = DataBase("db.db")
mp = MarkupParser(config)


async def send_message(user_id, language, text, buttons, action):
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in await mp.get_buttons(language, buttons):
        keyboard.row(*i)
    await bot.send_message(user_id, await mp.get_text(language, text), reply_markup=keyboard)
    await db.set_action(user_id, action)


@dp.message_handler(content_types=["text"])
async def message_handler(message):
    if message.text == "/start":
        await db.add_user(message.from_user.id, "", "")
        await send_message(message.from_user.id, "INT", "msg_start", "btn_langchoose", "langchoose")

    language = await db.get_language(message.from_user.id)
    action = await db.get_action(message.from_user.id)

    if action == "langchoose":
        if config["INT"].get(message.text) == "engchoose":
            language = "ENG"
            await db.set_language(message.from_user.id, "ENG")

        if config["INT"].get(message.text) == "ruschoose":
            language = "RUS"
            await db.set_language(message.from_user.id, "RUS")

        if language is not None:
            await send_message(message.from_user.id, language, "msg_action", "btn_action", "actionchoose")

    if language is not None:
        msg = config[language].get(message.text)

        if msg is None:
            return

        if msg == "back":

            if action == "actionchoose":
                await send_message(message.from_user.id, "INT", "msg_start", "btn_langchoose", "langchoose")

            if action == "encode" or action == "decode":
                await send_message(message.from_user.id, language, "msg_action", "btn_action", "actionchoose")

        if msg == "encode":
            await send_message(message.from_user.id, language, "msg_encode", "btn_encode", "encode")

        if msg == "decode":
            await send_message(message.from_user.id, language, "msg_decode", "btn_decode", "decode")


@dp.message_handler(content_types=["document"])
async def document_handler(message):
    action = await db.get_action(message.from_user.id)
    if action is not None:
        if message.caption is None:
            return
        try:
            while True:
                print(1)
                file = open("temp.f")
                await asyncio.sleep(1)
        except:
            file = await bot.get_file(message.document.file_id)
            file_name = message.document.file_name
            await bot.download_file(file.file_path, "temp.f")
            info_coder.set_file(open("temp.f", "rb"))
            if action == "encode":
                info_coder.encode_info(message.caption)
            elif action == "decode":
                info_coder.decode_info(message.caption)
            file = open(file_name, "wb")
            if action == "encode":
                file.write(info_coder.get_locked())
            elif action == "decode":
                file.write(info_coder.get_unlocked())
            file.close()
            await bot.send_document(message.from_user.id, open(file_name, "rb"))
        os.remove("temp.f")
        os.remove(file_name)


if __name__ == "__main__":
    aiogram.executor.start_polling(dp)
