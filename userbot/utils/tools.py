import re
import hashlib
import asyncio
import shlex
import os
from os.path import basename
import os.path
from html_telegraph_poster import TelegraphPoster
from PIL import Image
from yt_dlp import YoutubeDL
from typing import Optional, Union
from userbot import bot, LOGS, SUDO_USERS

from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator, DocumentAttributeFilename


async def md5(fname: str) -> str:
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def media_type(message):
    if message and message.photo:
        return "Photo"
    if message and message.audio:
        return "Audio"
    if message and message.voice:
        return "Voice"
    if message and message.video_note:
        return "Round Video"
    if message and message.gif:
        return "Gif"
    if message and message.sticker:
        return "Sticker"
    if message and message.video:
        return "Video"
    if message and message.document:
        return "Document"
    return None


def humanbytes(size: Union[int, float]) -> str:
    if size is None or isinstance(size, str):
        return ""

    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
    )
    return tmp[:-2]


def human_to_bytes(size: str) -> int:
    units = {
        "M": 2 ** 20,
        "MB": 2 ** 20,
        "G": 2 ** 30,
        "GB": 2 ** 30,
        "T": 2 ** 40,
        "TB": 2 ** 40,
    }

    size = size.upper()
    if not re.match(r" ", size):
        size = re.sub(r"([KMGT])", r" \1", size)
    number, unit = [string.strip() for string in size.split()]
    return int(float(number) * units[unit])


async def is_admin(chat_id, user_id):
    req_jo = await bot(GetParticipantRequest(
        channel=chat_id,
        user_id=user_id
    ))
    chat_participant = req_jo.participant
    if isinstance(
            chat_participant,
            ChannelParticipantCreator) or isinstance(
            chat_participant,
            ChannelParticipantAdmin):
        return True
    return False


async def runcmd(cmd: str) -> tuple[str, str, int, int]:
    """ run command in terminal """
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(*args,
                                                   stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return (stdout.decode('utf-8', 'replace').strip(),
            stderr.decode('utf-8', 'replace').strip(),
            process.returncode,
            process.pid)


async def take_screen_shot(video_file: str, duration: int, path: str = '') -> Optional[str]:
    """ take a screenshot """
    LOGS.info(
        '[[[Extracting a frame from %s ||| Video duration => %s]]]',
        video_file,
        duration)
    ttl = duration // 2
    thumb_image_path = path or os.path.join(
        "./temp/", f"{basename(video_file)}.jpg")
    command = f"ffmpeg -ss {ttl} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await runcmd(command))[1]
    if err:
        LOGS.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None


async def check_media(reply_message):
    if reply_message and reply_message.media:
        if reply_message.photo:
            data = reply_message.photo
        elif reply_message.document:
            if (
                DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
                in reply_message.media.document.attributes
            ):
                return False
            if (
                reply_message.gif
                or reply_message.video
                or reply_message.audio
                or reply_message.voice
            ):
                return False
            data = reply_message.media.document
        else:
            return False
    else:
        return False

    if not data or data is None:
        return False
    else:
        return data


async def run_cmd(cmd: list) -> tuple[bytes, bytes]:
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await process.communicate()
    t_resp = out.strip()
    e_resp = err.strip()
    return t_resp, e_resp


async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


def post_to_telegraph(title, html_format_content):
    post_client = TelegraphPoster(use_api=True)
    auth_name = "Kayzu-Ubot"
    auth_url = "https://github.com/Kayzyu/Kayzu-Ubot"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=title,
        author=auth_name,
        author_url=auth_url,
        text=html_format_content,
    )
    return post_page["url"]


async def reply_id(event):
    reply_to_id = None
    if event.sender_id in SUDO_USERS:
        reply_to_id = event.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    return reply_to_id


