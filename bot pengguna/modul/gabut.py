from platform import uname
from userbot import ALIVE_NAME, CMD_HELP
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern="^.lrh1(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`𝐀𝐍𝐉𝐀𝐘 𝐋𝐔𝐑𝐀𝐇 𝐌𝐄𝐍𝐀𝐍𝐆🐣`")
# Salam


@register(outgoing=True, pattern="^.lrhh(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`𝐃𝐈𝐌𝐀𝐍𝐀 𝐀𝐃𝐀 𝐁𝐀𝐍𝐒𝐎𝐒.....𝐃𝐈 𝐒𝐈𝐓𝐔 𝐀𝐃𝐀 𝐋𝐔𝐑𝐀𝐇🐣`")
# Menjawab Salam


@register(outgoing=True, pattern="^.lrh(?: |$)(.*)")
async def perkenalan(event):
    event.pattern_match.group(1)
    await event.edit("`𝐀𝐍𝐉𝐀𝐘 𝐀𝐃𝐀 𝐁𝐀𝐍𝐒𝐎𝐒,𝐋𝐔𝐑𝐀𝐇 𝐆𝐈𝐊𝐄𝐒 𝐃𝐔𝐋𝐔🐣.....`")
# Istigfar


@register(outgoing=True, pattern="^.lrh2(?: |$)(.*)")
async def perkenalan(event):
    event.pattern_match.group(1)
    await event.edit(f"`𝐀𝐍𝐉𝐀𝐘 𝐋𝐔𝐑𝐀𝐇 𝐂𝐀𝐊𝐄𝐏🐣`")
    sleep(2)
    await event.edit(f"`𝙂𝙬 𝙏𝙞𝙣𝙜𝙜𝙖𝙡 𝘿𝙞 {WEATHER_DEFCITY}`")
    sleep(2)
    await event.edit("`𝙎𝙖𝙡𝙖𝙢 𝙆𝙚𝙣𝙖𝙡...`")
    sleep(2)
    await event.edit("`𝙐𝙙𝙖𝙝 𝙂𝙞𝙩𝙪 𝘼𝙟𝙖 :𝙫`")
# Perkenalan


CMD_HELP.update({
    "gabut": "**Modules** - `Gabut`\
    \n\n Cmd : `.lrh`\
    \nUsage : Lurah Gikes\
    \n\n Cmd : `.lrh2`\
    \nUsage : Memperkenalkan Diri\
    \n\n Cmd : `.lrhh`\
    \nUsage : bansos."
})
