class script(object):
    START_TXT = """<b>𝖸𝗈 {}, 𝖭𝗂𝖼𝖾 𝖳𝗈 𝖬𝖾𝖾𝗍 𝖸𝗈𝗎 🎊

<blockquote>𝖨'𝗆 𝖠 𝖡𝖺𝗍𝖼𝗁 𝖥𝗂𝗅𝖾 𝖲𝗍𝗈𝗋𝖾 & 𝖨𝗇𝗅𝗂𝗇𝖾 𝖥𝗂𝗅𝖾 𝖲𝖾𝖺𝗋𝖼𝗁 𝖡𝗈𝗍.</blockquote>

𝖧𝗂𝗍 /joinchannels 𝖳𝗈 𝖦𝖾𝗍 𝖮𝗎𝗋 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖫𝗂𝗌𝗍𝗌.</b>
"""

    HELP_TXT = """<b>Hᴇʏ {} 𝖨𝖺𝗆 𝖧𝖺𝗉𝗉𝗒 🖤 𝖳𝗈 𝖧𝖺𝗏𝖾 𝖸𝗈𝗎
    
𝖶𝗂𝗍𝗁 𝖳𝗁𝗂𝗌 𝖧𝖾𝗅𝗉 𝖸𝗈𝗎 𝖶𝗂𝗅𝗅 𝖴𝗇𝖽𝖾𝗋𝗌𝗍𝖺𝗇𝖽 𝖧𝗈𝗐 𝖳𝗈 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖡𝗈𝗍🏌️
    
𝖢𝗁𝖾𝖼𝗄 𝖡𝖾𝗅𝗈𝗐 𝖧𝖾𝗅𝗉 𝖥𝗎𝗇𝖼𝗍𝗂𝗈𝗇𝗌🤍</b>"""

    ABOUT_TXT = """<b>𝖰𝗎𝗂𝖼𝗄𝗅𝗒 𝖩𝗈𝗂𝗇 𝖮𝗎𝗋 𝖦𝗋𝗈𝗎𝗉𝗌 & 𝖢𝗁𝖺𝗇𝗇𝖾𝗅,
𝖫𝖾𝗍 𝖳𝗁𝖾 𝖴𝗇𝗅𝗂𝗆𝗂𝗍𝖾𝖽 𝖥𝗎𝗇 𝖡𝖾𝗀𝗂𝗇.! 🚀</b>"""

    ABOUT_TEXT = """<b>
○ 𝖢𝗋𝖾𝖺𝗍𝗈𝗋 : <a href='https://t.me/MCU_ADMIN_V1_BOT'>[𝐍𝐚𝐳𝐫𝐢𝐲𝐚 𝐀𝐝𝐦𝐢𝐧]</a>
○ 𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾 : <a href='https://www.python.org/downloads/release/python-3106/'>𝖯𝗒𝗍𝗁𝗈𝗇 𝟥</a>
○ 𝖲𝖾𝗋𝗏𝖾𝗋 : <a href='https://cloud.google.com/learn/what-is-a-virtual-private-server'>VPS</a>
○ 𝖣𝖺𝗍𝖺𝖻𝖺𝗌𝖾 : <a href='https://www.mongodb.com'>𝖬𝗈𝗇𝗀𝗈𝖣𝖡 𝖥𝗋𝖾𝖾 𝖳𝗂𝖾𝗋</a></b>"""
   
    MCAHU_TXT = """<b>The new command features are listed below. More features coming soon
    
/start - Welcome🤗 (Help , About and others)
    
/setchat - force Sub Channel ID

/viewchat - which force sub running chek

/delchat - Delete Requests (force Sub)

/stats - Check Stats

/deletefiles - Movie name all Files delete 

/ping - Bot Speed , Cpu etc

/restart - Restart ✅

/logs - bot logs txt</b>"""

    STATUS_TXT = """<b><u>📂 𝖳𝗈𝗍𝖺𝗅 𝖥𝗂𝗅𝖾𝗌 -</u></b> <code>{}</code>

<b><u>🗃 𝖣𝖺𝗍𝖺𝖻𝖺𝗌𝖾 1️⃣</u></b>
╭ ▸ 𝖴𝗌𝖾𝗋𝗌 : <code>{}</code>
├ ▸ 𝖢𝗁𝖺𝗍𝗌  : <code>{}</code>
╰ ▸ 𝖴𝗌𝖾𝖽 𝖲𝗍𝗈𝗋𝖺𝗀𝖾: <code>{}</code>MB

<b><u>🗃 𝖣𝖺𝗍𝖺𝖻𝖺𝗌𝖾 2️⃣</u></b>
╭ ▸ 𝖳𝗈𝗍𝖺𝗅 𝖥𝗂𝗅𝖾𝗌 : <code>{}</code>
╰ ▸ 𝖴𝗌𝖾𝖽 𝖲𝗍𝗈𝗋𝖺𝗀𝖾: <code>{}</code>MB

<b><u>🗃 𝖣𝖺𝗍𝖺𝖻𝖺𝗌𝖾 3️⃣</u></b>
╭ ▸ 𝖳𝗈𝗍𝖺𝗅 𝖥𝗂𝗅𝖾𝗌 : <code>{}</code>
╰ ▸ 𝖴𝗌𝖾𝖽 𝖲𝗍𝗈𝗋𝖺𝗀𝖾: <code>{}</code>MB

<b><u>🗃 𝖣𝖺𝗍𝖺𝖻𝖺𝗌𝖾 4️⃣</u></b>
╭ ▸ 𝖳𝗈𝗍𝖺𝗅 𝖥𝗂𝗅𝖾𝗌 : <code>{}</code>
╰ ▸ 𝖴𝗌𝖾𝖽 𝖲𝗍𝗈𝗋𝖺𝗀𝖾: <code>{}</code>MB

<b><u>🗃 𝖣𝖺𝗍𝖺𝖻𝖺𝗌𝖾 5️⃣</u></b>
╭ ▸ 𝖳𝗈𝗍𝖺𝗅 𝖥𝗂𝗅𝖾𝗌 : <code>{}</code>
╰ ▸ 𝖴𝗌𝖾𝖽 𝖲𝗍𝗈𝗋𝖺𝗀𝖾: <code>{}</code>MB

<blockquote><b><u>🚀 𝖫𝖺𝗌𝗍 𝖴𝗉𝖽𝖺𝗍𝖾𝖽 𝖮𝗇 🚀</u></b>
{}</blockquote>"""

    TOTAL_TXT = """<b><u>📂 𝖳𝗈𝗍𝖺𝗅 𝖥𝗂𝗅𝖾𝗌 -</u></b> <code>{}</code>

<blockquote><b><u>🚀 𝖫𝖺𝗌𝗍 𝖴𝗉𝖽𝖺𝗍𝖾𝖽 𝖮𝗇 🚀</u></b>
{}</blockquote>"""

    LOG_TEXT_G = """#NewGroup
Group = {}(<code>{}</code>)
Total Members = <code>{}</code>
Added By - {}
"""

    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Name - {}
