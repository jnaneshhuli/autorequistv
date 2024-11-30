from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant, FloodWait
from database import add_user, add_group, all_users, all_groups, remove_user
from configs import cfg
import random
import asyncio

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

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Approve Join Requests ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel)
async def approve_and_notify(_, m: Message):
    chat = m.chat
    user = m.from_user

    try:
        # Approve the join request
        await app.approve_chat_join_request(chat.id, user.id)
        add_user(user.id)  # Add the user to the database for broadcasting

        # Send a confirmation message to the user
        confirmation_message = f"""
**Hello {user.mention}, Your request to join {chat.title} has been approved! 🎉**

Subscribe to our YouTube channel for the latest updates:
👉 [JN Entertainment](https://youtube.com/@Jnentertainment.?si=-xZOdUGBD3yxLjgW)

Don't forget to join our backup channel:
👉 [@ROCKERSBACKUP](https://t.me/ROCKERSBACKUP)
"""
        await app.send_message(user.id, confirmation_message)
    except errors.PeerIdInvalid:
        print(f"Unable to send message to {user.first_name}. User has not started the bot.")
    except Exception as e:
        print(f"Error in approving join request: {e}")


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("start"))
async def start(_, m: Message):
    try:
        if m.chat.type == enums.ChatType.PRIVATE:
            add_user(m.from_user.id)
            await m.reply_text(
                f"Hello {m.from_user.mention}!\n\n"
                "**I'm an auto-approval bot. Add me to your groups or channels, and I'll handle join requests automatically.**\n\n"
                "Subscribe to our YouTube channel:\n"
                "👉 [JN Entertainment](https://youtube.com/@Jnentertainment.?si=-xZOdUGBD3yxLjgW)\n\n"
                "Join our backup channel:\n"
                "👉 [@ROCKERSBACKUP](https://t.me/ROCKERSBACKUP)"
            )
        elif m.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            add_group(m.chat.id)
            await m.reply_text("I've been added to your group! Promote me to admin to approve join requests.")
    except Exception as e:
        print(f"Error in start command: {e}")


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Message ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    # Combine all members (users who started the bot + users who sent join requests)
    all_members = all_users() + all_groups()
    lel = await m.reply_text("`⚡️ Processing broadcast...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0

    for member_id in all_members:
        try:
            await m.reply_to_message.copy(int(member_id))  # Send a copy of the original message
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)  # Handle rate limits
            await m.reply_to_message.copy(int(member_id))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(member_id)  # Remove deactivated users
        except errors.UserIsBlocked:
            blocked += 1  # Handle users who blocked the bot
        except Exception as e:
            print(f"Failed to send message to {member_id}: {e}")
            failed += 1

    await lel.edit(f"""
✅ Successfully broadcast to `{success}` members.
❌ Failed to `{failed}` members.
👾 Blocked: `{blocked}` users.
👻 Deactivated: `{deactivated}` users.
""")


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Forward Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m: Message):
    # Combine all members (users who started the bot + users who sent join requests)
    all_members = all_users() + all_groups()
    lel = await m.reply_text("`⚡️ Processing forward broadcast...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0

    for member_id in all_members:
        try:
            await m.reply_to_message.forward(int(member_id))  # Forward the original message
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)  # Handle rate limits
            await m.reply_to_message.forward(int(member_id))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(member_id)  # Remove deactivated users
        except errors.UserIsBlocked:
            blocked += 1  # Handle users who blocked the bot
        except Exception as e:
            print(f"Failed to forward message to {member_id}: {e}")
            failed += 1

    await lel.edit(f"""
✅ Successfully broadcast to `{success}` members.
❌ Failed to `{failed}` members.
👾 Blocked: `{blocked}` users.
👻 Deactivated: `{deactivated}` users.
""")


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Stats Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("stats") & filters.user(cfg.SUDO))
async def stats(_, m: Message):
    user_count = all_users()
    group_count = all_groups()
    total = len(user_count) + len(group_count)
    await m.reply_text(f"""
📊 **Bot Stats**:
🙋‍♂️ Users: `{len(user_count)}`
👥 Groups/Channels: `{len(group_count)}`
🚀 Total: `{total}`
""")


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Run the Bot ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

print("Bot is now running!")
app.run()
