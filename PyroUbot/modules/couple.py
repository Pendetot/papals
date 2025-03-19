import requests
from pyrogram import *
from PyroUbot import *
from pyrogram.types import *
import wget
import os
import glob

__MODULE__ = "ᴄᴏᴜᴘʟᴇ"
__HELP__ = """
📚 <b>--Folder Untuk Coople--</b>

<blockquote><b>🚦 Perintah : <code>{0}couple</code> ᴊᴜᴍʟᴀʜ/ᴋᴀᴛᴀ_ᴋᴜɴᴄɪ
🦠 Penjelasan : Untuk Mencari Photo Couple Secara Random.</b></blockquote>
"""

@WANN.UBOT("couple")
async def pinterest(client, message):
    prs = await EMO.PROSES(client)
    err = await EMO.GAGAL(client)
    jalan = await message.reply(f"{prs}<b>ᴘʀᴏᴄᴇssɪɴɢ...</b>")
    chat_id = message.chat.id
    url = f"https://api.botcahx.eu.org/api/randomgambar/couplepp?apikey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        male_url = data['male']
        female_url = data['female']

        # Download images using wget
        male_image_filename = wget.download(male_url, out="male.jpg")
        female_image_filename = wget.download(female_url, out="female.jpg")

        # Prepare media group
        media_group = [
            InputMediaPhoto(media=male_image_filename),
            InputMediaPhoto(media=female_image_filename)
        ]

        # Send media group
        janda = await client.send_media_group(chat_id, media_group)
        if janda:
            await jalan.delete()
        # Clean up downloaded files
        os.remove(male_image_filename)
        os.remove(female_image_filename)
    else:
        await message.reply(f"Request failed with status code {response.status_code}")
