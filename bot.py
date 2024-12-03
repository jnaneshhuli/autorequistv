from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

gif = [    
    'https://graph.org/file/a8a0e8eb4b05399ef9eec.mp4',
    'https://graph.org/file/a8a0e8eb4b05399ef9eec.mp4'
]


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve(_, m: Message):
    chat = m.chat
    user = m.from_user
    try:
        add_group(chat.id)  # Add group to the database
        add_user(user.id)   # Add user to the database
        await app.approve_chat_join_request(chat.id, user.id)  # Approve the request
        img = random.choice(gif)
        await app.send_video(
            user.id,
            img,
            f"Hello {user.mention}, your request to join **{chat.title}** has been approved!\n\n"
            f"📢 **Stay updated with our latest updates**\nJoin our backup channel: @ROCKERSBACKUP"
        )
    except errors.PeerIdInvalid:
        print(f"Cannot send message to {user.id}: PeerIdInvalid.")
    except errors.UserIsBlocked:
        print(f"Cannot send message to {user.id}: User has blocked the bot.")
        remove_user(user.id)  # Clean up database
    except Exception as e:
        print(f"Error in approving join request: {e}")   
 
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("start"))
async def op(_, m :Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id) 
        if m.chat.type == enums.ChatType.PRIVATE:    
            add_user(m.from_user.id)
            await m.reply_text(
                f"Hello {m.from_user.mention}!\n\n"
                "**I'm an auto-approval bot. Add me to your groups or channels, and I'll handle join requests automatically.**\n\n"
                "More Bots:\n"
                "👉 [@Rockers_Bots](https://t.me/Rockers_Bots)\n\n"
                "Join our backup channel:\n"
                "👉 [@ROCKERSBACKUP](https://t.me/ROCKERSBACKUP)"
            )
            
        elif m.chat.type == enums.ChatType.GROUP or enums.ChatType.SUPERGROUP:
            keyboar = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🍿BOT BACKUP CHANNEL🍿", url="http://t.me/ROCKERSBACKUP")
                    ]
                ]
            )
            add_group(m.chat.id)
            await m.reply_text("** Hello start me private for more details @ROCKERSBACKUP**")
        print(m.from_user.first_name +" Is started Your Bot!")

    except UserNotParticipant:
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔎 Check Again 🚀", "chk")
                ]
            ]
        )
        await m.reply_text("**<strong>Hello {}  its good to see u again\n\n⚠️Access Denied!⚠️\n\n🍿Subscribe my youtube channel\n\nLink :- https://youtube.com/@jn2flix?si=mIBelp3uW-NE28sL\n\nAnd join BOT backupChannel\n\nLINK :- ©️@ROCKERSBACKUP\n\nIf you joined click check again button to confirm.</strong>**".format(cfg.FSUB), reply_markup=key)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb : CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
        if cb.message.chat.type == enums.ChatType.PRIVATE:            
            add_user(cb.from_user.id)
            await cb.message.edit("**<strong>I'm an auto approve [Admin Join Requests]({}) Bot.I can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission join here for\n\n🍿 New Movie https://t.me/+D7L-rX9lKA43MGRl\n\n🔞 new adult videos https://t.me/+P-wgbt_2dlU3MTM1\n\nBOT BACKUP CHANNEL :- @ROCKERSBACKUP</strong>**")
        print(cb.from_user.first_name +" Is started Your Bot!")
    except UserNotParticipant:
        await cb.answer("🙅‍♂️ You are not joined to channel join and try again. 🙅‍♂️")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m : Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

print("I'm Alive Now!")
app.run()

