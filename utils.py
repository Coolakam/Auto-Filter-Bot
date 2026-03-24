from pyrogram.errors import UserNotParticipant, FloodWait
from info import ADMINS, IS_PREMIUM, TIME_ZONE
import asyncio
from pyrogram.types import InlineKeyboardButton
from pyrogram import enums
from datetime import datetime
from database.users_chats_db import db
from shortzy import Shortzy
import pytz


class temp(object):
    START_TIME = 0
    BANNED_USERS = []
    BANNED_CHATS = []
    ME = None
    CANCEL = False
    U_NAME = None
    B_NAME = None
    SETTINGS = {}
    VERIFICATIONS = {}
    FILES = {}
    USERS_CANCEL = False
    GROUPS_CANCEL = False
    BOT = None
    PREMIUM = {}


async def is_subscribed(bot, query):
    btn = []

    if await is_premium(query.from_user.id, bot):
        return btn

    stg = db.get_bot_sttgs()
    if not stg or not stg.get('FORCE_SUB_CHANNELS'):
        return btn

    for id in stg.get('FORCE_SUB_CHANNELS').split(' '):
        chat = await bot.get_chat(int(id))
        try:
            await bot.get_chat_member(int(id), query.from_user.id)
        except UserNotParticipant:
            btn.append(
                [InlineKeyboardButton(f'Join : {chat.title}', url=chat.invite_link)]
            )

    if stg and stg.get('REQUEST_FORCE_SUB_CHANNELS') and not db.find_join_req(query.from_user.id):
        id = stg.get('REQUEST_FORCE_SUB_CHANNELS')
        chat = await bot.get_chat(int(id))
        try:
            await bot.get_chat_member(int(id), query.from_user.id)
        except UserNotParticipant:
            url = await bot.create_chat_invite_link(int(id), creates_join_request=True)
            btn.append(
                [InlineKeyboardButton(f'Request : {chat.title}', url=url.invite_link)]
            )

    return btn


def list_to_str(k):
    if not k:
        return "N/A"
    elif len(k) == 1:
        return str(k[0])
    else:
        return ", ".join(str(i) for i in k)


async def is_check_admin(bot, chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in [
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.OWNER
        ]
    except:
        return False


async def get_verify_status(user_id):
    verify = temp.VERIFICATIONS.get(user_id)
    if not verify:
        verify = await db.get_verify_status(user_id)
        temp.VERIFICATIONS[user_id] = verify
    return verify


async def update_verify_status(user_id, verify_token="", is_verified=False, link="", expire_time=0):
    current = await get_verify_status(user_id)
    current['verify_token'] = verify_token
    current['is_verified'] = is_verified
    current['link'] = link
    current['expire_time'] = expire_time

    temp.VERIFICATIONS[user_id] = current
    await db.update_verify_status(user_id, current)


async def is_premium(user_id, bot):
    if not IS_PREMIUM:
        return True

    if user_id in ADMINS:
        return True

    mp = db.get_plan(user_id)

    if mp['premium']:
        if mp['expire'] < datetime.now():
            await bot.send_message(
                user_id,
                f"Your premium {mp['plan']} plan expired on {mp['expire'].strftime('%Y.%m.%d %H:%M:%S')}, use /plan to activate again"
            )
            mp['expire'] = ''
            mp['plan'] = ''
            mp['premium'] = False
            db.update_plan(user_id, mp)
            return False
        return True

    return False


async def check_premium(bot):
    while True:
        pr = [i for i in db.get_premium_users() if i['status']['premium']]

        for p in pr:
            mp = p['status']
            if mp['expire'] < datetime.now():
                try:
                    await bot.send_message(
                        p['id'],
                        f"Your premium {mp['plan']} plan expired on {mp['expire'].strftime('%Y.%m.%d %H:%M:%S')}"
                    )
                except Exception:
                    pass

                mp['expire'] = ''
                mp['plan'] = ''
                mp['premium'] = False
                db.update_plan(p['id'], mp)

        await asyncio.sleep(1200)


async def broadcast_messages(user_id, message, pin):
    try:
        m = await message.copy(chat_id=user_id)
        if pin:
            await m.pin(both_sides=True)
        return "Success"

    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message, pin)

    except Exception:
        await db.delete_user(int(user_id))
        return "Error"


async def groups_broadcast_messages(chat_id, message, pin):
    try:
        k = await message.copy(chat_id=chat_id)

        if pin:
            try:
                await k.pin()
            except:
                pass

        return "Success"

    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await groups_broadcast_messages(chat_id, message, pin)

    except Exception:
        await db.delete_chat(chat_id)
        return "Error"


async def get_settings(group_id):
    settings = temp.SETTINGS.get(group_id)

    if not settings:
        settings = await db.get_settings(group_id)
        temp.SETTINGS[group_id] = settings

    return settings


async def save_group_settings(group_id, key, value):
    current = await get_settings(group_id)
    current[key] = value

    temp.SETTINGS[group_id] = current
    await db.update_settings(group_id, current)


def get_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0

    while size >= 1024.0 and i < len(units) - 1:
        size /= 1024.0
        i += 1

    return "%.2f %s" % (size, units[i])


async def get_shortlink(url, api, link):
    shortzy = Shortzy(api_key=api, base_site=url)
    return await shortzy.convert(link)


def get_readable_time(seconds):
    periods = [('d', 86400), ('h', 3600), ('m', 60), ('s', 1)]
    result = ''

    for name, count in periods:
        if seconds >= count:
            value, seconds = divmod(seconds, count)
            result += f'{int(value)}{name}'

    return result


def get_wish():
    now = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%H")

    if now < "12":
        return "ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ 🌞"
    elif now < "18":
        return "ɢᴏᴏᴅ ᴀꜰᴛᴇʀɴᴏᴏɴ 🌗"
    else:
        return "ɢᴏᴏᴅ ᴇᴠᴇɴɪɴɢ 🌘"


async def get_seconds(time_string):
    value = int(''.join(filter(str.isdigit, time_string)))
    unit = ''.join(filter(str.isalpha, time_string))

    if unit == 's':
        return value
    elif unit == 'min':
        return value * 60
    elif unit == 'hour':
        return value * 3600
    elif unit == 'day':
        return value * 86400
    elif unit == 'month':
        return value * 86400 * 30
    elif unit == 'year':
        return value * 86400 * 365

    return 0
