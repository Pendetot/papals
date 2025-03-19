import os
from PyroUbot import *
import requests

__MODULE__ = "ᴇᴘʜᴏᴛᴏ"
__HELP__ = """
📚 <b>--Folder Untuk Ephoto--</b>

<blockquote><b>🚦 Perintah : <code>{0}ytsilverbutton</code>
🦠 Penjelasan : Untuk Membuat Gambar YT SILVER BUTTON Pake Namamu.</b></blockquote>
<blockquote><b>🚦 Perintah : <code>{0}ytgoldbutton</code>
🦠 Penjelasan : Untuk Membuat Gambar YT GOLD BUTTON Pake Namamu.</b></blockquote>
"""

def get_ytsilverbutton_image(text):
    url = "https://api.botcahx.eu.org/api/ephoto/ytsilverbutton"
    params = {
        "text": text,
        "apikey": f"{API_KEY}"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        if response.headers.get("Content-Type", "").startswith("image/"):
            return response.content
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def get_ytgoldbutton_image(text):
    url = "https://api.botcahx.eu.org/api/ephoto/ytgoldbutton"
    params = {
        "text": text,
        "apikey": f"{API_KEY}"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        if response.headers.get("Content-Type", "").startswith("image/"):
            return response.content
        else:
            return None
    except requests.exceptions.RequestException:
        return None

@WANN.UBOT("ytsilverbutton")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("Gunakan perintah /ytsilverbutton <teks> untuk membuat gambar.")
        return

    request_text = args[1]
    await message.reply_text("Sedang memproses, mohon tunggu...")

    image_content = get_ytsilverbutton_image(request_text)
    if image_content:
        temp_file = "ytsilverbutton.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("Gagal membuat gambar. Coba lagi nanti.")

@WANN.UBOT("ytgoldbutton")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("Gunakan perintah /ytgoldbutton <teks> untuk membuat gambar.")
        return

    request_text = args[1]
    await message.reply_text("Sedang memproses, mohon tunggu...")

    image_content = get_ytgoldbutton_image(request_text)
    if image_content:
        temp_file = "ytgoldbutton.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("Gagal membuat gambar. Coba lagi nanti.")
        
        
