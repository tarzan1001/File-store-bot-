import sys
import asyncio
import datetime, pytz, time
from os import environ, execle, system
import os
import logging
import random
from typing import List, Tuple
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_inlinedb import Media2, Media3, Media4, Media5, get_file_details, unpack_new_file_id, delete_files_below_threshold
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id
from database.users_chats_db import db
from plugins.fsub import ForceSub
from info import CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, DATABASE_URI, DATABASE_NAME, BATCH_FILE_CAPTION
from utils import get_settings, get_size, is_subscribed, save_group_settings, temp
from database.connections_mdb import active_connection
import re
import json
import base64
logger = logging.getLogger(__name__)

import pymongo

fclient = pymongo.MongoClient(DATABASE_URI)
fdb = fclient[DATABASE_NAME]
fcol = fdb['forward']

BATCH_FILES = {}

DELETE_TXT = """‼️ 𝗜𝗠𝗣𝗢𝗥𝗧𝗔𝗡𝗧 ‼️

<blockquote>⚠️ 𝙁𝙞𝙡𝙚 𝙒𝙞𝙡𝙡 𝘽𝙚 𝘿𝙚𝙡𝙚𝙩𝙚𝙙 𝙄𝙣 𝟱 𝙈𝙞𝙣𝙪𝙩𝙚𝙨.</blockquote>

𝗜𝗳 𝘆𝗼𝘂 𝘄𝗮𝗻𝘁 𝘁𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘁𝗵𝗲𝘀𝗲 𝗳𝗶𝗹𝗲𝘀, 𝗞𝗶𝗻𝗱𝗹𝘆 𝗙𝗼𝗿𝘄𝗮𝗿𝗱 𝘁𝗵𝗲𝘀𝗲 𝗳𝗶𝗹𝗲𝘀 𝘁𝗼 𝗮𝗻𝘆 𝗰𝗵𝗮𝘁 (𝘀𝗮𝘃𝗲𝗱) 𝗮𝗻𝗱 𝘀𝘁𝗮𝗿𝘁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱...

<blockquote>𝗙𝗼𝗿 𝗠𝗼𝗿𝗲 𝗤𝘂𝗮𝗹𝗶𝘁𝗮𝘁𝗶𝘃𝗲 𝗙𝗶𝗹𝗲𝘀 𝗨𝘀𝗲 𝗕𝗲𝗹𝗼𝘄 𝗕𝗼𝘁𝘀.</blockquote>

𝗧𝗵𝗮𝗻𝗸 𝗬𝗼𝘂 :)"""

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [[
                    InlineKeyboardButton('😇 𝖲𝗎𝗋𝗉𝗋𝗂𝗌𝖾', callback_data='about'),
                    InlineKeyboardButton('‼️ 𝖣𝖬𝖢𝖠', callback_data='dmca')
                ]]

        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup)
        await asyncio.sleep(2) # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
                    InlineKeyboardButton('😇 𝖲𝗎𝗋𝗉𝗋𝗂𝗌𝖾', callback_data='about'),
                    InlineKeyboardButton('‼️ 𝖣𝖬𝖢𝖠', callback_data='dmca')
                ],[
                    InlineKeyboardButton('🔍 𝖲𝖾𝖺𝗋𝖼𝗁 𝖧𝖾𝗋𝖾', switch_inline_query_current_chat='')
                ],[
                   InlineKeyboardButton('ᴀᴅᴍɪɴs ᴇxᴛʀᴀ ғᴇᴀᴛᴜʀᴇs', callback_data='machu')
                ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        if message.command[1] == "subscribe":
            await ForceSub(client, message)
            return

        buttons = [[
                    InlineKeyboardButton('😇 𝖲𝗎𝗋𝗉𝗋𝗂𝗌𝖾', callback_data='about'),
                    InlineKeyboardButton('‼️ 𝖣𝖬𝖢𝖠', callback_data='dmca')
                ],[
                    InlineKeyboardButton('🔍 𝖲𝖾𝖺𝗋𝖼𝗁 𝖧𝖾𝗋𝖾', switch_inline_query_current_chat='')
                ],[
                   InlineKeyboardButton('ᴀᴅᴍɪɴs ᴇxᴛʀᴀ ғᴇᴀᴛᴜʀᴇs', callback_data='machu')
                ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    kk, file_id = message.command[1].split("_", 1) if "_" in message.command[1] else (False, False)
    pre = ('checksubp' if kk == 'filep' else 'checksub') if kk else False
    deep_link = message.text.split(None, 1)[1]
    def_url = f"https://t.me/{temp.U_NAME}?start={deep_link}"
    status = await ForceSub(client, message, file_id=def_url)
    if not status:
        return
    
    data = message.command[1]
    if not file_id:
        file_id = data
    
    if data.split("-", 1)[0] == "BATCH":
        sts = await message.reply("𝖥𝖾𝗍𝖼𝗁𝗂𝗇𝗀 𝖳𝗁𝖾 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖥𝗂𝗅𝖾𝗌.....\n𝖪𝗂𝗇𝖽𝗅𝗒 𝖶𝖺𝗂𝗍!!!!")
        file_id = data.split("-", 1)[1]
        msgs = BATCH_FILES.get(file_id)
        if not msgs:
            file = await client.download_media(file_id)
            try: 
                with open(file) as file_data:
                    msgs=json.loads(file_data.read())
            except:
                await sts.edit("FAILED")
                return await client.send_message(LOG_CHANNEL, "UNABLE TO OPEN FILE.")
            os.remove(file)
            BATCH_FILES[file_id] = msgs
        new_messages = []
        for msg in msgs:
            title = msg.get("title")
            size=get_size(int(msg.get("size", 0)))
            f_caption=msg.get("caption", "")
            if BATCH_FILE_CAPTION:
                try:
                    f_caption=BATCH_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption=f_caption
            if f_caption is None:
                f_caption = f"{title}"
            try:
                bj = await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton('🖥 𝗡𝗘𝗪 𝗢𝗧𝗧 𝗨𝗣𝗗𝗔𝗧𝗘𝗦 🖥', url=f"https://t.me/MCUupdatesLINKS"),InlineKeyboardButton('⭕️ 𝐌𝐎𝐕𝐈𝐄 𝐆𝐑𝐎𝐔𝐏 𝐋𝐈𝐍𝐊 ⭕️', url="https://t.me/+JRWRXAzDwkc2NDA1")]] ))
            except FloodWait as e:
                await asyncio.sleep(e.x)
                logger.warning(f"Floodwait of {e.x} sec.")
                bj = await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton('🖥 𝗡𝗘𝗪 𝗢𝗧𝗧 𝗨𝗣𝗗𝗔𝗧𝗘𝗦 🖥', url=f"https://t.me/MCUupdatesLINKS"),InlineKeyboardButton('⭕️ 𝐌𝐎𝐕𝐈𝐄 𝐆𝐑𝐎𝐔𝐏 𝐋𝐈𝐍𝐊 ⭕️', url="https://t.me/+JRWRXAzDwkc2NDA1")]]))
            except Exception as e:
                logger.warning(e, exc_info=True)
                continue
            new_messages.append(bj)
            await asyncio.sleep(1) 
        await sts.delete()
        ok = await message.reply_text(
            text=script.DELETE_TXT,
            disable_web_page_preview=True,   
            reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton('🖥 𝗡𝗘𝗪 𝗢𝗧𝗧 𝗨𝗣𝗗𝗔𝗧𝗘𝗦 🖥', url=f"https://t.me/MCUupdatesLINKS"),InlineKeyboardButton('⭕️ 𝐌𝐎𝐕𝐈𝐄 𝐆𝐑𝐎𝐔𝐏 𝐋𝐈𝐍𝐊 ⭕️', url="https://t.me/+JRWRXAzDwkc2NDA1")]]))
        await asyncio.sleep(300)
        for sodha in new_messages:
            await sodha.delete()
            await ok.delete()
        await message.reply_text(
            text="<b>Your File Has Been Deleted To Avoid BOT Ban.😇\nYou Can Request Again If You Want!🫵🏻</b>",
            disable_web_page_preview=True,   
            reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton('🖥 𝗡𝗘𝗪 𝗢𝗧𝗧 𝗨𝗣𝗗𝗔𝗧𝗘𝗦 🖥', url=f"https://t.me/MCUupdatesLINKS"),InlineKeyboardButton('⭕️ 𝐌𝐎𝐕𝐈𝐄 𝐆𝐑𝐎𝐔𝐏 𝐋𝐈𝐍𝐊 ⭕️', url="https://t.me/+JRWRXAzDwkc2NDA1")] ]))
        return
    
    elif data.split("-", 1)[0] == "DSTORE":
        sts = await message.reply("𝖥𝖾𝗍𝖼𝗁𝗂𝗇𝗀 𝖳𝗁𝖾 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖥𝗂𝗅𝖾𝗌.....\n𝖪𝗂𝗇𝖽𝗅𝗒 𝖶𝖺𝗂𝗍!!!!")
        b_string = data.split("-", 1)[1]
        decoded = (base64.urlsafe_b64decode(b_string + "=" * (-len(b_string) % 4))).decode("ascii")
        try:
            f_msg_id, l_msg_id, f_chat_id, protect = decoded.split("_", 3)
        except:
            f_msg_id, l_msg_id, f_chat_id = decoded.split("_", 2)
            protect = "/pbatch" if PROTECT_CONTENT else "batch"
        diff = int(l_msg_id) - int(f_msg_id)
        messages = list()
        async for msg in client.iter_messages(int(f_chat_id), int(l_msg_id), int(f_msg_id)):
            if msg.media:
                media = getattr(msg, msg.media.value)
                if BATCH_FILE_CAPTION:
                    try:
                        f_caption=BATCH_FILE_CAPTION.format(file_name=getattr(media, 'file_name', ''), file_size=getattr(media, 'file_size', ''), file_caption=getattr(msg, 'caption', ''))
                    except Exception as e:
                        logger.exception(e)
                        f_caption = getattr(msg, 'caption', '')
                else:
                    media = getattr(msg, msg.media.value)
                    file_name = getattr(media, 'file_name', '')
                    f_caption = getattr(msg, 'caption', file_name)
                try:
                    _m = await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                    messages.append(_m)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    _m = await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                    messages.append(_m)
                except Exception as e:
                    logger.exception(e)
                    continue
            elif msg.empty:
                continue
            else:
                try:
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            await asyncio.sleep(1)
        await sts.delete()
        ok = await message.reply_text(
            text=script.DELETE_TXT,
            disable_web_page_preview=True,   
            reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton('🖥 𝗡𝗘𝗪 𝗢𝗧𝗧 𝗨𝗣𝗗𝗔𝗧𝗘𝗦 🖥', url=f"https://t.me/MCUupdatesLINKS"),InlineKeyboardButton('⭕️ 𝐌𝐎𝐕𝐈𝐄 𝐆𝐑𝐎𝐔𝐏 𝐋𝐈𝐍𝐊 ⭕️', url="https://t.me/+JRWRXAzDwkc2NDA1")]]))
        await asyncio.sleep(20)
        for _m in messages:
            await _m.delete()
            await message.reply_text(
                text="<b>Your File Has Been Deleted To Avoid BOT Ban.😇\nYou Can Request Again If You Want!🫵🏻</b>",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton('🖥 𝗡𝗘𝗪 𝗢𝗧𝗧 𝗨𝗣𝗗𝗔𝗧𝗘𝗦 🖥', url=f"https://t.me/MCUupdatesLINKS"),InlineKeyboardButton('⭕️ 𝐌𝐎𝐕𝐈𝐄 𝐆𝐑𝐎𝐔𝐏 𝐋𝐈𝐍𝐊 ⭕️', url="https://t.me/+JRWRXAzDwkc2NDA1")]]))
            return

    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                protect_content=True if pre == 'filep' else False,
                reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton('🖥 𝗡𝗘𝗪 𝗢𝗧𝗧 𝗨𝗣𝗗𝗔𝗧𝗘𝗦 🖥', url=f"https://t.me/MCUupdatesLINKS"),InlineKeyboardButton('⭕️ 𝐌𝐎𝐕𝐈𝐄 𝐆𝐑𝐎𝐔𝐏 𝐋𝐈𝐍𝐊 ⭕️', url="https://t.me/+JRWRXAzDwkc2NDA1")]] ))
            filetype = msg.media
            file = getattr(msg, filetype)
            title = file.file_name
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                except:
                    return
            await msg.edit_caption(f_caption)
            return
        except:
            pass
        return await message.reply('No such file exist.')
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    f = await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton('🖥 𝗡𝗘𝗪 𝗢𝗧𝗧 𝗨𝗣𝗗𝗔𝗧𝗘𝗦 🖥', url=f"https://t.me/MCUupdatesLINKS"),InlineKeyboardButton('⭕️ 𝐌𝐎𝐕𝐈𝐄 𝐆𝐑𝐎𝐔𝐏 𝐋𝐈𝐍𝐊 ⭕️', url="https://t.me/+JRWRXAzDwkc2NDA1")] ] ))
    ok = await message.reply_text(
        text=script.DELETE_TXT,
        disable_web_page_preview=True,   
        reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton('🖥 𝗡𝗘𝗪 𝗢𝗧𝗧 𝗨𝗣𝗗𝗔𝗧𝗘𝗦 🖥', url=f"https://t.me/MCUupdatesLINKS"),InlineKeyboardButton('⭕️ 𝐌𝐎𝐕𝐈𝐄 𝐆𝐑𝐎𝐔𝐏 𝐋𝐈𝐍𝐊 ⭕️', url="https://t.me/+JRWRXAzDwkc2NDA1")]]))
    await asyncio.sleep(300)
    await f.delete()
    await ok.delete()
    await message.reply_text(
        text="<b>Your File Has Been Deleted To Avoid BOT Ban.😇\nYou Can Request Again If You Want!🫵🏻</b>",
        disable_web_page_preview=True,   
        reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton('🖥 𝗡𝗘𝗪 𝗢𝗧𝗧 𝗨𝗣𝗗𝗔𝗧𝗘𝗦 🖥', url=f"https://t.me/MCUupdatesLINKS"),InlineKeyboardButton('⭕️ 𝐌𝐎𝐕𝐈𝐄 𝐆𝐑𝐎𝐔𝐏 𝐋𝐈𝐍𝐊 ⭕️', url="https://t.me/+JRWRXAzDwkc2NDA1")]]))
    return

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)

