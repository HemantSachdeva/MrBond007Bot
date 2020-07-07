import html
import requests
from telegram import ParseMode, Bot, Update
from telegram.ext import CommandHandler, run_async, Filters
from haruka.modules.tr_engine.strings import tld
from haruka import dispatcher





@run_async
def format_help(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    update.effective_message.reply_text(tld(chat.id, "format_list"),
                                        parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(tld(chat.id, "format_try"))
    update.effective_message.reply_text(tld(chat.id, "format_helps"))
    update.effective_message.reply_text(tld(chat.id, "format_note"))
@run_async
def format_convo(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    update.effective_message.reply_text(tld(chat.id, "conversation_list"), parse_mode=ParseMode.HTML)


__help__=True


MD_HELP_HANDLER = CommandHandler("formats",
                                 format_help,
                                 filters=Filters.private)
CONVO_HELP_HANDLER = CommandHandler("conversation",
                                 format_convo,
                                 filters=Filters.private)
dispatcher.add_handler(MD_HELP_HANDLER)
dispatcher.add_handler(CONVO_HELP_HANDLER)                               