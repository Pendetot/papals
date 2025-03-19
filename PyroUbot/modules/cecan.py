from PyroUbot import *
import random
import requests
from pyrogram.enums import *
from pyrogram import *
from pyrogram.types import *
from io import BytesIO

__MODULE__ = "ᴄᴇᴄᴀɴ"
__HELP__ = """
📚 <b>--Folder Untuk Cecan--</b>

<blockquote><b>🚦 Perintah : <code>{0}cecan [query]</code>
🦠 Penjelasan : Mengirim Foto Random Sesuai Query.</b></blockquote>
<blockquote><b>📖 Penggunaan : 
 Query: 
    Indonesia,
    china,
    thailand,
    vietnam,
    waifu,
    malaysia,
    japan,
    korea</b></blockquote>
"""

URLS = {
    "indonesia": f"https://api.botcahx.eu.org/api/cecan/indonesia?apikey={API_KEY}",
    "china": f"https://api.botcahx.eu.org/api/cecan/china?apikey={API_KEY}",
    "thailand": f"https://api.botcahx.eu.org/api/cecan/thailand?apikey={API_KEY}",
    "vietnam": f"https://api.botcahx.eu.org/api/cecan/vietnam?apikey={API_KEY}",
    "waifu": f"https://api.botcahx.eu.org/api/anime/waifu?apikey={API_KEY}",
    "malaysia": f"https://api.botcahx.eu.org/api/cecan/malaysia?apikey={API_KEY}",
    "japan": f"https://api.botcahx.eu.org/api/cecan/japan?apikey={API_KEY}",
    "korea": f"https://api.botcahx.eu.org/api/cecan/korea?apikey={API_KEY}"
}

@WANN.UBOT("cecan")
@WANN.TOP_CMD
async def _(client, message):
    # Extract query from message
    query = message.text.split()[1] if len(message.text.split()) > 1 else None
    
    if query not in URLS:
        valid_queries = ", ".join(URLS.keys())
        await message.reply(f"Query tidak valid. Gunakan salah satu dari: {valid_queries}.")
        return

    processing_msg = await message.reply("Processing...")
    
    try:
        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        response = requests.get(URLS[query])
        response.raise_for_status()
        
        photo = BytesIO(response.content)
        photo.name = 'image.jpg'
        
        await client.send_photo(message.chat.id, photo)
        await processing_msg.delete()
    except requests.exceptions.RequestException as e:
        await processing_msg.edit_text(f"Gagal mengambil gambar cecan Error: {e}")
