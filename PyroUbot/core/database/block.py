from PyroUbot.core.database import mongodb

blockuser = mongodb["wannfyy"]["block"]

async def block_user(user_id: int):
    await blockuser.insert_one({"_id": user_id})

async def unblock_user(user_id: int):
    await blockuser.delete_one({"_id": user_id})

async def is_user_blocked(user_id: int) -> bool:
    return await blockuser.find_one({"_id": user_id}) is not None