async def edit_or_reply(
    event,
    text,
    parse_mode=None,
    link_preview=None,
    file_name=None,
    aslink=False,
    deflink=False,
    noformat=False,
    linktext=None,
    caption=None,
):
    link_preview = link_preview or False
    reply_to = await event.get_reply_message()
    if len(text) < 4096 and not deflink:
        parse_mode = parse_mode or "md"
        if not event.out and event.sender_id:
            if reply_to:
                return await reply_to.reply(
                    text, parse_mode=parse_mode, link_preview=link_preview
                )
            return await event.reply(
                text, parse_mode=parse_mode, link_preview=link_preview
            )
        await event.edit(text, parse_mode=parse_mode, link_preview=link_preview)
        return event
    if not noformat:
        text = md_to_text(text)
    if aslink or deflink:
        linktext = linktext or "**Pesan Terlalu Panjang**"
        response = await paste_message(text, pastetype="s")
        text = linktext + f" [Lihat Disini]({response})"
        if not event.out and event.sender_id:
            if reply_to:
                return await reply_to.reply(text, link_preview=link_preview)
            return await event.reply(text, link_preview=link_preview)
        await event.edit(text, link_preview=link_preview)
        return event
    file_name = file_name or "output.txt"
    caption = caption or None
    with open(file_name, "w+") as output:
        output.write(text)
    if reply_to:
        await reply_to.reply(caption, file=file_name)
        await event.delete()
        return os.remove(file_name)
    if not event.out and event.sender_id:
        await event.reply(caption, file=file_name)
        await event.delete()
        return os.remove(file_name)
    await event.client.send_file(event.chat_id, file_name, caption=caption)
    await event.delete()
    os.remove(file_name)


async def edit_delete(event, text, time=None, parse_mode=None, link_preview=None):
    parse_mode = parse_mode or "md"
    link_preview = link_preview or False
    time = time or 15
    if not event.out and event.sender_id:
        reply_to = await event.get_reply_message()
        newevent = (
            await reply_to.reply(text, link_preview=link_preview, parse_mode=parse_mode)
            if reply_to
            else await event.reply(
                text, link_preview=link_preview, parse_mode=parse_mode
            )
        )
    else:
        newevent = await event.edit(
            text, link_preview=link_preview, parse_mode=parse_mode
        )
    await asyncio.sleep(time)
    return await newevent.delete()


eod = edit_delete


async def media_to_pic(event, reply):
    mediatype = media_type(reply)
    if mediatype not in ["Photo", "Round Video", "Gif", "Sticker", "Video"]:
        await edit_delete(
            event,
            "**Saya tidak dapat mengekstrak gambar untuk memproses lebih lanjut ke media yang tepat**",
        )
        return None
    media = await reply.download_media(file="./temp")
    event = await edit_or_reply(event, "`Transfiguration Time! Converting....`")
    file = os.path.join("./temp/", "meme.png")
    if mediatype == "Sticker":
        if media.endswith(".tgs"):
            await runcmd(
                f"lottie_convert.py --frame 0 -if lottie -of png '{media}' '{file}'"
            )
        elif media.endswith(".webp"):
            im = Image.open(media)
            im.save(file)
    elif mediatype in ["Round Video", "Video", "Gif"]:
        extractMetadata(createParser(media))
        await runcmd(f"rm -rf '{file}'")
        await take_screen_shot(media, 0, file)
        if not os.path.exists(file):
            await edit_delete(
                event,
                f"**Maaf. Saya tidak dapat mengekstrak gambar dari ini {mediatype}**",
            )
            return None
    else:
        im = Image.open(media)
        im.save(file)
    await runcmd(f"rm -rf '{media}'")
    return [event, file, mediatype]

ydl_opts = {
    "format": "bestaudio[ext=m4a]",
    "geo-bypass": True,
    "noprogress": True,
    "user-agent": "Mozilla/5.0 (Linux; Android 7.0; k960n_mt6580_32_n) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
    "extractor-args": "youtube:player_client=all",
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


def download_lagu(url: str) -> str:
    info = ydl.extract_info(url, download=False)
    ydl.download([url])
    return os.path.join("downloads", f"{info['id']}.{info['ext']}")
