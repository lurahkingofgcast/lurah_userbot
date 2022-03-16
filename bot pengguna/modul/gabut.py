from platform import uname
from userbot import ALIVE_NAME, CMD_HELP
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern="^.lrh(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("𝐀𝐍𝐉𝐀𝐘 𝐋𝐔𝐑𝐀𝐇 𝐂𝐀𝐊𝐄𝐏🐣")
# lurah


@register(outgoing=True, pattern="^.lrh1(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("𝐃𝐈𝐌𝐀𝐍𝐀 𝐀𝐃𝐀 𝐁𝐀𝐍𝐒𝐎𝐒.....𝐃𝐈 𝐒𝐈𝐓𝐔 𝐀𝐃𝐀 𝐋𝐔𝐑𝐀𝐇🐣")
# lurah1


@register(outgoing=True, pattern="^.lrh2(?: |$)(.*)")
async def perkenalan(event):
    event.pattern_match.group(1)
    await event.edit("𝐀𝐍𝐉𝐀𝐘 𝐋𝐔𝐑𝐀𝐇 𝐌𝐄𝐍𝐀𝐍𝐆🐣")
# lrh2


@register(outgoing=True, pattern="^.lrh3(?: |$)(.*)")
async def perkenalan(event):
    event.pattern_match.group(1)
    await event.edit(f"𝐀𝐍𝐉𝐀𝐘 𝐀𝐃𝐀 𝐁𝐀𝐍𝐒𝐎𝐒,𝐋𝐔𝐑𝐀𝐇 𝐆𝐈𝐊𝐄𝐒 𝐃𝐔𝐋𝐔🐣.....")
# lrh3


@register(outgoing=True, pattern="^.lrh4(?: |$)(.*)")
async def perkenalan(event):
    event.pattern_match.group(1)
    await event.edit(f"𝗜𝗡𝗜 𝗔𝗗𝗔𝗟𝗔𝗛 𝗟𝗨𝗥𝗔𝗛 𝗥𝗔𝗝𝗔 𝗠𝗘𝗞𝗦𝗜𝗞𝗢 𝗘𝗟 𝗠𝗔𝗧𝗔𝗗𝗢𝗥𝗘 𝗦𝗔𝗟𝗩𝗔𝗗𝗢𝗥𝗘 𝗧𝗘𝗤𝗨𝗜𝗟𝗔 𝗘𝗟 𝗞𝗢𝗡𝗧𝗢𝗟𝗘🐣")


CMD_HELP.update({
    "gabut": "Modules - Gabut\
    \n\n Cmd : .lrh\
    \nUsage : Untuk Menjawab Salam\
    \n\n Cmd : .lrh1\
    \nUsage : Memperkenalkan Diri\
    \n\n Cmd : .lrh2\
    \nUsage : Untuk Memberi Salam."
    \n\n Cmd : .lrh3\
    \nUsage : Salam."
    \n\n Cmd : .lrh4\
    \nUsage : bansos."
})
