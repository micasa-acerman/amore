# -*- coding: utf-8 -*-
# from telethon import functions
from pyrogram import Client, filters
import time
from pyrogram import enums
from random import Random

from gpt import gpt
import string

def preprocess_text(text):
    # Преобразование в lowercase
    text_lower = text.lower()
    
    # Удаление знаков препинания
    text_no_punctuation = text_lower.translate(str.maketrans("", "", string.punctuation))
    
    return text_no_punctuation


api_id = 12345
api_hash = "0123456789abcdef0123456789abcdef"


api_id = 25382489
api_hash = '9501211cbdb6b33f3ebfcf92d1375336'

app = Client("my_account", api_id=api_id, api_hash=api_hash)

def count_of_spaces(string):
    count = 0
    for i in range(0, len(string)):
        if string[i] == " ":
            count += 1
    return count


@app.on_message(filters.text & filters.private)
async def echo(client, message):
    my_id = 6546956005
    if message.from_user and (message.from_user.id == my_id or message.from_user.id == 1234060895) or message.from_user.first_name == None:
        return
    timeout = Random().randint(2,5)
    print(f'Получено новое сообщение. Таймаут: {timeout}')
    time.sleep(timeout)
    crt_timestamp = None
    conversation=[]
    async for item in app.get_chat_history(message.chat.id, limit=10):
        text = item.text
        if crt_timestamp == None:
            crt_timestamp = item.date.timestamp()
            continue
        if text == None:
            if item.sticker != None:
                text = item.sticker.emoji
            else:
                text = "[Какая-то фотография]"
        conversation.append(f"{item.from_user.first_name}: {text}")
            
    conversation = "\r\n".join(list(reversed(conversation)))+f".\r\nMilana отвечает с большим юмором и любопытством. Он также может задать вопрос:"
    
    await app.read_chat_history(message.chat.id)
    await app.send_chat_action(message.chat.id, enums.ChatAction.TYPING)

    txt=gpt("Milana", message.from_user.first_name, conversation)
    if txt.find(':') != -1:
        txt = txt.split(':')[1]
    timeout = max(count_of_spaces(txt) // 5,1)
    print(f'Переключение в режим typing и ожидание {timeout} секунд')
    await app.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    time.sleep(timeout)
    last_msg = [i async for i in app.get_chat_history(message.chat.id, limit=1)][0]
    if crt_timestamp == None or crt_timestamp ==  last_msg.date.timestamp():
        await message.reply(preprocess_text(txt))
    else:
        print('skip')
        
app.run()

