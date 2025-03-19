import asyncio
from datetime import datetime

from pyrogram.types import InlineKeyboardMarkup
from pytz import timezone

from PyroUbot import *

async def expiredUserbots():
    while True:
        for X in ubot._ubot:
            time = datetime.now(timezone("Asia/Jakarta")).strftime("%d-%m-%Y")
            exp_date = await get_expired_date(X.me.id)
            
            if exp_date is None:
                continue

            exp = exp_date.strftime("%d-%m-%Y")

            if time == exp:
                await X.unblock_user(bot.me.username)
                await remove_ubot(X.me.id)
                await remove_all_vars(X.me.id)
                await rem_expired_date(X.me.id)
                ubot._get_my_id.remove(X.me.id)
                ubot._ubot.remove(X)
                await X.log_out()
                await bot.send_message(
                    X.me.id,
                    MSG.EXP_MSG_UBOT(X),
                    reply_markup=InlineKeyboardMarkup(BTN.EXP_UBOT()),
                )

        await asyncio.sleep(60) 
