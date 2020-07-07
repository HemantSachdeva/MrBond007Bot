from telegram import Update, Bot
from telegram.ext import run_async
from typing import List
from haruka.modules.disable import DisableAbleCommandHandler
from haruka import dispatcher

@run_async
def shout(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat

    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        data = " ".join(args)
    else:
        data = tld(chat.id, "memes_no_message")

    msg = "```"
    result = []
    result.append(' '.join([s for s in data]))
    for pos, symbol in enumerate(data[1:]):
        result.append(symbol + ' ' + '  ' * pos + symbol)
    result = list("\n".join(result))
    result[0] = data[0]
    result = "".join(result)
    msg = "```\n" + result + "```"
    return update.effective_message.reply_text(msg, parse_mode="MARKDOWN")
   
__help__ = True



SHOUT_HANDLER = DisableAbleCommandHandler("shout", shout, pass_args=True)

dispatcher.add_handler(SHOUT_HANDLER)
