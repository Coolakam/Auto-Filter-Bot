import os
import random
import string
import asyncio
from time import time as time_now
from time import monotonic
import datetime

from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.ia_filterdb import db_count_documents, get_file_details, delete_files
from database.users_chats_db import db

from datetime import datetime, timedelta

from info import (
    OWNER_USERNAME, IS_PREMIUM, URL, INDEX_CHANNELS, ADMINS,
    IS_VERIFY, VERIFY_EXPIRE, SHORTLINK_API, SHORTLINK_URL,
    DELETE_TIME, SUPPORT_LINK, UPDATES_LINK, LOG_CHANNEL,
    PICS, REACTIONS, PM_FILE_DELETE_TIME
)

from utils import (
    is_premium, upload_image, get_settings, get_size,
    is_subscribed, is_check_admin, get_shortlink,
    get_verify_status, update_verify_status,
    save_group_settings, temp, get_readable_time,
    get_wish, get_seconds
)


@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):

    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if not await db.get_chat(message.chat.id):
            total = await client.get_chat_members_count(message.chat.id)
            username = f'@{message.chat.username}' if message.chat.username else 'Private'
            await client.send_message(LOG_CHANNEL, script.NEW_GROUP_TXT.format(
                message.chat.title, message.chat.id, username, total))
            await db.add_chat(message.chat.id, message.chat.title)

        wish = get_wish()
        user = message.from_user.mention if message.from_user else "Dear"

        btn = [[
            InlineKeyboardButton('⚡️ ᴜᴘᴅᴀᴛᴇs ⚡️', url=UPDATES_LINK),
            InlineKeyboardButton('💡 sᴜᴘᴘᴏʀᴛ 💡', url=SUPPORT_LINK)
        ]]

        await message.reply(
            text=f"<b>ʜᴇʏ {user}, <i>{wish}</i>\nʜᴏᴡ ᴄᴀɴ ɪ ʜᴇʟᴘ ʏᴏᴜ??</b>",
            reply_markup=InlineKeyboardMarkup(btn)
        )
        return

    try:
        await message.react(emoji=random.choice(REACTIONS), big=True)
    except:
        await message.react(emoji="⚡️", big=True)

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL,
            script.NEW_USER_TXT.format(message.from_user.mention, message.from_user.id)
        )

    verify_status = await get_verify_status(message.from_user.id)

    if verify_status['is_verified'] and datetime.now() > verify_status['expire_time']:
        await update_verify_status(message.from_user.id, is_verified=False)

    # Default start
    if len(message.command) == 1:
        buttons = [[
            InlineKeyboardButton("+ ᴀᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ +",
                url=f'http://t.me/{temp.U_NAME}?startgroup=start')
        ],[
            InlineKeyboardButton('ℹ️ ᴜᴘᴅᴀᴛᴇs', url=UPDATES_LINK),
            InlineKeyboardButton('🧑‍💻 sᴜᴘᴘᴏʀᴛ', url=SUPPORT_LINK)
        ]]

        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, get_wish()),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
        return

    mc = message.command[1]

    # Verify system (cleaned)
    verify_status = await get_verify_status(message.from_user.id)
    if IS_VERIFY and not verify_status['is_verified'] and not await is_premium(message.from_user.id, client):
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        await update_verify_status(message.from_user.id, verify_token=token, link=mc)

        link = await get_shortlink(
            SHORTLINK_URL,
            SHORTLINK_API,
            f'https://t.me/{temp.U_NAME}?start=verify_{token}'
        )

        btn = [[InlineKeyboardButton("🧿 Verify 🧿", url=link)]]

        await message.reply(
            "You not verified today! Kindly verify now. 🔐",
            reply_markup=InlineKeyboardMarkup(btn),
            protect_content=True
        )
        return

    # File handling
    type_, grp_id, file_id = mc.split("_", 2)

    files = await get_file_details(file_id)
    if not files:
        return await message.reply('No Such File Exist!')

    settings = await get_settings(int(grp_id))

    CAPTION = settings['caption']
    f_caption = CAPTION.format(
        file_name=files['file_name'],
        file_size=get_size(files['file_size']),
        file_caption=files['caption']
    )

    btn = [[
        InlineKeyboardButton('⚡️ ᴜᴘᴅᴀᴛᴇs', url=UPDATES_LINK),
        InlineKeyboardButton('💡 ꜱᴜᴘᴘᴏʀᴛ', url=SUPPORT_LINK)
    ],[
        InlineKeyboardButton('❌ ᴄʟᴏsᴇ ❌', callback_data='close_data')
    ]]

    vp = await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        reply_markup=InlineKeyboardMarkup(btn)
    )

    time_text = get_readable_time(PM_FILE_DELETE_TIME)

    msg = await vp.reply(
        f"⏳ This file will be deleted in {time_text}, save it somewhere else."
    )

    await asyncio.sleep(PM_FILE_DELETE_TIME)

    await msg.delete()
    await vp.delete()

    await message.reply("❌ File deleted. Request again if needed.")


@Client.on_message(filters.command('stats'))
async def stats(bot, message):
    if message.from_user.id not in ADMINS:
        return await message.delete()

    files = db_count_documents()
    users = await db.total_users_count()
    chats = await db.total_chat_count()
    prm = db.get_premium_count()

    used_files_db_size = get_size(await db.get_files_db_size())
    used_data_db_size = get_size(await db.get_data_db_size())

    uptime = get_readable_time(time_now() - temp.START_TIME)

    await message.reply_text(
        script.STATUS_TXT.format(
            users, prm, chats,
            used_data_db_size,
            files, used_files_db_size,
            "-", "-", uptime
        )
    )


@Client.on_message(filters.command('ping'))
async def ping(client, message):
    start = monotonic()
    msg = await message.reply("👀")
    end = monotonic()
    await msg.edit(f'{round((end - start) * 1000)} ms')
