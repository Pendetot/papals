import os
from PyroUbot import *
import requests

__MODULE__ = "flux ai"
__HELP__ = """
📚 <b>--Folder Untuk Flux Ai--</b>

<blockquote><b>🚦 Perintah : <code>{0}fluxai</code>
🦠 Penjelasan : Untuk Membuat Gambar Text To Img</b></blockquote>
"""

def fluxai(text):
    url = f"https://api.siputzx.my.id/api/ai/flux"
    params = {
        "prompt": text,
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
        
@WANN.UBOT("fluxai|flux")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("Gunakan perintah /fluxai <teks> untuk membuat Txt2Img.")
        return

    request_text = args[1]
    await message.reply_text("Sedang memproses, mohon tunggu...")

    image_content = fluxai(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("Gagal membuat gambar. Coba lagi nanti.")
