import random
from PyroUbot import *

__MODULE__ = "bokep"
__HELP__ = """
📚 <b>--Folder Untuk Bokep--</b>

<blockquote><b>🚦 Perintah : <code>{0}bokep</code>
🦠 Penjelasan : Untuk Melihat Vidio 18+.</b></blockquote>
"""

@WANN.UBOT("bokep")
async def video_bokep(client, message):
    y = await message.reply_text("**mencari video bokep**...")
    try:
        await client.join_chat("https://t.me/+kJJqN5kUQbs1NTVl")
    except:
        pass
    try:
        bokepnya = []
        async for bokep in client.search_messages(
            -1001867672427, filter=MessagesFilter.VIDEO
        ):
            bokepnya.append(bokep)
        video = random.choice(bokepnya)
        await video.copy(message.chat.id, reply_to_message_id=message.id)
        await y.delete()
    except Exception as error:
        await y.edit(error)
    if client.me.id == OWNER_ID:
        return
    await client.leave_chat(-1001867672427)
