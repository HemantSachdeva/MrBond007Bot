#    Haruka Aya (A telegram bot project)
#    Copyright (C) 2017-2019 Paul Larsen
#    Copyright (C) 2019-2020 Akito Mizukito (Haruka Network Development)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import random, re, io, asyncio
from PIL import Image
from io import BytesIO
from spongemock import spongemock
from zalgo_text import zalgo
from deeppyer import deepfry
import os
from pathlib import Path
import glob

from typing import List
from telegram import Update, Bot, ParseMode, Message
from telegram.ext import run_async

from haruka import dispatcher, DEEPFRY_TOKEN, LOGGER
from haruka.modules.disable import DisableAbleCommandHandler
from telegram.utils.helpers import escape_markdown
from haruka.modules.helper_funcs.extraction import extract_user
from haruka.modules.tr_engine.strings import tld, tld_list

WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000

# D A N K modules by @deletescape vvv


@run_async
def owo(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    message = update.effective_message

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    faces = [
        '(・`ω´・)', ';;w;;', 'owo', 'UwU', '>w<', '^w^', '\(^o\) (/o^)/',
        '( ^ _ ^)∠☆', '(ô_ô)', '~:o', ';____;', '(*^*)', '(>_', '(♥_♥)',
        '*(^O^)*', '((+_+))'
    ]
    reply_text = re.sub(r'[rl]', "w", data)
    reply_text = re.sub(r'[ｒｌ]', "ｗ", data)
    reply_text = re.sub(r'[RL]', 'W', reply_text)
    reply_text = re.sub(r'[ＲＬ]', 'Ｗ', reply_text)
    reply_text = re.sub(r'n([aeiouａｅｉｏｕ])', r'ny\1', reply_text)
    reply_text = re.sub(r'ｎ([ａｅｉｏｕ])', r'ｎｙ\1', reply_text)
    reply_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', reply_text)
    reply_text = re.sub(r'Ｎ([ａｅｉｏｕＡＥＩＯＵ])', r'Ｎｙ\1', reply_text)
    reply_text = re.sub(r'\!+', ' ' + random.choice(faces), reply_text)
    reply_text = re.sub(r'！+', ' ' + random.choice(faces), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text = reply_text.replace("ｏｖｅ", "ｕｖ")
    reply_text += ' ' + random.choice(faces)

    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)


@run_async
def stretch(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    message = update.effective_message

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    count = random.randint(3, 10)
    reply_text = re.sub(r'([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])', (r'\1' * count), data)

    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)


@run_async
def vapor(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    reply_text = str(data).translate(WIDE_MAP)

    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)


@run_async
def zalgotext(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    noreply = False
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        noreply = True
        data = message.text.split(None, 1)[1]
    else:
        noreply = True
        data = tld(chat.id, "memes_no_message")

    reply_text = zalgo.zalgo().zalgofy(data)
    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)


# Less D A N K modules by @skittles9823 # holi fugg I did some maymays ^^^
# shitty maymay modules made by @divadsn vvv


@run_async
def deepfryer(bot: Bot, update: Update):
    message = update.effective_message
    chat = update.effective_chat
    if message.reply_to_message:
        data = message.reply_to_message.photo
        data2 = message.reply_to_message.sticker
    else:
        data = []
        data2 = []

    # check if message does contain media and cancel when not
    if not data and not data2:
        message.reply_text(tld(chat.id, "memes_deepfry_nothing"))
        return

    # download last photo (highres) as byte array
    if data:
        photodata = data[len(data) - 1].get_file().download_as_bytearray()
        image = Image.open(io.BytesIO(photodata))
    elif data2:
        sticker = bot.get_file(data2.file_id)
        sticker.download('sticker.png')
        image = Image.open("sticker.png")

    # the following needs to be executed async (because dumb lib)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        process_deepfry(image, message.reply_to_message, bot))
    loop.close()


async def process_deepfry(image: Image, reply: Message, bot: Bot):
    # DEEPFRY IT
    image = await deepfry(img=image,
                          token=DEEPFRY_TOKEN,
                          url_base='westeurope')

    bio = BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')

    # send it back
    bio.seek(0)
    reply.reply_photo(bio)
    if Path("sticker.png").is_file():
        os.remove("sticker.png")


# shitty maymay modules made by @divadsn ^^^




@run_async
def insults(bot: Bot, update: Update):
    message = update.effective_message
    chat = update.effective_chat
    text = random.choice(tld_list(chat.id, "memes_insults_list"))

    if message.reply_to_message:
        message.reply_to_message.reply_text(text)
    else:
        message.reply_text(text)


@run_async
def runs(bot: Bot, update: Update):
    chat = update.effective_chat
    update.effective_message.reply_text(
        random.choice(tld_list(chat.id, "memes_runs_list")))


@run_async
def slap(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    msg = update.effective_message

    # reply to correct message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(msg.from_user.first_name,
                                                   msg.from_user.id)

    user_id = extract_user(update.effective_message, args)
    if user_id:
        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        if slapped_user.username == "RealAkito":
            reply_text(tld(chat.id, "memes_not_doing_that"))
            return
        if slapped_user.username:
            user2 = "@" + escape_markdown(slapped_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(slapped_user.first_name,
                                                   slapped_user.id)

    # if no target found, bot targets the sender
    else:
        user1 = "[{}](tg://user?id={})".format(bot.first_name, bot.id)
        user2 = curr_user

    temp = random.choice(tld_list(chat.id, "memes_slaps_templates_list"))
    item = random.choice(tld_list(chat.id, "memes_items_list"))
    hit = random.choice(tld_list(chat.id, "memes_hit_list"))
    throw = random.choice(tld_list(chat.id, "memes_throw_list"))
    itemp = random.choice(tld_list(chat.id, "memes_items_list"))
    itemr = random.choice(tld_list(chat.id, "memes_items_list"))

    repl = temp.format(user1=user1,
                       user2=user2,
                       item=item,
                       hits=hit,
                       throws=throw,
                       itemp=itemp,
                       itemr=itemr)

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)


__help__ = True

OWO_HANDLER = DisableAbleCommandHandler("owo",
                                        owo,
                                        admin_ok=True,
                                        pass_args=True)
STRETCH_HANDLER = DisableAbleCommandHandler("stretch", stretch, pass_args=True)
VAPOR_HANDLER = DisableAbleCommandHandler("vapor",
                                          vapor,
                                          pass_args=True,
                                          admin_ok=True)
ZALGO_HANDLER = DisableAbleCommandHandler("zalgofy", zalgotext, pass_args=True)
DEEPFRY_HANDLER = DisableAbleCommandHandler("deepfry",
                                            deepfryer,
                                            admin_ok=True)

INSULTS_HANDLER = DisableAbleCommandHandler("insult", insults, admin_ok=True)
RUNS_HANDLER = DisableAbleCommandHandler("runs", runs, admin_ok=True)
SLAP_HANDLER = DisableAbleCommandHandler("slap",
                                         slap,
                                         pass_args=True,
                                         admin_ok=True)

dispatcher.add_handler(OWO_HANDLER)
dispatcher.add_handler(STRETCH_HANDLER)
dispatcher.add_handler(VAPOR_HANDLER)
dispatcher.add_handler(INSULTS_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(DEEPFRY_HANDLER)
