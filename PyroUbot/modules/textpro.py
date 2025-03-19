import os
from PyroUbot import *
import requests

__MODULE__ = "ᴛᴇxᴛᴘʀᴏ"
__HELP__ = """
📚 <b>--Folder Untuk TextPro--</b>

<blockquote><b>🚦 Perintah : <code>{0}giraffe</code>
🦠 Penjelasan : Untuk Membuat Gambar Ada Text ( test aja ).</b></blockquote>
<blockquote><b>🚦 Perintah : <code>{0}magma</code>
🦠 Penjelasan : Untuk Membuat Gambar Ada Text ( test aja ).</b></blockquote>
<blockquote><b>🚦 Perintah : <code>{0}3dstone</code>
🦠 Penjelasan : Untuk Membuat Gambar Ada Text ( test aja ).</b></blockquote>
<blockquote><b>🚦 Perintah : <code>{0}hallowen</code>
🦠 Penjelasan : Untuk Membuat Gambar Ada Text ( test aja ).</b></blockquote>
<blockquote><b>🚦 Perintah : <code>{0}blood</code>
🦠 Penjelasan : Untuk Membuat Gambar Ada Text ( test aja ).</b></blockquote>
"""

def get_giraffe_image(text):
    url = "https://api.botcahx.eu.org/api/textpro/giraffe"
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

def get_magma_image(text):
    url = "https://api.botcahx.eu.org/api/textpro/magma"
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

def get_3dstone_image(text):
    url = "https://api.botcahx.eu.org/api/textpro/3dstone"
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

def get_hallowen_image(text):
    url = "https://api.botcahx.eu.org/api/textpro/hallowen"
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
 
def get_blood_image(text):
    url = "https://api.botcahx.eu.org/api/textpro/blood"
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
                                                       
@WANN.UBOT("giraffe")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("<b><i>Gunakan perintah /giraffe <teks> untuk membuat gambar</i></b>.")
        return

    request_text = args[1]
    await message.reply_text("<b><i>Sedang memproses, mohon tunggu</i></b>...")

    image_content = get_giraffe_image(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("Gagal membuat gambar. Coba lagi nanti.")

@WANN.UBOT("magma")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("<b><i>Gunakan perintah /magma <teks> untuk membuat gambar.</i></b>")
        return

    request_text = args[1]
    await message.reply_text("<b><i>Sedang memproses, mohon tunggu...</i></b>")

    image_content = get_magma_image(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("Gagal membuat gambar. Coba lagi nanti.")       

@WANN.UBOT("3dstone")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("<b><i>Gunakan perintah /3dstone <teks> untuk membuat gambar.</i></b>")
        return

    request_text = args[1]
    await message.reply_text("<b><i>Sedang memproses, mohon tunggu...</i></b>")

    image_content = get_3dstone_image(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("Gagal membuat gambar. Coba lagi nanti.")       

@WANN.UBOT("hallowen")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("<b><i>Gunakan perintah /hallowen <teks> untuk membuat gambar.</i></b>")
        return

    request_text = args[1]
    await message.reply_text("<b><i>Sedang memproses, mohon tunggu...</i></b>")

    image_content = get_hallowen_image(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("Gagal membuat gambar. Coba lagi nanti.")

@WANN.UBOT("blood")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("<b><i>Gunakan perintah /blood <teks> untuk membuat gambar.</i></b>")
        return

    request_text = args[1]
    await message.reply_text("<b><i>Sedang memproses, mohon tunggu...</i></b>")

    image_content = get_blood_image(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("Gagal membuat gambar. Coba lagi nanti.")
