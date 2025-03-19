import os
from PyroUbot import *
import requests

__MODULE__ = "ʙʀᴀᴛ"
__HELP__ = """
📚 <b>--Folder Untuk Brat--</b>

<blockquote><b>🚦 Perintah : <code>{0}brat</code>
🦠 Penjelasan : Untuk Membuat Gambar Text Seperti Tren Tiktok</b></blockquote>
"""

def get_brat_image(text):
    url = "https://api.botcahx.eu.org/api/maker/brat"
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
        
@WANN.UBOT("brat")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("Gunakan perintah /brat <teks> untuk membuat gambar.")
        return

    request_text = args[1]
    await message.reply_text("Sedang memproses, mohon tunggu...")

    image_content = get_brat_image(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("Gagal membuat gambar. Coba lagi nanti.")