@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.txt')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("⏳", quote=True)
    else:
        await message.reply('**Reply to the file with /delete that you want to delete**', quote=True)
        return

    for file_type in ("document", "video"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('**This is not a supported file format**')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    # Check if the file exists in Media collection
    result_media1 = await Media2.collection.find_one({'_id': file_id})

    # Check if the file exists in Mediaa collection
    result_media2 = await Media3.collection.find_one({'_id': file_id})   
    result_media3 = await Media4.collection.find_one({'_id': file_id})   
    result_media4 = await Media5.collection.find_one({'_id': file_id})   
        
    if result_media1:
        # Delete from Media collection
        await Media2.collection.delete_one({'_id': file_id})
    elif result_media2:
        # Delete from Mediaa collection
        await Media3.collection.delete_one({'_id': file_id})
    elif result_media3:
        # Delete from Mediaa collection
        await Media4.collection.delete_one({'_id': file_id})
    elif result_media4:
        # Delete from Mediaa collection
        await Media5.collection.delete_one({'_id': file_id})
    else:
        # File not found in both collections
        await msg.edit('File not found in the database')
        return

    await msg.edit('File is successfully deleted from the database')

@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="CANCEL", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )

@Client.on_message(filters.command('settings'))
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)

    if settings is not None:
        buttons = [
            [
                InlineKeyboardButton(
                    '🍾 𝖶𝖾𝗅𝖼𝗈𝗆𝖾',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ 𝖸𝖾𝗌' if settings["welcome"] else '❌ 𝖭𝗈',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    '🔎 𝖲𝗉𝖾𝗅𝗅 𝖢𝗁𝖾𝖼𝗄',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✅ 𝖸𝖾𝗌' if settings["spell_check"] else '❌ 𝖭𝗈',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply_text(
            text=f"<b>𝖢𝗁𝖺𝗇𝗀𝖾 𝖸𝗈𝗎𝗋 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌 𝖥𝗈𝗋 {title} 𝖠𝗌 𝖸𝗈𝗎𝗋 𝖶𝗂𝗌𝗁</b>",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=message.id
        )

@Client.on_message(filters.command('restart') & filters.user(ADMINS))
async def restart_bot(client, message):
    msg = await message.reply_text(
        text="<b>Bot Restarting ...</b>"
    )        
    await msg.edit("<b>Restart Successfully Completed ✅</b>")
    system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
    execle(sys.executable, sys.executable, "bot.py", environ)
    
@Client.on_message(filters.command("deletefiles") & filters.user(ADMINS))
async def deletemultiplefiles(bot, message):
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, This command won't work in groups. It only works on my PM !</b>")
    else:
        pass
    try:
        keyword = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, Give me a keyword along with the command to delete files.</b>")
    btn = [[
       InlineKeyboardButton("YES", callback_data=f"killfilesdq#{keyword}")
       ],[
       InlineKeyboardButton("CANCEL", callback_data="close_data")
    ]]
    await message.reply_text(
        text="<b>Are You Sure About That?",
        reply_markup=InlineKeyboardMarkup(btn),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command("deleteallf") & filters.user(ADMINS))
async def process_command(client, message):
    chat_id = message.chat.id
    processing_message = await message.reply_text("<b>Processing: Deleting files...</b>")
    
    total_files_deleted = 0
    batch_size = 250

    while True:
        deleted_files = await delete_files_below_threshold(db, threshold_size_mb=40, batch_size=batch_size)
        
        if deleted_files == 0:
            break

        total_files_deleted += deleted_files

        # Update the message to show progress
        progress_message = f'<b>Processing: Deleted {total_files_deleted} files in {total_files_deleted // batch_size} batches.</b>'
        await processing_message.edit_text(progress_message)
        await asyncio.sleep(3)

    print(f'Total files deleted: {total_files_deleted}')
    await processing_message.edit_text(f'<b>Deletion complete: Deleted {total_files_deleted} files.</b>')

@Client.on_message(filters.command("deleted") & filters.user(ADMINS))
async def delete_duplicate_files(client, message):
    ok = await message.reply("prosessing...")
    deleted_count = 0
    batch_size = 0
    async def remove_duplicates(collection, unique_files, ok, deleted_count, batch_size):                        
        async for duplicate_file in collection.find():
            file_size = duplicate_file["file_size"]
            file_id = duplicate_file["file_id"]
            if file_size in unique_files and unique_files[file_size] != file_id:
                result_media1 = await Media2.collection.find_one({'_id': file_id})
                result_media2 = await Media3.collection.find_one({'_id': file_id})   
                result_media3 = await Media4.collection.find_one({'_id': file_id})   
                result_media4 = await Media5.collection.find_one({'_id': file_id})   
                if result_media1:
                    await Media2.collection.delete_one({'_id': file_id})
                elif result_media2:
                    await Media3.collection.delete_one({'_id': file_id})
                elif result_media3:
                    await Media4.collection.delete_one({'_id': file_id})
                elif result_media4:
                    await Media5.collection.delete_one({'_id': file_id})
                deleted_count += 1                
                if deleted_count % 100 == 0:
                    batch_size += 1
                    await ok.edit(f'<b>Processing: Deleted {deleted_count} files in {batch_size} batches.</b>')
        return deleted_count, batch_size
    # Get all four collections
    media1_collection = Media5
    media2_collection = Media2
    media3_collection = Media3
    media4_collection = Media4

    # Get all files from each collection
    all_files_media1 = await media1_collection.find({}, {"file_id": 1, "file_size": 1}).to_list(length=None)
    all_files_media2 = await media2_collection.find({}, {"file_id": 1, "file_size": 1}).to_list(length=None)
    all_files_media3 = await media3_collection.find({}, {"file_id": 1, "file_size": 1}).to_list(length=None)
    all_files_media4 = await media4_collection.find({}, {"file_id": 1, "file_size": 1}).to_list(length=None)

    # Combine files from all collections
    all_files = all_files_media1 + all_files_media2 + all_files_media3 + all_files_media4

    # Remove duplicate files while keeping one copy
    unique_files = {}
    for file_info in all_files:
        file_id = file_info["file_id"]
        file_size = file_info["file_size"]
        if file_size not in unique_files:
            unique_files[file_size] = file_id

    # Delete duplicate files from each collection
    deleted_count, batch_size = await remove_duplicates(media1_collection, unique_files, ok, deleted_count, batch_size)
    deleted_count = deleted_count
    batch_size = batch_size
    deleted_count, batch_size = await remove_duplicates(media2_collection, unique_files, ok, deleted_count, batch_size)
    deleted_count = deleted_count
    batch_size = batch_size
    deleted_count, batch_size = await remove_duplicates(media3_collection, unique_files, ok, deleted_count, batch_size)
    deleted_count = deleted_count
    batch_size = batch_size
    deleted_count, batch_size = await remove_duplicates(media4_collection, unique_files, ok, deleted_count, batch_size)    
    deleted_count = deleted_count
    batch_size = batch_size
    
    # Send a final message indicating the total number of duplicates deleted
    await message.reply(f"Deleted {deleted_count} duplicate files. in {batch_size} batches")

async def forward_files(chat_id, skip_count, channel_id, bot, message):
    total_files = skip_count

    # Fetch files from the first database
    cursor1 = Media2.collection.find()
    cursor2 = Media3.collection.find()
    cursor3 = Media4.collection.find()
    cursor4 = Media5.collection.find()
    
    files1 = await cursor1.to_list(length=None)
    files2 = await cursor2.to_list(length=None)
    files3 = await cursor3.to_list(length=None)
    files4 = await cursor4.to_list(length=None)
    
    # Combine files from both databases
    files = files1 + files2 + files3 + files4

    all_files = files[skip_count:skip_count+3000]

    for i, file in enumerate(all_files, 1):
        caption = file["file_name"]
        await bot.send_cached_media(
            chat_id=int(channel_id),
            file_id=file["_id"],
            caption=f'<b>{file_name}\n\n{file_caption}<\n\n🎊 𝖯𝗈𝗐𝖾𝗋𝖾𝖽 𝖡𝗒 [[𝖯𝗂𝖱𝖮]](t.me/piroxbots)</b>'
        )
        total_files += 1                
        fcol.update_one({"_id": "forward_progress"}, {"$set": {"last_forwarded_file": total_files}}, upsert=True)
        if total_files % 20 == 0:
            tz = pytz.timezone('Asia/Kolkata')
            today = datetime.date.today()
            now = datetime.datetime.now(tz)
            ttime = now.strftime("%I:%M:%S %p - %d %b, %Y")      
            await message.edit(f"Forwarded {total_files} files. \n\nlast updated at {ttime}")
        await asyncio.sleep(3.5)
    balance = len(files) - total_files
    return total_files, balance

async def handle_forward_command(update, bot):
    message = update
    chat_id = message.chat.id    
    channel_id = "-1002231012161"    
    reply_message = await message.reply_text("Forwarding files...")
    while True: 
        progress_document = fcol.find_one({"_id": "forward_progress"})    
        if progress_document:
            skip_count = progress_document.get("last_forwarded_file", 0)
        else:
            skip_count = 0
        total_forwarded, balance = await forward_files(chat_id, skip_count, channel_id, bot, reply_message)
        if balance == 0:
            await reply_message.edit(f"Forwarded {total_forwarded} files.")
            break
            
@Client.on_message(filters.command("forward") & filters.user(ADMINS))
async def forward_command_handler(client, message):
    await handle_forward_command(message, client)
