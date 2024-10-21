import re
from os import environ
from dotenv import load_dotenv
from Script import script 
import time 

# load_dotenv("./config.env")
load_dotenv("./dynamic.env", override=True)

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
PICS = (environ.get('PICS', 'https://telegra.ph/file/eb2076910fc1faa2f1c61.jpg https://telegra.ph/file/c3f4699d4678f873e3986.jpg https://telegra.ph/file/aaef98ebba21f74d58b97.jpg https://telegra.ph/file/dcb9a1f6d71e422f880a6.jpg https://telegra.ph/file/bf5365c9a3a109b260552.jpg https://telegra.ph/file/3c51670082a64f6fa74f6.jpg https://telegra.ph/file/511e1b7f439a39b6ce89b.jpg https://telegra.ph/file/48facaa4f70faa38ccdf2.jpg https://telegra.ph/file/b9ccf34a299a8d55d12ff.jpg https://telegra.ph/file/16af79f52b612816eb4f7.jpg')).split()
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ.get('API_ID', '19071424'))
API_HASH = environ.get('API_HASH', 'c4b3e298cc50fd4cc563ae75ee882948')
BOT_TOKEN = environ.get('BOT_TOKEN', '7697119880:AAEIbIPBvFqHIuEExWRRIBX7AopM2teSqzo')

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '7425490417').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1002397004421 -1002284227206').split()]
JOIN_CHANNELS = [int(-1002247041357), int(-1001544569591)]
PIRO_CHANNELS = [int(-1002323077913)]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []

# MongoDB information
#DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://rai:rai@cluster0.zcrha.mongodb.net/?retryWrites=true&w=majority")

DATABASE_NAME = environ.get('DATABASE_NAME', "Manaf")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://Manaf:Manaf@cluster0.h8xkden.mongodb.net/")
DATABASE_URI2 = environ.get('DATABASE_URI2', "mongodb+srv://Mamithav2:Mamithav2@cluster0.8uofp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_URI3 = environ.get('DATABASE_URI3', "mongodb+srv://Mamithav3:Mamithav3@cluster0.gdwtz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_URI4 = environ.get('DATABASE_URI4', "mongodb+srv://Mamithav4:Mamithav4@cluster0.xy8lu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_URI5 = environ.get('DATABASE_URI5', "mongodb+srv://Mamithav5:Mamithav5@cluster0.g7tzh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
                            

# FSUB
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
# Set to False inside the bracket if you don't want to use Request Channel else set it to Channel ID

REQ_CHANNEL=environ.get("REQ_CHANNEL", "-1002247041357")
REQ_CHANNEL = (int(REQ_CHANNEL) if REQ_CHANNEL and id_pattern.search(REQ_CHANNEL) else False) if REQ_CHANNEL is not None else None
REQ_CHANNEL2=environ.get("REQ_CHANNEL2", None)
REQ_CHANNEL2 = (int(REQ_CHANNEL2) if REQ_CHANNEL2 and id_pattern.search(REQ_CHANNEL2) else False) if REQ_CHANNEL2 is not None else None
JOIN_REQS_DB = environ.get("JOIN_REQS_DB", DATABASE_URI)

# Others
LOG_CHANNEL = -1002276401285
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "False")), False)
IMDB = is_enabled((environ.get('IMDB', "False")), True)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), False)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "<b>👋 𝘏𝘦𝘭𝘭𝘰 𝘛𝘩𝘦𝘳𝘦, 𝘠𝘰𝘶𝘳 𝘍𝘪𝘭𝘦 𝘐𝘴 𝘏𝘦𝘳𝘦!</b>\n\n<blockquote>🗃️ <b>{file_name}</b>\n\n<b>{file_caption}</b></blockquote>\n\n**🔔 𝖩𝗈𝗂𝗇 [𝖡𝖫𝖠𝖲𝖳𝖤𝖱 𝖫𝖨𝖭𝖪𝖹](t.me/blaster_linkz)**")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", '<b>{file_caption}</b>\n\n**╔═══ ᴊᴏɪɴ ᴡɪᴛʜ ᴜs ═══╗\n➲ @MCUupdatesLINKS\n╚═══ ᴊᴏɪɴ ᴡɪᴛʜ ᴜs ═══╝**')
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "🏷 𝖳𝗂𝗍𝗅𝖾: <a href={url}>{title}</a> \n🔮 𝖸𝖾𝖺𝗋: {year} \n⭐️ 𝖱𝖺𝗍𝗂𝗇𝗀𝗌: {rating}/ 10  \n🎭 𝖦𝖾𝗇𝖾𝗋𝗌: {genres} \n\n🎊 𝖯𝗈𝗐𝖾𝗋𝖾𝖽 𝖡𝗒 [[𝖯𝗂𝖱𝖮]](t.me/piroxbots)")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '-1002206726320')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "False")), False)

LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your current IMDB template is {IMDB_TEMPLATE}"
