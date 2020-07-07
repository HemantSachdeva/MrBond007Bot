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

from functools import wraps

from telegram import Chat, ChatMember, Update, Bot

from haruka import DEL_CMDS, SUDO_USERS, WHITELIST_USERS
import haruka.modules.sql.admin_sql as admin_sql
from haruka.modules.tr_engine.strings import tld
from haruka.modules import connection

def can_delete(chat: Chat, bot_id: int) -> bool:
    return chat.get_member(bot_id).can_delete_messages


def is_user_ban_protected(chat: Chat,
                          user_id: int,
                          member: ChatMember = None) -> bool:
    if chat.type == 'private' \
            or user_id in SUDO_USERS \
            or user_id in WHITELIST_USERS \
            or chat.all_members_are_administrators:
        return True

    if not member:
        member = chat.get_member(user_id)
    return member.status in ('administrator', 'creator')


def is_user_admin(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    if chat.type == 'private' \
            or user_id in SUDO_USERS \
            or user_id == int(777000) \
            or chat.all_members_are_administrators:
        return True

    if not member:
        member = chat.get_member(user_id)
    return member.status in ('administrator', 'creator')


def is_bot_admin(chat: Chat,
                 bot_id: int,
                 bot_member: ChatMember = None) -> bool:
    if chat.type == 'private' \
            or chat.all_members_are_administrators:
        return True

    if not bot_member:
        bot_member = chat.get_member(bot_id)
    return bot_member.status in ('administrator', 'creator')


def is_user_in_chat(chat: Chat, user_id: int) -> bool:
    member = chat.get_member(user_id)
    return member.status not in ('left', 'kicked')


def bot_can_delete(func):
    @wraps(func)
    def delete_rights(bot: Bot, update: Update, *args, **kwargs):
        chat = update.effective_chat

        if can_delete(update.effective_chat, bot.id):
            return func(bot, update, *args, **kwargs)
        else:
            update.effective_message.reply_text(
                tld(chat.id, 'helpers_bot_cant_delete'))

    return delete_rights


def can_pin(func):
    @wraps(func)
    def pin_rights(bot: Bot, update: Update, *args, **kwargs):
        chat = update.effective_chat

        if update.effective_chat.get_member(bot.id).can_pin_messages:
            return func(bot, update, *args, **kwargs)
        else:
            update.effective_message.reply_text(
                tld(chat.id, 'helpers_bot_cant_pin'))

    return pin_rights


def can_promote(func):
    @wraps(func)
    def promote_rights(bot: Bot, update: Update, *args, **kwargs):
        chat = update.effective_chat

        if update.effective_chat.get_member(bot.id).can_promote_members:
            return func(bot, update, *args, **kwargs)
        else:
            update.effective_message.reply_text(
                tld(chat.id, 'helpers_bot_cant_pro_demote'))

    return promote_rights


def can_restrict(func):
    @wraps(func)
    def promote_rights(bot: Bot, update: Update, *args, **kwargs):
        chat = update.effective_chat

        if update.effective_chat.get_member(bot.id).can_restrict_members:
            return func(bot, update, *args, **kwargs)
        else:
            update.effective_message.reply_text(
                tld(chat.id, 'helpers_bot_cant_restrict'))

    return promote_rights


def bot_admin(func):
    @wraps(func)
    def is_admin(bot: Bot, update: Update, *args, **kwargs):
        chat = update.effective_chat

        if is_bot_admin(update.effective_chat, bot.id):
            return func(bot, update, *args, **kwargs)
        else:
            update.effective_message.reply_text(
                tld(chat.id, 'helpers_bot_not_admin'))

    return is_admin


def user_admin(func):
    @wraps(func)
    def is_admin(bot: Bot, update: Update, *args, **kwargs):
        user = update.effective_user
        chat = update.effective_chat
        if user and is_user_admin(update.effective_chat, user.id):
            try:
                return func(bot, update, *args, **kwargs)
            except Exception:
                return

        elif not user:
            pass

        elif DEL_CMDS and " " not in update.effective_message.text:
            update.effective_message.delete()

        elif (admin_sql.command_reaction(chat.id) == True):
            update.effective_message.reply_text(
                tld(chat.id, 'helpers_user_not_admin'))

    return is_admin


def user_admin_no_reply(func):
    @wraps(func)
    def is_admin(bot: Bot, update: Update, *args, **kwargs):
        user = update.effective_user
        if user and is_user_admin(update.effective_chat, user.id):
            return func(bot, update, *args, **kwargs)

        elif not user:
            pass

        elif DEL_CMDS and " " not in update.effective_message.text:
            update.effective_message.delete()

    return is_admin


def user_not_admin(func):
    @wraps(func)
    def is_not_admin(bot: Bot, update: Update, *args, **kwargs):
        user = update.effective_user
        if user and not is_user_admin(update.effective_chat, user.id):
            return func(bot, update, *args, **kwargs)

    return is_not_admin

def dev_plus(func):
    @wraps(func)
    def is_dev_plus_func(bot: Bot, update: Update, *args, **kwargs):

        user = update.effective_user

        if user.id in SUDO_USERS:
            return func(bot, update, *args, **kwargs)
        elif not user:
            pass
        elif DEL_CMDS and " " not in update.effective_message.text:
            update.effective_message.delete()
        else:
            update.effective_message.reply_text("This is a developer restricted command."
                                                " You do not have permissions to run this.")

    return is_dev_plus_func
def connection_status(func):
    @wraps(func)
    def connected_status(bot: Bot, update: Update, *args, **kwargs):
        conn = connected(bot, update, update.effective_chat, update.effective_user.id, need_admin=False)

        if conn:
            chat = dispatcher.bot.getChat(conn)
            update.__setattr__("_effective_chat", chat)
            return func(bot, update, *args, **kwargs)
        else:
            if update.effective_message.chat.type == "private":
                update.effective_message.reply_text("Send /connect in a group that you and I have in common first.")
                return connected_status

            return func(bot, update, *args, **kwargs)

    return connected_status
    from haruka.modules import connection

connected = connection.connected
def user_can_ban(func):
    @wraps(func)
    def user_is_banhammer(bot: Bot, update: Update, *args, **kwargs):
        user = update.effective_user.id
        member = update.effective_chat.get_member(user)
        if not (member.can_restrict_members or member.status == "creator") and not user in SUDO_USERS:
            update.effective_message.reply_text("Sorry son, but you're not worthy to wield the banhammer.")
            return ""
        return func(bot, update, *args, **kwargs)
    
    return user_is_banhammer
