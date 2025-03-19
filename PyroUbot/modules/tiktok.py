import asyncio
import requests
import os
from pyrogram.raw.functions.messages import DeleteHistory
import aiohttp
from PyroUbot import *

__MODULE__ = "ᴛɪᴋᴛᴏᴋ"
__HELP__ = """
<blockquote> <b>Bantuan Untuk Tiktok</b>

• <b>Perintah</b> : <code>{0}tt</code> -v atau -m <b>[link nya]</b>
• <b>Penjelasan : Download Vt No Vm, -v untuk video -m untuk musik.</b></blockquote>

"""

async def download_file(url, path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(path, 'wb') as f:
                    f.write(await response.read())
            else:
                print(f"Failed to download file: {response.status}")

async def downloader_tiktok(client, message, perintah,tujuan):
    url = f"https://api.botcahx.eu.org/api/dowloader/tiktok?url={tujuan}&apikey={API_KEY}"
    headers = {"accept": "application/json"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        if data['status'] == True:
            if perintah == "-v":
                video_url = data['result']['video'][0]
                video_path = "video.mp4"
                await download_file(video_url, video_path)
                await client.send_video(message.chat.id, video_path, caption=f"Download by: {client.me.mention}")
                os.remove(video_path)
            elif perintah == "-m":
                music_url = data['result']['audio'][0]
                music_path = "music.mp3"
                await download_file(music_url, music_path)
                await client.send_audio(message.chat.id, music_path, caption=f"<b>Download by: {client.me.mention}</b>")
                os.remove(music_path)
            else:
                return await message.reply("Gunakan format -v atau -m.")
        else:
            print("Failed to fetch download URLs.")
    else:
        print(f"Request failed with status code {res.status_code}")

@WANN.UBOT("tt")
async def _(client, message):
    if len(message.command) < 3:
        return await message.reply(
            f"<code>{message.text.split()[0]}</code> use -v for video or use -m for audio")
    command, isi = message.command[:2]
    link = " ".join(message.command[2:])
    return await downloader_tiktok(client, message, isi, link)
