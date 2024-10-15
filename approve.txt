import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import Message, User, ChatJoinRequest
from pyrogram.errors import UserIsBlocked, PeerIdInvalid
from info import JOIN_CHANNELS, PIRO_CHANNELS

@Client.on_chat_join_request((filters.group | filters.channel) & filters.chat(JOIN_CHANNELS) if JOIN_CHANNELS else (filters.group | filters.channel))
async def accept_request(client, r):

    rm = InlineKeyboardMarkup([[
        InlineKeyboardButton('🔰 𝖡𝖫𝖠𝖲𝖳𝖤𝖱 𝖫𝖨𝖭𝖪𝖹 🔰', url=f"https://t.me/blaster_linkz"),
        InlineKeyboardButton('🚀 𝖯𝖨𝖱𝖮 𝖡𝖮𝖳𝖲 🚀', url=f"https://t.me/piroxbots")
    ]])
    
    try:
        await client.send_photo(
            r.from_user.id,
            'https://graph.org/file/5cb80fa6096997b7226b3.jpg',
            f"**𝖧𝖾𝗅𝗅𝗈 {r.from_user.mention} 👻, 𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖳𝗈 {r.chat.title}\n𝖸𝗈𝗎𝗋 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖧𝖺𝗌 𝖡𝖾𝖾𝗇 𝖠𝗉𝗉𝗋𝗈𝗏𝖾𝖽...!!!\n\n𝖧𝗂𝗍 /joinchannels 𝖥𝗈𝗋 𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌.\n\n𝖧𝗂𝗍 /help 𝖥𝗈𝗋 𝖬𝗈𝗋𝖾 𝖦𝗎𝗂𝖽𝖺𝗇𝖼𝖾.**",
            reply_markup=rm)

    except UserIsBlocked:
        print("User blocked the bot")
    except PeerIdInvalid:
        print("Err")
    except Exception as e:
        print(f"#Error\n{str(e)}")

    await r.approve()

@Client.on_chat_join_request((filters.group | filters.channel) & filters.chat(PIRO_CHANNELS) if PIRO_CHANNELS else (filters.group | filters.channel))
async def accept_request(client, r):

    rm = InlineKeyboardMarkup([
        [InlineKeyboardButton('⚡️ 𝖯𝖨𝖱𝖮 𝖥𝖨𝖫𝖤𝖲 [𝖶𝖺𝗂𝗍𝗂𝗇𝗀 𝖠𝗋𝖾𝗇𝖺] ⚡️', url=f"https://t.me/piro_files")],
        [InlineKeyboardButton('🔰 𝖡𝖫𝖠𝖲𝖳𝖤𝖱 𝖫𝖨𝖭𝖪𝖹 🔰', url=f"https://t.me/blaster_linkz"),
        InlineKeyboardButton('🚀 𝖯𝖨𝖱𝖮 𝖡𝖮𝖳𝖲 🚀', url=f"https://t.me/piroxbots")
        ]])
    
    try:
        await client.send_photo(
            r.from_user.id,
            'https://graph.org/file/00567846bb6fa88ad4c29.jpg',
            f"**𝖧𝖾𝗅𝗅𝗈 {r.from_user.mention} 👻, 𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖳𝗈 {r.chat.title}\n𝖸𝗈𝗎𝗋 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖧𝖺𝗌 𝖡𝖾𝖾𝗇 𝖠𝗉𝗉𝗋𝗈𝗏𝖾𝖽...!!!\n\n𝖧𝗂𝗍 /joinchannels 𝖥𝗈𝗋 𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌.\n\n𝖧𝗂𝗍 /help 𝖥𝗈𝗋 𝖬𝗈𝗋𝖾 𝖦𝗎𝗂𝖽𝖺𝗇𝖼𝖾.**",
            reply_markup=rm)

    except UserIsBlocked:
        print("User blocked the bot")
    except PeerIdInvalid:
        print("Err")
    except Exception as e:
        print(f"#Error\n{str(e)}")

    await r.approve()