"""

    SPELL_TEXT = """<b>🔖 𝖸𝗈 {} ,
𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖬𝗈𝗏𝗂𝖾/𝖲𝖾𝗋𝗂𝖾𝗌 𝖡𝖠𝖳𝖢𝖧 𝖥𝗂𝗅𝖾𝗌 𝖠𝗋𝖾 𝖭𝗈𝗍 𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾.

𝖧𝗂𝗍 /check 𝖳𝗈 𝖦𝖾𝗍 𝖫𝗂𝗌𝗍 𝖮𝖿 𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝖬𝗈𝗏𝗂𝖾𝗌/𝖲𝖾𝗋𝗂𝖾𝗌 𝖡𝖠𝖳𝖢𝖧 𝖥𝗂𝗅𝖾𝗌.

𝖪𝗂𝗇𝖽𝗅𝗒 𝖴𝗌𝖾 𝖮𝗎𝗋 𝖡𝖾𝗅𝗈𝗐 𝖡𝗈𝗍𝗌 𝖥𝗈𝗋 𝖠𝖽𝖽𝗂𝗍𝗂𝗈𝗇𝖺𝗅 𝖬𝗈𝗏𝗂𝖾𝗌/𝖲𝖾𝗋𝗂𝖾𝗌</b>
"""

    DMCA_TXT = """<b>📯𝗗𝗜𝗦𝗖𝗟𝗔𝗜𝗠𝗘𝗥 :
