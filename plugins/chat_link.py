from pyrogram import Client, filters 
from info import JOIN_CHANNELS
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from datetime import datetime, timedelta

@Client.on_message(filters.command("joinchannels") & filters.incoming & filters.private)
async def check_joined(client, message):
    sts = await message.reply("Checking......")
    text = "<b><u>⚡️ 𝗖𝗵𝗲𝗰𝗸𝗼𝘂𝘁 𝗢𝘂𝗿 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀 ⚡️</u></b>\n\n"
    buttons = []
    for i, channel in enumerate(JOIN_CHANNELS, start=1):
        chat = await client.get_chat(channel)
        text += f"<b>{i}. {chat.title}: </b>"
        try:
            await client.get_chat_member(chat_id=channel, user_id=message.from_user.id)
        except UserNotParticipant:
            now = datetime.now()
            revoke_time = now + timedelta(minutes=3)
            text += "❌"
            invite_link = (await client.create_chat_invite_link(chat_id=channel, expire_date=revoke_time, creates_join_request=True)).invite_link
            buttons.append([InlineKeyboardButton(chat.title, url=invite_link)])
        else:
            text += "✅"
        text += "\n"
    text += "<b><i>\n⚠️ 𝗡𝗢𝗧𝗘:\n𝖠𝗅𝗅 𝖫𝗂𝗇𝗄𝗌 𝖶𝗂𝗅𝗅 𝖡𝖾 𝖦𝖾𝗍𝗍𝗂𝗇𝗀 𝖤𝗑𝗉𝗂𝗋𝖾𝖽 𝖶𝗂𝗍𝗁𝗂𝗇 3 𝖬𝗂𝗇𝗎𝗍𝖾𝗌!\n\n𝖨𝖿 𝖳𝗁𝖾 𝖫𝗂𝗇𝗄 𝖤𝗑𝗉𝗂𝗋𝖾𝖽, 𝖢𝗅𝗂𝖼𝗄 /joinchannels 𝗍𝗈 𝖦𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝖭𝖾𝗐.\n\n🔥 𝖩𝗈𝗂𝗇 @piroxbots 𝖥𝗈𝗋 𝖬𝗈𝗋𝖾</b>"
    await sts.edit(text=text, reply_markup=InlineKeyboardMarkup(buttons) if buttons != [] else None)