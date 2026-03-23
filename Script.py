class script(object):

    START_TXT = """<b>ɪ ᴀᴍ ᴘᴏᴡᴇʀғᴜʟ ᴀᴜᴛᴏ ғɪʟᴛᴇʀ ʙᴏᴛ. ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴀꜱ ᴀᴜᴛᴏ ғɪʟᴛᴇʀ ᴡɪᴛʜ ʟɪɴᴋ sʜᴏʀᴛᴇɴᴇʀ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ... ɪᴛ'ꜱ ᴇᴀꜱʏ ᴛᴏ ᴜꜱᴇ ᴊᴜsᴛ ᴀᴅᴅ ᴍᴇ ᴀꜱ ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ɪ ᴡɪʟʟ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇʀᴇ ᴍᴏᴠɪᴇꜱ ᴡɪᴛʜ ʏᴏᴜʀ ʟɪɴᴋ ꜱʜᴏʀᴛᴇɴᴇʀ... ♻️</b>""""""

    MY_OWNER_TXT = """★ Name: GGAS Bots
★ Username: @filesprovidebot
★ Country: India Coimbatore
"""

    NOT_FILE_TXT = """ Hello {},

I can't find the <b>{}</b> in my database! 

👉 Google Search and check your spelling is correct.
👉 Please read the Instructions to get better results.
👉 Or not been released yet."""
    
    IMDB_TEMPLATE = """ I Found: <code>{query}</code>

🏷 Title: <a href={url}>{title}</a>
🎭 Genres: {genres}
📆 Year: {year}
🌟 Rating: {rating} / 10
☀️ Languages: {languages}
📀 RunTime: {runtime} Minutes

🗣 Requested by: {message.from_user.mention}
©️ Powered by: <b>{message.chat.title}</b>"""

    FILE_CAPTION = """<i>{file_name}</i>

🚫 ᴘʟᴇᴀsᴇ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ᴄʟᴏsᴇ ʙᴜᴛᴛᴏɴ ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ sᴇᴇɴ ᴛʜᴇ ᴍᴏᴠɪᴇ 🚫"""

    WELCOME_TEXT = """👋 Hello {mention}, Welcome to {title} group! 💞"""

    HELP_TXT = """👋 Hello {},
    
I can filter movie and series you want
Just type you want movie or series in my PM or adding me in to group
And i have more feature for you
Just try my commands"""

    ADMIN_COMMAND_TXT = """<b>Here is bot admin commands 👇


/index_channels - to check how many index channel id added
/stats - to get bot status
/delete - to delete files using query
/delete_all - to delete all indexed file
/broadcast - to send message to all bot users
/grp_broadcast - to send message to all groups
/pin_broadcast - to send message as pin to all bot users.
/pin_grp_broadcast - to send message as pin to all groups.
/restart - to restart bot
/leave - to leave your bot from particular group
/users - to get all users details
/chats - to get all groups
/invite_link - to generate invite link
/index - to index bot accessible channels
/add_prm - to add new premium user
/rm_prm - to add remove premium user
/delreq - to delete join request in db (if change REQUEST_FORCE_SUB_CHANNELS using /set_req_fsub then must need use this command)
/set_req_fsub - to set request force subscribe channel
/set_fsub - to set force subscribe channels</b>"""
    
    PLAN_TXT = """Activate any premium plan to get exclusive features.

You can activate any premium plan and then you can get exclusive features.

Basic premium features:
Ad free experience
Online watch and fast download
No need joind channels
No need verify
No shortlink
Admins support
And more...

Support: @{}"""

    USER_COMMAND_TXT = """<b>Here is bot user commands 👇

/start - to check bot alive or not
/myplan - to check my activated premium plan
/plan - to view premium plan details
/img_2_link - upload image to uguu.se and get link
/settings - to change group settings as your wish
/connect - to connect group settings to PM
/id - to check group or channel id</b>"""
    

