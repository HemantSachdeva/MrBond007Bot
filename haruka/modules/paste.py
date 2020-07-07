from typing import List

import requests
from telegram import Update, Bot, ParseMode
from telegram.ext import run_async
from telegram.utils.helpers import escape_markdown, mention_html
from haruka import dispatcher
from haruka.modules.disable import DisableAbleCommandHandler
from haruka.modules.tr_engine.strings import tld


@run_async
def paste(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat  # type: Optional[Chat]
    BURL = 'https://del.dog'
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.text
    elif len(args) >= 1:
        data = message.text.split(None, 1)[1]
    else:
        message.reply_text(tld(chat.id, "paste_invalid"))
        return

    r = requests.post(f'{BURL}/documents', data=data.encode('utf-8'))

    if r.status_code == 404:
        update.effective_message.reply_text(tld(chat.id, "paste_404"))
        r.raise_for_status()

    res = r.json()

    if r.status_code != 200:
        update.effective_message.reply_text(res['message'])
        r.raise_for_status()

    key = res['key']
    if res['isUrl']:
        reply = tld(chat.id, "paste_success").format(BURL, key, BURL, key)
    else:
        reply = f'Pasted to {BURL}/{key}'
    update.effective_message.reply_text(reply,
                                        parse_mode=ParseMode.MARKDOWN,
                                        disable_web_page_preview=True)


@run_async
def get_paste_content(bot: Bot, update: Update, args: List[str]):
    BURL = 'https://del.dog'
    message = update.effective_message
    chat = update.effective_chat  # type: Optional[Chat]

    if len(args) >= 1:
        key = args[0]
    else:
        message.reply_text(tld(chat.id, "get_pasted_invalid"))
        return

    format_normal = f'{BURL}/'
    format_view = f'{BURL}/v/'

    if key.startswith(format_view):
        key = key[len(format_view):]
    elif key.startswith(format_normal):
        key = key[len(format_normal):]

    r = requests.get(f'{BURL}/raw/{key}')

    if r.status_code != 200:
        try:
            res = r.json()
            update.effective_message.reply_text(res['message'])
        except Exception:
            if r.status_code == 404:
                update.effective_message.reply_text(
                    tld(chat.id, "paste_404"))
            else:
                update.effective_message.reply_text(
                    tld(chat.id, "get_pasted_unknown"))
        r.raise_for_status()
        

    update.effective_message.reply_text('Here is your content.\n\n```'+escape_markdown(r.text)+
                                        '```',
                                        parse_mode=ParseMode.MARKDOWN)


@run_async
def get_paste_stats(bot: Bot, update: Update, args: List[str]):
    BURL = 'https://del.dog'
    message = update.effective_message
    chat = update.effective_chat  # type: Optional[Chat]

    if len(args) >= 1:
        key = args[0]
    else:
        message.reply_text(tld(chat.id, "get_pasted_invalid"))
        return

    format_normal = f'{BURL}/'
    format_view = f'{BURL}/v/'

    if key.startswith(format_view):
        key = key[len(format_view):]
    elif key.startswith(format_normal):
        key = key[len(format_normal):]

    r = requests.get(f'{BURL}/documents/{key}')

    if r.status_code != 200:
        try:
            res = r.json()
            update.effective_message.reply_text(res['message'])
        except Exception:
            if r.status_code == 404:
                update.effective_message.reply_text(
                    tld(chat.id, "paste_404"))
            else:
                update.effective_message.reply_text(
                    tld(chat.id, "get_pasted_unknown"))
        r.raise_for_status()

    document = r.json()
    key = document['id']
    views = document['viewCount']
    reply = f'Stats for **[/{key}]({BURL}/{key})**:\nViews: `{views}`'
    update.effective_message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

__help__ = True

PASTE_HANDLER = DisableAbleCommandHandler("paste", paste, pass_args=True)
GET_PASTE_HANDLER = DisableAbleCommandHandler("getpaste",
                                              get_paste_content,
                                              pass_args=True)
PASTE_STATS_HANDLER = DisableAbleCommandHandler("pastestats",
                                                get_paste_stats,
                                                pass_args=True)
                                                
dispatcher.add_handler(PASTE_HANDLER)
dispatcher.add_handler(GET_PASTE_HANDLER)
dispatcher.add_handler(PASTE_STATS_HANDLER)