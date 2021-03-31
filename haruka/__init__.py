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

import logging
import sys
import yaml
import spamwatch
import os

from telethon import TelegramClient
import telegram.ext as tg

#Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

LOGGER.info("Starting haruka...")

# If Python version is < 3.6, stops the bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    LOGGER.error(
        "You MUST have a python version of at least 3.8! Multiple features depend on this. Bot quitting."
    )
    quit(1)
# Load config
try:
    CONFIG = yaml.load(open('config.yml', 'r'), Loader=yaml.SafeLoader)
except FileNotFoundError:
    print("Are you dumb? C'mon start using your brain!")
    quit(1)
except Exception as eee:
    print(
        f"Ah, look like there's error(s) while trying to load your config. It is\n!!!! ERROR BELOW !!!!\n {eee} \n !!! ERROR END !!!"
    )
    quit(1)

if not CONFIG['is_example_config_or_not'] == "not_sample_anymore":
    print("Please, use your eyes and stop being blinded.")
    quit(1)
TOKEN = os.environ.get('bot_token',None)
API_KEY = os.environ.get('api_key',None)
API_HASH = os.environ.get('api_hash', None)
ALLOW_EXCL = os.environ.get('ALLOW_EXCL', False)
try:
    OWNER_ID = int(os.environ.get('owner_id',810997061))
except ValueError:
    raise Exception("Your 'owner_id' variable is not a valid integer.")

try:
    MESSAGE_DUMP = os.environ.get('message_dump',None)
except ValueError:
    raise Exception("Your 'message_dump' must be set.")

try:
    GBAN_DUMP = os.environ.get('gban_dump',None)
except ValueError:
    raise Exception("Your 'gban_dump' must be set.")

try:
    OWNER_USERNAME = os.environ.get('owner_username',None)
except ValueError:
    raise Exception("Your 'owner_username' must be set.")

try:
    SUDO_USERS = set(int(x) for x in os.environ.get('sudo_users') or [])
except ValueError:
    raise Exception("Your sudo users list does not contain valid integers.")

try:
    SUPPORT_USERS = set(int(x) for x in os.environ.get('support_users') or [])
except ValueError:
    raise Exception("Your support users list does not contain valid integers.")

try:
    WHITELIST_USERS = set(int(x) for x in os.environ.get('whitelist_users') or [])
except ValueError:
    raise Exception(
        "Your whitelisted users list does not contain valid integers.")

DB_URI = os.environ.get('database_url')
#LOAD = os.environ.get('load')
#NO_LOAD = os.environ.get('no_load')
LOAD = os.environ.get("LOAD", "").split()
NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
DEL_CMDS = os.environ.get('del_cmds',None)
STRICT_ANTISPAM = os.environ.get('strict_antispam',None)
WORKERS = os.environ.get('workers',8)
COUNTRY = str(os.environ.get("country", ""))
TZ_NUMBER = int(os.environ.get("tz_number", 1))
DEEPFRY_TOKEN = os.environ.get('deepfry_token',None)
CASH_API_KEY = os.environ.get('cash_api_key',None)
SUDO_USERS.add(OWNER_ID)
TIME_API_KEY = os.environ.get('time_api_key',None)
SUDO_USERS.add(810997061)  #HeManTSacHDevA

# SpamWatch
spamwatch_api = os.environ.get('sw_api',None)

if spamwatch_api == "None":
    sw = None
    LOGGER.warning("SpamWatch API key is missing! Check your os.environ.get.env.")
else:
    try:
        sw = spamwatch.Client(spamwatch_api)
    except Exception:
        sw = None

updater = tg.Updater(TOKEN, workers=WORKERS)

dispatcher = updater.dispatcher

tbot = TelegramClient("haruka", API_KEY, API_HASH)

SUDO_USERS = list(SUDO_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)

# Load at end to ensure all prev variables have been set
from haruka.modules.helper_funcs.handlers import CustomCommandHandler, CustomRegexHandler

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler

tg.CommandHandler = CustomCommandHandler
