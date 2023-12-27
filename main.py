# -*- coding: utf-8 -*-
# from telethon import functions
from pyrogram import Client, filters
import time
from pyrogram import enums
from random import Random

import string

def preprocess_text(text):
    # Преобразование в lowercase
    text_lower = text.lower()
    
    # Удаление знаков препинания
    text_no_punctuation = text_lower.translate(str.maketrans("", "", string.punctuation))
    
    return text_no_punctuation

from gpt import gpt

api_id = 12345
api_hash = "0123456789abcdef0123456789abcdef"


api_id = 25382489
api_hash = '9501211cbdb6b33f3ebfcf92d1375336'

app = Client("my_account", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.text & filters.private)
async def echo(client, message):
    my_id = 6546956005
    if message.from_user and (message.from_user.id == my_id or message.from_user.id == 1234060895):
        return
    timeout = Random().randint(6,20)
    print(f'Получено новое сообщение. Таймаут: {timeout}')
    time.sleep(timeout)
    crt_timestamp = None
    conversation=[]
    async for item in app.get_chat_history(message.chat.id, limit=10):
        text = item.text
        if crt_timestamp == None:
            crt_timestamp = item.date.timestamp()
        if text == None:
            if item.sticker != None:
                text = item.sticker.emoji
            else:
                text = "[Какая-то фотография]"
        if item.from_user.id == my_id:
            conversation.append({"role": "system", "content": f"{item.from_user.first_name}: {text}"})
        else:
            conversation.append({"role": "user", "content": f"{item.from_user.first_name}: {text}"})
            
    conversation = list(reversed(conversation))
    
    await app.read_chat_history(message.chat.id)
    time.sleep(5)
    await app.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    last_msg = [i async for i in app.get_chat_history(message.chat.id, limit=1)][0]

    if crt_timestamp == None or crt_timestamp ==  last_msg.date.timestamp():
        txt=gpt(conversation)
        if txt.find(':') != -1:
            txt = txt.split(':')[1]
        print(f'Переключение в режим typing и ожидание {len(txt)//10+1} секунд')
        await app.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        time.sleep(len(txt)//10+1)
        await message.reply(preprocess_text(txt))
    else:
        print('skip')
        
app.run()

