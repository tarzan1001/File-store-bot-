from pyrogram import Client, filters, enums
import os, pytz, re, datetime, logging, asyncio, math, time, sys, psutil, shutil
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from database.ia_inlinedb import Media2, Media3, Media4, Media5, get_file_details, get_search_results, get_bad_files, db as clientDB, db2 as clientDB2, db3 as clientDB3, db4 as clientDB4, db5 as clientDB5
from info import ADMINS, LOG_CHANNEL, MELCOW_NEW_USERS
from database.users_chats_db import db
from utils import get_size, temp, get_settings
from Script import script
from pyrogram.errors import ChatAdminRequired
from utils import humanbytes

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    r_j_check = [u.id for u in message.new_chat_members]
    if temp.ME in r_j_check:
        if not await db.get_chat(message.chat.id):
            total=await bot.get_chat_members_count(message.chat.id)
            r_j = message.from_user.mention if message.from_user else "Anonymous" 
            await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j))       
            await db.add_chat(message.chat.id, message.chat.title)
        if message.chat.id in temp.BANNED_CHATS:
            buttons = [[InlineKeyboardButton('🧬 𝖲𝗎𝗉𝗉𝗈𝗋𝗍', url=f'https://t.me/raixchat')]]
            reply_markup=InlineKeyboardMarkup(buttons)
            k = await message.reply(
                text='**𝖳𝗁𝗂𝗌 𝖢𝗁𝖺𝗍 𝖨𝗌 𝖭𝗈𝗍 𝖠𝗅𝗅𝗈𝗐𝖾𝖽.!\n𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖬𝗒 𝖬𝖺𝗌𝗍𝖾𝗋.**',
                reply_markup=reply_markup,
            )

            try:
                await k.pin()
            except:
                pass
            await bot.leave_chat(message.chat.id)
            return
        buttons = [[
            InlineKeyboardButton('🧬 𝖲𝗎𝗉𝗉𝗈𝗋𝗍', url=f'https://t.me/raixchat'),
            InlineKeyboardButton('⚡𝖴𝗉𝖽𝖺𝗍𝖾𝗌', url=f'https://t.me/piroxbots')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=f"𝗧𝗵𝗮𝗻𝗸𝘀 𝗙𝗼𝗿 𝗔𝗱𝗱𝗶𝗻𝗴 𝗠𝗲 𝗜𝗻 {message.chat.title} ❣️\n**𝖨𝖿 𝖸𝗈𝗎 𝖧𝖺𝗏𝖾 𝖠𝗇𝗒 𝖣𝗈𝗎𝖻𝗍𝗌, 𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖲𝗎𝗉𝗉𝗈𝗋𝗍.!**",
            reply_markup=reply_markup)
    else:
        settings = await get_settings(message.chat.id)
        if settings["welcome"]:
            for u in message.new_chat_members:
                if (temp.MELCOW).get('welcome') is not None:
                    try:
                        await (temp.MELCOW['welcome']).delete()
                    except:
                        pass
                temp.MELCOW['welcome'] = await message.reply(f"<b>𝖧𝖾𝗅𝗅𝗈 𝖳𝗁𝖾𝗋𝖾, {u.mention}🎊,\n𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖳𝗈 {message.chat.title}</b>")

@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        buttons = [[InlineKeyboardButton('🧬 𝖲𝗎𝗉𝗉𝗈𝗋𝗍', url=f'https://t.me/raixchat')]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat,
            text='**𝖳𝗁𝗂𝗌 𝖢𝗁𝖺𝗍 𝖨𝗌 𝖭𝗈𝗍 𝖠𝗅𝗅𝗈𝗐𝖾𝖽.!\n𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖬𝗒 𝖬𝖺𝗌𝗍𝖾𝗋.**',
            reply_markup=reply_markup,
        )

        await bot.leave_chat(chat)
        await message.reply(f"left the chat `{chat}`")
    except Exception as e:
        await message.reply(f'Error - {e}')

@Client.on_message(filters.command('disable') & filters.user(ADMINS))
async def disable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat_ = int(chat)
    except:
        return await message.reply('Give Me A Valid Chat ID')
    cha_t = await db.get_chat(int(chat_))
    if not cha_t:
        return await message.reply("Chat Not Found In DB")
    if cha_t['is_disabled']:
        return await message.reply(f"This chat is already disabled:\nReason-<code> {cha_t['reason']} </code>")
    await db.disable_chat(int(chat_), reason)
    temp.BANNED_CHATS.append(int(chat_))
    await message.reply('Chat Successfully Disabled')
    try:
        buttons = [[
            InlineKeyboardButton('🧬 𝖲𝗎𝗉𝗉𝗈𝗋𝗍', url=f'https://t.me/raixchat')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat_, 
            text=f'**𝖳𝗁𝗂𝗌 𝖢𝗁𝖺𝗍 𝖨𝗌 𝖭𝗈𝗍 𝖠𝗅𝗅𝗈𝗐𝖾𝖽.!\n𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖬𝗒 𝖬𝖺𝗌𝗍𝖾𝗋.**\n\nReason : <code>{reason}</code>',
            reply_markup=reply_markup)
        await bot.leave_chat(chat_)
    except Exception as e:
        await message.reply(f"Error - {e}")

@Client.on_message(filters.command('enable') & filters.user(ADMINS))
async def re_enable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat_ = int(chat)
    except:
        return await message.reply('Give Me A Valid Chat ID')
    sts = await db.get_chat(int(chat))
    if not sts:
        return await message.reply("Chat Not Found In DB !")
    if not sts.get('is_disabled'):
        return await message.reply('This chat is not yet disabled.')
    await db.re_enable_chat(int(chat_))
    temp.BANNED_CHATS.remove(int(chat_))
    await message.reply("Chat Successfully re-enabled")

@Client.on_message(filters.command('invite') & filters.user(ADMINS))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        return await message.reply('Give Me A Valid Chat ID')
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply("Invite Link Generation Failed, Iam Not Having Sufficient Rights")
    except Exception as e:
        return await message.reply(f'Error {e}')
    await message.reply(f'Here is your Invite Link {link.invite_link}')

@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a user id / username')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("This is an invalid user, make sure ia have met him before.")
    except IndexError:
        return await message.reply("This might be a channel, make sure its a user.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"{k.mention} is already banned\nReason: {jar['ban_reason']}")
        await db.ban_user(k.id, reason)
        temp.BANNED_USERS.append(k.id)
        await message.reply(f"Successfully banned {k.mention}")
    
@Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a user id / username')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("This is an invalid user, make sure ia have met him before.")
    except IndexError:
        return await message.reply("Thismight be a channel, make sure its a user.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"{k.mention} is not yet banned.")
        await db.remove_ban(k.id)
        temp.BANNED_USERS.remove(k.id)
        await message.reply(f"Successfully unbanned {k.mention}")
    
@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    raju = await message.reply('Getting List Of Users')
    users = await db.get_all_users()
    out = "Users Saved In DB Are:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += '( Banned User )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="List Of Users")

@Client.on_message(filters.command('chats') & filters.user(ADMINS))
async def list_chats(bot, message):
    raju = await message.reply('Getting List Of chats')
    chats = await db.get_all_chats()
    out = "Chats Saved In DB Are:\n\n"
    async for chat in chats:
        out += f"**Title:** `{chat['title']}`\n**- ID:** `{chat['id']}`"
        if chat['chat_status']['is_disabled']:
            out += '( Disabled Chat )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('chats.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('chats.txt', caption="List Of Chats")

@Client.on_message(filters.command('status') & filters.user(ADMINS))
async def get_stats(bot, message):
    rju = await message.reply('👀')
    tot1 = await Media2.count_documents()
    tot2 = await Media3.count_documents()
    tot3 = await Media4.count_documents()
    tot4 = await Media5.count_documents()
    total = tot1 + tot2 + tot3 + tot4
    users = await db.total_users_count()
    chats = await db.total_chat_count()
    stats = await clientDB.command('dbStats')
    used_dbSize = (stats['dataSize']/(1024*1024))+(stats['indexSize']/(1024*1024))        
    stats2 = await clientDB2.command('dbStats')
    used_dbSize2 = (stats2['dataSize']/(1024*1024))+(stats2['indexSize']/(1024*1024))
    stats3 = await clientDB3.command('dbStats')
    used_dbSize3 = (stats3['dataSize']/(1024*1024))+(stats3['indexSize']/(1024*1024))  
    stats4 = await clientDB4.command('dbStats')
    used_dbSize4 = (stats4['dataSize']/(1024*1024))+(stats4['indexSize']/(1024*1024))  
    stats5 = await clientDB5.command('dbStats')
    used_dbSize5 = (stats5['dataSize']/(1024*1024))+(stats5['indexSize']/(1024*1024))  
    current = temp.CURRENT
    tz = pytz.timezone('Asia/Kolkata')
    today = datetime.date.today()
    now = datetime.datetime.now(tz)
    time = now.strftime("%I:%M:%S %p - %d %b, %Y")
    await rju.edit(
        text=script.STATUS_TXT.format(total, users, chats, round(used_dbSize, 2), tot1, round(used_dbSize2, 2), tot2, round(used_dbSize3, 2), tot3, round(used_dbSize4, 2), tot4, round(used_dbSize5, 2), time),
        parse_mode=enums.ParseMode.HTML)

@Client.on_message(filters.command('stats') & filters.incoming)
async def get_ststs(bot, message):
    rju = await message.reply('👀')
    tot1 = await Media2.count_documents()
    tot2 = await Media3.count_documents()
    tot3 = await Media4.count_documents()
    tot4 = await Media5.count_documents()
    total = tot1 + tot2 + tot3 + tot4
    users = await db.total_users_count()
    chats = await db.total_chat_count()
    stats = await clientDB.command('dbStats')
    used_dbSize = (stats['dataSize']/(1024*1024))+(stats['indexSize']/(1024*1024))        
    stats2 = await clientDB2.command('dbStats')
    used_dbSize2 = (stats2['dataSize']/(1024*1024))+(stats2['indexSize']/(1024*1024))
    stats3 = await clientDB3.command('dbStats')
    used_dbSize3 = (stats3['dataSize']/(1024*1024))+(stats3['indexSize']/(1024*1024))  
    stats4 = await clientDB4.command('dbStats')
    used_dbSize4 = (stats4['dataSize']/(1024*1024))+(stats4['indexSize']/(1024*1024))  
    stats5 = await clientDB5.command('dbStats')
    used_dbSize5 = (stats5['dataSize']/(1024*1024))+(stats5['indexSize']/(1024*1024))  
    current = temp.CURRENT
    tz = pytz.timezone('Asia/Kolkata')
    today = datetime.date.today()
    now = datetime.datetime.now(tz)
    time = now.strftime("%I:%M:%S %p - %d %b, %Y")
    await rju.edit(
        text=script.TOTAL_TXT.format(total, time),
        parse_mode=enums.ParseMode.HTML)

@Client.on_message(filters.command('tutorial'))
async def tutorial(client, message):
    await message.reply_video(
        video="https://graph.org/file/a9f37d2c26de7f9b74ecc.mp4",
        caption="**𝖶𝖺𝗍𝖼𝗁 𝖳𝗁𝗂𝗌 𝖳𝗎𝗍𝗈𝗋𝗂𝖺𝗅 𝖵𝗂𝖽𝖾𝗈 & 𝖦𝖾𝗍 𝖲𝗍𝖺𝗋𝗍𝖾𝖽!\n\n🚀 𝖬𝖺𝖽𝖾 𝖡𝗒 <a href='https://t.me/piroxbots'>[𝖯𝗂𝖱𝖮]</a>**",
        reply_markup=InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('📚 𝖱𝖤𝖰𝖴𝖤𝖲𝖳 𝖦𝖴𝖨𝖣𝖤 📚', url=f"https://graph.org/%F0%9D%97%A0%F0%9D%97%BC%F0%9D%98%83%F0%9D%97%B6%F0%9D%97%B2--%F0%9D%97%A6%F0%9D%97%B2%F0%9D%97%BF%F0%9D%97%B6%F0%9D%97%B2%F0%9D%98%80-%F0%9D%97%A5%F0%9D%97%B2%F0%9D%97%BE%F0%9D%98%82%F0%9D%97%B2%F0%9D%98%80%F0%9D%98%81-%F0%9D%97%9A%F0%9D%98%82%F0%9D%97%B6%F0%9D%97%B1%F0%9D%97%B2-11-29")
        ],[
            InlineKeyboardButton('👥 𝖲𝗎𝗉𝗉𝗈𝗋𝗍 𝖦𝗋𝗈𝗎𝗉 💭', url=f"https://t.me/raixchat")
        ]]
        ),
        quote=True)

@Client.on_message(filters.command('help'))
async def help(client, message):
    await message.reply_text(
        text=script.HELP_TXT.format(message.from_user.mention),
        parse_mode=enums.ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('📚 𝖱𝖤𝖰𝖴𝖤𝖲𝖳 𝖦𝖴𝖨𝖣𝖤 📚', url=f"https://graph.org/%F0%9D%97%A0%F0%9D%97%BC%F0%9D%98%83%F0%9D%97%B6%F0%9D%97%B2--%F0%9D%97%A6%F0%9D%97%B2%F0%9D%97%BF%F0%9D%97%B6%F0%9D%97%B2%F0%9D%98%80-%F0%9D%97%A5%F0%9D%97%B2%F0%9D%97%BE%F0%9D%98%82%F0%9D%97%B2%F0%9D%98%80%F0%9D%98%81-%F0%9D%97%9A%F0%9D%98%82%F0%9D%97%B6%F0%9D%97%B1%F0%9D%97%B2-11-29")
        ],[
            InlineKeyboardButton('👥 𝖲𝗎𝗉𝗉𝗈𝗋𝗍 𝖦𝗋𝗈𝗎𝗉 💭', url=f"https://t.me/raixchat")
        ]]
        ),
        quote=True)

@Client.on_message(filters.command('about'))
async def about(client, message):
    await message.reply_text(
        text=script.ABOUT_TEXT.format(message.from_user.mention),
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('🚀 𝖯𝖨𝖱𝖮 𝖡𝖮𝖳𝖲 🚀', url=f"https://t.me/piroxbots")
        ],[
            InlineKeyboardButton('👥 𝖲𝗎𝗉𝗉𝗈𝗋𝗍 𝖦𝗋𝗈𝗎𝗉 💭', url=f"https://t.me/raixchat")
        ]]
        ),
        quote=True)