<blockquote>𝖠𝗅𝗅 𝗍𝗁𝖾 𝖿𝗂𝗅𝖾𝗌 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍 𝖺𝗋𝖾 𝖿𝗋𝖾𝖾𝗅𝗒 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝗈𝗇 𝗍𝗁𝖾 𝗂𝗇𝗍𝖾𝗋𝗇𝖾𝗍 𝗈𝗋 𝗉𝗈𝗌𝗍𝖾𝖽 𝖻𝗒 𝗌𝗈𝗆𝖾𝖻𝗈𝖽𝗒 𝖾𝗅𝗌𝖾.
𝖳𝗁𝗂𝗌 𝖻𝗈𝗍 𝗂𝗌 𝗂𝗇𝖽𝖾𝗑𝗂𝗇𝗀 𝖿𝗂𝗅𝖾𝗌 𝗐𝗁𝗂𝖼𝗁 𝖺𝗋𝖾 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝗎𝗉𝗅𝗈𝖺𝖽𝖾𝖽 𝗈𝗇 𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖿𝗈𝗋 𝖾𝖺𝗌𝖾 𝗈𝖿 𝗌𝖾𝖺𝗋𝖼𝗁𝗂𝗇𝗀,
𝖶𝖾 𝗋𝖾𝗌𝗉𝖾𝖼𝗍 𝖺𝗅𝗅 𝗍𝗁𝖾 𝖼𝗈𝗉𝗒𝗋𝗂𝗀𝗁𝗍 𝗅𝖺𝗐𝗌 𝖺𝗇𝖽 𝗐𝗈𝗋𝗄𝗌 𝗂𝗇 𝖼𝗈𝗆𝗉𝗅𝗂𝖺𝗇𝖼𝖾 𝗐𝗂𝗍𝗁 𝖣𝖬𝖢𝖠 𝖺𝗇𝖽 𝖤𝖴𝖢𝖣.</blockquote>

𝖨𝖿 𝖺𝗇𝗒𝗍𝗁𝗂𝗇𝗀 𝗂𝗌 𝖺𝗀𝖺𝗂𝗇𝗌𝗍 𝗅𝖺𝗐 𝗉𝗅𝖾𝖺𝗌𝖾 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 𝗎𝗌 𝗌𝗈 𝗍𝗁𝖺𝗍 𝗂𝗍 𝖼𝖺𝗇 𝖻𝖾 𝗋𝖾𝗆𝗈𝗏𝖾𝖽 𝖺𝗌𝖺𝗉.</b>"""

    DELETE_TXT = """‼️ 𝗜𝗠𝗣𝗢𝗥𝗧𝗔𝗡𝗧 ‼️

<blockquote>⚠️ 𝙁𝙞𝙡𝙚 𝙒𝙞𝙡𝙡 𝘽𝙚 𝘿𝙚𝙡𝙚𝙩𝙚𝙙 𝙄𝙣 𝟱 𝙈𝙞𝙣𝙪𝙩𝙚𝙨.</blockquote>

𝗜𝗳 𝘆𝗼𝘂 𝘄𝗮𝗻𝘁 𝘁𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘁𝗵𝗲𝘀𝗲 𝗳𝗶𝗹𝗲𝘀, 𝗞𝗶𝗻𝗱𝗹𝘆 𝗙𝗼𝗿𝘄𝗮𝗿𝗱 𝘁𝗵𝗲𝘀𝗲 𝗳𝗶𝗹𝗲𝘀 𝘁𝗼 𝗮𝗻𝘆 𝗰𝗵𝗮𝘁 (𝘀𝗮𝘃𝗲𝗱) 𝗮𝗻𝗱 𝘀𝘁𝗮𝗿𝘁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱...

<blockquote>𝗙𝗼𝗿 𝗠𝗼𝗿𝗲 𝗤𝘂𝗮𝗹𝗶𝘁𝗮𝘁𝗶𝘃𝗲 𝗙𝗶𝗹𝗲𝘀 𝗨𝘀𝗲 𝗕𝗲𝗹𝗼𝘄 𝗕𝗼𝘁𝘀.</blockquote>

𝗧𝗵𝗮𝗻𝗸 𝗬𝗼𝘂 :)"""

#𝗝𝘂𝘀𝘁 𝗦𝗲𝗻𝗱 𝗖𝗼𝗿𝗿𝗲𝗰𝘁 𝗠𝗼𝘃𝗶𝗲/𝗦𝗲𝗿𝗶𝗲𝘀 𝗡𝗮𝗺𝗲 𝗪𝗶𝘁𝗵𝗼𝘂𝘁 𝗦𝗽𝗲𝗹𝗹𝗶𝗻𝗴 𝗠𝗶𝘀𝘁𝗮𝗸𝗲𝘀.
#𝗜 𝗪𝗶𝗹𝗹 𝗦𝗲𝗻𝗱 𝗙𝗶𝗹𝗲𝘀 𝗧𝗼 𝗬𝗼𝘂.
#[𝖣𝗈𝗇'𝗍 𝖴𝗌𝖾 𝖠𝗇𝗒 𝖲𝗒𝗆𝖻𝗈𝗅 : ; & 𝖾𝗍𝖼]
