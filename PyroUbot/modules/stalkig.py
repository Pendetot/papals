import requests
import wget
import os
from pyrogram import Client
from PyroUbot import *

__MODULE__ = "ꜱᴛᴀʟᴋɪɢ"
__HELP__ = """
<blockquote><b>『 ꜱᴛᴀʟᴋɪɢ 』</b>

  <b>➢ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}stalkig</code> 
   <i>penjelasan:</b> untuk stalking instagram menggunakan username</i></blockquote>
"""

@WANN.UBOT("stalkig")
async def stalkig(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    
    jalan = await message.reply(f"{prs} Processing...")
    
    if len(message.command) != 2:
        return await jalan.edit(f"{ggl} Please use the command `stalkig` followed by the Instagram username.")
    
    username = message.command[1]
    chat_id = message.chat.id
    url = f"https://api.botcahx.eu.org/api/stalk/ig?username={username}&apikey={API_KEY}"
    
    try:
        response = requests.get(url)
        
        # Ensure we received a successful response
        if response.status_code == 200:
            data = response.json()
            
            # Check if the 'status' is True and 'code' is 200
            if data.get('status') == True and data.get('code') == 200:
                hasil = data.get('result', {})
                username = hasil.get('username', 'N/A')
                fullName = hasil.get('fullName', 'N/A')
                followers = hasil.get('followers', 'N/A')
                following = hasil.get('following', 'N/A')
                postsCount = hasil.get('postsCount', 'N/A')
                photoUrl = hasil.get('photoUrl', '')
                bio = hasil.get('bio', 'N/A')
                
                # Format the message
                caption = f"""
<b><emoji id=5841235769728962577>⭐</emoji>Username: <code>{username}</code></b>
<b><emoji id=5843952899184398024>⭐</emoji>Full Name: <code>{fullName}</code></b>
<b><emoji id=5841243255856960314>⭐</emoji>Followers: <code>{followers}</code></b>
<b><emoji id=5352566966454330504>⭐</emoji>Following: <code>{following}</code></b>
<b><emoji id=5841243255856960314>⭐</emoji>Posts: <code>{postsCount}</code></b>
<b><emoji id=5353036831581544549>⭐</emoji>Bio: <code>{bio}</code></b>
"""
                # Download the photo and send
                if photoUrl:
                    photo_path = wget.download(photoUrl)
                    await client.send_photo(chat_id, caption=caption, photo=photo_path)
                    if os.path.exists(photo_path):
                        os.remove(photo_path)
                else:
                    await client.send_message(chat_id, caption)
            
            else:
                # If the status or code is not as expected
                await jalan.edit(f"{ggl} Invalid API response. Status: {data.get('status')}, Code: {data.get('code')}")
        else:
            # Handle non-200 status code
            await jalan.edit(f"{ggl} Request failed with status code {response.status_code}.")
    
    except requests.exceptions.RequestException as e:
        await jalan.edit(f"{ggl} Request failed: {e}")
    
    except Exception as e:
        await jalan.edit(f"{ggl} An error occurred: {e}")
