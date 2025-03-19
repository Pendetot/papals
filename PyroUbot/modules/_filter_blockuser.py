from PyroUbot import *
from PyroUbot.core.database.block import *

@WANN.NO_CMD_UBOT("BLOCK", bot)
async def check_blocked_global(client, message):
    user_id = message.from_user.id
    
    if await is_user_blocked(user_id):
        await message.reply_text("Anda telah diblokir dari bot ini.")
        return

@WANN.CALLBACK("block")
async def handle_block_callback(client, callback_query):
    user_id = callback_query.from_user.id
    target_user_id = int(callback_query.data.split()[1]) 

    if await is_user_blocked(target_user_id):
        await callback_query.answer("Pengguna Sudah Ada Di Dalam Database ✅", show_alert=True)
    else:
        await block_user(target_user_id)
        await callback_query.answer("Pengguna Berhasil Di Blokir ✅", show_alert=True)
    
@WANN.BOT("block")
async def block(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Gunakan perintah: `/block <user_id>`")
        return

    try:
        user_id = int(message.command[1])
        await block_user(user_id)
        await message.reply_text(f"Pengguna dengan ID `{user_id}` telah diblokir.")
    except ValueError:
        await message.reply_text("ID pengguna tidak valid.")

@WANN.BOT("unblock")
async def unblock(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Gunakan perintah: `/unblock <user_id>`")
        return

    try:
        user_id = int(message.command[1])
        await unblock_user(user_id)
        await message.reply_text(f"Pengguna dengan ID `{user_id}` telah dihapus dari daftar blokir.")
    except ValueError:
        await message.reply_text("ID pengguna tidak valid.")
