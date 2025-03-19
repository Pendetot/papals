import aiohttp
import filetype
import requests
from io import BytesIO
from PyroUbot import *

__MODULE__ = "ʀᴇᴍɪɴɪ"
__HELP__ = """
<blockquote><b>『 ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ʀᴇᴍɪɴɪ 』</b>

  <b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}remini</code> [ʀᴇᴘʟʏ ᴛᴏ ᴘʜᴏᴛᴏ]
  <b>• ᴘᴇɴᴊᴇʟᴀsᴀɴ:</b> ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴅ/ʜᴀʟᴜsᴋᴀɴ ɢᴀᴍʙᴀʀ</blockquote>
"""

async def upload_media(message):
    media = await message.reply_to_message.download()
    url = "https://itzpire.com/tools/upload"

    async with aiohttp.ClientSession() as session:
        with open(media, "rb") as file:
            files = {"file": file}
            async with session.post(url, data=files) as response:
                if response.status == 200:
                    data = await response.json()
                    link = data["fileInfo"]["url"]
                    return link
                else:
                    return f"Error: {response.status}, {await response.text()}"

@WANN.UBOT("remini|hd")
async def _(client, message):
    try:
        if not message.reply_to_message:
            return await message.reply("Silakan balas gambar yang ingin dihaluskan.")
        
        reply_message = message.reply_to_message
        xx = await message.reply("<b>Proses sedang dilakukan, mohon tunggu...</b>")
        
        foto = await upload_media(message)
        if not foto:
            await xx.edit("<b>Penggunaan salah, mohon reply foto.</b>")
            return
        
        api_url = f'https://api.botcahx.eu.org/api/tools/remini?url={foto}&apikey={API_KEY}'
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as api_response:
                if api_response.status != 200:
                    await xx.edit(f"Failed to fetch image: HTTP {api_response.status}")
                    return
                
                image = await api_response.json()
                url = image.get("url")
                if url:
                    await client.send_photo(message.chat.id, url, caption='<b>Berhasil Di Haluskan</b>')
                    await xx.delete()
                else:
                    await xx.edit('Image URL not found in the response.')
    
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
